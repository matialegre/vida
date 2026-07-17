# Nocturno LOCAL — 2026-07-17 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa, que sea esto)

**Las últimas dos noches de análisis de galgas leyeron el sketch equivocado.** El repo tiene
**dos linajes de firmware de emisor**, y el cuartel documenta el **retirado**. El emisor de
producción es `firmware/ota_wm_pp/ota_wm_pp.ino` (**3.6.5**), no `firmware/esp_a_emisor/`
(**0.8.1**, retirado el 27-abr cuando nació el PLAN v5).

De ahí salen 3 cosas que cambian tus prioridades de octubre:

1. 🔴 **El sistema no entra en alerta solo.** En el firmware vigente, `in_alert` **no se
   calcula de la señal**: es el **perfil de compilación**. No hay umbral, ni hold, ni
   `set_thresholds`. El RX sólo muestra el flag que le llega. **El lazo señal→alerta no está
   cerrado**, y no figuraba en ningún `QUE_FALTA`.
2. 🔴 **`QUE_FALTA` #4 ("re-flashear B, A ya está en 0.1.3") es una instrucción dañina**:
   ejecutada tal cual, **downgradea B** al linaje retirado (le saca los 5 perfiles de energía
   y el gateway del PLAN v5).
3. 🟢 **Buena noticia: el bloqueante #1 está mejor de lo que dice el cuartel.** "RX completo"
   figura como el bloqueante rojo #1 de octubre; en realidad la **Task 08 está terminada** en
   `rx/task08-completo` (3.7.0) con la deuda del @verificador ya pagada (3.7.1, compila).
   **Falta banco, no código.**

**Causa raíz:** `act.md` se declara "fuente de verdad del estado" pero **termina en la sesión
8 (26-abr)** y nunca registró el corte de linaje del 27-abr. `QUE_FALTA.md` y `PORTFOLIO.md`
copiaron sus números de buena fe. Llevan ~3 meses desactualizados.

## Tarea elegida y por qué
**Resolver el hallazgo (a) que el turno 16-b dejó abierto** — *"contradicción de versión de
firmware: el repo dice 0.8.1, el cuartel dice 0.1.3; no se puede saber cuál rige sin mirar el
device"*. Ese turno lo listó como **una de las 2 decisiones que sólo Matías podía tomar**, y
como bloqueante del #4 (rojo de octubre).

Resultó **resoluble sin hardware, por arqueología del repo** — y la respuesta era que **la
pregunta estaba mal planteada**: no es `0.8.1` *vs* `0.1.3`; **las dos son viejas** y
pertenecen a un linaje que se retiró. La contradicción era el síntoma, no la enfermedad.

Por qué esta y no otra, recorridos los 4 `QUE_FALTA` y todas las branches:
- **Todo bloqueante duro sigue con branch** (galgas: RX/SCADA/OTA-A-B/vpp/energy/hold/docs ×7;
  datalogger: ina219/ecolora, sd-integrity ×2, rssi; FrioSeguro: **5 branches** = deuda de
  *deploy*, no de código — **10ª noche avisando**, no apilo más; cosechador: P2, gated por compra).
- **El benchmark MicroPython vs C del datalogger (#1) ya está en `main`** (commit `56cf0b0`,
  "listo para flashear") — no era tarea nueva, aunque el `QUE_FALTA` lo liste como bloqueante.
- **Corregir la base de evidencia le gana a producir más evidencia.** Veníamos de 4 noches de
  herramientas de análisis stdlib, y esta noche descubrí que **2 de ellas apuntaron a un
  archivo muerto**. Escribir una 5ª herramienta sobre cimientos equivocados habría sido
  cantidad, no calidad.

## La evidencia (toda verificable en el repo, sin hardware)

**La prueba que cierra el caso** — `docs/PLAN_v5_GATEWAY.md`, el plan **vigente**:
- §5, título literal: *"## 5. Emisores (A y B) — ya implementado en 3.5.0"* → y acto seguido
  *"`firmware/ota_wm_pp/ota_wm_pp.ino` ya tiene: …"* + la lista de features de producción.
- §8 (cronograma): `` `ota_wm_pp.ino` 3.5.0 | Claude #1 | ✅ listo ``
- `grep -rn "esp_a_emisor" docs/PLAN_v5_GATEWAY.md` → **cero resultados**.
- El RX se escribe como **compañero** de ese emisor, perfil `ALWAYS_ON` → por eso se llama
  `3.6.7-RX-p**always**`: comparte numeración y perfiles con el linaje vigente, no con `0.8.x`.

| | Linaje **RETIRADO** | Linaje **VIGENTE** |
|---|---|---|
| Sketch | `esp_a_emisor/` + `esp_b_emisor/` + `shared/` | `ota_wm_pp/ota_wm_pp.ino` |
| Versión | `0.8.1-*-otatest` | `3.6.5-<DEV>-<perfil>` |
| Líneas | 384 | **2015** |
| Plan | v3 | **v5 (vigente)** |
| Perfiles de energía | no tiene | 5 |
| Gateway RX (PLAN v5) | no | sí |

**Timeline** (mtimes de bins + `config.h` + `act.md`): `0.1.3` (26-abr, act.md sesión 8 — *acá
termina el doc*) → `0.8.0/0.8.1` (26-abr 23:32-23:52) → **corte 27-abr, nace PLAN v5** →
`3.3.0/3.3.1-pnorm` (27-abr) → `3.6.3→3.6.5-palways` (29-abr 21:40) → hoy: A/B **3.6.5**, RX
**3.6.7** → branch: RX **3.7.0/3.7.1**.

**El hueco de la alerta** (§4 del doc nuevo):
- `ota_wm_pp.ino:1411` y `:1900` — `bool is_alert = (strcmp(PROFILE_NAME, "ALERTA") == 0);`
- `grep -nE "th_v|threshold|self_alert|SELF_TRIGGER|hold_sec" ota_wm_pp.ino` → **vacío**.
- `esp_rx_receptor.ino:849` — `r->in_alert = doc["in_alert"] | false;` (sólo consume)
- `esp_rx_receptor.ino:115-116` — LED/buzzer salen de `stateA.in_alert || stateB.in_alert`.
- El `config.h` del RX no tiene ningún umbral.

## Qué hice — branch `nocturno/local-2026-07-17-linaje-firmware`
Sale de `main`. **3 archivos, sólo docs. Cero código, nada borrado, nada movido.**

| Archivo | Qué |
|---|---|
| `docs/ESTADO_FIRMWARE.md` (nuevo) | La reconstrucción completa: los 2 linajes, la prueba del PLAN v5, el timeline, qué versión rige cada device, el hueco de la alerta (§4), qué NO se puede saber sin device (§5), y 5 recomendaciones para @firmware/@director. |
| `QUE_FALTA.md` | Aviso arriba de todo + **#4 corregido** (era dañino) + #1 actualizado (Task 08 lista) + #2/#3 marcados 🔀 (escritos contra el sketch retirado) + **#16 nuevo** (lazo de alerta abierto, 🔴) + **#17 nuevo** (destino del linaje retirado). |
| `act.md` | Aviso al tope: **se corta en la sesión 8 (26-abr), no es el estado actual**; apunta a `ESTADO_FIRMWARE.md`. No borré nada — el histórico hasta el 26-abr sigue siendo válido y útil. |

## Corrección honesta de mis propios turnos previos
Los nocturnos del **07-15 (energy-budget)** y **07-16 (alert-hold-replay)** leyeron
`esp_a_emisor/`. En particular, el **"bug latente de correctness"** que el 16 elevó al cuartel
(*"`set_thresholds` cloud es no-op — `esp_a_emisor.ino:259` decide con `SELF_TRIGGER_VPP_V` e
ignora `th`"*) **es cierto en ese archivo, pero ese archivo no es producción**. Como bug de
octubre **queda anulado** — y reemplazado por uno peor (#16): no es que el umbral no se pueda
configurar, es que **no hay umbral**.

**Lo que sí se salva:** el análisis de datos de esas noches no depende del sketch. El replay
sobre `data/field_captures/` (falso positivo sostenido del canal B, hold=2-3 barato, 0
espurias en reposo) sigue válido y **ahora tiene destinatario correcto**: es el insumo para
diseñar el umbral que hay que **escribir** en `ota_wm_pp.ino`. Las herramientas no se tiran;
cambian de destinatario.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-17-linaje-firmware
git diff main --stat                                  # -> 3 archivos, solo docs

grep -n "ya implementado en 3.5.0" docs/PLAN_v5_GATEWAY.md   # el emisor vigente
grep -rn "esp_a_emisor" docs/PLAN_v5_GATEWAY.md              # -> CERO
grep -nE "th_v|threshold|self_alert|SELF_TRIGGER|hold_sec" firmware/ota_wm_pp/ota_wm_pp.ino  # -> vacio
grep -n "is_alert    =" firmware/ota_wm_pp/ota_wm_pp.ino     # -> strcmp(PROFILE_NAME,"ALERTA")
grep -rn "define FW_VERSION" firmware/*/config.h firmware/ota_wm_pp/*.ino
```
**Compilación del sketch vigente** (arduino-cli 1.4.1 + core esp32 3.3.8 **ya instalados —
cero descargas**, ~1 min, sin riesgo de timeout):
```bash
/c/Tools/arduino-cli/arduino-cli compile \
  --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs \
  --build-property "compiler.cpp.extra_flags=-DPROFILE_ALERTA -DDEVICE_TARGET_A" \
  --output-dir build/_verif_otawmpp_0717 firmware/ota_wm_pp
```
**Resultado obtenido esta noche: OK** — `1.226.600 bytes (62%)` de programa, globals
`48.792 (14%)`, exit 0. ⇒ el linaje que declaro vigente **compila hoy tal cual está en el
repo** (no es código muerto ni a medio terminar). El artefacto de build **no se commiteó**.

## Qué quedó SIN verificar (necesita device o cloud)
1. **Qué bin está flasheado hoy en A, B y RX.** El repo no lo sabe. Requiere Serial o
   `select id, firmware_version from devices` en Supabase. **Hacer esto ANTES de flashear B.**
2. **Si el `0.1.3` de A fue pisado por un flasheo de `3.x`.** Muy probable (los bins
   `3.6.x-A-*` existen, 29-abr) pero **no verificado**.
3. **Qué perfil tiene compilado cada emisor ahora** (`pnorm`/`palerta`/`palways`/…) — hoy eso
   determina si el sistema está o no "en alerta".
4. **Las sesiones 9+ de `act.md`** (27-abr→jul): sólo Matías sabe qué pasó en el banco.
   **No las inventé** — dejé el vacío marcado, que es peor mentira taparlo.

## Reglas respetadas
Nada borrado, nada movido, cero cambios de código/firmware/schema/migraciones. No toqué
`data/field_captures/` (sagrado — ni lo leí esta noche). No mDNS. Sin secretos. La única
verificación pesada (compilación) fue **con toolchain ya instalado** y con timeout. El branch
**no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-17-linaje-firmware` (pusheado a origin; sale de `main`).

⚠️ **Aviso de merge:** este branch y `nocturno/local-2026-07-16-b-docs-entrada` tocan los dos
`QUE_FALTA.md` saliendo de `main` ⇒ **conflicto probable**. Trivial: son notas en ítems
distintos (el 16-b toca el #14, éste el #1/#2/#3/#4/#14/#16/#17), se aceptan las dos. Sugerencia
de orden: **alert-hold (07-16) → docs-entrada (07-16-b) → éste**, porque éste corrige
afirmaciones de los dos anteriores y conviene que quede arriba.

## Notas para el @director / @verificador / @firmware / @cronista
- **Para el @director — esto reordena octubre.** El bloqueante #1 ("RX completo") está
  **hecho y esperando banco**, no código. En cambio apareció un bloqueante **que no estaba en
  la lista**: el lazo de alerta abierto (#16). El trabajo pendiente de galgas es **más de
  banco y menos de teclado** de lo que dice el PORTFOLIO. **No actualicé el PORTFOLIO** con el
  `0.1.3` viejo (línea 32) — es tuyo, y prefiero que la corrección la mires vos.
- **Para el @verificador:** el DoD es *"cada afirmación de `ESTADO_FIRMWARE.md` es verificable
  contra el repo sin hardware"*. Los greps de arriba son el test. El punto a atacar: **¿es
  `esp_a_emisor/` realmente el retirado y no el sucesor?** Mi caso se apoya en que el PLAN v5
  (vigente) lo ignora por completo y trata a `ota_wm_pp` como producción, más el hecho de que
  el RX comparte la numeración `3.x-p<perfil>` del linaje B. **Si eso se cae, se cae el
  informe entero** — es la afirmación que hay que romper primero.
- **Para @firmware:** el fix del #16 (cerrar señal→umbral→alerta en `ota_wm_pp.ino`) es la
  tarea grande de octubre. Los insumos de diseño ya existen (vpp-audit 07-11 + alert-hold
  07-16). **No lo hice yo**: tocar el firmware de producción sin banco es exactamente lo que
  la doctrina prohíbe.
- **Lección de harness (2 noches seguidas apuntando al mismo tipo de falla).** El 16-b arregló
  los docs de **entrada** (README/INDEX/CLAUDE frenaban a un agente cold-start); esta noche,
  los docs de **estado** (`act.md` mandó a dos noches al archivo muerto). Mismo patrón: **el
  proyecto P0 tiene docs que se declaran fuente de verdad y no lo son**. El costo ya no es
  hipotético: son **2 noches de análisis sobre un sketch retirado**. Sugerencia concreta para
  el #17: mover el linaje retirado a `firmware/_legacy/` (como ya hizo el repo `datalogger`
  con `firmwares/_legacy/`) — mientras `esp_a_emisor/` siga con el nombre más obvio del árbol,
  va a seguir cazando agentes.
- **10ª noche avisando:** la pila de **FrioSeguro (5 branches)** necesita **~1 h de día**. Es
  deploy/merge, no código. El worker no la toca de noche a propósito.
