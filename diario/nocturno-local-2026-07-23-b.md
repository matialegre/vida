# Nocturno LOCAL — 2026-07-23-b (turno 22:00, worker de la PC, Matías durmiendo)

> Segundo turno del mismo día: el de las 02:00 fue el de galgas/firmware-check
> (`diario/nocturno-local-2026-07-23.md`). Este es el de las 22:00.

## TL;DR para Matías (si leés una sola cosa)
**La retención de datos de FrioSeguro no estaba "por hacer": estaba hecha, rota y sin
que nadie se enterara.** El cron semanal que borra readings viejos mandaba un filtro
`not.in` mal formado (array sin paréntesis) → PostgREST 400 → **borraba 0 filas todos los
lunes**; y si la RPC de protegidos fallaba, el fallback borraba **todo** lo viejo,
incluido el último reading de cada device — justo lo que el header promete conservar.
Además hay evidencia fuerte de que **los 3 crons nunca dispararon en el proyecto nuevo**
(el `app.settings.supabase_url` del repo apunta al Supabase que borraste el 13/07).
Auditado, modelado con oráculo y **25 tests offline (OK)**, 2 de los 4 hallazgos ya
corregidos. Branch: **`nocturno/local-2026-07-23-b-retencion-datos` (frioseguro),
pendiente de merge.**

## Tarea elegida y por qué
**FrioSeguro #12 — retención de datos (pg_cron).** Razones:
- **Es PLATA** (categoría 1 de la jerarquía), y frioseguro venía sin turno desde el
  20/07 — galgas se llevó el turno de las 02:00 de hoy y ya tiene **10 branches**
  esperando merge; datalogger se llevó el 21/07. No apilo donde ya hay pila.
- Era el único ítem de frioseguro **sin branch previo** que fuera 100 % software puro:
  #10, #11 y #18 ya están en branch; #1/#2/#5/#7/#8/#9 son hardware; #6 y #13 tocan
  precios (fuera de mi mandato: nada de decisiones de plata).
- Es **la única pieza del sistema que BORRA datos del cliente**. Un error ahí no tira un
  error: tira una pérdida silenciosa. Y el free tier ya se pausó una vez por tamaño
  (PORTFOLIO 13/07) — la retención es lo que evita que vuelva a pasar.
- Cero hardware, cero nube, cero descargas → sin riesgo de timeout (disciplina 07-07).

## Qué hice — branch `nocturno/local-2026-07-23-b-retencion-datos` (frioseguro)
Sale de `main`, commit `ddf5134`. **6 archivos, 603 inserciones / 45 borradas. No toca
migraciones (ninguna nueva), ni firmware, ni la nube, ni borró una sola fila.**

1. `supabase/functions/_shared/retention.ts` — **lógica PURA** (sin APIs de Deno):
   `cutoffISO`, `formatInList`, `selectProtectedIds` (oráculo fiel de la RPC
   `get_latest_reading_ids`, incluido el desempate del `DISTINCT ON`), `planReadingsCleanup`
   y `planAlertsCleanup`. Comparación por `Date.parse`, no por string: PostgREST devuelve
   `+00:00` y `toISOString()` devuelve `Z` — compararlos como texto da resultados falsos.
2. `_shared/retention.test.ts` — **25 tests** con `node --test` (Node 24, type stripping
   nativo; sin Deno, sin red). Fijan las 3 invariantes que se le cobran al cliente:
   **R1** nada más nuevo que el cutoff se borra · **R2** nunca se borra el ÚLTIMO reading
   de un device (equipo apagado 8 meses = último estado conocido que el dashboard muestra)
   · **R3** nunca se borra una alerta sin resolver. Más bordes: cutoff exacto, 1 ms antes,
   device con un solo reading, y que el plan sea una **partición** de las filas.
3. `cron-cleanup-readings/index.ts` — **H1 y H2 corregidos** (abajo), ahora delega toda la
   decisión al módulo puro.
4. `cron-cleanup-alerts/index.ts` — usa el cutoff compartido (era 180 días duplicado a mano).
5. `docs/retention.md` — auditoría + runbook del día con los SQL/curl exactos.
6. `QUE_FALTA.md` #12 → nota EN BRANCH con los 4 hallazgos.

### Los 4 hallazgos
| | Qué | Estado |
|---|---|---|
| 🔴 **H1** | `.not("id","in",protectedIds)` con array pelado → supabase-js interpola `not.in.1,2,3`, PostgREST exige `not.in.(1,2,3)` → 400 → **la limpieza semanal borraba 0 filas**. El comentario del código afirmaba exactamente lo contrario. | **CORREGIDO** (`formatInList`, que además rechaza ids no enteros: la lista se interpola en la URL) |
| 🟠 **H2** | Si la RPC de protegidos fallaba, solo logueaba un warning y borraba **todo** lo >90 días, incluido el último reading de cada device (violación silenciosa de R2). | **CORREGIDO**: aborta 500 sin borrar nada y dice cómo crear la RPC |
| 🟠 **H3** | `app.settings.supabase_url` se define en **un solo lugar** del repo (`migration_cron_jobs.sql:184`) y apunta a `nwugnhsktcihusopfldu` — **el proyecto que eliminaste el 13/07**. En `cjdluhemschrynijzvap`, si no se re-corrió, `current_setting` da NULL → `net.http_post(url := NULL)` → **los 3 crons nunca corrieron**. | **NO corregido** (necesita la service_role real): paso 1 del runbook, con el SQL que lo confirma en 10 s |
| 🟡 **H4** | `--project-ref` de deploy apuntando al proyecto muerto. | Corregido en las 2 funciones tocadas; queda drift en ~12 archivos más |

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-07-23-b-retencion-datos
node --test supabase/functions/_shared/retention.test.ts   # -> 25 pass / 0 fail
node -e "import('./supabase/functions/cron-cleanup-readings/index.ts').catch(e=>console.log(e.code))"
#   -> ERR_UNSUPPORTED_ESM_URL_SCHEME  (parseó bien; solo falta el runtime Deno)
git diff main --stat    # -> 6 archivos, 603+/45-
```
**Resultado de esta noche:** 25/25 tests OK; ambas Edge Functions parsean.

## Qué quedó SIN verificar (día, con nube — todo está en `docs/retention.md`)
1. **H3**: correr los 3 SELECT del paso 1 del runbook (`current_setting`, `cron.job`,
   `cron.job_run_details`). Es el chequeo más barato y el de mayor impacto de la noche:
   dice si la retención + el vencimiento de suscripciones vienen muertos hace 10 días.
2. Si H3 se confirma: `ALTER DATABASE ... SET app.settings.*` con la key nueva (a mano,
   NO commiteada) + re-correr `SETUP_CRON_JOBS.sql`.
3. Deploy de las 2 funciones + smoke curl. Con ~10 días de datos, la corrida correcta
   debe devolver **`deleted: 0`** y `protected_count` = cantidad de devices. Si devuelve
   `protected_count: 0`, la RPC no está → parar y revisar antes de seguir.
4. Confirmar H1 contra PostgREST real (los 2 curl del paso 5: 400 vs 200).

## Observaciones para el día (no tareas mías)
- **`cron-device-alerts` existe como función pero ningún SQL del repo la agenda**
  (`cron.schedule` aparece 3 veces y ninguna es esa). O se agenda o sobra.
- **`SETUP_COMPLETO.sql:~899` tiene un secret hardcodeado en formato nuevo**
  (`sb_secret_...`) dentro del trigger `notify_alert_push`. Es del proyecto viejo (muerto),
  pero **`tools/scan_secrets.py` (el scanner ya mergeado del 10/07) NO lo caza: verifiqué
  sus `PATTERNS` y solo tiene `sbp_[0-9a-f]{40}`, JWT, Telegram, AWS y private keys — no
  hay ningún patrón `sb_secret_`.** Es un punto ciego justo en el formato de key que
  Supabase usa ahora. Fix de 3 líneas (un patrón más + un test), pero es del scanner, no
  de la retención: no lo mezclo con este branch.
- Tablas que crecen **sin ninguna retención**: `ota_updates`, `push_subscriptions`,
  `payments`. No urgente con 2 placas; sí antes de 20 abonos.
- frioseguro quedó con **6 branches nocturnos sin mergear** (07-11-b, 07-13, 07-14,
  07-18, 07-20 + este; los de 07-10-b y 07-12 ya están en main). Igual que galgas: la
  sesión de drenaje con
  @verificador es en sí misma la tarea más rentable del portfolio ahora mismo.

## Reglas respetadas
Solo software backend + docs. Nada borrado, nada deployado, **ninguna migración nueva**
(deliberado: los cambios de base del runbook son manuales para que nadie los corra por
accidente con la key equivocada), `data/field_captures` de galgas ni tocado. Sin
compilaciones ni descargas pesadas. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-23-b-retencion-datos` (frioseguro, pusheado a origin; sale de
`main`, commit `ddf5134`; commit del branch `34ca9d3`).

## Notas para @verificador / @backend / @director
- **@verificador:** DoD = *"lo que la función borra es exactamente lo que dice el oráculo,
  y ninguna invariante R1/R2/R3 se puede violar"*. Ataques sugeridos: (a) correr los 25
  tests y agregar casos raros (timestamps con offset `-03:00`, device con 10k readings,
  ids gigantes); (b) buscar un camino en `cron-cleanup-readings` donde se borre algo que
  `planReadingsCleanup` conserva; (c) atacar `formatInList` (¿entra algo que no sea un
  entero en la URL?); (d) revisar si el fail-safe de H2 puede dejar la base creciendo sin
  que nadie lo note — hoy solo loguea, no avisa a nadie.
- **@backend (día):** el paso 1 del runbook son 3 SELECT; hacelo antes que cualquier otra
  cosa de frioseguro. Si H3 se confirma, `cron-subscription-expiry` tampoco corrió → hay
  suscripciones que deberían estar vencidas y no lo están.
- **@director:** 2 turnos hoy (02:00 galgas, 22:00 frioseguro). Ambos repos P0/P1 tienen
  la misma enfermedad: **branches nocturnos que se apilan sin drenar** (galgas 10,
  frioseguro 8). El cuello de botella ya no es producir trabajo de noche: es verificarlo
  y mergearlo de día.
