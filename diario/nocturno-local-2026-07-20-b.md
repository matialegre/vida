# Nocturno LOCAL — 2026-07-20 turno B (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
La decisión de **OTA** de galgas — "¿me actualizo? ¿con cuál `.bin`?", que en octubre
tiene que correr **sola, por aire, en planta** — vivía entera en
`firmware/shared/supabase_client.cpp` y **no tenía ni un test offline**. Escribí su
modelo/oráculo espejo 1:1 (`tools/ota_decision_model.py`, stdlib) + **23 tests** + doc.
Y al reproducir la lógica saltó un hallazgo **🔴 latente y peligroso**: la compuerta
que decide si una versión es "más nueva" usa **`strcmp` (comparación lexicográfica de
string), no semver**. Hoy no molesta porque el firmware va por `0.1.x`; pero **en el
primer bump a dos dígitos se rompe**: `0.9.0 → 0.10.0` **no actualiza** (el equipo
queda clavado para siempre) y `0.10.0` con un `0.9.0` publicado **downgradea** (con el
`ESP.restart()` del flujo OTA, riesgo de loop). **No corregí firmware** (es de
@firmware/@backend, en banco). **Branch: `nocturno/local-2026-07-20-b-ota-decision-model`
(galgas), pendiente de merge.**

## Tarea elegida y por qué
**galgas #5 (P0 — parada de octubre).** El ítem 🟡 "OTA que distinga A/B". 100 %
software, sin hardware, no destructivo, patrón probado (modelo/oráculo offline).

Recorrí los 4 `QUE_FALTA`, todos los branches nocturnos y los nocturnos previos. Por qué ésta:
- **FrioSeguro (P1, PLATA = top):** el **turno A de HOY** (07-20) ya cerró
  `door-alert-model`. No apilo en el mismo repo la misma noche; además su pila ya
  tiene 6+ branches esperando merge.
- **datalogger (P0 octubre):** cerró `rv1-mesh-model` el 07-19-b (hace 1 día). No apilo.
- **cosechador (P2):** cerró `modelo-energia` el 07-18-b; lo que queda es compra/hardware.
- **galgas (P0 octubre):** cerró `rx-detection-replay` el 07-19, pero ese modeló la
  **decisión de alerta del RX**, no el **OTA**. El OTA es el segundo ítem 🟡 sin ningún
  test offline y es **crítico para octubre** (equipos que se actualizan solos en planta).
  Ese era el pedazo verificable sin hardware que faltaba.

Por qué el modelo-y-test: mismo patrón que ya funcionó (alert/door en frioseguro,
vpp/rx en galgas, mesh en datalogger, energía en cosechador) aplicado al **subsistema
OTA que faltaba**, con un ancla dura: **auditar la compuerta de versión real** contra
lo que un check correcto (semver) decidiría.

## Qué hice — branch `nocturno/local-2026-07-20-b-ota-decision-model` (galgas)
Sale de `main`. **3 archivos nuevos + 1 nota en QUE_FALTA. Cero borrados, no toca
firmware, ni la nube, ni otra branch.** (`git diff --cached --stat` → 554 inserciones,
4 archivos.)

| Archivo | Qué |
|---|---|
| `tools/ota_decision_model.py` (nuevo, 239 líneas) | Espejo 1:1 de la decisión de OTA. `select_firmware_row(rows, device_id, device_type)` reproduce la query `?or=(device_id.eq.<ID>,and(device_id.is.null,device_type.eq.<TYPE>))&order=device_id.desc.nullslast,released_at.desc&limit=1` (per-device gana a global = **el mecanismo de distinción A/B del #5**). `version_gate_firmware(latest, current)` reproduce EXACTO `sc.cpp:239` (`strcmp(latest,current)<=0 → no update`). `version_gt_semver` = comparador semántico de referencia (NO existe en el firmware; solo para exponer la divergencia). `ota_decision(...)` = flujo completo. CLI: `--demo-hallazgo` (exit 1) y `--current X --latest Y`. |
| `tools/test_ota_decision_model.py` (nuevo) | **23 tests** `unittest` (sin deps, no tocan hardware): compuerta (update/igual/menor/patch un dígito/sufijo), **regresión del hallazgo #1** (0.9→0.10 pierde update, 0.10→0.9 downgrade, coincide mientras no cruce dos dígitos), semver de referencia, selección de fila (solo global, per-device gana a global, **A no toma la fila de B**, released_at desc, device_type distinto), y flujo E2E (update normal, sin fila, sin storage_path, cuelgue en 0.10, A y B reciben firmware distinto). |
| `docs/ota-decision-model.md` (nuevo) | Por qué existe, tabla de correspondencia 1:1 con el `.cpp`, los 2 hallazgos con evidencia, cómo verificar, y alcance honesto (qué NO cubre: download/flasheo, gates de energía/RSSI, `ota_forced`). |
| `QUE_FALTA.md` (galgas) | Nota "EN BRANCH pendiente" bajo #5. |

## Los hallazgos (NO corregidos — son de @firmware/@backend, en banco)

### 🔴 #1 — La compuerta de versión usa `strcmp` (lexicográfico), no semver
`parseFirmwareRow` (`supabase_client.cpp:239`, y el path legacy `:332`) decide si
actualizar con `strcmp(latest_version, current_version) <= 0`. `strcmp` compara **byte
a byte**, no por valor numérico. Consecuencias, todas verificables offline:
- **Pierde updates reales al cruzar a dos dígitos:** `strcmp("0.10.0","0.9.0") < 0`
  (porque `'1' < '9'`) → el firmware trata `0.10.0` como **más viejo** → **no
  actualiza**, queda clavado en `0.9.0`. Igual `0.1.9 → 0.1.10`. `act.md` va por
  `0.1.2 → 0.1.3`: **el bug es latente, se dispara en el primer bump a dos dígitos.**
- **Downgrade espurio:** en `0.10.0`, si la fila más nueva es `0.9.0`,
  `strcmp("0.9.0","0.10.0") > 0` → la trata como más nueva → **downgrade** + posible
  loop de reboot.
- **Sufijos frágiles:** los `FW_VERSION` reales llevan sufijo (`"0.8.1-A-otatest"`);
  la comparación es de string completo.

Salida real de esta noche (`--demo-hallazgo`, exit 1):
```
HALLAZGO #1 - la compuerta de version usa strcmp (lexicografico), no semver
  Escenario: equipo en 0.9.0, se publica 0.10.0 (un update REAL).
  Firmware REAL (strcmp<=0):   NO actualiza (se cuelga en 0.9.0)
  Lo CORRECTO (semver):        ACTUALIZA
  -> divergencia observable: SI
    current=0.1.9    latest=0.1.10   firmware=skip   correcto=update [PIERDE UPDATE]
    current=0.10.0   latest=0.9.0    firmware=update correcto=skip   [DOWNGRADE]
```
**Fix candidato (banco):** comparar por semver en `parseFirmwareRow` (~10 líneas). Al
aplicarlo, cambiar `version_gate_firmware` del modelo y actualizar
`TestHallazgo1StrcmpNoEsSemver` en el mismo commit.

### 🟠 #2 — `unique(device_type, version)` no incluye `device_id`
El schema (`20260425000001_initial_schema.sql:104`) tiene `unique (device_type,
version)`. La migración per-device (`20260426170000_firmware_per_device.sql`) agregó
la columna `device_id` **pero no tocó el unique** → no se puede publicar la misma
`version` como fila per-device (device_id='A') y como global del mismo device_type
(ni la misma version para A y B). La resolución per-device del cliente asume que esas
filas coexisten. **Fix:** `unique (device_type, version, device_id)` (migración
append-only, coordinar con @backend).

### Nota sobre el #5 (aclaración de estado)
El QUE_FALTA dice "hoy comparten target `emisor`", pero al leer el código los 3 equipos
**ya llaman** `supabaseFirmwareCheckForDevice(DEVICE_ID, DEVICE_TYPE, ...)`
(`esp_a_emisor.ino:343`, `esp_b_emisor.ino:343`, `esp_rx_receptor.ino:970`) — o sea el
**mecanismo** de distinción A/B (columna `device_id` + query per-device) **existe y
está wired**. Lo que faltaba era el **test que lo demuestre** (ahora está) y publicar
filas per-device en la tabla (backend/día). El bug real que bloquea el OTA confiable
para octubre no es el A/B sino la compuerta de versión (#1).

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-20-b-ota-decision-model
git diff main --stat                                   # -> 4 archivos, 554 inserciones
python -m py_compile tools/ota_decision_model.py tools/test_ota_decision_model.py   # exit 0
cd tools && python -m unittest test_ota_decision_model   # -> OK (23 tests)
cd .. && python tools/ota_decision_model.py --demo-hallazgo   # -> HALLAZGO #1, exit 1
python tools/ota_decision_model.py --current 0.9.0 --latest 0.10.0   # -> DIVERGENCIA, exit 1
```
**Resultado obtenido esta noche:** `py_compile` exit 0 · **23/23 OK** en <0.01 s ·
`--demo-hallazgo` marca la divergencia (exit 1) · `--current 0.9.0 --latest 0.10.0`
divergencia. Sin descargas ni toolchains pesados — **cero riesgo de timeout**
(disciplina del 07-07 respetada).

## Qué quedó SIN verificar (necesita banco — no se cierra de noche)
1. **Que el fix #1 (semver) se comporte bien en hardware** — requiere publicar dos
   versiones que crucen el dígito (p. ej. equipo en `0.9.0`, publicar `0.10.0`) y ver
   que el ESP actualiza. Hoy no se puede sin banco + nube.
2. **Que la resolución per-device funcione E2E con la tabla real** — el modelo asume
   la semántica de PostgREST (`device_id.desc.nullslast`); confirmar contra Supabase
   real que devuelve la fila per-device antes que la global.
3. **El fix #2 (migración del unique)** — que no rompa filas existentes; es de @backend.

## Reglas respetadas
Solo software. Nada borrado, nada movido. **No toqué firmware** (`supabase_client.cpp`
intacto — los hallazgos se flagean, no se corrigen), ni schema, ni nube, ni secretos.
No toqué `data/field_captures` (sagrado). No toqué otros repos. Identidad git = Matías.
El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-20-b-ota-decision-model` (galgas, pusheado a origin; sale de `main`).

## Notas para @verificador / @firmware / @backend / @director
- **@verificador:** el DoD es *"cada decisión de `ota_decision_model.py` coincide con
  `supabase_client.cpp::supabaseFirmwareCheckForDevice`+`parseFirmwareRow`, y el
  hallazgo #1 es real"*. La tabla de correspondencia 1:1 está en el doc. Puntos a
  atacar: (a) **¿el `strcmp` de `sc.cpp:239` es el gate?** Confirmá `<=0 → return
  false`. (b) **¿la resolución del modelo (`order=device_id.desc.nullslast`) coincide
  con PostgREST?** (per-device gana a global, luego `released_at.desc`). (c) **¿el #2
  es real?** `grep -n "unique" backend/supabase/migrations/20260425000001_initial_schema.sql`.
- **@firmware (dueño del fix #1):** cambiar `parseFirmwareRow` a comparación semver
  (~10 líneas); confirmá en banco con dos versiones que crucen el dígito y actualizá
  modelo+test en el mismo commit.
- **@backend:** #2 es una migración append-only del unique; validá que no rompa filas
  existentes. Y para que el #5 (A/B) funcione de verdad hay que **publicar filas
  per-device** en `firmware_versions` (device_id='A'/'B').
- **@director:** una noche de **P0 octubre** (segundo en la jerarquía tras PLATA/uni)
  que cierra el **test offline del OTA que faltaba** y encuentra que **la compuerta de
  versión se va a colgar en el primer bump a dos dígitos** — sin gastar un peso, sin
  tocar hardware ni firmware. Complementa al turno A de hoy (FrioSeguro/PLATA), sin
  apilar en el mismo repo. **Sigue en pie:** las pilas de branches nocturnos (galgas,
  frioseguro, datalogger, cosechador) necesitan sesiones de día con @verificador para
  mergear en orden.
