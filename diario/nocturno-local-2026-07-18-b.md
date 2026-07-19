# Nocturno LOCAL — 2026-07-18 (turno B, worker de la PC, Matías durmiendo)

> Segundo turno del 18. El turno A (`nocturno-local-2026-07-18.md`) trabajó **FrioSeguro**
> (modelo offline de la alerta). Este turno trabajó **cosechador** — otro repo, sin pisarse.

## TL;DR para Matías (si leés una sola cosa)
El **cosechador** tenía el paper analizado y las decisiones de componentes tomadas, pero
**ni un solo número de diseño calculado**: cuánta energía guarda el banco, cuántos días
aguanta, cuántas transmisiones da, si el emisor sin batería cierra energéticamente. Todo
figuraba "No medido" en `PROGRESS.md`. Escribí un **modelo de energía en Python puro**
(`analisis/harvester_model.py`) + **18 tests** que **reproducen las Tablas 5 y 6 del paper**
(8.70 h de carga para el design 2 vs 8.69 h publicado ✓) y **derivan lo que faltaba**:
energía útil **15.25 J**, autonomía solo-sleep **77 días**, **~18.900 TX** por carga, y el
hallazgo de diseño clave: **el cuello de botella NO es el consumo en régimen — es el arranque
en frío** (8.1 h con el mejor design). Es el insumo directo de **dos finales-por-proyecto**
(TC2 + Medidas 2 → UNIVERSIDAD, prioridad #1). De paso destapó **2 números mal en los docs**.
**Branch: `nocturno/local-2026-07-18-modelo-energia` (cosechador), pendiente de merge.**

## Tarea elegida y por qué
**Convergencia académica del cosechador → TC2 + Medidas Electrónicas 2 (UNIVERSIDAD, prioridad #1).**
Recorrí los 4 `QUE_FALTA` y todas las branches. Por qué ésta y no otra:

- **galgas** (P0 octubre, prioridad #2): todos los bloqueantes duros ya tienen branch (RX
  task08, SCADA, OTA A/B, vpp, energy, hold, docs, linaje ×7) o son hardware (galga física,
  LiPo, brownout) o firmware de producción prohibido de noche (#16 lazo de alerta abierto).
- **datalogger** (P0): benchmark en `main`; el resto en branch (ina219/ecolora, sd-integrity
  ×2, rssi, ssid-casing de anoche) o hardware (piezo, alcance).
- **FrioSeguro** (P1, la plata): el turno A de HOY ya trabajó su core (alert-model). No apilo
  sobre el mismo repo la misma noche; la pila de deploy (6 branches) sigue esperando ~1 h de día.
- **cosechador** (P2): **cero branches nocturnos, ningún nocturno previo lo tocó — área fresca.**
  Es P2 en la *cola de HARDWARE* (arranca cuando el datalogger cierre su DoD, comparten el
  front-end piezo). Pero su **capa de análisis/caracterización** es exactamente lo que la
  sección *Convergencias* de su `QUE_FALTA` mapea a **dos finales-por-proyecto** — y eso es
  **prioridad #1 (UNIVERSIDAD)**, no #2. `PROGRESS.md` item 10 ("Caracterización … comparar
  con valores del paper") está pendiente con TODO en "No medido". El pedazo que **no necesita
  hardware** — reproducir el paper y derivar los números de diseño — se puede cerrar de noche.

Por qué el modelo y no otra cosa: es el patrón que ya funcionó (frioseguro `alert_model.py`,
`scan_secrets.py`, datalogger `wifi_nets.py` — tools stdlib con tests), aplicado a un hueco
distinto: **la energía del harvester**, con un ancla de verificación dura (los números del paper).

## Qué hice — branch `nocturno/local-2026-07-18-modelo-energia` (cosechador)
Sale de `main`. **3 archivos nuevos + `.gitignore` + 2 docs actualizados. Cero borrados, no
toca el paper, ni el BOM, ni ninguna decisión de compra.**

| Archivo | Qué |
|---|---|
| `analisis/harvester_model.py` (nuevo) | Modelo stdlib del flujo de energía piezo→LTC3588→supercap→ATmega+NRF24. Cada constante citada a Tabla 5/6 o DECISIONS. Funciones puras: `stored_energy_j` (½CV²), `usable_energy_j`, `charge_current_a` (i=C·dV/dt), `sleep_autonomy_days`, `tx_budget_*`, `characterize`. CLI que imprime la tabla de caracterización lista para el informe de la uni. |
| `analisis/test_harvester_model.py` (nuevo) | **18 tests** `unittest` (sin deps). Ancla: reproduce el tiempo 0→3 V de la Tabla 6 (3 designs), la energía por TX y el sleep de la Tabla 5, ½CV², la autonomía y los presupuestos cruzados (por carga vs por energía coinciden a <5 %). |
| `docs/energia-modelo.md` (nuevo) | Por qué existe, el fundamento del modelo de carga (por qué corriente constante NO es especulación: es la lectura de la Tabla 6), correspondencia 1:1 con el paper, resultados, los 2 hallazgos de docs, límites honestos, y el mapeo explícito a TC2 y Medidas 2. |
| `PROGRESS.md` · `QUE_FALTA.md` | "Modelado" en la tabla de métricas + nota "EN BRANCH pendiente". |
| `.gitignore` (nuevo) | `__pycache__/` + `*.pyc` (el repo no tenía). |

## El fundamento (por qué no es especulación)
El paper reporta la carga como **tasa lineal `Tchr [V/h]`** (Tabla 6). Carga lineal en tensión
sobre un capacitor **es** corriente constante: `i = C·dV/dt → I_harv = C·(Tchr/3600)`. El modelo
encapsula la relación que **el propio paper usa** para publicar su columna "Time 0→3V" — no
inventa dinámica que el paper no midió. Sleep (0.75 µA) y TX (8 mA·33 ms) también son cargas de
corriente, así que todo el balance sale de `Q=C·ΔV` y `E=½CV²`, sin constantes libres. Si en
banco la curva real se aparta de la lineal, se cambia una sola función (`charge_current_a`) por
la curva medida y el resto del balance no cambia.

## Resultados (salida real del CLI de esta noche)
**Ancla — reproduce el paper:** 28.30 / **8.70** / 12.66 h (paper: 28.30 / **8.69** / 12.65) ✓.
**Derivado (nuevo para el proyecto):**
- Energía total @3.3 V = **54.45 J**; **útil** (2.8–3.3 V) = **15.25 J** (5.0 C).
- Autonomía **solo sleep, sin harvest** = **77.2 días**.
- **~18.900 TX** por carga (por-carga 18.939 vs por-energía 19.304, coinciden a ~2 %).
- Design 2 en vibración: harvest **2.87 mW** vs sleep 2.07 µW → **harvest domina ~1000×**;
  sostiene **3.6 TX/s** vibrando.
- **Conclusión de diseño:** el cuello de botella es el **arranque en frío** (0→2.8 V de boot):
  **8.1 h** con el mejor design (2, bi-clamped), hasta 26 h con el peor (1, disco). Refuerza D11
  (empezar con disco, migrar a bi-clamped) y sugiere un indicador "first light".

## Hallazgos (2 números mal en los docs, para reconciliar — NO los toqué)
1. **`DECISIONS.md` D9 dice "10 F a 3.3 V = 27 J".** El correcto es ½·10·3.3² = **54.45 J**.
   Los 27 J corresponden a **C = 5 F** (el banco en serie, antes de duplicar por los 2 ramos
   en paralelo, o el "5F 5.5V" del BOM original). → **@esquematico** confirma y corrige.
2. **`DECISIONS.md` D5 dice "energía cosechada ~µW promedio".** La Tabla 6 implica **~2.9 mW
   DURANTE la vibración** a 4 g/150 Hz. No es contradicción: µW = promedio real con duty cycle
   bajo; mW = banco bajo excitación continua. Falta el **duty cycle real de la cosechadora** para
   cerrar la autonomía de campo. → **@energia** lo define.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\cosechador
git checkout nocturno/local-2026-07-18-modelo-energia
git diff main --stat                                     # -> 3 nuevos + .gitignore + 2 docs
cd analisis
python -m py_compile harvester_model.py test_harvester_model.py   # -> exit 0
python -m unittest test_harvester_model -v               # -> 18 tests OK
python harvester_model.py                                # -> tabla de caracterizacion
```
**Resultado obtenido esta noche:** `py_compile` exit 0 + **18/18 OK** en <0.01 s + CLI reproduce
el paper. Sin descargas ni toolchains pesados — cero riesgo de timeout.

## Qué quedó SIN verificar (necesita banco — fase 2 del PROGRESS)
1. **Que el disco 27 mm real rinda como el paper** — el modelo reproduce las cifras publicadas,
   no las mide. Rendimiento real del piezo, sleep real del Pro Mini y alcance siguen "No medido".
2. **La dinámica fina del LTC3588** (histéresis UVLO, empaquetado por ciclo de buck) — el modelo
   usa la corriente promedio equivalente del paper; si la curva de banco se aparta, se ajusta 1 función.
3. **El duty cycle real de vibración** (hallazgo 2) — es el dato que falta para la autonomía de campo.

## Reglas respetadas
Solo software. Nada borrado, nada movido. No toqué el paper, ni el BOM, ni ninguna decisión de
compra, ni hardware. No toqué `data/` de galgas (otro repo). El `.gitignore` evita commitear
`.pyc`. Verificación instantánea con Python ya presente (3.14), con la disciplina de tiempo del
07-07. **Nota:** el repo cosechador no tenía identidad git seteada (migrado hace poco) — la
configuré local = Matías (`alegrematiasdev1@gmail.com`) para poder commitear. El branch **no se
mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-18-modelo-energia` (cosechador, pusheado a origin; sale de `main`).

## Notas para @verificador / @esquematico / @energia / @director
- **@verificador:** el DoD es *"cada cifra del modelo coincide con el paper (Tablas 5/6) y las
  derivaciones son ½CV² / Q=C·ΔV sin constantes libres"*. Los 18 tests son el oráculo. Punto a
  atacar: **¿el puente V/h ↔ corriente constante es legítimo?** Mi caso: el paper publica la carga
  como tasa lineal y extrapola linealmente a "Time 0→3V" — el modelo usa exactamente esa relación.
  Si eso se cae (p.ej. la carga real es sqrt por potencia constante), se cae la reproducción del
  ancla — es lo primero a romper. Segundo punto: **¿los 2 hallazgos de docs son correctos?** El de
  D9 (27 J = 5 F, no 10 F) es aritmético y sólido; el de D5 (µW vs mW) es de interpretación.
- **@esquematico (dueño de D9):** confirmá el número de energía del banco (54.45 J total / 15.25 J
  útil para 10 F) y corregí D9.
- **@energia (dueño de D5 y del perfil de energía):** el modelo te da los dos extremos
  (solo-sleep 77 días y en-vibración 3.6 TX/s); falta el **duty cycle real de vibración** de la
  cosechadora para la autonomía de campo. Ese número lo tenés que estimar/medir vos.
- **@director:** una noche de **UNIVERSIDAD (prioridad #1)** que convierte el cosechador (hasta
  hoy 10 %, todo hardware pendiente) en **material concreto de 2 finales-por-proyecto** (TC2 +
  Medidas 2) **sin gastar un peso ni tocar la cola de hardware**. Es la jugada de la CONVERGENCIA
  del PORTFOLIO, ejecutada en offline. Buen candidato a mergear directo tras @verificador — es un
  tool autocontenido, no depende de ninguna otra branch. **Recordá:** el turno A de hoy avisó que
  la pila de FrioSeguro (6 branches) sigue necesitando ~1 h de día con @verificador.
