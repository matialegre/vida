# Nocturno local — 2026-08-13

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "terminarlo primero, antes del
trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-13-cadena-puesta-en-marcha` (pusheado, `0399124`).

## TL;DR

El paso 1 del procedimiento de campo —**"mantené BOOTSEL apretado mientras lo
enchufás"**— es, literalmente, el gesto que pone la placa en el **bootloader
UF2**: aparece como disco `RP2350`, MicroPython no corre, el LED no titila, no
hay AP y no se mide nada. El propio repo lo documenta así en otras cuatro
páginas… porque ahí es el procedimiento de **flasheo**.

De los 7 pasos de la puesta en marcha, **4 están bloqueados, 1 tiene fricción y
2 son ejecutables**, y el primer freno está en el PASO 1. El segundo más filoso:
elegir **LAB** en cualquiera de los tres nodos flasheados termina, 20 s después,
en el **nodo clásico** — y la única pantalla que el operario puede mirar sigue
diciendo **"Misión actual: LAB"**.

## Tarea elegida y por qué

Por rotación tocaba datalogger (los tres turnos previos fueron galgas,
cosechador y frioseguro; la última noche de datalogger fue el 08-10).

Los 🔴 del `QUE_FALTA` sin branch siguen siendo banco o hardware. Y los 16
branches previos de este repo auditan, todos, **el nodo ya andando**:

| noche | qué audita | dónde empieza |
|---|---|---|
| 08-03 `registro-sd` | contabilidad de lo que se graba | nodo corriendo |
| 08-04-b `contrato-rv1` | forma del frame LoRa | nodo corriendo |
| 08-06-b `contrato-nube` | forma de lo que llega a la nube | nodo corriendo |
| 08-08 `fidelidad-benchmark` | si el benchmark mide lo que dice | nodo corriendo |
| 08-10 `cadena-vibracion` | qué **significan** los números | nodo corriendo |

**Nadie audita cómo el nodo llegó a ese estado.** Y ese tramo es, además, el
código **más nuevo del repo**: el selector sin cable, el WiFi manager en runtime
y el fix de `flash_node.ps1` son de la última semana (`bb92a8a`, `513c79b`,
`3d2cbc5`, `e611bc5`). `tools/test_misiones.py` los cubre desde el lado de la
señal; nadie los miró desde el lado del que instala. La pregunta que elegí:

> el operario llega al punto con el nodo y el celular, aprieta BOOTSEL, elige
> una misión y se va. **¿el nodo queda midiendo lo que eligió?**

Elegí este ítem sobre cualquier otro por dos razones: **el hallazgo C1 vale
antes de la próxima salida a campo, no después**, y **C8 toca el bloqueante #1**
(si el botón se lee una vez por muestra, el benchmark de runtime mide el jitter
del botón junto con el de MicroPython).

## Qué hice

**`tools/check_commissioning_chain.py`** (stdlib, solo lectura, sin red ni
hardware, no compila nada). Cruza `misiones/selector.py`, `main.py`, el SCHEMA de
`config.py`, los **tres `config.P*.json` que están flasheados**, `flash_node.ps1`,
las cuatro misiones y los documentos que le dicen al operario qué hacer. Exit
0/1/2/3, `--json`, `--detail`, `--fail-on`, `--root`.

**Dos oráculos** que demuestran los hallazgos en vez de afirmarlos:

- `--demo-campo` recorre los **7 pasos** como quien hace la instalación por
  primera vez y marca cada uno *ejecutable / fricción / BLOQUEADO*. Resultado:
  **2 / 1 / 4**, primer freno en el PASO 1.
- `--demo-mision` cruza los tres configs reales contra las cuatro misiones y
  deduce **qué termina corriendo** el nodo, cuánto tarda en caer, y **qué dice la
  página mientras tanto**.

**`tools/test_check_commissioning_chain.py` — 94 tests en 7 capas:** utilidades
de texto, extractores sobre fuentes sintéticas, los dos oráculos con números
fijados, un test por código de hallazgo sobre un **repo sano al que se le inyecta
un solo defecto** (control negativo + delta), regresión sobre el repo real y CLI.

**`docs/commissioning-chain.md`** — el análisis completo y el orden de arreglo.

### Lo que hubo que resolver

- **El orden del gesto es el hallazgo, no la palabra "BOOTSEL".** Mi primer
  detector marcaba cualquier frase que juntara BOOTSEL y "enchufar" — y así
  también marcaba *"enchufá y **después** apretá BOOTSEL"*, que es el
  procedimiento **correcto**. Un checker que se enciende cuando alguien arregla
  el bug es peor que no tenerlo. Ahora mira qué hay **entre** las dos palabras y
  descarta el orden inverso; hay test.
- **Documentar el gesto del bootloader no es un defecto.** El repo tiene que
  explicar cómo se flashea un Pico. El hallazgo es la **contradicción**: el mismo
  gesto prometido para dos resultados distintos. El detector exige las dos
  mitades, y el control negativo lo fija (un repo sano documenta el UF2 y no
  enciende nada).
- **Leer una rama `elif` sin comerse la siguiente.** El handler `/m` y el
  `/wifi` son ramas hermanas: cortando por indentación floja, `/m` se queda con
  los `guardar()` de `/wifi` y el hallazgo del guardado parcial se disuelve. La
  mutación que afloja el corte hace fallar 7 tests.
- **El docstring del selector es una fuente de afirmaciones, no evidencia de
  comportamiento.** Es donde vive la instrucción al operario (C1, C12) y a la vez
  menciona cosas que el código no hace. Hay que blanquear docstrings para los
  hechos y leerlos aparte para las promesas — con la numeración de líneas
  intacta, para que la evidencia siga siendo citable.
- **C2 no podía depender de que los configs no tengan credenciales.** Escrito
  así, el "defecto" era el config y el arreglo era ponerle un SSID. El hallazgo
  real es el **camino**: una misión con precondición + un `except` que sigue de
  largo. Los configs son la evidencia de que hoy muerde, y entran en el texto,
  no en la condición.
- **`dreyfus` no entra en C8 y me obligó a afinar el alcance.** Lee el botón en
  el lazo, sí, pero escribe la SD *inline* a 5 Hz: no hay hilo en el core 1. El
  riesgo es de la **combinación**; quedó un test que fija que dreyfus y lab **no**
  aparecen en la evidencia.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **5 error · 5 warn · 2 info.**

| código | sev | qué |
|---|---|---|
| **C1** | error | **el gesto escrito para abrir el selector es el gesto del bootloader UF2.** *"Mantené BOOTSEL apretado mientras lo enchufás… soltalo cuando el LED titile"* (`selector.py` + `docs/MODOS_MISION.md`). La ROM del RP2350 muestrea BOOTSEL en el power-up: apretado al arrancar ⇒ disco `RP2350`, sin MicroPython, **sin LED, sin AP, sin medición**. El repo lo dice en `README.md:262`, `QUE_HACER.md:100` (*"BOOTSEL = sin MicroPython"*), `setup-completo.md:68` y `benchmark/README.md:57` — ahí es el procedimiento de **flasheo**. La ventana de 3 s de `rp2.bootsel_button()` **existe y funciona**: hay que apretar **después** del arranque, y eso no lo dice ningún documento. |
| **C2** | error | **la misión que no arranca se sustituye por otra, en silencio.** `mision_lab.conectar()` levanta `RuntimeError` sin WiFi (timeout 20 s); `main.py` la atrapa y sigue con el **nodo clásico**. Los tres `config.P*.json` **no traen `wifi_ssid`/`wifi_pass`** ⇒ hoy elegir LAB en cualquiera de los tres nodos termina en el clásico. El nodo queda vivo, con el LED igual, grabando a la SD: **parece éxito**, y el aviso existe sólo por USB — justo lo que el selector sin cable vino a evitar. |
| **C3** | error | **el único indicador de campo muestra la misión guardada, no la que corre.** La página rotula *"Misión actual: X"* con `cfg["mision"]`; ninguna misión escribe una marca de runtime. Con C2, un nodo caído al clásico dice **"Misión actual: LAB"** para siempre: el operario que verifica recibe de vuelta su propia intención. |
| **C4** | error | **reflashear borra la puesta en marcha.** `flash_node.ps1` copia `config.PX.json` **encima de** `/config.json`, y ninguno de los tres define `mision`, `wifi_ssid`, `wifi_pass` ni `wifi_mode` ⇒ cada actualización devuelve el nodo a `mision="off"` (clásico) y le borra el WiFi de campaña. Mismo modo de falla que el commit `3d2cbc5` (*"las misiones caían al nodo clásico en silencio"*), ahora por el lado de la config. |
| **C5** | error | **`flash_node.ps1` declara éxito sin evidencia.** (1) el `py_compile` de control corre **sólo sobre los `.py` de la raíz**: no cubre `misiones/`, que es el directorio del bug que motivó el guard; (2) cada copia fallida imprime en rojo **y sigue** — la última línea escribe `LISTO` en verde aunque hayan fallado todas (`$ErrorActionPreference="Stop"` no atrapa exit codes de `mpremote`); (3) no verifica lo que quedó en la placa, ni un `fs ls`. |
| **C6** | warn | **una clave WiFi de menos de 8 caracteres deja SSID nuevo + clave vieja.** El handler persiste clave por clave (`wifi_ssid → wifi_pass → wifi_mode`) y el validador rechaza `1..7`: revienta **después** de escribir el SSID. La excepción la come el `except` del loop (sólo cierra el socket): el celular muestra "no responde", no hay reset y no hay página de error. |
| **C7** | warn | **entrar al selector es un viaje de ida.** `run()` es un `while True` sin timeout. Un BOOTSEL de 3 s accidental durante la misión (el botón rozado al cerrar el gabinete) **detiene la campaña para siempre** y deja un AP abierto consumiendo. |
| **C8** | warn | **se lee BOOTSEL una vez por muestra con el escritor de SD en el core 1.** `baja` y `media` llaman `boton.revisar()` en cada vuelta (hasta ~333 Hz) y arrancan `RegistroSD` (hilo en core 1). Leer BOOTSEL en runtime suspende el acceso a la flash QSPI con IRQ deshabilitadas. **No afirmo que falle**: son dos riesgos a medir en banco (jitter y estabilidad con dos núcleos) y **tocan el bloqueante #1**. Se acota barato: revisar cada 100 ms. |
| **C9** | warn | AP **abierto** (`security=0`) con acciones destructivas por **GET**: `/m?v=off` reinicia el nodo en clásico. Un prefetch del navegador alcanza. Acotado (el AP sólo vive mientras dura el selector) ⇒ warn. |
| **C10** | warn | **`wifi_mode` significa algo distinto en cada misión** (lab lo ignora, media lo exige, el clásico decide AP vs push) y el selector lo **pisa a `"sta"`** al guardar una red: cargar el WiFi cambia de paso el comportamiento del clásico y de `media`, sin que nadie lo pida. |
| **C11** | info | el SSID se inyecta crudo en `value="…"`; sólo se escapa la comilla simple. Un SSID con comilla doble rompe el formulario justo en la pantalla donde hay que cargar la red. |
| **C12** | info | el docstring dice *"arranca normal (0 costo)"* y la ventana **cuesta los 3 s enteros** en cada arranque (lee el botón cada 30 ms y titila el LED), incluido el reset del propio selector y el de recovery de OTA. |

**Orden sugerido:**

1. **C1 — corregir la instrucción** (`selector.py` + `docs/MODOS_MISION.md`):
   *"enchufá, esperá el titileo, **después** apretá BOOTSEL"*. Cinco minutos, y
   sin eso los otros once no importan porque nadie llega al paso 2.
2. **C2 + C3, un solo commit de firmware**: que la misión que no arranca **se
   note** (código de LED por misión, o `mision_fallo` que la página lea) y que la
   página muestre lo que **corre**. Es la diferencia entre verificar en el campo
   y verificar volviendo con la notebook.
3. **C4 + C5** — `mision`/`wifi_*` en los `config.P*.json` (o que el flasheo
   **mergee** en vez de pisar), `LISTO` condicionado al conteo de fallos y un
   `fs ls`. Todo en el script, sin tocar firmware.
4. **C7** — timeout que reanude la misión. Diez líneas.
5. **C8 — antes de la sesión de banco del #1**, no después.
6. **C6, C9, C10, C11, C12** — higiene; salen solos cuando se toque el selector.

## Lo que está BIEN (fijado por test, para no ir a revisarlo)

- **`baja` y `media` drenan la cola de la SD antes de entrar al selector**
  (`registro.cerrar()`), y `dreyfus` hace `sd.flush()`: el reset no se lleva
  puesto el buffer en RAM. Eso es el fix de `e611bc5` bien terminado.
- **El scan de redes se hace ANTES de levantar el AP**, con el comentario que
  explica por qué (el CYW43 devuelve scan vacío con el AP activo).
- **El AP se llama `PICO-<node_id>`**: cada nodo se distingue del de al lado
  (contraste con FrioSeguro, donde las 5 placas publican el mismo SSID).
- **El fix de `3d2cbc5` está**: `flash_node.ps1` sí copia `misiones/`.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-13-cadena-puesta-en-marcha

python tools/check_commissioning_chain.py                  # informe; exit 3
python tools/check_commissioning_chain.py --detail         # + evidencia y hechos
python tools/check_commissioning_chain.py --demo-campo     # los 7 pasos, uno por uno
python tools/check_commissioning_chain.py --demo-mision    # que corre vs que elegiste
python tools/check_commissioning_chain.py --json

python -m unittest tools.test_check_commissioning_chain    # -> Ran 94 tests, OK
python -m unittest tools.test_misiones                     # -> 20 OK (regresion intacta)
```

Tres hallazgos se comprueban **sin la herramienta**:

- `grep -n "BOOTSEL" docs/MODOS_MISION.md README.md QUE_HACER.md` (C1)
- `grep -n "mision" firmwares/pico2w-node/config.P*.json` → **cero hits** (C4)
- `grep -n "LISTO" firmwares/pico2w-node/flash_node.ps1` y mirar qué la condiciona (C5)

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **94 tests en verde** (1,4 s). Sin descargas ni toolchains: cero riesgo de timeout.
- **`test_misiones` sigue en 20/20**: no toqué nada del firmware.
- **Control negativo real:** un repo sintético sano no enciende **nada**, y cada
  defecto inyectado por separado enciende **uno y sólo un** código. Cinco de los
  hallazgos tienen además su test "no salta cuando no corresponde" (C1 sin la
  contraparte del bootloader, C2 sin precondición, C6 con validador permisivo,
  C8 sin hilo en el core 1, y el caso de dos defectos → dos códigos).
- **Verificado por mutación — las 8 hacen fallar la suite:** sacar la guardia del
  orden del gesto, aflojar el corte del bloque `elif`, no blanquear docstrings,
  cambiar el AND de C1 por OR, sacarle a C8 la exigencia del hilo, invertir la
  prioridad del exit code, buscar los `guardar()` en el archivo entero en vez de
  la rama, y sacarle a C2 la exigencia del fallback de `main.py`.
  *(El andamio de mutación fue descartable: no se commiteó. Borré el
  `__pycache__` antes de cada corrida.)*
- **No se tocó una sola línea de firmware, ni de `vercel-dashboard/`, ni el
  script de flasheo.** El branch agrega 3 archivos y edita `QUE_FALTA.md`. No hay
  build de dashboard que correr (`vercel-dashboard/` es HTML estático + funciones
  serverless; su `package.json` no tiene `scripts`).

## Qué quedó sin verificar

- **Todo sale de leer el repo, no de mirar una puesta en marcha.** Los oráculos
  demuestran el efecto de lo que dice el código; no que la placa lo haga.
- **C1 se apoya en el comportamiento documentado de la ROM del RP2350.** Es
  exactamente lo que el propio repo describe en su procedimiento de flasheo,
  pero **conviene confirmarlo con la placa en la mano antes de reescribir el
  instructivo**: enchufar un Pico con BOOTSEL apretado y mirar si Windows monta
  el disco `RP2350` o si aparece la red `PICO-P1`. **20 segundos, sin
  instrumental.** Es la verificación de mayor valor de toda la noche.
- **C8 es un riesgo declarado, no medido.** Se cierra contando gaps en banco con
  y sin la lectura del botón en el lazo.
- **C2 no se probó de punta a punta**: la caída al clásico está deducida del
  camino de excepciones, no observada. Se ve en un minuto con el Serial abierto,
  eligiendo LAB con un SSID inexistente.
- **Ningún fix aplicado** — generator ≠ evaluator. El primero de la lista (C1) es
  una línea de texto en dos archivos, y aun así no lo toqué: el que reescribe el
  instructivo tiene que ser el que lo probó con la placa.

## Estado

- Branch `nocturno/local-2026-08-13-cadena-puesta-en-marcha` pusheado (`0399124`),
  sale de `main` (`e611bc5`). datalogger volvió a `main` limpio.
- `QUE_FALTA.md` de datalogger: ítem **#10b** nuevo, dentro del branch.
  ⚠️ **Numeración:** lo numeré `10b` a propósito — el branch
  `nocturno/local-2026-08-10-cadena-vibracion` agrega un `#15`, y así los dos se
  mergean en cualquier orden sin pelearse el número (sí va a haber un conflicto
  trivial de contexto: los dos tocan la misma zona del archivo).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día SIN COMMITEAR**
  (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`, los dos tests del nodo GIMAP,
  `docs/ARMADO_NODO_GIMAP.html`, `.gitignore` modificado). **No lo toqué.**
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Duodécima noche que lo reporto:** es firmware que va a un equipo a 2000 km y
  vive **sólo en este disco**. **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  diecisiete noches anteriores: `agentes/`, `dominios/`, `enlace/`, más
  `agentes/diseno3d.md`, `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html` y
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- ℹ️ `C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-08-11-b-presupuesto-standby`. **No lo cambié.**
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío (sólo el `.gitkeep`). El único
  `enlace\maquinas\*.estado.json` (DESKTOP-RK8DH7C) tiene `ultima_vez_viva` del
  **2026-08-07** — el latido volvió a correr en agosto pero está parado hace
  6 días. **No lo toqué** (los scripts de ENLACE son trabajo de día sin commitear).
- La cola de merge suma **55 branches** en origin (galgas 19, datalogger **17**,
  frioseguro 17, cosechador 2).

## Para @firmware / @muestreador / @cronista / @verificador

- **@firmware:** **C1 es tuyo y son dos líneas de texto** —pero pasalas por la
  placa antes de escribirlas. **C2+C3 son el mismo commit** y son la diferencia
  entre un sistema que se verifica parado en el punto de medición y uno que no.
  **C4+C5** son del script, no del firmware: media hora y sacan de la mesa el
  modo de falla que ya mordió una vez.
- **@muestreador:** **C8 entra en tu bloqueante #1.** Si el benchmark
  MicroPython-vs-C se corre con `boton.revisar()` en el lazo, parte del jitter
  medido es del botón, no del runtime — y la decisión fundacional del proyecto se
  toma con ese número. Acotarlo a 100 ms **antes** de la sesión de banco.
- **@cronista:** `docs/MODOS_MISION.md:21` presenta el fallback silencioso como
  una virtud (*"ante cualquier error cae al nodo clásico"*). Para `mision=off` lo
  es; para una misión elegida hace 30 segundos, no. Ese párrafo hay que
  reescribirlo junto con el arreglo de C2, no antes.
- **@verificador:** el DoD es *"cada paso del procedimiento de puesta en marcha
  tiene un hecho del repo que lo confirma o lo desmiente"*. Los 94 tests son el
  oráculo y `TestRepoReal` fija los 12 hallazgos. **Puntos a atacar, en orden:**
  (1) **C1 es el único hallazgo con una premisa fuera del repo** —el muestreo de
  BOOTSEL por la ROM del RP2350—; si esa premisa cayera, C1 se cae entero (los
  otros once no dependen de ella). Es también el más barato de confirmar: 20 s
  con una placa. (2) **C8 está declarado como riesgo, no como hecho**: si lo
  medís y no hay jitter, bajalo a info, pero el conteo de errores no cambia.
  (3) **C9 es el más discutible**: el AP sólo existe mientras dura el selector,
  así que la exposición es física y acotada — está en warn por eso.
