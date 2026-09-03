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
