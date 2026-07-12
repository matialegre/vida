# Nocturno LOCAL — 2026-07-12 (worker de la PC, Matías durmiendo)

## Tarea elegida y por qué
**FrioSeguro #4 — linter de config de provisioning de un dispositivo** (backend/
tooling, software puro). Es **PLATA** (tope de la jerarquía del portfolio).

Recorrí los 4 `QUE_FALTA` + los 8 nocturnos previos + los branches nocturnos de
los 4 repos. Estado de branches esperando merge: **galgas** (RX-deuda, vpp-audit),
**datalogger** (eco-lora, sd-integrity, rssi-calib), **frioseguro** (secret-scan,
resumen-mensual). Con la jerarquía **PLATA y UNIVERSIDAD primero, octubre segundo**:

- **FrioSeguro (PLATA)** es el tope. Los ítems de software ya tocados: #11 resumen
  mensual (branch 07-11-b), #6 secretos (branch 07-10-b). Verifiqué en código (no
  de memoria) que **#12 retención NO rinde tarea nueva**: ya existen
  `cron-cleanup-readings` (90 días, protege el último) y `cron-cleanup-alerts` —
  la retención está *escrita*, falta *deployarla* (nube, día). El **#4
  (credenciales de producción / "sacar defaults + credencial única por cliente")**
  estaba **sin tocar como software**: el 07-10-b cubrió la *filtración* de secretos,
  pero **nadie valida la corrección operativa de la config** de un device antes de
  flashearlo. Eso es software puro, 100% offline, y bloquea de hecho el primer
  abono (la definición de "vendible" exige "credenciales únicas por cliente").
- **datalogger/galgas** son octubre (2º) y sus wins de software limpios ya están
  en branches. No apilo más deuda de merge ahí.
- **cosechador** es P2 (arranca cuando datalogger cumple DoD) → no corresponde.
- **UNI** vive fuera de los 4 repos, pero esto **converge con Sistemas de Control
  Industrial**: el linter es la especificación formal de las guardas de un lazo de
  alarma umbral+delay+cooldown (crédito doble, PORTFOLIO §CONVERGENCIA).

Encaja con el patrón que funciona (herramienta offline stdlib + tests + docs,
mergeable ya) y con "UNA tarea bien hecha por noche". No estaba en ningún branch.

## Hallazgo que motivó la tarea (leyendo el código real)
Un error de config **no falla la compilación** — falla en el comercio del cliente
semanas después. Cuatro modos de falla, cada uno anclado a código:
- **Orden de umbrales**: `alerts.h::checkAlerts` (línea 137) dispara la alerta
  crítica con `temp > temp_critical`; `_shared/monthly_summary.ts` cuenta
  excursiones vs `temp_max`. Si `temp_min < temp_max < temp_critical` se rompe,
  las alertas **no disparan nunca o disparan siempre**. Nada lo chequea.
- `alert_delay_sec = 0` → alerta en cada pico transitorio (defrost) = tormenta de
  falsas alarmas = **churn**.
- `OTA_PASSWORD ""` (config.h:176) con OTA on → reflasheo abierto en la LAN del
  comercio.
- Bot+chat de Telegram compilados (config.h:94-95) → alertas de todos los clientes
  al mismo chat.

(Además detecté, sin actuar por ser firmware+hardware: el firmware solo alerta
sobre `temp_critical`, nunca sobre `temp_max` —la "warning"—; y las alertas de
puerta de `door_sensors.h` solo mandan Telegram, no persisten `door_events`, tabla
que el resumen mensual lee. Anotado para @firmware/@backend, ver más abajo.)

## Qué hice — branch `nocturno/local-2026-07-12-lint-device-config` (sale de `main`)
Software **aditivo**, solo lectura. No toqué firmware, ni schema, ni datos.

| Archivo | Qué |
|---|---|
| `tools/lint_device_config.py` | Linter stdlib. Entra por `--from-header config.h` (extrae los `#define DEFAULT_*` + provisioning, deriva `has_sim800` de `PLACA_NUM∈{4,5}`) o `--json-in` (fila de device de Supabase) o JSON por stdin. 10 chequeos con severidad (error/warn/info): orden y rango de umbrales, `alert_delay`, `door_open_max`, `defrost_cooldown`, `OTA_OPEN`, `TELEGRAM_HARDCODED`, `AP_OPEN`, `SIM_APN`. **Umbrales obligatorios** (error si faltan); **provisioning opcional** (solo corre si el campo está → una fila de Supabase valida solo umbrales, el `config.h` valida todo). Exit **0/1/2** como gate pre-flash, `--json`, `--fail-on {error,warn}`. Fuerza stdout a utf-8 (consola Windows cp1252 rompía con `°`/`→`). |
| `tools/test_lint_device_config.py` | **35 checks** (fixtures en runtime, sin secretos reales ni tocar archivos del repo): cada chequeo, extracción de `config.h` sintético, carga JSON plano/anidado, `_strip_comment` con `//` dentro de comillas, y exit codes de `main()` por subprocess. |
| `docs/lint-device-config.md` | Problema, tabla de fallas ancladas a código, uso, chequeos, salida real, convergencia UTN. |
| `QUE_FALTA.md` (#4) | Anotado "EN BRANCH … pendiente de merge". |

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-07-12-lint-device-config

# 1) Sintaxis
python -m py_compile tools/lint_device_config.py tools/test_lint_device_config.py

# 2) Self-test (sintético, no toca archivos del repo)
python tools/test_lint_device_config.py            # -> "OK: 35 checks", exit 0

# 3) Lint real del firmware que se flashea
python tools/lint_device_config.py --from-header firmware_modular/config.h  # -> exit 1
```
**Resultado obtenido esta noche** (Python 3.14.3): `py_compile` **OK**; self-test
**OK: 35 checks** (exit 0); lint real del `config.h` (PLACA_NUM=4):

```
lint_device_config — 4 hallazgo(s): 1 error, 1 warn, 2 info
  [ERROR] OTA_OPEN: OTA habilitado con OTA_PASSWORD vacio...
  [WARN ] TELEGRAM_HARDCODED: bot+chat de Telegram compilados en el firmware...
  [info ] AP_OPEN: AP de configuracion sin password (portal cautivo, por diseño)...
  [info ] SIM_APN: APN generico/vacio con SIM800 habilitado...
VEREDICTO: config NO apta — 1 hallazgo(s) >= 'error'
```
Los **umbrales por defecto están bien** (`-40 < -18 < -10`, delay 300 s) → sin
hallazgo. Lo que marca es que una placa flasheada **tal cual el `config.h`** aún
**no es client-ready** — justo el pendiente del #4.

## Qué quedó SIN verificar / SIN hacer (necesita día — hardware/nube/decisión)
- **Definir `OTA_PASSWORD` y ruteo de chat por cliente** y sumar el linter al alta
  de un cliente nuevo. Es decisión de Matías + @firmware/@backend, no nocturna.
- **Gaps de integración detectados (para @firmware/@backend, NO tocados):**
  (a) el firmware solo alerta sobre `temp_critical`; `temp_max` se envía a la API
  pero no genera alerta → un cliente por encima de `temp_max` durante horas no
  recibe aviso. (b) las alertas de puerta solo mandan Telegram y **no persisten**
  en la tabla `door_events` que el resumen mensual (#11) lee → la sección de
  puertas del resumen quedaría vacía en producción. Ambos son decisiones de diseño
  de firmware+schema; los dejo documentados, no los improviso de noche.

## Reglas respetadas
Nada borrado. No toqué firmware, ni schema, ni datos, ni migraciones. No mDNS (no
aplica). **No se copiaron secretos**: el linter enmascara (no imprime token ni
APN; los detecta por presencia). Software aditivo en branch nuevo salido de `main`.
No stageé `tools/__pycache__/`. Sin compilación pesada: verificación instantánea
(Python puro), sin timeouts. El branch **no se mergea** hasta que @verificador lo
revise — pero la herramienta + tests son mergeables ya (no dependen de nube ni
hardware).

## Branch
`nocturno/local-2026-07-12-lint-device-config` (pusheado a origin, 1 commit). Sale
de `main`.

## Nota para el @director / @cronista
- **FrioSeguro acumula 3 branches de PLATA** esperando una sesión de día: #6
  secret-scan (07-10-b), #11 resumen mensual (07-11-b), #4 linter (hoy). Los tres
  son **software listo**; lo que falta es la sesión de Supabase/decisión de Matías
  (rotar claves, deployar functions, definir credenciales por cliente). Sigue en
  pie la sugerencia del 07-11-b: **agrupar un bloque backend FrioSeguro de ~1h**.
- **Drift menor detectado**: el QUE_FALTA #12 (retención pg_cron) está esencialmente
  **hecho** en código (`cron-cleanup-readings`/`cron-cleanup-alerts`) — falta
  deployarlo, no escribirlo. Convendría reescribir el ítem como "deployar retención"
  cuando alguien lo toque, para no re-evaluarlo cada noche.
