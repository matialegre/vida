# Nocturno local — 2026-08-16

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\cosechador` (convergencia **UNIVERSIDAD** —
prioridad #1— y el único repo donde un análisis todavía cambia una compra).
**Branch:** `nocturno/local-2026-08-16-cadena-medicion` (pusheado, `e7aea9e`).

## TL;DR

El cosechador se justifica con una palabra: **replicación**. El DoD del repo la
escribe explícita — *«métricas comparadas contra el paper»*. Los tres análisis
previos miran el sistema **por dentro**. Ninguno preguntó cómo se produce el
número que va del otro lado del signo igual.

**De las 5 métricas objetivo: 0 medibles, 2 con reservas, 3 no medibles** con el
instrumental y los procedimientos que el repo declara hoy. Y las **dos que el
DoD cita textualmente** —tiempo de carga y sleep— están entre las no medibles.

Tres números, sacados de los propios documentos:

- **El amperímetro se pone donde no están las cargas.** La métrica de sleep
  declara tres consumidores; el único procedimiento de medición escrito en todo
  el repo lo pone en serie **en la rama del Pro Mini**, y los otros dos cuelgan
  del mismo rail en paralelo. **Ve 1 de 3.**
- **Los «8,69 h» del paper no son un tiempo medido.** Son `3 V / 0,345 V/h`: la
  extrapolación lineal **×17,4** de un ensayo de 30 minutos en el que el banco
  subió **172 mV**. Con el modelo físico de un buck alimentado por potencia
  aproximadamente constante (`V(t)=V_ref·√(t/t_ref)`), el **mismo dato** da
  **151 h**. El objetivo «≤ 12 h» **aprueba con un modelo y reprueba con el
  otro**, y ningún documento dice cuál usa.
- **El objetivo de energía por TX es más chico que la estimación de diseño del
  propio repo**: ≤ 1 mJ contra 1,3 mJ. **Reprobada en el papel, antes de comprar
  nada.**

## Tarea elegida y por qué

Por rotación tocaba cosechador (los cinco turnos previos: galgas 08-13-b,
cosechador 08-14, frioseguro 08-14-b, datalogger 08-15, galgas 08-15-b — el más
viejo era éste).

Dentro del repo, todo el `QUE_FALTA` sigue bloqueado por la compra, y los tres
análisis previos ya cubrieron sus ejes:

| noche | qué modela | dónde empieza y termina |
|---|---|---|
| 07-18 `modelo-energia` | cuánta energía entra | dentro del emisor |
| 08-11-b `presupuesto-standby` | qué se pierde con la máquina parada | dentro del emisor |
| 08-14 `cadena-alarma` | hay fuego, ¿avisa alguien? | del sensor al buzzer |

La pregunta que ninguno contesta:

> El paper dice 0,75 µA y 8,69 h.
> **¿Con qué instrumento, en qué punto del circuito, contra qué referencia y con
> cuántas repeticiones se produce un número NUESTRO que se pueda poner al lado?**

Tres razones para elegirla esta noche:

1. **Es la convergencia declarada del repo con la uni, y es de medición.**
   `QUE_FALTA:19` mapea la caracterización a **Medidas Electrónicas 2**. Una
   materia de medidas cuyo proyecto tiene cinco métricas sin procedimiento es
   exactamente el trabajo que no se puede entregar.
2. **Sigue siendo el único repo donde un análisis cambia una compra, y esta vez
   agrega ítems al carrito en vez de sólo corregirlos.** Dos de los arreglos son
   instrumental que no está comprado ni listado.
3. **Es el otro extremo del 08-14.** Esa noche auditó si el sistema avisa. Ésta
   pregunta si, cuando funcione, vamos a poder **demostrar** que funcionó como
   el paper.

## Qué hice

**`analisis/measurement_chain.py`** (stdlib, sólo lectura, sin red ni hardware,
no compila nada). **No inventa números: los LEE** de `PROGRESS.md`,
`CHANGELOG.md`, `DECISIONS.md`, `QUE_FALTA.md`, `docs/architecture.md` y
`docs/setup-completo.md`, y cita `archivo:línea` de cada afirmación. Exit
0/1/2/3, `--json`, `--detail`, `--fail-on`, `--root`.

**Tres oráculos** que demuestran los hallazgos en vez de afirmarlos:

- `--demo-metricas` recorre **las 5 métricas** y marca cada una *medible /
  con reservas / NO MEDIBLE*, con su procedimiento (si existe) y los hallazgos
  que la afectan. Resultado: **0 / 2 / 3**.
- `--demo-extrapolacion` toma la Tabla 6 del paper y muestra, para los tres
  diseños, **qué se midió de verdad** (53, 172 y 118 mV en 30 min) y qué da cada
  modelo: lineal (28,3 / 8,7 / 12,7 h) contra potencia constante (1602 / 151 /
  320 h). Y en qué fila se da vuelta el veredicto contra el objetivo del repo.
- `--demo-amperimetro` pone el procedimiento escrito al lado del objeto de
  medida que la métrica declara, y cuenta cuántas cargas ve el instrumento
  (**1 de 3**). Después chequea las dos exigencias del ensayo por separado.

**`analisis/test_measurement_chain.py` — 146 tests en 7 capas:** utilidades de
texto, física de la medición, extractores sobre fuentes sintéticas, los tres
oráculos con números fijados, **control negativo** (un repo sintético sano no
enciende nada) con un defecto inyectado por vez que enciende **exactamente** su
código, la capa «no salta cuando no corresponde», y regresión sobre el repo real
+ CLI.

**`docs/cadena-medicion.md`** — el análisis completo, el orden de arreglo y las
premisas externas declaradas una por una.

### Lo que hubo que resolver

- **Un paso de markdown envuelto en dos líneas es un solo paso.** El
  procedimiento de medición del repo nombra el punto de medida en su **segunda**
  línea (`setup:334`). Leyendo sólo la primera, M1 reportaba *«ve 0 de 3»*
  cuando la verdad es **1 de 3**. Un hallazgo **exagerado** es tan inservible
  como uno perdido: el que lo va a arreglar abre el archivo, ve que el Pro Mini
  sí está nombrado, y deja de creerle al resto del informe. Ahora los items se
  arman uniendo continuaciones y sub-viñetas. Hay test, y la mutación que lo
  deshace mata la suite.
- **El diagrama de bloques es arte ASCII en COLUMNAS.** Una sola línea de texto
  atraviesa los tres bloques del emisor, así que `Active:` del MCU y `TX pico:`
  de la radio **caen en la misma línea**. Mi primer extractor leía «4 mA» como
  el pico de TX del NRF24 — la corriente del vecino. Las corrientes ahora salen
  de la **tabla** de balance energético y de la **prosa** de los gotchas, nunca
  del diagrama.
- **El nombre de una métrica contiene el nombre de otra.** La métrica de sleep
  se llama *«Consumo sleep (Pro Mini + flame sensor + NRF24L01 idle)»*: buscar
  «flame» devuelve **esa** fila, y la métrica del sensor de llama se queda sin
  dueño. **M8 desaparecía en silencio.** Ahora cada fila se asigna una sola vez,
  de la más específica a la más genérica. Es la misma clase de falla que el
  forward contado como pull del 08-15-b: el hallazgo no sale mal, sale **cero**.
- **Un DoD truncado elige el diseño equivocado.** `parse_dod` leía la primera
  línea; el dato que dice **contra qué diseño del paper** se compara («design
  2») puede caer en la segunda. Con el DoD cortado, el análisis compara contra
  otro diseño y no avisa. Ahora junta el párrafo.
- **Mi propio titular de M2 estaba medio equivocado, y lo dijo el oráculo.**
  Había escrito que el DMM «no resuelve» los microamperes. Falso: a 0,1 µA por
  cuenta, separar 0,75 de 5 µA le sobra. Lo que **no** puede es cubrir el rango
  dinámico del **ensayo** — el nodo arranca a través del amperímetro y despierto
  pide 5 mA, que son 25× el fondo de escala y 500 mV de caída. Reescribí el
  hallazgo, y el oráculo ahora **imprime «alcanza»** en la línea de resolución:
  la herramienta dice la verdad aunque debilite mi titular.
- **A5 del 08-14 me enseñó a ponerle umbral a los adjetivos, y acá hice al
  revés y estuvo mal.** Mi primera versión de M6 disparaba con «el criterio no
  tiene número», y eso también castiga a las Fases 4 y 5, que son ensayos
  **funcionales** donde un número no corresponde. Quedó acotado a la única fase
  que alimenta una métrica **cuantitativa** de la tabla.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **5 error · 3 warn · 3 info.**

| código | sev | dueño | qué |
|---|---|---|---|
| **M1** | error | @energia | **El amperímetro se pone donde no están las cargas que la métrica nombra.** `PROGRESS:111` declara *Pro Mini + flame sensor + NRF24L01 idle*; `setup:333` manda ponerlo «en serie entre VOUT y VCC del Pro Mini». Los otros dos cuelgan del mismo rail, **aguas arriba**. Ve **1 de 3**. *(No es S2 del 08-11-b, que discute cuál corriente decide la autonomía: es que el procedimiento no mide ni lo que su propia métrica declara.)* |
| **M2** | error | @energia | **El instrumental no cubre el rango dinámico del propio ensayo.** Único instrumento de corriente imprescindible: un DMM de mano (`setup:19`). **La resolución alcanza** para el objetivo de 5 µA. Lo que falla es que el mismo amperímetro tiene que dejar arrancar un nodo que despierto pide **5 mA**: **25× el fondo de escala** del rango µA y **500 mV** de caída sobre un rail que sólo tiene 2,7-3,3 V. O el nodo no arranca, o el operario cambia de rango — y cambiar de rango abre el circuito, resetea el MCU y devuelve el consumo de otro estado. |
| **M3** | error | @energia | **La métrica de energía por TX no tiene instrumento y ya está reprobada.** Objetivo ≤ 1 mJ (`PROGRESS:112`) contra 1,3 mJ de diseño (`architecture:108`). Y medirla es integrar **33 ms**: la ventana de min/máx de un DMM (~100 ms) es 3× más larga, y el osciloscopio está declarado **opcional** (`setup:21`). |
| **M4** | error | @energia | **El número contra el que se compara la carga no es un tiempo medido.** `3 V / 0,345 V/h = 8,70 h`: el tiempo declarado **es** la división de un ensayo de 30 min que subió **172 mV**. Extrapolar lineal supone corriente constante; detrás de un buck lo ~constante es la **potencia** → **151 h**. El objetivo ≤ 12 h aprueba con un modelo y reprueba con el otro. |
| **M5** | error | @hardware | **El DoD depende de una medición que el propio manual declara imposible.** No hay **excitador de vibración** ni **acelerómetro** en herramientas ni en el BOM, y `setup:312` ya admite que *«no es comparable directo al paper sin set-up de vibración mecánica controlada»* — pero el DoD (`QUE_FALTA:6`) y la tabla de métricas lo siguen pidiendo igual. |
| **M6** | warn | @energia | **La Fase 2 no puede aprobar ni reprobar.** Criterio cualitativo («sube monotónicamente») alimentando una métrica que es un tiempo. Con las tasas del paper, unos minutos de vibración **a mano** dan **decenas de mV** sobre 10 F: el orden de la relajación dieléctrica del propio supercap. |
| **M7** | warn | @comms | **El «margen» del alcance RF no tiene observable.** El ensayo es binario, y con auto-ACK y hasta **15 reintentos** (`architecture:190`) un enlace al borde suena **igual** que uno sano. El dato que los separa existe y es gratis (contador ARC de `OBSERVE_TX`, o entregas sobre N paquetes) y no lo pide ninguna fase. |
| **M8** | warn | @hardware | **La sensibilidad del sensor de llama es un ajuste, no una propiedad.** «≥ 30 cm» no dice qué llama —el repo nombra **dos fuentes distintas**, vela (`PROGRESS:80`) y encendedor (`setup:343`)—, ni con qué luz ambiente, ni con el potenciómetro de umbral del módulo en qué posición. |
| **M9** | info | @comms | **La energía por TX se compara contra una radio que el paper no declara** (`CHANGELOG:46`: «Módulo RF (no especificado…)»). Comparar mJ/TX entre dos radios que pueden no ser la misma mide qué radio se eligió, no replicación. *(Distinto de A7 del 08-14, que es el desacuerdo interno 15 vs 12 mA.)* |
| **M10** | info | @esquematico | **El banco no es el del paper, y no pesa igual en las dos métricas.** Para la **carga** da igual (misma capacidad efectiva); para el **sleep** no: el balanceo de D3 es un consumo permanente que el montaje del paper no tenía. Las dos dicen «contra el paper» con dos grados de comparabilidad. |
| **M11** | info | @cronista | **4 de 5 métricas no tienen procedimiento escrito.** La tabla dice qué y cuánto; nunca con qué, dónde, contra qué ni cuántas veces. Las cinco figuran «No medido» desde el 2026-05-20. |

**Orden sugerido:**

1. **M5 y M2 primero, porque son de la lista de compras y no se compró nada.**
   Un shunt calibrado (o uCurrent/SMU) y una forma de excitar el piezo a
   amplitud conocida con un acelerómetro que la verifique. Comprarlos después
   es otro envío y otras tres semanas.
2. **M4 — decidir y escribir el modelo de extrapolación.** Es gratis y define si
   el ensayo de carga es de una noche o de una semana.
3. **M1** — el nodo se mide en el **borne del banco**, no en la rama del MCU.
4. **M3** — o el objetivo sube a ≥ 1,3 mJ, o se aclara que se mide con
   osciloscopio. Hoy no se puede cumplir aunque el diseño sea perfecto.
5. **M11** — una columna «cómo» en la tabla. Lo más barato del informe.
6. **M6, M7, M8** — ponerle un número a tres adjetivos.
7. **M9, M10** — dos aclaraciones de comparabilidad.

## Lo que está BIEN (fijado por test, para no ir a revisarlo)

- **La Tabla 5 del paper es coherente consigo misma**: `8 mA × 3,0 V × 33 ms =
  0,79 mJ`. La transcripción del dato de referencia está bien.
- **La Tabla 6 también**: las tres filas cumplen `3 V / Tchr = tiempo declarado`
  a menos del 5 %. El problema de M4 no es la aritmética, es el **modelo**.
- **La Fase 1 sí tiene criterio numérico** (`VOUT ≥ 3,0 V`): el repo sabe
  escribir un criterio verificable. M6 es una omisión, no una costumbre.
- **El repo ya admite por escrito el problema de la vibración** (`setup:312`).
  M5 no descubre nada nuevo: descubre que esa admisión **nunca subió al DoD**.
- **La única métrica con procedimiento es la de sleep** — la que M1 y M2
  desarman. Corregirla es corregir el ejemplo que van a copiar las otras cuatro.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\cosechador
git checkout nocturno/local-2026-08-16-cadena-medicion

python analisis/measurement_chain.py                       # informe; exit 3
python analisis/measurement_chain.py --detail              # + evidencia archivo:linea
python analisis/measurement_chain.py --demo-metricas       # las 5, una por una
python analisis/measurement_chain.py --demo-extrapolacion  # de donde salen las 8.69 h
python analisis/measurement_chain.py --demo-amperimetro    # que ve el instrumento
python analisis/measurement_chain.py --json

cd analisis && python -m unittest test_measurement_chain   # -> Ran 146 tests, OK
```

Cuatro hallazgos se comprueban **sin la herramienta**, con la calculadora y dos
`grep`:

```bash
# M4: 3 / 0.345 = 8.70 h  vs  0.5 * (3/0.1725)^2 = 151 h
grep -n "8.69 h" CHANGELOG.md
# M3: el objetivo es mas chico que la estimacion de diseno
grep -n "≤ 1 mJ" PROGRESS.md ; grep -n "1.3 mJ" docs/architecture.md
# M5: cero hits
grep -n "shaker\|acelerómetro\|excitador" docs/setup-completo.md
# M7: cero hits
grep -rn "RSSI\|OBSERVE_TX\|paquetes perdidos" .
```

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **146 tests en verde** (3,7 s). Sin descargas ni toolchains: cero riesgo de
  timeout.
- **Control negativo real:** un repo sintético sano no enciende **nada** (exit
  0, las 5 métricas medibles), y cada defecto inyectado por separado enciende
  **exactamente** el código esperado. Los once tienen además su test «no salta
  cuando no corresponde».
- **Verificado por mutación — 18 mutaciones, las 18 hacen fallar la suite:**
  el paso sin unir su continuación · el DoD truncado a la primera línea ·
  `pick_metric` sin exclusión de filas · `number_with_unit` sin lookahead
  (`mAh` contando como `mA`) · la Tabla 6 leída por los dos primeros números ·
  `power_time_to` lineal en vez de cuadrática · exit code con la severidad menos
  grave · M1 sin exigir que la carga cuelgue del mismo rail · el rango dinámico
  de una sola década · M3 sin el término objetivo-menor-que-diseño · M4 sin
  verificar que el tiempo declarado **es** la división · M5 sin mirar el BOM ·
  M6 sin exigir umbral · M7 sin mirar si alguien pide calidad de enlace · M8 con
  `or` en vez de `and` · M11 conformándose con un keyword · el pico de TX leído
  del diagrama ASCII · toda herramienta contada como imprescindible.
  *(La primera pasada dejó **una viva**, y era **un test flojo mío**: el test del
  arte ASCII agregaba el diagrama a `architecture.md` mientras el extractor lee
  `setup-completo.md` — no podía fallar nunca. Lo reescribí como contrato
  directo sobre `parse_nrf_tx_ma` y ahora muerde. El andamio de mutación fue
  descartable, en `/tmp`: **no se commiteó**. Borré el `__pycache__` antes de
  cada corrida y restauré el archivo al final; `git status` quedó limpio.)*
- **No se tocó ninguna decisión de compra, ni el BOM, ni el paper, ni los PDFs.**
  El branch agrega 4 archivos (incluido `.gitignore`) y edita `QUE_FALTA.md` y
  `PROGRESS.md`. No hay firmware ni dashboard que compilar: el repo no tiene
  código de producción.

## Qué quedó sin verificar

- **Todo sale de leer documentos, no de medir un sistema.** No hay sistema: nada
  está comprado. Los oráculos demuestran el efecto de lo que el repo *dice*.
- **M2 se apoya en dos premisas externas declaradas como constantes con
  nombre:** el shunt del rango µA (100 Ω) y su fondo de escala (200 µA). **Se
  cierran leyendo el manual del multímetro que ya está en el cajón.** Si el
  shunt real fuera de 10 Ω, la caída baja a 50 mV y el hallazgo se debilita —
  **el sobrerrango de 25× no depende de ninguna de las dos.**
- **El modelo de potencia constante de M4 es un modelo, no una medición.** No
  afirmo que las 151 h sean el número correcto. El hallazgo es que **hay dos
  modelos plausibles que difieren 17× y el repo no dice cuál usa**; sobrevive
  aunque el paper tenga razón.
- **`DMM_MINMAX_WINDOW_MS = 100`** es un valor típico. Si el multímetro real
  captura en 1 ms, M3 pierde su segunda mitad — la primera (objetivo menor que
  el diseño) es aritmética y se sostiene sola.
- **M8 supone que el módulo de sensor de llama trae potenciómetro de umbral en
  la salida digital.** Es lo normal en esos módulos, pero **el SKU sigue sin
  elegir** — es el mismo hueco que S6 (08-11-b) y A1 (08-14). **Al elegirlo hay
  ahora tres cosas para anotar juntas: rango de alimentación, consumo en reposo
  y si el umbral es ajustable.**
- **La verificación de mayor valor es de día y no cuesta nada:** abrir el manual
  del multímetro y mirar el rango de µA. Con ese dato, M2 queda cerrado o
  reducido sin discusión.
- **Ningún fix aplicado** — generator ≠ evaluator. Ni siquiera M11, que es una
  columna en una tabla: el que escribe el «cómo» tiene que ser el que después lo
  ejecuta.

## Estado

- Branch `nocturno/local-2026-08-16-cadena-medicion` pusheado (`e7aea9e`), sale
  de `main` (`388795b`). **cosechador volvió a `main` limpio.**
- `QUE_FALTA.md` y `PROGRESS.md` del repo actualizados **dentro del branch**.
  ⚠️ **Conflicto anunciado (el mismo de siempre en este repo):** los branches
  del **08-11-b** y del **08-14** agregan una sección con el **mismo encabezado**
  (`## Análisis offline hecho…`) en `QUE_FALTA.md`. Usé el encabezado
  textualmente igual **a propósito**: al mergear se conserva un solo encabezado
  y **los tres bloques**, uno abajo del otro. En `PROGRESS.md` mi bloque va
  pegado a la tabla de métricas; los otros dos escriben en `## Anda ✅` y en la
  misma tabla — conflicto trivial de contexto.
  ⚠️ También agregué `.gitignore`, igual que los branches del 07-18 y del
  08-11-b: **tercer conflicto trivial** en ese archivo (contenido idéntico).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Decimoctava noche que lo reporto**: es firmware que va a un equipo a 2000 km
  y vive **sólo en este disco**. **No lo toqué.**
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día SIN COMMITEAR**
  (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`, los dos tests del nodo GIMAP,
  `docs/ARMADO_NODO_GIMAP.html`, `.gitignore`). **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  veintitrés noches anteriores: `agentes/`, `dominios/`, `enlace/`, más
  `agentes/diseno3d.md`, `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html` y
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío. El único
  `enlace\maquinas\*.estado.json` (DESKTOP-RK8DH7C) sigue con `ultima_vez_viva`
  del **2026-08-07**: el latido está parado hace **9 días**. **No lo toqué** (los
  scripts de ENLACE son trabajo de día sin commitear).
- La cola de merge suma **61 branches** en origin (galgas **21**, datalogger 18,
  frioseguro 18, cosechador **4**).
  **Nota de prioridad, otra vez:** los **4 de cosechador siguen siendo los más
  baratos de mergear de toda la cola** — el repo no tiene firmware, ni nube, ni
  dashboard: no hay nada que romper. Y son los únicos cuyos hallazgos **todavía
  pueden cambiar una compra**. Con el de esta noche son **dos ítems nuevos** que
  entran al carrito, no sólo correcciones.

## Para @energia / @hardware / @comms / @esquematico / @cronista / @verificador

- **@energia: M4 es tuyo y es el que ordena todo lo demás.** Hasta que no esté
  escrito si la carga se extrapola lineal o por potencia, no se puede planificar
  el ensayo (¿una noche o una semana de banco vibrando?) ni juzgar el resultado.
  Después **M1** (una línea: el nodo se mide en el borne del banco) y **M2**
  (que es un ítem de compra, no un cálculo). Ojo con M3: **el objetivo de mJ por
  TX está por debajo de tu propia estimación de diseño** — uno de los dos
  números está mal y hay que elegir cuál.
- **@hardware: M5 es tuyo y es la compra.** El carrito suma **dos ítems** que
  hoy no están en ningún lado: un **shunt calibrado** (o uCurrent/SMU) y una
  forma de **excitar el piezo a amplitud conocida con acelerómetro**. Sin ellos,
  dos de las cinco métricas no se cierran nunca. Y el **SKU del sensor de llama**
  ya acumula **tres** requisitos para anotar juntos: rango de alimentación (A1,
  08-14), consumo en reposo (S6, 08-11-b) y **umbral ajustable** (M8, esta
  noche).
- **@comms: M7 es tuyo y sale casi gratis.** Pedir el contador de reintentos en
  la Fase 5 convierte un ensayo binario en una medida con margen — y es el
  mismo dato que A5 del 08-14 te pedía usar para decidir qué hace el emisor
  cuando el ACK no llega. **Un solo cambio cierra los dos.**
- **@esquematico: M10.** Dejar dicho en qué se parece y en qué no el banco al del
  paper. Se cruza con D3, que S3 (08-11-b) ya pidió rehacer: aprovechá el mismo
  pase.
- **@cronista: M11.** Una columna «cómo» en la tabla de métricas objetivo de
  `PROGRESS.md`. Es la corrección más barata del informe y la que hace
  verificables a las otras. Y de paso: la tabla dice «Última actualización:
  2026-05-20» mientras el repo acumula cuatro análisis desde julio.
- **@verificador:** el DoD es *«cada métrica declarada tiene instrumento, punto
  de medida y referencia comparable, o está marcada como no medible»*. Los 146
  tests son el oráculo y `TestRepoReal` fija los 11 hallazgos. **Puntos a
  atacar, en orden:**
  1. **M2 es el que más se apoya en premisas externas** (shunt y fondo de escala
     del DMM). Se cierra leyendo el manual del multímetro que ya está en casa.
     El sobrerrango de 25× no depende de ninguna de las dos.
  2. **M4 es el más valioso y el más discutible a la vez.** Atacá el modelo de
     potencia constante — pero notá que el hallazgo sobrevive igual, porque su
     forma es *«hay dos modelos y no está dicho cuál»*, no *«el número correcto
     es 151 h»*.
  3. **M3 y M5 son los más sólidos**: uno es una desigualdad entre dos números
     del propio repo, el otro es un `grep` que da cero.
  4. **M6 y M8 son los más blandos**, y por eso están en warn: los dos se pueden
     defender como «se entiende igual».
  5. **Revisá que M1 no se pise con S2 del 08-11-b.** Están cerca a propósito y
     son distintos: S2 discute *cuál* corriente decide la autonomía; M1 dice que
     el procedimiento no mide ni lo que su propia métrica declara. Si te parece
     que son el mismo, el que sobra es M1.
