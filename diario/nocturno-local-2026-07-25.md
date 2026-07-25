# Nocturno LOCAL — 2026-07-25 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
El turno de anoche (24-c) dejó la **cola de merge** con una tarea de análisis que un worker
nocturno SÍ puede cerrar sin humano ni hardware: **decidir el par redundante
`07-09`/`07-15 sd-integrity` de datalogger**. Lo diffeé con git real y encontré algo grave:
**ninguna de las dos ramas es mergeable.** Además del entregable (el analizador de integridad
de SD), **cada una BORRA el subsistema `misiones/` completo** (~1591 líneas) porque se cortaron
de un main viejo — y el main de hoy tiene **6 commits que son justamente ese subsistema** (la
taxonomía de 4 dataloggers, el selector sin cable, el WiFi manager, el fix de flash de misiones,
el desacople de la SD). `merge-tree` las daba "LIMPIO", pero mergear cualquiera **habría intentado
borrar el núcleo del firmware actual** — el peligro STALE exacto que la cola advertía.
**Lo resolví extrayendo el entregable real limpio** (`tools/sd_integrity.py` + su test, stdlib puro,
no existían en main → 100% aditivo, cero borrado) sobre el main de HOY, en un branch nuevo:
**`nocturno/local-2026-07-25-sd-integrity-rebase` (datalogger)** — **29 tests OK offline**.
**Neto: 2 branches tóxicos → 1 branch limpio.** Descartá 07-09 y 07-15 al confirmar.

## Tarea elegida y por qué
**Cerrar la decisión "par redundante sd-integrity" de la COLA_MERGE, extrayendo el entregable
limpio sobre main vivo.** Razones:
- **El sistema entero viene gritando que el cuello de botella es DRENAR, no producir**
  (últimos ~8 nocturnos + la cola del 24-c). Producir el branch #28 de un modelo+tests sería de
  valor negativo. En cambio, esta tarea **saca 2 branches de la pila y los reemplaza por 1 limpio**:
  drenaje neto, que es exactamente lo que hace falta.
- **Era una de las 3 cosas que el 24-c dejó explícitamente "para el día", y la ÚNICA que un
  worker nocturno puede cerrar solo** (las otras dos — mergear y rebasear+testear los 8 de
  datalogger — requieren criterio humano/hardware). Decidir el par redundante es análisis de git
  puro. El Director "persigue los huecos hasta cerrarlos"; éste era cerrable esta noche.
- **P0-octubre** (datalogger, categoría 2 de la jerarquía) y toca el DoD #5 (integridad SD).
- **100% software/análisis + stdlib de git y Python**, sin red, sin nube, sin hardware, sin
  compilar → cero riesgo de timeout (disciplina 07-07).

## Qué hice
1. **Diff real de las dos ramas** (`git diff --stat main..<branch>`): ambas tocan los mismos 18
   archivos y borran `misiones/__init__`, `mision_baja/media/dreyfus/lab`, `registro`, `selector`,
   `tools/test_misiones.py`, `tools/lab_rx.py` (−1591). 07-15 es la más completa (+785 vs +464:
   `sd_integrity.py` 372 vs 260 líneas, test 300 vs 157).
2. **Confirmé el peligro**: `git ls-tree main` → **main SIGUE teniendo todo `misiones/`**, y su
   `git log` muestra 6 commits construyéndolo (da574c3 taxonomía, bb92a8a/513c79b selector+WiFi,
   3d2cbc5 fix flash, e611bc5 desacople SD). O sea: mergear 07-09 o 07-15 borraría firmware vivo.
3. **Verifiqué que el entregable es extraíble limpio**: `tools/sd_integrity.py` importa solo
   stdlib (argparse/glob/math/os/re/sys/json); el test solo stdlib + `sd_integrity`; **ninguno de
   los dos existe en main** → agregarlos es puramente aditivo, sin dependencia de `misiones/`.
4. **Creé `nocturno/local-2026-07-25-sd-integrity-rebase`** desde `main` de hoy y extraje **solo**
   esos 2 archivos de la versión 07-15 (`git checkout 07-15 -- tools/sd_integrity.py tests/test_sd_integrity.py`).
   Cero borrados, cero mission-code tocado.
5. **Corrí los tests offline**: `python -m unittest tests.test_sd_integrity` → **Ran 29 tests, OK**.
6. Segundo commit en el branch: `QUE_FALTA.md #5` apuntando al branch limpio y marcando 07-09/07-15
   como NO mergeables. (Dejé el `main` de datalogger **prístino** — el QUE_FALTA va en el branch.)
7. En MATI-HQ actualicé `COLA_MERGE_NOCTURNOS.md` (tabla datalogger, TL;DR, peligro #3, sección
   "✅ RESUELTO") para que la sesión de drenaje no vuelva a evaluar el par.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-25-sd-integrity-rebase
python -m unittest tests.test_sd_integrity            # -> Ran 29 tests ... OK
git diff main --stat                                  # -> SOLO 3 archivos: sd_integrity.py + test + QUE_FALTA (aditivo, 0 borrados de misiones)
# Prueba del peligro que evité (por qué NO se mergean 07-09/07-15):
git ls-tree -r --name-only main | Select-String "misiones/"         # -> main TIENE todo misiones/
git diff --stat main..nocturno/local-2026-07-15-sd-integrity | Select-String "misiones|deletions"  # -> las borra (-1591)
git checkout main
```
**Resultado de esta noche:** 29/29 tests OK sobre el main vivo; el branch limpio es 100% aditivo;
los dos branches viejos quedan documentados como tóxicos con la evidencia de git.

## Qué quedó SIN verificar / para el día (Matías + @verificador)
1. **Mergear el branch limpio** `07-25-sd-integrity-rebase` (mecánico, aditivo, tests verdes) y
   **borrar las ramas `07-09-sd-integrity` y `07-15-sd-integrity`** de local y origin al confirmar.
   Eso es acción de drenaje con criterio humano — no la hago yo.
2. **La parte de firmware del DoD #5** (seq numbers en el log + la prueba física de N horas
   continuas a fs objetivo) sigue pendiente y **necesita hardware** — el analizador ofrece el
   gate offline, no reemplaza el ensayo.
3. **Ojo con el otro par STALE de datalogger** (`07-07-ina219-ecolora` / `08-ecolora-fixes`):
   mismo patrón — cortados de main viejo, probablemente arrastran borrados de estado que main ya
   cambió. **Diffear igual que hice acá antes de mergear** (no confiar en `merge-tree` "LIMPIO").

## Observaciones para el día (no tareas mías)
- El hallazgo **valida el diagnóstico de la cola**: en datalogger, `merge-tree --name-only`
  "LIMPIO" **no es seguro** — no muestra que un merge borraría archivos que main modificó después.
  Para los 8 branches STALE de datalogger, la verificación correcta es diffear contra main y mirar
  qué **borran**, no solo si "aplica limpio".
- `data/field_captures` de galgas: ni mirado. No toqué galgas ni frioseguro ni cosechador.

## Reglas respetadas
Solo software (Python stdlib) + docs + análisis de git. **Nada mergeado, borrado, movido ni
deployado**; no borré ninguna rama; `main` de datalogger quedó **prístino**; sin `rm -rf`, sin
`reset --hard`, sin `push --force`; sin migraciones; sin mDNS; `data/field_captures` intacto; sin
compilaciones ni descargas → cero riesgo de timeout. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-25-sd-integrity-rebase` (datalogger, pusheado a origin; sale del `main`
de hoy; 2 commits: extracción del deliverable + pointer en QUE_FALTA).

## Notas para @verificador
- **DoD** = *"el branch limpio agrega el analizador sd_integrity + tests SIN tocar `misiones/`,
  los 29 tests pasan sobre el main vivo, y el entregable equivale al de 07-15 (la versión más
  completa)"*.
- Ataques sugeridos: (a) `git diff main --numstat` en el branch → confirmar 0 borrados;
  (b) correr los 29 tests + agregar un CSV con gap real y confirmar `GATE: FALLA` + exit 1;
  (c) diffear `tools/sd_integrity.py` del branch vs el de 07-15 → deben ser idénticos (extracción
  fiel, no reescritura); (d) confirmar que 07-09 no tenía nada **único** que 07-15 no tenga
  (`git diff 07-09 07-15 -- tools/sd_integrity.py`) — si aparece algo, avisá antes de descartar 07-09.
