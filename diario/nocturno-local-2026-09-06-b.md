# Nocturno local — 2026-09-06-b

**Trabajador:** worker nocturno local (Matías durmiendo). **Segundo turno** de la
noche — el primero fue `nocturno-local-2026-09-06.md` (datalogger, el hueco que
no se ve).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA — prioridad #1 de la
jerarquía**), zona `firmware_modular/` + `tools/` únicamente.
**Branch:** `nocturno/local-2026-09-06-b-la-puerta-fantasma` (pusheado).
**Sale de `main` (`2ac3a7d`) con `nocturno/local-2026-07-20-door-alert-model`
mergeado adentro** (ver "Nota de merge").
**No toca SQL, ni el panel, ni el servidor, ni `alerts.h`, ni `sensors.h`, ni
`hardware/`.**

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_frioseguro`, ya
eliminado) porque el árbol de `frioseguro` tiene el KiCad de Matías sin
commitear y un `checkout` lo habría tocado. **Verificado al terminar: el árbol
quedó idéntico**, en el branch `nocturno/local-2026-09-04-b` donde estaba.

---

## TL;DR

> **Un equipo sin sensor de puerta avisaba "puerta abierta".** La puerta
> principal estaba `enabled = true` fijo, ignorando `config.doorEnabled`. Con el
> pull-up interno y nada enchufado, GPIO5 lee HIGH — y HIGH significa *abierta*.
> Así que un comercio que sólo contrató monitoreo de temperatura recibía, **a
> los 2 minutos del primer arranque**, un Telegram diciendo *"🚪 PUERTA ABIERTA
> — La puerta Principal lleva 2 minutos abierta"*, y su equipo publicaba
> `door1_open: true` y `any_door_open: true` permanentes en la nube. El primer
> aviso que el cliente recibe del producto que se vende como *"te avisamos
> cuando pasa algo"* era falso.

## Por qué esta tarea

1. **Es PLATA y es la mitad del producto que no se había mirado nunca.** La
   puerta del freezer olvidada abierta es la 2ª causa de pérdida de mercadería
   de un comercio. Las últimas seis noches cerraron la rama de **temperatura**
   (sonda caída, temperatura congelada, Telegram, cola de avisos del servidor).
   La rama de **puerta** no se había tocado.
2. **Había tres hallazgos escritos desde julio esperando a alguien.** El branch
   `07-20` los documentó con tests que los demuestran y los dejó explícitamente
   *"para @firmware, en banco con un reed real"*. Resultó que ninguno de los
   tres necesitaba un reed: los tres se cierran y se verifican sin hardware.
3. **Estaba libre.** Revisé los 34 branches abiertos de frioseguro: el único que
   toca `door_sensors.h` es el `09-01-b`, y sólo en las 3 líneas del envío por
   Telegram (ver "Nota de merge").

## El agujero, y por qué nadie lo veía

```c
doorsState.doors[0].enabled = true;   // <- fijo, ignora config.doorEnabled
...
return digitalRead(doorsState.doors[doorIndex].pin) == HIGH;   // HIGH = abierta
```

Tres disfraces, y ninguno es un descuido:

1. **En el banco siempre hay un reed puesto.** El equipo con el que se prueba
   tiene el sensor conectado y el imán cerca: GPIO5 lee LOW, la puerta se ve
   cerrada, y nada de esto se manifiesta. El caso que falla es el **equipo sin
   reed**, que es justamente el que nadie arma para probar.
2. **El header decía que el módulo no corría.** Arriba de todo,
   `door_sensors.h` afirmaba *"NOTA: Este módulo NO está integrado aún. Solo
   definiciones."* — mientras el `.ino` lo incluía, lo inicializaba en `setup()`
   y lo corría en el `loop()` cada 500 ms. Cualquiera que abriera el archivo
   buscando de dónde salía un aviso de puerta concluía que ese código no corre.
   (Era el hallazgo #3 del 07-20, el que parecía el más inofensivo de los tres.)
3. **Y el firmware tenía la defensa correcta, escrita, sin usar.** `sensors.h`
   **sí** respeta `config.doorEnabled` y pone `sensorData.doorOpen = false`. Y
   `supabase.h` publicaba:

   ```c
   doc["door1_open"] = doorsState.doors[0].enabled ? doors[0].isOpen : sensorData.doorOpen;
   ```

   Como `enabled` era `true` siempre, **la rama de la derecha —la correcta— era
   código muerto**. El valor bueno se calculaba en cada ciclo y no se usaba
   jamás. Las dos capas están bien por separado y el agujero está justo en el
   medio: el mismo patrón de la sonda caída (08-29) y de la temperatura
   congelada (09-04-b).

## Los otros tres, abiertos desde julio

**#1 — El umbral que el cliente configuraba no gobernaba nada.**
`config.doorOpenMaxSec` (default **180 s**) es un parámetro de primera clase en
todo el firmware menos donde importa: se carga de Preferences, **se sincroniza
desde Supabase** en cada pull de config, se expone y se edita por la web, se
muestra en el status JSON y se setea por serial. Y la decisión comparaba contra
`#define DOOR_OPEN_ALERT_SEC 120`. **El cliente configura "avisame si queda
abierta 5 minutos", el equipo lo recibe, lo guarda, lo muestra… y avisa a los
2.** Ni el default coincidía (config decía 180, el módulo usaba 120). Es el
mismo **"OK vacío"** que el `CMD_SET_POTENCIA` de galgas del 09-05.

**#2 — La alerta de puerta no llegaba a `alerts`.** Sólo Telegram, nunca
`sendAlertToSupabase`. El evento no quedaba registrado: invisible en el panel,
ausente del historial y **ausente del resumen mensual** (branches 07-11-b/07-13)
que se vende como la razón para seguir pagando el abono — *"este mes: 2 alertas,
0 pérdidas"*. La 2ª causa de pérdida del comercio no se contaba.

**#3 — La nota que mentía.** Corregida.

## Lo que salió al arreglarlo (y no estaba en el plan)

**El aviso se consumía antes de mandarse.** `door->alertSent = true` estaba
**afuera** del `if (state.internetAvailable && config.telegramEnabled)`. Con el
router abajo el aviso se marcaba como dado y **no salía nunca más**. No es un
escenario exótico: **la puerta que queda abierta durante un corte de luz es
exactamente el caso en que el router también está abajo.** Es el tercer branch
seguido que encuentra este mismo patrón (`faultAlerted1 = true` en el 08-29,
`lastSupabaseSync = now` en el 08-26).

**Y una decisión que va al revés que la de la sonda.** Al escribirlo como
máquina de estados apareció el caso: el aviso no salió, y para cuando vuelve
internet **la puerta ya se cerró**. En el 08-29 la regla fue cancelar (avisar
"la sonda volvió" de algo que el cliente nunca escuchó caer es ruido). Acá es lo
contrario: **una puerta que estuvo 8 minutos abierta es una pérdida que ya
ocurrió**, y el comerciante la quiere saber. Así que el aviso no se descarta:
cambia de tiempo verbal —*"estuvo N minutos abierta"*— y sale con la duración
final, que es el dato útil.

**Un `door_open_max_sec = 0` habría alertado en cada apertura.** La nube puede
mandarlo y el linter de provisioning (branch 07-12) no lo chequea. Esa es la
tormenta de falsas alarmas que hace que el cliente silencie el bot y después
deje de pagar. Por debajo de 30 s se ignora la config y se usa el default.

## Qué se entregó

`firmware_modular/door_alert_model.h` — **puro** (sin Arduino, sin HTTP, sin
`digitalRead`) e **incluido** por `door_sensors.h`: no es un espejo, lo que se
testea es lo que se flashea. Mismo criterio que `sensor_fault_model.h` (08-29),
`temp_report_model.h` (09-04-b) y `logica/reintentos.py` (09-05-b).

`door_sensors.h` quedó con **una sola fuente de verdad por puerta** (el
`DoorAlertState`): los campos sueltos `isOpen`/`openSince`/`alertSent` del
struct viejo se fueron y el único consumidor externo (`supabase.h`, 4 líneas)
apunta al modelo. La puerta principal sigue a `config.doorEnabled` **en vivo**
—se re-evalúa en cada chequeo—, así el cliente la apaga desde la web o desde la
nube sin reiniciar el equipo; al apagarse se borra el cronómetro y cualquier
aviso pendiente, porque lo que se midió mientras nadie miraba la puerta no es un
dato.

## Cómo verificarlo (comandos exactos, sin hardware, sin nube, ~2 minutos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-09-06-b-la-puerta-fantasma

# 1) la decisión, contra el header que se flashea
g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_door_alert.exe tools/test_door_alert.cpp
./tools/test_door_alert.exe

# 2) el modelo de detección del 07-20, actualizado
cd tools && python -m unittest test_door_alert_model && cd ..
python tools/door_alert_model.py --demo-hallazgo    # exit 0 = hallazgo #1 cerrado

# 3) que compile de verdad
arduino-cli compile --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" firmware_modular
```

**Resultados obtenidos esta noche:**

- `test_door_alert.exe` → **34 checks, 0 fallos, sin warnings**. Dos bloques
  están escritos como **regresión**, y comprobé con **3 mutantes** que
  reimplantan los defectos que los tests los matan:

  | mutante | qué reimplanta | fallas |
  |---|---|---|
  | 1 | el umbral hardcodeado en 120 s | **8** |
  | 2 | el aviso se consume aunque no se haya entregado | **5** |
  | 3 | el aviso se descarta cuando la puerta se cierra | **3** |

- `test_door_alert_model` (el del 07-20, actualizado al firmware nuevo) →
  **16 tests OK**. `--demo-hallazgo` pasó de **exit 1** ("divergencia
  observable") a **exit 0** ("hallazgo cerrado: SI").
- **`arduino-cli compile --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs"`** →
  **exit 0, 65 % de flash (1.289.156 B), 16 % de RAM (53.848 B), 0 warnings y
  0 errores** (`grep -ci "warning|error"` sobre el log completo → **0**).
  Mismos números que el 08-29 y el 09-04-b.
- **El primer intento de compilación FALLÓ y eso es parte de la verificación**:
  al sacar `isOpen` del struct, el compilador encontró **dos usos más** en
  `supabase.h` (`door2_open` y `door3_open`/`door4_open`) que el `grep` inicial
  no había mostrado. Corregidos.

## Qué quedó SIN verificar (pide un reed switch y el banco)

1. **Arrancar un equipo con `door_enabled=false` y sin reed conectado**, y
   confirmar que ya no llega el Telegram falso a los 2 minutos ni se publica
   `door1_open: true`. Es el escenario del bug principal y el más importante.
2. **Configurar `door_open_max_sec = 300` desde el panel** y cronometrar: el
   aviso tiene que llegar a los 5 minutos, no a los 2.
3. **Abrir la puerta con el router apagado**, pasar el umbral, prender el router
   después: el aviso tiene que llegar igual, hasta 60 s más tarde.
4. **Lo mismo cerrando la puerta antes de que vuelva el router**: tiene que
   llegar en pasado, con la duración final.
5. **Confirmar UNA fila en `alerts`** con `alert_type='door'` por evento, y que
   el panel y el resumen mensual la cuenten.
6. **El rebote del reed** (chatter mecánico): la lectura sigue sin debounce. Ya
   estaba anotado como límite por el 07-20 y **este branch no lo toca**; para
   saber si hace falta hay que ver un reed real.

## Nota de merge

**Sale de `main` (`2ac3a7d`) con `nocturno/local-2026-07-20-door-alert-model`
mergeado adentro.** Lo traje a propósito: el 07-20 dejó un modelo Python cuyos
tests **fijaban el bug como conducta esperada**, y su propio doc pedía *"al
aplicar el fix, quitar el `alert_threshold_sec` fijo del modelo y actualizar el
test `TestHallazgo1UmbralIgnorado` en el mismo commit"*. Eso hice. **Al mergear
éste entra también el 07-20**; no hace falta mergearlo aparte.

**Colisión posible con un solo branch**:
`nocturno/local-2026-09-01-b-el-aviso-que-no-sale`, y sólo en el tramo de envío
de `doorSensorsCheck()` — él reemplaza el `if (internetAvailable) sendTelegramAlert(...)`
por `telegramNotify(msg, TG_SRC_DOOR, false)` del gate con reintento. **Los dos
lados quieren lo mismo** (que el aviso no se dé por dado si no salió); se
resuelve **quedándose con su `telegramNotify` adentro de mi `doorDeliverNotice()`**,
usando su retorno como el `delivered` que consume el pendiente. Con el resto de
los 34 branches, ninguna: nadie más toca `door_sensors.h`, y en `supabase.h`
sólo cambié 4 líneas de `doorN_open`.

En `QUE_FALTA.md` el ítem se numeró **21** (el 09-05-b usó el 21 también —
**corregir al mergear**: si entran los dos, éste pasa a 22).

## Anotado y NO tocado

- **`sensors.h` y `door_sensors.h` leen el MISMO GPIO5 por su cuenta**, con dos
  `pinMode`, dos cronómetros y dos cadencias distintas (`readSensors()` cada
  varios segundos vs. cada 500 ms), y `web_api.h` publica uno mientras
  `supabase.h` publica el otro. Hoy no se contradicen porque los dos siguen
  `config.doorEnabled`, pero **son dos verdades del mismo interruptor** —
  exactamente lo que la doctrina de una sola fuente de verdad condena.
  Unificarlo toca el contrato del panel: es la deuda más grande que queda en
  esta rama. [@firmware + @backend]
- **`power_monitor.h` tiene los mismos dos bugs y esta vez SÍ está sin
  integrar** (el `.ino` no lo incluye): `powerState.alertSent = true` está
  afuera del `if` de internet, y `sim800SendPowerAlert(true)` se llama sin
  mirar si hay módem. Cuando se conecte el corte de luz —que para un comercio
  es EL evento, y es de lo que más se habla en el pitch— tiene que pasar por
  esta misma máquina. **Candidato claro para la próxima noche.** [@firmware]
- **Las puertas 2, 3 y 4 siguen en `enabled = false` fijo**, sin config que las
  gobierne, y `config.doorOpenMaxSec` es global a las cuatro. No hay hoy ningún
  cliente con más de una puerta; el día que lo haya necesitan su propio flag en
  `Config` y en la tabla `devices`.
- **El aviso no escala**: si la puerta sigue abierta media hora después del
  primer aviso, no se vuelve a avisar. Es el comportamiento de siempre y evita
  la tormenta; un re-aviso cada N minutos es una decisión comercial, no un fix
  de noche. [@comercial + @firmware]
- **`.gitignore`**: agregué `tools/*.exe` (los binarios de los tests de host se
  regeneran con g++ y no tienen por qué viajar en el repo).

## Estado del repo

`C:\Proyectos\frioseguro` quedó **exactamente como estaba** (el KiCad sin
commitear de Matías, intacto, en el branch del 09-04-b). El worktree temporal
`C:\Proyectos\_noche_frioseguro` se eliminó. El branch está pusheado y el
`QUE_FALTA.md` actualizado (ítem 21 + los 3 hallazgos del 07-20 marcados como
cerrados).
