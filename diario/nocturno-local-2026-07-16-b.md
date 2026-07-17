# Nocturno LOCAL — 2026-07-16 (turno B, worker de la PC, Matías durmiendo)

Segundo turno del día (el de las 2:00 hizo el `alert-hold-replay` de galgas — ver
`nocturno-local-2026-07-16.md`). Verifiqué primero que ese turno estuviera entregado
de verdad: branch `nocturno/local-2026-07-16-alert-hold-replay` commit `2ee6552` en
origin + diario + MATI-HQ `5833fd9`. Turno nuevo, no re-disparada ⇒ **UNA tarea nueva**.

## Tarea elegida y por qué
**galgas #14 — que los docs de ENTRADA digan la verdad.** Único ítem listado en un
`QUE_FALTA` sin branch, 100 % offline, y resultó **no ser cosmético**.

Recorrí los 4 `QUE_FALTA` y el estado real de branches. Lo que ordenó la decisión:
- **Todos los bloqueantes duros ya tienen branch**, en los 4 repos. galgas: RX
  (`rx/task08-completo`), SCADA (`web/scada-redler`), OTA A/B (`backend/ota-ab-bucket-firmado`),
  vpp (07-11), energy (07-15), hold (07-16). datalogger: ina219/ecolora, sd-integrity ×2,
  rssi. FrioSeguro: **5 branches sin mergear** — deuda de *deploy*, no de código (avisado
  8 noches; no apilo más). cosechador: P2, todo gated por compra.
- Lo que quedaba de galgas eran **hardware** (#2 galga física, #3 LiPo, #4 reflashear B,
  #7 brownout) o **cloud/deploy** (#6, #8). El #14 era el único software puro sin dueño.
- **La serie de 4 herramientas stdlib seguidas** (rssi/vpp/energy/hold) ya era monocultivo
  declarado por el propio worker. Otra más habría sido cantidad, no calidad.

## Por qué NO era cosmético — el bug de harness
`CLAUDE.md:22` (§2 "Antes de tocar código — LEER EN ESTE ORDEN") manda leer **`README.md`
primero**. Y el README decía:

> `README.md:5` — `## Estado: 🟡 Scaffolding creado, esperando contexto de uso real`
> `README.md:7` — *"Antes de empezar la refactorización, completar `CONTEXTO_USO_REAL.md`"*

…combinado con `CLAUDE.md:24`: *"Si está vacío/incompleto, **detenerse y preguntar**"*.

⇒ **Cualquier agente (o Matías) que arrancara por la puerta del proyecto P0 de octubre se
frenaba solo**, creyendo que es scaffolding sin empezar. Y las dos premisas son falsas:
el sistema está validado E2E en banco, y `CONTEXTO_USO_REAL.md` tiene **203/295 líneas
completas**, no está en blanco. Eso es exactamente "arreglar la capa del harness".

## Drift encontrado (todo verificado con file:línea)
| Afirmación del doc | Realidad |
|---|---|
| `README:5` "Scaffolding, esperando contexto" | 15 migraciones, 13 sketches, bins de OTA, dashboard, A+B posteando en banco |
| `README:12,24` → `docs/PLAN_v2_DEFINITIVO.md` | **No existe.** Es `PLAN_v2_HISTORICO.md`; el vigente es `PLAN_v5_GATEWAY.md` |
| `README:34-36` `backend/config.toml` + `backend/migrations/` | Real: `backend/supabase/…` (ADR-0002 §Actualización) |
| `README:54` "8 carpetas top-level" | **24 entradas** reales |
| `README:53` "sin espacios en paths" | `ejemplo supabase/` **tiene un espacio** (viola su propio ADR-0001) |
| `README:97` workspace `Documents\GALGAS CON SUPABASE\` | Se mudó a `C:\Proyectos\galgas` el 2026-07-07 |
| `README` completo | Nunca nombraba a `act.md` (fuente de verdad) ni a `QUE_FALTA.md` |
| `docs/INDEX.md` | Listaba **8 docs de 14** y **2 ADRs de 5** — faltaba el **plan vigente** v5, `DEPLOYMENT_DREYFUS`, `MAIL_DREYFUS_IT` y `docs/reports/` |
| `CLAUDE.md:23` "PLAN_v3 = plan vigente" | `PLAN_v5_GATEWAY.md` (2026-04-27) dice "Reemplaza PLAN_v4" y define el rol del RX |

## Qué hice — branch `nocturno/local-2026-07-16-b-docs-entrada`
Sale de `main`. **4 archivos, solo docs. Nada borrado, nada movido, cero código.**

| Archivo | Qué |
|---|---|
| `README.md` | Reescrito para decir la verdad. Estado con **tabla de evidencia verificable en el repo**, y separado explícitamente de **lo que relayo de `act.md`/cuartel y no puedo verificar** (banco: A+B posteando, RX heartbeat-only, `DEV_SIMULATE_ADC`/`DEV_BENCH_NO_BATTERY`). Orden de lectura real (QUE_FALTA → act.md → CLAUDE → v5 → v3). Estructura real. Principios que sí rigen (data/ inmutable, append-only, NO mDNS, GTS Root R4). Sección **"Deudas de documentación conocidas"**. |
| `docs/INDEX.md` | Completado: 14 docs + 5 ADRs + `reports/`, agrupados (Planes / Entrega y campo / Proceso y legado). El v5 marcado **VIGENTE**. Nota de que **no hay PLAN_v4** en el repo aunque el v5 dice reemplazarlo. |
| `CLAUDE.md` §2 | Orden de lectura arreglado + gate de `CONTEXTO_USO_REAL` **acotado a lo que realmente bloquea** (UX y rol del RX §11) en vez de a todo el proyecto. |
| `QUE_FALTA.md` | #14 → "EN BRANCH … pendiente de merge" con el resumen y los 2 hallazgos. |

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-16-b-docs-entrada
git diff main --stat                       # -> 4 archivos, solo docs
Get-Content README.md | Select-Object -First 30
```
**Verificación hecha esta noche:** chequeador ad-hoc de links markdown →
**21/21 resuelven a archivos que existen** (0 rotos). Los números del README los conté
contra `git ls-files`: 15 migraciones, 13 sketches, 24 entradas top-level.

> **Nota de honestidad:** mi primer chequeador dio 23 falsos positivos (agarraba refs a
> archivos del proyecto de referencia FrioSeguro dentro de `CLAUDE.md` §9 y texto adentro
> de links). Lo rehíce acotado a links markdown reales. Y en el borrador **yo mismo escribí
> "7 migraciones"** (había leído la lista truncada): al verificar contra `git ls-files`
> salieron **15** y lo corregí **antes** de commitear. No commiteé mi propia versión del
> pecado que vine a arreglar.

## Hallazgos que NO resolví (necesitan device/cloud) — para @firmware / @backend
1. 🔴 **Contradicción de versión de firmware.** El repo dice `FW_VERSION "0.8.1-A-otatest"`
   (`firmware/esp_a_emisor/config.h:18`, ídem B) con `bins_ota_0.8.0/` y `bins_ota_0.8.1/`;
   el cuartel (`PORTFOLIO.md` línea 32, `QUE_FALTA.md` #4) dice OTA **`0.1.2 → 0.1.3`** y
   "A ya está en 0.1.3". **No se puede saber cuál rige sin mirar el device o la tabla
   `firmware_versions`.** Importa: el #4 es "reflashear B" y hoy **no está claro contra qué
   versión**. Lo dejé documentado en los dos lados, sin elegir ganador.
2. 🟡 **La estructura real viola el ADR-0001** (24 entradas vs "8 carpetas"; `ejemplo
   supabase/` con espacio). **No moví ni borré nada** — reordenar carpetas es decisión de
   Matías, y el ADR es una decisión suya que no me toca reescribir de noche. Queda
   documentado en vez de mentido.

## Qué quedó SIN verificar
- **El estado de banco que el README relaya** (A+B posteando, RX heartbeat-only) sale de
  `act.md` §Sesión 5 (abril) y del PORTFOLIO — **no lo verifiqué con hardware**. Por eso en
  el README está explícitamente separado de la tabla de evidencia del repo.
- **`act.md` sigue siendo de abril.** Actualizarlo con lo de mayo→julio es tarea de
  @cronista **con Matías** (yo no sé qué pasó en el banco desde entonces; inventarlo sería
  peor que el drift que arreglé).
- Docs históricos con paths viejos (`docs/CLAUDE_workspace_*`, `prompts/FIRST_PROMPT.md`):
  **no los toqué** — la convención del propio `INDEX.md` dice no editar históricos. Avisados
  en el README.

## ⚠️ Aviso de merge (importante)
**Los dos branches de hoy tocan `QUE_FALTA.md`** (`-alert-hold-replay` el #2; este el #14)
y salen los dos de `main` ⇒ **conflicto probable al mergear el segundo**. Es trivial: son
notas en ítems distintos, se aceptan las dos. Sugerencia: mergear primero el alert-hold
(tiene los 30 tests) y después este.

## Reglas respetadas
Nada borrado ni movido. No toqué firmware, ni schema, ni migraciones, ni
`data/field_captures/` (sagrado — ni lo leí para esto), ni docs históricos. No mDNS (al
contrario: lo reafirmé como decisión cerrada). Sin secretos. Verificación instantánea, sin
compilación ni timeouts. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-16-b-docs-entrada` (pusheado a origin, 1 commit `9b7e002`; sale de `main`).

## Notas para el @director / @verificador / @cronista
- **Rompí el monocultivo a propósito.** Eran 4 herramientas stdlib seguidas (rssi/vpp/energy/
  hold); esta noche tocaba la deuda que ninguna herramienta iba a pagar. El #14 llevaba 9 días
  listado sin dueño porque "arreglar docs" suena a poco — y resultó ser un **bloqueo de
  arranque del proyecto P0 de octubre**.
- **Para @verificador:** el DoD es "cada afirmación del README es verificable contra el repo".
  El cold-start test que corresponde: abrir Claude en `C:\Proyectos\galgas` y decir "¿qué
  hacemos?" — antes se frenaba en "esperando contexto de uso real"; ahora debería ir a
  `QUE_FALTA.md`. Eso ataca también el **hueco #2 del PORTFOLIO** (sistema de agentes sin
  cold-start test).
- **Para Matías, 2 decisiones que no puedo tomar:** (1) **qué versión de firmware rige**
  (0.8.1 vs 0.1.3) — bloquea reflashear B; (2) si se reordena la estructura para cumplir el
  ADR-0001 o se actualiza el ADR a la realidad.
- **9ª noche avisando:** la pila de **FrioSeguro (5 branches)** necesita **~1 h de día**. Es
  deploy/merge, no código. El worker no la toca de noche a propósito.
