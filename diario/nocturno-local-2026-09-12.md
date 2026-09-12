# Nocturno local — 2026-09-12

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (**octubre — parada de planta Dreyfus**),
zona `firmware/banco_consumo/` + `firmware/esp32_logger/` + `tools/` + `docs/`.
**Branch:** `nocturno/local-2026-09-12-el-banco-que-se-mide-a-si-mismo`
(pusheado, `a7d4ab5`).
**Sale de `origin/main` (`35a8200`) limpio**, sin ningún otro branch mergeado
adentro.
**Verificado contra los 37 branches abiertos de galgas: ninguno toca
`firmware/banco_consumo` ni `firmware/esp32_logger`.** El único roce es
`QUE_FALTA.md`, que tocan 33 de ellos — añadido contra añadido, se resuelve
quedándose con los dos lados. **No toca `data/field_captures/`** (sagrado), ni
SQL, ni el firmware del nodo de producción, ni `tools/banco_server.py`.

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_galgas_0912`)
porque el árbol de `galgas` tiene **52 archivos sucios** de Matías (KiCad del
módulo `alim`, los `.ino` del banco, binarios). **Verificado al terminar: el
árbol quedó idéntico** (mismo hash de `git status`, `a22a8947…`), en el branch
`09-05` donde estaba.

---

## TL;DR

> **El banco de consumo le cobraba al nodo su propia instrumentación.**
>
> `anunciar(n, ...)` imprimía `ESTADO n NOMBRE` —que es la línea que le **abre**
> la ventana de medición al ESP— y **después** parpadeaba el LED n veces, 200 ms
> por destello. Esos `n × 200 ms` de CPU despierta caían **adentro** de la
> ventana que el logger estaba promediando.
>
> El sesgo es **proporcional al número de estado**: 200 ms en DORMIDO, 1200 ms en
> TODO. Y como el anuncio cuesta siempre lo mismo (~2 mA), **empuja a todos los
> estados hacia ese valor**. La tabla de consumo salía **achatada**: error
> exactamente **0 % en ADC** (que consume lo mismo que el anuncio) y creciendo
> hacia los dos lados.
>
> **El segundo agujero está en el promedio**: era `suma / n`, la media
> aritmética. Esa media sólo vale con muestras equiespaciadas, y el `loop()` del
> ESP no lo está — entre dos lecturas del INA219 puede meterse la FIFO entera del
> RA-02 y un `printf` por USB. Durante LORA_TX el nodo manda ~170 paquetes en
> 8 s y el ESP los recibe e imprime **todos**: el estado donde la cifra más
> importa es donde el muestreo más se desparrama.
>
> **La integral ya estaba calculada y se tiraba.** El logger acumulaba `mA·s`
> para informar los mAh, y después sacaba la autonomía del aritmético. El número
> correcto estaba adentro del programa y no se usaba.

## Por qué esta tarea

1. **Es de lo que Matías está haciendo esta semana con las manos.** Los tres
   commits más nuevos de `main` son del banco (`4b5cd6b` medición de consumo,
   `35a247e` ADS1220, `35a8200` pinout del RA-02, todos del 09-09 al 09-11). El
   `esp32_logger` y el `banco_consumo` son **código de tres días, sin auditar**,
   y es el instrumento del que sale el número.
2. **De acá sale el presupuesto de energía de octubre** — el ítem #3 del
   `QUE_FALTA` («presupuesto de energía **medido**»), que decide si el nodo
   aguanta la parada sin que nadie suba al REDLER a cambiarle la pila.
3. **Es un error que no se ve.** No tira un valor absurdo: tira uno plausible, un
   poco más chico, **siempre del mismo lado**. Se anota, se compara contra la
   tabla teórica de `RETOMAR_BANCO.md`, cierra razonablemente bien, y queda.
4. **Estaba libre**: ninguno de los 37 branches abiertos toca la carpeta del
   banco (verificado con `git diff origin/main...<branch>`, no de memoria).
5. **Se hace entera sin hardware**: la estadística es pura y las dos
   compilaciones corren en esta máquina.
6. **Le tocaba a octubre por rotación**: los dos turnos del 09-11 fueron
   datalogger y frioseguro, y frioseguro se llevó 3 de los últimos 4.

## Las cifras del sesgo

Con el anuncio a ~2 mA (CPU a 4 MHz ≈ 1,7 mA + LED encendido el 30 % del tiempo)
y las corrientes esperadas de `RETOMAR_BANCO.md`:

| n | estado | real | ventana vieja | medía | error corriente | error autonomía |
|---|---|---|---|---|---|---|
| 1 | DORMIDO | 0,021 mA | 8200 ms | **0,069 mA** | ×3,3 | ÷3,3 |
| 2 | DESPIERTO | 1,7 mA | 8400 ms | 1,714 mA | +0,8 % | −0,8 % |
| 3 | ADC | 2,0 mA | 8600 ms | 2,000 mA | **0 %** | 0 % |
| 4 | LORA_RX | 12 mA | 8800 ms | **11,09 mA** | −7,6 % | +8,2 % |
| 5 | LORA_TX | 100 mA | 9000 ms | **89,11 mA** | −10,9 % | **+12,2 %** |
| 6 | TODO | 110 mA | 9200 ms | **95,91 mA** | −12,8 % | **+14,7 %** |

### El caso DORMIDO, que es el que decide la autonomía

`RETOMAR_BANCO.md` es honesto: dice que el INA219 con shunt de 0,1 Ω no resuelve
los ~21 µA del nodo dormido, y el logger tiene el guardarraíl puesto — si el
promedio no llega a **0,05 mA**, no da autonomía y manda a medir con téster.

**El anuncio solo aporta `200 ms × 2 mA / 8200 ms = 0,0488 mA`.** Cae **encima de
la línea**. O sea que si el guardarraíl protege o no lo decide el LED: un destello
de 70 ms en vez de 60 y el logger cruza el umbral e **imprime una autonomía del
estado que declara no poder medir** (~60 600 h ≈ 6,9 años: una cifra grande,
redonda y creíble, fabricada íntegramente por el LED de anuncio).

Un guardarraíl que depende de un artefacto del propio instrumento no es un
guardarraíl.

## El discriminador que ordenó el diseño

La pregunta no era *«¿cuánto cuesta el anuncio?»* sino **«¿de quién es este
tiempo?»**.

- **Bajar los destellos a 20 ms** achica el error y no lo resuelve: sigue siendo
  tiempo del anuncio contado como tiempo del estado, y vuelve con el próximo que
  le agregue una línea a `anunciar()`.
- **Mover los destellos antes del `ESTADO`** los manda adentro de la ventana del
  estado **anterior**, que todavía está abierta. El error se muda de borde.

La única forma de que el tiempo del anuncio no sea de nadie es que **la ventana
tenga los dos bordes explícitos**. Por eso hay una línea nueva, `FIN n`, y un
tramo `ENTRE` que se informa aparte — así el costo del anuncio **se ve** en vez
de deducirse.

Mismo patrón que otras noches: el estado se actualiza donde la cosa **realmente
ocurre**, no donde uno espera que ocurra.

## Qué se entregó

- **`firmware/esp32_logger/consumo_stats.h`** (nuevo) — la estadística del
  tramo, **pura** (sin Arduino/Wire/SPI) e **incluida** por el `.ino`: no es un
  espejo, lo que se testea es lo que se flashea. **Un solo promedio: integral /
  duración.** El aritmético queda de **testigo**.
- **`firmware/banco_consumo/banco_consumo.ino`** — destellos primero, anuncio
  después, `terminar(n)` manda `FIN n`. `esperarConLed()` → `esperar()` (no
  tocaba el LED, y el nombre decía que DESPIERTO se medía con el LED prendido,
  que es otra corriente).
- **`firmware/esp32_logger/esp32_logger.ino`** — ventana con dos bordes, tramo
  `ENTRE`, y el resumen que declara **cómo se cerró la ventana**.
- **`tools/test_consumo_stats.cpp`** y **`tools/mutantes_consumo_stats.py`**.
- **`docs/banco-consumo-sesgo.md`** y el sub-ítem del #3 en el `QUE_FALTA` de
  galgas.

### Lo que el resumen ahora dice y antes no

- `ventana cerrada por: ...` — un nodo viejo sin `FIN` **sigue funcionando**, y
  el resumen declara que esa ventana incluye el anuncio.
- `OJO: muestreo desparejo` si el aritmético se aparta más de 2 % del ponderado:
  **el instrumento avisa cuando su propio muestreo no da para afirmar la cifra.**
- `FIN_DESPAREJO` si llega un `FIN` de otro estado — a 9600 baudios contra una
  UART por polling se puede perder una línea, y una ventana con un borde perdido
  no es una medición.
- `corriente NEGATIVA: el INA219 esta al reves`. Antes eso caía en la misma rama
  que «por debajo de lo que el INA219 resuelve», así que el operador leía un
  mensaje que lo mandaba a buscar un téster en vez de a dar vuelta dos cables.

## Un bug que encontró el test, no yo

La integral no cubría la ventana entera: el tramo entre la apertura y la primera
muestra se contaba en la **duración** pero no en la **integral**, o sea como si
el nodo no consumiera nada hasta que lo miramos. Con muestreo a 1 kHz sobre 8 s
son −0,0125 %, nada — pero es un sesgo de un signo solo, y es exactamente lo que
este header existe para no tener. La primera muestra ahora se sostiene hacia
atrás hasta la apertura, y la última hacia adelante hasta el cierre.

## Los mutantes también hicieron su trabajo

En la primera corrida **sobrevivieron dos de catorce**:

- **Real**: el parser aceptaba `FIN3` pegado. Yo había probado `FINAL 3`, que
  **no discrimina** (falla igual por otra razón). Se cerró con dos checks nuevos.
- **Equivalente**: castear la resta de `millis()` a `int32_t` da los mismos bits
  en complemento a dos. Lo reemplacé por el que sí es un bug de verdad: el
  `if (ahora > antes)` que parece prudente y devuelve cero justo cuando
  `millis()` da la vuelta.

Lo anoto porque es la parte que importa del método: **una suite que pasa no dice
nada si no hay nada que pueda hacerla fallar.**

## Cómo verificarlo (comandos exactos, sin hardware, ~1 minuto)

```bash
cd C:\Proyectos\galgas
git fetch origin
git checkout nocturno/local-2026-09-12-el-banco-que-se-mide-a-si-mismo

g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_consumo_stats.exe tools/test_consumo_stats.cpp
./tools/test_consumo_stats.exe

python tools/mutantes_consumo_stats.py
```

**Resultados obtenidos esta noche:**

- **93 checks, 0 fallos, sin warnings.** Los bloques **2 y 3 son REGRESIÓN**:
  fallan contra la lógica vieja (promedio aritmético, ventana con el anuncio
  adentro). El bloque 10 recorre la vuelta completa de los 6 estados como la va
  a ver el ESP.
- **15/15 mutantes muertos.** El mutante 1 reimplanta el bug original
  (`promedio = suma / n`).
- Las **dos compilaciones reales**, las dos en exit 0 y sin warnings:
  - `arduino-cli compile --clean --fqbn arduino:avr:pro:cpu=8MHzatmega328 --build-property build.f_cpu=4000000L firmware/banco_consumo`
    → **5864 B flash (19 %), 263 B RAM (12 %)**. Contra `origin/main`: **+248 B
    flash, 0 B RAM** (medido compilando el original aparte, no estimado).
  - `arduino-cli compile --fqbn "esp32:esp32:esp32s3:USBMode=hwcdc,CDCOnBoot=cdc,FlashSize=16M,PSRAM=opi" firmware/esp32_logger`
    → **355 382 B (27 %), 24 188 B RAM (7 %)**.

⚠ **`--clean` en el AVR no es opcional** (la trampa del core cacheado con el
`F_CPU` equivocado, ya pagada).

## Compatibilidad

- **El CSV sigue teniendo 5 columnas**, que es lo que exige `tools/banco_server.py`
  (`if len(parts) != 5: return`). Lo que cambió es que la **4ª ahora es el
  promedio ponderado**. La interfaz web no se toca y no hay que tocarla.
- **Un nodo viejo sigue funcionando**: si nunca manda `FIN`, el tramo se cierra
  con el `ESTADO` siguiente igual que antes — pero el resumen lo declara.
- **Orden de flasheo: indistinto.** Las dos mitades degradan solas.

## Qué quedó SIN verificar (pide el banco)

1. **La corriente real del anuncio.** Los 2 mA de la tabla son hoja de datos
   (1,7 mA a 4 MHz / 3 V) más un LED estimado. **El banco nuevo la mide solo** —
   la línea `# entre estados: X s a Y mA prom`. Es el primer número a mirar, y
   con él se recalcula la tabla con datos en vez de cuentas. [@energia]
2. **Que los dos promedios se aparten en LORA_TX.** El aviso de `muestreo
   desparejo` es **la predicción principal de este branch** y sólo se confirma
   con el RA-02 transmitiendo de verdad contra el ESP recibiendo e imprimiendo.
   Si **no** salta, el muestreo del ESP es más parejo de lo que supuse y hay que
   anotarlo. [@energia + @muestreador]
3. **Que la ventana medida dé 8,0 s** y el tramo `ENTRE` dé `n × 200 ms`: es la
   comprobación de que el `FIN` llega y de que los bordes quedaron donde se
   quiso. [@energia]
4. **Los `.hex` de `firmware/bins_nodo/banco_consumo/` quedaron viejos** — son
   del firmware con el sesgo. **Regrabar el ATmega desde el fuente, no desde ese
   `.hex`.** No los regeneré: los binarios de ese directorio los viene firmando
   Matías con cada etapa del banco. [@firmware]

## Lo que NO hice, a propósito

- **No toqué `tools/banco_server.py`.** Es la interfaz web y no está trackeada
  (ver abajo). Cambiar el formato del CSV habría sido meterse con código sin
  firmar de Matías; por eso el CSV **mantiene sus 5 columnas** y la corrección
  entra por el contenido de la columna, no por su cantidad.
- **No cambié `PILA_MAH = 4200`.** El número sale de `ENERGIA_REV_D` («2 ×
  ER14505 derateadas a 2100 mAh c/u») y decidir si esa cifra es correcta es de
  @energia, no de esta noche.
- **No toqué `power_all_enable()` en `dormir8s()`.** Cambia **qué** mide el
  banco, y eso es una decisión de medición (ver deuda).
- **No regeneré los binarios** de `bins_nodo/`.
- **No arreglé la numeración duplicada del `QUE_FALTA`** (los dos ítems «3»):
  es drift ya anotado por el branch `09-05` y tocarlo garantiza un conflicto.

## Deuda anotada, NO tocada

- **`dormir8s()` cierra con `power_all_enable()`**, así que del estado 2 en
  adelante el ATmega corre con TWI, timer1, timer2 y su ADC interno **con reloj**
  — mientras el docstring del estado DESPIERTO dice «periféricos apagados».
  Decidir qué tiene que estar prendido para que DESPIERTO **represente al nodo
  real** es una decisión de medición, y mueve la referencia contra la que se
  comparan los otros cinco estados. [@energia]
- **`PILA_MAH = 4200` está escrito a mano en tres lugares** (el logger,
  `ENERGIA_REV_D`, `RETOMAR_BANCO.md`) y el logger no puede saber si los otros
  dos cambiaron. Regla de la casa: un dato duplicado a mano se desincroniza y
  nadie se entera. [@energia + @cronista]
- **⚠️ `tools/banco_server.py` NO ESTÁ EN GIT.** Existe **sin trackear** en el
  árbol de Matías (20 110 bytes) y `RETOMAR_BANCO.md` —que **sí** está
  commiteado— le dice al operador que lo corra. Es la interfaz web del banco y
  hoy **vive en un solo disco**. **No lo commiteé porque es trabajo sin firmar de
  Matías.** [MATÍAS]
- **El ESP imprime una línea por cada trama LoRa recibida** (~170 en 8 s durante
  LORA_TX), y es parte de por qué el muestreo se desparrama. Silenciarlas haría
  el muestreo más parejo pero taparía la única señal de que el enlace anda; con
  el aviso de `muestreo desparejo` puesto, la decisión se puede tomar con el dato
  a la vista. [@energia + @comms]
- **`RETOMAR_BANCO.md` va a quedar desactualizado al mergear**: describe el
  protocolo de una sola línea (`ESTADO n NOMBRE`) y la salida vieja del logger.
  No lo toqué para no mezclar el diff; se actualiza al mergear. [@cronista]

## Anotado y NO tocado

- **37 branches abiertos en galgas**, ninguno mergeado; éste es el 38.º. **Sigue
  siendo la deuda más grande del repo: el trabajo está hecho y no está en
  `main`**, y quedan **siete semanas** para la parada. [@verificador → MATÍAS]
- **`consumo_stats.h` es candidato a la biblioteca**: un acumulador de integral
  con ventana de bordes explícitos sirve para cualquier medición etiquetada por
  estado. **No lo coseché porque no se probó contra el banco real.**
  [@bibliotecario]
- En MATI-HQ quedaron **sin commitear, tal como los encontré**,
  `comercial/panamerican/PRESUPUESTO_CERRO_MORO_INTERNO.html`,
  `dominios/{backend,comercial,diseno,frontend,pcb}.md` y
  `scripts/turno_noche_log.txt`. **Tercera noche que se anota.**

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-12-el-banco-que-se-mide-a-si-mismo`
  (`a7d4ab5`), sobre `origin/main` (`35a8200`) limpio.
- `QUE_FALTA.md` de galgas actualizado (sub-ítem del **#3**, «Test con LiPo
  REAL»). Detalle técnico en `docs/banco-consumo-sesgo.md`.
- Worktree `C:\Proyectos\_noche_galgas_0912` eliminado; el árbol de `galgas`
  quedó **idéntico** (los 52 archivos sucios de Matías intactos, en el branch
  `09-05`).
- Nada corriendo, nada abierto.
