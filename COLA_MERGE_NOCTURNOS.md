# COLA DE MERGE — branches nocturnos pendientes de drenar

> Generado 2026-07-24 (turno nocturno local, worker de la PC) con datos **reales de git**
> (`merge-tree --write-tree`, `rev-list`, `merge-base`) tomados esa noche.
> **Por qué existe:** los últimos ~8 nocturnos vienen diagnosticando lo mismo — *"el cuello
> de botella ya no es producir trabajo de noche, es drenarlo de día con @verificador"*.
> Hoy hay **25 branches nocturnos útiles sin mergear** (26 ramas, una subsumida) repartidos
> en 4 repos, y **ningún diario individual sabe cómo se comporta su branch contra el main de
> HOY ni contra los otros branches**. Este doc es esa vista cruzada: el plan de drenaje.
>
> **Este es el análisis de la noche, no un branch nuevo** (hubiera sido el #27). Es 100 %
> software/análisis, no destructivo, no toca ninguno de los 4 repos.

> ## ✅ ACTUALIZACIÓN (2026-07-29) — el estado fresco y la buena noticia
> Reporte de HOY: **`COLA_MERGE_STATUS_2026-07-29.md`** (34 branches). El tool
> `tools/merge_queue_status.py` fue **corregido y extendido** esta noche:
> 1. **Bug del conteo de conflictos:** antes reportaba "3 archivos en conflicto" donde había
>    **1** — metía las 2 líneas informativas de git (`Auto-merging…`, `CONFLICT (content):…`)
>    como si fueran archivos. Ahora corta en la línea en blanco → conteo real.
> 2. **Clasificación doc vs código:** cada conflicto/colisión se etiqueta `[SOLO docs]`,
>    `[codigo]` o `[doc+codigo]`. **Hallazgo que des-asusta la cola:** de los **8 CONFLICTO,
>    los 8 son SOLO `QUE_FALTA.md`** (0 tocan firmware/código); y de 14 `REVISAR-STALE`, 10
>    son solo docs. El atasco entero es de **bitácora, no de código**: se resuelve tomando
>    ambos lados del `.md`, no es riesgo. **Orden de drenaje sugerido:** 9 `LIMPIO-ADITIVO`
>    primero (mecánico) → 10 stale-docs (revisión de 1 min) → 8 conflictos-docs (tomar ambos)
>    → dejar para el final los pocos que tocan código (datalogger `ecolora-fixes` doc+código,
>    galgas `rx-deuda` con binarios, frioseguro `resumen-mensual` código). Correr
>    `python tools/merge_queue_status.py` para el estado del momento.
>
> ## ⚠️ CORRECCIÓN (2026-07-27) — leer ANTES que lo de abajo
> Este doc es del **07-24 y ya drifteó** (le faltan branches, arrastra clasificaciones viejas).
> **Reemplazado por un tool que lo regenera con git en vivo:** `tools/merge_queue_status.py`
> (reporte fresco en `COLA_MERGE_STATUS_2026-07-27.md`). **Corrección de fondo:** la alarma de
> abajo *"los 8 branches STALE de datalogger borrarían `misiones/`"* **es FALSA** — surgió de medir
> con `git diff main..branch` (two-dot), que muestra las adiciones POSTERIORES de main como falsos
> "borrados". Con la métrica correcta (merge 3-way real: `merge-tree --write-tree` → diff vs main),
> **ninguno de los 32 branches borra un solo archivo** (verificado esta noche). Los 8 de datalogger
> mergean **limpios**; 7 quedan como `REVISAR-STALE` (modifican firmware/QUE_FALTA desde una base
> vieja — revisar, no tóxicos) y 1 es `SUBSUMIDO`. Correr `python tools/merge_queue_status.py` para
> el estado de HOY antes de drenar. (Lo de abajo se conserva como registro del análisis del 07-24.)

## TL;DR para Matías / @verificador (si leés una sola cosa)
1. **galgas (10 branches)** y **cosechador (1)** están **sanos**: salen del mismo main, 0
   commits atrás, mergean limpio. Drenaje mecánico — el único cuidado es `QUE_FALTA.md`
   (lo tocan casi todos → conflicto **garantizado** después del primer merge de cada repo:
   resolver a mano, no es un error). **Empezá por acá: es la victoria más barata.**
2. **datalogger (8 branches)** ✅ **TRIADO (07-25/-25-b/-26)**: eran STALE (6-8 commits atrás,
   nunca rebaseados) y **los 8 borrarían `misiones/`** — `merge-tree` "limpio" era engañoso.
   Ya ninguno se mergea: los deliverables útiles se extrajeron limpios sobre main vivo en
   **3 branches aditivos** (`07-25-sd-integrity-rebase`, `07-25-b-ina219-extract`,
   `07-26-stale-cluster-extract`; ssid-casing a rehacer sobre main). **Acción restante = HUMANA:
   mergear esos 3 + borrar los 8 viejos. No queda triaje nocturno pendiente en datalogger.**
3. **2 pares redundantes ya detectados** (no drenar los dos):
   - frioseguro `07-11-b` está **subsumido** en `07-13` (es su ancestro) → mergear **solo 07-13**.
   - datalogger `07-09-sd-integrity` y `07-15-sd-integrity`: **✅ RESUELTO 07-25 — ninguna se
     mergea** (ambas borran todo `misiones/`, que main construyó después). El entregable se
     extrajo limpio en `nocturno/local-2026-07-25-sd-integrity-rebase`. Drenar ese; descartar las dos.
4. **1 branch arrastra basura**: galgas `07-09` trae **6 binarios de build** (`.bin/.elf/.map`,
   ~144k líneas). Sacarlos del árbol antes de mergear (o cherry-pick solo del source).

---

## Estado por repo (números reales al 2026-07-24)

| Repo | Branches pend. | Main (commits) | Salud | Acción global |
|---|---|---|---|---|
| **galgas** | 10 | 2 | ✅ sano (todos base 07-07, 0 atrás, merge limpio) | drenar en orden; resolver `QUE_FALTA.md` a mano |
| **datalogger** | 8 | 10 | 🔴 STALE (6-8 commits atrás) | **rebasear c/u** antes de mergear |
| **frioseguro** | 8 (7 útiles) | 13 | 🟡 mixto (2 viejos conflictúan, 1 subsumido) | drenar los nuevos; decidir los 2 viejos |
| **cosechador** | 1 | 2 | ✅ sano | drenar directo |

Convención de la columna **merge**: `LIMPIO` = `merge-tree` sin conflictos contra el main de
hoy · `STALE-N` = mergea limpio pero está N commits atrás (revisar/rebasear) · `CONFLICTO` =
conflicto textual real.

---

## galgas — ✅ drenaje mecánico (P0 octubre)
Todos salen de `main` (07-07), **0 commits atrás**, **merge LIMPIO**. Orden sugerido: docs
primero (bajan ruido), luego los modelos+tests, RX al final (el más pesado).

| # | Branch | Qué | Archivos / líneas | Nota |
|---|---|---|---|---|
| 1 | `nocturno/local-2026-07-16-b-docs-entrada` | Docs de entrada (README/INDEX/CLAUDE/QUE_FALTA) | 4 / +152-99 | — |
| 2 | `nocturno/local-2026-07-17-linaje-firmware` | Linaje/estado de firmware (act.md, ESTADO_FIRMWARE) | 3 / +214-4 | — |
| 3 | `nocturno/local-2026-07-22-readme-drift` | Fix drift README vs código | 2 / +57-45 | — |
| 4 | `nocturno/local-2026-07-11-vpp-threshold-audit` | Modelo+tests umbral Vpp de alerta | 4 / +683 | test: `tools/test_vpp_threshold_audit.py` |
| 5 | `nocturno/local-2026-07-15-energy-budget` | Presupuesto de energía del nodo galga | 4 / +700 | test: `tools/test_energy_budget.py` |
| 6 | `nocturno/local-2026-07-16-alert-hold-replay` | Modelo hold/replay de alertas | 4 / +720 | test: `tools/test_alert_hold_replay.py` |
| 7 | `nocturno/local-2026-07-19-rx-detection-replay` | Modelo detección RX (replay) | 4 / +683 | test: `tools/test_rx_detection_replay.py` |
| 8 | `nocturno/local-2026-07-20-b-ota-decision-model` | Modelo decisión OTA A/B | 4 / +554 | test: `tools/test_ota_decision_model.py` |
| 9 | `nocturno/local-2026-07-23-firmware-check-edge` | Edge Function firmware-check + tests | 5 / +553 | test: `logic.test.ts` (Deno/node) |
| 10 | `nocturno/local-2026-07-09-rx-deuda-verificador` | RX receptor (Task 08) firmware + migración set_config | 12 / +144775-90 | ⚠️ **incluye 6 binarios de build** en `build/esp_rx_371/` — sacarlos antes de mergear |
| 11 | `nocturno/local-2026-07-27-readme-drift` | Fix README raíz que mentía (scaffolding/ruta vieja/pointer roto) vs estado E2E real | 2 / +59-75 | LIMPIO · solo docs, sin tests; el más barato de drenar (07-27) |

**Cuidado transversal galgas:** los 10 tocan `QUE_FALTA.md`. Tras el primer merge, los otros 9
conflictúan ahí → resolución trivial a mano (quedarse con la unión de los ítems marcados
"EN BRANCH"). No es un bug del branch.

---

## datalogger — 🔴 STALE: rebasear antes de mergear (P0 octubre)
Main tiene **10 commits**; **los 8 branches salen de 07-07/07-08 y están 6-8 atrás** — nunca
se rebasearon. El "+X-1591" de casi todos es porque el branch **no tiene** cambios que el main
de día ya incorporó. `merge-tree` los da limpios, pero es estado viejo del firmware:
**`git rebase main` + re-correr tests por branch**; si el rebase toca `firmwares/pico2w-node/*`
que main ya cambió, revisar a mano.

| Branch | Qué | Atrás | Nota |
|---|---|---|---|
| ~~`nocturno/local-2026-07-21-eco-schedule-model`~~ | Modelo duty-cycle nodo ECO + 23 tests | 6 | 🛑 **NO MERGEAR** — borra todo `misiones/` (ver ✅ RESUELTO 07-26). Extraído limpio en `07-26-stale-cluster-extract` |
| ~~`nocturno/local-2026-07-19-b-rv1-mesh-model`~~ | Modelo ruteo mesh RV1 + tests | 6 | 🛑 **NO MERGEAR** — ídem. Extraído en `07-26-stale-cluster-extract` |
| `nocturno/local-2026-07-17-b-ssid-casing` | Casing SSID `Gimap`/`GIMAP` + wifi_nets | 6 | 🟡 **NO extraído** — `wifi_nets.py` es firmware; main ya tiene WiFi manager (513c79b). Rehacer con integración, no mergear (ver ✅ RESUELTO 07-26) |
| ~~`nocturno/local-2026-07-15-sd-integrity`~~ | Integridad SD (seq/gaps) + tests | 6 | 🛑 **NO MERGEAR** — borra todo `misiones/` (ver ✅ RESUELTO abajo). Reemplazado por `07-25-sd-integrity-rebase` |
| ~~`nocturno/local-2026-07-10-rssi-calib`~~ | Calibración RSSI↔distancia + tests | 6 | 🛑 **NO MERGEAR** — ídem. Extraído en `07-26-stale-cluster-extract` |
| ~~`nocturno/local-2026-07-09-sd-integrity`~~ | Integridad SD (versión previa) | 6 | 🛑 **NO MERGEAR** — ídem 07-15. Reemplazado por `07-25-sd-integrity-rebase` |
| ~~`nocturno/local-2026-07-08-ecolora-fixes`~~ | Fixes eco-LoRa (grande) | 8 | 🛑 **NO MERGEAR** — borra todo `misiones/` (−4266). Driver INA219 extraído en `07-25-b-ina219-extract` (ver ✅ RESUELTO). |
| ~~`nocturno/local-2026-07-07-ina219-ecolora`~~ | Driver INA219 + eco-LoRa (base) | 8 | 🛑 **NO MERGEAR** — subsumido en 07-08 (es su ancestro). Reemplazado por `07-25-b-ina219-extract`. |

**✅ RESUELTO (nocturno 2026-07-25) — sd-integrity 07-09/07-15:** se diffearon con git real.
Hallazgo grave: **ninguna de las dos es mergeable.** Además del entregable, cada una **borra el
subsistema `misiones/` entero** (~1591 líneas: selector, mision_baja/media/dreyfus/lab, registro,
test_misiones, lab_rx) porque se cortaron de un main viejo — y **main tiene esas 6 commits
justamente construyendo ese subsistema** (taxonomía 4-dataloggers, selector sin cable, WiFi
manager, fix de flash de misiones, desacople SD en core 1). `merge-tree` las daba "LIMPIO" pero
mergear cualquiera **intentaría nukear el núcleo del firmware actual** — el peligro STALE exacto
que este doc advertía. **Acción tomada:** el entregable real (`tools/sd_integrity.py` +
`tests/test_sd_integrity.py`, stdlib puro, no existían en main, 100% aditivo) se extrajo de la
versión más completa (07-15) sobre el main de HOY en el branch limpio
**`nocturno/local-2026-07-25-sd-integrity-rebase`** (29 tests OK offline). → **Drenar ese branch;
NO drenar 07-09 ni 07-15** (borrar sus ramas al confirmar). Neto: 2 branches tóxicos → 1 limpio.

**✅ RESUELTO (nocturno 2026-07-25-b) — eco-LoRa 07-07/07-08:** diffeados con git real. **Confirmado
el mismo patrón tóxico:** `07-07` es **ancestro de** `07-08` (subsumido) y `07-08` **borra 41
archivos, entre ellos todo `misiones/` (−4266)** porque salió de `75bd118` (main viejo) → mergear
cualquiera **nukearía el firmware vivo**. La única joya cleanly-extractable era `ina219.py` (driver
INA219 del DoD #4, dep solo `machine`, 100% aditivo, no existía en main): extraído byte-fiel sobre
el main de HOY + test offline nuevo (13 tests OK) en **`nocturno/local-2026-07-25-b-ina219-extract`**.
`eco.py`/`power_monitor.py`/ventana-RX (item #3) quedan SIN extraer — entrelazados con firmware que
main cambió; **rehacer sobre main, no mergear los viejos.** → **Drenar ese branch; NO drenar 07-07 ni
07-08** (borrar sus ramas al confirmar). Neto: 2 branches tóxicos → 1 limpio.

**✅ RESUELTO (nocturno 2026-07-26) — los 4 branches STALE restantes:** diffeados con git real.
**Mismo patrón tóxico en los 4**: `07-21-eco-schedule`, `07-19-b-rv1-mesh`, `07-17-b-ssid-casing`
y `07-10-rssi-calib` salen de `8784075` (main viejo) y **los 4 borrarían todo `misiones/`**.
3 de ellos son **modelos+tests offline aditivos** (solo stdlib, no existen en main): extraídos
byte-fiel sobre el main de HOY en **`nocturno/local-2026-07-26-stale-cluster-extract`** —
`eco_schedule_model` (23 tests, DoD #3), `rv1_mesh_model` (32, DoD #6), `rssi_calibrate` (27,
DoD #7) + sus 3 docs. **82 tests OK offline.** El 4º, `ssid-casing/wifi_nets.py`, es un **módulo
de firmware** que main ya cubre con el WiFi manager (513c79b) → **NO extraído** (sería código
muerto; rehacer con integración sobre main, no mergear el viejo). → **Drenar el branch limpio;
NO drenar 07-21/07-19-b/07-10; cerrar 07-17-b.** Neto: 4 branches tóxicos → 1 limpio.

**🎯 Con esto el cluster STALE de datalogger (8 branches) queda 100% TRIADO** — los 8 borraban
`misiones/`; 7 reemplazados por branches aditivos limpios (`07-25-sd-integrity-rebase`,
`07-25-b-ina219-extract`, `07-26-stale-cluster-extract`), 1 (ssid-casing) documentado como
"rehacer sobre main". Ningún branch STALE de datalogger es ya una trampa oculta.

---

## frioseguro — 🟡 mixto (P1 = PLATA, categoría 1 de la jerarquía)
Los **nuevos** (base ≥07-14) mergean limpio; los **dos viejos** (07-11-b, 07-13) son
pre-reconstrucción del 13/07, están 10 atrás y conflictúan en `QUE_FALTA.md`.

| Branch | Qué | Atrás | Merge | Acción |
|---|---|---|---|---|
| `nocturno/local-2026-07-26-b-provision-device` | Generador de config por cliente (`provision_device.py`) — la otra mitad del pipeline; se niega a emitir si no pasa el linter | 0 | LIMPIO | drenar (aditivo: 2 tools + doc + gitignore; 36 tests OK) |
| `nocturno/local-2026-07-24-scan-secrets-sbkeys` | Scanner secrets esquema `sb_secret_/sb_publishable_` | 0 | LIMPIO | drenar (chico, tests verdes) |
| `nocturno/local-2026-07-23-b-retencion-datos` | Retención datos cron + oráculo + 25 tests | 0 | LIMPIO | drenar |
| `nocturno/local-2026-07-20-door-alert-model` | Modelo alerta de puerta + tests | 0 | LIMPIO | drenar |
| `nocturno/local-2026-07-18-alert-model` | Modelo de alertas + tests | 1 | LIMPIO | drenar |
| `nocturno/local-2026-07-14-vista-estabilidad-comercio` | Vista estabilidad comercio (dashboard) | 2 | LIMPIO | drenar (rebase trivial) |
| `nocturno/local-2026-07-13-resumen-mensual-fixes` | Resumen mensual #11 + fixes @verificador | 10 | 🔴 CONFLICTO `QUE_FALTA.md` | **contiene al 07-11-b**; rebasear + resolver + decidir si el feature sigue vigente |
| ~~`nocturno/local-2026-07-11-b-resumen-mensual`~~ | (subsumido: es ancestro de 07-13) | 10 | 🔴 CONFLICTO | **NO drenar por separado** — ya está dentro de 07-13 |

---

## cosechador — ✅ (P2)
| Branch | Qué | Atrás | Merge |
|---|---|---|---|
| `nocturno/local-2026-07-18-modelo-energia` | Modelo energía harvester (Tablas 5/6 del paper) + 18 tests | 0 | LIMPIO |

---

## Los 4 peligros transversales (lo que un merge apurado rompería)
1. ✅ **datalogger stale (6-8 commits atrás × 8 branches) — TRIADO (07-25 / -25-b / -26).**
   Los 8 borraban `misiones/` (`merge-tree` "limpio" ≠ seguro). Ya NO se mergea ninguno: 7
   reemplazados por 3 branches aditivos limpios (`07-25-sd-integrity-rebase`,
   `07-25-b-ina219-extract`, `07-26-stale-cluster-extract`), 1 (ssid-casing) a rehacer sobre main.
   **Lo que queda es acción humana: mergear esos 3 branches limpios + borrar los 8 viejos.**
2. 🟡 **`QUE_FALTA.md` es un imán de conflictos** en los 4 repos (casi todos lo tocan). Tras el
   primer merge de cada repo, el resto conflictúa ahí. Trivial de resolver (unión de ítems),
   pero hay que esperarlo. Alternativa de fondo: dejar de tocar QUE_FALTA en los branches.
3. 🟡 **Pares redundantes**: frioseguro 07-11-b⊂07-13 (subsumido). datalogger 07-09/07-15
   sd-integrity → **✅ RESUELTO 07-25** (reemplazadas por `nocturno/local-2026-07-25-sd-integrity-rebase`).
   datalogger 07-07/07-08 eco-LoRa → **✅ RESUELTO 07-25-b** (07-07⊂07-08, ambas borran `misiones/`;
   driver INA219 extraído en `nocturno/local-2026-07-25-b-ina219-extract`). **Ambos pares STALE
   peligrosos de datalogger quedan triados.**
4. 🟢 **Binarios de build en galgas 07-09** (`build/esp_rx_371/*.bin/.elf/.map`, ~144k líneas).
   No deben entrar a main. Sacarlos del árbol o cherry-pick solo del source; sumar `build/` al
   `.gitignore` de galgas si no está.

## Cómo verificar cada branch antes de mergear
Cada branch tiene su **diario** con los comandos exactos (tests, `--demo-hallazgo`, etc.):
`diario/nocturno-local-<fecha>.md` (o `-b`). El patrón general de los branches "modelo+tests":
```powershell
cd C:\Proyectos\<repo>
git checkout <branch>
python -m unittest <el test_*.py listado arriba>   # o el comando exacto del diario de esa fecha
git diff main --stat                                # confirmar archivos/líneas
```
Para los STALE de datalogger, **antes**: `git rebase main` y recién ahí correr los tests.

## Cómo se generó este doc (reproducible)
```bash
# por cada branch nocturno de cada repo:
git -C C:/Proyectos/<repo> rev-list --count <branch>..main      # cuántos commits atrás está
git -C C:/Proyectos/<repo> merge-tree --write-tree --name-only main <branch>   # conflictos vs main HOY
git -C C:/Proyectos/<repo> diff --shortstat main..<branch>      # tamaño
git -C C:/Proyectos/<repo> merge-base --is-ancestor <A> <B>     # detectar subsunciones
```

## Higiene detectada de paso (no la toqué)
- **frioseguro** y **cosechador** quedaron con el working tree **checkouteado en un branch
  nocturno** (no en `main`) de turnos previos. Inofensivo, pero conviene volverlos a `main`
  al terminar de drenar para que el próximo worker cree branches desde main fresco.

---
*Mantener este doc: al mergear un branch, tacharlo/borrar su fila. Cuando la cola llegue a 0,
borrar el archivo — su trabajo estará hecho.*
