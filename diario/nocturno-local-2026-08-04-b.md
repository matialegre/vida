# Nocturno local — 2026-08-04 (2do turno, "-b")

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "terminarlo primero, antes del trabajo Dreyfus").
**Branch:** `nocturno/local-2026-08-04-b-contrato-rv1` (pusheado, commit `3c7523b`).

## Tarea elegida y por qué

El 1er turno de hoy fue a galgas, y los dos de ayer a datalogger y FrioSeguro.
Repasé los ítems sin branch de los cuatro repos:

- **FrioSeguro** (P1 PLATA): sus 🔴 sin branch son flashear, el piloto en la heladera,
  comprar la caja IP65 y **decidir precio/contrato** — hardware, compras o decisiones de
  plata. Nada de software puro me queda ahí esta noche.
- **Cosechador** (P2): bloqueado por la compra; su único análisis offline ya está en branch.
- **Datalogger** (P0): es el repo con el commit de día más reciente (`e611bc5`) y el que
  la orden de Matías pone primero.

Así que fui a datalogger. Y como anoche, el hueco real no era un ítem del `QUE_FALTA` —
era algo que el `QUE_FALTA` **no nombraba**:

> **el contrato del frame RV1.**

El frame RV1 es lo único que cruza los **tres lenguajes** del sistema. Lo arman **12
lugares** (MicroPython del nodo, C++ del gateway, el benchmark) y lo desarman **3 parsers**.
Nadie los comparaba.

Lo elegí porque **los tres modos de falla no son equivalentes, y el peor es mudo**:

| Falla | Qué pasa | ¿Se nota? |
|---|---|---|
| Campo de más | basura en `payload` | sí |
| **Campo de menos** | `nodo.py:386` `if len(parts) < 8: return` · gateway `if (idx < 0) return false` | **NO — descarte silencioso** |
| `src`/`dst` invertidos | el dato se atribuye al nodo equivocado; el dedupe `src#pid` colisiona | no, hasta que dos nodos se pisan |

El descarte silencioso es el caro: el emisor **transmitió bien** (el TX de LoRa devuelve OK,
`tx_ok` sube) y el receptor nunca lo vio. Sin contador, sin log, sin error. **En el campo
eso se lee como "problema de alcance"** — y el ítem #6 del QUE_FALTA es justamente una
prueba de alcance.

No duplica ningún branch: los 13 de datalogger son eco-schedule, INA219, sd-integrity ×4,
stale-cluster y afines. Ninguno mira el frame.

## Qué hice

1. **`tools/check_rv1_contract.py`** (stdlib, solo lectura, sin radio ni hardware). Cruza
   emisores, parsers y specs de doc contra el canónico
   `RV1|src|dst|pid|ttl|tipo|via|payload`:
   - **Emisores Python**: literal `"RV1|…"` + su tupla de args del `%`, mapeando cada
     placeholder a su argumento **posicionalmente** — hace falta para distinguir
     `cfg["node_id"]` (identidad propia) de `cfg["mesh_dst"]` en los campos 1 y 2, que es
     donde vive el hallazgo del orden. Junta sentencias partidas en varias líneas.
   - **Emisores C++**: la concatenación `"RV1|…" + expr + "|…"` se normaliza sustituyendo
     cada término no-literal por `{expr}` y se cuenta el shape resultante.
   - **Parsers**: los 3 idiomas reales (split+len en MicroPython, el lazo de separadores
     en C++). Lo que no entiende lo marca `P-UNKNOWN` — **nunca lo da por bueno en silencio**.
   - **Specs de doc**: `RV1|a|b|c` en comentarios, docstrings triples y markdown. Hizo
     falta seguir los docstrings triples: **la mitad de las specs del contrato viven ahí**,
     no en comentarios `#`.
   - **Descubrimiento**: un archivo con frames RV1 fuera de la lista auditada levanta
     `S-NEW`, así que una fuente nueva no pasa desapercibida. (Se disparó de verdad: cazó
     mis propios archivos nuevos mientras trabajaba.)

   Exit 0/1/2 para usarlo de gate antes de tocar frames. `--json`.

2. **`tools/test_check_rv1_contract.py`** — **56 tests** en 7 capas: doc-vs-código, los
   helpers puros, los dos extractores de emisores, el de parsers, cada código de hallazgo
   por separado, la **regresión sobre el repo real** (la evidencia de los hallazgos) y el CLI.

3. **`docs/rv1-contract.md`** + ítem **#14** nuevo en `QUE_FALTA.md` y notas en el **#3** y
   el **#6**.

## Hallazgos (con test que los demuestra — NO corregidos, generator ≠ evaluator)

Corrida real: **12 emisores (6 conformes), 3 parsers, 12 specs de doc → 26 hallazgos.**

- **H1 — el grande: 3 de las 4 misiones no llegan al gateway.**
  `mision_baja:103`, `mision_media:99` y `mision_dreyfus:125` emiten
  `RV1|<dst>|<src>|<ttl>|<cuerpo>` — **5 campos y con src/dst invertidos**. El gateway
  busca 7 separadores y hace `return false`; el nodo hace `return`. **El frame no existe.**
  Es el commit `da574c3` completo ("los 4 dataloggers de la taxonomía GIMAP en un
  firmware") con 3 de sus 4 misiones sin canal en vivo. (`mision_lab` se salva: va por
  broadcast UDP, no toca RV1.) La SD sigue siendo la fuente de verdad, así que **el dato no
  se pierde** — lo que se pierde es la única forma de mirar el nodo sin ir a buscar la
  tarjeta, que es lo que se necesita en campaña.

- **H2 — el gateway manda los comandos con 7 campos.** `esp32_dashboard.ino:391` arma
  `"RV1|GW|" + node + "|" + pid + "|3|C|" + cmd`: le falta el `via` vacío. El **orden está
  bien** (el gateway es el `src` legítimo — el checker no lo marca por orden, sólo por
  conteo), pero `nodo.py:386` exige 8 → descarte. El nodo nunca recibe el comando, nunca
  ackea, y el gateway loguea `[cmd] sin ACK de P1, abandono`.
  **Esto toca el QUE_FALTA #3 de frente:** ahí está anotado *"no mandar `eco on` a P1/P2,
  quedan inalcanzables"*, atribuido al sleep. **Hay una segunda causa, más simple y
  anterior.** Cuál manda hoy se decide en banco. Lo que lo delata: el nodo **sí** emite sus
  ACKs con 8 campos (`nodo.py:343`) — emisor y receptor del mismo par están desalineados en
  un solo sentido.

- **H3 — sin salto de repetidor para tráfico de misiones.** El relay (`nodo.py:415`) corre
  **después** del parseo de 8 campos. **El QUE_FALTA #6 no puede pasar** con misiones: es
  falla de contrato, no de alcance. (Con frames de datos `tipo D` sí funciona.)

- **H4 — src/dst invertidos.** Si alguien "arregla" sólo el conteo, el gateway registraría
  todo bajo el nodo `GW` y la clave de dedupe pasaría a ser `GW#<ttl>`, **igual para todos
  los nodos**: el segundo que hable se descarta como duplicado. Sería peor que hoy porque
  ya no es mudo, es plausible.

- **H5 — la doc es la causa raíz.** `nodo.py:265` y `esp32_dashboard.ino:195` documentan
  **7 campos** (omiten `via`) — y el `.ino` se **contradice a sí mismo seis líneas más
  abajo**, en la misma función (`:201` sí dice 8). Y `docs/MODOS_MISION.md:39` documenta el
  dialecto de 5 campos invertido **afirmando "compatibles con el gateway/malla existente"**.
  La lectura más probable: las misiones se programaron **contra el docstring, no contra el
  parser**, y el docstring estaba mal. La spec correcta estaba en **`QUE_HACER.md:213`**
  todo el tiempo.

- **H6 — el test que existe FIJA el dialecto roto.** `test_misiones.py:170,201` afirman
  `frame.startswith("RV1|GW|P1|3|DREY,seq=")`. La suite pasa **20/20 en verde** validando
  el frame que el gateway descarta: no es un test de contrato, compara la misión consigo
  misma. Al aplicar el fix, esas dos aserciones cambian en el mismo commit.

- **Nota aparte — dos caminos documentados que no existen:** (a) `mision_dreyfus.py:20`
  dice que *"`esp32_lora_rx.py` ya sube frames RV1 al cloud"* — ese script **sólo imprime
  por USB**, no parsea RV1 ni habla con la nube; (b) el protocolo **SD-por-LoRa** de
  `mision_media` (`SDLS`/`SDGET`/`SDCHK`) **no tiene contraparte**: el gateway no menciona
  ninguno de los tres. El nodo escucha pedidos que nadie manda.

**Lo que está BIEN y queda fijado por test** (tan importante como lo anterior):
**`nodo.py` es canónico en sus 5 emisores** (ack, ráfaga, relay, datos, stream) y **los dos
parsers principales están exactamente de acuerdo** — 8 campos, campo 1 = origen. El núcleo
de la malla (datos + ACK + relay + el `via` que reconstruye la ruta en el gateway) es
sólido; lo roto es la capa de misiones que se le montó encima. Y el checker **no marca
todo**: `QUE_HACER.md:213` y `QUE_FALTA.md` salen limpios — son el control positivo.

**Advertencia sobre el fix** (en el doc, no aplicado): pasar las misiones al frame canónico
hace que **llegue**, no que **se entienda**. El gateway no tiene handler para los cuerpos
`BAJA,…`/`DREY,…`: al no ser tipo `D` caen en el `else` de `loop()`, que registra el nodo y
loguea la línea pero no extrae ningún campo. **El fix completo son dos pasos**, y el
segundo es del gateway.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-04-b-contrato-rv1
python tools/check_rv1_contract.py                  # -> 26 hallazgos, exit 1
python tools/check_rv1_contract.py --json
python -m unittest tools.test_check_rv1_contract    # -> Ran 56 tests, OK
python tools/test_misiones.py                       # -> 20 OK (regresión intacta)
```

Los tests de `TestRepoReal` **fijan los 26 hallazgos actuales**: si alguien arregla uno, el
test falla y avisa que hay que actualizar el doc. Es la red de seguridad, no una foto.

## Qué quedó sin verificar (banco / hardware — trabajo de día)

- **Que el descarte sea realmente silencioso en la placa.** Está leído del código (`return`
  sin contador), no observado. **Demostración de 10 minutos:** nodo en misión `baja`, mirar
  el Serial del gateway — la línea `[lora rx] rssi=… | RV1|GW|P1|3|BAJA,…` **sí** aparece
  (`:1258` imprime siempre, antes del parseo) y el nodo **no** aparece en el dashboard. Ese
  par de hechos juntos es el hallazgo entero.
- **Cuál de las dos causas manda en `eco on`** (H2 o el sleep del #3): probar con el nodo
  despierto.
- **El salto de repetidor** (H3) con dos nodos separados.
- Que el `tipo` nuevo del fix propuesto no colisione con `D`/`C`/`A`/`B`/`S`.
- El checker lee el **repo**. Si hay una placa flasheada con firmware no commiteado, el
  repo miente: verificar qué versión corre antes de concluir.
- No corrí ningún build de dashboard (no toqué web/ ni el `.ino`).

## Estado

- Branch `nocturno/local-2026-08-04-b-contrato-rv1` pusheado (1 commit, `3c7523b`).
  datalogger volvió a `main` limpio.
- `QUE_FALTA.md` de datalogger: ítem **#14** nuevo + notas en **#3** y **#6** (en el branch).
- 4 repos intactos salvo el branch de trabajo. `data/field_captures` de galgas **no tocado**
  (este trabajo ni entra a ese repo). Jamás mDNS: no toqué nada de descubrimiento.
- ℹ️ **`C:\Proyectos\cosechador` está checkouteado en `nocturno/local-2026-07-18-modelo-energia`,
  no en `main`** (estado previo, no lo hice yo). **No lo cambié** — cambiar el checkout de
  Matías sin avisar es peor que dejarlo. Cuando drene ese branch, ojo con eso.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las cuatro noches
  anteriores: `agentes/{esquematico,pcb}.md`, `dominios/{diseno,esquematico,firmware,hardware,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md` y `dominios/diseno3d.md`).
  **No los toqué ni los commiteé** — no es trabajo mío. Matías: commitealos, o la rutina
  cloud choca en el próximo `git pull`.
- La cola de merge suma **41 branches** en origin (galgas 15, datalogger 13, frioseguro 12,
  cosechador 1). El tooling de drenaje (`tools/merge_queue_status.py` +
  `tools/resolve_doc_conflicts.py`) sigue listo y sin usar: falta la sesión humana.
  **Nota de prioridad:** este branch explica por qué dos ítems del DoD del datalogger
  (#3 y #6) podrían venir fallando por una causa que no es la anotada — si Matías drena
  poco, éste da información que cambia qué se prueba en banco.
