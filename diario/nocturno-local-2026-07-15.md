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
