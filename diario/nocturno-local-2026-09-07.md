# Nocturno local — 2026-09-07

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (**P0 octubre**, y con el frente comercial
abierto: hay cámaras compitiendo adentro de Dreyfus y la reunión con Juliano ya
pasó).
**Branch:** `nocturno/local-2026-09-07-la-trama-que-nadie-leyo` (pusheado, `7ad6d50`).
**Sale de `origin/main` (`515bf87`) limpio.**
**No toca el firmware del nodo** (ni el `.ino` ni `config_nodo.h`), ni SQL, ni
`data/field_captures/`, ni nada del ESP32, ni `hardware/kicad/`.
**No colisiona con ningún branch abierto.**

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_galgas`, ya
eliminado) porque el árbol de `galgas` tiene el KiCad de Matías sin commitear
(la rev G a medio cerrar: `nodo_galga_v3.kicad_pcb`, `drc.rpt`, `salida/e1.ses`,
`e2.dsn`, `e2.ses`, `puentes.json`) y un `checkout` lo habría tocado.
**Verificado al terminar: el árbol quedó idéntico**, en el branch
`nocturno/local-2026-09-05-la-potencia-que-nadie-cambio` donde estaba, con los
mismos 6 archivos modificados/sin trackear.

---

## TL;DR

> **El nodo transmite y nadie recibe.** No es una figura: `esp_rx_receptor` no
> tiene **una sola línea de LoRa** — hoy le entran las lecturas por HTTP. O sea
> que **ninguna trama de este nodo fue decodificada nunca por nada**, y el
> contrato que las describe está escrito en dos copias que nadie comparó: las
> tablas C2.x del doc (de donde va a salir el receptor) y `armarTrama()` /
> `armarTramaDiag()` (lo que sale al aire). **Las tramas se parsean por
> offset**: si esas copias se corren un byte entre sí, el sistema **no falla** —
> entrega un número plausible y falso al LCD, a Supabase y a la comparación A vs
> B, que es la lógica de detección entera.

## Por qué esta tarea

1. **El doc lo pide y lo llama «el más importante de todos».** C5.2.1 de
   `COMMS_REV_D.md` es un aviso de @firmware a @comms del 03-09: *«el nodo al
   menos falla al compilar si se pasa del buffer; **el receptor nunca falla**,
   entrega un valor plausible y falso»*. Enumera cinco barreras y las deja
   asignadas a «@firmware (receptor), 6 días». Cuatro de las cinco **no
   necesitan el receptor** para escribirse, y escribirlas ahora es lo que
   impide que el receptor nazca corrido.
2. **Es lo único del enlace que se puede hacer sin hardware.** La radio del RX,
   el `radioTask`, el alcance, el soak: todo eso necesita placas. El contrato de
   trama no.
3. **Baja el punto 3 de los 6 días de C5.3** sin tocar el resto de la
   estimación. El parser del receptor pasa a hacerse **incluyendo** un header,
   no reescribiéndolo.
4. **Lo que ya existía no cubre esto.** `cruzar_largos_de_trama()` de
   `check_pinout_nodo_v3.py` cuenta **cuántos** bytes escribe el encoder contra
   los largos declarados. Eso caza el campo que se agrega y no mueve el largo.
   **No caza el campo que se mueve**: intercambiar dos campos de un byte, o
   correr uno y compensar con otro, deja el conteo intacto, el doc intacto y el
   receptor leyendo corrido para siempre. Y no mira el doc, que es la copia de
   la que va a salir el receptor.

## Qué hice

### `firmware/shared/trama_revd.h` — la tabla de offsets, una sola vez

Puro a propósito (`stdint.h`, `stddef.h` y nada más: sin Arduino, sin SPI, sin
`String`), incluido por el test — **lo que se testea es lo que se flashea**,
mismo criterio que `ota_rescue.h` acá y que `sensor_fault_model.h` en
FrioSeguro. Va en `firmware/shared/` y no en el sketch del receptor para ser la
**copia única**.

Implementa 4 de las 5 barreras de C5.2.1: tabla única de offsets con
`static_assert` de que el último campo cierra el largo declarado · **largo
EXACTO** (`n != 22 && n != 9`, nada de `if (n > max) n = max`, que es el patrón
que el doc prohíbe porque hace que una trama de 23 bytes parsee «bien») · el
`tipo` identifica el **layout** y no el contenido · plausibilidad en runtime.
Más `trArmarC0()`, que vive acá y no del lado del receptor porque **el XOR del
`chk` es el único cálculo que los dos extremos tienen que hacer igual**, y
hacerlo distinto no da error: da una trama que el nodo descarta en silencio y un
comando que «se pierde».

### El hallazgo: el `id 0x00` se descartaba en silencio

C2.0 dice, con diez líneas de diferencia:

- *«si `tipo` no es conocido o **`id` no está en la tabla, se descarta en
  silencio y se cuenta**»* — y la tabla es `0x01`, `0x02`, `0x10`, `0xFF`;
- *«Default de fábrica `0x00` = sin asignar: un nodo con `id=0` **transmite
  igual, pero el receptor lo muestra como `NODO SIN ID`**. **Falla ruidosa, no
  silenciosa.**»*

`0x00` no está en la tabla. La barrera 5 lo refuerza en la dirección equivocada
(*«`id ∈ {1,2}`. Si falla: `trama_implausible++` y se descarta»*).

**Y `0x00` no es un caso exótico: es el estado de fábrica**, el de un nodo recién
flasheado al que todavía nadie le escribió la EEPROM — o sea, **el momento exacto
de la instalación en el REDLER**, con la placa en la mano y el instalador
esperando ver algo. Escrito así, **un nodo sin `id` se ve idéntico a un nodo que
no transmite**: mismo silencio en el LCD, misma ausencia en Supabase, y el
diagnóstico manda a mirar la antena, la radio o la pila cuando lo que falta es un
byte de EEPROM.

Se resuelve separando lo que estaba mezclado: **decodificar** es leer los bytes
(sale bien — el layout no depende del `id`), **mapear** es decidir de qué cadena
es (no sale — no hay cadena). Tres resultados y no dos, misma doctrina que los
flags de validez de temperatura de FrioSeguro:

| `id` | Decodifica | Mapea a cadena | Qué hace el receptor |
|---|---|---|---|
| `0x01` / `0x02` | sí | `'A'` / `'B'` | lo de siempre |
| **`0x00`** | **sí** | **no** | LCD `NODO SIN ID`, contador propio; no entra en la comparación A vs B |
| `0x10`, `0xFF`, otro | no | — | descarte silencioso + contador |

Anotado en el contrato como **C2.0.1** para que @comms lo firme o lo corrija —
mismo procedimiento que usó el branch del 09-05 con C2.4.2.

### Dos correcciones a la barrera 5, con el número al lado

- **El piso de `vbat` no es 2000 mV, es 1500.** El nodo transmite la trama corta
  justo para avisar que la pila se terminó (`VBAT_MV_AGOTADA = 2850 mV`) y sigue
  transmitiendo mientras el BOD lo deje — y el `BODLEVEL` adoptado es **1,8 V**.
  Un piso de 2000 mV descartaría por implausibles **las últimas tramas de un nodo
  agonizante**, que son exactamente las que hay que ver.
- **`n = 0` es legal.** El doc dice «`n < 60` = medición degradada», no
  imposible.

### Los otros dos archivos

- `tools/test_trama_revd.cpp` — **barrera 3, la trama de oro**: cuatro vectores
  fijos en hexa (`0xA3` larga, `0xA3` corta de pila agotada, `0xA4` cédula, `0xC0`
  downlink) con sus valores decodificados esperados.
- `tools/check_trama_revd.py` — cruza **las tres copias** campo por campo
  (nombre, offset, tamaño), más largos, tipos, flags, comandos e `id` entre
  `config_nodo.h` y el header; y verifica que el decoder **use** cada offset que
  declara y que aplique las barreras 2 y 5.
- `docs/trama-revd.md` — el detalle.

## Cómo verificarlo (exacto, sin hardware ni nube)

```
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-09-07-la-trama-que-nadie-leyo

g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_trama_revd.exe tools/test_trama_revd.cpp
./tools/test_trama_revd.exe                    # 124 checks OK, 0 fallos
python tools/check_trama_revd.py               # OK: las tres copias dicen lo mismo
python tools/check_trama_revd.py --mutantes    # 17/17 muertos
python tools/check_pinout_nodo_v3.py           # sigue OK (no se tocó el nodo)

g++ -std=c++11 -Wall -Wextra -Wpedantic -c -o /dev/null -x c++ firmware/shared/trama_revd.h
```

**Resultados de esta noche:** `124 checks OK, 0 fallos`, sin warnings ·
`17/17 mutantes muertos` · el header compila solo en **c++11** (el estándar del
core ESP32) con `-Wpedantic` · `check_pinout_nodo_v3.py` sigue OK.

Los checks que valen: el **corrimiento de un byte en las dos direcciones**, la
trama de 23 bytes y la de 21, una `0xA6` de 22 bytes que **no** se interpreta
como `0xA3`, el largo y el bit `flags.b2` que tienen que concordar en los dos
sentidos, el `id 0x00` como regresión, que **la trama corta no inventa lo que no
viajó** (`media`/`ganancia`/`n`/`ack` en cero explícito con `t.corta` al lado, en
vez de publicar el cero de la inicialización como si fuera medición — la
enfermedad de la temperatura congelada de FrioSeguro), y que **el `ack` de la v1
que escribe el nodo hoy decodifica exacto bajo la v2 de C2.4.1** (los `cmd` van
de `0x00` a `0x07`, así que `b7=0` y `b6-b4=0`): **el receptor se escribe una sola
vez, contra C2.4.1, y anda con el firmware de hoy y con el que traiga el NACK**.

Mutantes que motivaron el checker y que ahora mueren: «se intercambian dos campos
de 1 byte (el conteo no cambia)», «el encoder mueve la ganancia después de `n`»,
«el doc corre un offset y el código no», «vuelve el defecto: el nodo sin id se
descarta en silencio» y «el `chk` del downlink pierde la clave de sitio».

## Qué quedó SIN verificar (necesita banco / hardware)

1. **La trama de oro no vino del aire.** Los vectores salen de ejecutar el
   encoder a mano, y el checker garantiza que el encoder escribe esos campos en
   esos offsets. Lo que cierra el lazo de verdad es **capturar una trama real con
   el sniffer y pasarla por `trDecodificarA3()`** — ensayo 2.c de
   `BRINGUP_BANCO.md`. Hasta entonces **esto es un contrato verificado contra sí
   mismo**, y así está escrito en el doc.
2. Nada más de esto depende de hardware: los tres archivos corren en la PC.

## Pedidos que abre (por dueño)

- **@comms** — firmar o corregir **C2.0.1** (el `id 0x00`) y las dos
  correcciones a la barrera 5 (piso de `vbat`, `n = 0`). Es su contrato.
- **@firmware (nodo)** — el NACK de C2.4.1 (prender el `b7` del `ack`). Mientras
  no esté, el receptor no puede distinguir «no ejecuté» de «no me llegó»: son 25
  minutos reintentando un comando que el nodo rechaza siempre.
- **@backend** — las columnas nuevas de Supabase (`nodo_id`, `seq`, `boots`,
  `mcusr`, `flags`, `n`, `ganancia`, `rssi`, `snr`), y ahora también **qué hace
  con un `nodo_id = 0`**.
- **@firmware (receptor)** — cuando arranquen los 6 días de C5.3, el parser se
  hace **incluyendo** `firmware/shared/trama_revd.h`, no reescribiéndolo.

## Drift corregido de paso

`QUE_FALTA.md` de galgas figuraba con tres branches «🔀 EN BRANCH … pendiente de
merge» que **ya están en `main`** (verificado con `git branch --merged main`):
`09-01-el-rescate-desarmado`, `09-03-el-adc-que-no-se-apaga` y
`09-05-la-potencia-que-nadie-cambio`. Se agregó un aviso arriba de la sección de
bloqueantes en vez de reescribir los cinco párrafos: el texto de cada uno vale
como bitácora de qué se hizo, el estado no. Con ellos entró también la
duplicación de #3 y #4b que el propio branch del 09-05 había anotado. [@cronista]

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-07-la-trama-que-nadie-leyo` (`7ad6d50`).
- Worktree `C:\Proyectos\_noche_galgas` eliminado; el árbol de `galgas` quedó
  **idéntico**, con la rev G de KiCad sin commitear como estaba.
- Nada corriendo, nada abierto.
