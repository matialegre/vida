# Nocturno local — 2026-09-06

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (**P0** — RuView/GIMAP, *"terminarlo
primero, antes del trabajo Dreyfus"*, orden de Matías del 07-07), zona
`visor_gimap.py` + `tools/` (la mitad de PC). **No toca el firmware del nodo.**
**Branch:** `nocturno/local-2026-09-06-el-hueco-que-no-se-ve` (pusheado, `9b35eda`).
**⚠ Sale de `nocturno/local-2026-09-04-el-nodo-que-se-queda-mudo` (`f57483f`)**,
que a su vez sale de `nodo-gimap/wifi-y-flasheo-2026-08-24`. Al mergear éste
entra también aquél: **no hace falta mergear el 09-04 aparte.**
**Nunca hubo mDNS de por medio.** No se tocó nada de galgas ni de frioseguro.

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_datalogger`, ya
eliminado) porque el árbol de `datalogger` tiene 6 archivos modificados y 3 sin
trackear de Matías, y un `checkout` los habría tocado. **Verificado al terminar:
los dos árboles (`datalogger` y `datalogger-gimap`) quedaron idénticos**, en los
branches donde estaban.

---

## TL;DR

> **El visor no miraba el `seq`.** Si un paquete se moría en el aire, sus 40
> muestras —200 ms de registro— desaparecían y las de los dos lados se pegaban
> **sin costura**. En pantalla: una onda continua, linda, sin ningún indicio. En
> un banco de vibraciones eso no es un detalle estético: es un empalme en el
> medio de la señal. La frecuencia que se lee de ahí está mal y **no hay forma de
> darse cuenta después**, ni en la pantalla ni en el CSV.

## Por qué esta tarea

1. **Cierra la otra mitad de una doctrina que ya estaba escrita.** *"Un visor sin
   datos no miente"* está resuelto desde hace varias noches: si no llega nada, la
   pantalla se vacía y lo grita. Lo que faltaba es **qué pasa cuando llega, pero
   incompleto** — que es el caso más probable en WiFi y el más peligroso, porque
   se ve bien.
2. **Es la cadena que Matías va a enchufar.** El nodo GIMAP + el visor son lo que
   se usa en el banco de vibraciones; las últimas noches cerraron el lado del
   nodo (OTA que no brickea, reenganche de WiFi). Éste es el **testigo del otro
   lado del enlace**, que no existía.
3. **Es 100 % software y se verifica sin hardware** — incluso mirándolo en el
   navegador, con el emisor sintético que ya estaba en el repo.

No había ningún branch abierto tocándolo: de los 28 nocturnos de `datalogger`,
**el único que toca `visor_gimap.py` o `tools/rx_gimap.py` es el 09-04**, que es
justamente la base de éste.

## El agujero, y por qué nadie lo veía

```python
def escucha_datos():
    ...
    magic, ver, seq, n, fs = struct.unpack(FMT_CAB, pkt[:TAM_CAB])
    ...
    _agregar(muestras)          # el seq se desempaqueta y NO SE USA
```

Tres disfraces, y ninguno es un descuido:

1. **El nodo no puede avisarlo.** UDP broadcast no tiene acuse: el nodo hace
   `sendto()`, el sistema le dice que sí, `seq` sigue subiendo. Un paquete que se
   pierde en el aire **no deja rastro del lado del nodo**.
2. **Y en la pantalla ya había un número que parecía ser justo ése.** El chip
   `gaps` viene del JSON de estado y lo cuenta **el nodo, sobre su propio
   muestreo** (cuántas veces se le pasó la ventana de 5 ms). Un `gaps: 0` se lee
   como *"no se perdió nada"* cuando lo que dice es *"no se me pasó ninguna
   ventana"*. **Todo lo que el visor mostraba de salud** (`gaps`, `recon`,
   `mudo_s`, `tx_err`, `uptime_s`) **era el nodo hablando de sí mismo.**
3. **La herramienta para probarlo ya existía y no probaba nada.**
   `emisor_prueba_SIN_HARDWARE.py` tiene `--gaps-falsos` desde hace rato, con el
   comentario *"para probar el contador de gaps"*. Saltea un `seq`… y el visor no
   lo notaba, porque el número que se movía en pantalla era el `gaps` que **el
   propio emisor fabricaba** en su JSON. La prueba confirmaba al emisor, no al
   visor.

Es el mismo patrón de las últimas noches (la sonda caída, la temperatura
congelada, el aviso que se rendía): **dos capas correctas y el agujero justo en
el medio.**

## Lo que salió al arreglarlo (y no estaba en el plan)

**1. El duplicado, que es el mismo error al revés.** Una PC con cable **y** WiFi
en la misma LAN recibe **cada broadcast dos veces**, una por interfaz. Sin mirar
el `seq`, el visor dibujaba las dos copias: cada tramo repetido y la onda con
**menos frecuencia de la real**. No es un escenario exótico: es la notebook
enchufada al cable sin apagar el WiFi. **Medido** (11 paquetes, 3 copias):

| | muestras dibujadas |
|---|---|
| visor viejo | **560** |
| visor nuevo | **440** (las que existían) |

27 % de señal que nunca se midió.

**2. El rearranque del nodo.** Al reiniciarse, el `seq` vuelve a 0 **y
`Piezos.cero()` mide de nuevo la línea de base**. Pegar el tramo nuevo al viejo
compara dos referencias distintas como si fueran una. Ahora se vacía la ventana y
se avisa.

**3. La `fs` efectiva estaba medida… al final del CSV.** `rx_gimap.py` la
calculaba y la imprimía; el visor no. Es el número que el propio `QUE_FALTA #5`
pide medir, y ahora está a la vista **mientras se ensaya**.

## Qué se entregó

`tools/continuidad_gimap.py` — **puro** (sin sockets, sin threads, sin reloj
propio: el tiempo entra por parámetro) y **compartido** por el visor y
`rx_gimap.py`, para que la pantalla y el CSV cuenten lo mismo de la misma manera.
Mismo criterio que `logica/reintentos.py` y `potencia_tx.h` de las noches
anteriores.

Cinco clases de paquete, y qué se hace con cada una:

| clase | qué se hace | por qué |
|---|---|---|
| `continuo` | se dibuja pegado | — |
| `hueco` | se dibuja **con un corte** y se cuenta | unir los dos lados dibuja una onda sobre un tramo que nunca se midió |
| `duplicado` | **se descarta** | dos interfaces oyendo el mismo broadcast |
| `desordenado` (≤4 atrás) | **se descarta** | sus muestras van *antes* de las que ya están dibujadas |
| `reinicio` | se **vacía** la ventana | la línea de base del piezo se volvió a medir |

**Se vacía cuando falta más de una pantalla entera** (`MAX_PUNTOS/40 = 15`
paquetes): si se perdió más que eso, lo que quedó dibujado no es contemporáneo de
lo que está entrando, y ponerlos uno al lado del otro miente igual que el
empalme.

En pantalla: **rayas rojas verticales** en los 4 gráficos (un hueco de 40
muestras en 600 se ve como un pliegue cualquiera si no se marca), **cartel
ámbar** —no rojo, a propósito: los datos que hay son reales, lo que dejó de ser
continuo es el eje de tiempo— y chips `perdidos en el aire` / `fs medida acá` /
`duplicados`. El chip viejo pasó a llamarse **`gaps (del nodo)`**.
En el CSV, columna nueva `perdidos_antes`, **al final** para que quien lea por
posición las 11 de siempre no se entere de que hay una doceava.

## Cómo verificarlo (comandos exactos, sin hardware, 3 minutos)

```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-09-06-el-hueco-que-no-se-ve

# 1) la lógica + el cableado REAL del visor
python tools/test_continuidad_gimap.py
python tools/test_continuidad_gimap.py --mutantes

# 2) de punta a punta, dos ventanas (el emisor NO es el nodo: grita SIMULADO)
python visor_gimap.py
python emisor_prueba_SIN_HARDWARE.py --destino 127.0.0.1 --gaps-falsos 5
#   -> http://127.0.0.1:8080
python emisor_prueba_SIN_HARDWARE.py --destino 127.0.0.1 --duplicar 3
```

**Resultados obtenidos esta noche:**

- `test_continuidad_gimap.py` → **56 chequeos, 0 fallos**. Tres bloques están
  escritos como **regresión** y comprobé que el mutante que reimplanta el defecto
  los pone en rojo: el hueco que se empalma, el duplicado que se dibuja, y el
  rearranque que no limpia. El bloque [10] **no es un espejo**: importa
  `visor_gimap.py` de verdad y le mete paquetes por la misma puerta por la que
  entran los del nodo.
- `--mutantes` → **10/10 muertos**.
- **De punta a punta contra `127.0.0.1`**, mismo escenario en las dos versiones:

| | `/datos` con `--gaps-falsos 5` |
|---|---|
| visor viejo | 600 muestras, **0 huecos**, **ninguna clave de salud de enlace** |
| visor nuevo | `perdidos: 6`, `perdida_pct: 16.2`, **3 marcas de hueco** en la serie |

- **Mirado en el navegador** (Playwright, no sólo el JSON):
  `docs/evidencia/visor-huecos.png` — cartel ámbar *"LLEGA INCOMPLETO — 7
  paquetes perdidos en los últimos 30 s (13.5%)"*, chip rojo `perdidos en el
  aire: 7`, `fs medida acá: 200.0 Hz` y las dos rayas rojas en el acelerómetro.
- Sin regresión: `test_protocolo_gimap`, `test_red_gimap`, `test_ota_gimap` y
  `test_reenganche_gimap` siguen los cuatro en verde.

## Qué quedó SIN verificar (pide el nodo enchufado)

1. Un hueco **real** —el nodo lejos del AP, el microondas prendido— apareciendo
   como raya roja. Lo probado es un hueco fabricado.
2. La notebook **con cable y WiFi a la vez** subiendo `duplicados` con el nodo
   real transmitiendo.
3. **Reiniciar el nodo a mano** con el visor abierto: la ventana tiene que
   vaciarse y salir el cartel del rearranque.
4. En un ensayo largo, correlacionar `fs medida acá` contra `gaps (del nodo)`:
   **si la fs cae y `gaps` no se mueve, la pérdida es de la red**; si se mueven
   los dos, es el nodo que no llega a muestrear. Ese cruce es diagnóstico y hasta
   hoy no se podía hacer.

## Anotado y NO tocado

- **El paquete no lleva tiempo propio.** El eje horizontal se reconstruye
  suponiendo `fs`. Los huecos ahora se ven; el **jitter del muestreo, no**. Meter
  un contador de microsegundos en la cabecera **cambia el formato de trama**
  (contrato con `rx_gimap.py`, el test de protocolo y el firmware): es una
  decisión, no un fix de noche. [@muestreador]
- **Un rearranque en los primeros 4 paquetes se lee como desorden** y se
  descartan hasta 4 paquetes antes de reengancharse. Es 1 segundo y se arregla
  solo; distinguirlo obligaría a cruzar el `uptime_s` del puerto de estado con el
  chorro de datos, dos flujos independientes. No vale la complejidad.
- **Sigue abierto el hallazgo que dejó el 09-04**: si el MPU6050 no responde,
  `main()` avisa 3 s y después transmite `ax..gz = 0` para siempre,
  indistinguible de un acelerómetro quieto, y el estado no publica ningún campo
  que lo diga. Es el mismo patrón (el nodo declarando una salud que no tiene) en
  el otro sensor. **Candidato claro para la próxima noche.** [@firmware]
- **`seq` es `uint32` en la cabecera** y entero infinito en MicroPython: a 5
  paquetes por segundo, `struct.pack(">I", seq)` reventaría a los ~27 años de
  encendido continuo. No se tocó.

## Nota de merge

Sale de `nocturno/local-2026-09-04-el-nodo-que-se-queda-mudo` (`f57483f`).
**Al mergear éste entra también el 09-04** (y con él la base
`nodo-gimap/wifi-y-flasheo-2026-08-24`); no hace falta mergearlo aparte.
**Con ningún otro de los 28 branches abiertos de `datalogger` hay colisión**: los
archivos compartidos son `visor_gimap.py`, `tools/rx_gimap.py`,
`emisor_prueba_SIN_HARDWARE.py` y `QUE_FALTA.md`, y **sólo el 09-04 los toca**,
ya adentro de la base. En `QUE_FALTA.md` el ítem se numeró **5c** (el 09-04 usó
5b) para no correr las referencias existentes a `#14` y a los ítems de abajo.

## Estado de los repos

`C:\Proyectos\datalogger` y `C:\Proyectos\datalogger-gimap` quedaron
**exactamente como estaban** (los 6 modificados + 3 sin trackear de Matías,
intactos; `datalogger-gimap` limpio en `3491b72`). El worktree temporal
`C:\Proyectos\_noche_datalogger` se eliminó. El branch está pusheado y el
`QUE_FALTA.md` del repo actualizado (ítem 5c).
