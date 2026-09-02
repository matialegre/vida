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
