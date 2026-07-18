# Nocturno LOCAL — 2026-07-18 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
La lógica que **dispara la alerta de temperatura** de FrioSeguro — o sea *lo que se
cobra* ("el servicio avisa") — **no tenía ningún test offline**. El único simulador
(`esp32_simulator.py`) no la modela: la **finge** (`alert_active = temp_avg > -10`).
Escribí un **modelo de referencia en Python puro** (`tools/alert_model.py`, espejo
fiel de `firmware_modular/alerts.h::checkAlerts`) + **12 tests** que pasan, sin
hardware ni nube. De paso, el modelo destapó un **bug latente** del firmware (con un
test que lo demuestra): **después de un descongelamiento largo, la primera lectura
crítica dispara la alerta al instante, salteándose `alert_delay_sec`** → riesgo de
falsa alarma post-defrost = molestia al cliente. **No lo corregí** (tocar firmware de
producción sin banco es lo que la doctrina prohíbe): queda listo para @firmware.
**Branch: `nocturno/local-2026-07-18-alert-model` (frioseguro), pendiente de merge.**

## Tarea elegida y por qué
**FrioSeguro es la PALANCA DE PLATA (prioridad #1 del portfolio, empatada con UNI).**
Las últimas 10 noches el worker evitó FrioSeguro porque sus 5 branches son **deuda de
deploy** (necesitan nube/hardware) — pero eso no significa que no haya software nuevo
y verificable offline. Recorrí los 4 `QUE_FALTA` y todas las branches:

- **galgas** (P0 octubre): todos los bloqueantes duros ya tienen branch (RX task08,
  SCADA, OTA A/B, vpp, energy, hold, docs, linaje-firmware ×7) o son hardware
  (galga física, LiPo, brownout) o firmware de producción prohibido de noche
  (#16 lazo de alerta abierto). Octubre es **segunda** prioridad, además.
- **datalogger** (P0): benchmark en `main`; el resto en branch (ina219/ecolora,
  sd-integrity ×2, rssi, ssid-casing de anoche) o hardware (piezo, alcance).
- **cosechador** (P2): gateado por compra, todo hardware.
- **FrioSeguro** (P1, la plata): revisé el CORE del producto — la decisión de alerta.
  **Ahí estaba el hueco de software real**: la lógica que decide si el cliente se
  entera de que se le rompe el freezer **no tiene red de seguridad**. Es la
  prioridad correcta (PLATA) y es 100% verificable offline.

Por qué el modelo y no otra cosa: es el patrón que ya funcionó en este repo
(`scan_secrets.py`, `lint_device_config.py` — tools stdlib con tests), aplicado a un
gap distinto: no config/secretos, sino **la lógica de runtime que se vende**.

## Qué hice — branch `nocturno/local-2026-07-18-alert-model` (frioseguro)
Sale de `main`. **3 archivos nuevos + nota en QUE_FALTA. Cero borrados, no toca
firmware, ni schema, ni nube.**

| Archivo | Qué |
|---|---|
| `tools/alert_model.py` (nuevo) | **Espejo fiel** de `alerts.h::checkAlerts/triggerAlert/clearAlert/acknowledgeAlert` en Python stdlib. `AlertEngine.tick(now_ms, temp, sensor_valid, defrost, cooldown)` decide como el firmware: alerta si `temp>temp_critical` sostenido `alert_delay_sec` s, con debounce 5 s y suspensión por defrost/cooldown. `replay()` corre una secuencia entera. Es un *oráculo* (reproduce hasta las rarezas del firmware), no una versión "limpia". |
| `tools/test_alert_model.py` (nuevo) | **12 tests** `unittest` (sin deps): normal nunca alerta · dispara solo al cumplir el delay · una bajada reinicia el conteo · defrost/cooldown suspenden · ack silencia pero no apaga · volver a normal apaga y resetea ack · debounce 5 s · **1 test [CARACTERIZACIÓN]** que demuestra el bug latente. |
| `docs/alert-model.md` (nuevo) | Por qué existe, correspondencia 1:1 con `alerts.h`, cómo correrlo, y el hallazgo con causa/evidencia/impacto/fix-candidato. |
| `QUE_FALTA.md` (#18) | Nota "EN BRANCH pendiente" en **main** (convención del repo: el índice de pendientes vive en main). |

## El hallazgo (evidencia ejecutable, no afirmación)
`alerts.h::checkAlerts` en las ramas de **defrost** (`:108-118`) y **cooldown**
(`:121-132`) hace `return` temprano **sin reiniciar** el acumulador estático
`highTempSec` (`:20`) ni `lastAlertCheck` (`:21`). Al salir del modo, la línea
`highTempSec += (now - lastAlertCheck)/1000` (`:141`) suma **toda la duración del
defrost** como si hubiera sido tiempo continuo sobre el crítico → con un defrost de
minutos, `highTempSec` supera `alert_delay_sec` en el **primer tick post-defrost** y
dispara al instante. Dirección **falso positivo**: un cliente que puso un delay alto
para tolerar el pico post-descongelamiento igual recibe la alerta. `test_alert_model.py::
TestDefrostAccumulatorStaleness` lo reproduce (defrost 10 min, `alert_delay_sec=300`
→ alerta en la 1ª muestra). **Fix candidato de 2 líneas** (documentado): reiniciar
`highTempSec=0` y `lastAlertCheck=0` en ambas ramas antes del `return`.

**Aclaración honesta:** `temp_max` (que el lint valida) **NO** dispara alerta y eso
**no es bug** — es el umbral de *warning/resumen* (lo consume el resumen mensual, aún
en branch), por diseño. El firmware alerta solo con `temp_critical`. Lo dejé escrito
explícito en el doc para que nadie lo lea como olvido.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-07-18-alert-model
git diff main --stat                                   # -> 3 nuevos + QUE_FALTA
python -m py_compile tools/alert_model.py tools/test_alert_model.py   # -> exit 0
python -m unittest tools.test_alert_model              # -> OK (12 tests)
```
**Resultado obtenido esta noche:** `py_compile` exit 0 + **12/12 OK** en <1 s. Sin
descargas ni toolchains pesados — cero riesgo de timeout.

## Qué quedó SIN verificar (necesita banco / device)
1. **Que el bug latente se manifieste en el device real** — el test lo demuestra
   sobre el modelo (que es fiel al código), pero la confirmación final es un ciclo de
   defrost real con temp crítica sostenida después. Tarea de @firmware en banco.
2. **El fix de 2 líneas** — no lo apliqué (firmware de producción sin banco = prohibido).
3. **Umbrales/tiempos reales de un freezer de comercio** — el modelo usa parámetros de
   ejemplo; los valores de cátedra (por rubro) los define @comercial/@firmware.

## Reglas respetadas
Solo software. Nada borrado, nada movido. **No toqué firmware** (`alerts.h` intacto),
ni schema, ni migraciones, ni nube, ni secretos. No toqué `data/` de galgas (otro
repo). Verificación instantánea con toolchain ya presente (Python), con la disciplina
de tiempo del 07-07. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-18-alert-model` (frioseguro, pusheado a origin; sale de `main`).
La nota #18 de `QUE_FALTA.md` está commiteada en **main** (`ddf5134`) siguiendo la
convención del repo (índice de pendientes en main).

## Notas para @verificador / @firmware / @director
- **@verificador:** el DoD es *"cada decisión de `alert_model.py` coincide con
  `alerts.h`, y el test de caracterización refleja el comportamiento real del
  firmware"*. Punto a atacar: **¿el modelo diverge del firmware en algún caso
  (p.ej. el orden de reset de `alert_acknowledged`, o la truncación entera del
  acumulador)?** El test es el oráculo; leé `alert_model.py` contra `alerts.h`
  línea por línea. Segundo punto: **¿el "bug" es realmente un bug o es tolerable?**
  El impacto (falso positivo post-defrost) está argumentado, pero la decisión final
  es de @firmware con datos de campo.
- **@firmware (dueño del fix):** el hallazgo y el fix candidato están en
  `docs/alert-model.md`. Si aplicás el fix, **actualizá `alert_model.py` y el test de
  caracterización en el mismo commit** — el oráculo debe seguir al firmware, si no
  el test empieza a mentir.
- **@director:** una noche de **PLATA** (FrioSeguro, prioridad #1) que agrega una red
  de regresión al **corazón del producto** (la alerta que se vende) **sin apilar deuda
  de deploy** — es un tool offline autocontenido, buen candidato a mergear directo tras
  @verificador. Sigue en pie el aviso de 10 noches: **la pila de FrioSeguro (ahora 6
  branches) necesita ~1 h de día con @verificador**; esta es chica y no depende de las
  otras 5.
