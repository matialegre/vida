# Nocturno LOCAL — 2026-07-17 (turno B, worker de la PC, Matías durmiendo)

> Segundo turno del 17. El turno A (`nocturno-local-2026-07-17.md`) trabajó galgas
> (linaje de firmware). Este turno trabajó **datalogger** — otro repo, sin pisarse.

## TL;DR para Matías
El nodo del datalogger tenía un **footgun de despliegue en el GIMAP**: los SSID WiFi son
**case-sensitive en el aire**, y el repo tenía la red del GIMAP escrita como **`"GIMAP"`** en
el nodo canónico y como **`"Gimap"`** en otros archivos. Si el AP real del GIMAP emite el
casing que no está en la lista, **el nodo no conecta** — y `QUE_HACER.md`/`LEEME_GIMAP.md`
ya lo advertían como riesgo abierto (item #8). Como **no se puede saber sin hardware** cuál
casing usa la red real, hice el nodo **tolerante a ambos**: una sola lista de redes
compartida (`wifi_nets.py`) con las dos variantes. Conecta emita `GIMAP` o `Gimap`, sin
depender de averiguar cuál es. Es un cambio quirúrgico, data-mayormente, verificado sin
hardware. **Branch: `nocturno/local-2026-07-17-b-ssid-casing` (datalogger), pendiente de merge.**

## Tarea elegida y por qué
**Datalogger #8 — "Verificar SSID real de GIMAP (case-sensitive `Gimap` vs `GIMAP`) y
reflashear gateway si difiere".** Nunca estuvo en un branch. Por qué esta y no otra:

- **Recorrí los 4 QUE_FALTA y todas las branches.** Casi todo bloqueante duro ya tiene branch
  esperando merge: galgas (7 branches), datalogger (5: ina219/ecolora, sd-integrity ×2, rssi),
  frioseguro (5, pura deuda de deploy — el turno A ya avisó 10 noches, no apilo más).
  Cosechador es P2 y está **gateado por compra** (todo hardware, sin software nuevo).
- **El benchmark MicroPython vs C (#1) ya está en `main`** (commit `56cf0b0`) — no es tarea nueva.
- **#8 era el hueco de software real que quedaba sin tocar** y con **impacto directo en el
  despliegue en el GIMAP** (que es el objetivo del datalogger: `LEEME_GIMAP.md` es literalmente
  la guía de traspaso a esa PC). Es un bug latente que muerde justo cuando el sistema llega a
  destino, el peor momento.
- **La parte de software es resoluble sin hardware, y de forma no-especulativa.** No adiviné el
  casing real: eliminé la dependencia de saberlo.

## Qué hice — branch `nocturno/local-2026-07-17-b-ssid-casing` (datalogger)
Sale de `main`. **1 archivo nuevo de firmware + 1 test nuevo + 3 imports + nota en QUE_FALTA.**
Cero borrados, no toca legacy ni snapshots físicos.

| Archivo | Qué |
|---|---|
| `firmwares/pico2w-node/wifi_nets.py` (nuevo) | **Fuente única** de la lista de redes. Mata la triplicación (`eco.py`/`ota.py`/`wifi_push.py` tenían cada uno su `NETS`, **raíz del drift de casing**). Incluye **ambos casings** del GIMAP con la misma clave. Docstring explica el porqué (constraint que el código no muestra). |
| `firmwares/pico2w-node/eco.py` · `ota.py` · `wifi_push.py` | Borran su `NETS` local y hacen `from wifi_nets import NETS`. El loop de conexión de cada uno queda igual. |
| `tests/test_wifi_nets.py` (nuevo) | Invariantes sin hardware: ambos casings presentes, misma clave, entradas `(str,str)` con límites 802.11/WPA2. |
| `QUE_FALTA.md` | #8 marcado 🔀 EN BRANCH + qué queda pendiente con hardware. |

**Por qué "ambos casings en la lista" y no un matcher case-insensitive por `scan()`:** el matcher
es más elegante, pero cambia el flujo de conexión (llama `scan()`, decodifica bytes) en 3
archivos de firmware que **no puedo correr sin hardware** — riesgo de romper el camino que HOY
anda (la red `"Pazos 2.4GHz"` de casa). La lista con dos entradas es **data**, no puede romper
ese camino, y es correcta por inspección del loop existente (recorre `NETS`, la variante ausente
falla y pasa a la siguiente). Doctrina: simplicidad primero, quirúrgico, nada especulativo.

## Cómo verificarlo (comandos exactos, sin hardware)
```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-17-b-ssid-casing
git diff main --stat

# El MISMO gate que corre el flasher (flash_node.ps1 hace py_compile antes de copiar):
cd firmwares/pico2w-node && python -m py_compile *.py     # -> exit 0

# Test de invariantes:
cd C:\Proyectos\datalogger && python tests/test_wifi_nets.py   # -> "OK: todos los invariantes..."

# Confirmar que ya no hay NETS local ni casing hardcodeado disperso:
grep -rn "NETS =" firmwares/pico2w-node/*.py    # -> solo wifi_nets.py
```
**Resultado obtenido esta noche:** `py_compile` exit 0 (los 8 `.py` del nodo) + los 3 tests
pasan. Sin descargas ni toolchains pesados — cero riesgo de timeout.

## Qué quedó SIN verificar (necesita hardware / banco en el GIMAP)
1. **Cuál es el SSID real del AP del GIMAP** (`GIMAP` o `Gimap`). El fix lo hace irrelevante para
   el nodo, pero conviene confirmarlo en banco y, si se quiere, dejar una sola entrada.
2. **El gateway físico.** Según `AGENTS.md`, el gateway hoy es el **Pico COM13
   (`pico2w-wifi-com13/wifi_push.py`)**, que usa `"Gimap"`. **No lo toqué** (es un snapshot de
   lo que está físicamente flasheado; divergirlo a ciegas es peligroso). Si ese gateway va al
   GIMAP, aplicarle el mismo criterio o reflashearlo con el nodo canónico. Queda anotado en #8.
3. **Que el nodo efectivamente conecte a una red `Gimap`/`GIMAP` real** — solo se prueba en el sitio.

## Reglas respetadas
Solo software. Nada borrado, nada movido. No toqué los snapshots por-COM (`com11/13/14`), ni el
ESP32 legacy, ni los `.py` legacy de la raíz (AGENTS.md los marca "no tocar"). No mDNS (no lo
rocé). Sin secretos nuevos (la clave `Gimap2218` ya estaba en el repo; no la agregué, la
centralicé). Verificación pesada = `py_compile`, instantánea, con toolchain ya presente. El
branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-17-b-ssid-casing` (datalogger, pusheado a origin; sale de `main`).

## Notas para @verificador / @comms / @director
- **@verificador:** el DoD es *"el nodo canónico conecta al GIMAP sea cual sea el casing del AP,
  sin cambiar el camino de conexión existente"*. Punto a atacar: **¿algún consumidor de `NETS`
  quedó sin migrar, o `wifi_nets.py` no se flashea?** Chequeo: `grep -rn "NETS" firmwares/pico2w-node`
  (solo wifi_nets define, los 3 importan) y `flash_node.ps1` copia **todos** los `*.py` de la
  carpeta (glob), así que el módulo nuevo viaja al device. Segundo punto: **¿el loop de `ota.py`
  penaliza mucho?** No corta en `NO_AP_FOUND` (espera su timeout), así que la variante ausente
  cuesta hasta 12 s en la ruta de recovery — está documentado en el docstring y es aceptable
  (sin el fix, esa ruta directamente fallaría).
- **@comms (dueño de #8):** falta el trabajo de banco (confirmar SSID real + decidir el gateway).
  El software ya no bloquea; el ítem queda como tarea de sitio, no de teclado.
- **@director:** una noche de datalogger P0 que **cierra un footgun de despliegue en el GIMAP**
  sin agregar branch a la pila de galgas. Sigue en pie lo que avisó el turno A: **la pila de
  merges (galgas 7 + datalogger 6 + frioseguro 5) necesita una sesión de día con @verificador.**
  Este branch suma uno más a datalogger, pero es chico y autocontenido (buen candidato a mergear
  primero para practicar el flujo).
