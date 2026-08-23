# Nocturno local — 2026-08-23

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la jerarquía).
**Branch:** `nocturno/local-2026-08-23-el-que-se-apaga-no-avisa` (pusheado, `20a5757`).
**Sale de:** `main`. **No depende de ningún otro branch nocturno de frioseguro** —
crea `supabase/functions/_shared/silence.ts` (no pisa el `_shared/retention.ts`
del `07-23-b`) y toca **una línea** de `AdminPanel.jsx` (no choca con el `08-19-b`,
que reescribe `fmtRelative` unas líneas más arriba pero no el mapa de badges).

## TL;DR

> **El modo de falla que más importa —el freezer que se queda sin luz— era el
> único que no avisaba.**

Y no por un bug sutil. Eran tres piezas, cada una razonable por separado, que
juntas dejaban un agujero del tamaño del producto:

| pieza | qué pasaba |
|---|---|
| `devices.is_online` | **es un latch.** Se escribe `TRUE` en tres lugares (INSERT de primer boot, heartbeat cada 60 s, y el trigger `update_device_last_seen` que corre con **cada** lectura) y `FALSE` en **ninguno**. No hay camino de vuelta. |
| `last_seen_at` | se actualiza bien. `v_devices_status` **ya expone** `seconds_since_seen`. La cuenta estaba hecha. **Nadie la consultaba.** |
| los 3 cron jobs | vencimiento de abono + dos limpiezas. Ninguno mira `last_seen_at`. |
| `cron-device-alerts` | se llama *cron* pero es un **webhook sobre `alerts`**: necesita que alguien inserte una fila. **Un equipo sin luz no inserta filas.** |

El resultado en el panel: un equipo muerto hace una semana se veía **`● Online`**,
para siempre. **La ausencia de datos era indistinguible de "todo bien"** — que es
exactamente el escenario en el que el comerciante pierde la mercadería y descubre
que el servicio que paga no le dijo nada. `PLATA.md` vende esto con cinco
palabras: *«el servicio avisa»*.

El número que lo vuelve inequívoco: el firmware manda una lectura **cada 10 s** y
un heartbeat **cada 60 s** (`config.h`). Quince minutos de silencio son **~90
lecturas y ~15 heartbeats perdidos**. No hay ambigüedad que interpretar.

## Tarea elegida y por qué

Por rotación tocaba frioseguro (anoche fueron datalogger y galgas), y la
jerarquía manda **PLATA**, así que coincide.

Dentro del repo seguí el patrón que viene funcionando: **no abrir una auditoría
nueva, tomar un pendiente ya nombrado con su evidencia medida.** La auditoría
`08-14-b cadena-continuidad` dejó nueve hallazgos con dueño, y sobre dos de ellos
escribió esta frase literal:

> *«@backend: R7 y R1 son tuyos, y son la noche entera.»*

Nueve días después seguían sin tocar. Los cinco turnos de frioseguro posteriores
(`08-16-b` tiempo, `08-18` alert-delay, `08-19-b` frescura, `08-21-b` uptime)
fueron todos de firmware y frontend — **ningún branch tocó backend desde el
07-23**. Verificado uno por uno con `git diff --name-only main..<branch>` sobre
los 20 branches nocturnos del repo: ninguno crea un cron ni escribe `is_online`.

Elegí R1+R7 y no otro por tres motivos:

1. **Son la misma tarea.** Apagar `is_online` sin alertar es un cambio de color
   en una pantalla que nadie mira a las 3 de la mañana; alertar sin apagar el
   flag deja el panel diciendo `Online` **al lado** de la alerta que dice lo
   contrario (es el hallazgo R9, «dos verdades contradictorias en la misma
   pantalla»). Hacer uno solo deja el sistema peor que antes.
2. **Es lo que se cobra.** Todo lo demás del repo son mejoras sobre un servicio
   que funciona. Esto es el servicio.
3. **Se puede hacer y verificar entero sin hardware ni nube.** La decisión es
   pura; la I/O es cuarenta líneas.

## Qué hice

**Toda la decisión en una función pura** — `supabase/functions/_shared/silence.ts`.
`planSilenceSweep({devices, openAlerts, nowMs})` devuelve un plan
(`markOffline` / `open` / `escalate` / `resolve` / `skipped`) y no toca la red.
La Edge Function `cron-device-silence` sólo ejecuta el plan. Es el mismo patrón
que `_shared/retention.ts` del `07-23-b`, y es lo que permite tener 28 tests que
corren en 0,2 s sin Supabase.

```
pg_cron (*/5)  ──►  cron-device-silence  ──►  silence.ts (puro)
                          ├─► UPDATE devices SET is_online = false
                          ├─► UPDATE alerts  SET resolved  = true      (el equipo volvió)
                          ├─► INSERT alerts  (device_silence)  ──webhook──► push
                          └─► UPDATE alerts  (warning → critical) ──invoke──► push
```

**Los umbrales, y por qué esos.**

| | valor | por qué |
|---|---|---|
| aviso | **15 min** | ~90 lecturas perdidas. Debajo de eso es un hipo de router, y alertar por eso **es churn** (la misma lección del `08-18`: una falsa alarma por ciclo de descongelamiento sobre exactamente lo que se cobra). |
| crítico | **1 h** | a la hora ya no es "se cayó el WiFi": es mercadería sin vigilar. |
| cadencia | **5 min** | peor caso de aviso: ~20 min desde que el equipo se calla. |

**Seis invariantes, cada una con su test.** Las que más me importaron:

- **S3 — una sola alerta abierta por device.** Sin dedupe, un cron cada 5 min
  sobre un equipo muerto insertaría **288 alertas y 288 pushes por día**. El
  cliente silencia las notificaciones el primer día y el producto se muere.
- **S4 — la alerta se resuelve sola cuando el equipo vuelve.** Sin esto el panel
  queda tapado de alertas viejas y el resumen mensual (`docs/monthly-summary.md`,
  branch `07-13`) contaría incidentes que ya no existen — justo el documento que
  se le manda al cliente para retener el abono.
- **S1 — un equipo que nunca reportó no se alerta.** Es una placa en stock, no un
  servicio caído. Alertar equipos sin instalar es la vía más rápida a que el
  cliente ponga la app en silencio.
- **S6 — ante una fecha inválida o futura, no se afirma nada.** Misma regla que
  `lib/freshness.js` del `08-19-b`: *nunca verde por descarte* — pero tampoco una
  alerta inventada. Se reporta en `skipped` con el motivo, visible en el JSON de
  respuesta y en el log.

**Tres decisiones que podrían haber sido otras** (están argumentadas en el doc):
escalar la alerta existente en vez de abrir una segunda (y **una sola vez**: hay
un test que fija que el segundo barrido no re-escala, si no cada corrida del cron
sería otro push); notificar la escalada con un `functions.invoke` explícito
porque el webhook de Supabase dispara con `INSERT` y una escalada es un `UPDATE`;
y **no agregar ninguna migración** — `idx_alerts_active` (parcial, `WHERE resolved
= FALSE`) ya cubre la única query nueva.

**Una duplicación deliberada, anotada:** `formatSilence()` repite el formato de
`web-dashboard/src/lib/uptime.js` (branch `08-21-b`) — mismo output exacto
(`2d 3h` / `5h 12m` / `7m` / `45s`), porque el push y el panel tienen que decir lo
mismo. Son dos runtimes distintos (Edge/Deno vs. bundle del navegador) en dos
branches sin relación. Los tests fijan el formato de los dos lados, así que no
pueden divergir en silencio; cuando los dos mergeen, colapsarlo es de @frontend.

**Archivos:** `_shared/silence.ts` + `silence.test.ts` (nuevos),
`cron-device-silence/index.ts` (nuevo), `cron-device-alerts/index.ts` (+8 líneas:
`device_silence` en `HANDLED_TYPES` y su rama de copy), `SETUP_CRON_JOBS.sql`
(4º job), `AdminPanel.jsx` (**1 línea**: el badge `📴 Sin señal`, que sin eso
se renderizaba con el slug crudo), `docs/device-silence.md`, `QUE_FALTA.md` #19.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-23-el-que-se-apaga-no-avisa

# 1. La lógica -> 28 pass, 0 fail (0,2 s)
node --test supabase/functions/_shared/silence.test.ts

# 2. Sintaxis de las 3 Edge Functions (Node 24 hace type-stripping nativo)
node --check supabase/functions/_shared/silence.ts
node --check supabase/functions/cron-device-silence/index.ts
node --check supabase/functions/cron-device-alerts/index.ts

# 3. El dashboard
cd web-dashboard
npx eslint src/AdminPanel.jsx    # 2 errores + 1 warning: EXACTAMENTE los de main
npm run build                    # vite, OK en 2,48 s
```

**Verificado esta noche:**
- `node --test` → **28/28 OK**.
- `node --check` en las 3 Edge Functions → OK. Además, chequeo explícito de que
  los 6 símbolos que `index.ts` importa de `silence.ts` **existen** (un typo ahí
  sólo se vería al deployar).
- `npx eslint src/AdminPanel.jsx` → 2 errores + 1 warning. **Mismo resultado con
  el archivo de `main`** (medido con `git stash`): **cero lint nuevo**.
- `npm run build` → OK.
- **Mutación: 10 mutantes, los 10 caen.** No resolver al que vuelve → 2 tests;
  escalar siempre → 1; umbral `<=` en vez de `<` → 1; ignorar el estado del abono
  → 3; romper el dedupe → 4; ignorar `last_seen_at` nulo → 4; aceptar fechas
  futuras → 1; reescribir `is_online` que ya está en `false` → 2; nunca escalar a
  critical → 5; cambiar el formato de minutos → 2.

## Lo que quedó SIN verificar (y por qué)

- **Nada corrió contra Postgres.** No hay `psql` ni Docker en esta máquina. El
  SQL del cron job es una copia estructural de los 3 jobs que ya funcionan, pero
  **su sintaxis no se ejecutó**.
- **Ninguna Edge Function se ejecutó.** Importan `esm.sh` y `Deno.serve`. Se
  verificó sintaxis y símbolos; el camino de I/O (nombres de columna, formas de
  respuesta de PostgREST) es **revisión de código, no ejecución**.
- **El copy no lo vio nadie.** `📴 … dejó de reportar hace 20m` y `⛔ … no reporta
  hace 2h 12m. No hay forma de saber a qué temperatura está.` es lo que el cliente
  lee en el celular a las 3 de la mañana. **@diseno / @comercial antes del primer
  abono.**

## Próximo paso (para Matías, de día)

1. **Mergear** el branch (es independiente; sale de `main`).
2. **Supabase:** `supabase functions deploy cron-device-silence` y
   `... cron-device-alerts` (esta cambió), re-correr `supabase/SETUP_CRON_JOBS.sql`.
3. **Verificar que el Database Webhook de `alerts` INSERT está activo** — de eso
   depende que el push llegue. Si no está, la alerta se crea y se ve en el panel,
   pero no suena el celular.
4. **@tester, con una placa:** desenchufarla, esperar 20 min, y ver los **tres**
   eslabones — `is_online` en `false`, la alerta en el panel, el push en el
   celular. Después enchufarla y ver que la alerta **se cierra sola**.

**Nota de higiene:** el working tree de `frioseguro` tiene bastante sin trackear
(`kit_santacruz/`, `firmware_revival/`, `backup_supabase/`, `BOOTSTRAP_2026-08-19.sql`,
`REVIVAL_2026-08.md`, dos `.zip`). Es trabajo de día de Matías; **no lo toqué ni lo
commiteé** — el `git add` de esta noche fue archivo por archivo. Vale la pena
decidir de día qué de eso entra al repo, sobre todo `BOOTSTRAP_2026-08-19.sql`,
que hoy es el esquema de verdad y está fuera de git.
