# Nocturno local — 2026-08-06 (2do turno, "-b")

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (P0 — "terminarlo primero, antes del
trabajo Dreyfus", orden de Matías).
**Branch:** `nocturno/local-2026-08-06-b-contrato-nube` (pusheado, commit `85dd9b8`).

## Tarea elegida y por qué

El 1er turno de hoy fue a galgas (identidad de binarios OTA), los de ayer a
FrioSeguro y datalogger. Repasé los ítems sin branch de los cuatro repos:

- **FrioSeguro** (P1 PLATA): sus 🔴 sin branch siguen siendo flashear, el piloto
  en la heladera, comprar la caja IP65 y decidir precio — hardware, compras o
  decisiones de Matías. (Ojo: **hay trabajo de día nuevo sin commitear ahí**,
  ver Estado.)
- **Cosechador** (P2): bloqueado por la compra.
- **Datalogger** (P0): es el que la orden de Matías pone primero y tocaba por
  rotación.

Fui a datalogger, y como las noches anteriores el hueco real no era un ítem del
`QUE_FALTA` — era algo que el `QUE_FALTA` **no nombraba**:

> **el contrato de la ingesta a la nube.**

El dato cruza **cuatro artefactos en tres lenguajes** y nadie los comparaba:

```
gateway ESP32-S3 (C++)  --JSON 1 Hz-->  /api (Node/Vercel)  --REST-->  Supabase
     esp32_dashboard.ino                  api/index.js              ruview_readings
                                                                          |
                                index.html  <---- /api/history -----------+
```

Lo elegí porque **el modo de falla de esta cadena no es un crash, es un
silencio**, y los tres saltos fallan distinto:

| Falla | ¿Se nota? |
|---|---|
| El gateway manda un campo de más | sí, sobra en el JSON |
| **El relay no copia un campo** | **NO** — nunca existió en la nube |
| **Supabase rechaza el INSERT** | **NO** — el `catch` es mudo y nadie mira la respuesta |
| **El comando cae en otra instancia lambda** | **NO** — la página igual dice "✓ enviado" |

**Encaja con el trabajo previo sin pisarlo.** Los 13 branches de datalogger son
eco-schedule, INA219 ×2, sd-integrity ×4, stale-cluster, RSSI, SSID, mesh RV1,
registro-SD y el **contrato del frame RV1** (08-04-b). Ese último audita
nodo→gateway; **éste empieza exactamente donde ese termina**: el frame llegó al
gateway, ¿qué pasa después? La cadena queda auditada de punta a punta.

## Qué hice

1. **`tools/check_cloud_contract.py`** (stdlib, solo lectura, sin red ni
   hardware). Lo que hizo falta resolver:
   - **Reconstruir el JSON que emite el gateway** desde C++: junté los string
     literals de cada `+=` en orden y caminé el esqueleto resultante con un
     scanner que lleva un stack de paths. Tolera a propósito los desbalanceos
     que dejan los `for` y los `if` (repetir una clave en el mismo path es
     idempotente; un cierre de más no puede vaciar el stack).
   - **Inlinear `streamFields()` dentro de `buildApi()`** — es una llamada, no
     código en línea. Sin el inline, los campos del nodo y los paquetes
     colgarían de la raíz y **todo el cruce posterior sería falso**. Hay un test
     que lo fija.
   - **Sacar comentarios sin romper strings**: `CLOUD_URL` contiene
     `"https://..."` y ese `//` no es un comentario. Con un stripper ingenuo se
     pierde la URL y con ella la clave y la tabla.
   - **Entender que el acceso a las filas del histórico es dinámico**
     (`r[metric]`): las opciones del `<select>` **son** parte del contrato, y
     una magnitud calculada en el browser (`ma`) no es una columna faltante.
     Sin esa distinción el checker gritaría por la única métrica que sí funciona.

   Exit 0/1/2, `--json`, `--fail-on`. Sirve de gate antes de re-deployar.

2. **`tools/test_check_cloud_contract.py` — 84 tests en 7 capas:** helpers puros,
   el reconstructor del esqueleto JSON (el núcleo), el parser del gateway con su
   inline, los tres parsers de la nube, **cada código de hallazgo con repos
   sintéticos en disco**, la **regresión sobre el repo real** (la evidencia) y
   el CLI.

3. **`docs/cloud-contract.md`** + ítem **#14** en `QUE_FALTA.md` y nota en el **#10**.

### Un falso negativo que cazaron los propios tests

El chequeo "no hay DDL de la tabla en el repo" empezó **sin disparar**: el
scanner encontraba `create table ruview_readings` … **adentro de mis propios
fixtures de test**. O sea, el checker se auto-absolvía del hallazgo más caro que
tiene. Lo cazó el test de totales al no cuadrar. Corregido excluyendo la
herramienta y su test del scan, con una regresión que lo fija.

## Hallazgos (con test que los demuestra — NO corregidos, generator ≠ evaluator)

Corrida real: **11 campos por paquete emitidos, 7 columnas persistidas, 6
consultadas, 4 magnitudes en el selector → 4 error / 17 warn.**

- **H1 (error) — el INSERT es mudo.** `persist()` (`api/index.js:48`) hace
  `await fetch(.../ruview_readings)` y **nunca mira la respuesta**: no hay
  `const r =`, no hay `r.ok`. Todo el camino de error muere en
  `catch (e) { /* nunca romper el push si Supabase falla */ }`.
  Tragar la excepción **está bien** — es deliberado y está comentado. Lo que
  falta al lado es **un contador**: hoy un INSERT exitoso y uno rechazado
  producen la misma traza, **ninguna**. Lo puede rechazar una policy RLS, una
  columna renombrada, la anon key rotada o el proyecto Supabase **pausado por
  inactividad** (el plan gratis lo hace). **El histórico puede estar vacío hace
  meses y el dashboard en vivo se vería perfecto**, porque el vivo no pasa por
  Supabase: sale del `global` del relay. La única señal sería un gráfico plano
  en "Historial por tiempo" — y eso se lee como "todavía no hay datos".

- **H2 (error) — la cola de comandos vive en la memoria de UNA lambda.**
  `store()` guarda todo en `global.__gimap`. En Vercel eso es la memoria de una
  instancia serverless, no estado compartido. El campo que duele es `cmds`: la
  página encola en la instancia A, el ESP postea contra la B, y **el comando no
  se entrega nunca**. Con tráfico bajo hay una sola instancia y **funciona** —
  por eso es insidioso: anda en el banco y falla cuando hay concurrencia, o sea
  justo cuando alguien mira el dashboard mientras el ESP empuja a 1 Hz.
  Los otros tres campos son la misma causa en warn: `lastIns` (el throttle de
  20 s es **por instancia**: con K instancias entran hasta K filas por ventana)
  y `raw`/`ts` (un GET en instancia fría devuelve `"esperando ESP..."` aunque el
  ESP lleve horas empujando).

- **H3 (error) — la UI confirma un envío que puede no haber pasado.**
  `index.html:315` decide con `r.ok` y le escribe al usuario
  **"✓ llega por LoRa en unos seg"**. El 200 sólo significa "una instancia lo
  anotó en su RAM". Es la misma clase de bug que los H1/H3 de FrioSeguro (el
  sistema le miente al usuario), y acá pega donde más molesta: **los comandos
  son `eco on/off`, la palanca del ítem #3.** Un `eco on` perdido se lee como
  "el nodo no respondió" — es decir, **como un problema de radio**, igual que el
  descarte silencioso que encontró el branch del frame RV1. Dos caminos
  distintos, el mismo diagnóstico equivocado esperando en el campo.

- **H4 (error) — la tabla no existe en el repo.** No hay
  `create table ruview_readings` en ningún archivo: la única definición vive
  dentro del proyecto Supabase. Si se pierde (o se pausa), no hay con qué
  recrearla — y no hay contra qué validar las columnas que el relay escribe a
  ciegas, lo que empeora H1. **galgas y frioseguro sí tienen su DDL versionado**
  (`SETUP_COMPLETO.sql`): datalogger es el que quedó afuera.

- **H5 (warn ×6) — la vibración nunca llega a la nube.** Los seis ejes del MPU
  (`ax,ay,az,gx,gy,gz`) se emiten, se dibujan en vivo y **no se persisten**. La
  única otra copia es `HIST` en el navegador: **se pierde al recargar la
  pestaña**. No es necesariamente un error (la SD es el registro, la nube es la
  vista de salud) pero **no estaba escrito en ningún lado**, y aclara el DoD:
  "logueando sin gaps" se verifica en la SD, **no en Supabase**.

- **H6 (warn) — el histórico es un muestreo, no un registro.** De cada push se
  guarda **un** paquete (el último de 25) y encima throttleado a 1 fila por nodo
  cada 20 s. Decisión razonable de costo; lo importante es que quede escrito,
  porque cualquier análisis que trate esa tabla como serie completa (consumo,
  gaps, pérdidas) está mirando 1 de cada N.

- **H7 (warn ×2) + H8 (warn) — el desperdicio que es casi una feature.**
  `route` y `seq` se escriben en cada fila y el histórico **no las pide nunca**;
  `hops` se pide y el dashboard **no la dibuja**. `seq` es la que duele: es
  exactamente lo que haría falta para detectar gaps, y ya se está guardando.
  Los tres juntos son **una vista de salud de la malla a un `<option>` de
  distancia**.

- **H9 (warn) — el histórico trunca el extremo NUEVO.**
  `api/history.js` consulta con `order=ts.asc&limit=10000`: PostgREST corta
  **después** de ordenar, así que con orden ascendente **lo que se pierde son
  las filas más recientes**. A 180 filas/hora/nodo el límite llega a las ~56 h
  con un nodo y **~19 h con tres**. El rango por defecto del selector es **24 h**.
  O sea: **con la malla de tres nodos andando, el rango por defecto ya trunca**,
  y el gráfico muestra datos viejos como si fueran los actuales, sin aviso — el
  "ahora" del eje X no es ahora. **Fix de una palabra: `ts.desc`.**

- **H10 (warn) — el rango que se ofrece no se puede devolver.** El endpoint
  clampea a 2160 h y el selector ofrece 7 y 30 días, pero el límite sólo alcanza
  para ~56 h de un nodo: las dos opciones largas están **garantizadas** a
  truncar. Se arregla junto con H9.

- **H11 (warn) — la clave, escrita a mano en tres archivos.** `gmp7h2qz9k` está
  en `api/index.js`, en `index.html` y **en el firmware** (`CLOUD_URL`,
  `esp32_dashboard.ino:40`). Rotarla obliga a tocar los tres **y a reflashear el
  ESP que está en GIMAP**. Además viaja como query string (`?k=…`), la parte de
  la URL que termina en los logs de acceso, y hoy alcanza para encolar comandos
  a los nodos.

**Lo que está BIEN y queda fijado por test** (tan importante: es lo que NO hay
que ir a revisar): **el relay escribe en la misma tabla de la que lee el
histórico**; **las claves del relay y de la página coinciden** (el encolado no
da 401); **ninguna magnitud del selector quedó sin fuente** — `vbat`/`temp_c`/
`rssi` son columnas consultadas y `ma` tiene su rama de cálculo en el browser,
así que **ningún gráfico sale vacío por contrato roto**; y **`vbat`, `temp_c` y
`rssi` cierran de punta a punta**: los emite el gateway, los persiste el relay,
los consulta el histórico y los dibuja la página. **El camino de la telemetría
de salud está sano; lo roto es lo que se le montó alrededor.**

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-08-06-b-contrato-nube
python tools/check_cloud_contract.py                  # -> 4 error / 17 warn, exit 1
python tools/check_cloud_contract.py --json
python tools/check_cloud_contract.py --fail-on warn
python -m unittest tools.test_check_cloud_contract    # -> Ran 84 tests, OK
```

Gate antes de re-deployar:
`python tools/check_cloud_contract.py && cd vercel-dashboard && vercel --prod`.

H9 se comprueba sin la herramienta, leyendo tres líneas
(`vercel-dashboard/api/history.js:11-14`): `order=ts.asc` + `limit=10000` +
`Math.min(2160, …)`.

Los tests de `TestRepoReal` **fijan los 21 hallazgos de hoy**: si alguien
arregla uno, el test falla y obliga a actualizar `docs/cloud-contract.md` en el
mismo commit. Es la red de seguridad, no una foto. (Ya funcionó una vez esta
noche: cazó el falso negativo del DDL.)

## Qué quedó sin verificar (nube — trabajo de día)

- **Si H1 ya pasó.** `select count(*), max(ts) from ruview_readings;` — si
  `max(ts)` es viejo, el hallazgo dejó de ser hipótesis y pasa a ser un
  histórico perdido. **Es la primera consulta que haría.**
- **El DDL real**, para versionarlo (H4): sacarlo del SQL Editor y commitearlo.
- **Las RLS de `ruview_readings`**: la anon key está en el bundle del dashboard,
  o sea es pública. ¿Cualquiera puede insertar telemetría? (Se cruza con el H5
  del branch de galgas de esta misma noche: la misma pregunta, otra tabla.)
- **H2 en vivo**: encolar un comando y ver por serial si el ESP lo retira;
  repetir con dos pestañas encolando a la vez — la segunda expone el problema.
- **H9 en vivo**: pedir 30 días y comparar el `ts` del último punto del gráfico
  contra el `max(ts)` de la tabla.
- **Todo está leído del código, no observado.** No hay ESP encendido ni acceso a
  la nube desde acá.
- **No corrí `npm run build`**: `vercel-dashboard` es HTML+JS plano, sin build
  step (`package.json` de 156 bytes, sin dependencias). No lo modifiqué: sólo lo
  leo.
- **Jamás mDNS**: no toqué nada de descubrimiento. No entré a
  `data/field_captures` (es de galgas, este trabajo ni pisa ese repo).

## Estado

- Branch `nocturno/local-2026-08-06-b-contrato-nube` pusheado (1 commit,
  `85dd9b8`: 4 archivos). datalogger volvió a `main` limpio.
- `QUE_FALTA.md` de datalogger: ítem **#14** + nota en el **#10** (en el branch).
- 4 repos intactos salvo el branch de trabajo.
- 🆕 **`C:\Proyectos\frioseguro` tiene trabajo de día NUEVO sin commitear**:
  `REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/` y un
  `FRIOSEGURO_SANTACRUZ_KIT.zip`. **No lo toqué ni lo commiteé** — no es trabajo
  mío, y el `.zip` en el repo probablemente no quiera versionarse. Matías:
  revisalo antes de que se mezcle con otra cosa.
- ℹ️ **`C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main`** (estado previo, no
  lo hice yo). **No lo cambié.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las siete
  noches anteriores: `agentes/{esquematico,pcb}.md`,
  `dominios/{comms,diseno,esquematico,firmware,hardware,logo_acceso_remoto,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md`,
  `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html`,
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué** — no es trabajo mío. Matías:
  commitealos, o la rutina cloud choca en el próximo `git pull`.
- ⚠️ **Queda el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota`**
  en galgas (0 commits; su contenido ya está adentro del branch del 08-06). No
  lo borré: `git branch -d` cuando Matías quiera.
- La cola de merge suma **44 branches** en origin (galgas 16, datalogger 14,
  frioseguro 13, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo
  y sin usar: falta la sesión humana.
  **Nota de prioridad:** de los 14 de datalogger, éste es el que **cambia lo que
  hay que probar antes del ítem #3 (ECO-LoRa)**. H2+H3 dicen que el canal por el
  que se manda `eco on` puede tragarse el comando y avisar que salió bien; si eso
  no se arregla primero, la primera prueba de ECO-LoRa que falle va a mandar a
  Matías a debuggear la radio, que es donde no está el problema.
