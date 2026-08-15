# Nocturno local — 2026-08-15

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "terminarlo primero, antes del
trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-15-cadena-recuperacion` (pusheado, `b0d2477`).

## TL;DR

El datalogger existe para producir **un archivo**. Todo el repo —el muestreo, la
SD desacoplada en el core 1, las misiones, el frame LoRa— converge en un CSV en
`/sd/logs`. Nadie había recorrido nunca el tramo que arranca **cuando el nodo se
apaga**: el operario vuelve con la SD y hay que llegar a un informe.

**De los 8 eslabones: 0 ejecutables, 3 con fricción, 5 ROTOS.** Y los cinco rotos
comparten una sola causa: **el archivo no se autodescribe.** Todo lo que hace
falta para interpretarlo —qué nodo, qué momento, qué misión, qué tasa, qué
unidades, cuánto se perdió— vive en el nodo. Y el nodo se apaga.

Tres números, sacados del propio código:

- **El CSV de campaña no lo lee la única herramienta de análisis del repo.** El
  nodo escribe `t_ms,seq,ax,…`; `import_sd_csv` conoce dos formatos y ese no es
  ninguno, así que cae a la rama del sniffer y toma la columna 0 —**milisegundos**—
  como **segundos**. Una vibración de 66 Hz sale por **0,066 Hz**. El único
  consumidor que lo lee bien es el `/plot` que corre **en la placa**.
- **El nombre del archivo es el uptime, y se abre en modo `"w"`.**
  `mpu_<segundos desde el arranque>.csv`. Dos arranques que abran su primer
  archivo en el mismo segundo producen **exactamente los mismos nombres**, y el
  segundo **trunca** al primero. Es todo o nada: la rotación se cuenta desde la
  apertura, así que si coincide el primero coinciden todos.
- **No hay reloj en todo el firmware del nodo.** Ni `ntptime` ni `machine.RTC`.
  Ningún CSV dice en qué día se tomó.

## Tarea elegida y por qué

Por rotación tocaba datalogger (los cuatro turnos previos: datalogger 08-13,
galgas 08-13-b, cosechador 08-14, frioseguro 08-14-b — el más viejo era éste).

Los 🔴 del `QUE_FALTA` sin branch siguen siendo banco o hardware (#1 necesita
flashear, #2 es el front-end del piezo, #3 y #4 necesitan medir). Y los 17
branches previos cubren, todos, **el nodo andando o llegando a andar**:

| noche | qué audita | dónde empieza y termina |
|---|---|---|
| 08-03 `registro-sd` | contabilidad de lo que se graba | nodo corriendo |
| 08-04-b `contrato-rv1` | forma del frame LoRa | nodo corriendo |
| 08-06-b `contrato-nube` | forma de lo que llega a la nube | nodo corriendo |
| 08-08 `fidelidad-benchmark` | si el benchmark mide lo que dice | nodo corriendo |
| 08-10 `cadena-vibracion` | qué **significan** los números | nodo corriendo |
| 08-13 `cadena-puesta-en-marcha` | cómo el nodo **llegó** a ese estado | antes de andar |

**Ninguna mira el tramo de después.** La pregunta que elegí:

> la campaña terminó. **¿los datos llegan a un informe, y se sabe de qué nodo y
> de cuándo son?**

Tres razones para elegirla sobre cualquier otra cosa esta noche:

1. **Es el otro extremo del 08-10.** Esa noche auditó si el número de Hz que sale
   **en pantalla** es la frecuencia de la máquina. Ésta audita el camino
   **offline** —el que el repo llama "la fuente de verdad"— y ahí el error es de
   1000×, no de matices de ventana.
2. **Es lo que se va a vender.** El 🟢 #13 del `QUE_FALTA` es *"estudio de
   vibraciones con informe"*, y en octubre hay que entregarle algo a Dreyfus. El
   entregable no es la SD: es el informe.
3. **El fix más importante no toca el lazo de muestreo.** D2+D3 son el nombre del
   archivo y una línea de cabecera. Se pueden cerrar de día, sin banco, sin
   hardware, sin tocar el código que el 08-03 y el 08-13 auditaron.

## Qué hice

**`tools/check_retrieval_chain.py`** (stdlib, solo lectura, sin red ni hardware,
no compila nada). **No inventa números: los LEE** de `firmwares/pico2w-node/`,
`pc-sniffer/analysis.py` y los docs, y cita `archivo:línea` de cada afirmación.
Exit 0/1/2/3, `--json`, `--detail`, `--fail-on`, `--root`.

**Cuatro oráculos** que demuestran los hallazgos en vez de afirmarlos:

- `--demo-recuperacion` recorre los **8 eslabones** como quien vuelve del campo
  con la SD y marca cada uno *ejecutable / fricción / ROTO*. Resultado:
  **0 / 3 / 5**, primer eslabón roto: el **1**.
- `--demo-nombres` simula dos arranques con rotación horaria y muestra **qué
  archivo pisa a cuál**, en los dos escenarios: mismo segundo de arranque (9 de 9
  truncados) y un segundo de diferencia (0 colisiones, 18 archivos mezclados sin
  nada que diga de qué campaña es cada uno).
- `--demo-analisis` fabrica un CSV con el **encabezado real** del nodo y una
  senoidal conocida, lo pasa por una réplica en stdlib de la lógica de despacho
  de `import_sd_csv` y hace la DFT en Python puro: **0,0660 Hz para una señal de
  66 Hz**.
- `--demo-bajada --horas 8` mide la línea CSV con el **format string real** (72 B)
  y cuantifica los tres canales: 690 MB, 7.192.800 frames de LoRa.

**`tools/test_check_retrieval_chain.py` — 126 tests en 7 capas:** utilidades de
texto, extractores sobre fuentes sintéticas, los cuatro oráculos con números
fijados, **control negativo** (un repo sintético sano no enciende nada), un
defecto inyectado por vez que enciende **exactamente** su código, la capa "no
salta cuando no corresponde", y regresión sobre el repo real + CLI.

**`docs/retrieval-chain.md`** — el análisis completo y el orden de arreglo.

### Lo que hubo que resolver

- **Un checker que hardcodea las dos mitades de una contradicción no sirve.**
  Casi todo hallazgo acá es un **desencuentro** entre dos archivos (el encabezado
  que escribe el nodo contra el formato que espera el laboratorio, el docstring
  contra el encabezado). Por eso **parsea los dos lados**: corregido cualquiera de
  ellos, el hallazgo se apaga solo. Hay test de eso para los diez.
- **La prueba de mutación encontró un bug real en mi propio extractor.**
  `maybe_start_net(nodo)` aparece **dos veces** en `main.py`: en la definición y
  en la llamada. Buscar el texto suelto contaba la `def` como si fuera el arranque
  de los servidores, así que D7 seguía encendido después de sacar la llamada. Lo
  cazó el test "no salta cuando no corresponde", no el hallazgo. Ahora la busca
  anclada a principio de línea, y la mutación que revierte el fix falla.
- **El veredicto de la cadena no podía ser mío.** Mi primera versión marcaba
  **ROTO** cualquier eslabón golpeado por cualquier hallazgo, y daba 7 de 8 rotos
  —incluyendo eslabones que rompía un `info`—. Un detector de incendios que marca
  todo rojo no informa nada. Ahora **ROTO sale de la severidad**: sólo un `error`
  rompe; `warn`/`info` dejan **fricción**. El resultado (5 rotos) es más chico y
  se puede defender línea por línea.
- **D6 no podía exigir que exista la implementación buena.** Mi primera condición
  pedía una mala **y** una buena para hacer el contraste — o sea que si alguien
  "arreglaba" `web.py` rompiéndolo, el hallazgo **desaparecía**. Ahora dispara con
  la mala sola y el contraste es texto opcional. Hay test.
- **El caso peor de D2 es un supuesto, y hay que decirlo.** Que los dos arranques
  abran su primer archivo en el **mismo segundo** de uptime no está garantizado.
  Por eso el demo muestra los dos escenarios: el que trunca y el que no. El que
  no trunca tampoco sirve — deja las dos campañas mezcladas.
- **La réplica de `import_sd_csv` tenía que ser fiel, no prolija.** Mi primera
  versión dividía la columna por 1000 "para que diera bien". El original **no hace
  eso**: hace `idx.get("host_t", 0)` y usa la columna cruda. La mutación que
  reintroduce el arreglo prolijo mata dos tests.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **5 error · 3 warn · 2 info.**

| código | sev | dueño | qué |
|---|---|---|---|
| **D1** | error | @muestreador | **El laboratorio no entiende el formato de campaña.** `nodo.py:171` escribe `t_ms,seq,ax,ay,az,gx,gy,gz,tempC,vbat`; `analysis.py:41` decide "formato crudo" por `"t_us" in header` y `analysis.py:66` cae a `idx.get("host_t", 0)`: usa la columna 0 **en ms** como si fueran **segundos**. fs, duración y **toda frecuencia** salen /1000, y `vb` (la columna se llama `vbat`) vuelve en ceros. |
| **D2** | error | @firmware | **El nombre no identifica ni el nodo ni la campaña, y `open(..., "w")` trunca.** `nodo.py:167` + `_ts()` (`nodo.py:157`) = segundos desde el arranque, sin `node_id`. Los tres nodos producen los mismos nombres; dos arranques del mismo nodo se pisan. Y **el selector termina en reset**: dos arranques es el caso normal, no el raro. |
| **D3** | error | @firmware | **No hay reloj.** Ni `ntptime` ni `machine.RTC` en todo `firmwares/pico2w-node/`. Ningún CSV dice en qué día ni a qué hora se tomó. Y `ticks_ms` envuelve a los 2³⁰ ms = **12,4 días**: en una campaña larga el eje de tiempo **retrocede**. |
| **D4** | error | @cronista | **El encabezado promete metadatos que no escribe.** `mision_media.py:18` declara *"se anota la fs exacta en el encabezado del CSV para el análisis posterior"*; el encabezado es fijo y no trae fs, ni node_id, ni misión, ni unidades. |
| **D5** | error | @muestreador | **Dreyfus reusa las columnas.** `mision_dreyfus.py:157` manda `senal, v, 0.0` en las posiciones de `ax, ay, az` — el comentario lo dice: *"reuso write_sample"*. Mismo encabezado, mismo patrón de nombre, otra magnitud. El `/plot` del nodo lo rotula **"Aceleración (g)"**. |
| **D6** | warn | @backend | **La descarga por HTTP puede truncar sin que se note.** `sd_server.py:81` sirve el CSV **sin `Content-Length`**, con `cl.send(chunk)` crudo (sin reintentar escrituras parciales) y con `except Exception: pass`. En HTTP/1.0 sin `Content-Length`, cerrar la conexión **es** el fin del archivo. **El mismo repo lo hace bien en `web.py:457`.** |
| **D7** | warn | @firmware | **El nodo que graba no tiene servidor de descarga.** `main.py:25`: la misión toma el control y corta `main` **antes** de `maybe_start_net`. Durante la campaña el único canal es LoRa SDGET de a **96 B** (y sólo en la misión `media`). Para usar HTTP hay que sacar el nodo de la misión: un reset, o sea otro arranque (**D2**). |
| **D8** | warn | @firmware | **`cerrar()` sólo se llama desde la rama del botón** (2 de 2 call sites). Es lo único que drena la cola en RAM (hasta 600 líneas) y hace `flush`. Una campaña que termina **como terminan las campañas** —se acaba la batería, se desenchufa— deja en RAM lo último que midió. |
| **D9** | info | @muestreador | **El archivo no dice cuánto falta.** `gaps` (las tres misiones) y `descartes` (`registro.py:58`) se cuentan y viajan por LoRa y por el print de la serie; el CSV no tiene columna ni línea de cierre. Es el otro lado del H1 del 08-03: ahí la pérdida era invisible **en vivo**; acá es invisible **después**. |
| **D10** | info | @frontend | **El orden de los archivos no es cronológico.** `nodo.py:242` y `sd_server.py:65` ordenan por **nombre** en `reverse=True` y lo presentan como "el más reciente primero"; el nombre es el uptime. Un archivo viejo de 9 h aparece antes que uno nuevo de 2 minutos. |

**Orden sugerido:**

1. **D2 + D3 — el nombre y el sello de tiempo. Es la pieza más barata de la
   cadena y la que más cambia.** Un contador de campaña en `config.json` (que
   **ya sobrevive resets**) más el `node_id` en el nombre saca a D2, a D10 y a
   media D1. *Sin esto no se puede verificar nada en el campo: no hay forma de
   decir "este archivo".*
2. **D4 + D9 + D5, un solo commit: una línea `#` de cabecera** con `node_id`,
   `mision`, `fs`, unidades y contadores. Los tres se arreglan en el mismo lugar,
   y **`import_sd_csv` ya sabe leer líneas `#`** (de ahí saca `accel_LSB_per_g`).
3. **D1** — enseñarle el formato al laboratorio, o escribir `t_us`. Cualquiera de
   las dos, pero **decidirlo**.
4. **D8** — llamar `cerrar()` también en el camino de batería baja.
5. **D6** — `Content-Length` + bucle de `send`: está copiado al lado, en `web.py`.
6. **D7** — decisión de producto (RAM y SPI), no bug.

## Lo que está BIEN (fijado por test, para no ir a revisarlo)

- **`web.py:_send_file` sirve archivos correctamente** (`Content-Length` + bucle
  sobre el retorno de `send`): la implementación buena de D6 ya está escrita.
- **El `/plot` que corre en la placa interpreta bien la columna de tiempo**
  (`t_ms/1000`). El único consumidor sano de la cadena.
- **`import_sd_csv` sabe leer metadatos en líneas `#`**: el mecanismo del arreglo
  de D4 existe.
- **`config.json` sobrevive resets**: el contador de campaña de D2 tiene dónde
  vivir.
- **`RegistroSD.cerrar()` está bien hecho** (drena con timeout y hace flush). D8
  es un call site que falta, no una función por escribir.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-15-cadena-recuperacion

python tools/check_retrieval_chain.py                       # informe; exit 3
python tools/check_retrieval_chain.py --detail              # + evidencia archivo:linea
python tools/check_retrieval_chain.py --demo-recuperacion   # los 8 eslabones
python tools/check_retrieval_chain.py --demo-nombres        # que archivo pisa a cual
python tools/check_retrieval_chain.py --demo-analisis       # que lee el laboratorio
python tools/check_retrieval_chain.py --demo-bajada --horas 8
python tools/check_retrieval_chain.py --json

python -m unittest tools.test_check_retrieval_chain         # -> Ran 126 tests, OK
python -m unittest tools.test_misiones                      # -> 20 OK (regresion intacta)
```

Cuatro hallazgos se comprueban **sin la herramienta**:

```bash
grep -n "self.f.write" firmwares/pico2w-node/nodo.py                    # D1: el encabezado
grep -n "t_us\|host_t" pc-sniffer/analysis.py                           # D1: lo que espera el lab
grep -n "self.path\|_ts\|open(self.path" firmwares/pico2w-node/nodo.py  # D2
grep -rn "ntptime\|machine.RTC" firmwares/pico2w-node/                  # D3: cero hits
grep -n "Content-Length" firmwares/pico2w-node/sd_server.py firmwares/pico2w-node/web.py  # D6
```

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **126 tests en verde** (4,5 s). Sin descargas ni toolchains: cero riesgo de
  timeout.
- **`test_misiones` sigue en 20/20**: no toqué una línea de firmware.
- **Control negativo real:** un repo sintético sano no enciende **nada** (exit 0,
  los 8 eslabones ejecutables), y cada defecto inyectado por separado enciende
  **uno y sólo un** código. Los diez tienen además su test "no salta cuando no
  corresponde".
- **Verificado por mutación — 15 mutaciones, las 15 hacen fallar la suite:**
  la cadena ignorando la severidad · D2 sin exigir el modo `"w"` · D3 sin mirar
  si hay reloj · `strip_line_comments` ciego a los strings · `blank_docstrings`
  perdiendo la numeración · `func_body` cortando con `<` en vez de `<=` ·
  contando la `def` como llamada · D8 sin exigir que **todos** los call sites
  sean del botón · la réplica del laboratorio "arreglando" la división por 1000 ·
  exit code con la severidad menos grave · el match laxo del nombre de columna en
  dreyfus · bytes por línea estimados en vez de medidos · el demo de nombres
  ignorando el segundo de arranque de cada boot · `extraer_reloj` sin excluir
  `__pycache__` · D9 sin mirar si la columna existe.
  *(El andamio de mutación fue descartable, fuera del repo, en el temp: **no se
  commiteó**. Borré el `__pycache__` antes de cada corrida y restauré el archivo
  al final; `git status` quedó igual que antes, y hay un test que lo verifica.)*
- **No se tocó firmware, ni el dashboard, ni el script de flasheo, ni
  `pc-sniffer/`.** El branch agrega 3 archivos y edita `QUE_FALTA.md`.

## Qué quedó sin verificar

- **Todo sale de leer el repo, no de recuperar una campaña.** No hay SD con datos
  ni nodo flasheado al que preguntarle de noche.
- **D3 y D6 tienen premisas fuera del repo**: el ancho de `ticks_ms` en
  MicroPython (30 bits → 12,4 días) y el comportamiento de `socket.send` con
  envíos parciales. Las dos se confirman con la placa en la mano; **D6 no depende
  de la segunda**: la falta de `Content-Length` es un hecho del código.
- **D2 en su peor caso supone que los dos arranques abren su primer archivo en el
  mismo segundo de uptime.** El demo muestra también el caso benigno — y el
  benigno tampoco sirve: deja dos campañas mezcladas sin nada que las distinga.
  **La verificación de mayor valor de la noche es barata:** poner la SD de un
  nodo que ya midió en la PC y mirar los nombres de `/sd/logs`. Un minuto.
- **Las tasas de HTTP y LoRa del `--demo-bajada` son supuestos explícitos**, no
  están medidos en el repo. El volumen (690 MB) y la cuenta de frames sí salen
  del format string real.
- **No se probó qué hace `import_sd_csv` de verdad** (necesita numpy, y la réplica
  es mía): lo que está verificado es que **reproduce la lógica de despacho** que
  el archivo tiene escrita.
- **Ningún fix aplicado** — generator ≠ evaluator. Ni siquiera D6, que es copiar
  seis líneas de `web.py`: el que toca el servidor tiene que poder probarlo.

## Estado

- Branch `nocturno/local-2026-08-15-cadena-recuperacion` pusheado (`b0d2477`),
  sale de `main` (`e611bc5`). **datalogger volvió a `main` limpio.**
- `QUE_FALTA.md` de datalogger: ítem **#10c** nuevo, **dentro del branch**.
  Lo numeré así a propósito: el branch del 08-10 agrega un `#15` y el del 08-13
  un `#10b`, así que los tres se mergean en cualquier orden sin pelearse el
  número (sí va a haber conflicto trivial de contexto: los tres tocan la misma
  zona).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día SIN COMMITEAR**
  (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`, los dos tests del nodo GIMAP,
  `docs/ARMADO_NODO_GIMAP.html`, `.gitignore`). **No lo toqué.**
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Decimosexta noche que lo reporto**: es firmware que va a un equipo a 2000 km
  y vive **sólo en este disco**. **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  veintiún noches anteriores: `agentes/`, `dominios/`, `enlace/`, más
  `agentes/diseno3d.md`, `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html` y
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío (sólo el `.gitkeep`). El único
  `enlace\maquinas\*.estado.json` (DESKTOP-RK8DH7C) sigue con `ultima_vez_viva`
  del **2026-08-07**: el latido está parado hace **8 días**. **No lo toqué** (los
  scripts de ENLACE son trabajo de día sin commitear).
- La cola de merge suma **59 branches** en origin (galgas 20, datalogger **18**,
  frioseguro 18, cosechador 3).

## Para @muestreador / @firmware / @backend / @frontend / @cronista / @verificador

- **@muestreador: D1 es tuyo y es la noche entera.** El repo llama a la SD "la
  fuente de verdad" y hoy la fuente de verdad, leída por la herramienta del
  laboratorio, da frecuencias **1000× más chicas**. Es el complemento exacto del
  `cadena-vibracion` del 08-10: ahí auditaste el camino en vivo, éste es el
  offline. Y **D9 + D5 se arreglan en la misma línea de cabecera que D4**.
- **@firmware: D2 y D3 son tuyos y son la pieza más barata de toda la cadena.**
  El contador de campaña va en `config.json`, que ya sobrevive resets; el
  `node_id` ya está ahí. No toca el lazo de muestreo ni la cola del core 1: no
  hay riesgo de reabrir lo que el 08-03 auditó. Después **D8** (un call site) y
  **D7** (decisión, no bug).
- **@backend: D6.** Seis líneas, y la versión correcta está en el mismo repo, en
  `web.py:457`. Hoy un CSV que se corta a la mitad **se ve completo**.
- **@frontend: D10.** El día que el nombre lleve fecha (D2), el orden se arregla
  solo; hasta entonces la lista miente en las dos pantallas que la muestran.
- **@cronista:** `mision_media.py` promete en su docstring una fs en el
  encabezado que no existe (D4), y `PROGRESS.md:68` da por pendiente el botón de
  "bajar" — que es exactamente D7. Conviene reescribir los dos **junto con** el
  fix de la cabecera, no antes.
- **@verificador:** el DoD es *"cada eslabón de la recuperación tiene un hecho del
  repo que lo confirma o lo desmiente"*. Los 126 tests son el oráculo y
  `TestRepoReal` fija los 10 hallazgos. **Puntos a atacar, en orden:**
  1. **D2 es el más fácil de confirmar o tumbar y el más valioso**: poné la SD de
     un nodo que ya midió en la PC y mirá los nombres. Si hay dos campañas ahí,
     ya está el veredicto.
  2. **D1 es el más sólido** (es una comparación de encabezados) pero **la
     réplica de `import_sd_csv` es mía**: corrélo contra el original con numpy y
     un CSV real antes de darlo por cerrado.
  3. **D3 se apoya en el ancho de `ticks_ms`** (30 bits). Si esa premisa cayera,
     el wrap se cae — **el resto de D3 no** (que no haya reloj es un `grep`).
  4. **D6 tiene dos mitades**: la falta de `Content-Length` es un hecho; lo del
     `send` parcial es un riesgo del runtime.
  5. **D7 y D10 son los más discutibles** y están en warn/info por eso: uno es
     una decisión de diseño defendible, el otro sale gratis cuando se arregla D2.
