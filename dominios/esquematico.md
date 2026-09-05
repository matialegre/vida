# Dominio: esquematico (agente @esquematico)

Doc de dominio + bitacora. El agente lo lee al arrancar y lo actualiza al cerrar. Backlog inicial: ver seccion "Tu backlog inicial" en ~/.claude/agents/esquematico.md (copia en ../agentes/esquematico.md).

## Bitacora
- 2026-07-07 - Agente creado por Claude Fable con backlog real de los repos migrados (C:/Proyectos).

- 2026-07-08 [BRIEFING GIMAP] — leer ../BRIEFING_EQUIPO_GIMAP.md y los 4 docs (PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO). Para vos: la peluda analogica: (a) front-end Wheatstone con shunt-cal (R+relay/MOSFET por canal, INA precision, gateo del puente); (b) front-end PIEZO del lab (op-amp o puente diodos+cap). Protecciones TVS.

- 2026-07-30 [LASER-PCB] Placa de interfaz impresora->laser TTL + spindle DC: HECHA y verificada.
  - Entregables en C:/Proyectos/laser-pcb/esquematico/: INTERFAZ_LASER_DREMEL.md (calculos completos), BOM.md (precios AR estimados + 3 candidatos de modulo laser ML, recomendado el generico 5.5W 12V TTL ~$13-30k para quemar pintura), kicad/ con proyecto KiCad 10 REAL (interfaz_laser_dremel.kicad_sch/.kicad_pro/.pdf/.svg/.net + erc.rpt).
  - Circuito: 2x PC817 como front-end de las salidas de fan (LED del opto entre FAN+ y FAN-: resuelve low-side, nivel y aislacion; emisor-seguidor a +5V con pull-down 4k7 = TTL 0 seguro ante cable cortado); interlock clase 4 = llave + microswitch de puerta EN SERIE con la bobina de un SRD-12VDC que conmuta la POTENCIA del laser (no la senal); spindle IRLZ44N + SB560 + P6KE36A + fusible 6.3A; L7805 para el riel TTL; 3 fusibles por rama; LEDs armado/spindle. V_PSU 12V con valores 24V entre parentesis (modelo de impresora PENDIENTE = bloqueante ya conocido del proyecto).
  - Evidencia: ERC 0 errores 0 warnings con --severity-all; netlist exportado y revisado red por red (23 redes OK, solo K1-NC sin conectar, marcado); SVG renderizado y REVISADO visualmente seccion por seccion (multimodal).
  - HALLAZGO TECNICO para el toolchain KiCad-por-codigo (vale para frioseguro tambien): un .kicad_sch generado sin los bloques (pin "n" (uuid)) e (instances ...) por simbolo NO conecta pines a cables en KiCad 10 (netlist vacio, wire_dangling en ERC). El generador nuevo (generar_interfaz.py + symlib.py, que extrae simbolos de las libs oficiales y resuelve extends) ya lo hace bien; el generar_kicad_sch.py de frioseguro es solo diagrama de bloques y no sufre esto, pero si se lleva a simbolos reales hay que portar el fix. Otros gotchas resueltos: origenes en grilla 1.27mm, buses partidos en cada tap, propiedades rotadas 90 para simbolos verticales, justify espejado en simbolos rot180.
  - Proximo paso: Matias/@verificador revisan el esquematico (PDF) -> @hardware verifica precios BOM y candidatos ML -> con modelo de impresora confirmado se fija V_PSU y conectores -> netlist a @pcb.

- 2026-07-30 [LASER-PCB] DOCTRINA APLICADA a los dos esquematicos existentes + herramienta de QA nueva.
  - **`herramientas/chequear_solapes_sch.py` (NUEVO)** — analogo de `chequear_solapes.py` pero para el
    `.kicad_sch`: parser propio de s-expressions, calcula el rectangulo de cada texto visible (notas,
    labels, Reference/Value/campos de usuario) con la formula de DOCTRINA 6.4 (`ancho = n_car x size`,
    `alto = n_lineas x size x 1.6`) y falla si dos se pisan. Informa ademas texto rotado, bbox y
    ocupacion real (densidad por celdas de 2.54 mm, no bbox: el bbox mide extension, no densidad).
    Va en el pipeline ANTES de exportar el PDF. Uso: `python chequear_solapes_sch.py x.kicad_sch`.
  - **detector_campo (GRAVE -> OK)**: reescrito `ejemplo_kicad/tools/gen_sch.py`. De **0 cables / 30
    global labels** a **41 cables + 8 labels** (16 %, y 5 de esos son solo documentacion de net).
    `GND`, `GND_HV` (power:GND1 con Value GND_HV = masa flotante del campo) y `+3V3` como simbolos de
    power con PWR_FLAG. **Barrera de aislacion** dibujada bajo U1 y rotulada (Viso 5 kVrms, creepage
    >= 8 mm). 3 bloques con marco punteado y titulo numerado. `Value` = part number (antes "ESP32" /
    "CAMPO 190Vcc" rompian el BOM); la funcion va en el campo de usuario `Funcion`. Notas de calculo
    de las 4 redes + tabla de revisiones. Nets renombradas FIELD_N->GND_HV y 3V3->+3V3 (ya reflejado
    en `tools/gen_pcb.py`; el .kicad_pcb hay que regenerarlo).
  - **interfaz_laser_dremel (prolijidad)**: `generar_interfaz.py` pasa a **layout declarativo por
    celdas** (funcion `bloque(dx,dy)`: cada bloque se emite con su offset, las coordenadas internas no
    se tocan). Titulo corto en su banda (ya no pisa el bloque 3), 4 marcos en las celdas de DOCTRINA
    6.2, numeracion en orden de lectura por filas, 0 solapes Reference/Value (eran 5), 0 texto
    rotado, 2 barreras de aislacion (U2/U3) y ~30 lineas de CALCULOS escritos (7805 a 12 y 24 V, IF de
    cada opto, seguidor por emisor, Vgs, gate, LEDs, K1, fusibles). `Value` limpiado a valor puro.
  - **HALLAZGO KiCad (corrige lo que decia la auditoria)**: KiCad **ajusta el angulo del campo a 0/90 y
    despues le SUMA la rotacion del simbolo**. O sea: campo a 0 en un simbolo rotado 90 sale VERTICAL,
    y campo a 180 sale vertical igual (180 se normaliza a 90). Regla del generador:
    `ta = 90 if rot in (90,270) else 0`. Los "12 campos rotados" que la auditoria conto en el archivo
    en realidad se dibujaban horizontales. Ademas: en simbolo espejado (`mirror y`) se invierte el
    justify, y los labels con `justify bottom` se dibujan ARRIBA del punto (el chequeador ya modela
    las tres cosas).
  - **DEFECTO ELECTRICO REPORTADO POR @pcb: NO esta en el esquematico.** El netlist real
    (`kicad-cli sch export netlist`) dice `+5V = C2.1 C4.1 U1.3 U2.4 U3.4` y `U2.3 = R2.1 + R3.1`:
    el seguidor por emisor YA ESTA bien dibujado desde la rev A. Lo que esta mal es el netlist
    **escrito a mano** en `tools/gen_pcb_interfaz.py` (U2/U3 con pin3=GND y pin4=OPTOx_C, y K1 con los
    pines 1/2/4 cambiados). La solucion no es parchear el PCB: es generarlo desde el `.net`.
  - **Cambio de valor decidido: R6 1k -> 2k2** (bleeder de gate). Con 1k el opto tenia que hundir
    4.8 mA de los 5.4 mA que garantiza el PC817 con CTR minimo 50 % (margen 1.1x); con 2k2 el margen
    es 2.4x y el apagado del gate queda en ~7 us, despreciable frente al PWM de fan (~1 kHz).
  - Evidencia: ERC **0/0 con --severity-all** en los dos; `chequear_solapes_sch.py` **0 solapes** en
    los dos; PDFs exportados y **mirados** (render a PNG con pymupdf, revision multimodal en 4 pasadas:
    cada defecto visto se corrigio y se volvio a mirar). PDFs en `*/salida/`.
  - Pendiente: ocupacion 50 % (detector, A4) y 36 % (interfaz, A3) contra el objetivo 55-75 % de la
    doctrina — la interfaz tiene los 4 bloques en las celdas correctas pero cada bloque usa poco de su
    celda; se resuelve reacomodando dentro de cada celda, no moviendo bloques.

- 2026-08-19 [GALGAS / DREYFUS] **NODO EMISOR v3 — esquematico completo + informe para la materia.**
  Todo nuevo en `C:\Proyectos\galgas\hardware\` (repo galgas, carpeta que no existia).
  - **Esquematico**: `kicad/nodo_galga_v3.kicad_sch` (A2, 6 bloques, 33 componentes, 47 redes)
    generado por `kicad/generar_nodo_galga.py` + `symlib.py` + `galgas.kicad_sym` (simbolo propio
    del modulo RA-02, con su `sym-lib-table` y `.kicad_pro` para que el ERC lo resuelva).
    **ERC 0 errores / 0 advertencias con `--severity-all`**, `chequear_solapes_sch.py` **0 solapes**,
    PDF/SVG exportados y **mirados** (4 pasadas multimodales: bloque 1, MCU, alimentacion, hoja
    completa), netlist revisado red por red. Exportados: `.pdf`, `.svg`, `.net`, `erc.rpt`,
    `render_esquematico.png`.
  - **Circuito**: 1/4 de puente 350R a 3 hilos (completado R1 350R 0.1% 10ppm + pierna R2/R3) +
    shunt-cal (RCAL 174k65 + BSS138) + 3 TVS con **IR <= 10 nA exigido por calculo** + filtro
    RC diferencial 796 Hz / modo comun 15,9 kHz → **ADS1220** (AIN0/REFP1=E+, AIN1=sense, AIN2=ref,
    AIN3/REFN1=E- con la **llave interna gateando el puente**, medicion ratiometrica VREF=10b) →
    ATmega328P-AU (SPI, ISP, reed, LED, divisor de bateria **gateado por Q3**) → RA-02 433 MHz.
    Alimentacion: ER14505 → JP1 (puente extraible para medir consumo) → DMG2301L (inversion) →
    **supercap 1 F con RSC 10R ANTES del LDO** → MCP1700-3002 (riel unico 3,0 V).
  - **HALLAZGOS / correcciones de diseno** (todo con cuenta, en `NOTAS_CALCULO.md`):
    (a) **El supercap iba mal ubicado en `DISEÑO_DREYFUS.md`**: despues del LDO no aisla la pila
    (el regulador entrega toda la corriente que le pidan); lo que desacopla es impedancia serie →
    va aguas arriba. Con 10 Ω de RSC el pico al colocar la pila es 184 mA < 200 mA de limite, y la
    constante de 20 s **ES la despasivacion** que pide EEMB. Problema y solucion resultaron la
    misma pieza. (b) **El INA333 sale**: 0,09 µV rms del ADS1220 a G=128 (Tabla 7-1, pag. 16) son
    0,06 µε; una pre-ganancia solo agrega offset y deriva. (c) **20 SPS, no 500 Hz**: mejor ruido
    + rechazo simultaneo 50/60 Hz; la senal es de 0,397 Hz. (d) La caida de la llave (47 mV) **se
    cancela** porque REFN1 es el mismo nodo. (e) Prohibido TVS de 3,3 V de standoff: fuga de µA
    sobre 175 Ω = cientos de µε.
  - **CONTRADICCIONES marcadas (no resueltas en silencio)**: 1) `DISEÑO_DREYFUS.md` dice AD7124-8 y
    la lista de compra verificada del **mismo dia** dice "ADS1220, NADA de AD7124" (y es la que se
    ejecuto) → **se diseno con ADS1220, falta que Matias confirme que placa llego**; 2) el INA333 y
    los 500 Hz que venian "fijados" son de las generaciones 1 y 2, no de esta; 3) "v3" significa
    cosas distintas en el repo de software y en los docs de ingenieria.
  - **Informe HTML para el profesor de Diseno y Manufactura**:
    `hardware/INFORME_PLACA_GALGAS.html` (946 KB, autocontenido, sin CDNs, claro/oscuro,
    responsive, imprimible). 10 secciones: problema · **historia de las 3 generaciones** ·
    **datos REALES de la campana Dreyfus 11-13 feb 2026** (4 graficos en canvas con los CSV
    embebidos) · gen 2 · la placa (esquematico embebido) · bloque por bloque con calculos ·
    **algoritmo de deteccion** · que falta (12 etapas con dependencias, incluye fabricacion y
    armado) · por que sirve para la materia · anexos. Verificado con Playwright: 0 errores de
    consola, los 4 canvas con pixeles dibujados, screenshots mirados en claro, oscuro y movil.
  - **Datos de campo**: `hardware/extraer_datos_campo.py` (read-only sobre `data/field_captures/`)
    → `datos_campo.json`. Lo medido: evento **CADENA B ROTA real** el 13-feb 13:02:15-13:04:40
    (vA 2,013 V vs vB 1,091 V, **dV pico 922 mV**, se repara a los 145 s y los canales vuelven a
    superponerse) · ruido en reposo **σ = 1,73 / 2,23 mV** · fs real 4,98 Hz · **K_A = K_B = 1,00**
    (nunca se calibro la ganancia) · TH_V bajado de 70 a 10 mV **durante** la campana.
  - **Algoritmo**: documentado el que existe (`updateAlert()` del receptor: dv/ratio + HOLD 1,5 s +
    clasificacion contra 2σ del reposo) y el auto-disparo de la gen 2 (v_pp > 40 mV + guarda de
    rango + confirmacion). **Lo que NO existe**: el criterio de la gen 3 en µε con nodos que
    duermen → propuesta marcada como propuesta (2 niveles, M de N = 3 de 4, latencias calculadas,
    y la tasa de falsos positivos declarada como **no estimable** hasta medir con la cadena nueva).
  - **Proximo paso**: P1 confirmar el ADC fisico → banco con galga real (P4: 350R vs 10k en la
    pierna de referencia, con medicion de deriva) → @verificador revisa → netlist a @pcb.
    Pendientes P1-P7 en `NOTAS_CALCULO.md` §7. **Nada commiteado** (orden de la tarea).

- 2026-08-20 [GALGAS / DREYFUS] **REV B del nodo emisor: dos errores REALES del bloque 6
  (alimentacion), encontrados por Matias abriendo el KiCad.** Los dos eran electricos, no
  cosmeticos, y los dos habian pasado ERC 0/0 — recordatorio de que **el ERC verifica
  conectividad, no que el circuito haga lo que dice hacer**. Se arreglo el **generador**
  (`kicad/generar_nodo_galga.py`) y se regenero todo; **nada tocado a mano** sobre el `.kicad_sch`.
  - **Error 1 — Q2 al reves: la proteccion no protegia.** El P-MOS de pila invertida estaba con
    el **SOURCE del lado de la pila** y el drain a la carga. Con esa orientacion, si se coloca la
    pila al reves el **diodo de cuerpo queda en DIRECTA** y la corriente inversa pasa por toda la
    carga: el MOSFET estaba puesto exactamente para eso y no hacia nada. Corregido a **DRAIN a la
    pila, SOURCE a la carga** (`wire(JP1.pin(2), Q2.pin(3))`). Bonus geometrico: con `rot=90` el
    drain ya cae a la izquierda y el source a la derecha, asi que los cables **dejaron de cruzar
    el simbolo** (antes iban en diagonal por encima de Q2). Calculo nuevo **C13**.
  - **Error 2 — el supercapacitor estaba en DERIVACION: era decorativo.** El netlist decia
    `+BATT: ..., RSC.1, U4.3(VI)` y `Net-(CSC-Pad1): CSC.1, RSC.2` — o sea `+BATT → RSC → CSC →
    GND` era una **rama muerta** y el LDO colgaba directo de la pila. En el pulso de TX la
    corriente salia de la ER14505 (justo la que no puede darla: R_int alta + pasivacion) y el
    cap solo podia aportar a traves de los 10 Ω de RSC = 1,2 V de caida a 120 mA. Ahora va **EN
    SERIE**: `BT1 → JP1 → Q2 → +BATT(D4, RD1) → RSC → V_SC(CSC, CI) → U4`. RSC quedo `rot=90`
    como elemento del riel; CI se mudo al nodo del supercap (es el cap de entrada del LDO).
  - **HALLAZGO que nace del arreglo — requisito nuevo, y es bloqueante**: al poner el cap en
    serie, **su ESR pasa a ser la impedancia de fuente del pulso**. `Req = ESR ‖ (R_pila+RSC) =
    ESR ‖ 20 Ω`; con 0,42 V de margen (3,6 − 3,0 − 0,178 de dropout) y 120 mA de pico:
    **ESR 1 Ω → 0,13 V OK ; 3 Ω → 0,33 V justo ; 30 Ω → 1,46 V NO SIRVE**. El EDLC 1 F 5,5 V
    tipo moneda barato declara 30-100 Ω → **no sirve**. Nuevo pendiente **P8** (@hardware).
    En la topologia vieja este numero no importaba porque el cap no hacia nada: el error
    **escondia** el requisito.
  - **D4 revisado (decision tomada, no pateada): pasa a UNIDIRECCIONAL** (simbolo `D_Zener`,
    catodo a `+BATT`). El riel es continua siempre positiva; el bidireccional paga dos uniones de
    fuga para el mismo standoff y **la fuga se paga los 365 dias**: 1 µA = 8,8 mAh/ano (0,4 % de
    la pila), 100 µA la funde (42 %/ano). Ubicacion **confirmada en `+BATT`, antes de RSC**: la
    descarga de ESD se deriva sin pasar por un 0805 de 10 Ω. Lo que queda abierto es la parte
    concreta → **P9**: unidireccional, VRWM 5-6 V, `IR ≤ 1 µA @ 3,7 V`. **Aviso de seleccion**:
    los TVS *de potencia* de standoff bajo (SMAJ5.0A y familia) especifican fuga de **cientos de
    µA** a VRWM; hay que usar un diodo de proteccion ESD, no un TVS de potencia. Calculo **C12b**.
  - **C8 verificado, no copiado**: el `3,67/20 = 184 mA` sigue valiendo y ahora esta justificado
    en la hoja — los 20 Ω son `R_pila 10 + RSC 10` (+ 0,05 de Rds(on) de Q2, despreciable). Se
    agrego que esos mismos 20 Ω reponen los 18 mV del cap en 20 s, contra 300 s de ciclo.
  - **Detalle de ERC que vale para el toolchain**: al meter RSC en serie, el `PWR_FLAG` tuvo que
    **mudarse de `+BATT` a `V_SC`**, porque el pin `VI` de U4 se alimenta ahora a traves de una
    pasiva (`power_pin_not_driven`). El flag va en el nodo que realmente alimenta al regulador.
    Se agrego una funcion `label()` (etiqueta **local**, sobre el cable) para nombrar `V_SC`: no
    reemplaza cables, solo hace legible el netlist.
  - **Evidencia**: ERC `--severity-all` **0 errores / 0 advertencias**; `chequear_solapes_sch.py`
    **0 solapes**; PDF regenerado y **mirado** (zoom del bloque 6, hoja completa y bloque 5);
    netlist verificado red por red — `+BATT: D4.1(K), Q2.2(S), RD1.1, RSC.1` (**sin U4.3**),
    `/V_SC: CI.1, CSC.1, RSC.2, U4.3(VI)`, `Net-(JP1-B): JP1.2, Q2.3(D)`.
  - **Bloque 5 (calculos en la hoja) recompaginado**: C7/C8 rehechos + C12b y C13 nuevos; paso a
    paso de 3,0 → 2,7 u y texto 1,45 para que las 44 lineas entren **sin pisar el cajetin**
    (el chequeador de solapes no ve el title block: eso se detecta mirando el PDF). Rev **B**.
  - **`generar_informe.py` ahora embebe el SVG** (`data:image/svg+xml;base64`) en vez del PNG
    —el PNG pixelaba al hacer zoom, ya lo habia cambiado Matias a mano y se perdia al regenerar—
    y se actualizaron los calculos C7/C8/C13, la BOM (CSC con ESR, D4 unidireccional, Q2 con la
    orientacion) y una nota nueva que **cuenta las dos correcciones** (sirve para la materia:
    muestra revision de diseno real). Verificado con Playwright: 0 errores de consola, los 4
    canvas dibujados, el `<img>` del esquematico carga (naturalWidth 2245) y el bloque de
    calculos ya **no se corta** (scrollWidth == clientWidth).
  - **Proximo paso**: sin cambios de fondo (P1 ADC fisico, P4 banco), mas **P8 supercap con ESR
    ≤ 1 Ω** y **P9 D4 unidireccional con IR ≤ 1 µA** para @hardware — los dos hay que resolverlos
    antes de comprar. @verificador revisa la rev B antes del layout. **Nada commiteado.**

- 2026-09-01 [TERMOVIGIA / FRIOSEGURO] **TERMOVIGIA BASE v2 — esquematico completo, jerarquico, KiCad 10.**
  Todo en `C:\Proyectos\frioseguro\hardware\v2\termovigia_base\` (carpeta nueva).
  - **Entregables**: `termovigia_base.kicad_pro/.kicad_sch` (raiz A3: diagrama de bloques con sheet pins
    cableados + tabla GPIO) + 5 hojas hijas A3 (`01_alimentacion`, `02_entradas`, `03_mcu`, `04_salidas`,
    `05_4g`), `termovigia.kicad_sym` (DevKit 38p, modulo LM2596, modulo rele 2ch, breakout A7670,
    level-shifter, rieles +VIN/VSYS/+4V0), `termovigia.pretty` (4 huellas placeholder, A MEDIR),
    `termovigia_base.pdf` (6 paginas), `.net` (79 redes), `_bom.csv` (campos Funcion y Poblar),
    `erc.txt`, `DISENO.md` (calculos C1-C12, tabla GPIO para config.h, poblar Estandar/Premium,
    envolvente, riesgos), `generar_sch.py` + `kicad_gen.py` + `symlib.py` + `verificar.py`.
  - **Evidencia**: `kicad-cli sch erc --severity-all` **0 errores / 0 advertencias**; `chequear_solapes_sch`
    **0 solapes** en las 6 hojas; PDF exportado y **mirado** (5 pasadas, render PNG con pymupdf);
    netlist leido red por red. 108 componentes.
  - **Circuito**: entrada 12-24 V (jack + bornera) -> PTC 1,85 A -> SB540 serie -> P6KE30A -> +VIN ->
    OR SB540 con bateria -> VSYS -> LM2596 5 V (DevKit, 4 reles, buzzer) y LM2596 4,0 V (solo A7670,
    2x1000 uF). Premium: 3er LM2596 CC/CV 13,8 V / 0,7 A + 1N5822 + fusible 3 A + SLA Kaise KB1270,
    sensado red 100k/12k -> GPIO34 y bateria 100k/22k -> GPIO35 (clamps 1N5819). 1-Wire 4k7 + 3 borneras
    3P + P6KE6.8CA + 100R + clamps; 3 puertas con 10k/1k/100n/TVS; **2 optos PC817** (defrost GPIO33 +
    grupo GPIO36, pedido de @firmware) con barrera dibujada; SCT-013-000 burden 33R, bias 1,65 V ->
    GPIO32. Reles por BC547 colector abierto (**GPIO HIGH = ON**, reposo/reset = OFF; K4 reposo = RED,
    regla ATS). A7670SA-LASE con level-shifter BSS138 + jumper LV = VDD_EXT / +3V3, PWRKEY (25) y
    RESET (12) por BC547, STATUS -> GPIO39. DHT22 eliminado (sin GPIO libre).
  - **Cambios de decision durante la sesion** (del Director via @hardware/@firmware/@diseno3d): LM317 ->
    LM2596 CC/CV; entrada 12-19 -> 12-24 V; burden 22 -> 33 ohm; segunda opto; STATUS del modem;
    bordes de borneras y posicion de LEDs para @pcb. Todo reflejado en hojas y DISENO.md.
  - **HALLAZGOS del toolchain (van a kicad_gen.py y a la doctrina)**: (1) KiCad **fusiona referencias
    duplicadas** en el netlist sin error de ERC -> el generador chequea unicidad; (2) los `Conn_01x06`
    de KiCad NO estan centrados como el 01x04: pin 1 en +5.08 -> un cable salio en diagonal y la union
    no existia; ahora `wire()` prohibe diagonales; (3) `D_TVS` con rot 90 tiene el pin 1 ABAJO: los
    cables cruzaban el cuerpo (usar rot 270); (4) un extremo de cable sobre el interior de otro sin
    junction NO conecta y el ERC no lo dice -> chequeo de geometria en el generador; (5) la
    justificacion de texto se espeja con rot 90/180 y mirror y (el chequeador de solapes ya lo modelaba;
    el generador ahora escribe 'right' para que 'left' se dibuje como left); (6) hojas jerarquicas:
    sheet pin borde derecho = angulo 0 + justify right, izquierdo = 180 + left, shape igual al
    hierarchical_label; instances path `/ROOT_UUID/SHEET_UUID`.
  - **Para @bibliotecario**: `kicad_gen.py` (framework generico multi-hoja con ficha ORIGEN/PROBADO/USO/
    DEPENDE/GOTCHAS) + `symlib.py` + `chequear_solapes_sch.py` + `verificar.py` = toolchain KiCad-por-
    codigo probado en 3 proyectos (laser-pcb, galgas, termovigia). Cosechar a `C:\Proyectos\biblioteca\pc\kicad\`.
  - **Pendientes**: revision Matias/@verificador del PDF; @hardware confirma breakout A7670 (VDD_EXT
    expuesto o UART 3,3 V), LM2596 CC/CV y modulos; @pcb mide las 4 huellas placeholder y rutea desde
    `termovigia_base.net`; Director decide envolvente (100x80 NO entra con los 2 modulos de rele sobre
    la placa: DISENO.md seccion 8) y si la hoja 5 + riel 4 V se marcan `Poblar = PREMIUM` en la BOM.
    **Nada commiteado** en frioseguro (orden de la tarea: entregables en la carpeta).

- 2026-09-01 [FRIOSEGURO / TERMOVIGIA BASE v2] **Auditoría @verificador del esquemático rev A** →
  **APROBADO CON CORRECCIONES: rev B obligatoria antes de rutear; @pcb NO rutea desde este `.net`.**
  Informe completo: `C:\Proyectos\frioseguro\hardware\v2\termovigia_base\VERIFICACION_2026-09-01.md`.
  - Evidencia propia: ERC `--severity-all` re-corrido 0/0; PDF re-exportado; netlist (79 redes, 108 comp.)
    parseada y leída red por red — polaridades, OR, optos, buzzer, drivers, UART/shifter, PWRKEY/RESET
    coinciden con lo declarado; 0 refs duplicadas, 0 sin huella. Cold-start: `generar_sch.py` + `verificar.py`
    en copia aislada reproducen el entregado (solo UUIDs). GPIO12/0/2/15/5 en boot: OK. K4 en reposo = RED:
    físicamente correcto.
  - **Bloqueante H1**: breakout A7670 MLA1487294925 sin confirmar — la ficha ML dice "5V"; si es 5 V con
    regulador propio, +4V0 no sirve y el puente +5V→VCC (que no está en la netlist) compartiría el riel del
    ESP32 con ráfagas de 2 A. Posible doble inversión de PWRKEY si el breakout ya trae transistor.
    Propuesta: riel +VMODEM exclusivo por U103 (4,0 o 5,0 V) + JP para puentear Q501. Dueño: @hardware.
  - **Mayores (cambian netlist)**: H2 sirena sin alimentación en placa (Premium no tiene 12 V y +VIN es 0 en
    el corte); H3 sin LVD → la SLA se descarga a fondo en cortes largos (decisión Director); H4 J303 OLED
    VCC-SCL-SDA-GND no coincide con módulos comunes (GND-VCC-SCL-SDA); H5 K4/ATS en GPIO18 = `PIN_DHT22`
    del firmware heredado → `dht.begin()` (INPUT_PULLUP) satura Q404 y conmuta a GRUPO; falta R B-E 10 k en
    los drivers; H6 optos sin filtro (AC → 50 Hz en el GPIO); H7 batería invertida no protegida; H8 hoja
    raíz desactualizada (22R / ×0,130 / 1,0 V vs 33R / ×0,107 / 0,9 V — `generar_sch.py:1070,1072`).
  - Menores H9–H18 (símbolo TVS bidireccional para P6KE30A, GPIO39 flotante en Estándar, +3V3 sin PTC a
    sondas, MountingHole ausentes, `Poblar` de hoja 5, texto fuera de área útil, huella F101, etc.).
  - Para @firmware (bloqueo antes del primer flasheo en esta placa): `RELAY_ON HIGH`, `SENSOR_DHT22_ENABLED
    false` y no instanciar `DHT`, `MAX_RELAYS 4`, `#define` desde DISENO §2 (una vez corregida la raíz).
  - Próximo paso: @hardware responde H1 → @esquematico rev B → @verificador re-audita el `.net` → @pcb.

- 2026-09-01 [FRIOSEGURO / TERMOVIGIA BASE v2] **rev B del esquematico — cierra H1..H18 de la auditoria + datos B.1-B.5 de @hardware.**
  Todo regenerado en `C:\Proyectos\frioseguro\hardware\v2\termovigia_base\` (`generar_sch.py` -> `verificar.py` en verde:
  ERC `--severity-all` **0/0**, `chequear_solapes` **0 solapes / 0 fuera de area** en las 6 hojas, PDF + `salida/p1..p6.png`
  mirados, `.net` 82 redes / 136 componentes leido red por red, BOM 45 lineas siempre + 27 PREMIUM). DISENO.md reescrito
  con la seccion 12 "rev B — cambios por hallazgo" y la tabla GPIO final. **Nada commiteado** (orden).
  - **H1 (cerrado por @hardware: breakout = BK-A7670 v1 AND Technologies)**: riel `+VMODEM` exclusivo por U103 a **6,0 V**
    (VCC 5-10 V del breakout menos la caida del interruptor); UART 3,3 V **directa** (level-shifter U501 + JP501 eliminados);
    PWRKEY directo GPIO25 -> R501 1k -> JP502 2 pines (abierto: arranca solo); sin RESET/STATUS -> **MODEM_PWR_EN en GPIO12**:
    Q502 BC547 -> Q503 IRF9540N high-side (R504 47k G-S, R505 4k7, C504 4,7 uF: Vgs -5,4 V, arranque suave tau 20 ms, inrush
    0,4 A). GPIO12 strapping queda LOW en boot por 2k2 + 10k B-E -> modem arranca apagado. U502 = header 1x7 con numeros
    fisicos (G R T K V G S), huella `A7670_BK_1x07`. IO39 libre con R305 100k.
  - **H2** J104 SIRENA desde VSYS via F103 1,5 A T, K1 conmuta (sirena 12-24 V). **H3 LVD**: Q107 IRF9540N + TL431,
    56k/15k/470k/10k -> corta 10,9 V, reconecta 12,2 V (los 36k/10k/1M de B.3 daban 0,4 V de histeresis: oscila); R113 10k
    sangrador contra la fuga de D106; 0,17 mA con el LVD abierto. **H7**: Q106 IRF9540N (0,47 W a 2 A) **+ D109 crowbar**:
    sin el crowbar, bateria invertida con red = cargador CC en zona lineal sobre Q106 = **11 W** (el MOSFET solo no cierra
    H7). **H5**: R406-R410 10k B-E, **K4 -> GPIO23, K3 -> GPIO18**. **H6**: C222/C223 10 uF (con 1 uF el hueco de media onda
    llegaba a 2,15 V). H4 J303 GND-VCC-SCL-SDA. H8 33R/x0,107/0,9 V unicos. H9 D_Zener K a +VIN. H12 R224 22R 1W. H14 H1-H4
    MountingHole en (4,4)(116,4)(4,96)(116,96), PCB **120x100**, LEDs (110,90)/(110,78) confirmados. H15 Poblar PREMIUM.
    H16 tabla raiz en dos columnas. H17 F101/F102/F103 = portafusible 5x20 (2A T / 3A / 1,5A T; el PTC no existe en AR).
    H18 sin objeto (no hay RESET).
  - **HALLAZGO del toolchain (corregido en `kicad_gen.py`)**: KiCad aplica **rotacion primero, espejo despues**;
    `rot_offset()` lo hacia al reves -> un IRF9540N `rot 90 + mirror x` quedo con los pines en otro lugar y el ERC lo
    delato (`pin_not_connected` Q107). Con rot 0 el orden no importa, por eso rev A no lo vio. Para @bibliotecario.
  - Otros gotchas: `label()` local debe ir EXACTAMENTE sobre un punto del cable (a 0,4 u del cable = `label_dangling`);
    las lineas de heredoc con `'''` rompen la Bash tool -> scripts de parche por archivo (scratchpad).
  - **Proximo paso**: @verificador re-audita el `.net` rev B (misma lista) -> @hardware compra (BOM B.8) -> @pcb mide 3
    huellas placeholder y rutea desde `termovigia_base.net` -> @firmware `PINOUT.md` desde DISENO seccion 2
    (RELAY_ON HIGH, DHT fuera, K3=18, K4=23, MODEM_PWR_EN=12, sin LTE_RESET/STATUS).

- **2026-09-01 (noche) — @verificador: re-auditoria rev B del esquematico Termovigia Base v2.** Informe:
  `C:/Proyectos/frioseguro/hardware/v2/termovigia_base/VERIFICACION_2026-09-01_revB.md`. **Veredicto: APROBADO CON
  CORRECCIONES (rev B.1 corta antes de cerrar el ruteo; @pcb puede arrancar placement y medicion de huellas).**
  - Evidencia propia: ERC `--severity-all` 0/0 re-corrido; PDF byte a byte igual (414.059 B); cold-start en copia aislada
    (`generar_sch.py` + `verificar.py` exit 0) y parser propio del `.net`: conectividad, huellas y BOM **identicas** al entregado;
    136 comp., 0 dup, 0 sin huella, 0 huerfanas (9 NC marcados), 3 placeholders exactos; pads de huella = pines de simbolo.
  - **H1-H18: 17 cerrados con evidencia (pagina/ref/red), H18 sin objeto justificado.** Tabla GPIO raiz = DISENO 2 = `.net` =
    firmware (K3=18, K4=23, MODEM_PWR_EN=12, sin LTE_RST/STATUS). LVD recalculado: 10,9 / 12,2 V confirmados.
  - **Nuevos MAYOR**: H19 VBAT_SENSE no ve bateria ausente / F102 volado (con red el cargador CV la deja en 13,6 V; DISENO 3.5
    promete "0,1 V -> alarma" y es falso; opcion: divisor J102.1 -> IO39 libre). H20 LVD sin constante de tiempo: un pico de
    2 A (0,58 ms) o la sirena a 11,2 V lo enclava hasta 12,2 V (fix: 1 uF en REF). H21 LTE_TX sin R serie -> alimentacion
    fantasma del breakout con MODEM_PWR_EN LOW (fix: 1k serie o Serial2.end() antes de cortar).
  - **MENOR**: H22 IO35 flota en Estandar (R106/R107 solo PREMIUM); H23 fusibles por variante (sirena con strobo -> F103 2 A T /
    F101 3 A T) no estan en BOM; H24 Q503 a Vgs -5,45 V fuera de hoja (+VMODEM 7 V o P-MOS logic-level); H25 DISENO 3.5 se
    contradice sobre inversion sin red; H26 TL431 a 0,9 mA (R109 4k7); H27 apagado lento del modem + cada reset del ESP32 lo
    corta (regla AT+CPOF y LOW >= 10 s para @firmware); H28 medir R104 del breakout (decide si JP502 sirve); H29 PLAN 2.1/4.1
    desactualizado (@firmware). H30 informativo: burden es R220 33R (no R224): 100 A -> +-2,33 Vpk recortado, 24 A -> +-0,56 Vpk
    lineal, ADC lineal hasta ~36 A.
  - Duenos: rev B.1 (H19-H22) @esquematico; decision H19a/b y H24 Director; H23/H28 @hardware antes de comprar; H21/H27/H28/H29
    @firmware en PINOUT.md. Nada commiteado (orden). Detalle y reproduccion en el informe.

- 2026-09-02 [FRIOSEGURO / TERMOVIGIA BASE v2] **rev B.1 del esquematico — cierra H19..H30 de la re-auditoria de @verificador con las
  decisiones del Director.** Regenerado en `C:\Proyectos\frioseguro\hardware\v2\termovigia_base\` (`generar_sch.py` -> `verificar.py`
  en verde: ERC `--severity-all` **0/0**, `chequear_solapes` **0 solapes / 0 fuera de area** en las 6 hojas, PDF + `salida/p1..p6.png`
  mirados y ademas recortes a 200 dpi de cada bloque tocado; `.net` **84 redes / 143 componentes** parseado red por red, BOM 72 lineas
  = 45 siempre + 27 PREMIUM). DISENO.md con seccion 13 "rev B.1 — H19..H30" + diff de conectividad; **`PINOUT.md` nuevo** (tabla GPIO
  final + reglas para @firmware). **Nada commiteado** (orden).
  - **H19 opcion (a)**: divisor R114 100k / R115 22k + C112 + D110 (a +3V3) + **D111 (a GND: bateria invertida -> -12 V en J102)**
    desde **J102.1 pre-fusible** (etiqueta local `BATT_RAW`, unica etiqueta nueva: el resto es cable) -> **IO39 = `VBATT_RAW_SENSE`**.
    IO39 paso a la columna izquierda del simbolo del DevKit (con las otras ADC) sin mover ningun otro pin. **R305 eliminada**: con
    100k en paralelo el ratio de Premium pasaba a 6,55; el pull-down de Estandar es R115 22k siempre poblada (mismo criterio que
    **H22**: R107/C111 pasan a ESTANDAR+PREMIUM). Seccion 3.5 reescrita con tabla de casos: regla `|V39 - V35| > 0,5 V > 10 s`.
  - **H20**: C113 1 uF en REF del TL431: tau = (56k || 15k || 470k) x 1 uF = 11,5k x 1 uF = **11,5 ms**; la rafaga de 0,58 ms llega
    al 5 %. **H26**: R109 10k -> **4k7** (I_K 1,8-2,2 mA >= 1 mA de hoja). **H21**: R507/R508 1k en LTE_TX/LTE_RX (redes nuevas
    `Net-(U502-R)` / `Net-(U502-T)`) + regla `Serial2.end()` antes de bajar IO12. **H24**: +VMODEM **7,0 V** -> V_G 0,64 V, Vgs
    **-6,4 V**, caida < 0,4 V, VMODEM_SW >= 6,4 V (margen 1,4 V; era 0,4); condicion: regulador del breakout conmutado (@hardware).
    **H23**: F101 3 A T, F103 2 A T (un valor por posicion). H25/H27/H28/H30 en texto (hojas + DISENO): inversion siempre vuela F102,
    ~0,5 mA con LVD abierto, cada reset del ESP32 = 30-60 s sin LTE (AT+CPOF -> LOW >= 10 s), medir R104 del breakout, lineal ~36 A.
  - **Diff de conectividad rev B -> B.1** (no hay `.net` de rev B en git: la carpeta esta sin trackear; el diff sale del generador):
    nuevas `BATT_RAW`, `VBATT_RAW_SENSE`; cambiadas `Net-(U105-REF)` (+C113), `LTE_TX`/`LTE_RX` (partidas por R507/R508); eliminada
    `Net-(U301-IO39)` (R305); solo valor: R109, F101, F103, U103 (ajuste). Detalle en DISENO.md seccion 13.
  - **Dibujo**: para meter 3 columnas de sensado en la hoja 1 hubo que angostar el bloque 3 -> nuevo helper `parrafos()` en
    `generar_sch.py` (envuelve parrafos a N caracteres con `textwrap`; el ancho en mm = N x size, el mismo modelo que
    `chequear_solapes_sch.py`). Gotchas nuevos: (1) el chequeador no ve texto-sobre-simbolo (C112 tapaba a D111 con 0 solapes:
    solo se ve mirando el PNG); (2) un cable vertical que cruza el interior de otros cables no conecta ni da ERC, pero es ilegible
    (PWRKEY por x=212 cruzaba los pines G del breakout); (3) el sheet pin de la raiz tiene que quedar >= 2 u dentro del borde del
    bloque; (4) `label()` a 90 grados choca con cualquier nota horizontal que cruce: preferir angulo 0 en el extremo de un stub.
  - **Proximo paso**: @verificador re-audita solo las redes tocadas (diff de 5 lineas en DISENO seccion 13) -> @hardware compra
    (BOM B.8 + C113 1 uF, 1k x2, 1N5819 x2, 100k/22k 1 %, fusibles 3 A T / 2 A T) y mide R104 + regulador del breakout -> @pcb cierra
    el ruteo con `termovigia_base.net` rev B.1 -> @firmware implementa `PINOUT.md` (RELAY_ON HIGH, DHT fuera, IO39 vs IO35,
    MODEM_PWR_EN, Serial2.end).

- **2026-09-02 — @verificador: verificacion corta rev B.1 del esquematico Termovigia Base v2.** Informe:
  `C:/Proyectos/frioseguro/hardware/v2/termovigia_base/VERIFICACION_2026-09-02_revB1.md`. **Veredicto: APROBADO PARA LAYOUT.**
  - Evidencia propia: ERC `--severity-all` 0/0 re-corrido (KiCad 10); cold-start en copia aislada (generar_sch.py + verificar.py
    exit 0); parser propio: `.net` entregado = regenerado (84 redes / 143 comp., conectividad identica); BOM md5 identico
    (72 = 45 + 27); 9 redes de un nodo = 9 NC. Diff declarado en DISENO 13 verificado red por red contra el `.net`: coincide
    (BATT_RAW, VBATT_RAW_SENSE, U105-REF + C113, LTE_TX/RX partidas por R507/R508, R305 fuera; cuentas 136+8-1 y 82+3-1 cierran).
  - **H19-H30: 12/12 cerrados** con calculo propio: IO39 a 15 V = 2,70 V; invertida = -0,2 V por D111 con 0,14 mA (BATT_RAW queda
    negativa permanente, es pre-fusible); Estandar IO39 a GND por R115; tau LVD 11,5 ms (rafaga al 5 %); Vgs Q503 -6,36 V con
    VMODEM_SW >= 6,0 V peor unidad; I_K TL431 1,8-2,55 mA en 10,9-14,5 V. **PINOUT.md = config.h (v3.1, 98afbf7): 24/24 pines
    y todas las constantes coinciden.**
  - **Nuevos, menores, texto (sin cambio de netlist, @esquematico)**: H31 hoja 4 bloque 3 sigue diciendo "F103 1,5 A T"
    (generar_sch.py:1109); H32 DISENO 13 llama "nueva" a BATT_RAW y es la red J102.1-F102.1 renombrada (+R114.1); H33 nota de
    layout: R114 pegada a J102, BATT_RAW es la unica red sin fusible (tambien @pcb).
  - **Firmware (@firmware, no bloquean)**: H34 flote = 2,45-2,49 V en el ADC a 11 dB, calibrar en 13,8 V; H35 headers huerfanos
    current_sensor.h (PIN_CURRENT_SENSOR 36 = GEN_RUN_N) y power_monitor.h con pines viejos, no incluidos pero cargados; H36 boton
    WiFi 5 s (hoja 3 / PINOUT) vs 3 s (config.h / .ino) + config_SANTA_CRUZ.h con PIN_BUZZER 17 y RELAY_ON LOW sin aviso;
    H37 lo que PINOUT exige y v3.1 todavia no tiene (SCT_AMPS_PER_VOLT, BATT_V_SHUTDOWN, HAS_LTE/HAS_BATTERY, lte_a7670.h).
  - Nada commiteado, nada corregido (orden). Proximo: @pcb rutea con `termovigia_base.net` rev B.1; @hardware compra y mide
    R104 + regulador del breakout; @firmware H34-H37; la verificacion del firmware la hace otro agente.

- **2026-09-02 — @esquematico: DREYFUS/galgas — REV C del nodo de galga. Los 9 bloqueantes de P6, cerrados.**
  Repo `C:/Proyectos/galgas/hardware/`. Todo por generador (`kicad/generar_nodo_galga.py`), **nada a mano sobre el `.kicad_sch`**.
  Entregables: `kicad/nodo_galga_v3.kicad_sch` rev C · `kicad/nodo_galga_v3.net` (51 redes) · `kicad/erc_revC.rpt` **0/0 y sin
  chequeos apagados** · `kicad/DIFF_REDES_revB_revC.txt` (diff red por red) · `NOTAS_CALCULO.md` §10 (C21-C29, C7b, C10c) ·
  `kicad/verificar_sch.py` (nuevo) · PDF/SVG regenerados y **mirados**. **Sin commit** (ordenado): 41 archivos staged.
  - **G19 primero, era de una linea**: `hardware/` estaba **UNTRACKED**. `git add hardware/` + `.gitignore`
    (`hardware/kicad/.history/` era otro repo git adentro, `tools/*.exe`, `*.lck`, `__pycache__/`). El proyecto ya sobrevive a
    un `git clean -fd`.
  - **G1 anotacion**: 13 refs sin digito -> `RCAL1, CD1, CA1, CB1, CBLK1, RR1, RP1, RL1, RG1, RSC1, CI1, CO1` (+ `CSC1/CSC2`).
    Se agrega el `1`, no se renumera a `R17`: el nombre sigue diciendo que es. Propagado a la guia de perfboard y verificado
    contra el PLACEMENT de @pcb (55 refs, 0 huerfanas en los dos sentidos).
  - **G2/G3 RA-02**: `FP_RA02 = "galgas:RA-02"` en el generador **y** `galgas.kicad_sym` ahora **se escribe desde el mismo
    generador** con la huella adentro (una sola fuente de verdad; antes el PCB la forzaba con una tabla hardcodeada). Simbolo
    renumerado al **pinout fisico 1-16** (1 ANT, 2 GND, 3 3V3, 4 RESET, 5 DIO0 ... 12 SCK, 13 MISO, 14 MOSI, 15 NSS, 16 GND) y
    con los 16 pines (antes tenia 12 y los 3 GND del modulo quedaban en 2). @pcb ya habia renumerado `galgas.pretty/RA-02` a la
    numeracion oficial: coinciden. **P3 sigue abierto y esta escrito en negrita en la hoja**: el pinout sale del datasheet, no del
    modulo que tiene Matias — hay que medirlo con tester antes de fabricar.
  - **G4 bornera**: `TerminalBlock_Phoenix:...MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal` (era MX126 de 5,00 contra el BOM de 5,08).
  - **G5 RGD1 = 1 M** (no 100 k, y la cuenta esta escrita, C21): con 1 M los 100 nA de IGSS del BSS138 dan 0,1 V contra 0,8 V de
    Vgs(th) (margen 8x) y la descarga de Ciss tarda 27 us contra segundos de paso de calibracion; con 100 k se irian 30 uA.
  - **G6**: RPU1 (CS del ADS1220), RPU2 (NSS) y RPU3 (RESET del RA-02), 100 k. Costo real: 1 nA de media (30 uA solo mientras el
    micro fuerza el selector abajo, ~10 ms cada 300 s).
  - **G7 DIO0 -> PB0** y PD0/PD1 liberados a **J3** (header 1x3 TXD/RXD/GND, sin poblar). Aviso a **@firmware**: DIO0 pasa a
    **PCINT0**, no es mas una interrupcion de PORTD.
  - **G8 ANT**: alineado con la decision de @pcb (`LAYOUT.md` §4): **IPEX**, pad ANT sin poblar, sin linea de 50 ohm en la PCB.
  - **G9**: `/NODO_A`, `/E_REFN`, `/S_MAS`, `/S_MENOS`, `/V_BAT_SENSE`, `/V_SC_MID` con **etiqueta local sobre el cable** (no
    globales: la doctrina prohibe conectar con etiquetas lo que se conecta con un cable). Ojo: los **netclass_patterns del
    `.kicad_pro` apuntaban a los nombres viejos** (`Net-(D3-A2)`) — se actualizaron; era un dato duplicado a mano.
  - **Componentes nuevos de @hardware (§9)**: CSC1+CSC2 (2x Eaton HV0810, D10/P3.5) en serie con `V_SC_MID` + RB1/RB2 150 k;
    D4 = **ESD5Z5.0T1G** en `Diode_SMD:D_SOD-523` (la SOT-23 era huella de 3 pads para un simbolo de 2 patas).
  - **Deuda de documento mia, corregida con cuenta propia**: **G10** C12 tenia un factor 10 -> `10 nA x 175 ohm = 1,75 uV =
    **1,17 ue**` (no 0,12): **endurece P2**, 10 nA ya valen ~1 ue y hay que mirar la curva de fuga vs. temperatura. **G13** el
    dropout del MCP1700 es 178 mV **tipico** / 350 mV **maximo** (168 mV escalado a 120 mA), y aparece **C7b, el caso fin de
    vida** que faltaba: con OCV 3,2 V y R_pila 40 ohm el nodo **se apaga en la ultima TX** -> fin de vida = VBAT 3,3 V y back-off
    a +14 dBm por debajo de 3,35 V (@firmware). **G14** RD3 4M7 + CVB1 10 nF: ADC7 dejaba de violar `VCC+0,5` los 365 dias
    (queda en 3,03 V, cuesta 0,64 uA) y el S/H tiene su carga (constante del divisor: 0,2481 -> **0,2357**, esperar 12 ms +
    conversion dummy). **G11** el conteo real es **11 con nombre + 23 auto + 17 unconnected = 51** (la rev B declaraba 15+32, que
    no existian). **G16** unificado a **BSS138**, con criterio numerico para admitir un 2N7000: `Rds(on) <= 175 ohm` medido a
    3,3 V = 1 ue sobre 1000. **G12/G22** tabla de pines del micro y "sin cristal, RC interno 8 MHz" escritos en §4 y en la hoja.
  - **G25 y el harness (esto es lo que evita el proximo G1)**: el `.kicad_pro` no tenia seccion `erc` y regian los defaults **con
    4 chequeos en ignore, incluido el de anotacion**. Ahora estan **los 43 encendidos** (`unannotated: error`). Encenderlos
    **encontro 3 defectos reales que la rev B tenia y nadie veia**: (1) D1/D2/D3, simbolo de 2 patas sobre huella **SOT-23 de 3
    pads** -> `D_SOD-323`; (2) JP1 era un simbolo de *solder jumper* con huella de header -> `Conn_01x02`; (3) **4 cables de
    longitud cero** heredados (el generador ahora los descarta). Ademas `verificar_sch.py`: un comando que chequea anotacion +
    huellas vacias + ERC 0/0 sin ignores + la advertencia del export de netlist, y devuelve codigo != 0.
  - **Gotchas de dibujo de esta sesion** (para la doctrina): (a) un cable nuevo que comparte columna `x` con otro **se fusiona en
    silencio** — RPU1 en x=u(254) toco el bajante de CLK->GND y **cortocircuito CS con masa**; lo detecto el ERC por
    `pin_to_pin`, pero lo que lo hizo evidente fue el **diff de redes**; (b) un cable que pasa por **dentro del cuerpo** de una R
    no lo ve ni el ERC ni el chequeador de solapes (PD1 atravesaba RP1): solo se ve mirando el PDF ampliado; (c) el chequeador de
    solapes no compara texto contra **simbolo** (el GND de RGD1 tapaba el valor de RCAL1); (d) 64 renglones de calculo a paso 2,7 u
    se comen el **cuadro de rotulo** de la A2: paso 1,85 u y entran.
  - **Proximo**: **@verificador** re-audita **solo lo tocado** con `DIFF_REDES_revB_revC.txt` (18 redes quedaron identicas y
    ninguna red analogica cambio de nodos) -> **@pcb** rutea con `nodo_galga_v3.net` rev C (y puede borrar el
    `FOOTPRINT_FORZADO` de D4: ya sale del esquematico) -> **@energia** firma los +22,8 uA de reposo / 1,30 anos (P11) ->
    **@firmware** P12 (PCINT0, divisor 0,2357, back-off de TX) -> **@hardware** P10 (100 nF C0G en 0805) y G17 (el HT7130A
    comprado no da la TX; hace falta el MCP1700-3002).

- **2026-09-02 [FRIOSEGURO / KIT v1 — MODULOS CABLEADOS] Esquematico de CONEXIONADO de los 5 equipos de demo.**
  Carpeta nueva `C:\Proyectos\frioseguro\hardware\v1_modulos\`. **`v2/` no se toco** (verificado: `git status`
  solo lista `?? hardware/v1_modulos/`; los `.kicad_sch` de v2 conservan mtime 02:08).
  - **Entregables**: `kit_v1_modulos.kicad_sch` (A3, 1 hoja, 19 componentes, 11 redes con nombre) +
    `.pdf` + `.net` + `_bom.csv` + `erc.txt` + `salida/p1.png` · `generar_sch.py` (usa
    `C:\Proyectos\biblioteca\pc\kicad_gen` por `sys.path`, primera vez que se consume la copia de la
    biblioteca desde otro repo: anduvo sin cambios) · `kit_v1_modulos.kicad_sym` (2 simbolos propios) ·
    **`CABLEADO.md`** (guia de armado con tablas y colores, lo que miran Gonza y Sergio) ·
    **`PINOUT_V1.md`** (tabla GPIO para @firmware) · **`DIFERENCIAS_CON_V2.md`** (10 lineas).
  - **Evidencia**: ERC `--severity-all` **0 errores / 0 advertencias**; `chequear_solapes_sch`
    **0 solapes, 0 texto fuera del area util**; PDF exportado y **mirado** (hoja completa + 2 recortes a
    190-200 dpi del bloque de reles y del ESP32, 4 pasadas: se corrigieron etiquetas DOOR pisando los
    numeros de pin, dos solapes de simbolos de riel y el titulo cortado por el cajetin); `.net` leido
    red por red (`/RELAY3 = U1.28(IO18) U3.2(IN1)`, `/RELAY4 = U1.21(IO23) U3.3(IN2)`, etc.).
    **Cero cruces de cables** en toda la hoja: el orden de los pines del simbolo del DevKit se eligio
    para que los 4 canales de rele y las 3 puertas salgan en abanico sin cruzarse.
  - **Circuito**: J1 bornera 5 V -> estrella de 3 ramas (DevKit pin 19 / JD-VCC de U2 / JD-VCC de U3) con
    C1 1000 uF en la entrada y **C5 1000 uF al pie de las bobinas**; 3 borneras 3P en un solo bus 1-Wire con
    R1 4k7 -> IO4; 3 puertas con reed a masa, 4k7 a +3V3 y 100 nF -> IO5/IO13/IO14; 2 modulos de rele
    activo-LOW con **VCC del lado opto a +3V3 y JD-VCC a +5 V** -> IO26/IO27/IO18/IO23.
  - **POLARIDAD (lo central del pedido)**: modulos **activo en BAJO** -> `RELAY_ON LOW` / `RELAY_OFF HIGH`.
    `firmware_modular/config.h:135` **ya dice LOW**: para el v1 esta bien y no se toca; lo que hay que
    cambiar es `MAX_RELAYS 2 -> 4`, agregar `PIN_RELAY_3 18` / `PIN_RELAY_4 23`, borrar `PIN_DHT22 18` y
    poner `SENSOR_DHT22_ENABLED false`. El `PINOUT.md` de la v2 pide `RELAY_ON HIGH` **porque la v2 tiene
    BC547 que invierten**: esa instruccion NO se aplica al kit.
  - **Arranque, con cuenta**: antes del `setup()` los GPIO estan en alta impedancia; en el modulo con opto
    el LED va de VCC a IN, asi que sin camino a masa la corriente es 0 y **los 4 reles quedan ABIERTOS: la
    sirena no suena al enchufar**. Aun con un pull-down interno de 45 k serian 49 uA, 20x menos de lo
    necesario. El riesgo es 100 % de firmware. Regla escrita: `digitalWrite(pin, RELAY_OFF)` **antes** de
    `pinMode(pin, OUTPUT)`.
  - **JD-VCC (§3 de CABLEADO)**: con el puente puesto el LED del opto queda entre 5 V y el GPIO; con el GPIO
    en 3,3 V le sobran 1,7 V y circulan `(1,7-1,05)/1k = 0,6 mA` -> CTR ~30 % -> ~40 mA de colector -> **la
    bobina se queda a medio camino** (rele que zumba o no suelta). Sacando el puente: VCC = 3V3 (0,00 mA con
    IN alto, apagado duro; 2,2 mA con IN bajo) y JD-VCC = 5 V. Aclarado que **la masa sigue comun: no aisla**.
    Plan B escrito por si el modulo del stock necesita 5 V del lado opto: puente puesto + `OUTPUT_OPEN_DRAIN`
    (y por que eso esta fuera de hoja de datos, que es justamente el motivo de los BC547 de la v2).
  - **GPIO elegidos = LOS MISMOS DE LA v2** (K1=26, K2=27, K3=18, K4=23): asi entre kit y PCB el unico
    `#define` distinto es `RELAY_ON`. Ninguno es strapping (0,2,5,12,15) y ninguno tiene pull interno al
    reset. IO5 (puerta 1) **si** es strapping: con la puerta cerrada arranca en 0, y eso solo fija el timing
    del SDIO esclavo -> es seguro y ya esta en produccion desde la v2.6. Descartado IO33 para K4 porque
    choca con `PIN_DEFROST_INPUT 33` del config heredado.
  - **PUERTAS — respuesta clara a la pregunta de Matias**: con pull-up simple **NO se distingue "puerta
    abierta" de "cable cortado"** (los dos leen 1; el corte falla del lado seguro = alarma) y **el
    cortocircuito no se detecta nunca**. Opcion barata OFRECIDA, no impuesta: **doble fin de linea** (10 k en
    paralelo con el reed + 3k3 en serie, los dos EN LA CAJA DEL REED) leido por ADC -> 4 estados separados:
    **0,82 V cerrada / 1,88 V abierta / 3,30 V cortado / 0,00 V en corto**. Si se toma, las puertas se mudan
    a IO34/35/39 (solo entrada, ADC1, libres en el v1) y es cambio de firmware + 6 resistencias.
    Recomendacion: arrancar los 5 con pull-up simple (4k7 externo + 100 nF **y ademas** `INPUT_PULLUP`, para
    que si falta el 4k7 la entrada no flote).
  - **ALIMENTACION**: 4 bobinas 284 mA + LED 12 mA + DevKit 150 mA medio / 500 mA pico = **446 mA continuo,
    796 mA pico**. **Hace falta 5 V 2 A** (con 1 A anda al limite y C1/C5 pasan a obligatorios; con 700 mA
    entra en ciclo de brown-out). El amperaje de la fuente comprada **sigue siendo dato a confirmar**.
    Riel 3V3 del DevKit: 15,4 mA de todo lo externo, no se entera. Regla de armado: **USB y fuente nunca
    juntos** (el pin 5V esta unido al VBUS sin diodo en muchos DevKit).
  - **DISCREPANCIAS con `BOM_KIT_V1.md` de @hardware** (escrito en paralelo en la misma carpeta), anotadas
    en CABLEADO §10 en vez de resolverlas en silencio: (a) su checklist de continuidad usa IN1..IN4 en
    GPIO 25/26/27/32 y reeds en 16/17 — el mapa valido es el del `.net`; (b) el pide 2 sondas y 2 puertas,
    la tarea pide 3 y 3; (c) **afirma que con IN flotando "el rele cliquea y queda pegado"**, que es lo
    contrario de mi analisis: eso vale para un modulo SIN opto o con pull-down en IN. **Lo resuelve una
    medicion de 30 s** (alimentar el modulo con IN al aire y ver si cliquea), escrita como paso previo al
    armado. Si cliquea, hace falta 10 k de IN a VCC por canal y cambia la guia. Adoptado de su BOM: los
    **dos electroliticos de 1000 uF low-ESR** (C1 en la entrada, C5 al pie de las bobinas).
  - **Ocupacion de hoja 33 %** contra el 55-75 % de la doctrina: es un diagrama de cableado con 19
    componentes y mucho texto de procedimiento; se prefirio aire a apretar. Anotado como deuda menor.
  - **Proximo paso**: Matias/@verificador miran el PDF -> @hardware mide el modulo real (IN al aire) y lee
    la etiqueta de las 5 fuentes -> @firmware aplica `PINOUT_V1.md` (`MAX_RELAYS 4`, `PIN_RELAY_3 18`,
    `PIN_RELAY_4 23`, DHT fuera, `RELAY_ON LOW` que ya esta) -> Gonza y Sergio arman con `CABLEADO.md`.
    **Nada commiteado** (orden de la tarea).

- **2026-09-02 — @esquematico: DREYFUS/galgas — REV D del nodo de galga. La placa entera, en PASANTE y con MODULOS.**
  Repo `C:/Proyectos/galgas/hardware/`. Todo por el generador (`kicad/generar_nodo_galga.py`), **nada a mano sobre el
  `.kicad_sch`**. Reemplaza a la rev C que @verificador habia aprobado esta manana (P6b). **Sin commit** (ordenado).
  - **Entregables**: `kicad/nodo_galga_v3.kicad_sch` rev D (57 componentes, 50 redes, **243 cables / 52 uniones / 8
    etiquetas locales / 1 sola red por etiqueta global** = 2 % contra el 15 % que permite la doctrina) ·
    `kicad/nodo_galga_v3.net` · `kicad/erc_revD.rpt` **0/0 con `Ignored checks: None`** ·
    `kicad/DIFF_REDES_revC_revD.txt` (red por red) · `kicad/nodo_galga_v3.pdf` + `.svg` + `render_esquematico.png` ·
    **`NOTAS_REV_D.md` nuevo (C30-C40, con la simulacion numerica del ciclo)** · `NOTAS_CALCULO.md` **seccion 11**
    (no se toco nada anterior) · huellas propias `galgas.pretty/CJMCU-1220` y `CP_Radial_PB-5R0V105-R_P11.80mm`,
    **generadas desde el mismo script, con la cota a MEDIR como UNA variable de Python**.
  - **El diff de redes encontro DOS defectos electricos que el ERC 0/0 no ve** — es por esto que esta en el DoD:
    (1) el riel `/V_SC` terminaba en `x=u(102)` y el `PWR_FLAG` + la entrada del LDO quedaban en una red huerfana
    `Net-(U4-VI)`; **el ERC callaba porque el propio flag "alimentaba" esa red**. (2) **`RPU1` colgaba de la linea de
    MOSI, no de la de `CS`** (`Net-(J2-Pin_4) + RPU1.2` en el diff). Las dos corregidas y re-verificadas.
  - **Mirar el PDF encontro otras cuatro** que ninguna herramienta ve: el cable de PD7 corria por el primer renglon de
    la tabla de pines (**cable a traves de texto**); el valor de D31 impreso **encima del simbolo de masa** de RGD1
    (texto contra simbolo: el chequeador compara texto contra texto); el bajante de CLK **cruzaba** AVSS y DGND
    (resuelto reordenando el pin CLK al final de la columna del simbolo, no moviendo cables); y el bloque 5 metiendose
    en el **cuadro de rotulo** — el mismo vicio (d) de la rev C, ahora resuelto de raiz: **el interlineado se CALCULA**
    para que la ultima linea caiga arriba de 372 mm.
  - **Q2 y RG1 SALEN, y verifique el razonamiento antes de sacarlos** (es una pila de litio): con un Schottky por celda,
    la celda invertida queda con 7,2 V en inversa sobre su propio diodo y **la malla de 367 mA que Q2 nunca cubrio
    desaparece**. Lo que queda es la **fuga inversa**: BAT85 `IR <= 2 uA a 25 V/25 C` de hoja, ~22 uA a 60 C, contra el
    limite de 10 uA de la quimica. **Riesgo residual DECLARADO en la hoja**, con mitigacion de procedimiento (las dos
    pilas juntas, del mismo lote, polaridad verificada con tester).
  - **Schottky elegido: BAT85 (DO-35), no 1N5819.** El criterio es la **fuga GARANTIZADA por hoja**, no la tipica
    (misma doctrina que cerro P9): BAT85 **2 uA max a 25 V**; el 1N5819 solo garantiza **1 mA a 40 V** (100 veces el
    limite) y sus 3 uA salen de una curva tipica que a 75 C da 130 uA. Una propiedad de seguridad de litio no se compra
    con un tipico.
  - **Correccion al numero que se le presento a Matias: el diodo cuesta 224 mV, no 175.** Los 175 estan calculados a la
    corriente de **reposo**, y ese no es el punto de operacion: **el supercapacitor integra el consumo pulsado**, asi
    que sobre un ciclo el diodo pasa la corriente **MEDIA** (0,177 mA). Simule el ciclo de 300 s con la **ecuacion del
    diodo** ajustada a los maximos de hoja: `V_SC` en reposo = OCV - 224 mV, estable en los cinco casos.
    Autonomia honesta **~2,43 anos** (no 2,52).
  - **Y el numero que ordena todo (C37)**: a fin de vida (OCV 3,20 V, R_int 20 ohm, ESR_DC 1,0) **VOUT minimo = 2,643 V**.
    Contra el piso de 2,00 V (`BODLEVEL=110` **a 4 MHz**) sobran **643 mV**; contra 2,90 V (`BODLEVEL=101`) **faltan
    257 mV**. El nodo transmite hasta **OCV 2,56 V** con los fusibles bien y solo hasta **3,46 V** con los fusibles mal:
    **900 mV de OCV = la meseta entera de la pila**. Escrito en negrita en el bloque 6.
    Y **R3 (transmitir 30 s despues de medir) ya solo vale 6 mV**, no 47: con 1 F la medicion hunde la mitad y el diodo
    hace lenta la reposicion. Se mantiene porque es gratis, pero **la ultima TX la salvan los fusibles, no la espera**.
  - **Dos cuentas donde diferi de @hardware, con el numero al lado** (no las tome por orden):
    (a) **`RGD1` VUELVE A 100 k, no sigue en 1 M.** El 1 M era correcto para el MOSFET (IGSS 100 nA vs Vgs(th) 0,8 V);
    con el BJT lo que manda es la fuga del PIN del ATmega (1 uA) contra Vbe: `1 uA x 1 M = 1,0 V > 0,6 V` y **el
    shunt-cal quedaria ENCENDIDO durante el POR** — justo el modo de falla que G5 cerro, reintroducido por el cambio de
    tecnologia. (b) **`RB_Q1` = 22 k, no 100 k**: `Vce(sat)` de un BJT saturado **no tiende a cero**, tiende al voltaje
    de offset (`Vt·ln(1+1/betaR)`), y lo que entra al error no es Vce sino **Vce/Ic** = resistencia efectiva en serie con
    RCAL1. Con 100 k son 22 mV = 1298 ohm = **7,4 ue** de error de ganancia del escalon; con 22 k son 5,3 mV = **1,8 ue**,
    y la corriente de base solo circula durante la calibracion. Es sistematico y se mide en el bring-up; su deriva de
    25 a 60 C es 0,2 ue.
  - **Clamps de entrada: los puse EN EL CONECTOR, no detras de RS1** como proponia @hardware, y el motivo es un numero:
    la impedancia del nodo es **175 ohm** ahi y **1175 ohm** despues de RS1, o sea que el mismo diodo cuesta **6,7 veces
    mas error de cero**. Ademas `NODO_A` y `E_REFN` no admiten resistencia serie (una lleva la excitacion y la otra es
    REFN1), asi que dos de las tres lineas van clampeadas en el conector por obligacion. **Y la cuenta fina que no
    estaba en ningun lado**: con el puente excitado el nodo esta a `AVDD/2`, los DOS diodos quedan en inversa con casi
    la misma tension y **sus fugas se restan** -> al error entra el DESAPAREAMIENTO, no la suma (2,9 ue con 1N4148, no 5,8).
  - **C34, para @firmware**: el divisor de pila cuelga de `+BATT`, o sea **despues de los diodos**. Si deja
    `VBAT_MV_AGOTADA = 3050` mV el corte efectivo se va a **OCV 3,27 V** y se tira meseta. **3050 -> 2850 mV** y
    **3350 -> 3150 mV**, y la lectura **en reposo, antes de encender el puente** (a 10,4 mA el diodo cae 377 mV en vez
    de 224). Mas `V_BAT_SENSE` a **ADC3/PC3/pin 26** con `DIDR0` y sin pull-up, y `PC2` a masa **por 1 k** (`RSTRAP1`):
    no directo, porque el firmware maneja PC2 como salida.
  - **`RSC1` = 15 ohm y 1 W**: disipa **0,38 W durante ~20 s (4,6 J)** en la carga inicial y **eso no estaba anotado ni
    en C8 ni en C16**. Pico 160 mA totales = 80 mA por celda (40 % del pulso maximo). Y el checklist sigue valiendo:
    `V_SC > 3,0 V a los 46 s`.
  - **Huellas propias con UNA variable**: `SEP_FILAS_CJMCU = 20.32 mm` y `PASO_CSC = 11.80 mm` en el generador, con
    "PENDIENTE DE MEDIR (M2)" escrito en el `descr` del `.kicad_mod`. Cuando Matias pase el calibre se cambia **un
    numero** y se regenera; nadie edita un `.kicad_mod` a mano.
  - **Gotcha nuevo para la doctrina**: `Transistor_BJT:2N3904` es un simbolo `extends`; la copia aplanada que embebe el
    generador **no coincide byte a byte** con la libreria y el ERC lo reporta como `lib_symbol_mismatch`. Se usa el
    padre `Q_NPN_EBC` con el valor "2N3904" (mismo dibujo, misma numeracion E-B-C). Y los filtros de huella importan:
    `Device:C_Polarized` filtra `CP_*`, asi que la huella propia del supercap se llama `CP_Radial_...`.
  - **Proximo**: **@verificador** re-audita con `DIFF_REDES_revC_revD.txt` -> **@pcb** rutea con `nodo_galga_v3.net`
    rev D (restricciones de layout en `NOTAS_REV_D.md` C39; **M1 y M2 lo siguen bloqueando**) -> **@firmware** C34 y C37
    -> **@hardware** BAT85 x2, 1N3595 x6, RSC1 15R 1W, RB_Q1 22k, zocalo torneado DIP-28, y **2 ADS1220 (no 3: el
    receptor no mide)**.

- **2026-09-02 (b) — @esquematico: rev D, cierre de H-1 y H-2 de `VERIFICACION_REV_D.md`.** Aprobada con observaciones
  por @verificador (cold-start reproduce el `.kicad_sch`, el simbolo y las dos huellas **byte a byte**; 50/50 redes
  iguales; ERC 0/0 generado por el; `/E_REFN` disjunto de `GND`; 0 desajustes simbolo-huella en los 57 componentes;
  y **me dio la razon en las dos cuentas donde diferi de @hardware**, rehaciendolas). Los dos hallazgos que bloqueaban
  el layout quedan cerrados. Sin commit. **No toque `.kicad_pcb`, `LAYOUT.md` ni `gerbers/`** (@pcb esta trabajando ahi).
  - **H-1 — `SW1` tenia una huella peligrosa y se me habia perdido una pendiente de medicion. Aceptado sin discutir.**
    El reed de vidrio de 14 mm con la huella del axial de 1 W (`P15.24`) obliga a doblar el alambre a **0,62 mm del
    sello de vidrio**, que es exactamente el modo de falla que yo mismo habia escrito en negrita tres centimetros mas
    arriba en la hoja. Una huella que desmiente un aviso escrito es peor que no tener el aviso.
    **`PASO_SW1 = 22,86 mm`** (9 x 2,54, en grilla) -> **4,43 mm de alambre libre por lado**. Huella propia
    `galgas:REED_D2.7mm_L14.0mm_P22.86mm`, generada por `escribir_reed()` desde el mismo script, con el **`descr`
    explicando por que el paso no es libre** (para que nadie la "optimice" dentro de un año) y con el **courtyard
    cubriendo tambien los alambres** (+-12,33 mm), no solo el vidrio. **El paso resuelve el DOBLADO; el RTV a lo largo
    del tubo resuelve la RESONANCIA: son dos cosas distintas y hacen falta las dos.**
    **El hallazgo de metodo lo hago propio**: de las tres piezas cuya cota hay que medir, dos estaban declaradas
    (M2 CJMCU con su variable y su `descr`, M1 RA-02) **y la del reed se habia perdido**. Ahora es la tercera variable
    (`PASO_SW1` + `CUERPO_SW1`) y **`M5`/`D14` en C40**. `CUERPO_SW1 = (14,0 x 2,7)` sigue siendo `[SUP]`: @hardware da
    la parte, Matias mide, se cambia **un numero** y el nombre de la huella y el `descr` se recalculan solos.
  - **H-2 — faltaba la restriccion de layout mas importante, y corrige el G18 de la rev C.** `L10` agregada a C39, con
    su cuenta en **C39.1**: 20 mohm de cobre entre las tomas de `+3V0` de `R1` y de `R2` son
    `4,25 mA x 20 mohm = 85 uV = **56,7 ue de CERO CORRIDO**`, tolerancia para 1 ue = **0,353 mohm**, deriva
    **0,22 ue/C** (del mismo orden que la EMF termica de `L1`, y esta no se calibra sola). En cambio los mismos
    20 mohm entre el tope del puente y la toma de `REFP1` -que es adonde apuntaba G18- son **58 ppm = 0,06 ue de
    GANANCIA**: despreciable y calibrable. **G18 senalaba el nodo equivocado.**
    **Corolario que le sirve a @pcb: no hace falta partir `+3V0` con un net-tie.** Con que `R1.1` y `R2.1` caigan en el
    mismo pad (idem `R3.2` y `J1.3` sobre `E_REFN`, y la toma Kelvin de `REFP1`/`REFN1` en esos mismos puntos) el
    problema desaparece, porque no hay corriente entre las dos tomas. Es colocacion, no un componente.
  - **`L10` tambien quedo escrita en la hoja** (bloque 5, cuatro renglones con los numeros), porque es la restriccion
    que decide el cero de la placa y no puede vivir solo en un `.md`.
  - **Mirar el PDF otra vez encontro dos cosas mas**: la ultima linea del bloque 5 caia **justo sobre el borde del
    marco** y salia tachada (el objetivo del calculo automatico de interlineado baja de 372 a **368 mm**), y al
    condensar las notas en la pasada anterior habia quedado **una frase cortada** ("...y un zocalo de" sin
    continuacion). Las dos corregidas.
  - **Evidencia re-corrida**: `verificar_sch.py` **TODO OK** (108 refs anotadas, 57 huellas, ERC **0/0 sin chequeos
    apagados**, netlist sin advertencias) · `chequear_solapes_sch.py` **0 solapes** · `erc_revD.rpt` con
    `Ignored checks: - None` · netlist, PDF, SVG y `render_esquematico.png` regenerados · `DIFF_REDES_revC_revD.txt`
    rehecho (50 redes, sin cambios de conectividad respecto de la version aprobada: **lo unico que cambio en el
    netlist es la huella de `SW1`**).

- **2026-09-02 (c) - @esquematico: rev D, trazabilidad de rotulos y el aviso de serigrafia de @pcb.**
  Sin commit. Solo se toco `hardware/kicad/generar_nodo_galga.py` (+ lo regenerado) y `hardware/NOTAS_REV_D.md`.
  **No** se tocaron `.kicad_pcb`, `LAYOUT.md`, `gerbers/`, `MODULOS_REV_D.md`, `ENERGIA_REV_D.md` ni
  `VERIFICACION_REV_D.md`.
  - **Mis decisiones `D1`..`D14` de `NOTAS_REV_D.md` pasan a `DE-1`..`DE-14`** (uno a uno, sin reordenar).
    Choque real que levanto @hardware barriendo etiquetas: `D1`-`D4` son **designadores de componente** de esta
    misma placa (los clamps de la galga y el ESD del riel), y en mi propio documento conviven con `D11`, `D12`,
    `D21`, `D22`, `D31` y `D32`, que tambien son refdes. **El que se mueve es el rotulo de documento, no el
    refdes**: un designador vive en el netlist, el BOM, la serigrafia y la guia de armado. Coincido con el
    criterio de @hardware de no renumerar los suyos.
  - **Las citas ajenas siguen encontrandose**: agregue el mapeo como recuadro al principio de C40, con los dos
    casos citados desde afuera explicitos - **`D14` = `DE-14`** (la cota del reed, citada junto a `M5` en
    `VERIFICACION_REV_D.md` y en el plan maestro) y **`D5` = `DE-5`** (citado como "D5 de C40" en
    `NOTAS_CALCULO.md` 11.3, que no podia editar). **El nombre viejo queda como alias valido y la nota es lo
    que lo garantiza.**
  - Anotadas en el mismo recuadro las convenciones que se acordaron para no repetir el enredo: **`M5` sigue
    siendo mio** (@hardware movio su prueba de ruido del ADC a `M16`); los `C*` se citan **con el dueno**
    adosado ("calculo C6" contra "contradiccion C6 de @diseno"); y **`C-1`/`C-2`/`C-3` con guion** son las tres
    confirmaciones de conteo del bring-up, **no** los calculos `C1`/`C2`/`C3`.
  - **Cerrado el aviso de serigrafia de @pcb** (eran 2 avisos del DRC, el mismo defecto una vez por pata): la
    linea que representa el alambre en `REED_D2.7mm_L14.0mm_P22.86mm` llegaba hasta **-11,43 / +11,43**, o sea
    el CENTRO del pad, y entraba 0,90 mm en el cobre. Ahora termina en **+-10,40**, con el borde del pad en
    **+-10,53**: **0,13 mm de aire**. Y no quedo como numero fijo: sale de la geometria
    (`SILK_FIN = pr - PAD_SW1/2 - 0,13`), asi que si cambia `PASO_SW1` o el pad, el corte se recalcula solo.
    Verificado con un chequeo geometrico propio (extremos de serigrafia contra el radio de cada pad):
    **serigrafia fuera de todo pad**.
  - **Evidencia re-corrida**: `verificar_sch.py` **TODO OK** (ERC **0/0** con `Ignored checks: - None`, 108 refs
    anotadas, 57 huellas) - `chequear_solapes_sch.py` **0 solapes** - netlist, PDF y `render_esquematico.png`
    regenerados - `DIFF_REDES_revC_revD.txt` rehecho: **50 redes, conectividad identica a la version aprobada**
    (el cambio es solo de serigrafia dentro de la huella, no toca el netlist).

- **2026-09-04 — @esquematico: DREYFUS/galgas — REV E.1: puentes de aislación entre etapas.**
  Repo `C:/Proyectos/galgas/hardware/`. Todo por el generador (`kicad/generar_nodo_galga.py`), **nada a mano
  sobre el `.kicad_sch`**. Sin commit. **No** se tocaron `nodo_galga_v3.kicad_pcb`, `LAYOUT.md` ni `pcb/`.
  - **Primero, la rev E que dejó el turno cortado**: el `.kicad_sch` sí era rev E (44 piezas, JP2/JP3, sin D11..D32)
    pero **`nodo_galga_v3.net` seguía siendo el de la rev D** (nadie lo copió), el ERC estaba **0/2** (filtro de huella
    de `Jumper_*_Open` contra la tira de pines) y **nunca corrió `chequear_solapes_sch.py`**: había 3 textos pisados
    (título B1 sobre título B2, "modos de JP2" sobre "E_REFN NO ES MASA") y el `+3V0` de `RPU2` **dibujado encima del
    cable de NSS** (red bien, dibujo que se leía como corto). Además `C41..C45`, que la hoja cita, **no existen en
    `NOTAS_REV_D.md`**: quedan como deuda del turno de la rev E (anotado en C46). La rev E quedó congelada en
    `kicad/revE/` + `kicad/nodo_galga_v3_revE.net` como baseline del diff.
  - **Rev E.1 = rev E + 15 solder jumpers cerrados de fábrica** (`Jumper:SolderJumper-2_P1.3mm_Bridged_RoundedPad1.0x1.5mm`,
    net-tie, fuera del BOM): `JB11..15` sensor→ADC (+3V0 excitación, E+, S+, S-, E-), `JB21..23` ADC→micro (MISO rama,
    CS_ADC, DRDY), `JB31..34` LoRa→micro (MISO rama, NSS, RESET, DIO0), `JB41..43` +3V0 de CJMCU / micro / RA-02.
    **Refs numéricas** porque KiCad no anota `JB1a`. `SCK`/`MOSI` sin puente (compacidad) y la consecuencia escrita
    en la hoja (módulo sin +3V0 se alimenta por ESD si el bus habla). Pull-ups del lado del módulo. `JB11` aguas
    arriba del estrella → no toca L10 (0,3 mΩ × 4,25 mA = 1,3 µV, modo común y ratiométrico). **Tabla de aislación
    dibujada en el bloque 4** y en `salida/revE1_puentes.png`.
  - `JP2`/`JP3` → `Conn_01x03`/`Conn_01x02` (misma T; ERC vuelve a 0/0). PWR_FLAG en cada isla detrás de un `JB4x`.
  - **Evidencia**: `verificar_sch.py` TODO OK — ERC **0/0, `Ignored checks: None`** (`erc_revE1.rpt`) ·
    `chequear_solapes_sch.py` **0 solapes / 0 rotados** · netlist rev E.1 **59 comp / 64 redes** ·
    `DIFF_REDES_revE_revE1.txt`: 37 idénticas, 2 renombradas (JP2/JP3), y cada red tocada contiene exactamente un
    `JBxx` (`/S_MAS`, `/S_MENOS`, `/E_REFN`, `/NODO_A` conservan sus nodos salvo el pin del ADC que cruzó el puente) ·
    PDF/SVG/`render_esquematico.png` regenerados y **mirados** (6 recortes; corregí 3 rótulos pisados que sólo se
    veían en el render).
  - **Cuentas y restricción de layout**: `NOTAS_REV_D.md` **C46** (qué, por qué, tabla de uso, decisiones) y
    **L11** en la tabla C39 (placa alargada con etapas en fila; puentes contiguos en la frontera, accesibles con cutter).
  - **Próximo**: @verificador re-audita con `DIFF_REDES_revE_revE1.txt` → @pcb rutea con `nodo_galga_v3.net` rev E.1
    (L11). Deuda: escribir C41..C45 de la rev E.

- **2026-09-04 [FRIOSEGURO / TERMOVIGIA MINI] Esquematico completo de la PCB v1: el kit v1 hecho placa,
  con el modulo de rele ENCHUFADO COMO SHIELD. Carpeta nueva `C:\Proyectos\frioseguro\hardware\mini\`.**
  - **Entregables**: `termovigia_mini.kicad_sch` (A3, **una hoja**, 7 bloques, 70 componentes, 35 redes con
    nombre + 18 NC) + `.kicad_pro` + `.pdf` + `.net` + `_bom.csv` + `erc.txt` + `salida/p1.png` y 7 recortes ·
    `generar_sch.py` (usa `C:\Proyectos\biblioteca\pc\kicad_gen` por sys.path) · `termovigia_mini.kicad_sym`
    (4 simbolos propios) · `termovigia_mini.pretty/ESP32_DEVKIT_38_2x19_P2.54mm.kicad_mod` (huella generada
    por el mismo script) + `fp-lib-table` · **`DISENO_MINI.md`** (calculos K1-K8, medidas M1-M7, envolvente,
    riesgos) · **`PINOUT_MINI.md`** (para @firmware) · **`ALCANCE_1WIRE.md`** (la cuenta del 2k2, rev B con
    el caso de 25 m) · **`BOM_MINI.md`**. **Nada commiteado** (orden).
  - **Evidencia**: ERC `--severity-all` **0 errores / 0 advertencias con `Ignored checks: None`** (los 43
    chequeos encendidos a mano en el `.kicad_pro`, doctrina G25 de galgas); `chequear_solapes_sch` **0 solapes,
    0 texto fuera del area util**; PDF exportado y **mirado** (hoja completa + 7 recortes a 260 dpi, 6 pasadas);
    **netlist leido red por red**. 167 cables / 48 uniones / **4 redes por etiqueta de 40 = 10 %** (SDA, SCL,
    DEFROST1, DEFROST2), debajo del 15 % de la doctrina.
  - **Circuito**: J1 5 V -> **D1 SB540 serie** (inversion + no devuelve a la fuente si esta el USB) -> C1
    1000 uF + C2 100 nF; **bus 1-Wire con 6 sondas** en 2 borneras de 9 vias (grupos V-D-G), R3 22R 1W en el
    VCC de sondas, R1 2k2 + **R18 1k8 SIN POBLAR**, D2 P6KE6.8CA + R2 100R + D3/D4 clamps; **4 puertas** (se
    usan 2) con TVS en bornera + 100R + 10k + 100 nF; **shield de rele** = J8 (JD-VCC/VCC/GND) + J9
    (GND/IN1/IN2/VCC) con **el jumper del modulo SACADO** (VCC a +3V3, JD-VCC a +5 V) y R12/R13 10k a +3V3;
    **2 entradas de defrost optoacopladas** (PC817 + 2k2 0,5W + 1N4148 antiparalelo + RC 10k/10uF) con
    **barrera de aislacion dibujada**; buzzer activo por BC547; LED de encendido (fijo) y LED de latido;
    pulsadores RESET (EN) y WiFi (IO0); header I2C sin poblar; 8 agujeros M3.
  - **Pinout = el del kit v1** (1-Wire 4, puertas 5/13/14 + **25 nuevo**, reles 26/27, buzzer 19, LED 2):
    del firmware `HW_KIT_V1` solo cambian `MAX_RELAYS 2`, `MAX_DOOR_SENSORS 4`, `PIN_DOOR_4 25`,
    `MAX_PROBES 6`, `PIN_DEFROST_INPUT_2 32` y **borrar `PIN_CURRENT_SENSOR 32`** (si queda, pelea el pin
    con el 2do defrost).
  - **La cuenta que ordena el 2k2 (ALCANCE_1WIRE)**: el que muestrea es el **ESP32**, no la sonda
    (`VIH = 0,75x3,3 = 2,48 V` contra 2,2 V del DS18B20) -> `t = R C ln4 = 1,386 R C`. Con 100 pF/m:
    **4k7 = 651 ns/m (5 us a 7,7 m)** contra **2k2 = 305 ns/m (5 us a 16,4 m)**: **2,14x mas cable con el
    mismo margen**, y los 5 us son la mitad de los 10 us que deja `OneWire::read_bit()`. Costo: la sonda
    hunde 1,5 mA y garantiza 4,0 mA (2,7x). **Con los 25 m que pide Santa Cruz el 2k2 da 7,6 us: entra pero
    sin margen** -> por eso R18 (1k8 en paralelo = 990 ohm -> 3,4 us, margen de corriente 1,2x), que se
    puebla **solo si la prueba de banco M6 lo pide**. Cable: par trenzado con DQ y GND en el MISMO par.
  - **CAMBIO DE ALCANCE a mitad de la sesion (cliente de Santa Cruz: 2 reefers por placa)**: se agregaron las
    2 entradas de defrost (GPIO33 reefer A / GPIO32 reefer B, ninguno es strapping, ADC1 pero van digitales)
    con el mismo circuito ya validado en la v2 hoja 2 bloque 3, y **la placa dejo de entrar en 100 x 80 mm**:
    32 posiciones de bornera x 5,08 = 163 mm de paso, ~195 mm con las cajas, y el pedido es que **todas vayan
    en el MISMO borde** (prensacables de la caja IP65). **No cambie la medida solo**: DISENO_MINI seccion 8
    propone **200 x 80 (recomendada)** o 130 x 100 con dos filas escalonadas, y lo decide Matias. **Aviso**:
    @diseno3d esta haciendo en paralelo un gabinete impreso en `hardware/mini/gabinete/` dimensionado para
    100 x 80 — con la caja IP65 de ferreteria queda sin uso. No lo toque.
  - **HALLAZGO que encontro el netlist y que el ERC 0/0 NO ve**: en el primer armado del bloque 2, el **bus de
    VCC de sondas y el bus de datos salieron en la misma red** (`/VSONDAS` traia los pines 1,2,4,5,7,8 de las
    dos borneras). El ERC no dijo nada. Un test controlado (agregar a mano un cable que cruza tres buses y
    re-exportar el netlist) demostro que **un cruce puro NO conecta**; el defecto estaba en como salia el bus
    de datos por encima del bus de VCC. Solucion estructural: **el bus de DATOS va MAS AFUERA que los de VCC y
    GND**, asi su salida hacia el GPIO no cruza a los otros dos. **Regla: el netlist es la unica autoridad;
    leerlo red por red no es opcional.**
  - **Rotulos**: los calculos de la hoja se llaman **K1..K8**, no C1..C7, porque `C1`..`C8` son designadores de
    capacitor de esta misma placa (mismo criterio que `DE-1..DE-14` en galgas: el que se mueve es el rotulo de
    documento, no el refdes).
  - **Otros gotchas de esta sesion**: (a) `Connector:Screw_Terminal_01x02` **no esta centrado** (pin 1 en y=0,
    pin 2 en -2,54), a diferencia del 01x09 — el mismo vicio que el `Conn_01x06` de la v2; (b) el area util de
    la A3 es **15..405 x 15..250 mm**, bastante mas chica que el borde de la hoja: tres bloques de texto y dos
    marcos se salian y solo lo dijo `chequear_solapes_sch`; (c) el chequeador compara texto contra texto, **no
    texto contra simbolo**: el bloque de notas del jumper pisaba los simbolos J8/J9 con 0 solapes reportados —
    se ve mirando el PNG; (d) los conectores genericos con pines sin nombre (`Conn_01x03/04`) hacen ilegible un
    shield: se reemplazaron por **simbolos propios con los nombres de pin** (JD-VCC/VCC/GND, GND/IN1/IN2/VCC,
    GND/VCC/SCL/SDA) y desaparecieron 7 notas al lado del conector; (e) `four_way_junction` con los 43 chequeos
    encendidos delato un nodo con 4 cables en el clamp del GPIO4: se separo el tap de D4.
  - **Proximo paso**: **Matias decide la envolvente (seccion 8) — es lo que bloquea a @pcb** -> Gonza mide
    M1..M5 con calibre (5 variables de Python y se regenera) -> @verificador audita el `.net` -> @hardware
    confirma BOM y responde si el defrost del reefer es 12-24 V o contacto seco (R3) y si el modulo de rele
    clickea con IN al aire (M7) -> @tester corre M6 (100 lecturas de 1-Wire con 25 m reales) -> @pcb rutea ->
    @firmware aplica `PINOUT_MINI.md`.

- **2026-09-04 [FRIOSEGURO / TERMOVIGIA MINI **LITE**] La placa de las demos de Bahia: la Mini adelgazada.
  Carpeta nueva `C:\Proyectos\frioseguro\hardware\mini_lite\`. **`hardware/mini/` NO se regenero**
  (verificado por mtime: `.kicad_sch` 12:22 y `.kicad_pcb` 15:01, anteriores a la sesion).**
  - **Entregables**: `termovigia_mini_lite.kicad_sch` (A3, 1 hoja, 7 bloques, **47 componentes**,
    22 redes con nombre + 24 NC) + `.kicad_pro` (los 42 chequeos de ERC encendidos, copiados de la
    Mini) + `.pdf` + `.net` + `_bom.csv` (**30 lineas**) + `erc.txt` + `salida/p1.png` y 6 recortes ·
    `generar_sch.py` · `termovigia_mini_lite.kicad_sym` + `.pretty` + `fp-lib-table` ·
    **`DISENO_LITE.md`** (que salio y por que, tabla antes/despues, K1-K7, **cota A1**, envolvente) ·
    **`PINOUT_LITE.md`** · **`BOM_LITE.md`**. **Nada commiteado** (orden).
  - **Evidencia**: ERC `--severity-all` **0/0 con `Ignored checks: None`**; `chequear_solapes_sch`
    **0 solapes / 0 texto fuera del area util**; PDF exportado y **mirado** (5 pasadas: hoja completa
    + 5 recortes a 260-300 dpi; se corrigieron 6 defectos que solo se ven mirando); **netlist leido
    red por red**. 112 cables / 30 uniones y **0 conexiones por etiqueta**: las 10 etiquetas son
    documentacion sobre un cable que existe (incluido DEFROST, que en la Mini era etiqueta pura).
  - **QUE SALIO** (orden del Director, "debe ser simple faz la placa"; 2 capas se mantiene porque en
    JLCPCB cuesta lo mismo): 5 TVS P6KE6.8CA, 4 de los 5 1N4148, buzzer + BC547 + sus 2 R, header
    I2C, 2 de las 4 puertas, 1 de los 2 optos. **QUEDA** el DevKit en zocalo, el shield de rele
    (2 hembras + 4 M3 + jumper JD-VCC sacado + 10k de IN a 3V3), el bus 1-Wire con 2k2 + 6 sondas,
    5 V, 2 LED y RESET/WiFi.
  - **Componentes 70 -> 47 (-33 %)**; a soldar **62 -> 39 (-37 %)**; BOM 35 -> 30 lineas; posiciones
    de bornera **32 -> 26**. **Envolvente: 100 x 80 mm, ENTRA** (borde de 100: 3 sondas 45,0 + 2
    puertas 20,0 + alimentacion 10,0 = **75,0** sobre 87 libres; borde de 80: defrost 10,0 + 6 mm de
    aire + 3 sondas 45,0 = **61,0** sobre 67). Presupuesto de area **65 %** con la restriccion **L1**
    (bajo el modulo de rele, sobre separadores M3, van SOLO axiales acostados <= 4 mm; sin L1 se iba
    a 83 %). Fallback declarado: 110 x 80 sin mover borneras.
  - **Decisiones con criterio, no por lista**: (a) **los 100R de las puertas QUEDAN** — son lo que
    convierte a C3/C4 en un filtro de `100 ohm x 100 nF = 10 us` frente al cable; sin ellos el
    capacitor se carga desde el cable con impedancia casi nula y el flanco llega entero al pin
    (K4); (b) **D2 1N4148 queda**: no es clamp de entrada, protege el LED del PC817 (VR max 6 V)
    contra alterna o polaridad invertida; (c) **NO se dejaron huellas DNP de los TVS**: son DO-15 de
    13 mm justo en el borde de las borneras, que es lo que hay que despejar; la variante protegida
    ya existe entera y ruteada en `mini/`; (d) justificacion del retiro por norma, no por corazonada:
    **IEC 61000-4-5 clase de instalacion 0-1** para linea corta interior (no se ensaya sobretension).
  - **Los 3 hallazgos de @verificador (`mini/VERIFICACION_LAYOUT_2026-09-04.md`) atendidos**:
    1. **Cota A1** escrita en la hoja Y en DISENO_LITE 4: el keepout de aislacion **arranca en el
       BORDE DE LA PLACA** (rectangulo 30 x 18 mm centrado en J10 hasta el eje del PC817), incluye
       la bornera y el agujero M3 de la esquina, el plano de GND queda a >= 6,0 mm, y **6 mm de aire
       entre J10 y la bornera vecina**. El 6,0 sale de IEC 60664-1 (250 Vrms, polucion 2, IIIa:
       ~5,0 mm reforzada) y es **coherente con los 5,9 mm que fisicamente da el DIP-4 del PC817**
       (7,62 de paso - 1,7 de pad): no se declara mas de lo que el componente sostiene. El defecto
       de la Mini (6 mm declarados bajo el opto, **0,3 mm reales en la bornera**) no puede repetirse.
    2. **PASO 5,00 mm, TODAS** (`TerminalBlock_MaiXu_MX126-5.0-0xP`), en el cajetin de la hoja y en
       DISENO_LITE 5 en negrita. Y el harness: en `comun.py` las constantes se llaman **`FP_TB2_508`
       / `FP_TB2_500` / `FP_TB3_500`** — el paso va **en el nombre**, para que no se pueda mezclar.
       Ademas **6 borneras de 3 vias, una por sonda** en vez de 2 de 9: es lo que se consigue en AR,
       una bornera = una sonda, y el largo de borde es identico (6x3x5,00 = 2x9x5,00 = 90,0 mm).
    3. **No se publican coordenadas de pad**: DISENO_LITE 6 le pide a @pcb publicar el **CENTRO DEL
       COMPONENTE** para @diseno3d, con el motivo escrito (`SW_PUSH_6mm` tiene **dos pads numerados
       "1"**, el centroide de "el pad 1" no es el vastago).
  - **UNA sola fuente de verdad**: nuevo **`hardware/mini/comun.py`** con lo que no puede
    desincronizarse entre las dos placas (cotas M1..M5, constantes de huella, mapa de pines fisicos
    del DevKit, escritor del `.kicad_mod` del zocalo). **Los dos** generadores lo importan. **No** se
    compartio el dibujo: son dos circuitos distintos, no dos poblados, y un flag convertiria cada
    coordenada en un condicional. **Verificado**: `mini/generar_sch.py` refactorizado reproduce su
    `.kicad_sch` **byte a byte salvo UUID** (+ `.kicad_sym` y `.kicad_mod` identicos), probado en
    copia aislada en el scratchpad; los archivos de `mini/` no se regeneraron.
  - **Gotchas nuevos**: (a) helper **`y_centro(lib_id, y_pin1)`** — los `Screw_Terminal` de KiCad no
    estan centrados igual segun la cantidad de vias (ya habia mordido con el 01x02 y el `Conn_01x06`);
    ahora la posicion se **calcula** desde el PINMAP en vez de asumirse; (b) los **comentarios del
    cajetin** se salen del cuadro por derecha y **ningun chequeador los mira** (el de solapes no ve
    el title block): hay que contarlos a mano, ~70 caracteres; (c) el valor de un pulsador con
    `val_off=(-3,4)` cae exactamente sobre el bajante a GND: se ve solo en el PNG; (d) ocupacion
    **46 %** contra el objetivo 55-75 % de la doctrina — aceptado y declarado: el pedido era una hoja
    **mas despejada**, y la A3 se mantiene para no partir los calculos.
  - **Proximo paso**: @verificador audita el `.net` y **la cota A1** -> @hardware compra (BOM_LITE:
    **borneras MX126 de 5,00**, 4x2P + 6x3P) y mide M1..M5 -> @pcb rutea a **100 x 80** con L1 y A1,
    y publica **centros de componente** de LED/pulsadores para @diseno3d -> @firmware aplica
    `PINOUT_LITE.md` (MAX_RELAYS 2, MAX_DOOR_SENSORS 2, MAX_PROBES 6, sin buzzer, sin 2do defrost,
    la sirena pasa a ser carga del rele).

- **2026-09-04 (b) — @esquematico: DREYFUS/galgas — REV F. Medio puente FIJO con galga doble + la protección
  de entrada que faltaba. 12 de los 17 hallazgos de `VERIFICACION_REV_E1.md`, cerrados.**
  Repo `C:/Proyectos/galgas/hardware/`. Todo por el generador (`kicad/generar_nodo_galga.py`), **nada a mano**.
  Sin commit. **No** se tocaron `nodo_galga_v3.kicad_pcb`, `LAYOUT.md`, `pcb/` ni `U2` (hay una decisión de
  Matías pendiente sobre pasar el micro a Pro Mini).
  - **Decisión de Matías: se descarta el ¼ de puente.** SALEN `JP2` y `R1`; los dos brazos activos son las dos
    rejillas de la galga doble que ya está pegada en Dreyfus. Eso cierra **H-1** (no hay dos modos, así que no
    hay modo silencioso ni strap que agregar), **H-12** (no hay contacto mecánico dentro de un brazo: eran
    28,6 µε que saltan por fretting) y ordena **H-2**.
  - **`J1` reordenado (H-14)**: `1 MALLA · 2 E+ · 3 G1 · 4 SENSE · 5 E_REFN`. `E_REFN` —el riesgo #1— queda en
    un extremo y su único vecino es `SENSE`: **ese corto da fondo de escala, o sea que se ve**. `G1` y `SENSE`
    van los dos a la unión de las rejillas (uno lleva el shunt-cal, el otro no lleva corriente).
  - **Las DOS constantes del shunt-cal, escritas en la hoja (H-2/H-15)**: el escalón eléctrico es fijo,
    **−1,5015 mV**, y eso es **500,5 µε en flexión (+ε/−ε) y 770,0 µε en Poisson (+ε/−0,3ε)**. "1000 µε
    exactos" salió de todos lados: era del ¼ y encima eran 1001,0. **`M17` (= `DE-16`) queda abierto y
    bloquea la calibración**: en qué configuración están las galgas de Dreyfus.
  - **H-13, la protección de E+/E−, decidida con la cuenta**: por esas dos líneas circulan los **8,5 mA de
    excitación**, así que **no admiten R serie** (1 Ω en `E_REFN` = 2900 ppm de ganancia; 1 Ω en `E+` = 1400 µε
    de cero). Entonces: (1) **la protección primaria es la MALLA** — el cable apantallado pasa a ser requisito
    escrito, con el número que lo justifica (100 pF acoplados de un variador = 500 mA de pico y 1,28 mA medios);
    (2) **4 clamps 1N3595 en el conector** (`DE1/DE2` en E+, `DR1/DR2` en E_REFN), fuga 1 nA → **0,06 µε**;
    (3) **`RS3` = 100 Ω** en la toma Kelvin de `REFP1`, que baja el diodo interno de `AIN0` de 77 mA a
    **3,8 mA** y cuesta 17 ppm calibrables; (4) **`D4` vuelve al riel y cambia de parte**: `ESD5Z3.3T1G`, no el
    `ESD5Z5.0` de la rev D, que empezaba a conducir **por encima** del absoluto de 3,9 V del RA-02.
    Y el **criterio de reversión ahora es observable en campo** (el de la rev E no podía activarse nunca):
    el ATmega mide su propio riel con la referencia interna de 1,1 V contra `AVCC` — **si un nodo instalado
    reporta VCC > 3,15 V hay inyección por el cable**. Cuesta cero y es `DE-15` para @firmware.
  - **Documentación (H-6, H-7, H-8, H-9, H-10, H-11, H-17)**: escritos **`C41`** (galga doble: las tres
    orientaciones, y que el caso "las dos rejillas iguales" da 0,000 µV/µε **exactos** y ningún autotest lo
    ve), **`C42`**, **`C43`**, **`C44`** (los clamps, con el criterio de campo), **`C45`** (`CO2`/`CBLK1`, y la
    interacción `JB43`↔`CR2` resuelta **sin agregar piezas**: `CR2` alimenta el pulso de la radio que el
    puente cortado desconecta) y **`C47`** (la rev F entera). `C32` queda marcado **DEROGADO** (Q1/Q3/RGD no
    existen), `L3` sin `CBLK1`, `C33` con la capacidad real (12,6 µF, 10,1 detrás de `JB43`), `C36` con los
    clamps y `D4` reales (22,2 µA), `L10`/`C39.1` con `J1.5` y con la tolerancia del ½ puente (0,71 mΩ),
    y `C46.2` corregido: **`JB15` NO lleva 0 corriente, lleva los 8,5 mA** — de ahí sale **`L12`** (clase
    EXCITACIÓN para @pcb) y **`L13`** (los clamps van EN el conector). `CO1` pasa a **2u2 X7R** (H-17: un
    disco de 1 µF Y5V son 0,2 µF reales, debajo del mínimo del MCP1700). Cable unificado en 5 m de diseño.
  - **Evidencia**: `verificar_sch.py` **TODO OK** — ERC **0/0 con `Ignored checks: None`** (`erc_revF.rpt`),
    110 refs, 63 huellas · `chequear_solapes_sch.py` **0 solapes / 0 rotados** · netlist rev F **63 componentes
    / 63 redes** · `DIFF_REDES_revE1_revF.txt`: 56 redes idénticas, y lo único que se mueve es lo que se pidió
    (`/E_MAS_DOBLE`+`Net-(JB11-A)` → `/E_MAS`; `J1` corriendo de pin; los 4 clamps y `D4` colgando de `+3V0`/
    `GND`; `RS3` partiendo la toma de `REFP1`). **`/S_MAS`, `/S_MENOS` y `/NODO_B` intactas nodo por nodo** ·
    PDF/SVG regenerados y **mirados** (`salida/revF_bloque_sensor.png`, `salida/revF_puentes.png`) ·
    rev F congelada en `kicad/revF/`.
  - **Lo que NO cerré, y de quién es**: H-3/H-4/H-5 (`PINOUT.md`, @firmware), H-16 queda como `L12` para @pcb,
    y `M17`/`M18`/`M19` + `DE-19` (cable apantallado en el BOM) son mediciones de @hardware y Matías.
  - **Próximo**: @verificador re-audita la rev F con el diff → @pcb rutea con `nodo_galga_v3.net` rev F
    (L10..L13) → @firmware toma `DE-15` (alarma de riel) y la constante de calibración cuando cierre `M17`.

- **2026-09-04 [FRIOSEGURO / TERMOVIGIA MINI **LITE**] rev B: la placa que se hace en casa con acido.**
  Todo regenerado en `C:\Proyectos\frioseguro\hardware\mini_lite\` (`generar_sch.py`, nada a mano).
  **`hardware/mini/` no se regenero** (solo se le agregaron a `comun.py` dos constantes de huella y un
  parametro opcional en `simbolo_esp32`; su `.kicad_sch` no se toco). **Nada commiteado** (orden).
  - **Entregables**: `termovigia_mini_lite.kicad_sch` rev B (A3, 6 bloques, **45 componentes**) + `.pdf` +
    `.net` (**46 redes**) + `_bom.csv` (**21 lineas**) + `erc.txt` + `salida/p1.png` y 4 recortes ·
    `DISENO_LITE.md` reescrito (secciones 1 conexionado completo, 2 rev A->rev B, 3 tabla antes/despues,
    4 calculos K1-K7, 5 pasos de bornera, 6 envolvente, **7 notas de SIMPLE FAZ**, 8 M1-M5, 9 riesgos) ·
    `PINOUT_LITE.md` (tabla GPIO con **pin fisico y tira**, config.h, strapping uno por uno, redes) ·
    `BOM_LITE.md`.
  - **Evidencia**: ERC `--severity-all` **0/0 con `Ignored checks: None`**; `chequear_solapes_sch`
    **0 solapes / 0 texto fuera del area util**; PNG **mirado en 4 pasadas** (se corrigieron 3 defectos que
    el chequeador no ve); `.net` **leido red por red**.
  - **Que cambio (3 correcciones del Director durante la sesion, la ultima manda)**: (1) fuera la entrada de
    **defrost entera** (bornera, PC817, 2k2 0,5 W, 1N4148, pull-up, RC) y **con ella la cota A1**: sin tension
    de campo, todo el cobre es de baja tension y el plano de masa puede correrse entero por la unica cara;
    (2) **puertas 2 -> 5** (IO5, IO13, IO14, IO25, **IO33**) con **MASA COMUN**, en **2 borneras de 3**
    (6 posiciones); (3) **sondas: de 6 borneras de 3 vias a UNA sola bornera de 3** (V/D/G) de **perfil alto**
    -- todas las sondas van EN PARALELO, la placa solo tiene tres redes de sonda. **Conexionado total: 4
    borneras (2+3+3+3 = 11 posiciones, 55,2 mm de borde) + los 2 zocalos del shield de rele.** Los contactos
    COM/NO/NC **no pasan por la placa**: estan en las borneras del propio modulo.
  - **Componentes 47 -> 45**, a soldar 39 -> 37, BOM 30 -> 21 lineas, **posiciones de bornera 26 -> 11**,
    piezas de bornera 10 -> 4. **Envolvente sugerida 120 x 80 (fallback 130 x 90), la fija @pcb**: con 55 mm
    de borde el limite ya **no son las borneras sino el ruteo en una sola cara**.
  - **Lo que aporto pensar en SIMPLE FAZ (y una correccion a lo que yo mismo habia escrito)**: en la primera
    pasada declare que "los 5 GPIO de entrada son 5 pines fisicos consecutivos de la columna izquierda". **Es
    falso**: en el DevKit de 38, IO4 e IO5 son los **fisicos 32 y 29 (tira DERECHA)**; IO13/14/25/33 son los
    **15-12-9-8 (tira IZQUIERDA)** y **IN1/IN2 son los 10 y 11, en el medio de esas**. Lo correcto, y esta
    escrito en la hoja y en DISENO 7: las 4 puertas 2..5 caen juntas y se rutean paralelas; **ONEWIRE, DOOR1,
    IN1 e IN2 (4 pistas) cruzan por el pasillo libre de ~20 mm que queda ENTRE las dos tiras del zocalo** ->
    4 pistas de 0,5 mm en 20 mm, cero puentes. Ademas: los 6 pull-up en UNA fila (un solo hilo de +3V3),
    pad 3,0 / agujero 1,0 (1,3 en J2) con **corona >= 0,8 mm** porque sin metalizado la corona la sostiene el
    estano de un solo lado, y los puentes que hagan falta **se declaran** en el LAYOUT.
  - **Cambio de dibujo con motivo**: el simbolo del DevKit de esta placa usa un **orden de columna propio**
    (`ESP_IZQ_LITE`) para que las 6 entradas queden en filas seguidas; el **mapa** de pines
    (numero-nombre-tipo) sigue saliendo de `comun.py`. `simbolo_esp32(K, izq=...)` ahora acepta el orden;
    `mini/` no cambia. El orden es dibujo, el mapa es dato: lo compartido es el dato.
  - **Decisiones con cuenta, no por gusto**: (a) **el comun de las puertas es MASA y no positivo** -- un cable
    que roza el chasis (a tierra) toca masa; con comun positivo el chasis quedaria a 3V3 y un segundo roce
    daria PUERTA CERRADA falsa. Diafonia del retorno compartido: 10 m de 0,20 mm2 = 0,9 ohm x 1,65 mA =
    **1,5 mV** contra VIL 0,83 V; (b) **K3 recalculado para el paralelo**: 8 sondas = 12 mA sobre R3 22R =
    0,26 V -> 3,04 V, y el minimo del DS18B20 es 3,0 V -> **el limite de la placa son 8 sondas**; para mas,
    R3 10 ohm y entonces el corto son 1,1 W (R3 de 2 W); (c) **IO33 verificado**: input-capable, RTC/ADC1_CH5,
    **no strapping** -> sirve; el que si es strapping es **IO5** (timing de SDIO slave, viene del kit v1): una
    puerta cerrada al arrancar lo deja en 0, el arranque no se altera, y queda escrita la salida (DOOR1 ->
    IO32, fisico 7, libre); (d) 2 borneras de 3 y no 3 de 2: mismo borde, una pieza menos y **misma huella
    que ya usa la placa**; (e) **J2 es la unica de paso 5,08** (MKDS-3 perfil alto, 2,5 mm2) porque es la
    unica que tiene que aceptar 3-4 cables por tornillo -- declarado en la hoja, en el cajetin y en DISENO 5,
    con la regla de que si @hardware consigue otro paso **se cambia la constante y se regenera**.
  - **Los 3 defectos que solo se vieron MIRANDO el PNG** (el chequeador de solapes dio 0 en los tres): (1) el
    `Value` de J3 ("PUERTAS 1-3") caia **sobre la fila de pines de J4** -- texto contra simbolo, que el
    chequeador no compara; (2) los pull-up en una sola columna hacian que **el riel +3V3 de uno quedara pegado
    debajo del anterior**: parecian dos resistencias en serie con un tap -> se escalonaron en x (64/69) **y el
    rotulo de los escalonados va a la izquierda**, porque a la derecha se les cruzaba el capacitor de la fila;
    (3) los **comentarios del cajetin** se cortaban por derecha (>70 caracteres) -- el chequeador no mira el
    title block. Ademas el area util de la A3 mordio dos veces: el `ref_off=-7` de las borneras dejaba texto
    en x=14,0 mm (el area arranca en 15,0) y dos bloques de notas se pasaban de y=250 mm.
  - **Aviso a @pcb**: el `termovigia_mini_lite.kicad_pcb` y los gerbers/artworks que hay en la carpeta son de
    la **rev A** y ya no corresponden a este `.net` (cambiaron todos los conectores y la numeracion). Rutear
    de cero desde `termovigia_mini_lite.net` rev B.
  - **Proximo paso**: @verificador audita el `.net` rev B (46 redes) y la eleccion de GPIO -> @hardware compra
    (BOM_LITE 4.1: la bornera de 3 de PERFIL ALTO es lo unico no trivial) y mide M1..M5 -> @pcb rutea a
    120 x 80 en **una cara**, con las reglas de DISENO 7, y declara los puentes -> @firmware aplica
    `PINOUT_LITE.md` (MAX_DOOR_SENSORS 5, MAX_PROBES 8, RELAY_ON LOW, sin defrost/buzzer/DHT/SCT).
