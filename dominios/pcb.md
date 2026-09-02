# Dominio: pcb (agente @pcb)

Doc de dominio + bitacora. El agente lo lee al arrancar y lo actualiza al cerrar. Backlog inicial: ver seccion "Tu backlog inicial" en ~/.claude/agents/pcb.md (copia en ../agentes/pcb.md).

## Bitacora
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
