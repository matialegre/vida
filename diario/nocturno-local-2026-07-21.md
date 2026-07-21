# Nocturno LOCAL — 2026-07-21 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
El **planificador de duty-cycle** del nodo ECO del datalogger — el que decide **cuánto
duerme**, **cuándo es alcanzable** y **qué le reporta al dashboard** — vivía entero en
`firmwares/pico2w-node/eco.py::run()` y **no tenía ni un test offline**. Es la lógica que
gobierna a la vez el **perfil de ahorro de energía** ("el mejor del planeta", objetivo
declarado) y la advertencia del QUE_FALTA #3 *"si mandás `eco on` quedan inalcanzables"*.
Escribí su modelo/oráculo espejo 1:1 (`tools/eco_schedule_model.py`, stdlib) + **23 tests**
+ doc. Y al reproducir la lógica saltaron **3 hallazgos verificables**, el principal 🟠:
el perfil **`frecuente` (ciclo 20 s) tiene un margen de sueño tan fino que una reconexión
lenta o la primera conexión del arranque satura `sleep_ms` en 0** → **el nodo no duerme y
el perfil de ahorro se degrada en silencio** (queda 100 % activo, cero aviso). **No corregí
firmware** (es de @firmware/@energia, en banco con INA219 real). **Branch:
`nocturno/local-2026-07-21-eco-schedule-model` (datalogger), pendiente de merge.**

## Tarea elegida y por qué
**datalogger #3 (P0 octubre — "terminarlo primero, antes del trabajo Dreyfus").** El
bloqueante ECO-LoRa, mitad de software: el planificador de duty-cycle. 100 % software, sin
hardware, no destructivo, patrón probado (modelo/oráculo offline).

Recorrí los 4 `QUE_FALTA`, todos los branches nocturnos y los nocturnos previos. Por qué ésta:
- **FrioSeguro (P1, PLATA = top):** los DOS turnos de anoche (07-20 y 07-20-b) tocaron
  frioseguro (door-alert) y galgas (ota-decision). No apilo en repos tocados anoche;
  además la pila de FrioSeguro ya tiene 6+ branches esperando merge.
- **galgas (P0 octubre):** cerró `ota-decision-model` anoche (07-20-b). No apilo.
- **cosechador (P2):** cerró `modelo-energia` el 07-18-b; lo que queda es compra/hardware.
- **datalogger (P0 octubre):** cerró `rv1-mesh-model` el 07-19-b (hace 2 noches). Ese
  modeló el **ruteo LoRa** de `nodo.py`; el **duty-cycle del nodo ECO** (`eco.py`, otro
  firmware, por WiFi) es un subsistema distinto y **sin ningún test offline**. Es el que
  la advertencia "quedan inalcanzables" del #3 pone en el centro. Ese era el pedazo
  verificable sin hardware que faltaba, y toca de lleno el objetivo de energía.

Por qué el modelo-y-test: mismo patrón que ya funcionó (alert/door en frioseguro, vpp/rx/ota
en galgas, mesh en datalogger, energía en cosechador) aplicado al **subsistema que faltaba**,
con un ancla dura: **auditar el presupuesto de sueño y la alcanzabilidad reales** contra lo
que el firmware realmente decide.

## Qué hice — branch `nocturno/local-2026-07-21-eco-schedule-model` (datalogger)
Sale de `main`. **3 archivos nuevos + 1 nota en QUE_FALTA. Cero borrados, no toca firmware,
ni la SD, ni la nube, ni otra branch.** (`git diff --cached --stat` → 492 inserciones, 4
archivos.)

| Archivo | Qué |
|---|---|
| `tools/eco_schedule_model.py` (nuevo, 207 líneas) | Espejo 1:1 de `eco.py::run()`. `plan_cycle(cycle_s, burst_s, wifi_overhead_ms, awake, sleep_mode, use_wifi)` reproduce EXACTO: `sleep_ms = max(0, cycle*1000 - elapsed)` (eco.py:349-351), `reported_next_s = max(0, cycle - burst)` (eco.py:334), y la rama `awake` (no duerme, `_idle(1500)`, wifi vivo, eco.py:341-346). Deriva `actual_interval_s`, `next_error_s`, `worst_cmd_latency_s`, `duty_awake_frac` y el flag `sleep_clamped`. `estimate_wifi_overhead_ms()` compone los costos DOCUMENTADOS del propio firmware (warmup 1200 / discover 3000|1500 / connect ≤10000 / http×3). CLI: `--demo-hallazgo` (exit 1 si degrada), `--profile`, `--cycle/--burst/--overhead-ms/--awake/--sleep`. |
| `tools/test_eco_schedule_model.py` (nuevo) | **23 tests** `unittest` (sin deps, no tocan hardware): presupuesto de sueño (normal / borde exacto / clamp negativo / light==idle), modo awake (nunca duerme, wifi vivo, latencia baja), `next` reportado (fórmula, piso 0, subestima el real), alcanzabilidad (latencia=1 ciclo dormido, acotada por el ciclo), estimador de overhead (primera vez > conocido, lento > típico, componentes), sin-wifi, y **regresión del hallazgo A** (frecuente primera-vez-lento degrada, típico duerme, medio con margen sano, demo devuelve 1). |
| `docs/eco-schedule-model.md` (nuevo) | Por qué existe, tabla de correspondencia 1:1 con `eco.py`, los 3 hallazgos con evidencia, cómo verificar, y alcance honesto (qué NO cubre: consumo real en mA, la ráfaga interna, el nodo LoRa). |
| `QUE_FALTA.md` (datalogger) | Nota "EN BRANCH pendiente" bajo #3. |

## Los hallazgos (NO corregidos — son de @firmware/@energia, en banco)

### 🟠 A — El presupuesto de sueño del perfil `frecuente` es frágil
Con `cycle=20s` y `burst=5s` quedan **15 s** para todo el tramo wifi. Un ciclo con
**primera conexión** (discover 3 s, `eco.py:109`) + **asociación lenta** (connect hasta
10 s, `eco.py:91`) suma warmup 1.2 + connect 10 + discover 3 + 3×http 0.5 = **15.7 s**; con
la ráfaga (5 s) el `elapsed` llega a **20.7 s > 20 s** → `sleep_ms` se satura en 0
(`eco.py:350-351`) → **el nodo no duerme ese ciclo** y el perfil de ahorro se degrada sin
avisar (queda 100 % activo). Con una conexión típica ya conocida el mismo perfil sí duerme
(~8.8 s): el margen existe pero es tan fino que **cualquier reconexión lenta lo borra**.
`medio` (60 s) y `max` (600 s) tienen margen sano.

Salida real de esta noche (`--demo-hallazgo`, exit 1):
```
HALLAZGO A - el presupuesto de sueno del perfil 'frecuente' es fragil
  overhead wifi estimado = 15700 ms (warmup+connect+discover+3*http)
  elapsed (rafaga+wifi) = 20700 ms
  sleep_ms              = 0 ms  (durmio=False  <-- CLAMP a 0)
  (para comparar, mismo perfil con conexion tipica ya conocida: sleep_ms=8800)
```
**Fix candidato (banco):** subir el piso del perfil `frecuente` (ciclo ≥ 30 s) o loguear
cuando `sleep_ms==0` para que el degradado deje de ser silencioso. Al tocar la lógica,
actualizar `TestHallazgoFrecuenteFragil` en el mismo commit.

### 🟡 B — Nodo dormido = sordo: latencia de comando de hasta un ciclo entero
En modo dormir la única ventana para leer un comando del dashboard es el `_pull_config` del
tramo wifi (`eco.py:170`); durante el `lightsleep`/idle el nodo no escucha nada. Latencia
peor-caso de un comando (config, `awake`, OTA) = **un ciclo entero**: 20 s (`frecuente`),
60 s (`medio`), **600 s ~10 min (`max`)**. Es el *"quedan inalcanzables"* del #3
cuantificado: el nodo no se pierde para siempre, responde recién en su próxima ventana. UX:
un botón "despertar ya" no puede prometer respuesta inmediata salvo modo `awake`.

### 🟡 C — El `next` reportado ignora el overhead de wifi
`eco.py:334` reporta `next = cycle - burst`, pero el intervalo real entre envíos ≈ el ciclo
completo → subestima (en `medio`, reporta 50 s cuando el real es 60 s). Hoy **sin impacto**
porque Vercel marca stale por el push del ESP (15 s, `vercel-dashboard/api/index.js:91`),
no por `ecoNext`; pero el ESP guarda y publica ese `next` (`esp32_dashboard.ino:1001`), así
que cualquier consumidor que lo use contaría mal. Fix trivial si se usa: reportar `cycle`.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-21-eco-schedule-model
git diff main --stat                                   # -> 4 archivos, 492 inserciones
python -m py_compile tools/eco_schedule_model.py tools/test_eco_schedule_model.py   # exit 0
cd tools && python -m unittest test_eco_schedule_model   # -> OK (23 tests)
cd .. && python tools/eco_schedule_model.py --demo-hallazgo   # -> HALLAZGO A/B, exit 1
python tools/eco_schedule_model.py --profile frecuente --overhead-ms 16000   # AVISO no duerme, exit 1
python tools/eco_schedule_model.py --profile medio            # duerme sano, exit 0
```
**Resultado obtenido esta noche:** `py_compile` exit 0 · **23/23 OK** en <0.01 s ·
`--demo-hallazgo` marca la degradación (exit 1) · `--profile frecuente --overhead-ms 16000`
avisa que no duerme (exit 1) · `--profile medio` duerme sano (exit 0). Sin descargas ni
toolchains pesados — **cero riesgo de timeout** (disciplina del 07-07 respetada).

## Qué quedó SIN verificar (necesita banco — no se cierra de noche)
1. **El consumo REAL (mA) del ciclo degradado** — el modelo es de *tiempos*, no de energía;
   confirmar con el INA219 (bloqueante #4) cuánto cuesta que el perfil `frecuente` no
   duerma vs que duerma. El % activo del ciclo es el insumo, el mA lo da el hardware.
2. **Que el overhead de wifi real caiga en el rango modelado** — connect/discover/http
   dependen de la red de planta; medir en banco cuánto tarda de verdad una reconexión.
3. **El fix del perfil `frecuente`** — decisión de @energia (subir el piso vs descontar el
   overhead explícitamente); requiere re-medir tras aplicarlo.

## Reglas respetadas
Solo software. Nada borrado, nada movido. **No toqué firmware** (`eco.py` intacto — los
hallazgos se flagean, no se corrigen), ni la SD, ni la nube, ni secretos. Jamás mDNS. No
toqué otros repos. Identidad git = Matías. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-21-eco-schedule-model` (datalogger, pusheado a origin; sale de `main`).

## Notas para @verificador / @firmware / @energia / @director
- **@verificador:** el DoD es *"cada decisión de `eco_schedule_model.py` coincide con
  `eco.py::run()`, y el hallazgo A es real"*. La tabla de correspondencia 1:1 está en el
  doc. Puntos a atacar: (a) **¿`sleep_ms = cycle*1000 - elapsed` con clamp a 0?** Confirmá
  `eco.py:348-351` y que `elapsed` arranca en `t_cycle0` (línea 317, ANTES de la ráfaga).
  (b) **¿`reported_next = cycle - burst`?** `eco.py:334`. (c) **¿el escenario del hallazgo
  A es plausible?** warmup 1200 (`:82`) + connect ≤10000 (`:91`) + discover 3000 primera
  vez (`:109`) + ráfaga 5000 > 20000. Los costos variables son parámetro, no invención.
- **@firmware/@energia (dueños del fix):** A es la decisión de perfil (piso del `frecuente`
  o log del degradado), C es 1 línea (`eco.py:334`). Confirmá A en banco con INA219 y
  actualizá modelo+test en el mismo commit si tocás la lógica.
- **@director:** una noche de **P0 octubre** (segundo en la jerarquía tras PLATA/uni) que
  cierra el **test offline del planificador de duty-cycle que faltaba** y encuentra que **el
  perfil de ahorro más agresivo se degrada en silencio con una reconexión lenta** — sin
  gastar un peso, sin tocar hardware ni firmware. Complementa el mesh-model del 07-19-b (mismo
  repo, subsistema distinto) sin apilar en los repos tocados anoche. **Sigue en pie:** las
  pilas de branches nocturnos (galgas, frioseguro, datalogger, cosechador) necesitan sesiones
  de día con @verificador para mergear en orden.
