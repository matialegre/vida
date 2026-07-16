# Nocturno LOCAL — 2026-07-15 (worker de la PC, Matías durmiendo)

## Tarea elegida y por qué
**galgas #3 — presupuesto de energía del emisor (la MITAD DE SOFTWARE).**
Herramienta de análisis stdlib, verificable 100% offline, aditiva y READ-ONLY.

Recorrí los 4 `QUE_FALTA`, los nocturnos previos (07-10→07-14) y el estado real de
branches. Lo que ordenó la decisión:
- **FrioSeguro tiene 5 branches sin mergear** (secret-scan y lint YA en main;
  resumen-mensual + fixes + vista #10 esperan deploy). El worker viene avisando
  **6 noches seguidas** que no hay que apilar más deuda de merge ahí — FrioSeguro
  es **deuda de DEPLOY, no de código**. Otro branch de FrioSeguro sería lo mismo.
  Anoche (07-14) ya se diversificó a frontend; hoy toca **octubre** (prioridad #2).
- Entre galgas y datalogger (ambos octubre), elegí **galgas #3** porque:
  1. Es un **bloqueante duro del DoD de octubre** ("presupuesto de energía medido
     del ciclo wake→muestreo→POST→sleep") que **nadie había tocado como software**.
  2. Encaja **exactamente en el patrón que ya funcionó** dos veces (07-10
     `rssi_calibrate.py`, 07-11 `vpp_threshold_audit.py`): una herramienta stdlib
     de análisis + tests, que hace la mitad computable y deja la de hardware clara.
  3. **Converge con Medidas Electrónicas 2** (UNIVERSIDAD, prioridad #1) y sirve
     a la meta declarada de @energia ("el mejor perfil de energía del planeta").
  4. **Enchufa con otro pendiente**: cuando el INA219 mida corriente real
     (bloqueante #4 del datalogger), esos números entran con `--model` y la
     autonomía sale sola. Un pendiente destraba a otro.

Encaja con "UNA tarea bien hecha por noche" y no estaba en ningún branch.

## Qué hice — branch `nocturno/local-2026-07-15-energy-budget`
Sale de `main`. Software **aditivo** (2 archivos nuevos + 1 doc + 1 línea en
QUE_FALTA). No toqué firmware, ni datos, ni `field_captures/` (sagrado), ni schema.

| Archivo | Qué |
|---|---|
| `tools/energy_budget.py` | Modela el ciclo de deep sleep del firmware v3 y calcula **autonomía en días**. Periodos **EXACTOS** de `firmware/shared/protocol.h` (modos hibernado 3600 / normal 600 / vigilado 60 / alerta 10 s; perfiles usb_bench/bat_normal/bat_low) y ventana despierta ~5.5 s del header de `esp_a_emisor.ino`. Corrientes por defecto **ESTIMADAS** (datasheet + `PLAN_CONSUMO_ESP32`), reemplazables por medición INA219 con `--model medido.json` (merge parcial). CLI: `--profile/--mode/--period`, `--mix` (duty-cycle de modos ponderado por tiempo), `--capacity/--derate`, `--min-days` (exit 1 si no llega → check de CI), `--json`. Stdlib puro, sin deps. |
| `tools/test_energy_budget.py` | 28 tests `unittest`: cálculo a mano verificado, monotonías (periodo↑→corriente↓), bracketing de mezclas, merge de modelo parcial, validación, exit codes de CLI. |
| `docs/energy-budget.md` | Modelo, provenance de cada número (qué es exacto vs estimado), uso, hallazgo para @energia, pendientes de hardware, nota de convergencia UTN. |
| `QUE_FALTA.md` (galgas) | #3 → "EN BRANCH … pendiente de merge" con el hallazgo. |

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-15-energy-budget
cd tools
python -m unittest test_energy_budget -v      # -> Ran 28 tests ... OK
python energy_budget.py                        # tabla perfiles/modos
python energy_budget.py --profile bat_normal   # desglose por fase
python energy_budget.py --mix normal=0.99,alerta=0.01
python energy_budget.py --profile bat_normal --min-days 30   # exit 0/1
```
**Resultado obtenido esta noche** (Python 3.14.3): `unittest` → **28/28 OK** (0.03 s).
Salidas de CLI coherentes y verificables a mano (un test replica el cálculo:
10 s @ 100 mA / periodo 100 s / 1000 mAh → 10 mA prom → 100 h). Números con los
defaults estimados: bat_normal (600 s) ≈ **56.8 días**, bat_low ≈ 168 d,
hibernado ≈ 327 d, alerta (10 s) ≈ 22.9 h.

## Hallazgo que sale del modelo (para @energia / @firmware)
A 600 s de periodo, **el wake se lleva el 99.2 % de la energía** — el deep sleep
de 10 µA es despreciable. ⇒ La palanca de autonomía es **acortar/espaciar el
wake**, NO seguir optimizando el sleep. Candidatos concretos: reemplazar la
asociación WiFi (~2 s, la fase más cara) por **ESP-NOW** (§"Cambios NO
implementados" de `PLAN_CONSUMO_ESP32.md`), o subir el periodo cuando la señal lo
permita. Además, **1 % de duty en ALERTA baja la autonomía de ~57 a ~36 días** →
los falsos positivos cuestan batería (el cap de 1 h de `ALERT_MAX_DURATION_S` es
la decisión correcta; el audit de umbral v_pp del 07-11 va en la misma dirección).

## Qué quedó SIN verificar (necesita hardware — @energia con INA219)
- **Corrientes reales por fase** (boot / wifi_connect / active_online) y **deep
  sleep real**: los defaults son estimaciones. Medirlas con INA219 y cargarlas
  en `--model medido.json` es lo que convierte esto en un presupuesto *medido*
  (cierra el #3 de verdad). Hoy es el marco, no la medición.
- **Duración real de la asociación WiFi** en la planta Dreyfus (depende del RSSI
  y la congestión — afecta la fase más cara).
- **Capacidad y derate reales** de la LiPo elegida (temperatura, edad, corte 3.2 V).

## Reglas respetadas
Nada borrado. No toqué firmware, ni schema, ni datos, ni `field_captures/`
(READ-ONLY sagrado — ni lo leí para esto), ni migraciones. No mDNS (no aplica).
No hay secretos en el código. No stageé `__pycache__/`. Verificación instantánea
(Python puro, 0.03 s) — sin compilación pesada, sin timeouts. El branch **no se
mergea** hasta que @verificador lo revise; pero es aditivo, sin riesgo, y los 28
tests pasan.

## Branch
`nocturno/local-2026-07-15-energy-budget` (pusheado a origin, 1 commit `e82f29b`;
sale de `main`).

## Notas para el @director / @verificador / @energia / @cronista
- **Patrón sostenido, dominio rotado**: 3ª herramienta de análisis stdlib de la
  serie (rssi 07-10, vpp 07-11, energy 07-15) — todas hacen "la mitad de software"
  de un bloqueante de octubre y todas convergen con la uni. Esta noche **octubre**,
  no FrioSeguro, a propósito (ver decisión arriba).
- **Sigue en pie la sugerencia repetida**: agrupar un **bloque de día de ~1 h para
  bajar la pila de FrioSeguro** (5 branches) — es deploy/merge, no código.
- **Convergencia doble**: `energy_budget.py` es insumo directo de Medidas 2
  (incertidumbre/trazabilidad de la medición INA219) y de Electrónica Industrial
  (presupuesto de energía de la instrumentación del REDLER).
- **Encadenamiento**: este branch queda "esperando datos" del INA219 del
  datalogger (#4) — cuando @energia arme ese driver, el mismo CSV/medición
  alimenta las dos cosas. Un solo esfuerzo de banco cierra dos pendientes.

---

## Adenda — turno de las 22:00 (misma fecha, nuevo turno del nocturno)

El scheduler disparó el turno de las **22:00 del 15-jul** (~20 h después de la
corrida de las 2:00 que hizo el energy-budget). Verifiqué primero que la tarea de
las 2:00 estuviera **entregada de verdad**: branch `nocturno/local-2026-07-15-energy-budget`
commit `e82f29b` en origin, diario completo, MATI-HQ `9921a84` — todo OK. Es un
turno nuevo, no una re-disparada duplicada, así que hice **UNA tarea nueva** (no
FrioSeguro: ya son 6 noches avisando que ahí la deuda es de *deploy*, no de código).

### Tarea elegida — datalogger #5 (mitad de software): auditor de integridad SD
`nocturno/local-2026-07-15-sd-integrity` (sale de `main`, aditivo, READ-ONLY).

**Por qué:** el #5 es un **RED bloqueante del DoD** del datalogger ("integridad SD:
detección de gaps + prueba de N horas a la fs objetivo") que nadie había tocado
como software. A propósito elegí un **validador** (como `scan_secrets`/`lint_device_config`),
no otro *modelo* de señal — rompe el "monocultivo" de herramientas de análisis que
el propio worker venía marcando (rssi 07-10, vpp 07-11, energy 07-15, todas modelos).
Datalogger tiene **solo 1 branch pendiente** (rssi), así que no apila deuda de merge.
Converge con **Medidas Electrónicas 2** (fs real / trazabilidad del temporizado).

**Hallazgo que hizo la tarea segura (leyendo el firmware real):** el formato de la
SD **no lo inventé** — es exactamente el de `firmwares/pico2w-node/eco.py:205,248`:
`# eco rafaga hz_obj=N ...` + `t_us,ax,ay,az,gx,gy,gz`, con `t_us` en µs desde el
arranque de la ráfaga. No hay seq explícito, pero el `t_us` alcanza: un salto
`Δt > 1.5·periodo` = muestras perdidas por un stall del **SPI compartido SD↔LoRa**
(`lora_sx127x.py:5`) cuando el firmware flushea cada 64 muestras (`eco.py:250`).

| Archivo | Qué |
|---|---|
| `tools/sd_integrity.py` | Audita una ráfaga o una carpeta `e*.csv` (= la prueba de N horas). Reporta fs real vs objetivo, #gaps + muestras perdidas estimadas por gap (`round(Δt/periodo)-1`), `drop_ppm`, cobertura, jitter (% del periodo), **no-monótonas** (timestamp hacia atrás/wrap) y **corruptas** (línea truncada). `--hz`/`--gap-factor`/`--max-drop-ppm`/`--min-coverage`/`--json`, stdin, agregado multi-archivo con "peor archivo". Exit 0/1/2 como **gate de CI** del DoD "sin gaps". Stdlib puro. |
| `tests/test_sd_integrity.py` | **29 tests** unittest sobre ráfagas sintéticas: perfecta, gaps de 1 y N muestras, varios gaps ordenados, no-monótonas, corruptas, hz inferida vs override, cobertura, jitter, agregado, exit codes, stdin, JSON. |
| `docs/sd-integrity.md` | Por qué (bus compartido + flush cada 64), cómo detecta sin seq, uso, exit codes, qué falta (hardware), convergencia UTN. |
| `QUE_FALTA.md` (datalogger) | #5 → "EN BRANCH … pendiente de merge" con el resumen. |

### Cómo verificarlo (offline, sin hardware)
```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-15-sd-integrity
python -m unittest tests.test_sd_integrity -v      # -> Ran 29 tests ... OK
python tools/sd_integrity.py --help
# demo con gap (5 ms a 1 kHz -> 4 muestras perdidas, exit 1):
printf '# eco rafaga hz_obj=1000\nt_us,ax,ay,az,gx,gy,gz\n0,1,2,3,4,5,6\n1000,1,2,3,4,5,6\n2000,1,2,3,4,5,6\n7000,1,2,3,4,5,6\n' | python tools/sd_integrity.py -
```
**Resultado obtenido esta noche** (Python 3.14.3): `unittest` → **29/29 OK** (0.08 s).
CLI coherente y verificable a mano (gap de 5000 µs / periodo 1000 µs → 4 perdidas).

### Qué quedó SIN verificar (necesita hardware — @muestreador)
- **Correr la captura real de N horas** en el nodo y pasarla por la herramienta:
  esto es el marco de auditoría, no la medición. Cierra el #5 de verdad cuando haya
  ráfagas reales de banco.
- **Calibrar el umbral aceptable** (`--gap-factor`, `--max-drop-ppm`) con datos
  reales: cuánta pérdida tolera el análisis de vibración buscado.
- Comportamiento con el **otro path de SD** (streaming no-eco de `main.py`, si
  existiera un formato distinto): hoy la herramienta cubre el formato `eco.py`, que
  es el único con cabecera de columnas definida encontrado en el firmware.

### Reglas respetadas
Nada borrado. No toqué firmware, ni datos, ni la SD, ni mDNS (jamás en datalogger),
ni el path archivado `_ARCHIVO_RASPBERRY_copias_viejas`. No stageé `__pycache__/`.
Verificación instantánea (Python puro, 0.08 s) — sin compilación pesada ni timeouts.
El branch **no se mergea** hasta @verificador; es aditivo y los 29 tests pasan.
Branch `nocturno/local-2026-07-15-sd-integrity` (origin, commit `391f4ce`).

**Disciplina:** dos turnos hoy (2:00 energy-budget octubre-galgas / 22:00 sd-integrity
octubre-datalogger), UNA tarea cada uno, ambos octubre, ambos "mitad de software"
de un bloqueante duro, ambos convergentes con la uni. Sin apilar FrioSeguro.
