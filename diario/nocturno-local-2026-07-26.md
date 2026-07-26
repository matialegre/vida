# Nocturno LOCAL — 2026-07-26 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
Las 2 noches previas (`-25`, `-25-b`) triaron los **2 pares tóxicos** del cluster STALE de
datalogger (sd-integrity y eco-LoRa) y dejaron flagged que quedaban **4 branches STALE más**
(eco-schedule, rv1-mesh, ssid-casing, rssi-calib) — el **peligro #1 de la cola de merge**
("el mayor riesgo de la pila"). Los diffé con git real: **los 4 tienen el mismo patrón tóxico**
— salen de `8784075` (main viejo) y un merge naïve **borraría todo `misiones/`**. Pero 3 de
ellos son **modelos+tests offline cleanly-extractables** (solo stdlib, no existen en main → 100%
aditivos). Los extraje byte-fiel sobre el main de HOY en **un** branch y corrí sus tests:
**82 tests OK** (eco 23 + rv1 32 + rssi 27). El 4º (ssid-casing/`wifi_nets.py`) es un **módulo
de firmware** que main ya cubre con el WiFi manager (513c79b) → **NO lo extraje** (sería código
muerto especulativo; rehacer con integración, no a ciegas).
**Branch limpio: `nocturno/local-2026-07-26-stale-cluster-extract` (datalogger).**
**Neto: 4 branches tóxicos STALE → 1 branch limpio aditivo.** Descartá 07-21, 07-19-b y 07-10
al confirmar; ssid-casing queda documentado como "rehacer sobre main". **Con esto el cluster
STALE de datalogger (8 branches) queda 100% triado.**

## Tarea elegida y por qué
**Terminar de triar el cluster STALE de datalogger** — cerrar los 4 branches STALE que las
noches previas dejaron explícitamente pendientes, extrayendo los deliverables limpios sobre
main vivo. Razones:
- **El sistema viene gritando hace ~9 noches que el cuello es DRENAR, no producir.** Un branch
  #28 (otro modelo+tests especulativo) tendría valor negativo. Esta tarea **saca 4 branches de
  la pila y los reemplaza por 1 limpio**: drenaje neto, que es lo que hace falta.
- **Era el hueco que `-25`/`-25-b` dejaron flagged** ("los 6 STALE restantes siguen necesitando
  rebase + re-test antes de mergear") y la cola llama a estos branches **"el mayor riesgo de la
  pila" (peligro #1)**. Análisis de git puro → un worker nocturno lo cierra solo. El Director
  "persigue los huecos hasta cerrarlos"; éste era cerrable esta noche.
- **P0-octubre** (datalogger, categoría 2) y toca **3 items del DoD** de golpe (#3 ECO-LoRa,
  #6 mesh RV1, #7 RSSI↔distancia).
- **100% software** (git + Python stdlib) sin red/nube/hardware/compilación → cero riesgo de
  timeout (disciplina 07-07).

## Qué hice
1. **Diffié los 4 branches STALE restantes** (`git diff --diff-filter=D --name-only main..<b>`):
   los **4 salen de `8784075`** (misma base vieja) y **los 4 borrarían todo `misiones/`**
   (`__init__`, `mision_baja/media/dreyfus/lab`, `registro`, `selector`, `tools/lab_rx.py`,
   `tools/test_misiones.py`, `docs/MODOS_MISION.md`) — el patrón tóxico exacto de sd-integrity
   y eco-LoRa. `merge-tree` los daría "limpios"; **ninguno es mergeable naïve**.
2. **Separé los aditivos de los especulativos** (`git diff --diff-filter=A`):
   - **eco-schedule (07-21)**: `tools/eco_schedule_model.py` + test + `docs/eco-schedule-model.md`.
     Imports: `argparse, sys`. Oráculo fiel de `eco.py::EcoNode.run()` (duty-cycle/sleep).
   - **rv1-mesh (07-19-b)**: `tools/rv1_mesh_model.py` + test + `docs/rv1-mesh-model.md`.
     Imports: `sys, os, unittest`. Modelo de ruteo/dedupe/flood del frame RV1.
   - **rssi-calib (07-10)**: `tools/rssi_calibrate.py` + test (`tests/`) + `docs/rssi-calibration.md`.
     Imports: `argparse, csv, json, math, sys`. Ajuste log-distance path-loss.
   - **ssid-casing (07-17-b)**: `firmwares/pico2w-node/wifi_nets.py` + test → **NO extraído**.
     Es un módulo de firmware; main ya construyó el WiFi manager (513c79b) **después** de la base
     del branch → extraerlo sin wiring sería código muerto (Karpathy: nada especulativo). Es el
     mismo criterio con el que la noche `-25-b` descartó `power_monitor.py`.
3. **Confirmé que los 3 aditivos NO existen en main** (`git cat-file -e main:<f>` → todos "no
   existe") y que **dependen solo de stdlib** (cero `machine`, cero `misiones/`, cero `eco.py`)
   → 100% aditivos, sin dependencia del subsistema que los branches borrarían.
4. **Branch `nocturno/local-2026-07-26-stale-cluster-extract`** desde `main` de hoy. Extraje los
   **9 archivos** (3 tools + 3 tests + 3 docs) con `git checkout <branch> -- <archivos>`.
   Confirmé **byte-identidad** de los 3 módulos vs su fuente (idénticos salvo CRLF).
5. **Corrí los 3 tests offline sobre el main vivo**: eco `cd tools && python -m unittest
   test_eco_schedule_model` → **23 OK**; rv1 `python -m unittest tools.test_rv1_mesh_model` →
   **32 OK**; rssi `python tests/test_rssi_calibrate.py` → **OK: 27 tests**. Total **82/82**.
   `py_compile` de los 6 archivos: OK.
6. **QUE_FALTA.md #3/#6/#7** (en el branch) apuntan a los deliverables; **#8** documenta que
   ssid-casing NO se mergea y hay que rehacer `wifi_nets.py` con integración. `main` de
   datalogger quedó **prístino** (el pointer va en el branch, como `-25`/`-25-b`).
7. En MATI-HQ actualicé `COLA_MERGE_NOCTURNOS.md` (tabla datalogger, peligro #1, sección nueva).

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-26-stale-cluster-extract
cd tools; python -m unittest test_eco_schedule_model   # -> Ran 23 tests ... OK
cd ..;   python -m unittest tools.test_rv1_mesh_model   # -> Ran 32 tests ... OK
python tests/test_rssi_calibrate.py                     # -> OK: 27 tests
git diff main --numstat                                 # -> 9 archivos, TODOS con 0 en la col. de borrados
git diff --diff-filter=D --name-only main..HEAD         # -> VACIO (no borra nada de misiones/)
# Prueba del peligro que evité (por qué NO se mergean los 3 viejos):
git diff --diff-filter=D --name-only main..nocturno/local-2026-07-21-eco-schedule-model | Select-String "misiones/"   # -> las borra
git checkout main
```
**Resultado de esta noche:** 82/82 tests OK sobre el main vivo; el branch es 100% aditivo
(0 borrados); los tres branches viejos quedan documentados como tóxicos con evidencia de git.

## Qué quedó SIN verificar / para el día (Matías + @verificador)
1. **Los 3 modelos son oráculos/gates offline, NO reemplazan hardware.** eco_schedule espeja
   `eco.py` (las cuentas de sleep/alcanzabilidad son correctas, pero el consumo real y la ventana
   RX se miden con el chip); rv1_mesh valida el protocolo de ruteo (la prueba de alcance/salto
   de repetidor sigue siendo de campo); rssi_calibrate procesa mediciones reales (que aún no se
   tomaron). [@energia / @comms]
2. **ssid-casing / `wifi_nets.py` NO se extrajo** y sigue pendiente el DoD #8: verificar el SSID
   real de GIMAP (`Gimap` vs `GIMAP`) y, si hace falta el módulo `wifi_nets`, **rehacerlo sobre
   el main vivo integrándolo con el WiFi manager (513c79b)** — no mergear el branch viejo. [@comms]
3. **Mergear el branch limpio** `07-26-stale-cluster-extract` (mecánico, aditivo, 82 tests verdes)
   y **borrar las ramas `07-21-eco-schedule-model`, `07-19-b-rv1-mesh-model` y `07-10-rssi-calib`**
   de local y origin al confirmar. También cerrar `07-17-b-ssid-casing` (no aporta nada mergeable).
   Acción de drenaje con criterio humano — no la hago yo.

## Observaciones para el día (no tareas mías)
- **El cluster STALE de datalogger (8 branches) queda 100% TRIADO.** Los 4 pares/branches
  peligrosos: sd-integrity (07-09/07-15, `-25`), eco-LoRa (07-07/07-08, `-25-b`) y ahora
  eco-schedule/rv1-mesh/rssi-calib (`-26`). **Los 8 borraban `misiones/`**; 7 reemplazados por
  branches aditivos limpios, 1 (ssid-casing) documentado como "rehacer sobre main". Ya **ningún
  branch STALE de datalogger es una trampa oculta** — cada uno tiene veredicto escrito.
- **Confirmado por 3ª noche:** en datalogger `merge-tree` "LIMPIO" **NO es seguro** — la
  verificación correcta es `git diff --diff-filter=D main..<branch>` (qué **borra**). Los 8
  branches lo demostraron: todos "limpios", todos borrando el núcleo del firmware.
- El próximo cuello de la cola pasa a ser el **drenaje mecánico de galgas (10) + frioseguro (6) +
  cosechador (1)** — que ese sí necesita @verificador + criterio humano (mergear de verdad), no
  otro worker nocturno. La producción nocturna de datalogger está, por ahora, agotada de valor:
  lo que falta es hardware (medir con INA219, prueba de campo) o merge humano.
- No toqué galgas, frioseguro ni cosechador. `data/field_captures` de galgas: ni mirado.

## Reglas respetadas
Solo software (git + Python stdlib) + docs + análisis. **Nada mergeado, borrado, movido ni
deployado**; no borré ninguna rama; `main` de datalogger quedó **prístino**; sin `rm -rf`, sin
`reset --hard`, sin `push --force`; sin migraciones; sin mDNS; `data/field_captures` intacto;
sin compilaciones ni descargas de cores → cero riesgo de timeout. El branch **no se mergea**
hasta @verificador.

## Branch
`nocturno/local-2026-07-26-stale-cluster-extract` (datalogger, pusheado a origin; sale del `main`
de hoy; 1 commit: extracción de los 3 deliverables + 3 docs + punteros en QUE_FALTA).

## Notas para @verificador
- **DoD** = *"el branch limpio agrega 3 modelos+tests (eco_schedule, rv1_mesh, rssi_calibrate) +
  sus docs SIN tocar `misiones/`, los 82 tests pasan sobre el main vivo, y los 3 módulos son
  byte-idénticos a sus fuentes (extracción fiel, no reescritura)"*.
- Ataques sugeridos: (a) `git diff main --numstat` en el branch → confirmar **0 borrados** en las
  9 filas; (b) por cada módulo, `diff <(git show <branch-viejo>:<path> | tr -d '\r') <(tr -d '\r'
  < <path>)` → vacío (idénticos mod EOL); (c) correr los 82 tests + romper a mano una constante
  de cada módulo (p.ej. `PROFILES` en eco, `TTL` en rv1) y confirmar que un test falla (los tests
  son fieles, no tautológicos); (d) confirmar el peligro: `git diff --diff-filter=D --name-only
  main..nocturno/local-2026-07-21-eco-schedule-model` lista `misiones/*` → por eso NO se mergea el
  viejo; (e) decidir sobre ssid-casing: ¿hace falta `wifi_nets.py` como módulo, o el WiFi manager
  513c79b de main ya cubre el casing SSID? Si hace falta, es tarea de firmware sobre main, no merge.
