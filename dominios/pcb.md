# Dominio: pcb (agente @pcb)

Doc de dominio + bitacora. El agente lo lee al arrancar y lo actualiza al cerrar. Backlog inicial: ver seccion "Tu backlog inicial" en ~/.claude/agents/pcb.md (copia en ../agentes/pcb.md).

## Bitacora

## 2026-09-04 (e) — FRIOSEGURO / TERMOVIGIA **Mini LITE**: doble faz con DRC 0, y despues **dos cambios de reglas** que la frenaron a proposito

`C:\Proyectos\frioseguro\hardware\mini_lite\` — `LAYOUT_LITE.md` (estado completo),
`termovigia_mini_lite.kicad_pcb`, `drc.txt`, `salida\` (2D top/bottom, 3D top/bottom, **los 3
PDF de fabricacion casera**, `verificacion.json`), toolchain en `pcb\`. **Sin commit.** La
placa doble faz queda archivada como referencia en `doble_faz_descartada\`.

**Lo que se hizo y quedo medido (placa doble faz 110 x 80, terminada):** 47/47 componentes,
46 redes, 95 segmentos F.Cu + 87 B.Cu + 112 vias. `kicad-cli pcb drc --severity-all`:
**0 violaciones / 0 objetos sin conectar** (el reporte no tiene una sola linea).
`chequear_solapes.py` **0 solapes**; `verificar.py` **0 fallos / 0 avisos**. Renders 2D y 3D
**mirados** y corregidos en 8 iteraciones (de 145 violaciones de serigrafia a 0).

**Los cinco hallazgos que @verificador rechazo en la Mini, cerrados con numero:**
1. **A1 la hace cumplir el DRC, no un rectangulo dibujado.** Netclase **CAMPO** con las 3
   redes de campo + un `termovigia_mini_lite.kicad_dru` propio con la regla de clearance de
   6,0 mm entre CAMPO y todo lo demas (y la misma en `hole_clearance`). Eso cubre **pads,
   pistas, vias Y relleno**, que era exactamente lo que fallaba en H-01. La barrera
   geometrica ademas es una **"L"** (vertical entre las filas del DIP + horizontal por
   debajo) que ENCIERRA el campo contra los dos bordes de placa. **Medido: 6,22 mm en F.Cu
   y 6,22 en B.Cu**, y lo que limita es el pad del propio PC817, no el layout.
2. **Keepouts de agujero radio 3,60** (1,60 de taladro + 2,00 de guarda): prohiben relleno,
   pistas Y vias. Peor caso medido **1,93 mm del borde del agujero** = 3,53 del centro,
   contra una arandela M3 de 3,50. Los 8 verificados uno por uno.
3. **Centros de COMPONENTE, no de pad** (`centro_sw()`, `centro_led()`), publicados en
   `LAYOUT_LITE §3` + `verificacion.json`. El USB queda **1,64 mm adentro** del borde: se
   dice, no se declara "al ras".
4. **Paso de bornera 5,00 medido en la placa: error 0,000 mm**, y los bloques abutados
   tambien 0,000. En la serigrafia y en el LEEME.
5. **Desviaciones .net <-> placa**: `verificar.py` compara valor Y huella de los 47
   componentes contra el `.net`. **Cero.**
6. **L1** ya no se decide con una lista negra de subcadenas (H-14) sino con una **tabla de
   alturas por huella** (`ALTURA_MM`), y el chequeo **falla si una huella no declara altura**.

**Dato nuevo de @diseno3d absorbido:** el modulo de rele saca el cable de carga por su borde
de borneras, asi que el modulo se **giro 90 grados** para que ese lado mire al borde
DERECHO, el unico borde entero sin conectores; serigrafia `BORNERAS DE CARGA ->` con flecha.

**Por que 100 x 80 no cerraba** (el registro que pidio el Director, medido con courtyards
reales): borneras del borde izquierdo 13,0 + zocalo del DevKit 32,0 + modulo de rele 39,0 +
5,0 de aire = **89,0 mm**; en los 11 que sobraban tenian que entrar la zona A1 (23 de campo
+ 6,22 de creepage = **29,2**) y el M3 de esa esquina. **Faltaban ~18 mm de ancho.**

### Los dos cambios de reglas (por eso esta FRENADA, no abandonada)
- **La LITE no va a JLCPCB: la fabrican Matias, Gonza y Sergio en casa, con acido.** Eso
  invalida la doble faz entera: sin metalizado, las **112 vias** serian 112 remaches.
  Medicion que justifica REHACER en vez de convertir: `pcb/puentes.py` sobre este board dice
  que pasar ESTE placement a una sola cara costaria **30 puentes, 621 mm de alambre, el mas
  largo de 137 mm**.
- **Matias simplifico el circuito**: se va la entrada de defrost (opto, bornera y **toda la
  barrera A1**) y las puertas pasan a **una sola bornera de 5 vias**. @esquematico esta
  rehaciendo el `.net`; rutear el viejo con las reglas nuevas era trabajo perdido dos veces.

### Lo que se adelanto, que NO depende del netlist (corrido y mirado)
**`pcb/artwork.py`** — artwork **1:1** para fabricacion casera, dibujado desde el board (el
B&W de `kicad-cli` sale invertido): `artwork_cobre_espejado.pdf` (el que se plancha),
`artwork_cobre_directo.pdf` y `hoja_armado.pdf` (**reemplaza a la serigrafia**: courtyards,
referencias, los rotulos de la placa y los puentes en rojo punteado). Tiene lo que el export
no da: huecos del relleno bien restados (sin eso el plano sale macizo y la placa es un
corto), **marca de centrado en cada pad**, **marcas de registro** en las 4 esquinas, el
contorno **con los arcos** de las esquinas redondeadas, y **DOS reglas de 50 mm, una en X y
otra en Y** — una laser puede escalar distinto en cada eje por el arrastre del papel y con
una sola regla eso no se ve.
**Se auto-verifica**: reabre el PDF que acaba de escribir y MIDE. Corrida de hoy:
`regla X = 50,000 mm OK` y `borde mas largo = 104,000 mm` (= 110 - 2 x 3 de radio, exacto).
Mas `pcb/taladros.py` (tabla por mecha: cambiar de mecha es lo que mas rompe brocas de 0,8)
y `pcb/puentes.py` (cadenas de alambre con largo y extremos), **portados de galgas rev E.2 —
la regla de biblioteca funciono: el problema ya estaba resuelto y solo hubo que adaptarlo**.

### Reglas de la placa nueva, ya acordadas (LAYOUT_LITE §4)
1 cara (cobre en B.Cu) · **0 vias** · pista 0,5 senal / 1,0-1,5 alimentacion · aislacion 0,5
(relleno 0,6) · **pad 2,6 mm** con taladro 0,9-1,3 · **pad 2,0 en paso 2,54** (desviacion
DECLARADA: a 2,54 un pad de 2,6 se toca con el vecino; 2,0 deja 0,54 de aire) · sin mascara
ni serigrafia · envolvente de arranque **140 x 95** (entra en una virgen de 10 x 15 con
margen de corte).
**Consecuencia geometrica que hay que aceptar de entrada:** con pads de 2,0 y 0,5 de aire,
**entre dos pines a 2,54 NO PASA NINGUNA PISTA** (harian falta 1,5 y hay 0,54): el canal
entre las dos filas del zocalo **deja de ser un atajo** y hay que sacar de ahi todo lo que
hoy vive adentro.
**Topologia ya razonada para una cara:** las dos filas del DevKit parten la placa en dos
mundos y el reparto sale solo (columna A -> rele y alimentacion; columna B -> sondas,
puertas y panel), **sin un solo ramal cruzando**; las 6 sondas en un mismo borde con
**`/VSONDAS` por la franja que queda ENTRE los pads de las borneras y el borde de placa** y
`/1WIRE_BUS` por encima de los cuerpos, asi **los dos buses nunca se cruzan y no cuestan un
puente**; y RESET y BOOT **no van a quedar juntos**, a proposito (EN e IO0 estan en extremos
opuestos: juntarlos costaba dos puentes largos cruzando los buses de sonda).

### Trampas nuevas del harness (KiCad 10 + Python)
1. **`fp.Remove()` / `fp.Add()` degradan el handle de la huella a `SwigPyObject` pelado** y a
   veces tambien el del board: despues de eso `fp.Pads()`, `fp.GetPosition()` y hasta
   `board.Footprints()` explotan. Por eso `contornos.py` corre en **proceso propio y UNA
   huella por corrida** (11 procesos cortos). Y el origen de la huella no se pide con
   `GetPosition()`: se calcula del placement.
2. **Las formas que se agregan a una huella van en coordenadas ABSOLUTAS** (KiCad no las gira
   ni las traslada): hay que transformar cada esquina a mano.
3. **El courtyard de catalogo del MX126 mide 15,5 mm para 3 posiciones** (incluye la cola de
   encastre) pero el bloque mide n x 5,00 y esta HECHO para abutarse: con el contorno de
   catalogo, dos bloques pegados dan errores de patios y de serigrafia que no son errores.
   Se redibujan courtyard y silk al cuerpo real.
4. **`fitz` (PyMuPDF) existe en el Python de KiCad**: el artwork corre con el mismo
   interprete que `pcbnew` y no hace falta el puente de dos procesos que hubo que armar en
   galgas.

**Proximo paso:** llega el `.net` nuevo -> rehacer `placement.py` (no convertir) con las
reglas de acido -> rutear a mano los buses y el riel de 5 V con el A* forzado a una capa ->
minimizar puentes (meta: un digito) -> DRC 0 con 0,5/0,5 -> los 3 PDF mirados -> actualizar
los centros para @diseno3d, **que cambian y con ellos el gabinete**.
**Sigue bloqueando:** M1-M5 (DevKit y modulo de rele) siguen estimadas, en `../mini/comun.py`.

## 2026-09-04 — @verificador sobre TERMOVIGIA Mini rev A: **RECHAZADO** (14 hallazgos)

Informe completo: `C:\Proyectos\frioseguro\hardware\mini\VERIFICACION_LAYOUT_2026-09-04.md`.
Auditoría adversarial del layout de @pcb. Todo medido con pcbnew de KiCad 10 sobre el
`.kicad_pcb`, no leído de la doc. DRC re-corrido por el verificador: **0 violaciones, 0
desconectados** — reproducible; lo que se discute es su alcance. Sin commit, sin correcciones.

**Veredicto: RECHAZADO.** No es "APTO tras medir M2-M5": hay 2 defectos de diseño que no son
M2-M5, una cota mal entregada al gabinete, y un bloqueante mecánico del peso de M2 sin declarar.

**Bloqueantes (dueño):**
1. **H-01 CRÍTICO — la barrera de aislación no existe en la bornera. (@pcb)** `§2.3` declara
   creepage 6,02 mm y "lado campo sin plano de masa", pero `CAMPO_DEFROST` arranca en **x = 11,20**
   y `J11`/`J12` están en **x = 5,40**: los pads de 12-24 V quedan a **0,300 mm del relleno de GND,
   en las DOS capas** (medido en (6,45 , 77,30), red `Net-(J12-Pin_1)`). Por el criterio del propio
   `§2.3` (IPC-2221, 2,50 mm para 311 V) falla 8x. `J1.2` (GND de 5 V) a 4,03 mm del cobre de
   campo. Se ve en `pcb_top.png`/`pcb_bottom.png`: el keepout blanco no llega a la bornera.
2. **H-02 ALTO — `/DOOR4` (B.Cu) a 1,85 mm del centro de `H5`** = 0,25 mm del borde del agujero, y
   `+5V` a 2,70 mm. Los 8 keepouts de agujero prohíben **sólo relleno** (`tracks=False`,
   `vias=False`). Una arandela/tuerca M3 del módulo pisa la pista. **(@pcb)**
3. **H-03 ALTO — `§6` le da a @diseno3d los pulsadores mal por 3,25 X / 2,25 Y.** `verificar.py:89`
   usa `pad["SW1.1"]` y `SW_PUSH_6mm` tiene **dos pads numerados 1**: publica el último (76,5) en
   vez del centro del actuador (**73,25 , 95,85**). Idem SW2 (88,5 vs **85,25 , 95,85**). Un
   agujero de tapa ahí no toca el vástago. **(@pcb → @diseno3d)**
4. **H-04 ALTO — paso de bornera 5,08 vs 5,00, sin declarar.** `BOM_CERRO_MORO §5.3.1` pidió
   textualmente pasar a 5,00 **"antes de rutear"** y `J2`/`J3` como 3x3 apilables; la placa tiene
   13 borneras MKDS **5,08** y bloques de **9 vías de una pieza**. 9 vías a 5,08 vs 5,00 acumulan
   0,64 mm: no entra. **No está en `§9`, ni en el LEEME, ni en la serigrafía.** Es el mismo error
   del perfboard, tercera vez. **(@esquematico + @hardware)**
5. **H-05 ALTO — la desviación `.net` vs placa no está cerrada.** `§5` la declara en prosa, pero el
   `.net`, el campo `Value` de la placa, `gerbers/termovigia_mini_bom.csv` (**cant. 5, DO-15,
   columna `Poblar` VACÍA**) y `_pos.csv` dicen todos `P6KE6.8CA` DO-15. Quien compre por el BOM
   generado compra 5 TVS que no existen en AR y puebla `D2`, que rompe el bus a 25 m. Atenuante:
   los CSV **no** viajan dentro del ZIP. **(@esquematico + @pcb)**

**Sobre M2 (H-07, MEDIO):** el plan "5 líneas" no cierra. Simulado con courtyards reales: para
**M2 <= 16 mm** (variante tiras juntas) **`R12` y `R13` chocan con `J8`**, porque están fijados como
offsets constantes de `TIRA_B_X` en `placement.py:111-112`. Se rehace el bloque G entero + el
fan-out de `+5V`/`+3V3`/`GND`/`/RELAY1`/`/RELAY2`: medio día.
**Mitigación más barata, en orden: (1) comprar el módulo AHORA y medirlo** — el mismo argumento
que `BOM §5.3.3` hizo para el ESP32, elimina M2-M5 de una; (2) **doble juego de pads de zócalo,
poblando uno solo** (bajo el módulo hoy sólo hay `J8`,`J9`,`R12`,`R13`,`H5-H8`: sobra lugar; NO
poblar los dos o el módulo se hamaca); (3) **sacar `H5-H8` del camino crítico** — el módulo cuelga
del cabezal (lo dice el `.scad`), así que M4 deja de bloquear y de paso desaparece H-02.
Con (2)+(3) el bloqueo baja de {M2,M3,M4,M5} a {M3}.

**Otros:** H-06 la tabla DFM `§7` tiene 3 filas falsas (hay 12 vías de **0,60/0,30** con anillo
0,150 y no 0,80/0,40; taladro mínimo real **0,75** en `Q1`, no 0,80; y el proyecto bajó
`min_via_diameter/annular/through_hole` a la medida del board). H-08 el riel de `+5V` de 2,0 mm
pasa a **0,254 mm** del pad de GPIO4 (`U1.32`) — distancia más chica de la placa, en un pad que se
suelda a mano: un pelo de estaño = 5 V en un GPIO de 3V3. H-09 5 leyendas bajo cuerpo de
componente (refdes `J5` bajo `R3`, `R2` bajo `J3`, `LED1` bajo `D1`). H-10 el gabinete de
`gabinete/` está dimensionado para **100 x 80** y sin agujeros de pulsador: los STL son anteriores
al layout. H-11 `D2` DNP deja 2 pads Ø2,40 desnudos (uno es el bus; a 10,16 mm, no se puentea solo,
pero es entrada de ESD/condensación). H-12 los SMA son **bidireccionales** y la silk les dibuja
cátodo. H-13 dique de máscara 0,22 mm en `Q1` con el chequeo apagado
(`solder_mask_min_width = 0`). H-14 `chequear_solapes.py` decide "alto" con una lista negra de 9
subcadenas, y `RELE_W/RELE_H = 50x39` es un **sexto número estimado que no está en M1-M5** (en
plaza hay 50,6x38,8 y 50,0x41,0; `C1` tiene sólo 2,21 mm de margen).

**Lo que aguantó y hay que decirlo:** DRC 0 reproducible · **0 islas de masa flotantes** (las 7
sospechosas cuelgan de `U2.3`/`U3.3`/`C1.2`) · retorno de 1-Wire y puertas **continuo** hasta
`U1.14` (misma isla, 136 conex. en F.Cu / 161 en B.Cu) · el canal del 1-Wire entre pads del zócalo
da **0,37 mm** exactos y va **bajo máscara**, así que el riesgo de puente a mano ahí es bajo ·
**0 pistas y 0 vías de campo cruzan la barrera** (x máx de campo = 30,00 contra barrera en 31,30) y
creepage bajo el opto = 6,02 mm confirmado · keepout de antena limpio en 2 capas · nada más alto de
8 mm bajo el módulo, verificado uno por uno · **el TVS recibe la señal antes que la R serie** en
los 4 canales (traza `J4.1 -> D5.1 -> ... -> R4.1`) · ZIP con las 7 capas + drills + LEEME ·
serigrafía de armado completa y `JD-VCC` bien escrito. El trabajo de @pcb es sólido; lo que falla
es el borde, que es donde se pierden los proyectos que viajan 1.500 km.

**Nota para el harness:** dos evidencias resultaron no ser evidencia. `verificacion.json` publica
posiciones de **pad** como si fueran de componente (H-03), y `salida/pcb_3d.png` **no tiene modelo
3D ni del DevKit ni del módulo de relé** (son rectángulos vacíos), así que `§0` no puede citar los
renders para sostener la posición del USB — que además queda **2,34 mm adentro** del borde, no "al
ras" como dice `§6`.


## 2026-09-04 — FRIOSEGURO / TERMOVIGIA **Mini** rev A: placa completa, DRC 0, gerbers PRELIMINAR

`C:\Proyectosrioseguro\hardware\mini\` — `termovigia_mini.kicad_pcb`, `LAYOUT_MINI.md`,
`drc.txt`, `salida\` (2D top/bottom, 3D top/bottom, `.glb` 1,9 MB, `.step`, `verificacion.json`),
`gerbers\` + `termovigia_mini_gerbers_PRELIMINAR.zip` (17 archivos), toolchain en `pcb\`.
**Sin commit** (orden). Envolvente **120 x 100** confirmada por el Director y por @hardware
(200 mm no entra en ninguna caja de stock).

**Estado medido (no declarado):** 70/70 componentes, 53 redes, **208 segmentos F.Cu (1.333 mm) +
243 B.Cu (885 mm) + 193 vias**. `kicad-cli pcb drc --severity-all`: **0 violaciones / 0 objetos
sin conectar** — el reporte no tiene una sola linea. `chequear_solapes.py`: **0 solapes, nada
fuera del contorno**. `verificar.py` (nuevo, mide criterios y no fabricabilidad): **0 fallos,
0 avisos**. Renders 2D y 3D **mirados** y corregidos en 6 iteraciones.

### Lo que manda el placement (y no lo decide el DRC)
- **1-Wire corto de verdad**: GPIO4 es el **pad 32**, o sea la fila de ARRIBA del zocalo. El
  front-end se metio en la franja de 8 mm entre las borneras de sonda y el DevKit, y `/ONEWIRE`
  **sube por el canal entre las dos filas del zocalo**, entrando entre los pads 10 y 11 (pads
  achicados a 1,5 mm -> 1,04 mm de aire). **33 mm del GPIO al bus**, contra ~78 rodeando la placa.
- **Los dos buses de sonda no se cruzan**: DATO por F.Cu a y=7,8 **sin una sola via**; VSONDAS
  por encima a y=9,9 y **cada una de sus 6 bajadas salta por B.Cu**. Las vias van en el riel, no
  en el dato.
- **Barrera de aislacion = UNA recta**: U2 y U3 en el mismo eje x=30; rule area que prohibe
  relleno + pistas + vias en las dos capas, y **todo el lado campo sin plano de masa**. Medido
  sobre el board: **creepage borde-a-borde 6,02 mm**, 0 pistas adentro, 0 pads de logica del lado
  campo.
- **Antena del WROOM con keepout de verdad** (sin relleno, sin pistas, sin vias): se pudo prohibir
  tambien las pistas — al reves que en la Base v2 — porque todos los pads del zocalo estan en las
  dos filas exteriores y nadie necesita cruzar por debajo de la antena.
- **El bulk donde se pide la corriente**: C1 (1000 uF) a **11,1 mm de JD-VCC (J8.1)**, no en la
  entrada. El +5V llega a J8.1 **por el norte** y el +3V3 a J8.2 **por el sur**, para no cruzarse
  sobre el conector. C2 a 4,6 mm del pin 5V del DevKit.
- **Ancho por CAIDA, no por corriente**: +5V en **2,0 mm**. IPC-2221 daria 5,5 A y el pico son
  0,68 A; lo que manda es que el AMS1117 del DevKit tiene **280 mV de margen** y el camino
  J1 -> D1 -> C1 -> U1.19 mide **134,7 mm** (la diagonal de la placa, con la bornera de entrada en
  un borde y el pin 5V en la esquina opuesta). Medido: **22,2 mV**; con 1,0 mm serian 44.
- **Serigrafia que se ve con la placa armada**: el cuerpo de una bornera tapa la placa hasta
  y=10,75, asi que un rotulo "S1 / V D G" entre los pines **queda invisible**. Los 18 bornes de
  sonda tienen su etiqueta propia (`1V 1D 1G ... 6G`) en una fila ARRIBA del cuerpo, y los 7 del
  borde izquierdo llevan el nombre girado 90 en la franja de 1,2 mm entre bornera y bornera.

### Cambios de @hardware absorbidos el mismo dia (declarados en UN solo lugar)
`HUELLA_OVERRIDE` y `NO_POBLAR` en `placement.py`, y §5 de LAYOUT_MINI.md para @esquematico:
1. **D5..D8 pasan de DO-15 THT a `Diode_SMD:D_SMA_Handsoldering`** (el P6KE6.8CA no se consigue en
   Argentina; va SMAJ6.8CA en SMA). Variante *Handsoldering* a proposito: los sueldan Gonza y
   Sergio. **Son los 4 unicos SMD de la placa.**
2. **D2 NO SE POBLA** (su ~1000 pF solos rompen el timing a 25 m). Se conserva la huella pasante,
   marcada DNP y con `NO POBLAR: D2 R18 J10` en el silk. El bus queda con R2 100 R + los clamps
   1N4148 (~4 pF). Para @esquematico: en la rev B el TVS se muda al VCC de sondas.

### Lo que BLOQUEA la fabricacion
**M2/M3/M4/M5** (separacion, desfasaje, agujeros y paso de las dos tiras del modulo de rele) son
**estimados**. Viven en **5 lineas de `pcb/placement.py`**; todo lo demas (rectangulo del modulo,
rotulos, keepouts de los 4 agujeros, posicion de R12/R13) **se deriva**. La serigrafia lo dice en
la propia placa: `agujeros y tiras A MEDIR (M2-M5)`. Riesgo escrito: si el modulo real tiene las
dos tiras juntas en vez de a 40,6 mm, hay que rehacer 6 lineas de `rutas.py` y nada mas.

### Deudas declaradas (LAYOUT_MINI.md §9)
**39,9 % del cobre ruteado va por B.Cu** (885 de 2.219 mm): es la debilidad principal y se ve en
`salida/pcb_bottom.png` — ranuras de 0,7 mm en el plano de abajo, aceptables porque la senal mas
rapida es un 1-Wire de 15 kHz y el radio vive apantallado dentro del modulo. Rev B: rehacer a mano
el abanico por F.Cu. Ademas: R3 a 23 mm de las borneras (no entra en la franja de 8 mm, y es un
elemento serie), SDA/SCL con 74-78 mm para un header que no se puebla, RESET con 80 mm hasta EN,
**sin test points** (no estan en el netlist; rev B: 4 para @esquematico) y **sin fiduciales** a
proposito (no va a pick & place).

### Trampas nuevas del harness (KiCad 10 + Python) — para la biblioteca
1. **KiCad cachea el proyecto en el primer `LoadBoard` del proceso**: escribir las netclases en el
   `.kicad_pro` y releerlas en el MISMO proceso devuelve siempre el Default viejo (0,20) y el
   guardia falla sin motivo. La relectura de control tiene que correr en **otro proceso**.
2. **`SetTextAngleDegrees()` toma GRADOS, no decimas.** Heredar `rot=900` de la Base v2 deja los
   textos a 900 = 180 grados: rotulos dados vuelta y una docena de `silk_overlap` que parecen falta
   de espacio y no lo son.
3. **El router A\* trata todo pad como pasante**: con un TVS **SMA** dejo una pista de 10,6 mm en
   B.Cu que no conecta a nada. Lo que toca un pad SMD se rutea a mano.
4. **Camino degenerado del A\*** (0 tramos, 0 vias): el `while` no progresa y quema `MAX_PARES`
   girando en falso. Hay que declarar el par abierto y seguir (ya estaba aprendido en galgas; la
   copia de la Base v2 no lo tenia).
5. **Una pista que pasa entre los dos pads de un TO-92 lo cortocircuita**: al colector hay que
   entrar por el extremo, no "por el lado corto".
6. **Un pad SMD de masa queda flotando si dos pistas le estrangulan el relleno** por debajo del
   `min_thickness` (0,3): se arregla corriendo la pista 0,7 mm, no metiendo vias.
7. **El triangulo de pin 1 de las borneras horizontales cae fuera de la placa** cuando la bornera
   se monta con la boca en el borde: hay que borrar ese `fp_poly` de F.SilkS al cargar la huella.
8. `b.Remove(via)` con zonas rellenas es toxico: `limpiar_vias.py` corre en proceso propio, vacia
   las zonas, borra y despues rellena.

**Para @diseno3d** (LAYOUT_MINI.md §6, la PCB manda): LED1 (37,5 . 95,0), LED2 (58,5 . 95,0),
SW1 RESET (76,5 . 98,1), SW2 WIFI (88,5 . 98,1), **USB en el borde X=120 centrado en Y=35,3**,
**centro del modulo de rele (91,0 . 71,5)** con cuerpo 50 x 39 ocupando x 66..116 / y 52..91,
M3 de placa en (4,4) (116,4) (4,96) (116,96) con **separadores de nylon**, altura interior minima
**35 mm**, 6 prensacables abajo + 4 a la izquierda + ventana de USB a la derecha. `.step` exportado.

**Proximo paso:** Gonza mide M1..M5 -> 5 lineas -> `sh pcb/todo.sh` + `sh pcb/fabricacion.sh`;
@esquematico rev B (SMA, D2 mudado, 4 test points); @verificador antes de fabricar.

- 2026-07-07 - Agente creado por Claude Fable con backlog real de los repos migrados (C:/Proyectos).

- 2026-07-30 [LASER-PCB: demo punta a punta HECHA] — `C:\Proyectos\laser-pcb\ejemplo_kicad\`: detector de campo (190Vcc→2x22k 2W→PC817→GPIO27, LOW=campo OK) + divisor de bus opcional (9Vca→W10M→10uF→30k/10k+zener 3V3→GPIO39) para el drive del torno. KiCad 10 REAL: esquemático generado por script (S-expr, símbolos embebidos de libs oficiales, ERC 0) → netlist kicad-cli → PCB construido con API pcbnew (gen_pcb.py: placement con assert de 27 pads, ruteo manual single-side B.Cu 1.0/1.5mm, clearance 0.6, zona GND con keepout de creepage en la región de campo, keepouts en 4 agujeros M3, serigrafía completa). DRC --severity-all: 0 violaciones / 0 unconnected. Renders top/bottom MIRADOS (3 iteraciones: courtyards Phoenix vs holes/R1/D1, silk tapada por bornera). Salidas: gerbers B.Cu+B.Mask+F.SilkS+Edge, drill Excellon, BOM+pos, placa.glb 547KB para el visor 3D. Regeneración 100% por script (tools/gen_sch.py + tools/gen_pcb.py, comandos en LEEME.md). Lección: borneras MaiXu de la lib estándar no tienen modelo 3D → Phoenix MKDS 5.08 sí; pcbnew.BOARD() pelado segfaultea, usar pcbnew.NewBoard(path).
- 2026-08-21 [GALGAS / DREYFUS] **Guia de armado en PERFBOARD del acondicionador de galga** —
  `C:\Proyectos\galgas\hardware\perfboard\GUIA_ARMADO_PERFBOARD.md` (carpeta nueva). Matias suelda
  a mano hoy; NO se fabrica PCB. Derivada 100% del netlist rev B (`nodo_galga_v3.net`, ERC 0/0),
  sin inventar circuito.
  - **CORRECCION AL ENCARGO: el circuito NO lleva INA333.** El pedido decia "puente + INA333";
    el diseno aprobado lo **descarto explicitamente** (NOTAS_CALCULO §3 y §6-contradiccion-2): el
    INA333 es de la **generacion 1**. La v3 es galga → filtro RC → **ADS1220 con PGA interno
    G=128, ratiometrico**. Puesto como §0.1 de la guia para que nadie suelde un INA por inercia.
  - **Alcance decidido (Ponytail): "Placa A" = ACONDICIONADOR solo** (bloques 1-4: J1, puente,
    shunt-cal, filtro RC, modulo CJMCU-1220) en **perfboard 5x7 cm**, con salida SPI por header
    2x5 a un **Arduino Pro Mini 3,3 V externo** (hay 3 en stock; el ATmega328P-AU es TQFP-32, no
    se suelda a mano). Bloques 5/6/7 fuera: el micro va afuera, la **cadena de pila esta
    BLOQUEADA por P8 (supercap ESR ≤ 1 Ω) y P9 (D4)**, y el RA-02 es paso 2,0 mm. La Placa A es
    exactamente lo que hace falta para cerrar **P1** (¿llego el ADS1220?) y **P4** (350 Ω vs
    10 kΩ con deriva) — R2/R3 van **en zocalo** para poder cambiarlas sin desoldar.
  - **Contenido**: grilla 24 col x 18 filas con coordenadas por componente, 4 buses (+3V0 fila B,
    NODO_A fila F, **E−/REFN fila N**, GND fila Q) + dedo de AGND en la columna 14 unido a masa en
    **un solo agujero**; lista from-to en 5 pasos con **checkpoint de tester al final de cada
    bloque**; pinout de J3 al Pro Mini verificado contra el netlist; procedimiento de bring-up
    de 8 pasos (arrancar en **G=1** y subir por escalones).
  - **HALLAZGOS que la guia aporta al diseno (cuentas nuevas, no estaban en NOTAS_CALCULO):**
    (a) **R1 tiene que estar dentro de ±10,5 Ω de la galga o el PGA SATURA a G=128** — una 330 Ω
    (el E24 mas cercano) da 44 mV de offset contra una ventana de ±22,6 mV: **no sirve**; 350 Ω
    no existe en E24, hay que usar 348 Ω E96 o 330+18. (b) Lo mismo para el apareamiento de
    R2/R3: ventana 1,5 %, presupuesto 0,75 % → **aparear con tester, no comprar por tolerancia**.
    (c) **El residuo de flux es un error medible**: 10 MΩ de aislacion = 35 µε que se mueven con
    la humedad. (d) La resistencia del **hilo de retorno E−** entra en el brazo de la galga:
    0,05 Ω = **71 µε de offset fijo** que ademas consume ventana de PGA. (e) **CD/CC1/CC2 tienen
    que ser C0G**: un X7R es piezoelectrico y sobre una maquina que golpea genera senal falsa.
  - **Desviaciones declaradas** (3, marcadas como tales): **RGD 100 k agregada** como pull-down de
    la compuerta de Q1 (en el banco el cable de CAL_EN va a estar desconectado la mitad del tiempo
    y una compuerta MOS flotante enciende el shunt-cal sin avisar — **propongo que entre tambien
    al esquematico**, el mismo agujero existe durante el reset del micro); **D1/D2/D3 TVS NO
    poblados** (P2 sin resolver: sin `IR ≤ 10 nA` del datasheet, un TVS a ojo mete 117 µε de error
    sin dar sintoma, y el banco esta sobre una mesa); bloques 5/6/7 fuera de placa.
  - **BOM cruzado contra `dominios/hardware.md` + `comercial/LISTA_COMPRA_BANCO_GALGAS.md`**
    (regla dura del 2026-07-10). **Faltantes de riesgo alto, no registrados en ninguna bitacora**:
    las **resistencias de precision nunca se compraron** (R1 348 Ω, R2/R3, RCAL 174k65, RS1/RS2),
    los **capacitores C0G**, la **bornera de paso 5,08** (⚠ la del esquematico es MX126-5,0 y **no
    entra en la grilla de 2,54**) y el **cable apantallado de 3 conductores a la galga**. Sin eso
    no hay tarde de soldadura.
  - **Riesgo #1 de armado, escrito en grande**: `E−/REFN` **NO es masa** — se conecta a GND solo
    por la llave interna del ADS1220 y es el denominador de la medicion ratiometrica. Soldarlo al
    bus de masa (el error "obvio" de quien mira el dibujo apurado) mata el gateo y la referencia.
  - **Proximo paso**: Matias suelda y devuelve los valores MEDIDOS de R1/R2/R3/RCAL + el resultado
    del shunt-cal → con eso se cierra P1 y se puede correr P4. El **layout del PCB sigue en
    espera** de P6 (@verificador sobre la rev B), P8 y P9. Nada commiteado.

- 2026-07-08 [BRIEFING GIMAP] — leer ../BRIEFING_EQUIPO_GIMAP.md y los 4 docs (PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO). Para vos: placa emisor bajo consumo (gateo puente + supercap cerca del LoRa para el pulso, sin boost) + placa receptor ESP32+LoRa 220V. Convergencia UTN Diseño y Manufactura/Tecnología.

- 2026-09-02 (c) [GALGAS / DREYFUS] **DOSSIER en UN PDF, para el celular**:
  `C:\Proyectos\galgas\hardware\NODO_GALGA_v3_revC_DOSSIER.pdf` (**18 paginas, 3,25 MB**, A4,
  numerado, con marcadores) generado por `kicad\armar_dossier.py` + `kicad\pcb\metricas.py`.
  Misma herramienta y misma regla que el dossier de Termovigia: **ningun numero se tipea a mano**.
  - Contenido: portada con la banda roja PRELIMINAR - NO FABRICAR y los tres bloqueos nombrados |
    indice | **resumen de UNA pagina** (la cadena galga -> ADS1220 ratiometrico PGA 128 -> ATmega328P
    -> LoRa 433, con la pila de litio y los supercaps para el pulso de TX) | esquematico rev C |
    **la placa en 3 paginas completas** (2D superior, 3D arriba, 3D abajo) con la tabla del gabinete |
    layout (netclases con la cuenta de corriente, criterio del bloque analogico, corredor del ramal A
    y su regla propia, decision de antena) | estado medido sin maquillar | veredicto de P6b y lo que
    queda abierto | pendientes para fabricar con que se rehace si cae cada bloqueo | BOM de 35 lineas.
  - **Sello PRELIMINAR al pie de las 3 paginas de la placa** (banda roja con los tres bloqueos), para
    que una hoja impresa suelta no se confunda con la version final. Lo pidio el Director y es la
    parte que mas se va a imprimir.
  - **Una sola fuente de verdad, resuelta a pesar de los dos Python**: PyMuPDF vive en el Python del
    sistema y `pcbnew` en el de KiCad, y no se hablan. `armar_dossier.py` **delega**: corre
    `pcb/metricas.py` con el interprete de KiCad, que vuelca a `salida/metricas.json` las metricas
    exactas del board (segmentos por capa y su largo, vias, huellas, segmentos de B.Cu dentro del
    courtyard de U1/U2, la verificacion de `/E_REFN` y la BOM agrupada) y despues las lee. Las
    metricas siguen saliendo del `.kicad_pcb`.
  - **Tres cosas se corrigieron MIRANDO el PDF, no confiando en que estaba bien** (contact sheet de
    las 18 paginas + 3 paginas renderizadas a 140 dpi):
    (1) **el conteo de DRC estaba mal**: el reporte lista los pads sin conectar con severidad `error`
    y ademas los cuenta en su propio bloque, asi que contar `; error` sobre todo el archivo los sumaba
    dos veces -> el resumen decia "2 errores" donde hay **0**. Se cuenta solo dentro del bloque de
    violaciones; (2) el PDF salia de **12,86 MB** porque el contenido vectorial del esquematico se
    copiaba sin comprimir: con `deflate_images` + `deflate_fonts` + `clean` bajo a **3,25 MB**, y las
    imagenes se reescalan a 2000 px de lado largo; (3) habia **dos paginas casi vacias** (el resumen
    se desbordaba por cuatro lineas y la portadilla de la placa quedaba a medio llenar): el resumen
    se aprieta con CSS propio hasta entrar en UNA pagina y la tabla del gabinete se mudo a la
    portadilla de la placa, que es donde sirve. De 20 paginas a 18, todas llenas.
  - Mejora del conversor markdown->HTML propio: las lineas seguidas de un mismo parrafo ahora se
    **juntan**. Antes cada linea del `.md` era un `<p>` y el texto salia a los saltos: en el celular
    se leia mal.
  - Regeneracion desde cero verificada (borrando cache y JSON): 18 paginas, 3,25 MB. Sin commit.

- 2026-09-04 (g) [GALGAS] **Limpieza y archivo de la rev E.1** (pedido del verificador). Los dos
  `.bak` sueltos NO se borraron: son de la **rev E.1**, que hoy es una de las dos salidas reales,
  asi que se archivaron como corresponde en **`revE1/`** (`LAYOUT.md`, `rutas.py`, `LEEME_REVE1.txt`).
  El LEEME dice lo que falta y como se recupera: **el `.kicad_pcb` de la E.1 se sobrescribio** al
  derivar la E.2/E.3 sobre el mismo archivo, pero esta intacto en **git, commit `62b7996`**
  (verificado: placa 218 x 27 y `drc.rpt` con **0 violaciones / 0 unconnected / 0 footprint**), con
  el comando `git show` exacto para sacarlo. Tambien avisa que **`SIMPLE_FAZ = False` NO devuelve la
  E.1**: devuelve una doble faz con el placement de la E.3. Borrados los `__pycache__`; `*.bak`
  agregado al `.gitignore` con el motivo (cada revision se archiva en su `revX/`, no como `.bak`).
  Los `.txt` que marcaba el verificador ya no estaban; los `DIFF_REDES_*.txt` quedan: son los diffs
  de netlist entre revisiones, no temporales.
  **`LAYOUT.md` 0.5**: quedo escrita la conclusion que estaba solo en el chat — *partir por `JB2x`
  no ayuda* (la placa A se lleva 9 cruces y **los 45 del micro se van enteros a la B**: partir
  sirve cuando el problema esta en la frontera, y aca esta ADENTRO de un bloque) y **la salida es
  cambiar el encapsulado del micro** (con 0,6+0,6 no se pasa entre pines a 2,54, asi que los 28
  pines del DIP son una barrera de 36 mm en el medio de la placa). Anotado que Matias evalua el
  **Pro Mini 3,3 V** y que **hasta el netlist rev F el layout no se toca**.

## 2026-09-04 (f) — GALGAS rev E.3: **rehice el orden del digital y NO alcanza: ~48 puentes**

Se decidio seguir con simple faz (motivo de fabricacion: Matias la hace en acido y **alinear las
dos caras es donde se arruinan**). Rehice el orden fisico del bloque digital con la tecnica de la
rev D. **El numero final: ~48 puentes de alambre**, contra los 12 pedidos y los 20 del limite
acordado. Paro aca, como se acordo.

| | antes del rediseño | despues |
|---|---|---|
| cruces | 80 | **89** |
| puentes que pide | 46 | **48** |
| abiertas | 36 | 31 |

### Lo que SI arreglo el rediseño (y queda en la placa)
* **La regla que ordena el canal**: encima de la fila norte del zocalo NO HAY NADA, asi que un
  pin de esa fila se saca al norte sin cruzar a nadie. El bus del ADC entra por el canal y SUBE
  a su pin; lo que va al ISP y al radio SALE del mismo pin HACIA EL NORTE.
* **`J1` girado**: de oeste a este quedo **MALLA - E- - S+ - A - E+2**, que es el orden de sus
  destinos en la columna. Con el orden inverso, `A` y `S+` se cruzaban si o si. Este es el mismo
  criterio de la rev D y funciono igual de bien.
* ISP girado 270 y colgado del bus; `JB3x` reordenados por DE DONDE LLEGA cada señal (MISO y NSS
  del norte arriba; RST y DIO0 de la fila sur, abajo); el reed a la avenida sur; los dos rodeos
  del radio en carriles separados.

### El dato que decide: DONDE estan los cruces
| zona | cruces |
|---|---|
| A analogico + ADC (x < 104) | **9** |
| **B micro (104..150)** | **45** |
| C radio + ISP (150..190) | 20 |
| D alimentacion (> 190) | 15 |

**El problema no esta en la frontera entre bloques: esta DENTRO del bloque del micro.** Un
ATmega328P DIP-28 con 20 señales saliendo a los cuatro costados, en UNA cara y con 0,6 de
aislacion (que impide pasar entre pines), es un abanico que no se aplana moviendo cosas.

**Y por eso partirla en dos por `JB2x` NO ayuda**: la placa A (galga + columna + filtro + ADC) se
lleva **9** cruces y quedaria casi limpia, pero **los 45 del micro se van enteros a la placa B**.

### Las tres salidas reales
1. **Doble faz de fabrica (rev E.1)**: 218 x 27, **DRC 0/0/0, cero alambres**, ya cerrada.
2. **Simple faz casera con ~48 puentes**: viable y la placa esta lista, pero son 48 alambres
   soldados a mano en un nodo montado en un REDLER que golpea.
3. **Cambiar el encapsulado del micro**: la mitad de los cruces de la zona B salen de que el
   DIP-28 tiene 28 pines en dos filas a 2,54 y en una cara no se puede pasar entre ellos.

**Estado entregado:** 234,5 x 32 (ancho sin cambios), placement sin solapes, **DRC 186 / 31
abiertas**, **1 puente declarado** (el shunt-cal, con su agujero de paso en cada punta).
Artworks 1:1, hoja de armado con el rotulo de cada hilo, **169 agujeros en 6 mechas** y dossier
`NODO_GALGA_v3_revE3_DOSSIER.pdf` al dia. Renders mirados. Sin gerbers, sin commit.

## 2026-09-04 (e) — GALGAS rev E.3: **el ajuste fino NO alcanzo, y ahora se por que**

Me mandaron a cerrar el DRC "corriendo carriles, no rediseñando" -- que es lo que yo mismo
habia dicho. **Estaba equivocado y lo medi.** Estado real al cerrar: **164 violaciones, 36
pares abiertos** (18 son islas de masa) y **1 puente de alambre**.

### Lo que descompone esas 164
| | |
|---|---|
| separacion (decimas de mm) | **66** -> SI se arreglan moviendo |
| **cruces reales** | **80** -> NO se arreglan moviendo |

El relajador que escribi los bajo solo: **violacion total 227,6 -> 38,2 y puntos en falta
202 -> 65**. Pero un cruce no se separa empujando: en UNA cara cada cruce **cuesta un puente**.
Lo probe: convertir todos los cruces en puentes da **46 tramos levantados + 68 agujeros**, y
esos 68 agujeros de 1,8 en un ruteo denso **disparan el DRC a 273**. Por ese camino no cierra.

**Diagnostico:** con las reglas caseras (0,6/0,6 y pads de 1,8, que impiden pasar entre pines a
2,54) **el bloque digital no es planar con este placement**. Lo que falta no es una pasada de
ajuste: es **rehacer el orden fisico del digital para hacerlo planar** -- la tecnica de la rev D
(*los destinos al sur del micro EN EL ORDEN DE SUS PINES*), moviendo `J2`, `J3`, `LD1` y la
columna `JB3x`. Es una sesion, no un retoque.

### Lo que SI quedo cerrado
* **Bloque analogico completo en una cara**: `E-/REFN` sin vias y sin puentes, L10 y L1 intactos.
  **Ninguna red de MEDICION quedo abierta** -- lo garantiza el guardian de `cerrar_puentes.py`,
  que ABORTA si alguna aparece suelta.
* **Un solo puente de alambre** (el shunt-cal, 23,7 mm), con **agujero de paso en cada extremo**
  (0,8 con anillo 0,5): sin ese agujero el alambre no toca el cobre y la red queda abierta --
  bug que encontre y arregle en `rutear.py`.
* Artworks 1:1 y hoja de armado regenerados; **169 agujeros en 6 mechas**; dossier
  `NODO_GALGA_v3_revE3_DOSSIER.pdf` (23 pag) con la portada corregida: fabricacion CASERA, no
  JLCPCB, y el estado dice "digital EN PROGRESO" en vez de "ruteo COMPLETO".

### Harness nuevo (lo que permite cerrarlo la proxima)
| script | que hace |
|---|---|
| `pcb/chequear_tabla.py` | mide la tabla **antes** de aplicarla y dice **que ruta y que punto** falla. 2 s contra 40 s del ciclo con DRC |
| `pcb/relajar.py` | descenso local sobre los waypoints (el metodo de fuerzas **oscilaba**: subia de 139 a 160). Subdivide tramos largos, **fija los puntos compartidos entre rutas** (si no, la red se abre) y no toca el analogico |
| `pcb/cortar_cruces.py` | cruces -> puentes con sus agujeros, con lista de redes **protegidas** |
| `pcb/diagnostico.py` | agrupa las violaciones **por familia**: con 170, leerlas de a una no sirve |

### Trampas nuevas
1. **`rutear.py` no es idempotente si cambian las coordenadas**: hay que regenerar el board
   antes de rutear o quedan las pistas viejas Y las nuevas (me dio 231 violaciones fantasma).
2. **Un puente de alambre sin agujero en la punta no conecta nada** (y el DRC lo canta como red
   abierta, no como puente mal hecho).
3. **Mover waypoints rompe las uniones entre rutas** que compartian una coordenada: 11
   `track_dangling` y 40 pares abiertos hasta que las fije.

### Lo que tiene que decidir Matias
1. **Rediseñar el digital para una cara** (una sesion mas) -> casera de 234,5 x 32; o
2. **volver a la doble faz de la rev E.1** (218 x 27, **DRC 0/0/0**, sin un solo alambre) y
   mandarla a fabricar: es mas chica y ya esta cerrada.
**Y sigue faltando la cota del eje**, que es lo unico que puede volver a cambiar todo.

## 2026-09-04 (d) — GALGAS: **rev E.3, ACHICADA** (234,5 x 32, de 26 puentes a 18)

Orden de Matias con los numeros de la E.2 a la vista: **simple faz, pero achicar primero y
ruteAr una sola vez despues**. Resultado:

| | E.1 doble faz | E.2 simple faz | **E.3 achicada** |
|---|---|---|---|
| tamano | 218 x 27 (5.886 mm2) | 240 x 40 (9.600) | **234,5 x 32 (7.504)** |
| puentes de alambre | 0 | 26 (1.175 mm) | **18 (300 mm)** |

**−22 % de area y −8 mm de ancho contra la E.2**, y el alambre bajo a un cuarto.

### Cada recorte con su ahorro (lo que se pidio)
* **`J1` y `J4` fuera**: los cables van SOLDADOS DIRECTO, con huella propia `CABLE_1xN_P3.00`
  (pads de 2,4 con broca 1,3 + **dos agujeros de 2,5 de ALIVIO DE TRACCION**, uno a cada lado:
  el tiron se lo come el precinto, no la soldadura). J1: 26,4x10,8 -> 21,6x3,2 (**−7,6 de
  ANCHO**, que es lo que mas valia); J4: 21,3x10,8 -> 18,6x3,2.
* **El REED sale de la placa**: el iman esta en la estructura, asi que su lugar lo define el
  REDLER y no el layout. Queda cableado (2 pads) y **pegado a J4**, de modo que reed y pilas
  salen por el MISMO prensacable. 24,7 -> 12,6 mm y libera toda la franja sur del micro.
* **`JP1`**: 2 pads con tira cortable en vez de tira de pines (3,5x6,1 -> 5,0x2,6).
* **Los 15 `JB*` -> `JB_CUTTER`** propio (dos pads de 1,2x1,6 con tira de 0,4): sin mascara no
  hace falta el solder jumper de catalogo, que esta pensado para produccion.
* **Diez condensadores parados** (paso 5,00 -> 2,50): −1,6 mm cada uno, ~18 mm en total.
* `U4` TO-92 -> **TO-92_Wide** y `CR2` P2,00 -> **P2,50**: las dos huellas del netlist que NO
  eran fabricables a mano (pads a 1,27 se tocan con anillo 0,4).
* **El LED SE QUEDA**, y lo digo con la consecuencia: sacarlo ahorraba ~10 mm y **costaba la
  unica forma de diagnostico sin radio** (3 destellos = binario cruzado, 5 = fusibles). En una
  planta sin cobertura eso es quedarse ciego. No vale 10 mm.

### Lo que se aprendio achicando
* **En 32 mm de ancho una franja NO admite dos filas de pasivos mas un carril.** Se resolvio
  con `acomodar_filas()` en el generador: se declaran las filas (y, rot, [(ref, x deseada)]) y
  la funcion mide el courtyard REAL ya rotado y empuja al este lo que no entra. Calcular esos
  huecos a ojo fallo tres veces seguidas; ahora lo hace el script y ademas informa cuanto
  empujo a cada uno. **Trampa**: si la fila impone `rot`, pisa la rotacion propia del
  componente (J3 girado 270 se paraba y se salia de la placa); por eso `rot=None` = respetar.
* El courtyard del zocalo DIP-28 llega a y=21,33: la fila sur no puede estar a 21,8.
* **El mínimo alcanzable** (LAYOUT 0.6): el ancho tiene piso duro en **23,82 mm** (CJMCU con
  filas a 20,32). 30 mm apretando a una avenida por lado; **26 sin avenidas**; y si la cota del
  eje obligara, **partirla en dos** por la columna `JB2x` -- que existe justo para eso: son 5
  hilos (CS, DRDY, MISO, +3V0, GND) -- daria **~105 x 24** (sensor) y **~135 x 26** (nodo).

### Estado y lo que falta
Placement **sin solapes**, digital **ruteado a mano** (el A* no se volvio a usar), **18 puentes**
y artworks/hoja de armado/taladros regenerados (**168 agujeros en 6 mechas**). La hoja de armado
ahora lleva **el rotulo de cada hilo** (MALLA/E-/S+/A/E+2 en J1, +C1/GND/+C2/GND en J4, TX/RX/GND
en J3), que es lo que reemplaza a la serigrafia de las borneras que se sacaron.
**Falta**: una pasada de ajuste fino del ruteo (172 violaciones de separacion con la regla de
0,6; se corrigen corriendo carriles, no rediseñando) y **la cota del eje, que sigue sin darse**.

## 2026-09-04 (c) — GALGAS / DREYFUS: **rev E.2, SIMPLE FAZ + fabricacion CASERA** (EN PROGRESO)

Dos ordenes nuevas de Matias el mismo dia: **una sola cara de cobre** y **la fabrica el en casa,
con acido** (no JLCPCB). `C:\Proyectos\galgas\hardware\kicad\`. **No esta terminada y lo digo
con numeros** — la parte dificil (el analogico) esta hecha; el bloque digital falta.

### LA RESPUESTA QUE PIDIO: cuanto cuesta la simple faz casera
| | rev E.1 doble faz | rev E.2 simple faz casera |
|---|---|---|
| tamano | **218 x 27** (5.886 mm2) | **240 x 40** (9.600 mm2) = **+63 % de area** |
| pista/aislacion | 0,3 / 0,2 | **0,6 / 0,6** (masa y potencia 1,5) |
| vias | 38 | **0** |
| puentes de alambre | 0 | **26 (1.175 mm)**, el mayor de 264 mm |
| DRC | 0/0/0 | **58 sobre cobre + 18 abiertas** |

**Las tres cosas que la encarecen, medidas:**
1. **Con pads de 1,8 y aire de 0,6, entre dos pines a 2,54 quedan 0,74 mm: NO PASA NINGUNA
   PISTA** (hace falta 1,8). En la E.1 el ruteo se colaba entre pines en once lugares; ninguno
   sobrevive. Quedan como avenidas internas solo el canal del zocalo DIP-28 (5,82 mm) y el
   interior del CJMCU (18,5 mm).
2. **El ancho tuvo que ir de 27 a 40 mm** para abrir dos avenidas longitudinales: el CJMCU ocupa
   23,8 de los 27 viejos y no quedaba por donde llevar los rieles ni el bus.
3. **Dos huellas del netlist no son fabricables a mano** (misma pieza, sin tocar una red):
   `U4` TO-92 (pads a 1,27, se tocaban) -> **TO-92_Wide**; `CR2` radial P2,00 -> **D6.3 P2,50**.

**Dato para decidir:** con el placement de la E.1 tal cual, la simple faz costaba **24 puentes
(389 mm)** — lo medi antes de tocar nada. Hoy son 26, pero **20 de esos 26 son del bloque digital
sin rutear**, que los puso `cerrar_puentes.py` en linea recta. **El bloque analogico entero
necesito UN solo puente.** Estimacion con el digital ruteado a mano: **8-12**.
**Mi recomendacion: si se quiere chica y sin alambres, la E.1 doble faz sale mejor.**

### Lo que SI quedo hecho (y es lo dificil)
* **`SIMPLE_FAZ` es una VARIABLE, no un fork** (`generar_pcb.py`): de ella salen el ancho, el
  offset del contenido, el plano en una sola capa, los pads/brocas caseros y el **swap de capas**
  de `pcb/rutear.py` ("F" logica = B.Cu real; "B" logica = F.Cu = **puente de alambre**, capa que
  no se fabrica). Con `False` vuelve la doble faz.
* **Analogico completo en una cara**: `E-/REFN` **sin vias y sin puentes**, L10 (nudo en `JP2`) y
  L1 (seis de precision en un eje, paso 4,2) intactos. **Un solo puente**: el del shunt-cal,
  elegido a proposito porque es el unico camino que no entra ni en el cero ni en la ganancia
  (174 kOhm, ~17 uA).
* **Los 15 `JB*` pasaron a la cara del cobre (B.Cu)**: un pad SMD en la cara de componentes de
  una placa de una sola cara NO TOCA NADA. Ademas asi se cortan sin dar vuelta la placa.
* **Reglas caseras en el DRC** (`pcb/netclases.py` -> `.kicad_pro`): 0,6/0,6, anillo 0,5 (0,4 en
  pines a 2,54, porque con broca 1,0 un pad de 2,0 deja 0,54 entre pines), broca >= 0,8,
  agujero-a-agujero 0,8, y **`solder_mask_bridge` y toda la serigrafia en *ignore*** (no hay
  mascara ni serigrafia; lo que las reemplaza es el aire de 0,6 y la hoja de armado).
* **Salidas de fabricacion casera nuevas** (`pcb/artwork.py`, dibujadas del board con PyMuPDF
  porque el B&W de kicad-cli sale invertido): `artwork_cobre_espejado.pdf` (para planchar),
  `artwork_cobre_directo.pdf` (fotosensible) y `hoja_armado.pdf` (reemplaza a la serigrafia),
  **los tres 1:1 con una REGLA DE 50 mm dibujada** para detectar si la impresora escalo, y
  **marca de centrado en cada pad** para que la mecha no patine. Mas `pcb/taladros.py`:
  **156 agujeros en 5 escalones** (0,8 x89 - 1,0 x52 - 1,2 x4 - 1,3 x9 - 3,2 x2).
* **Herramientas nuevas**: `pcb/puentes.py` (agrupa el cobre de F.Cu en cadenas = inventario de
  alambres, con largo) y `pcb/cerrar_puentes.py`, que **ABORTA si una red de MEDICION quedo
  abierta**: E-/REFN y las ramas del puente se rutean en cobre o no se rutean.

### Lo que falta
Rutear a mano el bloque digital (SPI, ISP, radio, reed, LED, divisor). **El A* no sirve con
0,6/0,6**: intenta y se choca (genero 97 violaciones y hasta rompio redes analogicas, por eso lo
saque del cierre). De ahi salen las 18 abiertas y las 58 violaciones sobre cobre.

### Trampas del harness (nuevas, para la biblioteca)
1. **Un pad SMD en la cara equivocada de una placa de una sola cara no conecta con nada** y el
   DRC lo reporta como "unconnected" en redes que uno juraria ruteadas.
2. **Los dos pads de un net-tie a 1,3 mm se tapan entre si** cuando el clearance sube a 0,6: el
   A* decia "grupo sin celda libre" sin decir por que. Un net-tie no es obstaculo para su hermana.
3. **KiCad no espeja al leer una huella declarada en B.Cu**: la posicion es la que uno escribe,
   asi que NO hay que negar la X (si se niega, el pad 1 se va al otro lado y las rutas se invierten).
4. **Una netclase con anillo invalido (via 0,9 / broca 0,5) se descarta entera en silencio** y
   KiCad usa el valor viejo: la guardia de `netclases.py` lo caza.

- 2026-09-04 (b) [GALGAS / DREYFUS - rev E.1] **DOSSIER en UN PDF**: `hardware\NODO_GALGA_v3_revE1_DOSSIER.pdf`,
  **23 paginas, 4,24 MB**. Portada con 218 x 27 y el sello **PRELIMINAR - NO FABRICAR** con TODOS los
  bloqueos vigentes (M1/M2, M5, P3, D0 y **la cota del eje, que la debe Matias**) - resumen - esquematico
  rev E.1 vectorial - la placa (3D top/bottom, 2D top/bottom, **los 4 zooms por etapa** y la **tabla de
  aislacion de los 15 puentes**) - layout - estado medido - verificacion - pendientes.

  **El script se habia roto y el arreglo es de harness, no un parche.** `armar_dossier.py` buscaba las
  secciones del `LAYOUT.md` **por su titulo con regex** (`^## 3\. Las dos ESTRELLAS`) y abortaba con
  `no encontre la seccion` en cuanto el LAYOUT se rehizo para la E.1 (13 secciones nuevas). Ahora:
  1. **Una sola tabla `SECCIONES` arriba del script** (clave -> numero + pista de texto). Para adaptar el
     dossier a la proxima revision se toca SOLO esa tabla.
  2. Las secciones se buscan **por numero** (`^## N.`), no por texto; la pista sirve para el aviso y se
     compara **sin acentos** (la 12 se llama "Lo que se que es debil" y el acento la hacia fallar).
  3. **Si una seccion falta, avisa y sigue** (`AVISOS_SECCIONES`, que se imprime al final de la corrida)
     en vez de `SystemExit`. Una seccion renombrada no puede voltear el dossier entero.
  4. Los renders que faltan tambien avisan en vez de romper (`zoom_*_top.png`, `revE1_puentes.png`).
  5. `FECHA` sale del **mtime del `.kicad_pcb`**, no de una constante (decia 2026-09-02 con la placa del 04).
  Ademas la seccion 5.3 del dossier ya no tiene autocritica propia: **inserta la seccion 12 del LAYOUT**,
  para que no existan dos versiones de la misma debilidad. Verificado mirando el PDF: portada, zooms,
  tabla de puentes y estado medido. Corrida limpia: *"las 13 secciones del LAYOUT.md que pide el dossier
  estan todas"*.

## 2026-09-04 — GALGAS / DREYFUS: **rev E.1, la placa cambia de forma** (218 x 27, SOBRE EJE)

`C:\Proyectos\galgas\hardware\kicad\` — `nodo_galga_v3.kicad_pcb`, `generar_pcb.py` parametrizado,
`LAYOUT.md` rehecho (13 secciones), `drc.rpt`, `salida\` (3D top/bottom, 2D top/bottom, **8 zooms
recortados**, `.glb`, `.step`, `verificacion.json`), toolchain en `pcb\`. **La rev D entera se archivo
en `revD/`** con LEEME (placa, .pro, .dru, LAYOUT, drc, generador + `pcb/`, `salida_revD/`).
**Sin gerbers y sin commit** (orden).

**Estado medido (cierre):** 59/59 componentes, 64 redes, **327 segmentos + 38 vias**,
**DRC `--severity-all` = 0 violaciones, 0 pads sin conectar, 0 errores de huella** (el reporte no
tiene una sola linea). `pcb/verificar.py`: **0 fallos, 1 aviso** (los 15 tramos de B.Cu bajo el
zocalo del micro, aceptados y declarados). Renders 2D y 3D **mirados** (los enteros de 218x27 no se
pueden leer: `pcb/zooms.py` los corta en 4 tramos por cara).

### La decision del ANCHO: el zocalo NO alcanza, y el numero se dijo antes de forzar nada
Matias ordeno "el ancho lo fija el zocalo DIP-28". Se midio y **no entra**: el `DIP-28_W7.62mm_Socket`
ocupa 10,66 mm, pero el **CJMCU-1220 tiene las filas a 20,32 mm (23,82 de courtyard)** y el RA-02 con
adaptador a 22,86 (22,28). No es placement: es el paso de las tiras hembra, y no cambia ni girando ni
acostando. `ANCHO_MINIMO` se DERIVA (23,82 + 2 x 0,6 = 25,5) y se fijo **ANCHO_PLACA = 27,0**: los
1,5 mm extra los piden el lazo sur de E-/REFN (y = 25,3) y la fila sur del CJMCU (y = 23,66).
**El LARGO no se tipea**: `largo_derivado()` lo saca del courtyard mas al este -> **218,0 mm**.

### Girado / acostado / parado (decision 3 y 4)
Girados: `U1` 270, `U2` 90 (filas a lo largo), `U3` 180 (SPI al micro, 3V3/RST/DIO0 a la
alimentacion, IPEX en la esquina SE). Acostados a lo largo: `J1` (26,4), `J4` (21,3), `SW1` (24,7),
`CSC1` (supercap, en el extremo este). **Parados** (huella vertical forzada, sin cambio de red;
deuda para @esquematico): `RD1 RD2 RD3 RSTRAP1 RP1 RL1 RR1 RPU1 RPU2 RPU3` + `RSC1` + `DB1 DB2`.
Las seis de precision quedaron **acostadas a proposito** (L1): mismo eje, misma columna x = 42,5.

### L10 sobrevive al cambio de topologia: el nudo estrella ahora vive en JP2
`R2.1 -> JP2.2` = 4,19 mm y `R1.1 -> JP2.1` = 4,26 mm, dos rectas; en 1/4 de puente el shunt 1-2 las
une. **Asimetria 0,07 mm = 0,39 ue** (limite 1). `JB11` quedo **aguas arriba** del nudo (JB11.1 = red
del nudo, JB11.2 = +3V0), como se pidio. El nudo sigue por y = 13,5 **entre los dos pads de CD1** y
`JB12.2` baja a AVDD **entre los pines 11 y 12 del modulo** (0,32 mm de aire a cada lado).
`E-/REFN` es una "C" (lazo norte a R3.2 y JB15.1, lazo sur a JP3.1): **122,4 mm, 0 vias, solo F.Cu**,
4 pads exactos. Verificado sobre el cobre, no declarado.

### L11: los puentes por frontera, en columna, a paso 3,6
`JB15 JB14 JB12 JB11 JB13` (filtro->ADC, en el orden de los pines del CJMCU) · `JB22 JB41 JB23 JB21`
(ADC->micro) · `JB31 JB32 JB33 JB34` (micro->radio). Los de alimentacion van con su modulo: `JB41` en
la columna del ADC, `JB42` pegado a CM1, `JB43` pegado a CR1/CR2. Todos accesibles con cutter.

### La franja del zocalo es el UNICO lugar donde se corta el plano
Abajo va contra metal: B.Cu prohibido por rule areas en **todo el bloque analogico (x < 96)** y bajo
el **radio (x 146-172,5)**, con tres ventanitas de 3 x 1,4 mm para via-jogs declaradas. Medido:
**1 tramo bajo el CJMCU** (la via-jog de AVDD, bajo los pines 11/12) y **0 bajo el cuerpo del RA-02**.
Todo el resto de B.Cu (68 tramos) vive bajo el zocalo del micro. **Anotado en LAYOUT §3.1: hace falta
una lamina aislante** (Kapton/Nomex 0,2) entre la placa y el eje: los 90 pads pasantes asoman por
abajo y, si el eje esta a masa de la maquina, esa masa entra en la del ADC.

### El canal del zocalo como bus (lo que enseño esta placa)
En 27 mm de ancho, la unica via de paso longitudinal entre el ADC y el radio es el hueco de 6 mm
entre las dos filas del DIP-28. Quedo como bus de 6 carriles (SCLK 11,0 · MISO 12,0 · MOSI 13,0 ·
+3V0 14,35 · DRDY 15,3 · VBAT_RET 15,85). **Regla nueva: un carril que sigue hacia el este bloquea
las subidas de los carriles de abajo** -> cada carril termina EN SU PIN y la continuacion cambia de
capa (B.Cu, permitido justo ahi).

### Serigrafia: la mitad de las referencias va ABAJO, y es correcto
En 27 mm no entran 59 referencias arriba. `rotular.py` ahora esquiva ademas **pistas y vias de F.Cu**
y, si no hay lugar, manda la referencia a **B.SilkS espejada, pegada al componente**: 29 arriba, 25
abajo, 5 escondidas. En una placa toda pasante la cara de abajo es la que se mira al soldar.
Sanidad agregada: en F nunca espejada, en B siempre (si no, `mirrored_text_on_front_layer`).

### Trampas del harness nuevas (para la biblioteca)
1. **`b.Remove()` tambien degrada el board al borrar TEXTOS**: los rotulos fijos de la corrida
   anterior se borran en `pcb/limpiar_silk.py`, **proceso aparte** (si no, rotular.py explota).
2. **`GetFilledPolysList(capa)` dispara un assert MODAL** si la zona no esta rellena en esa capa —
   y una zona en F+B con `GetLayer()` devuelve UNA sola. Mataba `rutear_astar.py` en silencio.
3. **El heredoc de bash se come los `
` de los strings de Python**: escribir los parches como
   archivo (`Write`) y ejecutarlos, no pasarlos por `<<EOF`.
4. El item que el DRC muestra en un `shorting_items` **puede no ser el culpable** (mostro un pad de
   JB41 a 80 mm del conflicto real, que era JB43): mirar la RED que nombra, no la posicion.
5. **Anchos de netclase que no entran**: los dos rieles de +3V0 son de 0,5 y no 0,8 (hueco de 1,43 mm
   entre JB43 y DB1). Declarado en LAYOUT §7 con la cuenta (4,8 mV en el pulso de TX).

**Punto mas debil declarado (LAYOUT §12):** los 218 mm son un lazo largo — el bloque analogico y el
radio a 90 mm, y el ramal de +3V0 al ADC recorre ~80 mm desde el LDO; la forma la impuso el eje, no
la electronica, asi que **no hay separacion transversal analogico/digital**, solo longitudinal, y el
carril de +3V0 del nudo pasa por el canal del zocalo del micro.

**Sigue bloqueando gerbers:** **M1** (separacion real de filas del RA-02) y **M2** (calibre del
CJMCU — este SI manda el ancho de placa). Deuda para @esquematico: bajar al `.kicad_sch` las 13
huellas verticales y la pasante del RA-02 (no cambian ninguna red).

## 2026-09-02 (d) — GALGAS / DREYFUS: **rev D, la placa se rehizo entera** (120 x 90, TODO PASANTE)

`C:\Proyectos\galgas\hardware\kicad\` — `nodo_galga_v3.kicad_pcb`, `LAYOUT.md` (rehecho, no
parchado), `drc.rpt`, `salida\` (2D top/bottom, 3D top/bottom, `.glb`, `.step`, `verificacion.json`),
toolchain en `pcb\`. **La rev C entera se archivó en `revC/`** con un LEEME (H-15 de @verificador:
convivía con el netlist rev D y un cold-start podía abrir la placa vieja creyéndola nueva).
**Sin gerbers y sin commit** (orden). Dossier: `hardware\NODO_GALGA_v3_revD_DOSSIER.pdf`,
**16 páginas, 3,11 MB**.

**Estado medido (cierre):** 57/57 componentes, 50 redes, **338 segmentos + 28 vías**,
**DRC `--severity-all` = 0 errores, 0 pads sin conectar, 0 avisos, 0 errores de huella** —
el reporte no tiene una sola línea de violación.
`pcb/verificar.py` (nuevo): **0 fallos, 1 aviso**. Renders 2D y 3D **mirados**, más un zoom al bloque
analógico y un contact sheet de las 16 páginas del dossier.

**CIERRE (mismo día, después del reporte): el DRC quedó en CERO DE TODO.** Los 2 avisos que quedaban
eran uno solo repetido y no eran míos: la huella del reed dibujaba la línea del alambre **hasta el centro
del pad** (±11,43, o sea 0,90 mm dentro del cobre, una vez por pata). @esquematico lo cerró **sin número
fijo**: `SILK_FIN = pr − PAD_SW1/2 − 0,13`, derivado de la geometría, así que cuando caiga `DE-14`/`M5`
con el reed real medido y cambie `PASO_SW1`, el corte se recalcula solo. Re-importada la huella y rehecha
la placa con `sh pcb/todo.sh`:
**`Found 0 DRC violations` · `Found 0 unconnected pads` · `Found 0 Footprint errors`.**
Medido sobre el board: los extremos quedan a **1,03 mm del centro del pad = 0,070 mm de aire** entre el
borde de la línea y el borde del pad. Zoom de la zona del reed mirado (`salida/zoom_reed.png`): la línea
llega hasta casi el pad, no quedó cortada de más, y `SW1` + `REED: FIJAR CON RTV` se leen.
**Nota fina para @esquematico:** los 0,13 mm son al EJE de la línea; con el ancho de 0,12 el aire real es
0,07. Pasa porque este proyecto tiene `min_silk_clearance = 0`; si alguien la sube a 0,15 el aviso vuelve.
El valor a prueba de balas sería `SILK_FIN = pr − PAD/2 − 0,13 − ancho_linea/2`.
El netlist no cambió: 57 componentes / 50 redes, conectividad idéntica (`DIFF_REDES_revC_revD.txt`).

### Lo que mandó el layout: L10, que no estaba en la lista original
@verificador (H-2) encontró que **la restricción más dura faltaba**, y de paso corrigió un hallazgo
previo suyo: no es el Kelvin de `REFP1` (58 ppm = 0,06 µε, ganancia, se calibra), es que
**`R1.1` y `R2.1` tomen `+3V0` en el MISMO punto**: 20 mΩ de cobre entre las dos tomas = 85 µV =
**56,7 µε de cero corrido**, con 0,22 µε/°C de deriva. **Tolerancia para 1 µε: 0,35 mΩ.**
- **Estrella de excitación**: el nudo (52,30 · 24,50), con `R1.1` y `R2.1` llegando por ramales
  **espejados de 3,53 mm exactos**. Como las dos ramas consumen la MISMA corriente (3,0 V/700 Ω =
  4,29 mA), dos ramales iguales dan dos caídas iguales y **la asimetría se cancela exactamente**.
  Medido por script: **0,000 mm → 0,00 µε**. El Kelvin de AVDD/AIN0 sale de ese mismo nudo.
- **Estrella de retorno**: (49,81 · 8,00). `R3.2` entra con un ramal de 4,00 mm y de ahí sale el
  Kelvin a `REFN1`. Lo de aguas abajo (20 mm con 8,6 mA) es ganancia, no cero.
- **El ramal A no lleva nada más**: ni un pull-up. `RR1` se mudó al lado del ISP y se alimenta por el
  corredor este **justamente para no colgarse del Kelvin** (el A* quería conectarlo ahí: falló, y
  fue una suerte que fallara — quedó como ruta a mano).

### Tres decisiones de placement que son el orden de los pines, no estética
1. **`U1` (CJMCU) a 270°**: sus 4 pines analógicos quedan en el extremo OESTE de las dos filas y los
   digitales en el ESTE. Cero cruces entre el filtro y el ADC.
2. **`U2` (DIP-28) a 90°** y con el `cx` elegido para que **`U1.15/16` caigan justo sobre `U2.18/17`**:
   MISO y MOSI son dos bajadas rectas de 20 mm sin un codo.
3. **`U3` (RA-02) a 270°**: la fila del SPI mira al micro y `3V3/RST/DIO0` al norte, donde está la
   franja libre con `CR1/CR2`; el IPEX queda en la esquina NE, contra la pared del SMA.
4. Y el que resolvió el abanico del sur: **los destinos al sur del micro se colocaron EN EL ORDEN DE
   SUS PINES** (RR1/J3 al oeste, reed al SO, LED y radio al este). Con eso el abanico se dibuja con
   carriles paralelos y quedan sólo dos cruces topológicamente inevitables.

### Los tres carriles del bloque analógico
Las tres alturas de los pines de `J1` (E− 17,46 · S+ 22,54 · A 27,62) SON los tres carriles, y cada
uno **pasa por debajo del cuerpo de vidrio de sus dos clamps**, entre los pads: el carril no esquiva
a los diodos, los atraviesa por su nodo. Eso permitió los 6 clamps EN el conector (C31) sin deformar
nada. La columna de precisión es un solo eje `x = 46`, seis resistencias, ordenadas por cómo entran
y salen las redes (`NODO_B` un tramo de 10 mm entre tres pads contiguos, `NODO_A` otro de 5).
`CD1` quedó **centrado entre los dos carriles**: derivaciones de 7,5 mm exactos a cada lado.

### La doctrina de capas que cambió respecto de la rev C (y es lo que arregla su debilidad)
En una placa **toda pasante**: (a) una red entre dos pads pasantes se tiende entera por B.Cu **sin
una sola vía** — el costo no es eléctrico, es el TAJO al plano; (b) los 38 pads de masa pasantes
**cosen F.Cu con B.Cu**, así que un tajo en B.Cu queda puenteado por el relleno de F.Cu.
→ **F.Cu**: todo lo analógico, los rieles de +3V0 y el SPI. **B.Cu**: plano + las señales lentas.
→ Dos **rule areas** prohíben pistas de B.Cu bajo el ADC y bajo el radio: medido, **0 y 0 tramos**.
**La debilidad principal de la rev C (30 segmentos cortando el plano bajo el ADC de 24 bits) está
resuelta.** Aceptado y declarado: 8 tramos bajo el zócalo del micro.

### El router A* de Termovigía, cosechado y arreglado
El abanico digital del sur es **river routing**, no criterio: lo cerró `pcb/rutear_astar.py` (copiado
de `frioseguro/.../pcb/rutear_astar.py`, adaptado a 120×90 y origen 0,0) sobre la base hecha a mano,
con las rule areas puestas. **21-25 enlaces según la corrida**. Tres arreglos que valen para la biblioteca:
1. **Una rule area vale para LAS CAPAS QUE DECLARA, no para las dos.** El original bloqueaba
   `m[:, ...]`, así que los keepouts de B.Cu bajo los módulos dejaban a sus pads **sin una sola celda
   libre en F.Cu**, y el router informaba `grupo sin celda libre` sin decir por qué.
2. Si el A* devuelve un camino **degenerado** (0 tramos y 0 vías) el `while` no progresa y queda en
   **bucle infinito** hasta `MAX_PARES`. Hay que declarar el par abierto y seguir.
3. `CLR = 0,30` no deja pasar entre pads de header a 2,54 (0,84 mm de aire entre bordes): con 0,24
   entra una pista de 0,3 con 0,39 a cada lado.

### Bug propio nuevo del generador (familia de los cinco anteriores)
**Un courtyard dibujado como CÍRCULO se guarda con `(center)` y `(end)`: leer sólo esos dos puntos da
una caja del ANCHO DEL RADIO, no del diámetro.** Los electrolíticos radiales D5.0 quedaban declarados
de **4,55 × 1,60 mm (el tamaño de sus PADS)** en vez de 5,5 × 5,5 → `chequear_solapes` decía "sin
solapes" y el DRC cantaba `courtyards_overlap`. Arreglado en `courtyard_bbox()`: para `fp_circle` se
calcula el radio y se usa centro ± r.

### Serigrafía: la regla que faltaba
`rotular.py` evitaba solaparse con otra serigrafía, pero **no con los PADS**. En una placa que se
puebla a mano, tinta sobre el cobre donde va el estaño es un defecto real, no cosmético: agregando
los bounding boxes de todos los pads a la lista de ocupados, los avisos pasaron de **11 a 2** (y los
2 que quedan son de la huella del reed, §arriba). 57/57 referencias colocadas, **0 escondidas**.
Rótulos nuevos en cobre: `E-/REFN NO ES MASA`, el pinout de la galga, `PAD ANT: NO POBLAR`,
`SIN ANTENA NO ALIMENTAR`, `REED: FIJAR CON RTV`, `D4 = UNICO SMD` y —el que más importa—
**`J4: +C1 GND +C2 GND — 2 CELDAS EN PARALELO CON DIODO — NO PUENTEAR`**.

### Herramienta nueva: `pcb/verificar.py`
El DRC dice si la placa es **fabricable**; esto dice si es **la placa que se diseñó**. Chequea sobre
el board ruteado: las dos estrellas (largo real de cada ramal recorriendo el cobre), que `/E_REFN` no
tenga zonas ni pads de más, B.Cu bajo U1/U3, las 8 distancias de desacople, L1 (calor vs. precisión,
mismo eje, misma columna), la simetría del filtro y la mecánica. **Devuelve 1 si algo falla** →
entra en el DoD de cualquier revisión futura.

**Propiedad honesta del entregable, encontrada al re-correr:** la placa **se regenera** con un comando,
pero **no es bit a bit reproducible**. Tres pasadas sobre la misma entrada dieron 338, 349 y 351 segmentos:
lo ruteado a mano es determinista, lo que cierra el A* no. Por eso `pcb/verificar.py` corre en cada pasada
y entra en el DoD: **lo que se garantiza no son las coordenadas, son los criterios**, y se vuelven a medir
sobre el board cada vez (las dos estrellas dieron 3,53/3,53 mm y 0,00 µε en todas las corridas).
Está escrito en `LAYOUT.md` §12.1 y en el dossier, y el número de tramos de B.Cu bajo el zócalo del micro
**ya no se tipea**: sale de `salida/verificacion.json`.

**Renombre de @esquematico, anotado para no citar mal:** `D1`…`D14` de `NOTAS_REV_D.md` pasaron a
**`DE-1`…`DE-14`** para no chocar con los designadores reales (`D11 D12 D21 D22 D31 D32`, que quedan
intactos en la placa). Los nombres viejos siguen valiendo como alias; el mapeo está al principio de C40.
Lo que me bloquea sigue siendo lo mismo con otro nombre: **DE-1 = M1** (RA-02) y **DE-2 = M2** (CJMCU).

**Pendientes:** **M1** (separación entre filas del RA-02 con adaptador: 17,8 mm = paso 2,54 y esta
huella sirve; 14,0 = módulo pelado y hay que panelizar un adaptador) y **M2** (calibre al CJMCU).
Ninguna cambia una red: cambian los 32 agujeros de los dos módulos. **Hasta que estén, no hay
gerbers.** Para @esquematico: la línea de serigrafía del reed. Para @diseno3d: `LAYOUT.md` §10 (tabla
de agujeros y conectores) + el `.step` y el `.glb` ya exportados.

## 2026-09-02 (b) — GALGAS / DREYFUS: placa CERRADA, gerbers PRELIMINAR

Con P6b aprobado. `C:\Proyectos\galgas\hardware\kicad\` — board, `LAYOUT.md`, `drc.rpt`,
`salida\pcb_2d_top.png` + `pcb_3d_top/bottom.png`, `gerbers\` + `nodo_galga_v3_gerbers_PRELIMINAR.zip`
(27 archivos: gerbers, PTH/NPTH drl con mapas, pos, BOM de 35 líneas). Sin commit.

**Estado medido:** 55/55 componentes, 51 redes, **400 segmentos + 113 vías**,
**DRC `--severity-all` = 0 errores**, **2 pads sin conectar**, **0 `silk_overlap`** (eran 27) y
3 `silk_over_copper` (eran 24). Renders 2D y 3D top/bottom **mirados**.

**Los 2 sin conectar tienen nombre: `U2.3` y `U2.5`, los GND del ATmega.** El pin 21 (tercer GND
del mismo chip) sí está conectado y los tres están unidos internamente al lead frame: la placa
funciona, lo que se pierde es inductancia de masa. **No se cerró por geometría, no por falta de
intentos** — los cinco caminos probados y por qué falla cada uno están en `LAYOUT.md` §7. El
hallazgo que los explica: **el relleno que queda DENTRO del anillo de pads de un TQFP es siempre
una isla** (huecos de 0,25 mm a paso 0,8 contra 2 × 0,25 de clearance de zona), así que una vía de
masa ahí adentro no conecta con nada. Fix de una línea para la rev D: sacar CAL_EN del carril
oeste del micro.

**Lo que pidió el Director, hecho:**
- **Ruteo digital y de potencia completo**, incluido `/V_SC_MID` (las dos celdas en serie con
  RB1/RB2 colgando del nodo del medio). Potencia a mano por carriles paralelos que no se cruzan:
  +BATT por el norte (y = 50), /V_SC por el sur (y = 56,5).
- **Serigrafía**: de 51 avisos a 0 solapes. Referencias reubicadas por búsqueda EN ESPIRAL
  alrededor de cada componente (las 4 posiciones fijas chocan casi siempre en esta densidad), con
  el dibujo de serigrafía de las huellas y los rótulos fijos reservados ANTES. 12 rótulos útiles:
  título/versión/fecha/NS, pinout de la bornera de galga, ISP, serie, `ANT IPEX -> SMA`,
  `PAD ANT: NO POBLAR`, polaridad de los supercaps y **`E-/REFN NO ES MASA`** en el cobre.
- **G18 cerrado sin net-tie**, como ordenó el Director, con la medición como fundamento: la
  derivación de REFP1 sale del ramal A a 2,4 mm de R1.1 → 6,7 nV de cobre compartido = 2 ppb.
  La condición que el net-tie iba a imponer queda como regla escrita en `pcb/rutas.py`.
- **Corredor del ramal A**: área con nombre en la placa + regla propia en
  `nodo_galga_v3.kicad_dru` que **prohíbe POR RED** que el SPI y el DRDY entren en la franja. Un
  keepout común no servía (echaría también al riel). El DRC lo verifica en cada corrida.
- **Gerbers PRELIMINAR**, con los tres bloqueos y qué se rehace si cae cada uno (LAYOUT.md §11).

**Corrección honesta sobre la costura de vías que yo mismo había propuesto:** con plano en una
sola cara, una vía de costura NO conecta a nada en F.Cu — queda colgada y es decoración. Se probó
con relleno en las dos caras y **salió peor**: en la zona densa F.Cu se parte en slivers y cada
sliver que atrapa un pad SMD de masa deja ese desacople FLOTANDO (pasó con CA1, CB1, CM1, CM2, CM3).
Lo que quedó: relleno en las dos caras + **una vía de masa al lado de cada uno de los 4 cambios de
capa** (que es la costura que sí sirve) + grilla de ~10 mm en zonas libres + una vía por cada pad
que el relleno no alcanza, encontradas con `pcb/cerrar_gnd.py`.

**LA DEBILIDAD PRINCIPAL DE ESTA PLACA, dicha sin maquillaje:** 105 de los 400 segmentos van por
B.Cu y **30 caen dentro del courtyard de U1 o U2**. El haz digital de FreeRouting corta el plano
justo debajo del ADC de 24 bits. Se ve en el render inferior. Se intentó arreglar de dos maneras y
las dos fallaron **por herramienta**: (a) declarar B.Cu `(type power)` en el DSN — el DSN sale
bien pero con una sola capa de señal FreeRouting no converge; (b) rule areas prohibiendo pistas
por B.Cu bajo U1/U2/U3 — anda para el DRC pero FreeRouting abre una ventana y no termina nunca.
Queda para la rev D, a mano: son 6 redes cortas.

**Cambios de placement de esta tanda, todos con motivo:** CM3 (AREF) y CM2 movidos porque sus pads
de masa quedaban en bolsones; CM1 rotado 180 por lo mismo; RL1/LD1 rotados 180 para que los ánodos
queden adyacentes (estaban en los pads lejanos y el LED pedía rodear los dos cuerpos); CI1 al este
de U4 para que +BATT y /V_SC no se crucen; RGD1 rotado 90; los 4 agujeros M3 ahora tienen
referencia HM1..HM4.

**Trampas nuevas del harness (todas costaron tiempo real):**
1. `ExportSpecctraDSN` devuelve False sin mensaje si hay huellas con la MISMA referencia — los 4
   agujeros M3 tenían la referencia vacía y contaban como duplicados.
2. **`ImportSpecctraSES` REEMPLAZA todas las pistas y vías.** Las pistas protegidas vuelven; las
   vías NO. Hay que reponerlas después (`rutear.py --solo-vias`), y si se cambia una ruta hay que
   re-correr FreeRouting o el `.ses` viejo la pisa.
3. **KiCad le asigna a una vía nueva la red del cobre que toca**: dos vías de masa mías cayeron
   sobre pistas del autorouter y se volvieron CAL_EN y PB0 en silencio.
4. `pcbnew.VIATYPE_THROUGH` ya no existe; un `PCB_VIA` nace THROUGH y se posiciona con
   `SetStart`/`SetEnd`.
5. `EDA_TEXT.GetTextBox()` **pide un argumento** (`None` anda). Estimar la caja a mano da cajas
   chicas y el DRC canta los solapes igual.
6. `meta.version 1` en el `.kicad_pro` hace que KiCad **descarte `net_settings` en silencio** y
   vuelva a su Default interno de 0,2 mm. Tiene que ser 3.
7. FreeRouting **abre la ventana** de forma intermitente y el proceso no termina nunca
   (`Get-Process java | select MainWindowTitle` lo delata). **No se arregla con
   `-Djava.awt.headless=true`**: con eso arranca y no rutea nada (97 pads sin conectar). Matar el
   java y volver a correr.
8. Rotar una huella rota la posición de los pads pero **no su forma**: hay que sumarle la rotación
   al ángulo de CADA pad. En un 0805 casi no se nota; en un TSSOP a paso 0,65 los pads quedan
   apilados (61 errores de DRC).
9. El heredoc de bash se rompe con contenidos largos aunque esté citado: para archivos de más de
   ~100 líneas, tool de escritura.

**Pendientes:** rev D — sacar CAL_EN del carril del micro (cierra los 2 sin conectar) y rehacer a
mano el haz digital por F.Cu; fiduciales y test points; P3/CSC/P2/P10 antes de fabricar.

## 2026-09-02 — GALGAS / DREYFUS: ruteo del bloque analógico, netclases y antena (rev C, PRELIMINAR)

`C:\Proyectos\galgas\hardware\kicad\` — `nodo_galga_v3.kicad_pcb`, `LAYOUT.md`, `drc.rpt`,
`salida\pcb_3d_top.png` / `pcb_3d_bottom.png`, toolchain nuevo en `pcb\`
(`rutas.py`, `rutear.py`, `netclases.py`, `rellenar.py`). **Sin commit, sin gerbers** (orden).

**Estado medido:** 55/55 componentes (netlist rev C), 51 redes, **81 segmentos + 12 vías**,
**DRC `--severity-all` = 0 errores**, 0 solapes de courtyard, **89 pads sin conectar** (alcance
declarado: falta el digital y la potencia a propósito), 50 avisos de serigrafía (deuda escrita).
Renders 3D top/bottom **mirados**.

**La sesión cambió de objetivo dos veces en vuelo** y la placa lo aguantó: primero @hardware cerró
P8/P9 (supercap partido en 4 cuerpos, D4 a SOD-523), después @verificador **rechazó P6** y
@esquematico entregó la **rev C** con 10 componentes nuevos, 12 referencias renumeradas y las
4 redes analógicas rebautizadas. **Las netclases y el bloque analógico ruteado sobrevivieron sin
tocar una sola coordenada**, porque todo está anclado **POR PAD y no por nombre de red**. Esa
decisión de diseño se pagó sola el mismo día.

**Tres defectos de layout que un DRC 0 no ve, encontrados y corregidos:**
1. **El ADS1220 estaba mal orientado.** Sus 4 pines analógicos (7/8/9/10) están todos en UN
   extremo del TSSOP y los digitales en el otro; con U1 a 0° ese extremo miraba al sur y
   SCLK/CS/CLK quedaban enfrentados al bloque analógico. Rotado a 270°, y **el front-end se
   rehízo entero** (R3/R2/R1, RS2/RS1, CC2/CD1/CC1 reordenados de norte a sur) para que el orden
   físico de las señales sea el orden de los pines: cero cruces entre S+, S−, REFN y REFP.
2. **`RG1` (pull-down del gate de Q2, el FET de la pila) vivía en el bloque analógico**, a 30 mm
   de su transistor. Movido junto a Q2.
3. **`CBLK1` era "reserva de bloque" a 32 mm del radio.** Es el único bulk del riel del lado del
   RA-02 y de ahí sale el pulso de TX de 120 mA: movido a la esquina de potencia del módulo
   (+3V0 a 8,6 mm, GND a 7,0 mm).

**El Kelvin de REFP1, que es el punto fino.** REFP1 (pin 11) y AVDD/DVDD (12/13) son la MISMA red:
el esquemático no puede dar el Kelvin, lo da la geometría. Dos ramales que se juntan **en el LDO,
no en el chip**: ramal A (0,8 mm) lleva SOLO la excitación del puente (4,5 mA) al tope R1.1/R2.1,
y REFP1 se deriva a 2,4 mm de R1.1 → cobre compartido = **6,7 nV sobre 3 V = 2 ppb**. El consumo
propio del ADC (350 µA) va por el ramal D y no aparece en la referencia. R1 y R2 se colocaron
adyacentes (2,2 mm): con 10 mm entre ellos los 4,3 mA del brazo de la galga habrían metido 43 µV
= **29 µε de offset**.

**E−/REFN verificado en la placa, no sólo en el `.net`**: camino continuo `J1.3 → Q1.2 → D3.2 →
R3.2 → U1.6` sin una sola vía a masa. No lleva Kelvin **a propósito** (por el pin 6 circula toda
la corriente de excitación): se compensa con ancho y cortedad, 0,5 mm → 39 ppm fijos.

**Sólo 2 ranuras en el plano** (2,3 y 4,7 mm), las dos sobre `+3V0`, ninguna bajo el RA-02.
Un tercer cruce (`/NODO_A` contra el riel de E−) **se resolvió moviendo el ramal de calibración**
al sur del riel, no metiéndole vías a un nodo del puente.

**G8 — antena DECIDIDA: IPEX, el pad ANT sin poblar.** Motivo con número: una línea de 50 Ω en
2 capas FR4 1,6 mm pide ~2,9 mm de microstrip y la alternativa coplanar **no se puede validar sin
VNA**; con IPEX toda la cadena de 50 Ω está dentro del módulo. Además el nodo va en caja estanca
sobre un REDLER que vibra. Consecuencia para @diseno3d: pasamuros SMA en la pared derecha y
**≥ 12 mm libres sobre el módulo**. Y para @esquematico: que el símbolo diga el porqué.
Corolario que hay que entender: para un módulo apantallado con IPEX, el "keepout de antena"
clásico (vaciar cobre) **sería un error** — el plano va entero abajo, verificado en el render.

**Netclases (G9) al `.kicad_pro`, definidas POR PAD**: `EXCITACION` 0,5 / `ANALOGICA` 0,3 /
`ALIMENTACION` 0,8 / `GND` 0,6 / Default 0,3. Los 0,8 mm no los pide la ampacidad (IPC-2221 da
2,4 A, 20× el pulso de 120 mA) sino la **caída**: el presupuesto del pulso ya usa 132 mV de 420 y
el cobre suma 9 mV. `ANALOGICA` quedó en clearance 0,25 y no en 0,30 porque KiCad aplica la clase
GLOBALMENTE y el TSSOP de paso 0,65 no admite 0,30 — los ≥0,30 reales se consiguen por ruteo.

**Bug propio #4 del generador (familia de los tres de agosto): rotar una huella rota la POSICIÓN
de los pads pero NO su FORMA.** El ángulo del pad va en su propio `(at x y ANG)` y si no se
escribe queda 0. En un 0805 casi no se nota; en el TSSOP-16 de paso 0,65 con pads de 1,475 × 0,40
a 270° los pads quedan **apilados, solapándose 0,825 mm**: 33 `solder_mask_bridge` + 28
`shorting_items`. Arreglado sumando la rotación de la huella al ángulo de cada pad.

**Trampas nuevas del harness KiCad 10 + Python:**
- **`meta.version 1` en el `.kicad_pro` hace que KiCad DESCARTE `net_settings` en silencio** y
  vuelva a su Default interno de 0,2 mm. Tiene que ser `3` (además de `net_settings.meta.version 5`,
  ya conocido de Termovigía). El guardia de relectura por `GetNetClassByName` lo cazó.
- **`pcbnew.VIATYPE_THROUGH` ya no existe** en KiCad 10; un `PCB_VIA` nace THROUGH (tipo 4).
- Una vía se posiciona con `SetStart`/`SetEnd` (es un segmento de largo cero).
- **El heredoc de bash con contenido largo se rompe** aunque esté citado: para archivos de >100
  líneas, usar la tool de escritura, no `cat <<EOF`.

**Pendientes / entregado a otros:**
- El ruteo digital + potencia se corre **una sola vez**, contra el netlist rev C ya verificado.
- @esquematico: nota del pad ANT en el símbolo (G8).
- @diseno3d: tabla de agujeros/conectores en `LAYOUT.md` §5 — la PCB manda. Ojo `CSC1/CSC2`:
  13,5 mm de alto y a 0,71 mm del borde inferior.
- Serigrafía (50 avisos), fiduciales y test points: pendientes para la pasada final.
- Corregido de paso, por pedido: `perfboard/GUIA_ARMADO_PERFBOARD.md` §8.1 estaba **al revés**
  (los 2 HT7130A son el LDO de la **Placa A**, no de la B) + aviso grande de que el **MCP1700
  cambia de pinout entre SOT-23 y TO-92** y el símbolo usa el del SOT-23 (en la PCB va SOT-23:
  para el layout no cambia nada, el que se quema es el banco).


## 2026-08-21 — Layout del nodo de galga: placement completo, DRC 0

**Entregable:** `C:\Proyectos\galgas\hardware\kicad\nodo_galga_v3.kicad_pcb` (abrir con KiCad 10)
generado por `generar_pcb.py` — el placement vive como DATO en la tabla `PLACEMENT`
del script: mover un bloque es cambiar una coordenada y regenerar, no arrastrar
45 huellas a mano y perder el criterio.

**Estado medido (no declarado):**
- 45 de 45 componentes colocados, todos con su referencia y valor.
- **DRC: 0 violaciones** (`kicad-cli pcb drc --severity-error`, reporte en `drc.rpt`).
- 108 pads sin conectar = **NADA está ruteado todavía**. Es lo esperado: falta el ruteo.
- Placa 100 × 70 mm, 4 agujeros M3, plano de masa en B.Cu.

**Placement por bloques** (flujo izq→der, sin volver atrás):
`J1 galga → TVS → puente+shunt-cal → filtro RC → ADS1220 → ATmega → RA-02 (antena al borde derecho)`,
con la cadena de alimentación en la franja inferior (BT1 ocupa x 2..60; el resto a su derecha).

**Tres bugs propios encontrados y corregidos** (valen para el próximo layout por script):
1. **Rotación 180°**: intercambiar ejes sólo sirve para 90/270. Con 180 la caja queda
   del lado equivocado del origen → una bornera "adentro" con pads FUERA del borde.
   Ahora se rotan las 4 esquinas de verdad.
2. **Origen ≠ centro**: el portapilas se extiende 55 mm hacia un lado desde su origen.
   Colocar "por origen" es a ciegas → ahora se coloca por CENTRO del bounding box.
3. **KiCad 10 usa `(property "Reference" ...)`**, no `(fp_text reference ...)`. Apuntar
   al formato viejo dejaba las 45 huellas como `REF**` y la placa ilegible.
   (Además: el bounding box debe ser la UNIÓN de courtyard y pads — hay huellas
   cuyos pads sobresalen del courtyard.)

**Sujeto a P8/P9** (anotado en la capa Cmts.User del propio board): CSC (supercap) y D4
llevan footprint tentativo; si cambia el componente, cambia la huella.

**Pendiente para @esquematico:** el símbolo del RA-02 en `galgas.kicad_sym` tiene numeración
de pines que NO coincide con el módulo físico (si se asigna el footprint Ra-01 oficial tal cual,
**3V3 cae en un pad de GND**). Se resolvió con `galgas.pretty/RA-02.kicad_mod` renumerado para
calzar con el símbolo, pero conviene arreglarlo en el símbolo.

**Próximo paso:** rutear. Prioridad: (1) analógico — S+/S− cortas y lejos de digital, Kelvin
de REFP1 entre R1 y R2, **E−/REFN NO al plano de masa** (va sólo al pin AIN3); (2) alimentación;
(3) digital y RF con keepout de antena.

- 2026-09-02 [FRIOSEGURO / TERMOVIGIA Base v2 — layout rev B.1, PRELIMINAR] `C:\Proyectosrioseguro\hardware2	ermovigia_base\`
  (`termovigia_base.kicad_pcb`, `LAYOUT.md`, `drc.txt`, `salida\pcb_top/bottom/3d.png`, `gerbers\` PRELIMINAR,
  toolchain en `pcb\`). 143 componentes / 84 redes del `.net` de la rev B.1 (@esquematico), placement por bloques,
  potencia y buses a mano (`pcb
utas.py`, por pad), señales con FreeRouting, GND en las dos capas cosido.
  - **HALLAZGO PARA EL DIRECTOR: 120 x 100 NO ENTRA.** Cuenta con courtyards reales: 16.900 mm2 de cuerpos (7.400
    pasivos/conectores + 5.620 DevKit/3xLM2596/BK-A7670 + 3.900 los 2 modulos de rele) contra 12.000 de placa = 141 %
    antes de rutear. Hice la placa en **160 x 155** (68 % de ocupacion, M3 a 4 mm de las esquinas). El gabinete
    es parametrico (`pcb = [160,155,1.6]`): externo 190 x 185, 218 con orejas (Ender 3: al limite; acortar orejas).
    Alternativas descartadas con numeros en LAYOUT.md par. 1 (reles elevados sobre pasivos, reles fuera de la placa).
  - Decisiones de layout: DevKit con USB al borde superior (cara a 1,3 mm: ventana `usb_ventana`) y antena hacia
    adentro sobre keepout SIN RELLENO (pistas permitidas: el DevKit va en zocalo y si no, la columna derecha queda
    inalcanzable); pila de 3 LM2596 con U104 abajo (junto a la bateria), U102 medio, U103 arriba (junto al modem);
    modem en el borde derecho con el IPEX hacia la pared del SMA, C502 a 11 mm de V, C104 a 9,5 mm de U103.OUT+;
    barrera de los PC817 = una recta (los dos DIP alineados) con keepout de 6 mm; R114 a 6,5 mm de F102.1 en stub
    recto (H33); pinza con burden a 5 mm del jack y CT_BIAS en estrella de 8 mm; LEDs en (39,8,148,5)/(39,8,138,5).
    Prensacables y agujeros que el gabinete tiene que seguir: tabla en LAYOUT.md par. 2 (la PCB manda).
  - Netclases: POTENCIA/MODEM 1,5 mm (2 A), ALIM 1,0, senal 0,3; clearance Default/GND 0,20 (el TO-92_Inline tiene
    0,22 entre pads), pads de zocalos/headers de modulos 1,5/1,0 (con 1,7 no pasaba nada entre pines).
  - **Trampas nuevas del harness KiCad 10 + Python** (todas costaron > 20 min): (1) `ExportSpecctraDSN` devuelve
    False sin mensaje si hay dos huellas con la misma referencia (los 8 agujeros de los modulos eran "HR");
    (2) `PCB_VIA.GetWidth()` SIN capa y `GetBoundingBox()` sobre pistas del .ses abren un "wxWidgets Debug Alert"
    MODAL: el proceso queda colgado para siempre (`Get-Process python | select MainWindowTitle` lo delata);
    (3) `ZONE_FILLER.Fill()` sobre una rule area se cuelga; (4) el `.kicad_pro` con `net_settings.meta.version 4`
    se ignora y KiCad lo pisa con Default 0,2 al proximo Save — hay que escribir `version 5` + `tuning_profile`;
    y el chequeo de lectura es por NOMBRE DE CLASE (`GetNetClassByName("POTENCIA")`), con nombre de red devuelve
    Default; (5) `PCB_SHAPE.SetArcGeometry(start, mid, end)` para arcos; (6) el jack CUI SJ1-3523N trae un recorte
    en Edge.Cuts que rompe el contorno: borrar los items de Edge_Cuts de la huella al cargarla; (7) el DevKit sobre
    el agujero M3 de la esquina = `courtyards_overlap` aunque el tornillo quede debajo del zocalo.
  - Para @bibliotecario (cosechar en `pc\kicad_gen\` o `pc\kicad_pcb\`): `pcb\gen_pcb.py` (placa desde .net +
    placement + rutas por pad, keepouts derivados), `chequear_solapes.py` (courtyards con cajas exactas),
    `netclases.py` (con guardia y readback), `autorutear.py`/`importar_ses.py`/`cerrar_ruteo.py`/`coser_rellenar.py`
    (cadena FreeRouting con pistas protegidas), `rotular.py` (referencias en lugar libre), `render2d.py` (svg->png
    con pymupdf), `gen_modelos3d.py` (cajas VRML para modulos sin modelo), `verificar.py` (DRC+metricas+renders+
    gerbers+glb/step), `rutear_astar.py` (router A* sobre grilla 0,25 mm, 2 capas con vias, para lo que FreeRouting
    deja abierto: se probo con 3 redes de 40-130 mm y con islas de GND).
  - **Resultado final**: DRC `--severity-all` **0 errores / 0 sin conectar** (200 avisos de serigrafia: referencias
    encimadas), 0 solapes de courtyard, 787 segmentos + 354 vias, 44,5 % de segmentos en B.Cu (deuda: rev C a mano
    por F.Cu), caidas < 180 mV @ 2 A en toda la potencia, desacoples medidos (LAYOUT.md par. 7). Renders 2D/3D
    MIRADOS y corregidos (modulos de rele dibujados 40 mm abajo por el signo Y del VRML). Gerbers PRELIMINAR +
    glb + step. Mas trampas: (8) KiCad asigna a una via nueva la red del cobre que toca -> con las zonas rellenas
    una via de senal nace GND (cortocircuito): `UnFill()` antes de agregar vias; (9) `b.Remove(via)` con relleno
    previo -> segfault (exit 139): la costura ahora es aditiva/idempotente sin borrar; (10) DRC sin relleno previo
    = todos los pads de GND "sin conectar" (el A* se puso a unir 149 islas): rellenar SIEMPRE antes del DRC;
    (11) `Fill()` con rule areas en la lista se cuelga; (12) pads cuadrados: el obstaculo es la semidiagonal.
  - **Pendientes (LAYOUT.md par. 10)**: decision del Director sobre 160 x 155; mediciones de Gonza (martes) en
    `gen_huellas.py`; @diseno3d con la tabla de prensacables/LEDs/USB; serigrafia a mano (36 refs); rev C con el
    haz DevKit-borneras a mano por F.Cu. Nada commiteado (orden).

- 2026-09-02 [FRIOSEGURO / TERMOVIGIA Base v2 rev B.1] **DOSSIER en UN PDF, para el celular y para Gonza/Sergio**:
  `C:\Proyectos\frioseguro\hardware\v2\termovigia_base\TERMOVIGIA_BASE_v2_revB1_DOSSIER.pdf`
  (**43 paginas, 4,17 MB**, A4, numerado, con marcadores/TOC) generado por `armar_dossier.py` (misma carpeta).
  - Contenido: portada con logo + render 3D · indice · resumen de 1 pagina · **esquematico 6 hojas** (A3 -> A4
    apaisado, vectorial: zoom sin pixelar) · tabla GPIO + reglas de firmware + IO35/IO39 + poblar E/P ·
    layout (top, bottom, 2 renders 3D, mapas de taladro PTH/NPTH) · **7 capas de fabricacion**
    (`kicad-cli pcb export pdf --mode-multipage --include-border-title --drill-shape-opt 2`) · **BOM de 72 lineas**
    en apaisado con la columna Poblar sombreada · pendientes y deudas · anexo del gabinete.
  - **Regla del script: ningun numero tipeado a mano.** Lee la BOM (143 comp.), el `.net` (84 redes), el
    `.kicad_pcb` (bbox de Edge.Cuts = 160 x 155, 787 segmentos / 354 vias / 151 huellas), `drc.txt`
    (0 err / 0 sin conectar / 200 avisos de serigrafia), `erc.txt`, `salida/verificar.txt`, y trae las secciones
    de LAYOUT.md / DISENO.md / PINOUT.md / las 3 VERIFICACION_*.md por regex de titulo (conversor markdown->HTML
    propio). Si cambia el layout, se re-corre y el PDF queda al dia.
  - **Deudas puestas en el PDF, no escondidas**: 44,5 % de segmentos en B.Cu, antena con pistas debajo, 36 refs
    de serigrafia, desacoples de 5,9 y 12,6 mm aceptados con razon, veredictos de las 3 auditorias y H31-H37
    abiertos. Ademas **drift detectado al mirar el render**: el cajetin del esquematico todavia dice
    `PCB 120 x 100` y los M3 viejos -> nota en la portadilla del esquematico (no cambia ninguna red).
  - Toolchain (para @bibliotecario): PyMuPDF **`fitz.Story` + `DocumentWriter`** para texto/tablas paginadas
    (el `story.draw(page)` NO existe: hay que dibujar sobre el *device* del writer), `@font-face` con
    `C:\Windows\Fonts` via `fitz.Archive` para tener Ω/µ/×; **`width="%"` en los `<th>` es obligatorio** o las
    columnas de la derecha se caen fuera de la hoja; U+200B despues de `_ : - /` para que las huellas largas
    corten de linea; `insert_text` usa Latin-1 (los "—" salen como "?"): sanitizar; recorte del marco blanco
    de los PNG y de las paginas PDF (mapas de taladro) por bbox de tinta con PIL, si no se anexa medio A4 vacio.
  - Verificacion: contact sheet de las 43 paginas + 13 paginas renderizadas y MIRADAS a 115-125 dpi. Se
    corrigieron mirando: logo negro sobre azul (placa blanca), BOM con 3 columnas caidas fuera de la hoja,
    imagenes centradas con pie que no entraba, mapas de taladro al 25 % de la hoja, y **`redes = 0`** (el
    `.net` de KiCad 10 pone `(net` y `(code` en lineas distintas).

## 2026-09-02 — FRIOSEGURO KIT v1: plano de la PLAQUETA PERFORADA (no hay PCB)

`C:\Proyectos\frioseguro\hardware\v1_modulos\plaqueta\` — `plano.py` (generador, fuente unica),
`plano_componentes` / `plano_puentes` / `plano_soldadura` (.png + .pdf a escala 1:1),
`tablas.md`, `verificacion_netlist.txt`, `ARMADO_PLAQUETA.md`, `VERIFICACION_5_UNIDADES.md`.
**Sin commit** (orden). Trabajo distinto: **no se fabrica nada**, Gonza y Sergio sueldan 5
plaquetas perforadas PE04 150 x 56 identicas, agujero por agujero.

**Metodo (el mismo que el layout por script, aplicado a perfboard):** la grilla, el placement,
los 42 puentes y los rotulos viven en TABLAS de `plano.py`; los tres planos, las tres tablas de
coordenadas y la verificacion salen de ahi. Ninguna coordenada tipeada dos veces.
**Verificacion real, no declarada:** union-find sobre islas + rieles + puentes + patas, contra
`kit_v1_modulos.net`. **48 redes revisadas: las 11 con nombre tienen camino (OK), las 37
`unconnected-*` son de un solo pin** (25 pines libres del DevKit + 12 contactos de rele que salen
por la bornera del propio modulo). **179 agujeros ocupados, ninguno repetido** (el chequeo de
doble ocupacion es el "chequear_solapes" del mundo perfboard). Renders MIRADOS y corregidos en
3 iteraciones.

**Grilla declarada** (14 filas x 57 columnas, paso 2,54): P/Q rieles de arriba **NO SE USAN**
(los tapan las borneras) · A..E islas de 5 · canal · F..J islas de 5 · X = riel **GND** ·
Y = riel **+3V3**. Borneras con los pines en **fila A**, DevKit a caballo del canal en **filas
B y J** (columnas 39..57, USB al borde derecho = ventana del gabinete).

**42 puentes** (el BOM estimaba ~70): 14 pelados cortos, 25 aislados, 3 gruesos de 0,5 mm2 para
el +5 V. 20 de mas de 25 mm. El patron protoboard resuelve los otros ~28.

**Lo que el placement resuelve gratis, y es el punto del diseno:** cada bornera y su pasivo caen
en la MISMA isla vertical. C2/C3/C4 (100 nF) cruzan directo del borne de senal al borne de masa
de su propia bornera (5,08 mm = 2 columnas): **cero puentes**. R1..R4 van de la fila J al riel
+3V3, 11,9 mm, todas iguales. Los 3 ramales de +5 V salen de UNA isla (`FJ2`) = la estrella desde
J1 que pide `CABLEADO.md` 2.1, no una cadena.

**TRES HALLAZGOS QUE BLOQUEAN LA COMPRA (para @hardware / Matias):**
1. **7 borneras de 3 vias NO ENTRAN.** 7 x 15,24 = 106,7 mm de borde y el DevKit pide 51,5:
   158 > 150. Van **3 de 3 vias + 4 de 2 vias = 86,4 mm** (que es justo el numero que el propio
   BOM habia calculado en su 3.1). Corregir el renglon 2 del BOM.
2. **La bornera comprada es de paso 5,00 mm y la grilla es de 2,54.** Cuenta: 2 vias -> 0,08 mm
   de error (entra), **3 vias -> 0,16 mm (entra forzando el pin del medio)**, 4 vias -> no entra.
   Si todavia no se compro, pedir **5,08 mm (KF128-5.08 / XY308-5.08)**. Es el mismo error del
   banco de galgas (MX126-5,0) — segunda vez que aparece: **regla nueva: en perfboard, bornera
   5,08 SIEMPRE**.
3. **El gabinete de @diseno3d reserva `regleta = [100, 25]` y un carril propio para el ESP32.**
   Con esta plaqueta el ESP32 va en zocalo SOBRE la plaqueta: hay que poner `regleta = [150, 56]`,
   `regleta_ag = [134, 40.5]`, `regleta_alto = 25`, **eliminar el carril `esp*`** y alinear la
   ventana USB al borde derecho de la plaqueta (USB a y ~ 27 mm del borde de borneras).
   Separadores de **nylon**: el riel de +3V3 pasa a 4,7 mm del agujero M3 inferior.

**Decisiones de layout con razon (no "que no se solapen"):**
- Los rieles de ARRIBA se sacrifican a proposito: el cuerpo de la bornera los tapa y sus pines
  no pueden ir sobre un riel (cortocircuitaria las 7 borneras entre si). Se perforan para el M3.
- Los cabezales de rele fueron de la fila J a la **fila I** para que las patas de los 10 k
  opcionales (fila J -> riel Y) **no pasen por encima del conector**. Un puente que cruza un
  conector es una placa que no se puede desenchufar.
- 3 puentes de +3V3 marcados AISLADO no por largo sino porque **cruzan el riel de GND**.
- Debajo del DevKit los agujeros SI se usan por la cara de soldadura (el zocalo lo deja a 8,5 mm);
  debajo de las borneras NO (el cuerpo apoya en la placa): las filas B y C de esas columnas
  quedan muertas y el plano lo dice.
- Pinout de JR1/JR2 elegido **simetrico-seguro**: invertido, el 5 V cae en VCC-opto y el 3,3 V en
  JD-VCC -> los reles no accionan y no se quema nada.

**Pendientes:** (a) **PASO 0**: Gonza confirma con el tester el patron real de la PE04 (filas,
columnas, donde corta el riel) — si el corte no cae entre la columna 25 y la 31 hay que mover
2 puentes; (b) medir con calibre si las tiras del DevKit estan a 25,4 mm (10 pasos) o 22,86 (9):
si son 9, el zocalo baja a las filas **C y J** y se regenera; (c) medicion B del BOM 8.1 decide
si se pueblan R5..R8; (d) los 5 cambios del `.scad` para @diseno3d.
