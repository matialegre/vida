# Nocturno LOCAL — 2026-07-20 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
La alerta de **PUERTA ABIERTA** de FrioSeguro — la 2ª causa de pérdida de un
comercio, parte del core "el servicio avisa" que se cobra — vivía entera en
`door_sensors.h::doorSensorsCheck` y **no tenía ni un test offline**. El
alert-model del 07-18 cubrió la rama de **temperatura**; la de **puerta** es un
módulo aparte y quedó afuera. Escribí su modelo/oráculo espejo 1:1
(`tools/door_alert_model.py`, stdlib) + **16 tests** + doc. Y al reproducir la
lógica saltaron **3 hallazgos concretos y verificables**, el principal 🔴: el
firmware dispara la alerta de puerta con el **`#define DOOR_OPEN_ALERT_SEC 120`
hardcodeado** y **NO con `config.doorOpenMaxSec`** — el umbral que TODO el resto
del firmware carga de Preferences, **sincroniza desde Supabase** y expone en la
web. **El umbral de puerta que el cliente configura desde el dashboard no tiene
ningún efecto** (la placa lo recibe, lo guarda, y alerta igual a los 120 s
fijos). **No corregí firmware** (es de @firmware, en banco con un reed real).
**Branch: `nocturno/local-2026-07-20-door-alert-model` (frioseguro), pendiente de merge.**

## Tarea elegida y por qué
**FrioSeguro #18 (PLATA — prioridad TOP junto con universidad).** La mitad de
software del "cerrar hallazgo de la decisión de alerta (el core que se cobra)",
pero para la rama de PUERTA, que el alert-model del 07-18 dejó explícitamente
afuera. 100 % software, sin hardware, no destructivo.

Recorrí los 4 `QUE_FALTA`, todos los branches nocturnos y los nocturnos previos. Por qué ésta:
- **galgas (P0 octubre):** cerró `rx-detection-replay` el 07-19 (hace 1 día); no apilo.
- **datalogger (P0 octubre):** cerró `rv1-mesh-model` el 07-19-b (hace 1 día); no apilo.
- **cosechador (P2):** cerró `modelo-energia` el 07-18-b; y todo lo que le queda es
  compra/hardware (fases 1-6). Sin tarea software nueva sin apilar.
- **FrioSeguro (P1, PLATA = top):** el 07-18 modeló la alerta de **temperatura**
  (`checkAlerts`). Al releerlo noté que la promesa "el servicio avisa" tiene una
  **segunda pata sin cubrir**: la puerta abierta, que es un **módulo distinto**
  (`door_sensors.h`, corre por `doorSensorsLoop` cada 500 ms, no por `checkAlerts`)
  y **no tenía test offline**. Ese era el pedazo verificable sin hardware que
  faltaba, y es plata directa (churn/pérdida de mercadería del comercio).

Por qué el modelo-y-test: es el patrón que ya funcionó (alert-model en frioseguro,
vpp/rx en galgas, mesh en datalogger, energía en cosechador) aplicado al
**subsistema hermano que faltaba**, con un ancla dura: **auditar el umbral que el
firmware realmente usa** contra el que el cliente configura.

## Qué hice — branch `nocturno/local-2026-07-20-door-alert-model` (frioseguro)
Sale de `main`. **3 archivos nuevos + 1 nota en QUE_FALTA. Cero borrados, no toca
firmware, ni la nube, ni otra branch.** (`git diff --cached --stat` → 541
inserciones, 4 archivos.)

| Archivo | Qué |
|---|---|
| `tools/door_alert_model.py` (nuevo, 258 líneas) | Espejo 1:1 de `door_sensors.h::doorSensorsCheck` para una puerta. `DoorMonitor.tick(is_open_now, now_ms)` reproduce EXACTO las 3 ramas del firmware (flanco apertura → `OPENED`+openCount; flanco cierre → `CLOSED`+acumula totalOpenTime; "mucho tiempo abierta" → `ALERT` una sola vez con latch `alert_sent`). `open_seconds()` = espejo de `doorGetOpenSeconds`. `replay()` + `_sample_every(period_ms=500)` (cadencia real del loop). CLI: `--open`, `--threshold`, `--demo-hallazgo` (exit 1 si divergen umbral real vs configurado). El `alert_threshold_sec` es parametrizable SOLO para poder demostrar el hallazgo; por defecto es el `DOOR_OPEN_ALERT_SEC=120` real. |
| `tools/test_door_alert_model.py` (nuevo) | **16 tests** `unittest` (sin deps, no tocan hardware): transiciones (apertura/cierre/sin-cambio/permanece, acumulación multi-ciclo, openCount), umbral (dispara al pasar, no antes, una sola vez con latch, cierre antes no dispara, **re-arme tras abrir/cerrar**), `open_seconds`, **regresión del hallazgo #1** (real 120 vs configurado 180 divergen), y fidelidad del muestreo 500 ms. |
| `docs/door-alert-model.md` (nuevo) | Por qué existe, tabla de correspondencia 1:1 con el `.h`, los 3 hallazgos con evidencia, cómo verificar, y alcance honesto (qué NO cubre: rebote del reed, gating por internet/buffering, multi-puerta). |
| `QUE_FALTA.md` | Nota "EN BRANCH pendiente" bajo #18. |

## Los hallazgos (NO corregidos — son de @firmware/@backend, en banco)

### 🔴 #1 — El umbral configurable por cliente NO se respeta
`config.doorOpenMaxSec` (default 180 s, `config.h:153`) se carga de Preferences
(`storage.h:25`), **se sincroniza desde Supabase** en cada pull de config remota
(`supabase.h:248/253`), se expone/setea por la web (`web_api.h:110/150`), sale en
el status JSON (`ino:280`) y por serial (`serial_api.h:88`). Pero la decisión real
de alerta (`door_sensors.h:154`) compara contra el **`#define DOOR_OPEN_ALERT_SEC`
hardcodeado en 120**, no contra `config.doorOpenMaxSec`. **El cliente configura su
umbral de puerta desde el dashboard, la placa lo recibe y lo guarda, y la alerta
igual dispara a los 120 s fijos.** Además el default no coincide (config 180 ≠
módulo 120). Es exactamente la clase de bug que el linter de provisioning (branch
07-12) existe para cazar: no rompe la compilación, rompe al cliente.

Salida real de esta noche (`--demo-hallazgo`, exit 1):
```
HALLAZGO #1 - el umbral configurable NO se respeta
  Escenario: puerta abierta 150 s. Cliente configuro doorOpenMaxSec=180 s.
  Firmware REAL (DOOR_OPEN_ALERT_SEC=120): ALERTA a los 120s
  Lo que el cliente ESPERA (umbral 180): SIN alerta (todavia no llego a 180s)
  -> divergencia observable: SI
```
**Fix candidato (banco):** en `door_sensors.h:154` usar `config.doorOpenMaxSec` en
vez del `#define`. Al aplicarlo, quitar el `alert_threshold_sec` fijo del modelo y
actualizar `TestHallazgo1UmbralIgnorado` en el mismo commit.

### 🟠 #2 — La alerta de puerta NO llega a Supabase (solo Telegram)
`doorSensorsCheck` dispara `sendTelegramAlert` pero **nunca** `sendAlertToSupabase`
(la de temperatura sí, `alerts.h:64`). Un evento de puerta abierta **no queda en la
tabla `alerts`** → invisible en el dashboard y **ausente del resumen mensual**
(branches 07-11b/07-13, que venden retención). La 2ª causa de pérdida del comercio
queda sin registrar. **Fix:** agregar `sendAlertToSupabase("door","warning",msg)`.

### 🟡 #3 — Drift de docs
`door_sensors.h:5` dice "Este módulo NO está integrado aún. Solo definiciones." —
pero SÍ está wired (`doorSensorsInit` en `ino:191`, `doorSensorsLoop` en `ino:557`).

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-07-20-door-alert-model
git diff main --stat                                   # -> 4 archivos, 541 inserciones
python -m py_compile tools/door_alert_model.py tools/test_door_alert_model.py   # exit 0
cd tools && python -m unittest test_door_alert_model   # -> OK (16 tests)
cd .. && python tools/door_alert_model.py --demo-hallazgo   # -> HALLAZGO #1, exit 1
python tools/door_alert_model.py --open 200            # OPENED / ALERT@120s / CLOSED@200s
```
**Resultado obtenido esta noche:** `py_compile` exit 0 · **16/16 OK** en <0.01 s ·
`--demo-hallazgo` marca la divergencia real↔configurado (exit 1) · `--open 200`
alerta a los 120 s. Sin descargas ni toolchains pesados — **cero riesgo de
timeout** (disciplina del 07-07 respetada).

## Qué quedó SIN verificar (necesita banco — no se cierra de noche)
1. **Que los 3 fixes se comporten bien en hardware** — requiere un reed switch real
   y una placa flasheada (confirmar que respeta `doorOpenMaxSec`, que la alerta
   aparece en el dashboard, y que el header ya no miente).
2. **El rebote del reed** (chatter mecánico): el firmware no debouncea la lectura;
   el modelo toma `is_open_now` como verdad. Un reed que rebota podría inflar
   `openCount`. Solo se ve con reed físico.
3. **El gating por internet + buffering**: el firmware manda el Telegram solo si
   `internetAvailable` y **no bufferea** → una alerta de puerta durante un corte de
   WiFi se pierde (misma clase de hueco de resiliencia que la de temperatura).

## Reglas respetadas
Solo software. Nada borrado, nada movido. **No toqué firmware** (`door_sensors.h`
intacto — los hallazgos se flagean, no se corrigen), ni schema, ni nube, ni
secretos. No toqué otros repos. Identidad git = Matías. El branch **no se mergea**
hasta @verificador.

## Branch
`nocturno/local-2026-07-20-door-alert-model` (frioseguro, pusheado a origin; sale de `main`).

## Notas para @verificador / @firmware / @backend / @director
- **@verificador:** el DoD es *"cada decisión de `door_alert_model.py` coincide con
  `door_sensors.h::doorSensorsCheck`, y el hallazgo #1 es real"*. La tabla de
  correspondencia 1:1 está en el doc. Puntos a atacar: (a) **¿el modelo diverge del
  `.h` en alguna rama** — el orden apertura→cierre→"mucho tiempo abierta", o el
  reset de `alert_sent` en la apertura (`door_sensors.h:133`)? Leé el `.py` contra
  `door_sensors.h:118-170`. (b) **¿el hallazgo #1 es real o me equivoqué?** Mirá
  `door_sensors.h:154` (`if openSeconds >= DOOR_OPEN_ALERT_SEC`) y confirmá que
  `DOOR_OPEN_ALERT_SEC` es el `#define 120` de la línea 31 y NO `config.doorOpenMaxSec`.
  (c) **¿el #2 es real?** `grep sendAlertToSupabase firmware_modular/door_sensors.h`
  → 0 resultados.
- **@firmware (dueño de los fixes):** #1 es 1 línea (`door_sensors.h:154`), #2 son
  ~2 líneas (agregar la llamada a Supabase), #3 es borrar un comentario. Confirmá en
  banco con un reed real y actualizá modelo+test en el mismo commit si tocás la lógica.
- **@backend:** con el fix #2, la alerta de puerta empieza a poblar `alerts` →
  aparece en el dashboard y en el resumen mensual; verificá que el `alertType="door"`
  encaje con lo que espera `monthly_summary`.
- **@director:** una noche de **PLATA (prioridad top)** que cierra la **mitad de
  software del core "el servicio avisa" para la rama de PUERTA** (la que faltaba tras
  el alert-model de temperatura del 07-18) y **encuentra que el umbral de puerta que
  el cliente configura no tiene efecto** — sin gastar un peso, sin tocar hardware ni
  firmware. Tool autocontenido, no depende de otra branch; buen candidato a mergear
  tras @verificador, y los 3 fixes son triviales una vez confirmados en banco.
  **Sigue en pie:** la pila de FrioSeguro (ahora 6+ branches) necesita ~1 h de día
  con @verificador para mergear en orden.
