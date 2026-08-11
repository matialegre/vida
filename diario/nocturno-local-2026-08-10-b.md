# Nocturno local — 2026-08-10-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (P1 — LA PALANCA DE PLATA).
**Branch:** `nocturno/local-2026-08-10-b-cadena-temperatura` (pusheado, `6099803`).

## Tarea elegida y por qué

El 1er turno de hoy fue a datalogger. La jerarquía manda **PLATA**, así que
este fue a FrioSeguro.

De los ítems del `QUE_FALTA` sin branch: los 🔴 que quedan son hardware
(flashear, caja estanca), plata (precio, contrato) o nube. Todo lo software-puro
ya tenía branch. Así que fui —como las dos noches anteriores, en los otros dos
repos— **al tramo que ninguna auditoría había tocado**.

Repasando qué está cubierto en FrioSeguro:

| noche | qué audita | tramo |
|---|---|---|
| 07-18 `alert_model` | `checkAlerts` | la **decisión** de alertar |
| 08-02 `telegram_gate_model` | el gate de 300 s | la **entrega** del aviso |
| 08-03-b `check_schema_drift` | columnas firmware↔SQL | la **forma** de los datos |
| 08-09 `check_tenant_isolation` | RLS + grants | el **aislamiento** entre clientes |

Los cuatro empiezan **cuando el número ya existe**. Falta el tramo de arriba de
todos, y es el que se cobra:

> **el número de °C que dispara la alerta y que el cliente ve en pantalla,
> ¿de qué sonda física salió, y sigue siendo cierto?**

Es la misma pregunta que cerré anoche en datalogger (la cadena de vibración) y
anteanoche en galgas (la cadena de medición), en el tercer repo. Y acá pega más
fuerte que en los otros dos, porque en galgas y datalogger el número alimenta un
informe: en FrioSeguro **el número ES el servicio**.

## Qué hice

**`tools/check_temperature_chain.py`** (stdlib, solo lectura, sin nube ni
hardware, no compila nada). Modela los cuatro tramos —`sensors.h` → `alerts.h` →
las 29 columnas de `readings` → el dashboard— leyendo el código real, y trae
**tres oráculos numéricos** (`--demo-average`, `--demo-stale`, `--demo-order`)
que *demuestran* los hallazgos con números en vez de afirmarlos. Exit 0/1/2/3,
`--json`, `--fail-on`, `--root`.

**`tools/test_check_temperature_chain.py` — 80 tests en 7 capas:** utilidades de
texto, extractores sobre fuentes sintéticas, los tres oráculos con números
fijados, un test por código de hallazgo con repos sintéticos armados en disco,
**control negativo** (cada defecto inyectado por separado enciende uno y sólo un
código), regresión sobre el repo real y el CLI.

**`docs/temperature-chain.md`** — el análisis completo y el orden de arreglo.

Lo que hubo que resolver:

- **Separar la rama de simulación de la real.** Mi primera versión reportaba
  como "fórmula del promedio" la de `config.simTemp1 + config.simTemp2` —la de
  simulación— en vez de la que corre en campo. El hallazgo quedaba apoyado en
  código que no se ejecuta. Hay que cortar el `if (config.simulationMode)` con
  balanceo de llaves y auditar el resto.
- **El oráculo del orden de bus no probaba lo que decía.** Con los ROM de
  ejemplo que había elegido, el repuesto caía en el mismo lugar y **no había
  swap** — y la narración igual decía "el evaporador pasó de temp1 a temp2".
  Lo vi mirando la salida. Ahora la narración **sale del cálculo** (compara el
  índice antes y después) y no puede volver a mentir; y quedó un test para cada
  caso, porque **que haya swap o no depende del ROM que venga en la bolsa del
  repuesto: es azar, no configuración** — que es justamente el hallazgo.
- **La ventana del número congelado estaba corrida un ciclo.** El firmware
  declara la falla *en* la lectura número 3, no después: la tabla del oráculo
  marcaba `valid=true` un paso de más.
- **Qué es "estructural" y qué es un descuido.** Cuatro hallazgos (T3, T4, T5,
  T7) no salen de una línea mal puesta sino de cómo está armada la cadena: no se
  pueden apagar inyectando/quitando un defecto puntual. Los declaré explícitos en
  la suite (`BASE_ESPERADOS`) y el control negativo mide **el delta** que agrega
  cada defecto. Si no, el control negativo era imposible y quedaba decorativo.
- **Un fixture mío se contradecía:** el archivo "dashboard que NO usa
  sensor_probes" tenía escrito el comentario `// sin sensor_probes`, y el
  detector —que busca el string— lo contaba como uso. El test falló por el
  fixture, no por el checker.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **5 error · 6 warn · 2 info.**

### T1 — la alerta se decide sobre el PROMEDIO de las dos sondas

`checkAlerts` compara `sensorData.tempAvg` contra **un solo**
`config.tempCritical`, y la segunda sonda viene habilitada de fábrica
(`SENSOR_DS18B20_2_ENABLED = true`): **la ruta promediada es la de default.**

Con el crítico en −10 °C y la sonda sana en −20 °C (`--demo-average`):

```
  sonda mala   promedio   ¿alerta sola?   ¿alerta el promedio?
     -6.0       -13.0        SI              no
     -2.0       -11.0        SI              no
      0.0       -10.0        SI              no

  ZONA CIEGA: de -10.0 a 0.0 °C  (10.0 °C de ancho)
```

Y el ancho es exactamente `crítico − sonda_sana`, o sea: **cuanto mejor anda un
freezer, más se puede descongelar el otro sin que suene nada.** Es el escenario
que se cobra —un equipo desenchufado mientras el otro sigue andando— y el
mensaje de la alerta imprime ese promedio como si fuera la temperatura de un
lugar físico.

Es **decisión de producto, no bug**: o se alerta por sonda (necesita T2), o se
vende el kit con una sonda por equipo. La salida más barata mientras tanto:
alertar sobre **el máximo** de las sondas válidas en vez del promedio — una
línea, y la zona ciega desaparece.

### T2 — `sensor_probes` está en la base y en el dashboard, y nadie la escribe

La tabla existe en `SETUP_COMPLETO.sql` con todo lo necesario para que una sonda
tenga identidad (`rom_id`, `name`, `slot_index`, `last_temp_c`, y **umbrales
`temp_max`/`temp_critical` por sonda**), y el dashboard la lee y la edita
(`SensorManager.jsx`, `supabaseClient.js`, `DevicesAdminTable.jsx`).

**El firmware no la toca nunca.** La única mención en `firmware_modular/` es un
comentario en el encabezado de `supabase.h:11` que la anuncia como si existiera.

1. **Los umbrales por sonda que el cliente configura no llegan a la placa** — la
   alerta sigue usando el global. La UI muestra `CRIT: −12 °C` para el
   evaporador y la placa alerta con otro número.
2. **`last_temp_c` queda NULL para siempre** — y `GUIA_INSTALACION.md:365` pide,
   como paso de la instalación, *"las sondas muestran `last_temp_c` con valor
   real (no NULL)"*: **un ítem del checklist que no puede pasar nunca.**
3. **No hay auto-descubrimiento**: ninguna sonda llega jamás a `pending`, así que
   el flujo del `SensorManager` arranca sobre una lista vacía.

Es el tercer caso del repo de *UI escrita contra algo que no existe* (los dos
anteriores: las tres tablas faltantes del 08-03-b). Con una diferencia
incómoda: acá **la tabla sí existe** — lo que falta es el productor. El trabajo
de UI **ya está hecho y pagado**.

### T5 — cuál sonda es "la 1" lo decide el orden del bus, no la sonda

`sensors.h` lee con `getTempCByIndex(0)` y `(1)`, y **en todo el firmware no hay
una sola llamada a `getAddress`**: nunca se mira el ROM. El índice de una sonda
es su posición en el ROM ordenado del bus — **un ranking entre las presentes**,
no una identidad (`--demo-order`):

```
Instalación original:
   getTempCByIndex(0) -> 28FF3C1A02000059   cámara principal
   getTempCByIndex(1) -> 28FFA10B03000071   evaporador

Se quema la de la cámara y se pone el repuesto 28FFE2470400008A:
   getTempCByIndex(0) -> 28FFA10B03000071   evaporador     <-- se movió
   getTempCByIndex(1) -> 28FFE2470400008A   cámara (repuesto)
```

**La única sonda que no se tocó es la que cambió de columna.** El gráfico
histórico dibuja el salto como un cambio de temperatura, y el
`🔌 Sonda 1 desconectada` de la próxima falla nombra a la otra.

### T3 / T4 — con la sonda caída, el sistema deja de vigilar en silencio

`checkAlerts` arranca con `if (!sensorData.valid) return;`. Cuando la sonda 1
acumula 3 fallas, `valid = false` y **la temperatura deja de evaluarse por
completo**. Tres agravantes:

- **La alerta activa se congela**: el `return` saltea el `clearAlert()`, así que
  relé y buzzer quedan encendidos y `alert_active = true` se sigue publicando
  indefinidamente. No se apaga sola.
- **Ninguna de las 29 columnas de `readings` lleva `valid` ni `sensor_count`** →
  desde la nube no se distingue *"sin datos"* de *"todo bien"*. La card del
  comerciante se queda con el último número, **en verde**. Y la señal existe: el
  JSON local de `printStatusJSON` **sí** la publica. Mismo patrón que en los
  otros dos repos —*el sistema informa por un camino que no verificó*— con la
  evidencia calculada y tirada.
- **Antes de eso hay 6,0 s** (3 × 2000 ms) publicando el último valor bueno como
  si fuera de ahora; con posts cada 10 s, **60 % de chance de que uno caiga
  adentro**. En el historial se ve una **meseta perfecta**, que es exactamente lo
  que se ve cuando todo anda bien.

### Los otros warnings

- **T6** — `initSensors` **no llama a `ds18b20Classify`** (que existe y está
  bien): valida con `t > -55 && t < 125`, que **deja pasar 85,0 °C** — el
  centinela de power-on-reset, la lectura *más probable* justo después de
  energizar. Se guarda con `valid = true`: el historial del cliente puede
  arrancar con un pico de 85 °C en un freezer.
- **T7** — `sensorCount` se cuenta **sólo en el boot**, y el lazo de lectura está
  guardado por `if (sensorCount > 0)`. Una sonda enchufada después del arranque
  no se lee nunca (hay que reiniciar, y el instalador no tiene por qué saberlo);
  y si al arrancar no había ninguna, **el lazo entero se saltea**: no se lee, no
  se marca `valid = false` y **no se manda `sensor_fault`**. La placa reporta
  `temp1 = 0.0 °C` para siempre, sin una sola señal.
- **T8** — el dashboard decide cuántas sondas hay con
  `reading.temp2 > -55` (`App.jsx:766`). `temp2` sólo se asigna si la sonda 2 dio
  lectura válida; si no hay sonda 2 queda en **0.0**, y `0.0 > -55` ⇒ **dibuja
  una serie plana en 0 °C dentro del gráfico de un freezer** — un valor que
  además está sobre cualquier umbral crítico y parece un dato, no un hueco.
- **T9** — la falla de sonda **no llama a `sendTelegramAlert`** (sí lo hacen
  temperatura, puerta y corte de luz): el modo de falla más silencioso es el
  único que no suena en el teléfono. Y la push web tampoco identifica la sonda:
  la Edge Function arma el nombre con `metadata.probe_name || metadata.rom_id ||
  'Sonda ' + (slot_index+1)`, pero `supabaseSendAlert` publica sólo `device_id`,
  `alert_type`, `severity`, `message` — **sin `metadata`** ⇒ siempre dice "Sonda
  1", incluso cuando la que se cortó es la 2.
- **T2b** — `INTERVAL_DISCOVERY_SCAN_MS` definido y sin uso, y **`config_version`
  se pide en el SELECT y no se lee nunca**: el trigger que la base dispara cuando
  el usuario cambia una sonda **dispara al vacío**. `GUIA_INSTALACION.md`
  documenta el comportamiento que no existe (*"esperar 60 segundos a que
  recargue"*).
- **T10** — el modo simulación es **invisible desde la nube**: publica las mismas
  29 columnas y ninguna dice que el dato es ficticio. El default es `false` (a
  diferencia del `sim_data` del datalogger, que es `true`), pero **se persiste en
  NVS**: una placa que quedó simulando en el banco sale a un cliente simulando.
- **T11 (info)** — `delay(750)` cada 2000 ms: el **38 %** del lazo bloqueado.
  `setWaitForConversion(false)` ya está puesto, así que la espera es reemplazable.

### Lo que está BIEN y queda fijado por test

Tan importante: es lo que **no** hay que ir a revisar.

- **`ds18b20Classify` distingue los tres modos de falla del DS18B20** (−127 cable
  cortado, 85 power-on-reset, fuera de rango) en vez de tratar −127 como
  temperatura. Está bien pensado; el problema es quién lo llama (T6).
- **La falla se declara recién tras 3 lecturas malas SEGUIDAS**: no hay alarma
  por un glitch del bus.
- **`readings` publica `temp1`, `temp2` y `temp_avg` por separado** ⇒ el promedio
  de T1 es **auditable después, desde la nube**, sin volver al local. Lo que no
  se recupera es la alerta que no sonó.
- **Cuando falla la sonda 2, el promedio cae a `temp1`** en vez de envenenarse.
- **Descongelamiento y cooldown suspenden las alertas**: el falso positivo más
  obvio del negocio ya está cubierto.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-10-b-cadena-temperatura
python tools/check_temperature_chain.py                 # -> 5 error / 6 warn / 2 info, exit 1
python tools/check_temperature_chain.py --json
python tools/check_temperature_chain.py --demo-average   # la zona ciega (T1)
python tools/check_temperature_chain.py --demo-stale     # el número congelado (T3/T4)
python tools/check_temperature_chain.py --demo-order     # quién es "la sonda 1" (T5)
python -m unittest tools.test_check_temperature_chain    # -> Ran 80 tests, OK
```

T1, T2 y T5 se comprueban **sin la herramienta**, mirando tres lugares:
`float temp = sensorData.tempAvg;` (`alerts.h:134`), `grep -r sensor_probes
firmware_modular/` (un solo hit, y es un comentario) y `getTempCByIndex` en
`sensors.h:118,152`.

`TestRepoReal` **fija los 13 hallazgos**, las 29 columnas de `readings` y las 4
de `alerts`: si alguien arregla uno, el test falla y obliga a actualizar
`docs/temperature-chain.md` en el mismo commit.

**Verificado por mutación** — las 7 hacen fallar la suite: `strip_comments`
ingenuo (se come las URLs), cortar el cuerpo de una función en la primera `}`,
leer la fórmula del promedio de `readSensors` entero (incluyendo la simulación —
el bug que tuve de verdad), dar vuelta el álgebra de la zona ciega, no ordenar
los ROM, medir la ventana de congelado con el período de la nube en vez del de
lectura, y sumar mal el bloqueo del lazo.

**Un hueco real de la suite, encontrado por la última mutación:** cambiar `sum`
por `max` en el cálculo del bloqueo **no rompía ningún test**, porque
`readSensors` tiene un solo `delay()` y los dos criterios dan lo mismo. Agregué
el caso que los separa (dos `delay`, 750 + 50 sobre 2000 ms = 40 %). Segunda
noche seguida que pasa: **las mutaciones no sólo validan los tests, encuentran
los que faltan.**

## Qué quedó sin verificar

- Todo sale de **leer el código**, no de observar una placa. Los tres oráculos
  demuestran el **efecto** de lo que dice el código, no que el hardware lo haga.
- **No compilé firmware ni bajé toolchains** (regla de disciplina de tiempo), y
  **no corrí `npm run build`**: no toqué una línea de dashboard ni de placa, la
  herramienta es sólo lectura.
- El checker mira el **repo**, no la base viva. Si en producción alguien cargó
  filas en `sensor_probes` a mano, T2 sigue valiendo (el firmware no las lee),
  pero `last_temp_c` podría no estar NULL.
- **Falta en banco (10 min con el Serial, sin instrumental):** T3 desenchufando
  una sonda con una alerta activa y viendo si el relé se apaga; T6 mirando la
  primera línea de `[SENSOR] >>> TEMPERATURA INICIAL` después de un
  power-cycle; T7 arrancando la placa sin sondas y viendo si sale un
  `sensor_fault`; T5 anotando el ROM de cada sonda antes y después de cambiar
  una.
- **Ningún fix aplicado** — generator ≠ evaluator, y el primero de la lista (¿qué
  significa "la temperatura del local"?) es decisión de producto, con dueño
  (Matías + @firmware).

## Estado

- Branch `nocturno/local-2026-08-10-b-cadena-temperatura` pusheado (`6099803`).
  frioseguro volvió a `main` limpio.
- `QUE_FALTA.md` de frioseguro: ítems **#19, #20 y #21** nuevos (en el branch).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Novena noche que lo reporto:** es un firmware que va a un equipo a 2000 km y
  vive **sólo en este disco**. **No lo toqué.**
- ⚠️ **`C:\Proyectos\datalogger` tiene trabajo de día NUEVO sin commitear** que
  no estaba anoche: `firmwares/nodo-gimap/`, `tools/rx_gimap.py`,
  `tools/test_protocolo_gimap.py`, `tools/test_red_gimap.py`,
  `docs/ARMADO_NODO_GIMAP.html` y un `.gitignore` modificado. **No lo toqué.**
- ℹ️ `C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main` (estado previo). **No
  lo cambié.**
- ⚠️ Queda el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando Matías quiera.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  catorce noches anteriores). **No los toqué.** Matías: commitealos, o la rutina
  cloud choca en el próximo `git pull`.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` **vacío** (sólo el `.gitkeep`). El
  único `enlace\maquinas\*.estado.json` tiene `ultima_vez_viva` del **2026-07-07**:
  hace un mes que ninguna máquina late. **No lo toqué** (los scripts del
  protocolo son trabajo de día sin commitear).
- La cola de merge suma **51 branches** en origin (galgas 18, datalogger 16,
  frioseguro 16, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo
  y sin usar: falta la sesión humana.
  **Nota de prioridad:** de los 16 de frioseguro, éste y el de aislamiento
  (08-09) son los dos que tocan **lo que se cobra**. Y hay un solapamiento que
  conviene aprovechar: **T2/T5 (identidad de sonda) y el ítem #4 (credencial
  única por dispositivo) se resuelven en el mismo reflasheo** que ya está
  pendiente por la rotación de claves. Son tres razones para tocar la placa una
  sola vez.
