# Nocturno local — 2026-09-04

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (**P0** — RuView/GIMAP; "terminarlo
primero, antes del trabajo Dreyfus", orden de Matías del 07-07), zona
`firmwares/nodo-gimap/` + la mitad de PC.
**Branch:** `nocturno/local-2026-09-04-el-nodo-que-se-queda-mudo` (pusheado,
`f57483f`).
**⚠ Sale de `nodo-gimap/wifi-y-flasheo-2026-08-24` (`3491b72`), NO de `main`** —
es donde vive el firmware del nodo GIMAP. Ver la nota de merge más abajo.
**No colisiona con ningún branch abierto**: es el único que toca
`firmwares/nodo-gimap/`. No toca LoRa, ni el protocolo RV1, ni las misiones, ni
el gateway ESP32. **Nunca hubo mDNS de por medio.**

---

## TL;DR

> **El nodo GIMAP no reconectaba el WiFi. Si el enlace se caía después del
> arranque —un router que se reinicia, un canal que cambia— el nodo seguía
> midiendo para adentro, para siempre, con el LED diciendo "conectado y
> midiendo". En el banco de vibraciones eso es un ensayo perdido que no se
> repite.**

`red.conectar()` se llama **una sola vez**, en el arranque de `main()`. Después
de eso el loop principal no vuelve a mirar el enlace nunca más. Y `_broadcast()`
se tragaba entero cualquier error:

```python
def _broadcast(sock, puerto, datos):
    try:
        sock.sendto(datos, ("255.255.255.255", puerto))
    except Exception:
        pass
```

Tres hechos que juegan juntos, y ninguno de los tres alcanza solo:

1. **El CYW43 del Pico W no se reasocia solo.** En el port RP2 de MicroPython,
   perdido el AP la STA queda desasociada hasta que alguien vuelva a llamar a
   `connect()`. Nadie lo llamaba.
2. **UDP broadcast no acusa recibo**, y sobre una interfaz caída `sendto()`
   puede ni siquiera tirar. El `except: pass` cerraba el último resquicio por el
   que se podía notar.
3. **El LED seguía en `OK`** — dos destellos, que según la tabla del propio
   README significa "✅ Conectado y midiendo".

O sea: **el que mentía era el nodo.** Es el reverso exacto de la regla de la
casa *"un visor sin datos no miente"* — ahí el problema era la pantalla
dibujando señal linda de hardware muerto; acá es el hardware declarando una
salud que no tiene.

**Y hay un cabo suelto que esto puede atar.** En `PORTFOLIO.md` está anotado
*"el nodo se murió una vez a los 276 s, causa sin determinar"*. **Desde la PC no
hay ninguna diferencia entre un nodo muerto y un nodo mudo**: en los dos casos
dejan de llegar paquetes. Este defecto es un candidato concreto a explicar ese
episodio, y hasta hoy no quedaba rastro de un corte de enlace en ningún lado.
Con este branch, si vuelve a pasar hay tres hipótesis distinguibles con lo que
el propio nodo publica: **estado con `recon > 0`** = fue el WiFi · **`uptime_s`
reseteado** = se reinició · **no vuelve nada** = ahí sí está muerto.

## Por qué esta tarea y no otra

1. **Es el código más nuevo del portfolio y nadie lo auditó.**
   `firmwares/nodo-gimap/` se escribió anoche (23:01 del 03-09) y el último
   commit del cuartel dice *"Nodo GIMAP listo para enchufar del lado de la PC"*.
   Es lo próximo que Matías va a enchufar.
2. **Rotación.** Los tres turnos anteriores fueron frioseguro (09-03-b), galgas
   (09-03) y frioseguro otra vez (09-02-b). Datalogger es P0 y le tocaba.
3. **El PORTFOLIO pide exactamente esto**: dice *"NADA verificado con hardware"*
   y deja el episodio de los 276 s abierto. Atacar la parte de eso que se puede
   cerrar **sin** hardware es el mejor uso de una noche.
4. **Software puro y verificable sin banco**, y encima con un harness que ya
   existía en el repo para copiarle el estilo (`test_ota_gimap.py` reemplaza
   `machine` por un doble).
5. Miré antes los otros tres: galgas y frioseguro los trabajé anteanoche y
   anoche, y cosechador sigue bloqueado por la compra.

**Lo que NO elegí, y por qué lo digo:** el `red.py:64` que prefiere `wifi.json`
sobre `secrets.py` (la "deuda viva" del PORTFOLIO). Es real, pero **el daño
concreto es fino y de un solo uso**: sólo muerde a un nodo actualizado por OTA
que además tenga un `wifi.json` viejo, y el flasheo por cable lo tapa. Preferí
el que hoy puede arruinar un ensayo entero. Queda como estaba.

## Qué hice

**Invariante: el que dice si hay enlace es el CYW43, no el resultado del envío.**

**1. `red.enlace_ok()`** — `w.active() and w.isconnected()`. Las dos mitades:
`isconnected()` solo no alcanza si la radio quedó apagada por un intento previo
de `conectar()`, que termina con `wlan.active(False)`.

**2. La vigilancia cuelga del `if` que ya existía** (el del estado, cada 2 s).
No se agrega un temporizador nuevo:

```python
if time.ticks_diff(time.ticks_ms(), t_estado) > SEG_ESTADO * 1000:
    if not red.enlace_ok():
        s, ip = _reenganchar(s)
        n = 0
        t_prox = time.ticks_us()
    t_estado = time.ticks_ms()
```

**3. `_reenganchar()`** — reintenta con espera creciente `(0, 5, 15, 30, 60)` s y
se queda en 60, para siempre. Cuatro decisiones, y las cuatro son bugs que me
evité al escribirlas:

- **No reinicia el nodo.** Era la salida tentadora y es la peligrosa: `boot.py`
  cuenta arranques y a los 3 sin llegar a operativo **restaura los `.bak` del
  último OTA**. Un router que se reinicia no tiene por qué deshacer una
  actualización de firmware. (Es la regla `[[ota-nunca-ladrillo]]` aplicada a un
  camino que no parecía de OTA.)
- **Socket nuevo**: el viejo quedó atado a la IP anterior y el DHCP del
  laboratorio puede dar otra.
- **`ip` se actualiza**, si no el estado publica una IP muerta y el visor manda
  a Matías a una dirección que ya no existe.
- **Se tira el buffer a medio llenar** (`n = 0`). Si no, el paquete siguiente
  lleva muestras de los dos lados del hueco, declara `fs=200` y tiene un pozo de
  minutos adentro: el visor calcula una fs efectiva inventada — y la fs efectiva
  medida **es justamente el número que el README pide anotar el día del
  encendido**. Medio paquete perdido no es un dato; un paquete que miente sí es
  un problema.
- Y el **deadline se reinicia** (`t_prox = ticks_us()`), si no el nodo arrastra
  45 s de atraso e intenta "recuperar" 9.000 muestras que nunca existieron.

**4. El corte queda contado y legible.** `recon`, `mudo_s` y `tx_err` viajan en
el JSON de estado (50508) → chip **"cortes de WiFi"** en `visor_gimap.py` y una
línea en `tools/rx_gimap.py`. **Mientras el enlace está caído ese JSON no
llega**: por eso son acumulativos y se leen cuando el nodo ya volvió. `seq` no
sirve para eso — sólo avanza con los paquetes que se mandan, así que un corte
no deja salto.

**5. `_broadcast` devuelve `bool` y cuenta `tx_err`** (loguea el primero, después
sólo cuenta). No reemplaza a `enlace_ok()`: cubre el otro modo de falla, el
envío que sí tira.

Firmware del nodo **1.0.5 → 1.0.6**.

## Cómo verificarlo (comandos exactos, sin hardware, sin red, sin esperar)

```bash
cd C:\Proyectos\datalogger
# el checkout de esta carpeta está en otro branch y sucio: usá un worktree
git worktree add /c/Proyectos/_dl-rev nocturno/local-2026-09-04-el-nodo-que-se-queda-mudo
cd /c/Proyectos/_dl-rev

python tools/test_reenganche_gimap.py              # -> OK -- todo verde (12 chequeos)
python tools/test_reenganche_gimap.py --mutantes   # -> 6/6 mutantes muertos

# sin regresión en lo que ya había
python tools/test_protocolo_gimap.py               # contrato emisor <-> receptor
python tools/test_red_gimap.py                     # loopback UDP
python tools/test_ota_gimap.py                     # lote atómico + rescate

# y el chip del visor, mirándolo (dos consolas)
python visor_gimap.py
python emisor_prueba_SIN_HARDWARE.py --destino 127.0.0.1 --cortes 2 --mudo 57

git worktree remove --force /c/Proyectos/_dl-rev
```

Los cinco corrieron esta noche y dieron exactamente eso, más `py_compile` sobre
los siete archivos tocados.

**El harness es lo que más me importa de la noche.**
`tools/test_reenganche_gimap.py` **corre el `main()` REAL** —no una copia
limpia, no un espejo— contra dobles de `machine`, `network`, `socket`, `time`,
sensores y batería, con un **reloj virtual**: 90 s de nodo en un par de segundos
y **sin una sola espera real**. El escenario es el que rompe: el AP se cae 45 s
en medio del ensayo y vuelve.

Lo que el banco modela con fidelidad, que es todo el punto: **el CYW43 no se
reasocia solo** (una vez caído queda caído hasta que alguien llame a
`connect()`) y **`sendto()` no tira** con el enlace abajo. Es decir: el test
tampoco puede detectar el corte por el resultado del envío, igual que el nodo.

**Los 6 mutantes** existen porque un test verde sobre algo que no se puede
romper no prueba nada: nadie vigila el enlace (**el bug original**, mata 5
chequeos) · reenganchar sin actualizar la IP · sin tirar el buffer · sin
reiniciar el deadline · `_broadcast` tragándose el error · sin espera entre
reintentos. **El primero reproduce el estado anterior al branch: no es un test
que acompaña al arreglo, es uno que habría cazado el defecto.**

**Y el chip del visor se miró, no se dio por bueno**: navegador real,
`cortes de WiFi: 2 (57 s mudo)` en la fila de chips. Captura guardada en
`docs/evidencia/visor-cortes-wifi.png`. Para poder verlo sin apagar un router,
`emisor_prueba_SIN_HARDWARE.py` (el generador sintético que ya existía) tiene
ahora `--cortes/--mudo`, y su JSON de estado incluye los tres campos nuevos —
ese archivo es un espejo del formato del nodo y tenía que seguir siéndolo.

## ⚠ Al mergear — leer esto primero

**Este branch NO sale de `main`.** `firmwares/nodo-gimap/` **no existe en
`main`**: vive sólo en `nodo-gimap/wifi-y-flasheo-2026-08-24` (`3491b72`), que
son **5 commits por delante de `main`**. Ese branch se mergea primero; después
éste, que sale de él y aplica limpio.

**Efecto colateral que conviene saber: esos 5 commits estaban SIN PUSHEAR** —
existían sólo en este disco, y el PORTFOLIO lo anota. Al pushear mi branch se
fueron a `origin` como ancestros, así que **ya están respaldados**. Igual
conviene que Matías haga el `git push -u origin nodo-gimap/wifi-y-flasheo-2026-08-24`
para que el branch tenga su propia referencia en GitHub; es un comando.

Después del merge conviene sumar `python tools/test_reenganche_gimap.py` al
mismo lugar donde ya corren los otros tests del nodo.

## Qué quedó SIN verificar por falta de hardware

1. **Que el CYW43 se reasocie de verdad con este código.** Apagar el router un
   minuto con el nodo midiendo, prenderlo, y ver volver los paquetes y el estado
   con `recon=1`. **Es el escenario entero y es el que hay que ver ocurrir.**
   5 minutos con el visor abierto — y encaja perfecto con la sesión en que se
   enchufe el nodo por primera vez, no pide un viaje aparte.
2. **El LED durante el reenganche.** En la Pico W el LED va **por el chip de
   WiFi** (`Pin("LED")` = WL_GPIO0) y `red.conectar()` hace `wlan.active(False)`
   en cada intento. No debería tirar —el arranque ya pasa hoy por ese mismo
   camino— pero **no está observado**, y `Led._aplicar()` no tiene `try`. Si
   fallara, se ve al toque en la prueba (1). No lo blindé preventivamente: sería
   especular, y el daño está acotado (un reset ahí deja el contador de `boot.py`
   en 1, no en 3).
3. **Cuánto tarda en engancharse en la red del GIMAP**, para saber si los tramos
   0/5/15/30/60 s son razonables o hay que apretarlos.
4. **La fs efectiva post-reenganche**: que después de volver siga a 200 Hz.
   `rx_gimap.py` ya la calcula sola.

## Límites declarados (no son omisiones)

- **Mientras no hay enlace, el nodo no mide.** A propósito: no hay SD en este
  firmware, así que una muestra que no se transmite es una muestra perdida —
  guardarla en RAM sería inventar un buffer que nadie vacía. El hueco se cuenta
  (`mudo_s`) y se ve.
- **Si el AP no vuelve nunca, reintenta para siempre** con el LED en `BUSCANDO`.
  No cae a modo AP: el modo AP tampoco mide y necesita un celular al lado.
- **La detección tarda hasta 2 s.** Contra cortes de decenas de segundos no
  cambia nada y no justifica un temporizador aparte.
- **`gaps` y `mudo_s` cuentan cosas distintas** y hay un test que lo fija: un
  corte de WiFi suma `mudo_s` y **0 gaps**.

## Hallazgo colateral que el branch NO toca (a propósito)

**Si el MPU6050 no responde, el nodo avisa 3 segundos y sigue de largo.**
`main()` parpadea `ERR_MPU` 300 ciclos de 10 ms y después transmite paquetes con
`ax..gz = 0` **para siempre**, indistinguibles de un acelerómetro perfectamente
quieto; el estado no publica ningún campo que diga "estoy sin MPU". En el visor
se ve una traza de aceleración plana y prolija. **Es el mismo patrón que este
branch arregla —el nodo declarando salud que no tiene— pero en el otro sensor**,
y merece su propia decisión (¿un flag `mpu` en el estado? ¿el visor tachando el
panel?), no un parche de paso. Anotado en el doc y en `QUE_FALTA`.

## Cosecha a biblioteca

El par **"el estado de salud lo dicta la capa de abajo, no el resultado de la
operación"** ya va por cinco implementaciones en dos lenguajes: `lastSupabaseSync`
(08-26), `faultAlerted1` (08-29), `lastTelegramAlert` (09-01-b), `probe_fault`
(09-02-b), el `decidir/confirmar` del notificador (09-03-b) y ahora éste. **No se
cosecha todavía**, por la regla de la casa: ningún módulo entra sin decir dónde
se probó, y esto no vio hardware. Cuando pasen su prueba conviene mirarlas juntas
con `@bibliotecario` y cosechar una sola.

Lo que **sí** es candidato aparte y bastante limpio: **el banco de reloj virtual
para firmware MicroPython** (`modulos_falsos()` + `Banco`). Corre el `main()`
real, simula minutos en segundos y no necesita hardware; sirve igual para el
firmware de misiones del mismo repo. Después de que alguien lo use una segunda
vez, es una ficha de biblioteca.

## Estado del repo — dos cosas para un minuto tuyo

- **`C:\Proyectos\datalogger` sigue con el árbol sucio** (10 archivos) y el
  branch `nocturno/local-2026-08-31-el-csv-que-no-avisa` **sin un solo commit**,
  **sexta noche**. Ya no bloquea (se esquiva con worktree) pero es trabajo
  colgando: o se commitea, o se tira. Lo anoto por sexta vez y no lo toco.
- **`C:\Proyectos\datalogger-gimap`** (el worktree del nodo) quedó **exactamente
  como estaba**: limpio, en su branch, `3491b72`. Trabajé en un worktree aparte
  que ya borré, y verifiqué al cerrar que los dos checkouts de Matías están
  idénticos a como los encontré.

---

## Estado del branch

`nocturno/local-2026-09-04-el-nodo-que-se-queda-mudo` → `f57483f`, pusheado a
`origin`. `QUE_FALTA.md` del datalogger actualizado (ítem **5b**, numerado así
para no correr las referencias a #14). Documento largo:
`C:\Proyectos\datalogger\docs\nodo-mudo-sin-reconexion.md`.

**Archivos:** `firmwares/nodo-gimap/main.py` · `firmwares/nodo-gimap/red.py` ·
`firmwares/nodo-gimap/README.md` · `visor_gimap.py` · `tools/rx_gimap.py` ·
`emisor_prueba_SIN_HARDWARE.py` (modificados) ·
`tools/test_reenganche_gimap.py` · `docs/nodo-mudo-sin-reconexion.md` ·
`docs/evidencia/visor-cortes-wifi.png` (nuevos).
