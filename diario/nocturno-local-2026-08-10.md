# Nocturno local — 2026-08-10

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "terminarlo primero, antes del trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-10-cadena-vibracion` (pusheado, 2 commits:
`42b8781` la auditoría, `c82efed` la generalización a las rutas de muestreo).

## Tarea elegida y por qué

Por rotación tocaba datalogger (los dos turnos de ayer fueron frioseguro y
galgas; la última noche de datalogger fue el 08-08).

Repasé el `QUE_FALTA`: los 🔴 sin branch son banco o hardware (#1 necesita
flashear el Pico, #2 es el front-end del piezo, #3 y #4 necesitan medir). Los 16
branches previos cubren INA219, integridad de SD (tres veces), mesh RV1, RSSI,
SSID, eco-schedule, contabilidad del registro, el contrato del frame, el contrato
de la nube y la fidelidad del benchmark.

**Todos esos auditan tres cosas: *timing* (jitter del lazo), *contabilidad*
(muestras que se pierden) y *forma* (qué campos, qué columnas). Ninguno audita
*significado*.** Y el datalogger entrega **una frecuencia**: el DoD habla de
loguear a SD, el ítem 🟢 #13 quiere venderlo como *"estudio de vibraciones con
informe"*, y la vista tiene un chip que dice, con cero decimales:

```
Frec. dominante
    66
     Hz
```

Esa cadena tiene cuatro tramos y **tres implementaciones distintas de la FFT** —
el nodo mide la tasa, el dashboard hace una FFT en JS, el laboratorio otra con
numpy— y nadie las había comparado nunca. La pregunta que elegí responder:

> **¿el número de Hz que aparece en pantalla es la frecuencia de la máquina?**

Es el mismo hueco que cerré anoche en galgas (la cadena de medición), en el otro
repo. Y elegí este ítem sobre cualquier otro porque **su valor caduca**: sirve
*antes* de la sesión de banco del bloqueante #1, no después.

## Qué hice

**`tools/check_vibration_chain.py`** (stdlib, solo lectura, sin red ni hardware,
no compila nada). Modela el sensor a partir del register map, extrae las tasas
del SCHEMA **y de los tres `config.P*.json` que están flasheados**, y cruza el
reensamblado del gateway con las dos FFTs. Exit 0/1/2/3, `--json`, `--fail-on`,
`--root`, y **tres oráculos numéricos** (`--demo-alias`, `--demo-gap`,
`--demo-window`) con un DFT en Python puro: los hallazgos se *demuestran con
números*, no se afirman.

Lo que hubo que resolver:

- **Las misiones no usan `mpu6050.py`.** Esto lo encontré *escribiendo el
  informe*, y me obligó a rehacer el control principal. Cada misión de la
  taxonomía tiene **su propia copia** del setup del MPU y **sí** escribe el DLPF
  (`lab` → 184 Hz, `baja`/`media`/`dreyfus` → 94 Hz). Mirando sólo el driver
  compartido, el hallazgo quedaba mal alcanzado. La pregunta correcta no es "¿está
  configurado el DLPF?" sino **"¿el Nyquist de cada ruta queda arriba del ancho de
  banda que el sensor deja pasar?"**. Generalizado a las **cinco rutas** del repo,
  el resultado es más preciso y más incómodo (ver V1).
- **El relleno de huecos del dashboard muta el array in situ.** Mi primera
  réplica copiaba el array antes de rellenar —lo "prolijo"— y daba un escalón
  plano. El JS **no hace eso**: el vecino izquierdo de la muestra `i` es la `i-1`
  que acaba de inventar, así que el hueco se completa con una **rampa** que
  converge al vecino derecho. Lo agarró el test, y **cambió el texto del
  hallazgo**: había escrito "escalón plano" y sólo es plano cuando el chunk
  perdido es el 0.
- **El regex del gate del JSON no puede anclarse en `vibN` primero.** El fix
  natural de V4 es agregar `n.vibReady &&` **adelante** de la condición: un regex
  `if \(n\.vibN > 0…` deja de encontrarlo y el hallazgo desaparecería justo
  cuando alguien lo arregla, en la dirección que absuelve.
- **Balancear llaves para leer un cuerpo de función JS.** `fftMag` y `renderVib`
  tienen bloques anidados; cortando en la primera `}` los detectores leen medio
  cuerpo y dos hallazgos se apagan solos.
- **`literal_eval` sobre las entradas del SCHEMA revienta** (son
  `(default, tipo, lambda, ayuda)`): hay que leer `elts[0]` y sacar las cotas del
  **texto fuente** del lambda. Misma lección que la noche del benchmark.
- **Resolver los registros por nombre, no por número.** El driver escribe
  `writeto_mem(addr, PWR_MGMT_1, …)`: buscar `0x6B` en el texto no encuentra
  nada. Hay que mapear las constantes del módulo con el AST.
- **Sacar comentarios de C sin comerse las comillas** (la lección que ya viene de
  cuatro noches: `CLOUD_URL` tiene un `//` adentro).

**`tools/test_check_vibration_chain.py` — 82 tests en 7 capas:** utilidades de
texto, extractores sobre fuentes sintéticas, **los tres oráculos con números
fijados**, un test por código de hallazgo con repos sintéticos armados en disco,
un **control negativo** (repo sano → sólo el `info`) que además verifica que
**cada defecto inyectado por separado enciende uno y sólo un código**, la
regresión sobre el repo real y el CLI.

**`docs/vibration-chain.md`** — el análisis completo y el orden de arreglo.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **5 error · 4 warn · 1 info.**

### Los dos hechos del sensor de los que cae todo

Del register map del MPU-6050: el driver escribe `PWR_MGMT_1` (0x6B) y
`ACCEL_CONFIG` (0x1C) **y nada más**. Nunca toca `CONFIG` (0x1A, el DLPF) ni
`SMPLRT_DIV` (0x19). Entonces, por default:

1. **el ancho de banda del acelerómetro es 260 Hz**;
2. **la ODR del acelerómetro es fija en 1 kHz** (*"the same accelerometer sample
   may be output … more than once"*).

### V1 — hay rutas de muestreo sin filtro anti-alias (el más caro)

Una ruta aliasea cuando su Nyquist queda **por debajo** del ancho de banda que el
sensor deja pasar. Las cinco rutas del repo, con su fs **efectiva**:

| ruta | fs viene de | fs | Nyquist | BW | |
|---|---|---|---|---|---|
| clásico (`mision=off`) | SCHEMA default | 20 | 10,0 | 260 | **pliega 10–260** |
| clásico (`mision=off`) | `config.P1/P2.json` | 50 | 25,0 | 260 | **pliega 25–260** |
| clásico (`mision=off`) | `config.P3.json` | 10 | 5,0 | 260 | **pliega 5–260** |
| misión `baja` | nominal (`FS_DEF`) | 200 | 100,0 | 94 | ok |
| misión `baja` | `config.P1/P2.json` (`mpu_hz`) | 50 | 25,0 | 94 | **pliega 25–94** |
| misión `baja` | `config.P3.json` (`mpu_hz`) | 10 | 5,0 | 94 | **pliega 5–94** |
| misión `lab` | literal | 1000 | 500,0 | 184 | ok |
| misión `media` | divisor | 333 | 166,5 | 94 | ok |

Dos lecturas:

1. **La ruta que corre hoy es la clásica** —ninguno de los tres `config.P*.json`
   setea `mision`, y su default es `off`— y con `sd_interval_s = 0` graba **una
   fila de SD por muestra**: es el entregable del DoD.
2. **`mision_baja` filtra bien a su fs nominal y mal a la que le queda.** Escribe
   el DLPF de la taxonomía (94 Hz, correcto para 200 Hz) pero deriva su fs de
   `cfg["mpu_hz"]`, que en los nodos reales vale 50 o 10. **El filtro y la tasa se
   eligen en archivos distintos y nada los ata**: bajar `mpu_hz` por consola para
   ahorrar energía rompe el anti-alias sin tocar una línea de la misión.

Con números (`--demo-alias`, una máquina a 1320 rpm cuyo componente dominante es
el 3×):

```
ráfaga LoRa (1000 Hz)     -> pico dominante  66.00 Hz   (correcto)
canal continuo / SD (50)  -> pico dominante  16.00 Hz   <-- el ALIAS del 3x
    tono  66.0 Hz aparece en  16.0 Hz  <-- PLEGADO
    tono 110.0 Hz aparece en  10.0 Hz  <-- PLEGADO
```

Por qué es grave y no académico:

1. **Los defectos de rodamiento viven arriba de Nyquist** (3-10× rpm): con
   fs = 50 Hz **todos** caen dentro de 0-25 Hz. Un rodamiento picado se ve como
   un desbalanceo, o como nada.
2. **Los armónicos pares caen en DC**: `alias(50,50) = 0`, y el dashboard además
   resta la media.
3. **Dos componentes distintos pueden plegar al mismo lugar** y el espectro no
   tiene forma de saberlo.
4. **No hay síntoma.** Un CSV aliaseado tiene el largo correcto, `seq` contiguo y
   cero gaps: **pasa todos los controles de integridad de SD** de las tres noches
   que los escribieron. Integridad ≠ validez.
5. **El plegado pasa en el ADC del sensor**, antes de que el dato exista: no lo
   deshace ningún filtro digital ni ningún reprocesamiento de la SD.

**Y no lo arregla ningún runtime** — gane MicroPython o gane C, el canal continuo
sigue aliaseado. Eso lo anoté en el bloqueante #1: la decisión de fondo (¿el
canal continuo mide espectro o inclinación?) hay que tomarla **antes o durante**
la misma sesión de banco, no después.

**La buena noticia:** los valores correctos del DLPF **ya están escritos en el
repo** (la taxonomía los eligió bien para `lab` y `media`). No hay que
investigarlos: hay que centralizarlos en el driver y atarlos a la fs efectiva.

### V10 — el ancho de banda del sensor depende de lo que corrió antes

El DLPF se decide en **cuatro copias privadas** (una por misión) y el driver
compartido no es ninguna. Y el registro es **del chip**, no del programa: si se
vuelve a `mision = off` **sin cortar la alimentación** —un `cfg mision off` + reset
por software— el lazo clásico mide con el filtro de la misión anterior; arrancando
de cero, con 260 Hz. **El mismo código mide distinto según lo que pasó antes**, y
nada lo registra: ni el dato, ni el header del CSV, ni el frame de LoRa. Dos
capturas del mismo nodo con el mismo `mpu_hz` pueden tener anchos de banda
distintos y no hay forma de saberlo después.

### V4 — el espectro se dibuja de ráfagas incompletas, y se congela así

El gateway **sabe** si la ráfaga está completa: arma `vibMask` (32 bits, uno por
chunk) y prende `vibReady`. Pero **`vibReady` se escribe 3 veces y se lee 0** —
bandera muerta, igual que `vibTotal`— y el JSON publica la ráfaga con
`if (n.vibN > 0 …)`: sale al aire **en cuanto llegó un chunk**, y la información
de completitud **no viaja**. El dashboard no puede saber que le falta la mitad ni
queriendo. Y encima cachea por id de ráfaga (`lastVib[node.id] === v.id`):
**dibuja la primera versión que ve y no la vuelve a dibujar.**

El timing dice que no es un caso de borde: el push a la nube es cada **1000 ms**
y el comentario del propio `nodo.py` dice que la ráfaga *"bloquea ~1-3 s mientras
captura+envía"*. Con `fft_auto = true` en **los tres nodos**, eso pasa cada
15-20 s, solo.

Mismo patrón que viene apareciendo en los otros repos —**el sistema informa por
un camino que no verificó**— con un agravante: acá la información para
verificarlo **existe, se calcula, y se tira**.

### V5 — los chunks perdidos se rellenan con datos fabricados

Un chunk que no llegó queda como 32 ceros (el buffer del gateway se inicializa
así). El dashboard los detecta y los rellena mutando el array in situ ⇒ una
**rampa inventada** que converge al vecino derecho. Medido (`--demo-gap`):

```
LIMPIA          -> pico 70.31 Hz  amplitud 0.2000 g
chunk 3 perdido -> pico 70.31 Hz  amplitud 0.1753 g  (-12.3 %)
chunk 0 perdido -> pico 70.31 Hz  amplitud 0.1785 g  (-10.8 %)  [relleno PLANO]
```

**La frecuencia sobrevive; la amplitud no.** Eso es más incómodo de lo que
parece: el número que se usaría para decir *"esta máquina vibra más que ayer"* —
la métrica de un servicio de monitoreo— **se degrada con la calidad del enlace
LoRa**, que es justo lo que cambia cuando el nodo se aleja o llueve. Una
tendencia de amplitud a lo largo de semanas mezcla vibración con RSSI. Y **nadie
cuenta chunks perdidos**: ni el nodo, ni el gateway (tiene la máscara y no la
publica), ni la nube.

### V2 / V3

- **V2** — `burst_hz` acepta hasta **4000 Hz** y `eco_hz` hasta 2000, con la ODR
  fija en 1 kHz: a 4000 cada muestra se lee **4 veces** y el espectro muestra la
  máquina al 25 % de su frecuencia. El default (1000) es *exactamente* la ODR:
  dos relojes de 1 kHz sin sincronizar se repiten y se saltean muestras al azar.
  Y el indicador que existe no lo ve: **`real_hz` mide el lazo de lectura**, no
  la tasa a la que el sensor entrega datos nuevos.
- **V3** — `MPU6050.read()` divide por el literal `16384` ignorando
  `self.accel_lsb`, que es el campo que el propio driver mantiene. `capture_burst`
  sube a ±8 g y restaura dentro de un `except: pass`: si eso falla, **todo el
  canal continuo queda a ¼ de escala** y la gravedad marca 0,25 g — un valor
  plausible que nadie lee como error. Y `eco.py:204` escribe
  `accel_LSB_per_g=16384` **fijo** en el header del CSV, que es lo que
  `analysis.py` usa para reescalar.

### V6 / V7 / V8 / V9

- **V6** — `fftMag` recorta a la potencia de 2 más cercana y descarta el resto en
  silencio (`burst_n=1023` ⇒ **-50 % de muestras**); y el gateway topea en
  `vib[512]` mientras `burst_n` llega a 1024, **marcando los chunks descartados
  como recibidos** ⇒ `vibReady` dice "completa" con la mitad. Los dos límites
  están en repos distintos y nada los ata.
- **V7** — el dashboard **no aplica ninguna ventana**: el mismo tono se reporta
  con **36 % menos de amplitud** (-3,81 dB medido) según dónde caiga respecto del
  bin, y la UI imprime `toFixed(0)` sobre un bin de **3,9 Hz** ("66 Hz" cuando el
  dato es "entre 64 y 68"). El laboratorio hace lo contrario y tampoco cierra:
  Hanning sin corregir ganancia coherente y después normalizado al pico ⇒ su
  espectro es **adimensional**. **La misma ráfaga da dos amplitudes distintas y
  ninguna declara la ventana.** Para el final de **Medidas Electrónicas 2**
  (incertidumbre, resolución, trazabilidad) esto no es prolijidad: es el
  contenido de la materia.
- **V8** — `sim_data` tiene default **`True`**: una placa recién flasheada (o
  después de `config.reset()`) **inventa senos y los archiva en la SD** con un
  header idéntico al de una medición real, e `import_sd_csv` no puede
  distinguirlos. Los tres `config.P*.json` lo apagan: hoy se salva **por
  configuración, no por diseño** — y un nodo nuevo (Santa Cruz) nacería
  inventando.
- **V9 (info)** — la ráfaga mide un solo eje y nada registra la orientación
  física del sensor. Una amplitud sin dirección no entra en un informe, y el
  informe es el producto (#13).

### Lo que está BIEN y queda fijado por test

Tan importante: es lo que **no** hay que ir a revisar.

- **El chunk del nodo y el del gateway coinciden** (32): el reensamblado pone
  cada muestra en su lugar.
- **El nodo mide la tasa real de la ráfaga y la transmite, y el dashboard usa esa
  tasa para el eje de frecuencias** en vez del nominal: si el lazo no llega a
  1 kHz, el eje se corrige solo. Está bien pensado.
- **`fdom = di·hz/N` es la fórmula correcta** del centro de bin y el eje se
  rotula hasta Nyquist: el eje está bien **construido** — el problema es su
  resolución, no su escala.
- **La ráfaga transmite el `lsb` real del driver**, no un literal: ese camino es
  autoconsistente de punta a punta.
- **La ráfaga a 1000 Hz tiene Nyquist 500 > 260 Hz de BW ⇒ el camino de la
  ráfaga NO aliasea.** El plegado es exclusivo del canal continuo. Vale decir la
  inversión en voz alta: **el espectro lindo del dashboard es el honesto; el
  registro largo de la SD, el que respalda el DoD, es el aliaseado.**
- **`analysis.py::fft_uniform` resamplea a grilla uniforme** antes de la FFT: el
  lado laboratorio sí se hace cargo del jitter (el dashboard asume uniformidad).
- **`import_sd_csv` lee el LSB del header** en vez de asumirlo.
- **Las cuatro misiones sí configuran el DLPF**, y `lab` (1000/184) y `media`
  (333/94) están **correctamente filtradas**: ese trabajo está hecho y no hay que
  repetirlo.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-10-cadena-vibracion
python tools/check_vibration_chain.py                  # -> 5 error / 4 warn / 1 info, exit 1
python tools/check_vibration_chain.py --json
python tools/check_vibration_chain.py --demo-alias      # el número que miente (V1)
python tools/check_vibration_chain.py --demo-gap        # la amplitud que se pierde (V5)
python tools/check_vibration_chain.py --demo-window     # el scalloping (V7)
python -m unittest tools.test_check_vibration_chain     # -> Ran 82 tests, OK
python -m unittest tools.test_misiones                  # -> 20 OK (regresión intacta)
```

V1 se comprueba **sin la herramienta**, leyendo dos lugares: los `writeto_mem` de
`mpu6050.py` (no está `0x1A`) y `mpu_hz` en `config.P1.json`. V4 igual: buscar
quién **lee** `vibReady` en `esp32_dashboard.ino`.

`TestRepoReal` **fija los 10 hallazgos** y la tabla completa de rutas (cuáles
pliegan y cuáles no): si alguien arregla una, el test falla y obliga a actualizar
`docs/vibration-chain.md` en el mismo commit.

**Verificado por mutación** — las 7 hacen fallar la suite: rellenar los huecos
sobre una copia en vez de in situ, anclar el regex del gate a `vibN`-primero,
cortar el cuerpo de una función JS en la primera `}`, asumir `DLPF_CFG = 6` en
vez de 0, sacarle la escala `·2/N` al DFT, usar la fs **nominal** de `mision_baja`
en vez de la que le deja `mpu_hz`, y **juzgar el aliasing por la fs en vez de por
Nyquist**.

**Un hueco real de la suite, encontrado por la última mutación:** confundir
`fs/2 < BW` con `fs < BW` **no rompía ningún test**, porque con los valores reales
del repo los dos criterios dan el mismo veredicto. Agregué el caso que los separa
(`fs = 150` con `BW = 94` pliega **aunque la fs sea mayor** que el ancho de banda)
y el del borde exacto (`fs = 2·BW` no se marca, para no inventar hallazgos). Vale
anotarlo como método: **las mutaciones no sólo validan los tests, encuentran los
que faltan.**

## Qué quedó sin verificar (banco — trabajo de día)

Todo está **leído del código y del register map, no observado en una placa**. Lo
bueno: **nada de esto necesita instrumental** — alcanza el Pico en el banco con
el Serial abierto. En orden de valor:

1. **V2 en 10 minutos:** capturar una ráfaga y **contar muestras consecutivas
   idénticas**. Con el `read_raw` realmente sincronizado, duplicados exactos en
   16 bits serían raros; una tasa alta los confirma y **mide** cuánto se está
   repitiendo.
2. **V1 con un generador o un motorcito:** excitar el sensor a ~66 Hz y comparar
   lo que reporta la ráfaga (debería ver 66) contra lo que reporta el CSV a
   50 Hz (debería ver 16). Ahí V1 pasa de deducción a medición.
3. **V4 en un minuto:** mirar el `[vib] … rafaga N completa` del Serial del
   gateway contra el momento del push, o directamente apretar "📈 Capturar
   vibración" diez veces y contar cuántos espectros salen con un tramo raro.
4. **V3:** forzar el `except` de la restauración de rango (o hacer `set_accel_range(8)`
   a mano) y ver si la gravedad pasa a marcar 0,25 g.

Límites, escritos para no confundirlos:

- **No compilé firmware ni bajé toolchains** (regla de disciplina de tiempo). La
  auditoría es estática.
- **No hay `npm run build` que correr**: `vercel-dashboard/` es HTML estático +
  funciones serverless (su `package.json` no tiene `scripts`). Sólo lo leo.
- **Los oráculos numéricos demuestran el EFECTO de lo que dice el código**, no
  que la placa lo haga. Ningún número de jitter, amplitud o frecuencia salió de
  hardware.
- **La herramienta audita `firmwares/pico2w-node/`.** Revisé a mano las otras
  tres copias del driver (`pico2-lora-com10/`, `pico2w-wifi-com13/`, `pico/`):
  **ninguna escribe `0x1A` tampoco** — de hecho ninguna escribe ni
  `ACCEL_CONFIG` — así que **V1 vale para las cuatro**. No las metí en el checker
  para no atarlo a copias que el `QUE_HACER` trata como legacy.
- **Ningún fix aplicado** — generator ≠ evaluator, y el primero de la lista (¿qué
  mide el canal continuo?) es una decisión de diseño con dueño (@muestreador).

## Estado

- Branch `nocturno/local-2026-08-10-cadena-vibracion` pusheado (2 commits:
  `42b8781` la auditoría, `c82efed` la generalización a las rutas de muestreo + los
  11 tests nuevos). datalogger volvió a `main` limpio.
- `QUE_FALTA.md` de datalogger: ítem **#15** nuevo + notas en el **bloqueante #1**
  y en el **#5** (en el branch).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Octava noche que lo reporto:** es un firmware que va a un equipo a 2000 km y
  vive **sólo en este disco**. **No lo toqué.**
- ℹ️ `C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main` (estado previo). **No
  lo cambié.**
- ℹ️ `C:\Proyectos\datalogger` tiene sin trackear `docs/CONEXIONES_LAB.html`
  (previo). **No lo toqué.**
- ⚠️ Queda el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando Matías quiera.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las trece
  noches anteriores). **No los toqué.** Matías: commitealos, o la rutina cloud
  choca en el próximo `git pull`.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` está **vacío** (sólo el `.gitkeep`) — no
  hay pedidos sin atender. El único `enlace\maquinas\*.estado.json` tiene
  `ultima_vez_viva` del **2026-07-07**: hace un mes que ninguna máquina late. El
  latido no está corriendo (o `latido.ps1`, que está entre los archivos sin
  commitear, quedó a medio cambiar). **No lo toqué** porque toca los scripts del
  protocolo, que son trabajo de día sin commitear.
- La cola de merge suma **50 branches** en origin (galgas 18, datalogger 16,
  frioseguro 15, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo
  y sin usar: falta la sesión humana.
  **Nota de prioridad:** de los 16 de datalogger, éste es el único que mira **qué
  significan los números**, y su valor **caduca**: sirve *antes* de la sesión de
  banco del bloqueante #1. Si el banco se hace primero, se elige runtime con un
  benchmark impecable sobre un canal que mide el alias.
