# Nocturno local — 2026-08-08

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "terminarlo primero, antes del trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-08-fidelidad-benchmark` (pusheado, commit `b82f551`).

## Tarea elegida y por qué

Por rotación tocaba datalogger (las tres noches anteriores fueron frioseguro,
galgas y galgas; la última de datalogger fue el 08-06-b). Y en el `QUE_FALTA` de
datalogger hay un ítem que ninguna de las 14 noches previas tocó: el
**bloqueante #1**, el que el propio documento llama

> *"LA decisión fundacional: todo lo demás se construye arriba."*

Miré por qué nadie lo agarró: porque **necesita banco**. Hay que flashear el Pico,
correr las 5 fases y leer jitter real. Nada de eso se hace de noche sin hardware.

Pero al abrir `benchmark/` encontré algo que sí se puede hacer de noche, y que hay
que hacer **antes** de gastar la sesión de banco:

- el harness está **completo y bien escrito** (5 fases, espejo en C, tabla de
  decisión con umbrales derivados de la física, no opinados);
- y **nunca se corrió** — no existe `benchmark/resultados.md`.

De ahí sale la pregunta que elegí responder:

> **¿el benchmark mide el firmware que va a correr?**

Nada la había respondido todavía. Y tiene dos filos que se pagan distinto:

| | Si está mal… |
|---|---|
| El bench llama una API que los drivers no tienen | se pierde **la sesión de banco**: `AttributeError` en el primer segundo, de noche, con el nodo ya cableado |
| El bench mide un lazo que no es el de producción | se pierde **la decisión**: sale un número lindo, se elige runtime con él, y todo lo que viene después se construye arriba |

El primero se arregla con 20 minutos de análisis estático. El segundo es la
diferencia entre acertar y no acertar el bloqueante #1.

**No pisa ningún branch previo.** Los 14 branches de datalogger son INA219, SD,
mesh RV1, RSSI, SSID, eco-schedule, contabilidad de registro y contratos de nube.
Ninguno mira `benchmark/`.

## Qué hice

**`tools/check_benchmark_fidelity.py`** (stdlib, solo lectura, sin red ni
hardware; no compila nada). Audita `benchmark/` contra `firmwares/pico2w-node/`
en dos ejes: **paridad** (¿los dos lados miden lo mismo, con APIs que existen?) y
**fidelidad** (¿ese lazo es el que corre en el nodo?). Exit 0/1/2, `--json`,
`--fail-on`, `--root`.

**`tools/test_check_benchmark_fidelity.py` — 49 tests en 5 capas:** utilidades de
parseo (Python por AST, C a mano), un test por control de paridad y de fidelidad
con **repos sintéticos armados en disco**, la regresión sobre el repo real, y el
CLI.

**`docs/benchmark-fidelity.md`** — el análisis completo y la propuesta.

Lo que hubo que resolver:

- **El AST, no regex.** `bench_micropython.py` es MicroPython pero **sintaxis
  Python 3 válida**: parsea con `ast` sin ejecutar nada (los `import machine` no
  se resuelven). Eso permite comparar *estructura* — qué método se llama sobre
  qué objeto, dentro de qué rama — en vez de adivinar con texto.
- **`calls()` devuelve un set, y eso arruinó un control entero.** El detector de
  B6 pregunta "¿hay alguna llamada a `for_sd()` **fuera** de la rama de LoRa?".
  Contándolas sobre el set, dos llamadas colapsan en una y la respuesta es
  siempre "no": **el control disparaba hasta en un repo sintético limpio.** Hay
  que trabajar sobre los nodos `Call`, que sí son distintos. Lo agarró el test
  del repo limpio, que existe justamente para eso.
- **`%%` hay que consumirlo en la misma pasada.** Filtrarlo después no alcanza:
  en `100%% libre`, el segundo `%` se come el espacio como flag y la `l` como
  modificador de longitud, y la `i` de `libre` queda de conversión. Contaba 1
  donde va 0 — y de esa cuenta depende medir el ancho de las líneas `#RES`.
- **`nodo.py` aparece en prosa en el README y NO se copia.** Buscar
  `pico2w-node/*.py` en todo el archivo lo mete en la lista de módulos copiados,
  y entonces sus `import config` / `import network` se leen como dependencias
  faltantes: **un error grave que no existe.** Hay que buscar sólo dentro de la
  línea del `mpremote ... fs cp`.
- **El bench alias-ea `pack = struct.pack_into`** antes del lazo (para no pagar el
  lookup por muestra). Un detector que busque `struct.pack_into` no ve nada, y el
  hallazgo B1 — el más importante de los tres errores — desaparece.
- **`literal_eval` sobre las entradas de `config.py` revienta:** son
  `(default, tipo, lambda, ayuda)` y el validador es un `lambda`. La excepción se
  come el default y **el control B4 se apaga solo**, en silencio. Hay que leer
  `elts[0]` del `Tuple`.
- **Sacar comentarios de C sin comerse las comillas** (misma lección que las
  noches del contrato de la nube, el REVIVAL y el schema).

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **paridad 5/6 · 3 error / 6 warn / 3 info.**

### Lo que está BIEN, y es lo primero que hay que saber

**El harness está sano: se puede flashear tal cual.** Esto es tan importante como
lo otro, porque es lo que NO hay que ir a revisar en el banco:

- **Los 9 pines coinciden con `nodo.py`** (I2C, SPI0, los tres CS, RST, DIO0), y
  los que el lado C define también.
- **`FS_TARGETS`, `DUR_S`, `FREERUN_S` y `N_MAX` son idénticos** entre MicroPython
  y C: la comparación es peras con peras. Las 4 fs objetivo tienen periodo entero
  en µs (el deadline no arrastra).
- **El `#HDR` de 17 columnas es el mismo en los dos lados**, y coincide con la
  cantidad de `%` y de argumentos de cada `#RES`.
- **Todas las APIs que el bench llama existen**: `MPU6050.read_raw()`,
  `SX127x(cs=, reset=, dio0=, freq_hz=, tx_power=)`, `send(timeout_ms=)`,
  `_read()`, `SDCard(spi, cs, baudrate=)`. **Nada garantizaba esto antes** — el
  bench nunca se ejecutó.
- **El `mpremote fs cp` del README está completo**: los 3 drivers no importan nada
  fuera de `machine`/`time`/`struct`/`micropython`.
- `REC_BYTES = 18` es exactamente el ancho de `<Ihhhhhhh`.

### Los 3 errores: el bench y el nodo no son el mismo programa

El README promete *"el MISMO loop que `nodo.py`"*. Los pines sí; el loop, no.
Elige bien la referencia cuando dice *"estilo `capture_burst`"* — el problema es
que **`capture_burst()` no es el lazo del que habla el DoD.** `nodo.py` tiene dos
caminos de muestreo y el bench espeja el equivocado:

| | `capture()` del bench | `tick()` (el lazo del DoD) |
|---|---|---|
| Lectura MPU | `read_raw()` → tupla | `read()` → **dict + 7 divisiones float, por muestra** |
| Pacing | deadline en **µs** | deadline en **ms** (`1000 // mpu_hz`) |
| SD | bloque binario de 4086 B | **línea CSV `%.4f`** + `flush()` cada 100 líneas |
| Alocación en el lazo | ninguna, `gc.collect()` antes | un dict por muestra |
| LoRa | `send()` cada 2 s, standby | `poll()`+`service()` cada vuelta, RX continuo, relay |

- **B2 — el bench lee por el camino barato.** `read()` aloca un dict por muestra:
  a 500 Hz son 1500 objetos/s. **La pausa de GC es *el* modo de falla clásico de
  MicroPython en muestreo determinista** — exactamente el riesgo que este
  benchmark existe para medir — y `capture()` lo elimina por construcción. El
  comentario del código lo dice sin querer: *"GC antes, no durante (medimos el
  caso limpio)"*. Lo que sale es una **cota inferior del jitter, no una
  predicción**.
- **B3 — el pacing.** En producción el periodo está **cuantizado a 1 ms**: el piso
  de jitter es ±1 ms = **50 % del periodo a 500 Hz**, contra el umbral de **5 %**
  de la tabla de decisión. Con el lazo actual, producción **no puede** pasar el
  criterio de jitter a 500 Hz, gane quien gane el benchmark.
- **B1 — la fase C mide otra carga de SD.** El README la llama *"la prueba que
  mata o salva a MicroPython"*. Distinto tamaño, distinta alineación, distinta
  frecuencia: `sd_worst_us` no predice el stall de producción, y el costo de CPU
  del formateo CSV (caro en MicroPython) no aparece en ninguna fase.

### El hallazgo que cambia la pregunta

- **B9 (warn, pero es el más caro) — `gaps = 0` no lo puede cumplir nadie con esta
  arquitectura.** `tick()` dispara `capture_and_send()` cada `fft_period_s`
  (default 15 s) cuando `fft_auto` está prendido: 256 muestras a 1 kHz con espera
  activa + un `send_burst()` por LoRa. **El comentario del propio `nodo.py` lo
  dice: "Bloquea ~1-3 s mientras captura+envía".** Durante ese tiempo el muestreo
  continuo y la SD están detenidos: son **gaps garantizados, periódicos y
  grandes**, y ninguna fase del benchmark los produce. `gaps = 0` es el binario
  del que cuelga todo el DoD — y **no es un problema de runtime**: es que un solo
  hilo hace las dos cosas. Migrar a C no lo arregla.

### Los demás

- **B4 (warn) — el resultado y el consumo son la misma perilla.** El bench fija
  150 MHz (perfil `max`); el default de `config.py` es `normal` = **125 MHz**
  (20 % más lento) y el trabajo de energía empuja a `low` = **48 MHz** (3,1×). La
  fila 6 de la tabla trata el consumo como *tie-breaker independiente*: **no lo
  es.** Un "MicroPython alcanza" es un veredicto válido **sólo a máximo reloj**, y
  la tabla no lo aclara.
- **B5 (warn)** — la fase D transmite pero nunca llama `start_rx()`; `tick()` hace
  `poll()`+`service()` cada vuelta sobre el mismo SPI0 que la SD. La contención
  medida es la más benigna posible.
- **B6 (warn)** — `for_sd()` (= `spi.init()`) por muestra en producción, ausente
  en la fase C.
- **B7 (warn)** — la otra mitad de B2: `gc.collect()` antes y cero alocación
  adentro.
- **B8 (warn)** — `227 × 18 = 4086 B` **no es múltiplo de 512** (502 B sobre 7
  sectores): cada bloque fuerza un read-modify-write del último sector, que es
  justo lo que `sd_worst_us` reporta. El README lo llama "~8 sectores".
- **B11 / B12 / P4 (info)** — el bench corre en ±2 g y `capture_burst()` en ±8 g ·
  la cuenta del FIFO del README usa muestras de 12 B pero el driver lee **14**
  (→ ~146 ms de colchón, no 170; volcando sólo el acelerómetro serían ~340 ms) ·
  las líneas `#RES,…,SKIP,…` tienen 4 campos donde el `#HDR` declara 17.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-08-fidelidad-benchmark
python tools/check_benchmark_fidelity.py               # -> 3 error / 6 warn / 3 info, exit 1
python tools/check_benchmark_fidelity.py --json
python tools/check_benchmark_fidelity.py --fail-on warn
python -m unittest tools.test_check_benchmark_fidelity # -> Ran 49 tests, OK
```

B9 se comprueba sin la herramienta, leyendo dos lugares de `nodo.py`: el
`capture_and_send()` de `tick()` con su comentario *"Bloquea ~1-3 s"*, y el
criterio `gaps = 0` de `benchmark/README.md`.

`TestRepoReal` **fija los 12 hallazgos**: si alguien arregla uno, el test falla y
obliga a actualizar `docs/benchmark-fidelity.md` en el mismo commit. También falla
si aparece `benchmark/resultados.md` — recordatorio de releer la auditoría antes
de creerle a los números.

**Verificado por mutación** (las 6 hacen fallar la suite): contar `%%` mal, contar
`for_sd` sobre el set de `calls()`, buscar los módulos fuera de la línea del
`fs cp`, ignorar el alias `pack=struct.pack_into`, sacar comentarios de C con
regex, y `literal_eval` sobre la tupla con `lambda` de `config.py`.

## Qué quedó sin verificar (banco — trabajo de día)

**Nada de esto se corrigió.** Los arreglos son decisiones de firmware con dueño
(@firmware + @muestreador), y una de ellas (B9) es de arquitectura.

La propuesta de `docs/benchmark-fidelity.md`, en orden:

1. **Correr el benchmark como está** (~2,5 min). Da el techo de la plataforma. **Si
   la fase C ya falla en el caso limpio, la decisión está tomada — C, sin más
   discusión, y la fidelidad ni importa.**
2. Si pasa, **agregar una fase `PROD`** en la misma sesión: `tick()` instrumentado
   (con `read()`, pacing en ms, CSV vía `SDLogger`, `poll()` por vuelta). **La
   diferencia entre C y PROD es el presupuesto que se está regalando en la
   implementación**, y es accionable con o sin migrar de runtime.
3. **Anotar `cpu_mhz` junto a cada fila** de resultados (B4). El `#CFG` ya lo
   imprime; falta que la tabla lo exija.
4. **Decidir aparte si `fft_auto` convive con el logging continuo** (B9). No
   depende del runtime y hoy está tomada por default sin haberse discutido.
5. De una línea cada uno: buffer de SD alineado a 4096 B (B8), prefijo `#SKIP,`
   (P4), corregir la cuenta del FIFO del README (B12).

Límites, escritos para no confundirlos:

- **La auditoría es estática.** Ningún número de jitter, consumo o stall sale de
  acá: leí el código, no observé el hardware.
- **No compilé el lado C ni bajé el Pico SDK** (regla de disciplina de tiempo). El
  comando para el día: `cmake -G Ninja -B build -DPICO_BOARD=pico2_w && ninja -C build`
  desde `benchmark/bench_c`, con el instalador oficial del Pico SDK ≥ 2.1.
  **Verificación pendiente: que `bench_c` compile.** Las fases C/D del lado C
  siguen siendo TODO documentado en `main.c` — eso ya lo decía el README y no es
  hallazgo nuevo.
- **Comparé contra `firmwares/pico2w-node/`.** Existe además
  `firmwares/pico2-lora-com10/` con otra copia de los drivers: **no la miré.** Si
  el nodo del banco es ése, hay que repetir el control de pinout.
- No corrí `npm run build`: no toqué `vercel-dashboard/`.

## Estado

- Branch `nocturno/local-2026-08-08-fidelidad-benchmark` pusheado (1 commit,
  `b82f551`: 4 archivos). datalogger volvió a `main` limpio.
- `QUE_FALTA.md` de datalogger: nota en el **bloqueante #1** (en el branch).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Quinta noche que lo reporto:** es un firmware que va a un equipo a 2000 km
  esta semana y vive **sólo en este disco**. **No lo toqué.**
- ℹ️ `C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main` (estado previo, no lo
  hice yo). **No lo cambié.**
- ℹ️ `C:\Proyectos\datalogger` tiene sin trackear `docs/CONEXIONES_LAB.html`
  (previo, no lo hice yo). **No lo toqué.**
- ⚠️ Queda el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando Matías quiera.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las diez
  noches anteriores: `agentes/{esquematico,pcb}.md`,
  `dominios/{comms,diseno,esquematico,firmware,hardware,logo_acceso_remoto,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md`,
  `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html`,
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- La cola de merge suma **47 branches** en origin (galgas 17, datalogger 15,
  frioseguro 14, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo y
  sin usar: falta la sesión humana.
  **Nota de prioridad:** de los 15 de datalogger, éste es el único que toca el
  **bloqueante #1**, y su valor **caduca**: sirve *antes* de la sesión de banco,
  no después. Si el banco se hace primero, se gasta la noche de hardware midiendo
  el lazo equivocado.
