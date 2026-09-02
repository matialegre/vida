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
