# Nocturno local — 2026-08-28 (segunda pasada, "-b")

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (**RuView** — P0, *"terminarlo primero,
antes del trabajo Dreyfus"*).
**Branch:** `nocturno/local-2026-08-28-b-el-chunk-que-no-entra` (pusheado, `b8df100`).
**Sale de:** `nocturno/local-2026-08-26-b-la-rafaga-que-ensordece`.
**Orden de merge: `08-26-b` PRIMERO, éste después.** (La primera pasada de esta
noche, `08-28`, es de galgas y no se cruza con nada de acá.)

## Por qué esta tarea

`QUE_FALTA.md` de datalogger tenía el ítem **#14 en rojo**, abierto anoche por el
propio worker y dejado sin arreglar **a propósito** ("es un cambio coordinado de dos
firmwares, no es trabajo de una noche sin banco"). Era el único pendiente de software
puro que no estaba ya esperando merge, y el más caro de descubrir tarde: falla **solo
con vibración fuerte**, o sea que en el banco con la mesa quieta no aparece nunca —
aparece en Dreyfus, en octubre.

Resultó que **sí** es trabajo de una noche, porque el arreglo correcto no era el que
estaba anotado (bajar `CH` en los dos lados y rezar por flashearlos juntos).

## TL;DR

> **El chunk de ráfaga se pasaba de 255 B justo cuando el golpe era fuerte, y el
> número que lo definía estaba escrito dos veces, en dos firmwares distintos, en
> dos lenguajes, que se flashean por separado.**

```
cabecera "RV1|P1|GW|1000001|3|B||"            23 B
prefijo del body "1 0 8 1000 z 16384 "        23 B
32 valores de hasta 6 chars ("-32768")       192 B
31 comas                                      31 B
                                             -----
                                             269 B      <-- REG_PAYLOAD_LEN es de 8 bits
```

269 se escribe como **13**. El frame no sale "un poco cortado": sale con un largo
equivocado y se pierde entero. Y los valores llegan a 6 caracteres cuando el
acelerómetro satura — **exactamente el evento para el que existe la ráfaga**.

El anotado decía "bajar `CH` de 32 a ≤29". El problema es que estaba acá:

```python
# firmwares/pico2w-node/nodo.py       (MicroPython, se copia por USB)
CH = 32
```
```c
// firmwares/esp32s3-com11/esp32_dashboard/esp32_dashboard.ino  (se compila y flashea)
const int CH = 32;               // muestras por chunk (igual que el nodo)
int off = seq * CH, ...
```

Ese comentario —*"igual que el nodo"*— **es** el bug. Bajarlo de un lado no tira
ningún error: el gateway desparrama las muestras en el buffer y la FFT que sale de ahí
es basura con forma de dato bueno.

## Qué hice

**1. El gateway deja de tener el número: lo aprende del aire.**
`burst_reasm.h` (nuevo, sin una línea de Arduino adentro) cuenta los valores de
cualquier chunk que no sea el último —todos están completos por construcción— y con
eso ubica los demás. `const int CH` desapareció del `.ino`, que quedó como un
adaptador de 12 líneas.

Consecuencia práctica: **no hay día D**. Se flashea el gateway cuando se pueda y los
nodos cuando se pueda:

| gateway | nodo | resultado |
|---|---|---|
| nuevo | nuevo (24) | correcto |
| nuevo | viejo (32) | **correcto** — aprende 32 (hay test) |
| viejo | viejo | como hoy (se pierden las ráfagas anchas) |
| viejo | nuevo | ⚠️ desparrama → **por eso: gateway primero** |

**2. El nodo: `BURST_CHUNK = 24`**, constante de módulo con la cuenta del peor caso al
lado (antes era un `CH = 32` local, invisible desde afuera). Peor caso **medido**
armando el frame de verdad: **210 B** (214 con un `aux_seq` de 10 dígitos). El guard de
255 que puso el branch de anoche queda: ahora es inalcanzable, y es la red para el día
que alguien lo suba de nuevo.

**3. Tres cosas más del mismo reensamblado, que salieron al mirarlo:**
- **Fantasmas**: el `.ino` no limpiaba `vib[]` al empezar una ráfaga nueva. Si a la
  nueva le faltaba un chunk **del medio**, el hueco se publicaba en `/api` con las
  muestras de la ráfaga **anterior**, indistinguibles de datos buenos. Ahora el hueco
  es cero.
- **`/api` decía "acá hay una ráfaga" sin exigir que estuviera completa**: se agregó
  `"ok": true|false`.
- **Ubicar a ciegas**: si el único chunk que llegó es el último (que puede venir
  corto), ya no se adivina el offset — se cuenta como huérfano.

**Lo que cuesta:** la ráfaga pasa de 8 a 11 chunks (3 frames más de aire, repartidos
entre ticks — el lazo no se frena, eso lo arregló `08-26-b`). Es el precio correcto:
11 frames que llegan valen más que 8 de los cuales los anchos se pierden enteros.

## Cómo verificarlo (comandos exactos, todo ya corrido en verde)

```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-28-b-el-chunk-que-no-entra

python -m unittest discover -s tools -p "test_*.py"      # 43 tests, OK
python -m unittest tools.test_chunk_que_no_entra -v      # los 16 nuevos, uno por uno
```

Los tests del gateway **compilan con g++ el header real** (`tools/burst_harness.cpp`
lo `#include`a) y le dan de comer los frames que produce el **código real del nodo**,
extraído por AST. **Cero líneas de firmware copiadas en los tests**: si el firmware
cambia, los tests corren sobre el cambio. Si no hay g++ en el PATH, esa parte se
saltea diciéndolo (la del nodo corre igual).

**El firmware del gateway compila de verdad**, con la toolchain instalada:

```bash
cd C:\Proyectos\datalogger\firmwares\esp32s3-com11\esp32_dashboard
arduino-cli compile --fqbn esp32:esp32:esp32s3 .
```

| | flash | RAM global |
|---|---|---|
| antes | 1.163.413 B (88%) | 90.260 B (27%) |
| después | 1.163.565 B (88%) | 90.332 B (27%) |
| delta | **+152 B** | **+72 B** |

⚠️ Dato aparte, no es de este cambio: el sketch está al **88 % del espacio de
programa**. Todavía entra, pero conviene tenerlo en el radar antes de que alguien le
agregue una feature grande.

**Mutaciones** (que los tests muerdan, no que pasen): 10 mutaciones sobre
`burst_reasm.h` y `nodo.py` —aprender el chunk del último chunk, no limpiar el buffer,
ubicar a ciegas, sin recorte de overflow, no marcar el chunk recibido, `n` que
retrocede, aceptar `seq` fuera de rango, volver a 32, chunk al filo (29), guard
desactivado. **Ninguna sobrevive.** (Las dos primeras corridas dejaron 2
sobrevivientes; los tests que las dejaban pasar se endurecieron hasta matarlas.)

## Qué quedó sin verificar (necesita hardware)

- **El aire.** 11 frames por ráfaga en vez de 8 con varios nodos hablando: no está
  medido que el canal aguante. Con `fft_period_s=15` debería sobrar, pero es aire, no
  aritmética.
- **Que el SX1278 real acepte los 210 B** sin otra sorpresa de registro.
- **Saturar el MPU a propósito** (golpear la mesa fuerte durante la captura): es el
  caso que fallaba y el único que prueba el arreglo de punta a punta.

Receta de banco, cuando haya hardware:
1. Compilar y flashear el **gateway primero**.
2. `flash_node.ps1` para el nodo.
3. `set fft_auto 1`, `set fft_period_s 15`, golpear fuerte.
4. Nodo por USB: `st` → `burst_oversize` en **0**.
5. Gateway por serie: `[vib] P1 rafaga N completa (256 muestras @ 1000Hz, chunk de 24)`
   — **el "chunk de 24" es la prueba de que lo aprendió**.
6. `/api` del gateway: `"vib":{...,"ok":true,...}` con 256 valores.

## Yapa (3 líneas, ajena al cambio)

`tools/test_misiones.py` tenía un `sys.exit()` en el cuerpo del módulo: el comando de
verificación que documentan los branches anteriores —`python -m unittest discover -s
tools`— **fallaba con ERROR** aunque sus 20 checks pasaran. Ahora sale con código sólo
cuando se lo corre como script. El comando de verificación del repo vuelve a ser
verde de verdad.

## Estado

- Branch pusheado, `QUE_FALTA.md` #14 pasó de 🔴 a 🔀 **EN BRANCH — pendiente de merge**.
- Detalle técnico completo en el branch: `docs/chunk-que-no-entra.md`.
- **Cadena de merge de datalogger:** `08-26-b` → `08-28-b` (éste). Los branches
  anteriores (`08-24`, `08-22`, `08-20`, …) siguen esperando y no tocan estos archivos.
