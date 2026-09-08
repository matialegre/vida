# Nocturno local — 2026-09-07-b

**Trabajador:** worker nocturno local (Matías durmiendo). **Segundo turno** de la
noche — el primero fue `nocturno-local-2026-09-07.md` (galgas, la trama que nadie
leyó nunca).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA — prioridad #1 de la
jerarquía**), zona `firmware_modular/` + `tools/` + `docs/`.
**Branch:** `nocturno/local-2026-09-07-b-el-corte-que-nadie-avisa` (pusheado, `69dc151`).
**Sale de `main` (`2ac3a7d`) limpio**, sin ningún otro branch mergeado adentro.
**No toca SQL, ni el panel, ni el servidor, ni `alerts.h`, ni `sensors.h`, ni
`door_sensors.h`, ni `hardware/`.**

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_frio_b`, ya
eliminado) porque el árbol de `frioseguro` tiene el KiCad de Matías sin commitear
(TermoVigía Mini/Lite) y un `checkout` lo habría tocado. **Verificado al
terminar: el árbol quedó idéntico**, en el branch `09-04-b` donde estaba, con los
mismos 9 archivos modificados/sin trackear.

---

## TL;DR

> **El aviso de corte de luz no salía nunca, y el módulo que lo mandaba jamás
> había compilado.** `power_monitor.h` llamaba dos veces a
> `sim800SendPowerAlert()`, **una función que no existe en ningún archivo del
> repo** — el `#include` en el `.ino` da error de linkeo. Y adentro, el aviso se
> mandaba con `if (internetAvailable) …` y `alertSent = true` **afuera** del
> `if`: en un comercio el router no está en la UPS, así que **el evento que
> dispara el aviso es el mismo evento que rompe su único canal de salida**. No es
> "correlacionado" como el de la puerta de anoche: es **garantizado**.

## Por qué esta tarea

1. **La dejó marcada el turno anterior.** El informe del 09-06-b la nombra
   textualmente: *"`power_monitor.h` tiene los mismos dos bugs y esta vez SÍ está
   sin integrar… **Candidato claro para la próxima noche**"*. Y es **PLATA**, la
   prioridad #1.
2. **Para un comercio el corte de luz es EL evento**, y es de lo que más se habla
   en el pitch de TermoVigía. Las últimas noches cerraron temperatura (08-29,
   09-04-b) y puerta (09-06-b). Faltaba esta.
3. **Se hace entera sin hardware.** La decisión —cuándo hay evento, qué dice el
   mensaje, cuánto duró— no necesita ni un optoacoplador.
4. **Estaba libre.** Revisé los branches abiertos: sólo el `09-01-b` toca
   `power_monitor.h`, y es complementario (ver "Colisión").

## Lo que encontré, en orden de gravedad

### 0. El módulo nunca compiló

```c
extern void sim800SendPowerAlert(bool powerLost);   // no existe
sim800SendPowerAlert(true);
sim800SendPowerAlert(false);
```

`sim800.h` define `sim800SendAlert(const String&)`, que es **otra función**.
Grep en todo el repo: las únicas tres apariciones de `sim800SendPowerAlert` son
esas. **Nadie podía haber corrido este código**, y por eso los otros cuatro
defectos siguen ahí desde siempre.

La nota que encabezaba el archivo —*"Este módulo NO está integrado aún. Solo
definiciones."*— era doblemente engañosa: **no eran "solo definiciones"** (tenía
la lógica completa, 183 líneas) y **lo que faltaba no era integrarlo, era que
compilara**. Es el mismo tipo de comentario que mentía en `door_sensors.h`
anoche, pero al revés: allá decía que no corría y sí corría.

Y su único canal de aviso era el **SIM800, descartado del producto el
2026-07-13** (está escrito en `config.h` línea 25). Un evento crítico, con un
canal muerto y una función inexistente.

### 1. El corte apaga el router

```c
if (state.internetAvailable && config.telegramEnabled) {
  sendTelegramAlert("⚡ *CORTE DE LUZ* … funcionando con batería de respaldo.");
}
powerState.alertSent = true;
```

**Tercer branch consecutivo con este patrón** (`faultAlerted1 = true` en el
08-29, `door->alertSent = true` en el 09-06-b, `lastSupabaseSync = now` en el
08-26). Pero acá no hay que argumentar que el escenario es probable: **es el
escenario, siempre**.

**La decisión que sale de ahí** — y es la parte de diseño que me parece la buena:
el aviso pendiente sobrevive al corte y sale **cuando vuelve la luz**. Y cuando
sale ya no puede decir *"el sistema está funcionando con batería de respaldo"*
—eso ya es falso—, así que **cambia de tiempo verbal y el aviso de corte y el de
restauración colapsan en uno solo**:

> **HUBO UN CORTE DE LUZ.** El equipo estuvo 40 minutos sin energía eléctrica.
> La luz ya volvió. Revisá la mercadería: durante el corte el freezer no enfrió.

En este modelo ése **no es el caso raro: es el camino normal**. El *"volvió la
luz"* queda sólo para el equipo que sí tuvo internet durante el corte (router en
UPS, o corte de una sola fase), que es donde ese mensaje efectivamente cierra un
evento que el cliente ya había escuchado.

### 2, 3 y 4

- **Arrancar sin luz era silencio permanente.** El init ponía
  `acPowerPresent = false` y se callaba; el check sólo avisa ante un **cambio**.
  El equipo que bootea con batería en medio del corte —el caso normal si el corte
  lo rebooteó— no decía nada, y **lo primero que el cliente escuchaba era una
  "LUZ RESTAURADA" de un corte que nunca le avisaron**. Mismo patrón que el bus
  vacío al bootear del 08-29.
- **La duración post-reboot era basura.** `(millis() - powerLostTime)/60000` con
  `powerLostTime = 0` tras un reboot ⇒ **"Duración del corte: 0 minutos"** para un
  corte de 3 horas.
- **Debounce simétrico de 3 s.** La luz que vuelve y se cae tres veces en un
  minuto —que es cómo vuelve la luz de verdad— generaba un par de mensajes por
  parpadeo.

## Qué se entregó

`firmware_modular/power_alert_model.h` — **puro** (sin Arduino, sin HTTP, sin
`analogRead`) e **incluido** por `power_monitor.h`: no es un espejo, lo que se
testea es lo que se flashea. Mismo criterio que `sensor_fault_model.h` (08-29),
`temp_report_model.h` (09-04-b), `door_alert_model.h` (09-06-b) y
`trama_revd.h` (galgas, anoche).

Además de la promoción `PN_LOST → PN_WAS_OUT`:

- **Debounce asimétrico**: el corte se declara rápido (3 s, hay que avisar), la
  restauración lenta (15 s, no cantar victoria sobre un parpadeo).
- **Piso de reporte**: un corte que **ya terminó, nunca se avisó y duró menos de
  60 s** se descarta — es un parpadeo que el cliente no vio, y avisarlo es la
  tormenta de falsas alarmas que hace que silencie el bot. **No** aplica al corte
  arrancado en boot (no se sabe cuánto duró) ni al que ya se avisó.
- **Duración como PISO** (`"al menos N minutos"`) cuando el equipo no vio arrancar
  el corte. El equipo no inventa un número que no midió — misma doctrina que los
  flags de validez de temperatura del 09-04-b.
- **Fila en `alerts`** (`alert_type='power'`). El código viejo no lo registraba en
  ningún lado: el evento era invisible en el panel y **ausente del resumen
  mensual** ("este mes: 2 cortes, 0 pérdidas"), que es lo que se vende como la
  razón para seguir pagando el abono.

## Lo que salió al escribirlo (y no estaba en el plan)

**El rate limit de Telegram descarta en silencio.** `sendTelegramMessage()` tiene
arriba de todo `if (millis() - state.lastTelegramAlert < 300000) return;` y es
`void`: **el llamador no se entera de que su mensaje no salió**. Y el corte de luz
calienta el freezer, o sea que dispara también la alerta de temperatura: que el
aviso de corte caiga dentro de la ventana de 5 minutos de otro aviso **es
probable, no excepcional**. La entrega ahora replica las dos puertas
(token corto + ventana) antes de dar el aviso por entregado.

**Una lectura de ADC suelta no alcanza para el boot.** `analogRead()` del ESP32 es
ruidoso y una lectura mala en el arranque **arma un aviso de corte que no pasó**.
El init promedia 8 muestras.

## Sigue APAGADO, y es a propósito

`POWER_MONITOR_ENABLED 0` en `config.h`; el `.ino` incluye, inicializa y corre el
módulo **sólo bajo ese `#if`**. Sin el optoacoplador (PC817) en GPIO34 el pin
queda **flotando** y el equipo avisaría cortes que no ocurrieron: es
**exactamente el bug de la "puerta fantasma"** de anoche. El gate es de
**compilación** y no de runtime a propósito — una placa sin el circuito **ni
siquiera lleva el código**.

## Cómo verificarlo (comandos exactos, sin hardware, ~6 minutos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-09-07-b-el-corte-que-nadie-avisa

# 1) la decisión, contra el header que se flashea
g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_power_alert.exe tools/test_power_alert.cpp
./tools/test_power_alert.exe

# 2) que compile como se flashea HOY (módulo apagado)
arduino-cli compile --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" firmware_modular

# 3) que compile con el módulo PRENDIDO  <- esto prueba que ya linkea
arduino-cli compile --clean --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" \
  --build-property "compiler.cpp.extra_flags=-DPOWER_MONITOR_ENABLED=1" firmware_modular
```

**Resultados obtenidos esta noche:**

- `test_power_alert.exe` → **565 checks, 0 fallos, sin warnings**. Los bloques 3,
  7 y 8 están escritos como **regresión** (fallan contra la lógica vieja), y
  comprobé con **7 mutantes** que reimplantan los defectos que los tests los
  matan:

  | mutante | qué reimplanta | checks que fallan |
  |---|---|---|
  | 1 | el aviso se consume aunque no se haya entregado | 6 |
  | 2 | debounce simétrico (la vuelta se declara en 3 s) | 2 |
  | 3 | arrancar sin luz no arma el aviso | 4 |
  | 4 | la restauración nunca colapsa: siempre "LUZ RESTAURADA" | 7 |
  | 5 | el aviso pendiente se descarta cuando vuelve la luz | 7 |
  | 6 | sin piso de reporte: se avisa cualquier parpadeo | 3 |
  | 7 | la duración del corte en curso se congela en 0 | 3 |

  **7/7 muertos**, y el header quedó restaurado (re-corrí el test después: 565/0).
- **Compilación apagado** → **exit 0, 65 % flash (1.288.712 B), 16 % RAM
  (53.784 B), 0 warnings/errors**.
- **Compilación PRENDIDO** → **exit 0, 1.297.544 B flash, 53.912 B RAM, 0
  warnings/errors** (+8.832 B / +128 B). **Ésta es la verificación que importa**:
  es la prueba de que el módulo por fin linkea.

**Dos errores míos que corregí en el camino** (los anoto porque los dos eran del
verificador, no del código): la primera corrida del test daba 5 fallos por
aritmética mía —el reloj del debounce arranca en la primera muestra que cambió,
no en el boot, y mi helper `hold()` no cruzaba el wrap de `millis()`—; y **la
primera corrida de mutantes dio "0 fallan" en los 7**, que reporté como
sospechoso en vez de como éxito: era un `./tmp/mut.exe` en vez de `/tmp/mut.exe`,
o sea el binario no corría. Un mutante que "muere" sin ejecutar nada no prueba
nada.

## Qué quedó SIN verificar (pide banco y hardware)

1. **Armar el detector** (PC817 + divisor desde 220 V a GPIO34) y **medir qué lee
   el ADC con luz y sin luz**. ⚠️ **`POWER_THRESHOLD 2000` es un número heredado
   que nadie midió** — sale del archivo original, no de un ensayo. Todo lo de
   arriba decide bien sobre una entrada cuya calibración no está probada.
2. **⚠️ Decisión pendiente que no es mía: con qué batería de respaldo sale el
   producto.** Hoy **no hay ninguna**. Sin backup, el corte de luz apaga el ESP32
   y no hay nada que avisar en el momento: el equipo bootea cuando vuelve la luz
   y el único aviso posible es el de boot (duración como piso). Es una decisión de
   hardware y de costo. [@hardware + @comercial]
3. **Cortar la luz de verdad** y cronometrar: el aviso tiene que salir cuando
   vuelve el router (hasta 60 s después), en pasado y con la duración real.
4. **Parpadeo de red**: un solo aviso, no cuatro.
5. **UNA fila en `alerts`** con `alert_type='power'` por evento, y que el panel y
   el resumen mensual la cuenten. Confirmar que ese `alert_type` no rompe el
   render del panel (mismo chequeo que pedía el `sensor_fault` del 08-29).

## Colisión (la revisé mal la primera vez y la corregí)

**Escribí primero que no había ninguna, y era falso.**
`nocturno/local-2026-09-01-b-el-aviso-que-no-sale` **también edita
`power_monitor.h`** (commit `f13e2fe`). Su propio mensaje de commit avisa que ese
archivo **no pasó por el compilador** (*"power_monitor.h y current_sensor.h no
los incluye el .ino"*), y por eso dejó en pie los dos `sim800SendPowerAlert()`:
**con ese branch el módulo sigue sin linkear**.

**Son complementarios y ninguno reemplaza al otro:** él resuelve el
**transporte** (cola por fuente, reintento, resultado real del HTTP); éste, la
**decisión** (cuándo hay evento, qué dice, cuánto duró). Él vio el mismo agujero
de fondo y lo atacó del lado del transporte — pero una cola genérica **no puede
reescribir el mensaje que lleva adentro**, y el texto encolado durante el corte
dice *"está funcionando con batería de respaldo"*: cuando la cola lo entregue
—al volver el router, o sea al volver la luz— **ese texto ya es falso**. Por eso
la promoción a "hubo un corte" tiene que vivir en la capa de la decisión.

**Resolución al mergear** (cualquier orden, conflicto textual y chico): dentro de
`powerDeliverPending()`, `delivered = telegramNotify(msg, TG_SRC_POWER, false);`
y borrar `powerTelegramWindowOpen()`. Detalle en `docs/power-alert-model.md` §8.

## Anotado y NO tocado

- **Flag de runtime.** Cuando se prenda en el parque va a hacer falta un
  `config.powerEnabled` editable desde la web y sincronizado desde Supabase, como
  `config.doorEnabled` (es la lección del 09-06-b). Toca `types.h`, `storage.h`,
  `web_api.h`, `html_ui.h` y el pull de config: es su propio branch, y hoy no
  tiene sentido porque **no hay ni una placa con el detector puesto**. [@firmware]
- **`current_sensor.h` (255 líneas) tampoco lo incluye el `.ino`** y el 09-01-b lo
  tocó con la misma advertencia de "no pasó por el compilador". **No lo revisé.**
  Si tiene un fantasma como éste, no se va a saber hasta que alguien lo incluya.
  Candidato para una próxima noche. [@firmware]
- **La numeración de `QUE_FALTA.md` está pisada**: el 09-05-b, el 09-06-b y éste
  usaron todos el ítem **21**. Corregir al mergear, en orden de entrada. Lo dejé
  anotado dentro del propio ítem. [@cronista]

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-07-b-el-corte-que-nadie-avisa` (`69dc151`).
- `QUE_FALTA.md` de frioseguro actualizado (ítem 21).
- Worktree `C:\Proyectos\_noche_frio_b` eliminado; el árbol de `frioseguro` quedó
  **idéntico**, en el branch `09-04-b`, con el KiCad de TermoVigía sin commitear
  como estaba.
- El `.exe` del test no viaja en el commit (se regenera con g++).
- Nada corriendo, nada abierto.
