# Nocturno LOCAL — 2026-07-11-b (worker de la PC, 2ª pasada, Matías durmiendo)

> Esta noche ya había corrido un nocturno (`nocturno-local-2026-07-11.md`,
> auditoría del umbral v_pp de galgas). Soy la **2ª pasada** → variante `-b`,
> tarea distinta y de mayor prioridad de portfolio.

## Tarea elegida y por qué
**FrioSeguro #11 — Resumen mensual automático por cliente** (backend, software puro).
Es **PLATA** (prioridad #1 del portfolio, por encima de octubre): el resumen mensual
es el artefacto que **retiene el abono** — "este mes: 2 alertas, 0 pérdidas, la
mercadería estuvo protegida". Sin él, el comerciante no ve el valor y da de baja.

Recorrí los 4 `QUE_FALTA` + los 7 nocturnos previos + los branches nocturnos de los
4 repos. Jerarquía **PLATA y UNIVERSIDAD primero**:
- **galgas** (P0 octubre) ya tuvo su nocturno hoy (v_pp) → no repito, y octubre es 2º.
- **datalogger** (P0 pre-Dreyfus) ya tiene 4 branches nocturnos esperando merge
  (ina219-ecolora, ecolora-fixes, sd-integrity, rssi-calib) → no apilo más.
- **FrioSeguro (PLATA)**: los ítems de software no-tocados eran #10 (dashboard mobile,
  frontend grande sin dirección de diseño = especulativo de noche), **#11 (resumen
  mensual, backend, acotable y verificable)**, #12 (retención pg_cron, trivial). Elegí
  **#11**: alto valor comercial, alcance quirúrgico, y **la lógica se verifica 100%
  offline**. No estaba en ningún branch.
- **cosechador** es P2 (arranca recién cuando datalogger cumple DoD) → no corresponde.

Converge además con la doctrina backend del ERP (una sola fuente de verdad de la regla
de negocio, testeada) y con PLATA.md (retención = métrica de abonos vivos).

## Qué hice — branch `nocturno/local-2026-07-11-b-resumen-mensual` (sale de `main`)
Software **aditivo**. No toqué firmware, ni schema existente, ni datos. La regla de
negocio vive **una sola vez** y se importa; no se duplica.

| Archivo | Qué |
|---|---|
| `supabase/functions/_shared/monthly_summary.ts` | **Lógica pura, sin imports.** `buildMonthlySummary()` agrega las filas del mes (`readings`/`alerts`/`door_events`/`power_events` + config del device) → objeto con temperatura (avg/min/max/excursiones vs `temp_max`), alertas (total/sin resolver/por tipo/por severidad), puertas, cortes de luz, **cobertura horaria** del monitoreo, y veredicto **"0 pérdidas"** (= sin alerta temp `critical`). `renderSummaryText()` → texto castellano para WhatsApp/dashboard. `monthWindow()` calcula la ventana del mes en hora **AR (UTC−3)**. Nombres de columna tomados del schema real (`SETUP_COMPLETO.sql`), no de memoria. |
| `supabase/functions/_shared/monthly_summary.test.ts` | **13 checks** (`node --test`): ventana de mes (AR, cruce de año, UTC, mes inválido), formato de duración, mes sano (0 pérdidas), excursión + alerta crítica (veredicto baja), fallback `temp_avg`→sondas, sin datos de temp (no crashea), puertas+cortes, cobertura parcial (24h/744h=3.2 %), device sin actividad, defaults de name/location. |
| `supabase/functions/cron-monthly-summary/index.ts` | **Edge function (glue, deploy-pendiente)** que sigue el patrón exacto de las cron functions existentes (Deno + service role): lee la DB del mes anterior por device activo, **importa** la lógica pura, y hace upsert en `monthly_summaries`. Acepta body `{year,month}` para regenerar un mes puntual. |
| `supabase/migration_monthly_summaries.sql` | Tabla cache `monthly_summaries` (UNIQUE device+año+mes, JSON + texto). Estilo idéntico a las migraciones del repo. NO borra nada. |
| `supabase/SETUP_CRON_JOBS.sql` | Agregado el job `cron-monthly-summary` (1ro de mes 05:00 AR) — aditivo, no toca los 3 jobs previos. |
| `docs/monthly-summary.md` | Arquitectura, decisiones, salida real de ejemplo, pasos de deploy, convergencia. |
| `QUE_FALTA.md` (#11) | Anotado "EN BRANCH … pendiente de merge" con el resumen. |

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-07-11-b-resumen-mensual

# 1) Tests de la lógica (Node 24 strippea los tipos TS)
cd supabase\functions\_shared
node --test                 # -> tests 13 / pass 13 / fail 0

# 2) Sintaxis de los 3 .ts (incluye la edge function)
cd ..
node --check _shared/monthly_summary.ts
node --check _shared/monthly_summary.test.ts
node --check cron-monthly-summary/index.ts     # -> los 3 OK
```
**Resultado obtenido esta noche** (Node v24.14.0): `node --test` → **13/13 pass**;
`node --check` → **3/3 OK**. Salida real del texto (datos sintéticos de un mes):

```
📊 FrioSeguro · Resumen de Julio 2026
Carnicería Don José — Av. Alem 1200

• 2 alertas (1 temperatura, 1 puerta abierta) — todas resueltas
• Temperatura: prom -18.2 °C, máx -11.0 °C (objetivo ≤ -15.0 °C)
• 0 pérdidas: la mercadería estuvo protegida todo el mes 🧊
• Cobertura del monitoreo: 50.1 %
• Puertas: 1 apertura, 1 h 12 min en total
• Cortes de luz: 1 (18 min, cubierto por el sistema)
```

## Qué quedó SIN verificar (necesita Supabase — @backend / Matías de día)
- **Deploy real**: aplicar `migration_monthly_summaries.sql` + `supabase functions
  deploy cron-monthly-summary --project-ref <REF>` + re-correr `SETUP_CRON_JOBS.sql`.
  La edge function y la migración **no se pueden ejecutar offline** (necesitan la nube);
  quedan verificadas solo por `node --check` (sintaxis) — son glue mecánico alrededor
  de la lógica pura que sí está testeada.
- **Prueba con datos reales** de un device: `POST /functions/v1/cron-monthly-summary`
  con `{"year":2026,"month":6}` y mirar el `summary_text` contra la realidad del mes.
- **Render en dashboard/WhatsApp** del `summary_text` (se cruza con #10/#13/#16).

## Reglas respetadas
Nada borrado. No toqué firmware, ni schema existente, ni datos, ni migraciones previas
(solo agregué una nueva). No mDNS (no aplica). No se copiaron secretos. Software aditivo
en branch nuevo salido de `main`. Saqué del stage 2 `.pyc` de `__pycache__` que git había
capturado (no van al repo). Sin compilación pesada: verificación instantánea (Node puro),
sin timeouts. El branch **no se mergea** hasta que @verificador lo revise y se haga el
deploy — pero la lógica pura + tests son mergeables ya (no dependen de la nube).

## Branch
`nocturno/local-2026-07-11-b-resumen-mensual` (pusheado a origin, 1 commit). Sale de `main`.

## Nota para el @director
- **2 nocturnos la misma noche (07-11 y 07-11-b)**: el primero fue la rutina cloud
  (galgas v_pp); este es la pasada local. Sin colisión — tareas y repos distintos.
- **FrioSeguro acumula deuda de deploy**, no de código: #4 (secret-scan, 07-10-b) y ahora
  #11 dejan wiring listo que **necesita una sesión de Supabase de día** (rotar claves,
  aplicar migraciones, deployar functions). Sugerencia: agrupar un "bloque backend
  FrioSeguro" de ~1h con Matías para bajar los dos de una.
