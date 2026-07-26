# Nocturno LOCAL — 2026-07-25-b (2º turno de la noche, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
El 1er turno de esta noche (`-25`) cerró el par tóxico **sd-integrity** de datalogger y avisó:
*"Ojo con el otro par STALE — `07-07-ina219-ecolora`/`07-08-ecolora-fixes` — mismo patrón,
diffealo igual antes de mergear."* Lo hice: **es idéntico de tóxico.** `07-07 ⊂ 07-08`
(subsumido, como frioseguro 07-11-b⊂07-13) y **`07-08` borra el subsistema `misiones/` entero
(−4266 líneas)** porque salió de un main viejo → mergearlo **nukearía el firmware vivo**.
Pero adentro había una joya **cleanly-extractable**: `ina219.py`, el **driver INA219** que el
PORTFOLIO y el DoD #4 marcan pendiente ("consumo MEDIDO, no estimado"). Depende SOLO de `machine`,
no existía en main → 100% aditivo. Lo **extraje byte-fiel sobre el main de HOY** + le escribí un
**test offline nuevo** (13 tests OK) que ejercita el código real del driver sin el chip.
**Branch limpio: `nocturno/local-2026-07-25-b-ina219-extract` (datalogger).**
**Neto: 2 branches tóxicos más → 1 branch limpio.** Descartá `07-07` y `07-08` al confirmar.
Con esto **el cluster STALE de datalogger queda 100% triado** (los 2 pares peligrosos resueltos).

## Tarea elegida y por qué
**Cerrar el último par STALE ambiguo de la COLA_MERGE (`07-07`/`07-08` eco-LoRa), extrayendo
el deliverable limpio sobre main vivo.** Razones:
- **El sistema viene gritando hace ~8 noches que el cuello es DRENAR, no producir.** Un branch #28
  (otro modelo+tests) tendría valor negativo. Esta tarea **saca 2 branches de la pila y los
  reemplaza por 1 limpio**: drenaje neto, que es lo que hace falta.
- **Era el hueco que el turno `-25` dejó explícitamente flagged** ("diffear igual que sd-integrity
  antes de mergear"), y la cola lo llama **"el mayor riesgo de la pila"** (datalogger STALE). Es
  análisis de git puro → un worker nocturno lo cierra solo. El Director "persigue los huecos hasta
  cerrarlos"; éste era cerrable esta noche.
- **P0-octubre** (datalogger, categoría 2) y toca el **DoD #4** (driver INA219, consumo medido).
- **100% software** (git + Python stdlib + MicroPython) sin red/nube/hardware/compilación de core
  → cero riesgo de timeout (disciplina 07-07).

## Qué hice
1. **Relación entre los dos branches** (`git merge-base --is-ancestor`): **`07-07` es ancestro de
   `07-08`** → 07-08 lo subsume (mismo caso que frioseguro 07-11-b⊂07-13). Solo importa 07-08.
2. **Diff real `07-08` vs main** (`git diff --diff-filter=D --name-only main..07-08`): borra **41
   archivos**, entre ellos **todo `misiones/`** (7: `__init__`, `mision_baja/media/dreyfus/lab`,
   `registro`, `selector`), `tools/test_misiones.py`, `tools/lab_rx.py`, `docs/MODOS_MISION.md`,
   `benchmark/` y el `_legacy/` ESP32 — **−4266 líneas**. `git ls-tree main` confirma que main TIENE
   todo eso (lo construyó en 6 commits después de `75bd118`, la base de ambos branches).
   **Conclusión: mergear 07-07 o 07-08 borraría el núcleo del firmware actual.** Ninguno es mergeable.
3. **Identifiqué lo cleanly-extractable** (`git diff --diff-filter=A`): 3 archivos nuevos —
   `ina219.py` (dep: solo `machine`), `power_monitor.py` (dep: internals de `lora_sx127x` + `eco.py`),
   `docs/ECO_LORA_DISENO.md`. `eco.py` **ya existe en main** y el branch lo reescribe (628 líneas) →
   núcleo entrelazado, NO extraíble. `power_monitor.py` es la maquinaria eco-LoRa ligada a esa
   reescritura → incluirlo sin wiring sería código muerto/especulativo (Karpathy: nada especulativo).
   **El único deliverable limpio y auto-justificado es `ina219.py`.**
4. **Branch `nocturno/local-2026-07-25-b-ina219-extract`** desde `main` de hoy. Extraje **byte-fiel**
   `ina219.py` de `07-08` (`git checkout 07-08 -- ...ina219.py`; confirmado idéntico a la fuente).
5. **Test offline nuevo** `tools/test_ina219.py` siguiendo la convención del repo (`test_misiones.py`
   stubbea `machine`): un `_FakeI2C` registra escrituras y devuelve valores de registro programados,
   ejercitando el **código real** del driver — calibración (datasheet INA219 §8.5.1), **cap de
   overflow** del registro de cal, conversión signada (`_r16s`), decode de bus/shunt/corriente/
   potencia, `avg_ma`, y `sleep`/`wake` (bits de modo). **13 tests, OK.** Además `py_compile` OK.
6. **QUE_FALTA.md #4** (en el branch) apunta al branch limpio y marca `07-07`/`07-08` como NO
   mergeables. `main` de datalogger quedó **prístino** (el pointer va en el branch, como el `-25`).
7. En MATI-HQ actualicé `COLA_MERGE_NOCTURNOS.md` (tabla datalogger, peligro #1/#3, sección nueva).

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-25-b-ina219-extract
python -m unittest tools.test_ina219 -v          # -> Ran 13 tests ... OK
python -m py_compile firmwares/pico2w-node/ina219.py   # -> sin error
git diff main --stat                             # -> SOLO 3 archivos, +318, 0 borrados
git diff --diff-filter=D --name-only main..HEAD  # -> VACIO (no borra nada de misiones/)
# Prueba del peligro que evité (por qué NO se mergean 07-07/07-08):
git merge-base --is-ancestor nocturno/local-2026-07-07-ina219-ecolora nocturno/local-2026-07-08-ecolora-fixes; echo "exit $? (0 = 07-07 subsumido en 07-08)"
git diff --diff-filter=D --name-only main..nocturno/local-2026-07-08-ecolora-fixes | Select-String "misiones/"   # -> las borra
git checkout main
```
**Resultado de esta noche:** 13/13 tests OK sobre el main vivo; el branch es 100% aditivo (0
borrados); los dos branches viejos quedan documentados como tóxicos con evidencia de git.

## Qué quedó SIN verificar / para el día (Matías + @verificador)
1. **Consumo REAL con INA219 físico** (el corazón del DoD #4): medir mA por estado —muestreo /
   LoRa-TX / sleep— con el chip + LiPo. El driver + test dan el gate offline (las cuentas son
   correctas), **no reemplazan el ensayo en hardware**. [@energia]
2. **El resto del par eco-LoRa NO se extrajo** y sigue pendiente: `eco.py` reescrito, `power_monitor.py`
   y el **sleep con ventana RX (item #3 del DoD, "los nodos NO duermen")**. Están entrelazados con
   firmware que main modificó después → **rehacer sobre el main vivo, NO mergear los branches viejos.**
   ⚠️ Sigue en pie el aviso: `eco on` a P1/P2 con el firmware actual los deja inalcanzables.
3. **Mergear el branch limpio** `07-25-b-ina219-extract` (mecánico, aditivo, tests verdes) y **borrar
   las ramas `07-07-ina219-ecolora` y `07-08-ecolora-fixes`** de local y origin al confirmar. Acción
   de drenaje con criterio humano — no la hago yo.

## Observaciones para el día (no tareas mías)
- **El cluster STALE de datalogger (8 branches) queda TRIADO en sus 2 pares peligrosos**: sd-integrity
  (07-09/07-15, resuelto `-25`) y eco-LoRa (07-07/07-08, resuelto hoy). Ambos borraban `misiones/`;
  ambos reemplazados por un branch aditivo limpio. Los **6 branches STALE restantes** de datalogger
  (eco-schedule, rv1-mesh, ssid-casing, rssi-calib, y los propios core) siguen necesitando
  `git rebase main` + re-test **antes** de mergear — pero ya ninguno es un par redundante oculto.
- **Confirmado de nuevo:** en datalogger `merge-tree --name-only` "LIMPIO" **NO es seguro** — no
  muestra que un merge borraría archivos que main creó después. La verificación correcta es
  `git diff --diff-filter=D main..<branch>` (qué **borra**), no si "aplica limpio".
- No toqué galgas, frioseguro ni cosechador. `data/field_captures` de galgas: ni mirado.

## Reglas respetadas
Solo software (git + Python stdlib + MicroPython) + docs + análisis. **Nada mergeado, borrado,
movido ni deployado**; no borré ninguna rama; `main` de datalogger quedó **prístino**; sin `rm -rf`,
sin `reset --hard`, sin `push --force`; sin migraciones; sin mDNS; `data/field_captures` intacto;
sin compilaciones ni descargas de cores → cero riesgo de timeout. El branch **no se mergea** hasta
@verificador.

## Branch
`nocturno/local-2026-07-25-b-ina219-extract` (datalogger, pusheado a origin; sale del `main` de
hoy; 1 commit: extracción del driver + test offline + pointer en QUE_FALTA).

## Notas para @verificador
- **DoD** = *"el branch limpio agrega el driver `ina219.py` + su test SIN tocar `misiones/`, los 13
  tests pasan sobre el main vivo, y `ina219.py` es byte-idéntico al de `07-08` (extracción fiel, no
  reescritura)"*.
- Ataques sugeridos: (a) `git diff main --numstat` en el branch → confirmar **0 borrados**;
  (b) `diff <(git show 07-08:firmwares/pico2w-node/ina219.py) firmwares/pico2w-node/ina219.py` →
  idénticos (salvo CRLF); (c) correr los 13 tests + romper a mano una constante del driver (p.ej.
  `REG_BUS_V`) y confirmar que un test falla (el test es fiel, no tautológico); (d) confirmar que
  `07-07` no tiene nada **único** que `07-08` no tenga (`git diff 07-07 07-08 -- firmwares/pico2w-node/ina219.py`
  → vacío, porque 07-07 es ancestro) antes de descartar 07-07.
