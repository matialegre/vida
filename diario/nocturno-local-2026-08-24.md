# Nocturno local — 2026-08-24

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "terminarlo antes del trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-24-fase-prod` (pusheado, `aabe7a9`).
**Sale de:** `nocturno/local-2026-08-08-fidelidad-benchmark` → **mergear ese primero.**
No depende de la cadena de batería (`08-17` → `08-18-b` → `08-20` → `08-22`): son
archivos distintos.

## TL;DR

> **El benchmark que decide el bloqueante #1 nunca midió el firmware que va a correr —
> y la auditoría que lo descubrió tampoco había abierto el archivo donde está el lazo.**

La auditoría del 08-08 comparó el bench contra `nodo.py:tick()`. Pero producción no es
`tick()`: es el `while True` de `firmwares/pico2w-node/main.py` que lo llama. Ahí
adentro hay dos líneas que **ninguna fase del benchmark produce** y que le ponen un
techo al muestreo:

```python
if time.ticks_diff(time.ticks_ms(), last_gc) > 5000:
    gc.collect()                                  # B14 — una pausa de GC AGENDADA
sleep_ms = max(1, min(20, period // 4))
time.sleep_ms(sleep_ms)                           # B13 — el techo de la fs
```

| fs objetivo | periodo | micro-sleep | % del periodo |
|---|---|---|---|
| 100 Hz | 10 ms | 2 ms | 20 % |
| 200 Hz | 5 ms | 1 ms | 20 % |
| 500 Hz | 2 ms | 1 ms | **50 %** |
| 1000 Hz | 1 ms | 1 ms | **100 %** |

A 1000 Hz el micro-sleep se come el período entero: **`fs_real < fs_obj` por
construcción, gane MicroPython o gane C.** Y `fs_real < 0.99·fs_obj` es la fila 4 de
la tabla de decisión, la que manda a C. **Hoy esa fila la puede disparar la
implementación, no el runtime, y el benchmark no lo distinguiría.**

Y el tercero, del mismo tirón: **B10** — la fase D transmite cada **2000 ms** y
`config.py` tiene `lora_period_ms = 200`. La contención de SPI0 (LoRa y SD comparten
el bus) está medida **10× por debajo** de la real, justo en el escenario de la fila 1
de la tabla (*"a 500 Hz con SD+LoRa"*).

## Tarea elegida y por qué

Por rotación tocaba datalogger: las cuatro noches anteriores fueron datalogger (08-22),
galgas (08-22-b), frioseguro (08-23) y cosechador (08-23-b), y datalogger era el más
viejo del par que quedaba.

Dentro del repo seguí el patrón que viene funcionando: **no abrir una auditoría nueva,
tomar un pendiente ya nombrado con su evidencia.** La auditoría del 08-08 cerró con una
propuesta de cinco pasos en orden. El paso 1 necesita banco. El **paso 2 no**, y está
escrito así:

> *"Si pasa, **agregar una fase `PROD`** en la misma sesión: `tick()` instrumentado.
> **La diferencia entre C y PROD es el presupuesto que se está regalando en la
> implementación**, y es accionable con o sin migrar de runtime."*

Elegí ése y no otro por tres motivos:

1. **Es el único paso de la lista que se puede hacer entero de noche** y que cambia lo
   que la sesión de banco produce. Los otros cuatro son: correr el bench (hardware),
   anotar `cpu_mhz` (una línea del README, la hice de paso), decidir `fft_auto`
   (arquitectura, es de Matías) y tres one-liners.
2. **Su valor caduca.** Sirve *antes* de la noche de banco. Si el banco se hace primero,
   se gasta la noche de hardware midiendo el lazo equivocado y hay que repetirla.
3. **Es el bloqueante #1**, el que el propio `QUE_FALTA` llama *"LA decisión fundacional:
   todo lo demás se construye arriba"*. De los 16 branches de datalogger, éste y el
   08-08 son los únicos dos que lo tocan.

## Qué hice

**`capture_prod()` + `ProdSD`** en `benchmark/bench_micropython.py`. Corren a las
**mismas fs y la misma duración** que A–D, así que las columnas se comparan directo.
Cada diferencia con `capture()` es deliberada y está para **medirse**, no para evitarse
— y cada una tiene su hallazgo de la auditoría anterior:

| eje | `capture()` (A–D) | `capture_prod()` (P) | |
|---|---|---|---|
| lectura MPU | `read_raw()` → tupla | `read()` → dict + 7 divisiones float | B2 |
| pacing | deadline en µs | deadline en **ms**, con el resync de `tick()` | B3 |
| SD | bloque binario de 4086 B | **línea CSV `%.4f`**, flush cada 100 líneas / 2 s | B1 |
| SPI | `for_sd()` sólo en fase D | `for_sd()` **en cada escritura** | B6 |
| LoRa RX | nunca escucha | `start_rx()` + `poll_rx()` **cada vuelta** | B5 |
| LoRa TX | cada 2000 ms | cada **200 ms**, con listen-before-talk | B10 |
| micro-sleep | no existe | `sleep_ms(max(1, min(20, period_ms // 4)))` | B13 |
| GC | `collect()` antes, nunca adentro | **nunca antes**, `collect()` cada 5 s | B14 |

**El checker no valida la fase P contra una copia mía**, valida contra producción:
`PROD_LORA_MS` se compara con el default de `config.py`, `PROD_GC_MS` y la fórmula del
micro-sleep con lo que hay en `main.py`. Los umbrales no están escritos dos veces a
mano.

**Cada eje de fidelidad tiene ahora tres estados**, y ése es el punto del branch:

- **sin fase P** → el nivel original (`error`/`warn`): el bench no mide producción;
- **fase P que espeja el eje** → `info` *(cubierto por la fase P)*. El hallazgo **sigue
  siendo cierto de `capture()`** — la fase C sigue midiendo el caso limpio — pero eso
  pasa a ser deliberado y su contraparte fiel existe;
- **fase P que dejó de espejarlo** → **`error`**: *"la fase P no espeja producción"*.

El tercer estado es el seguro. **Una fase P despegada de `main.py` es peor que no
tenerla, porque miente con nombre de verdad.** Once tests la rompen de a un eje y
verifican que el error vuelve.

**Resultado del checker:** de **3 error / 6 warn / 3 info** a **0 error / 3 warn /
11 info**, con paridad **6/6** (P4 cerrado: las líneas de SKIP llevan prefijo `#SKIP,`
en los dos lados y ya no se disfrazan de fila de datos — eran 3 líneas, una del bench y
dos de `main.c`).

**Lo que la fase P NO cubre, escrito para que nadie lo lea como fidelidad completa:**
**B9** (la ráfaga de FFT que bloquea 1–3 s) necesita `send_burst()` de `nodo.py`, que el
bench no copia al Pico — sigue abierto y sigue siendo de arquitectura. Tampoco el
`poll()` de `web.py`/`wifi_push.py`/`sd_server.py` ni el `cli_poll()`: van **encima**.
La fase P sigue siendo optimista, sólo que mucho menos.

**Una cosa que la fase P suma y producción no tiene**, dicha porque es la única en esa
dirección: la lectura de ADC del canal piezo. Va porque las fases B/C/D la tienen y P se
compara contra C.

**Archivos:** `benchmark/bench_micropython.py` (+223), `benchmark/bench_c/main.c` (2
líneas), `benchmark/README.md` (fase P, `cpu_mhz` obligatorio en los resultados, la
advertencia de leer P antes de la tabla), `tools/check_benchmark_fidelity.py` (+311),
`tools/test_check_benchmark_fidelity.py` (49 → 79 tests), `tools/test_fase_prod_logica.py`
(nuevo, 14 tests), `docs/fase-prod.md` (nuevo), `docs/benchmark-fidelity.md` (banner de
actualización), `QUE_FALTA.md` (bloqueante #1).

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-24-fase-prod

# 1. el bench es MicroPython: solo sintaxis
python -m py_compile benchmark/bench_micropython.py

# 2. el checker -> 0 error / 3 warn / 11 info, paridad 6/6, exit 0
python tools/check_benchmark_fidelity.py
python tools/check_benchmark_fidelity.py --fail-on warn    # exit 1: queda B4/B8/B9
python tools/check_benchmark_fidelity.py --json

# 3. los tests -> Ran 93 tests, OK (3,3 s)
python -m unittest tools.test_check_benchmark_fidelity tools.test_fase_prod_logica
```

**Verificado esta noche:**

- **93/93 tests OK** en 3,3 s (79 del checker + 14 de la lógica del lazo).
- `py_compile` del bench OK. El lado C **no se compiló** (ver abajo).
- **La lógica de la fase P se ejecutó de verdad, sin Pico.**
  `tools/test_fase_prod_logica.py` **extrae `ProdSD` y `capture_prod` del archivo real
  por AST** (no una copia pegada: si el bench cambia, los tests corren sobre el cambio)
  y los corre en CPython contra un reloj falso y periféricos con costos declarados. Eso
  verifica lo que un `py_compile` no puede: el deadline, el resync, la contabilidad de
  `late`/`gaps`, `sd_worst`, que las líneas de la SD sean las muestras y ni una más, y
  que un error de I2C **no** escriba una fila con los valores de la muestra anterior.
- **Mutación: 11 mutantes de la fase P, los 11 caen.** Volver a `read_raw`, pacear en µs,
  escribir binario, no flushear, sacar el `for_sd()` por línea, no escuchar la malla,
  colectar *antes* del lazo, no dormir, dormir con otro divisor, colectar con otro
  período, transmitir a la cadencia del bench. Más dos del `main.py`: el micro-sleep
  puesto en el `while` equivocado (hay **dos** que llaman `tick()` — el del comando
  `bench` de la CLI no tiene ni sleep ni GC, y quedarse con el primero que devuelve
  `ast.walk` apaga los dos controles **en silencio**) y `sleep_triple` contra cuatro
  formas que no son la de `main.py`.
- **Dos controles leen `config.py` de verdad**, no una constante: si el default de
  `lora_period_ms` fuera 2000, B10 **no** dispara. Misma trampa del `lambda` que ya
  había pisado B4.

**Los números del modelo** (`test_fase_prod_logica.py`, costos declarados: muestra
400 µs, línea CSV 120 µs, flush 1,5 ms, cambio de bus 20 µs, TX LoRa 60 ms):

```
fs= 100  fs_real=  100.0  gaps=  0
fs= 200  fs_real=  200.0  gaps=  0
fs= 500  fs_real=  499.9  gaps=  0
fs=1000  fs_real=  629.0  gaps=1572     <-- el micro-sleep, no el runtime
con LoRa a la cadencia real (200 ms):
fs= 200  fs_real=  200.0  gaps=  1
fs= 500  fs_real=  470.4  gaps= 39      <-- un evento por TX
```

⚠️ **Esto es un modelo, no una medición.** Los costos son parámetros de ese archivo.
Sirve para dos cosas y ninguna más: que la fase P no tenga un bug de contabilidad, y
que las fs candidatas del banco se elijan sabiendo dónde está el borde.

## Lo que quedó SIN verificar (y por qué)

- **Nada corrió en hardware.** Ni un número de jitter, consumo o stall sale de este
  branch. El bench sigue sin correrse: no existe `benchmark/resultados.md`, y hay un
  test que falla el día que aparezca — para obligar a releer la auditoría antes de
  creerle a los números.
- **No compilé el lado C** (regla de disciplina de tiempo: no bajar el Pico SDK de
  noche). Toqué dos `printf` de `main.c` (prefijo `#SKIP,`). **Verificación pendiente:
  que `bench_c` compile.** Comando para el día, desde `benchmark/bench_c`:
  `cmake -G Ninja -B build -DPICO_BOARD=pico2_w && ninja -C build` (instalador oficial
  del Pico SDK ≥ 2.1).
- **La fase P la escribí y la verifiqué yo.** El checker compara estructuralmente contra
  `nodo.py`/`main.py`/`config.py`, que son la referencia y no algo que yo haya escrito,
  pero **una lectura de @firmware antes del banco vale**: lo que hay que buscar es si
  `capture_prod()` **omite** algo que `tick()` sí paga.
- **`late`/`gaps` de la fase P subestiman los stalls repetidos.** Uso la misma
  definición que A–D para que las columnas se comparen, pero el lazo real se recupera
  con ráfagas y eso deja el deadline sombra adelantado. **La pérdida real de la fase P
  se lee en `n`/`fs_real`**, no en `gaps`. Está escrito en el docstring, en el README y
  en el doc.
- **Comparé contra `firmwares/pico2w-node/`.** Existe `firmwares/pico2-lora-com10/` con
  otra copia de los drivers: **no la miré** (mismo límite que el 08-08). Si el nodo del
  banco es ése, repetir el control de pinout.

## Próximo paso (para Matías, de día)

1. **Mergear `08-08` y después este.** Este sale de aquél.
2. **Leer `docs/fase-prod.md` antes de la sesión de banco.** Son 10 minutos y cambian
   qué se mide esa noche.
3. **En el banco:** correr el bench (~3,2 min ahora) y **mirar la fila P al lado de la
   fila C de la misma fs**. Si P falla y C pasa, **el problema no es el runtime**: es
   `read()` vs `read_raw()`, el CSV, el pacing en ms, el micro-sleep y el GC — cinco
   arreglos conocidos y baratos. Migrar a C sin mirar P es pagar un puerto entero por un
   problema de implementación.
4. **Decisión que sigue siendo tuya, y que ninguna de las dos noches tocó:** ¿`fft_auto`
   convive con el logging continuo? (B9). No depende del runtime, y hoy está tomada por
   default sin haberse discutido.

## Estado de los otros repos (no los toqué)

- ⚠️ **`C:\Proyectos\frioseguro` sigue con trabajo de día SIN COMMITEAR** —
  `kit_santacruz/`, `firmware_revival/`, `backup_supabase/`, `BOOTSTRAP_2026-08-19.sql`,
  dos `.zip`. **Ya van muchas noches reportándolo.** `BOOTSTRAP_2026-08-19.sql` es hoy el
  esquema de verdad y vive **sólo en este disco**.
- ℹ️ `datalogger` tenía `.gitignore` modificado y bastante sin trackear
  (`visor_gimap.py`, `firmwares/nodo-gimap/`, `tools/rx_gimap.py`, `probar_piezo.py`…).
  Es trabajo de día. **No lo toqué ni lo commiteé**: el `git add` fue archivo por archivo.
- ⚠️ **MATI-HQ sigue con trabajo de día sin commitear** (`dominios/muestreador.md`, y sin
  trackear `SESION_1_FRIOSEGURO_SANTACRUZ.md`, `SESION_2_DATALOGGER_PIEZO.md`,
  `SESION_3_PID_TORNO_UTN.md`). No los toqué.
- La cola de merge sigue creciendo. De datalogger, **este y el 08-08 son los únicos dos
  que tocan el bloqueante #1**, y su valor caduca el día de la sesión de banco.
