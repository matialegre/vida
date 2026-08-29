# Nocturno local — 2026-08-29

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la jerarquía).
**Branch:** `nocturno/local-2026-08-29-la-sonda-que-se-cae` (pusheado, `be77516`).
**Sale de:** `main` (`ddf5134`). **No depende de ningún otro branch nocturno y no
colisiona con ninguno**: los 24 branches abiertos de frioseguro viven en
`supabase.h`, `web_api.h`, `html_ui.h`, el panel y `tools/`; éste toca
`firmware_modular/sensors.h` y agrega dos archivos nuevos. Se mergea en cualquier orden.

## TL;DR

> **Cuando se cae la sonda, el equipo deja de vigilar la heladera. Eso está bien.
> Lo que estaba mal es que el aviso de que dejó de vigilar era un disparo único
> que se perdía si en ese momento no había internet — y que si la sonda no
> estaba en el arranque, el aviso directamente no existía.**

`alerts.h::checkAlerts()` arranca con una línea:

```c
if (!sensorData.valid) return;
```

Con la sonda caída, **el motor de alertas de temperatura queda apagado, cada
segundo, para siempre**. Es la decisión correcta —no se puede alertar sobre una
lectura que no existe—, pero convierte al aviso de sonda caída en el **último
aviso que el sistema es capaz de dar**. Si ese aviso no sale, el comercio queda
con un equipo que late verde en el panel y no vigila nada.

Es el modo de falla exacto contra el que se vende el abono.

## Por qué esta tarea y no otra

1. **Rotación + jerarquía.** Anoche fueron galgas (`08-28`) y datalogger
   (`08-28-b`); frioseguro venía del `08-27-b`. Cosechador sigue siendo el más
   viejo (`08-23-b`) pero **todo lo que le queda está bloqueado por la compra**:
   sus cinco branches ya agotaron el análisis offline. Entre los desbloqueados,
   frioseguro es el más viejo **y** es PLATA. Desempata solo.
2. **No estaba en ningún branch.** Repasé los 24 branches nocturnos abiertos de
   frioseguro: ninguno tocó `sensors.h`. El ítem #18 del `QUE_FALTA` roza el tema
   (modelo de `checkAlerts`) pero su hallazgo está marcado **"NO corregido de
   noche, es de banco"** a propósito — no lo pisé.
3. **Es software puro y verificable sin hardware.** Y resultó que se podía
   verificar de las dos maneras: test de lógica **y** compilación real del
   firmware (el core ESP32 ya estaba instalado en esta máquina).

## Los tres agujeros

### 1. El aviso se consumía antes de mandarse

```c
// firmware_modular/sensors.h, main (antes)
if (faultCount1 >= DS18B20_FAULT_CONSECUTIVE && !faultAlerted1) {
  faultAlerted1 = true;                                    // <-- se consume ACA
  sensorData.valid = false;
  ...
  if (config.supabaseEnabled && state.internetAvailable) { // <-- y recien aca se manda
    sendAlertToSupabase("sensor_fault", "critical", msg);
  }
}
```

`faultAlerted1` es la memoria de *"ya avisé"*, y se ponía en `true` **arriba** de
la condición de envío. Con `state.internetAvailable == false` el aviso se marcaba
como dado y **no salía nunca** — ni en ese momento ni cuando volvía el router.

Y no es un escenario rebuscado: **la sonda y el router cuelgan del mismo corte de
luz.** El ESP32 arranca en segundos; el router del comercio tarda minutos. La
ventana en la que el equipo está prendido, midiendo y sin internet es exactamente
la ventana en la que se descubre que la sonda no volvió.

Es el mismo patrón que `state.lastSupabaseSync = now` arriba del `if` (branch
`08-26-el-hueco-y-el-reloj`): **el reloj avanza aunque la acción no ocurra.**
Tercera vez que aparece en este repo.

### 2. Sin sonda en el arranque: silencio total y permanente

`sensorData.sensorCount` se asignaba **sólo** en `initSensors()`, y el cuerpo
entero de `readSensors()` colgaba de `if (sensorData.sensorCount > 0)`.

Si en el arranque el bus 1-Wire no enumeraba nada —conector flojo, brownout del
compresor al arrancar, o el instalador que enchufó la sonda después de dar
corriente— entonces **para siempre**:

- no se leía ninguna temperatura,
- `sensorData.valid` quedaba en `false` → `checkAlerts()` retornaba en la línea 1,
- **los contadores de falla nunca corrían**, porque vivían adentro del mismo `if`,
- no salía un solo aviso.

El equipo seguía mandando `readings` y heartbeat: **verde en el panel, vigilando
nada.** Enchufar la sonda después tampoco lo arreglaba — hacía falta un reboot
manual que nadie sabía que hacía falta. Es el *"lo probé en el banco y en el
comercio no anda y no sé por qué"*.

### 3. No llegaba por el canal que el cliente mira

`triggerAlert()` (temperatura) manda Telegram. `sensor_fault` iba **sólo** a la
tabla `alerts` de Supabase. El comerciante no mira el panel: mira el celular. Y
"dejé de vigilar tu heladera" es *más* urgente que "está a -8 en vez de -10",
justamente porque a partir de ahí no va a salir ninguna alerta de temperatura.

## Qué hice

La decisión salió de `readSensors()` y vive en **`firmware_modular/sensor_fault_model.h`**:
un header **sin Arduino, sin HTTP, sin OneWire** —enteros y flags— que `sensors.h`
**incluye**. No es un espejo en otro lenguaje (el `alert_model.py` del branch
`07-18` avisa de ese riesgo): es el mismo archivo que se flashea, y por eso se
compila con `g++` en la PC y se testea sin hardware.

```
sfmFeed(s, cls)                     alimenta una lectura clasificada
sfmShouldNotify(s, now, retryMs)    ¿toca intentar entregar?
sfmNotified(s, now, delivered)      cierra el intento — solo consume si SALIO
```

**Invariante:** un aviso pendiente no se consume hasta que se entrega. Sin
internet queda pendiente y se reintenta cada 60 s hasta que sale.

De escribirlo como máquina de estados —en vez de dos `bool` sueltos— cayeron
solas cuatro cosas más:

| Situación | Antes | Ahora |
|---|---|---|
| La sonda vuelve | silencio | `Sonda N recuperada` — el que fue a apretar el conector tiene confirmación |
| Caída pendiente sin entregar + la sonda vuelve | — | **se cancelan las dos** |
| Recuperación pendiente + se vuelve a caer | — | gana la caída |
| Bus vacío (`sensorCount == 0`) | mudo para siempre | mismo debounce y mismo aviso que un cable cortado; el bus se re-enumera cada 30 s |
| Sonda redescubierta | — | se le reaplica resolución 12 bit y modo no bloqueante (si no volvía degradada) |

**La cancelación mutua la encontró el test, no yo.** Mi primera versión avisaba
"sonda recuperada" de una caída que el cliente nunca había escuchado caer —
porque el aviso de caída se había quedado pendiente sin internet. Ruido puro.
El test falló, y ahí se arregló el modelo.

Telegram se suma como canal del `sensor_fault`, con el mismo criterio de entrega.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-29-la-sonda-que-se-cae

# 1) La maquina de estados (segundos, sin hardware)
g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_sensor_fault.exe tools/test_sensor_fault.cpp
./tools/test_sensor_fault.exe

# 2) El firmware entero (~4,5 min en esta maquina)
arduino-cli compile --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" firmware_modular
```

**Resultado obtenido esta noche:**

- Test: **39 checks, 0 fail, exit 0**, sin un solo warning con `-Wall -Wextra`.
  Los agujeros (1) y (2) están escritos como **regresión** —fallan contra la
  lógica vieja—, más el wrap de `millis()` a los ~49,7 días y la saturación del
  contador.
- Compilación: **exit 0**, `1289304` bytes = **65 % de flash**, `53816` bytes =
  **16 % de RAM**, **cero warnings**. El core ESP32 ya estaba instalado
  (`~/AppData/Local/Arduino15/packages/esp32`) — no hubo que bajar nada.

El `.exe` del test **no se commiteó** (binario); se reconstruye con la línea de
arriba en un segundo.

## Qué quedó sin verificar (necesita hardware)

Los cuatro escenarios de banco, listados también en `docs/sensor-fault-notice.md`:

1. Desenchufar la sonda con el equipo andando → confirmar que el aviso llega a
   Supabase **y** a Telegram, y que llega **una sola vez**.
2. Repetir con el router apagado → confirmar que el aviso **sale cuando vuelve**
   el internet (éste es el bug principal; sin hardware sólo está probada la
   máquina de estados, no el POST real).
3. Arrancar el equipo **sin** sonda → confirmar que a los ~90 s avisa, y que al
   enchufarla se redescubre sola en ≤30 s y avisa la recuperación.
4. Confirmar que un `sensor_fault` con severidad `info` (la recuperación) no
   rompe el render del panel.

**Limitación honesta del criterio de "entregado":** es
`state.internetAvailable && (supabase || telegram habilitado)`, **no** el `201`
de PostgREST — `supabaseSendAlert()` devuelve `void`. Eso es territorio de los
branches `08-26-el-hueco-y-el-reloj` y `08-27-b-columnas-fantasma`; cuando esos
se mergeen, `sensorNoticeDeliver()` pasa a devolver el resultado real del POST y
la máquina de estados no cambia una línea. Está anotado en el doc.

## Deuda anotada, no tocada

Mientras la sonda está caída, `sensorData.temp1` / `tempAvg` conservan **el
último valor bueno** y se siguen publicando en `readings`. Va acompañado de
`valid:false`, así que el dato para distinguirlo existe, pero el panel muestra
una temperatura congelada que parece viva. Cambiar el valor publicado toca el
contrato con el panel y con la app Android: es trabajo de @frontend + @backend,
no de un parche de firmware de noche.

## Estado del repo al cerrar

`main` limpio en lo mío (sólo se commiteó el `QUE_FALTA.md`, ítem **#19**).
**Ojo:** el working tree de frioseguro tiene cambios sin commitear de Matías
(`android-app/`, `frioseguro-android/`) y varias carpetas sin trackear del
revival de Santa Cruz (`entrega_scz/`, `panel-web/`, `firmware_revival/`,
`kit_santacruz/`, `backup_supabase/`, `apk-panel/`, `REVIVAL_2026-08.md`).
**No los toqué.** Están así desde antes de esta noche.
