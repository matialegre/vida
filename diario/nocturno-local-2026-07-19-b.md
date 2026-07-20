# Nocturno LOCAL — 2026-07-19 (turno B, worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
La **malla RV1 del datalogger** (el flood routing: los nodos escuchan el aire,
deduplican, decrementan TTL y reenvían) vivía **solo en el firmware y sin un solo
test offline** — los branches de `sd-integrity` cubrieron la SD, nunca el ruteo.
Escribí un **modelo/validador offline espejo 1:1** de `nodo.py::LoRaTx.poll/.service`
(`tools/rv1_mesh_model.py`, stdlib) + **32 tests** + doc. Y al reproducir el formato de
frame que emite cada parte del sistema, saltó un **hallazgo 🔴 concreto y verificable**:
el **gateway arma el frame de comando con 7 campos (sin el campo `via`)** —
`esp32_dashboard.ino:391` → `RV1|GW|P2|42|3|C|reset` — pero **el nodo hace
`split('|',7)` y exige 8 campos**, así que **descarta todo comando downlink** antes de
mirarlo. Fix candidato de **1 carácter** (`|3|C||`, agregar el `via` vacío como ya hacen
todos los builders del nodo). **NO lo corregí** (es firmware, necesita confirmación en
banco con gateway + 2 nodos + ACK). **Branch: `nocturno/local-2026-07-19-b-rv1-mesh-model`
(datalogger), pendiente de merge.**

## Tarea elegida y por qué
**datalogger #6/mesh (P0 octubre — "terminarlo primero", orden de Matías 07-07).** La
mitad de software de "validar el salto de repetidor de la malla RV1": modelar offline el
ruteo antes de tener el banco de alcance. 100 % software, sin hardware.

Recorrí los 4 `QUE_FALTA`, todos los branches nocturnos y los nocturnos previos. Por qué ésta:
- **galgas (P0 octubre):** el turno de HOY (07-19) acaba de cerrar `rx-detection-replay`;
  no apilo dos análisis galgas el mismo día.
- **FrioSeguro (P1, plata):** el 18 trabajó su core (alert-model) y el 14 su vista; su deuda
  real es **deploy** (~1 h de día con @verificador sobre 6 branches), no código nuevo. No
  apilo la misma semana sobre el mismo repo.
- **cosechador (P2):** el 18-B cerró su modelo de energía; área cubierta esta semana.
- **datalogger (P0):** el benchmark quedó en `main`; el resto en branch (ina219/ecolora,
  sd-integrity ×2, rssi, ssid-casing). **Pero** toda esa pila toca SD, energía y RSSI —
  **el ruteo mesh RV1 (poll/dedupe/TTL/relay), que es el corazón del sistema, no tenía ni
  un test offline.** Ese era el pedazo verificable sin hardware que nadie había tocado.

Por qué el modelo-y-test: es el patrón que ya funcionó (vpp/alert-hold/rx-detection en
galgas, alert-model en frioseguro, energía en cosechador) aplicado al subsistema que faltaba,
con un ancla dura de valor: **auditar los frames que el codebase realmente emite** contra el
formato que el nodo exige.

## Qué hice — branch `nocturno/local-2026-07-19-b-rv1-mesh-model` (datalogger)
Sale de `main`. **3 archivos nuevos + 1 nota en QUE_FALTA. Cero borrados, no toca firmware,
ni la SD, ni la nube, ni ninguna otra branch.** (`git diff main --stat` → 732 inserciones, 4 archivos.)

| Archivo | Qué |
|---|---|
| `tools/rv1_mesh_model.py` (nuevo, 365 líneas) | Espejo 1:1 de `nodo.py::LoRaTx`. `parse_frame` (mismo criterio que el firmware: `startswith('RV1|')` + `split('|',7)` + `len>=8`), `validate_frame` (reporta campos faltantes/vacíos/tipos raros), `MeshNode.poll/.service` (eco, dedupe `src#pid`, cmd+ack, cancel-relay al ver dup, TTL relay con `via+=,id`), `_prune_seen`, y `audit_builders()` que reconstruye **cada frame que emite el codebase** (nodo D/S/B/A + gateway C) y lo valida. `simulate_flood()` propaga un frame por una topología y verifica que el TTL acota saltos y el dedupe acota transmisiones. CLI: `--audit-builders` (exit 1 si algún frame se dropearía), `--validate`, `--demo-flood`. |
| `tools/test_rv1_mesh_model.py` (nuevo) | **32 tests** `unittest` (sin deps, no tocan hardware): parseo (canónico, prefijo malo, pocos campos, payload con `|`, via con ruta, ttl basura), validación, dedupe (nuevo→encola, dup no reencola, dup cancela relay pendiente, eco propio, ttl=1 no reenvía, dst=yo no reenvía), comando (ack+ejecuta una vez; dup ackea pero no reejecuta), service (transmite tras backoff, uno por llamada), **auditoría (los frames del nodo válidos; el del gateway INVÁLIDO — regresión del hallazgo)**, y flood (TTL insuficiente no entrega, suficiente sí, dedupe acota TX). |
| `docs/rv1-mesh-model.md` (nuevo) | Formato canónico de 8 campos, los 3 hallazgos, cómo verificar, alcance honesto, y tabla de correspondencia 1:1 modelo↔firmware para @verificador. |
| `QUE_FALTA.md` | Nota "EN BRANCH pendiente" bajo #6 (mesh/repetidor). |

## El hallazgo (🔴, cuantificado, NO corregido — es de @firmware/@comms)
**El gateway emite el comando con 7 campos → el nodo lo dropea.**
`esp32_dashboard.ino:391` (`processPendingCmds`) hace:
```cpp
String f = "RV1|GW|" + pend[i].node + "|" + String(pend[i].pid) + "|3|C|" + pend[i].cmd;
// => "RV1|GW|P2|42|3|C|reset"  (7 campos: FALTA 'via')
loraSendFrame(f);
```
El nodo (`nodo.py:366-368`) hace `parts = s.split("|", 7)` y `if len(parts) < 8: return`.
Con 6 separadores → `len(parts)==7 < 8` → **descarta el comando** antes de mirar el `dst`.
Todos los builders del **nodo** sí ponen el `via` vacío (`||`, ver `nodo.py:324/430/455`);
el del gateway es el único que se lo saltea. **Fix candidato (1 char):** `...|3|C||` + cmd.

Salida real de esta noche (`--audit-builders`, exit 1):
```
[!! ] gateway comando (C)    esp32_dashboard.ino:391 processPendingCmds
      RV1|GW|P2|42|3|C|reset
      -> solo 7 campos, faltan 1 (el nodo hace split('|',7) y exige >=8 -> DROPEA el frame).
```
Hallazgos secundarios: **drift de docs** (los comentarios de `nodo.py:246` y
`esp32_dashboard.ino:195` describen el formato viejo de 7 campos sin `via`) y una
**observación** sobre que la ventana de dedupe es por tamaño (`>80`) + tiempo (`>8s`), no
solo tiempo (posible "nodo mudo tras reset" en mallas muy quietas). Detalle en el doc.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-19-b-rv1-mesh-model
git diff main --stat                                   # -> 4 archivos, 732 inserciones
python -m py_compile tools/rv1_mesh_model.py tools/test_rv1_mesh_model.py   # exit 0
python -m unittest tools.test_rv1_mesh_model            # -> OK (32 tests)
python tools/rv1_mesh_model.py --audit-builders         # -> [!!] gateway comando, exit 1
python tools/rv1_mesh_model.py --demo-flood             # TTL=2 no entrega; TTL>=3 sí
python tools/rv1_mesh_model.py --validate 'RV1|GW|P2|42|3|C|reset'   # INVALIDO
```
**Resultado obtenido esta noche:** `py_compile` exit 0 · **32/32 OK** en <0.01 s · la
auditoría marca 1 frame que el nodo dropearía (el comando del gateway) · el flood sobre la
malla `P4—P3—P2—GW` da entregado=False con TTL=2 y entregado=True con TTL≥3. Sin descargas
ni toolchains pesados — **cero riesgo de timeout** (disciplina del 07-07 respetada).

## Qué quedó SIN verificar (necesita banco — no se cierra de noche)
1. **Que el fix del hallazgo haga llegar el comando** — requiere gateway + 2 nodos + un
   comando real con su ACK. El modelo predice que con `||` funciona; falta el ensayo.
2. **El timing fino de la malla** (backoff, listen-before-talk, colisiones, latencia) — el
   modelo abstrae el tiempo por rondas; lo real es banco (QUE_FALTA #6/#7 de datalogger).
3. **El caso post-reboot del dedupe** — reproducirlo pide dos nodos y forzar un reset.

## Reglas respetadas
Solo software. Nada borrado, nada movido. **No toqué firmware** (`nodo.py` y
`esp32_dashboard.ino` intactos — el hallazgo se flagea, no se corrige), ni la SD, ni la
nube. No toqué otros repos. Jamás mDNS. `__pycache__` ya ignorado por el `.gitignore` del
repo (solo 4 archivos en el diff). Identidad git = Matías. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-19-b-rv1-mesh-model` (datalogger, pusheado a origin; sale de `main`).

## Notas para @verificador / @firmware / @comms / @director
- **@verificador:** el DoD es *"cada decisión de `rv1_mesh_model.py` coincide con
  `nodo.py::poll/.service`, y `audit_builders` cataloga bien cada frame emitido"*. La tabla
  de correspondencia 1:1 está en el doc. Puntos a atacar: (a) **¿el modelo diverge del
  `.ino`/`.py` en alguna rama** — el orden eco→dedupe→cmd→cancel-relay→TTL, o el
  `_build_relay` (¿`ttl-1` y `via` bien?)? Leé el `.py` contra `nodo.py:352-416`. (b) **¿el
  hallazgo del gateway es real o me equivoqué contando separadores?** Contá a mano los `|`
  de `esp32_dashboard.ino:391` vs. el `split('|',7)` de `nodo.py:366`. (c) **¿la sim de
  flood es una abstracción honesta** o esconde algo del timing que cambia el resultado de
  entrega/dedupe?
- **@firmware (dueño del fix):** el bug es de 1 carácter (`|3|C|` → `|3|C||`) en
  `esp32_dashboard.ino:391`, más actualizar los 2 comentarios de formato (drift #2). Al
  aplicarlo, actualizá el modelo/test en el mismo commit si tocás el formato. Confirmá en
  banco con un comando real + ACK antes de declararlo hecho.
- **@comms:** el modelo te sirve para razonar el ruteo antes del ensayo de alcance
  (QUE_FALTA #6): meté tu topología en `simulate_flood` y verificá que el TTL configurado
  (`mesh_ttl`) alcanza los saltos que vas a tener en campo.
- **@director:** una noche de **octubre (P0, "terminar el datalogger primero")** que da el
  **primer test offline del ruteo mesh** (subsistema crítico que estaba a ciegas) y
  **encuentra un bug de formato que dropea los comandos downlink** — sin gastar un peso, sin
  tocar hardware ni firmware. Tool autocontenido, no depende de otra branch; buen candidato
  a mergear tras @verificador, y el fix del gateway es trivial una vez confirmado en banco.
  **Sigue en pie:** la pila de FrioSeguro (6 branches) necesita ~1 h de día con @verificador.
