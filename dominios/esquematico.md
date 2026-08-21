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
