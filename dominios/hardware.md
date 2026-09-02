# Dominio: HARDWARE (agente @hardware)

Doc de dominio + bitácora. El agente lo lee al arrancar y lo actualiza al cerrar.

## Estado del dominio (nacimiento, 2026-07-07)
- Stock: 5 PCBs FrioSeguro fabricadas (2 SIM800 + 3 WiFi), 20 DS18B20, 10 reed, 5 ESP32, relés + stock enorme GIMAP. Compras: GIMAP banca hardware, Mundo Outdoor banca infra, ~$300k ARS/mes propios.
- galgas-supabase: brownout USB conocido; montaje de campo (enclosures/fijación a eje) pendiente para octubre.
- FrioSeguro: circuito SIM800 sin armar.
- Cosechador: BOM ~$154.500 sin comprar; riesgo stock LTC3588-1 y sensor de llama.
- Convergencia UTN: las PCB que se diseñen sirven para Diseño y Manufactura (cursada) y Tecnología (final por proyecto).

## ⚖️ DOCTRINA: qué micro para qué (complemento de la doctrina LoRa/WiFi de @comms, 2026-07-07)
Regla: **el enlace se elige primero (doctrina @comms); el micro es el más chico que sirva ese enlace y esa tarea.** El stock cubre los 4 escalones:

| Micro (stock) | Cuándo usarlo | Cuándo NO |
|---|---|---|
| **ESP32** (×10) | El nodo habla WiFi/HTTPS/cloud directo (FrioSeguro, galgas Dreyfus). TLS y OTA resueltos. Deep sleep decente (~10µA) con ráfagas | Nodo de años a batería con radio SPI simple: el ESP32 es un camión para eso |
| **Pico 2 W / RP2350** (×5) | **El datalogger**: PIO = muestreo determinista sin jitter, dual-core (core0 log, core1 comms), SD, LoRa por SPI | Ultra-low-power extremo (dormant de RP2350+CYW43 es mediocre) ni TLS pesado |
| **Pro Mini 3.3V/8MHz / ATmega328P pelado** (×3+3) | **Nodos ultra-low-power**: sleep <1µA (pelado, sin regulador ni LED), radio SPI (NRF24/LoRa), harvesting — el cosechador y el harvester-node de RuView. Es la razón por la que están en stock | Todo lo que necesite cómputo, WiFi o >2KB RAM de sobra |
| **STM32F446RE / BluePill** (×1+1) | Control en tiempo real y DSP serio (180MHz, FPU): candidato natural para el **proyecto de labo de Sistemas de Control** (ya hay material de puente H con STM32) e instrumentación fina | Prototipos rápidos de IoT (toolchain más pesada, sin WiFi) |

Corolario: datalogger = Pico (PIO+SD) + LoRa · nodos eternos = ATmega pelado + NRF24/LoRa · todo lo cloud = ESP32 · lazo de control de la uni = STM32. Cada compra futura se justifica contra esta tabla.

## Inventario / BOM (tabla viva)
| Ítem | Cant. | Ubicación | Proyecto | Fecha |
|---|---|---|---|---|
| PCB FrioSeguro (SIM800) | 2 | casa | FrioSeguro | 2026-07-07 |
| PCB FrioSeguro (WiFi) | 3 | casa | FrioSeguro | 2026-07-07 |
| Sondas DS18B20 | 20 | casa | FrioSeguro | 2026-07-07 |
| Reed switches | 10 | casa | FrioSeguro | 2026-07-07 |
| ESP32 | 10 | casa | varios | 2026-07-07 |
| Raspberry Pi Pico | 5 | casa | RuView/datalogger | 2026-07-07 |
| Arduino Pro Mini | 3 | casa | cosechador | 2026-07-07 |
| ATmega328P | 3 | casa | harvester node | 2026-07-07 |
| STM32F446RE | 1 | casa | libre (labo control?) | 2026-07-07 |
| STM32 BluePill | 1 | casa | libre | 2026-07-07 |
| Módulos 2 relés | ~10 | casa | upsell FrioSeguro | 2026-07-07 |
| Analizador lógico | 1 | casa | debug | 2026-07-07 |
| Supercapacitor 1F 5.5V (moneda) | 1+ | casa | ~~pulso TX LoRa emisor Dreyfus~~ **NO SIRVE como CSC** (ESR ~30 Ω, ver P8 / Rev C 2026-09-02) → backup RTC | 2026-07-10 · corregido 2026-09-02 |
| Cajas IP65 + prensacables PG7/PG9 + tapones | 3 cajas | casa | Termovigía | 2026-07-08 (compra) — **confirmar contando** |
| ESP32 en campo (reefer Cerro Moro) | 1 | Santa Cruz | Termovigía SCZ | 2026-08-21 — descontar del stock de ESP32 |
| PCB FrioSeguro v1 | 5 | casa | **no aptas para Base v2** (SIM800/ACS712) → banco/UTN | 2026-09-01 |
| DS18B20 / reed / módulos relé / ESP32 | 15-20 / 10-20 / 5-10 mód. / 4-9 | casa | Termovigía + galgas | 2026-09-01 — **discrepancia Matías vs bitácora: CONTAR** (ver BOM_5_EQUIPOS §1) |

## Compras en curso
- 2026-07-08 — Matías compra 3 cajas estancas IP65 + prensacables (PG7 sonda / PG9 alimentación) + tapones ciegos para huecos sin usar. Es el enclosure v1 de FrioSeguro (decisión: estanca de ferretería, NO 3D custom — ver bitácora 2026-07-07). Destraba las primeras 3 instalaciones comerciales.

## Bitácora
- 2026-07-07 — Agente creado por Claude Fable. Próximo paso sugerido: checklist de montaje de campo para octubre (enclosures, fijación, prensacables) + decidir compra del cosechador.
- 2026-07-07 — DECISIÓN (Ponytail) enclosure FrioSeguro: piloto casero = placa pelada; primeros comercios = **caja estanca IP65 de ferretería** con prensacables (mejor que PLA en ambiente húmedo de cámara, 20 min vs días); carcaza 3D custom = solo v2 con 5+ abonos (y candidata a pieza de Diseño y Manufactura / convergencia UTN). Comprar 2-3 cajas estancas + prensacables esta semana.

- 2026-07-08 [BRIEFING GIMAP] — leer ../BRIEFING_EQUIPO_GIMAP.md y los 4 docs (PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO). Para vos: COMPRAS 2026-07-08: 2 cajas estancas grandes + 10 precintos + 2 tomas (relé si hiciera falta; relé = solo aprendizaje, sin caso de negocio en FrioSeguro). BOM emisor 1 año: ATmega/STM32L+HX711+RA-02+LiSOCl2+supercap+LDO+MOSFET gateo, NO boost.

## IDEA a desarrollar — 2 tomas embebidas en las estancas de FrioSeguro (Matías 2026-07-08)
Matías tiene 2 tomas (enchufes) para embeber en las cajas estancas de FrioSeguro. Posible OFERTA (a definir con @comercial):
- **Toma passthrough con monitoreo de corriente**: el cliente enchufa la heladera/cámara a la toma del equipo → medimos la CORRIENTE del compresor (FrioSeguro YA tiene ACS712 en su diseño). Valor de venta nuevo: **"detectamos si el compresor dejó de andar"** — no solo la temperatura, sino la CAUSA (compresor parado, corte de luz visto desde el propio equipo). Diferencia "se está calentando" de "se rompió el motor".
- Alternativa (menos prioridad): la toma como salida conmutada por relé — pero relé = solo aprendizaje, sin caso claro (ver bitácora previa). El monitoreo de corriente SÍ suma sin el riesgo del relé.
- Estado: idea, baja prioridad vs. cerrar la venta base. @hardware evalúa factibilidad (ACS712 embebido + toma), @comercial si suma al pitch.

## Avance datalogger 2026-07-10
- Matías va a conseguir/arrancar con el **HX711** (ADC 24-bit de puente) para probar el salto de resolución vs el ADC actual (ver DISEÑO_DREYFUS §4). Primer paso concreto de la cadena analógica "peluda". @esquematico + @muestreador en cuanto tenga el módulo + una galga.

## ⚠️ LECCIÓN 2026-07-10 (error señalado por Matías)
La lista de compras v1 incluyó ítems YA en stock (LoRa, galgas, supercap) y un LDO que contradecía la decisión "directo sin LDO". **REGLA DURA para @hardware y todo agente que arme listas de compra: cruzar SIEMPRE contra (1) el inventario de este archivo y (2) las decisiones de diseño vigentes (DISEÑO_DREYFUS.md) antes de entregar.** Un BOM que ignora el stock propio y las decisiones tomadas es peor que no tener BOM.

## ⛔ DECISIÓN 2026-07-11 (Matías): SIM800 DESCARTADO de FrioSeguro
FrioSeguro va SOLO WiFi. Motivos: (1) técnico — el SIM800 no engancha bien la red (conexión inestable = equipo que a veces no reporta = cliente pierde confianza); (2) negocio — el SIM obliga a administrar chips/saldo/servicio como costo recurrente y responsabilidad mensual propia. Con WiFi la conexión la pone el cliente; el margen del abono queda limpio, sin la telefónica de intermediario. Las 2 PCBs con SIM800 quedan como stock a poblar en variante WiFi (o SIM800 sin soldar). La placa que Matías está terminando ahora = FrioSeguro-WiFi. NO poblar el SIM800.

## 2026-07-31 — LASER-PCB: presupuesto completo de la fábrica de PCBs
Entregado `C:\Proyectos\laser-pcb\docs\PRESUPUESTO_FABRICA_PCB.md` (10 secciones + anexo de metodología). Precios verificados EN VIVO en MercadoLibre AR el 2026-07-31.

**Hallazgos duros:**
1. ⚠ **El link del módulo láser del `esquematico/BOM.md` (MLA-785209325, $12.730) está MUERTO — HTTP 404.** El piso real de mercado hoy es ~$90.000 (7×). Todo cálculo con los $12.730 está mal. Corregir el BOM.
2. **Módulo láser — 3 candidatos vivos y verificados:** L1 [MLA2025931454] $151.452, único que declara textualmente *"Interfaz: 3 pines, 12V, GND, PWM"*, 450nm 12V 3A, ~5W ópticos · L2 [MLA2064142764] $90.582, 25 u. en stock, 450nm 12V foco ajustable, ~1,5-2,5W ópticos, **pero NO declara el conector TTL → hay guion de pregunta al vendedor en el doc** · L3 Lunyee [MLA2079239370] $178.051, 10W ópticos REALES, XH2.54-3P, PWM 0-5V. NEJE A40630 descartado ($897k).
3. **Anteojos 450nm — SÍ hay opciones serias en ML AR** (contra la hipótesis pesimista): FreeMascot OD6+ **190-490nm**, EN207, VLT 55%, "compatible 405/445/450nm" — $150.136 (MLA2074881222, 3 u. en stock). Alternativas: MCWlaser OD5+ 190-540nm $216.399 (35 días de plazo), FreeMascot OD8+ 190-450nm $180.747 (450 en el BORDE de banda → no primera opción). **Descartados por fraude verificado**: MLA2060292343 (título "190-540nm", descripción real "480-580nm" → NO cubre 450) y MLA2034992781 (no declara OD). Decisión: 2 pares del FreeMascot OD6+.
4. **Presupuesto de corriente 12 V calculado**: peor caso ≈ 9,4 A (láser 3A + spindle 775 calado 5-6A + resto) → **fuente 12 V 10 A mínimo**. Riesgo señalado: brownout que resetea la placa **dejando el láser encendido y quieto** (mismo patrón que el brownout USB de galgas-supabase).
5. **Escenarios**: MÍNIMO $484.229 (**≈$301.000 si GIMAP presta minitorno, fuente, cables, placas, percloruro, matafuego**) · RECOMENDADO $962.950 · COMPLETO $2.027.549.
6. **Bloqueo activo**: sin el modelo de impresora / tensión de su fuente (12 vs 24 V) y sin las medidas del carro con calibre, NO se compra fuente, módulo láser, relé (SRD-12 vs SRD-24) ni fichas. Una foto de la placa madre + etiqueta de la fuente + 4 medidas destraba $300k-$1M de compras.

**Pendiente @hardware:** (a) corregir el link muerto en `esquematico/BOM.md`, (b) mandar el guion de preguntas al vendedor del L2, (c) pedir a GIMAP la lista marcada 🏭 antes de comprar nada.

## 2026-07-13 — Torno Villatoro (variador CC): compra ByP hecha
Matías compró en ByP los módulos de la **Opción D** (presupuesto 0004-00046240, **$38.302 c/IVA**): dimmer SCR 4000W + puente 15A (armadura) + puente 8A (campo) + varistor + portafusible + disipador + 1 TYN612 de repuesto p/ la ME06 original. Registro completo con flags técnicos en `Downloads\Villatoro-torno CC\Villatoro-torno CC\COMPRA_BYP_2026-07-13.md`. **Pendiente antes de instalar:** fusible cerámico o térmica C10 (el de vidrio rápido es solo p/ banco — capacidad de ruptura y pico de arranque), gabinete IP54, bornera ignífuga 12P (ByP tenía 2 u.), cable 2,5 mm²+prensacables. Banco: trafo de aislación SÍ o SÍ (control a potencial de red).

## 2026-09-01 — TERMOVIGÍA Base v2: inventario reconciliado + BOM 5 equipos + compras
Entregado `C:\Proyectos\frioseguro\hardware\v2\BOM_5_EQUIPOS.md` (precios ML AR verificados en vivo 2026-09-01, ID por renglón; método: HTML público con UA de buscador — la API sigue 403 y el scraping común bloqueado).

**Inventario — discrepancias a CONTAR (Gonza/Sergio, 30 min):** ESP32 (Matías 5 / bitácora 10; 1 está en Cerro Moro) — **crítico porque galgas-Dreyfus necesita 3 en octubre**: 5 Termovigía + 3 galgas + 1 SCZ = 9 · DS18B20 (15 vs 20) · reed (20 vs 10) · módulos relé ("10 relés de 2" = ¿10 módulos o 5?) · 3 cajas IP65 (medida interior) y prensacables sobrantes. Las 5 PCB v1 (ALDI DISEÑO) **no sirven** para la Base v2 (footprint SIM800/ACS712): quedan para banco/UTN. En el repo frioseguro no hay ninguna compra registrada con cantidades.

**Escenarios:** MÍN 5 Estándar **$386.941** · REC 5 Est. + 2 Premium **$864.962** · COMPLETO +repuestos **$1.157.242** (estimados no verificables en ML: ~$107–129k). Estándar ≈ $65k/equipo; kit Premium ≈ $234.500, 63 % es el A7670SA.

**Hallazgos duros:** (1) A7670SA existe en AR: MLA1487294925 $146.673 (breakout + antena 4G + GPS, bandas B2/B4/B7/B28 ok); alternativa A7670G MLA2141725040 $88.999 sin confirmar antena/medidas (guion de preguntas en el doc); importado por courier ≈ $48k con el régimen nuevo (Dec. 604/2026: USD 400 solo IVA). (2) No hay "cargador flotante" chico en ML (todo cargadores de auto $29–386k) → el flotador es un LM2596 CC/CV a 13,8 V/0,7 A ($4.999) y Premium entra con fuente 19 V de notebook ($22.581), no 12 V. (3) Batería Motoma $21.600 dice "no apta UPS" → Kaise KB1270 $24.999. (4) La placa lleva 3 posiciones LM2596 (5 V / 4 V / flote) y jack DC + bornera en paralelo: una sola PCB para Estándar y Premium. (5) Transferencia: en placa solo contactos secos + entrada "grupo en marcha" por 2.ª fuente 12 V + PC817; contactores/tablero se cotizan aparte (referencia interna contactor bipolar 25 A $29–34k).

**PCB:** JLCPCB ×10 por DHL con CUIT ≈ $70–90k y 10–15 días (recomendada; 100×100 cuesta lo mismo si el breakout no entra en 100×80). 2gtech (MLA929971373) = cotizar como plan B. laser-pcb **descartado** para esto (bloqueado, sin láser comprado, y la v2 es doble faz con vías).

**Pendiente @hardware:** preguntar al vendedor del A7670SA medidas y conector de antena; preguntar a Gonza/Sergio qué tienen para fabricar; `PINOUT.md` de la Base v2 con @firmware cuando @pcb tenga el esquemático; medir ripple del 4 V bajo TX antes de dar por bueno el primer equipo.

## 2026-09-01 (noche) — TERMOVIGÍA Base v2: rev B del BOM (H1/H2/H3/H7/H17 del verificador + PCB 120×100)
Entregado: sección "rev B 2026-09-01" (B.1–B.9) al final de `C:\Proyectos\frioseguro\hardware\v2\BOM_5_EQUIPOS.md`. Sin commit.

**Hallazgos duros:**
1. **H1 CERRADO sin el vendedor.** El breakout de MLA1487294925 es el **BK-A7670 v1 de AND Technologies** (fotos de la publicación = manual del fabricante v1.0, leído completo): **VCC 5–10 V con regulador a bordo (TP 4,0 V), UART 3,3 V TTL, PWRKEY = pin K con R104 a GND (arranque automático), sin RESET ni STATUS en el header (7 pines G-R-T-K-V-G-S), 3 × IPEX (LTE/GPS/BT), 37 × 37 mm, un solo agujero de montaje, antena LTE FPC 2 dBi + GPS cerámica incluidas.** Para rev B: `+VMODEM` = **5,0 V** (no 4,0), JP501 en 1-2, U501 DNP, Q502/R502 fuera, huella 1×7, opcional `MODEM_PWR_EN` (P-MOSFET high-side) para reiniciar el módem por riel. Mensaje al vendedor redactado (confirma revisión, variante LASE/FASE, R104, stock) — Matías lo pega.
2. **PCB 120×100 cotizada EN VIVO en JLCPCB** (headless, capturas): 10 u. 2 capas = **USD 15,50** (100×100 = USD 5,00) + DHL DDP USD 28,97. Diferencia real 120×100 vs 100×100: **USD 10,50 = $25.271 con IVA**. Renglón PCB pasa de `EST.` 85.000 a **$122.026** (fab + DHL verificados; gestión 15k sigue `EST.`). 120×100 aprobado por costo; falta que entre en la caja (medir el martes).
3. **Sirena 12/24 V**: candidata **MLA1144075239** (15 W, DC 12/24 V, 110 dB, tamper, strobo). Va desde **VSYS** con F103 propio, conmutada por K1. Precio `PENDIENTE` (ver 5); referencia de clase $21.967.
4. **LVD + inversa** (kit Premium): `J102 → F102 → Q_REV (IRF9540, gate a GND 100k) → +BATT_OK → Q_LVD (IRF9540 + TL431 36k/10k, R_g 10k, histéresis 1M) → D106 → VSYS`; cargador y VBAT_SENSE cuelgan de +BATT_OK (batería invertida = 0 V en el ADC → alarma). Consumo del LVD ≈ 1,4 mA (@energia valida). IDs: IRF9540 MLA611352928 / MLA1444696259 / pack MLA3784963550; TL431 MLA653337466.
5. **PTC RXEF185 no existe en ML AR** → F101/F102/F103 = **portafusible 5×20** (2 A T Estándar / 3 A T Premium; 3 A F batería; 1–2 A sirena): una sola huella `Fuse_5x20`, 4 packs de portafusibles. Huella `MF-RG1100` se elimina.
6. OLED: sí, por cable a la tapa, J303 = GND-VCC-SCL-SDA, Nubbeo $7.699 (REC/COMPLETO, no MÍN).
7. **Totales rev B: MÍN $502.947 · REC $1.032.943 · COMPLETO $1.346.720** (+ LVD/inversa y pigtail `PENDIENTE`). El salto es la sirena (+$69k en MÍN), no la PCB (+$37k).

**Límite de la sesión:** MercadoLibre bloqueó la IP a las 22:20 (`account-verification` en todo, API 403, también headless y proxies). Todo lo nuevo tiene ID verificado por buscador y precio `PENDIENTE`; nada inventado. Scripts listos en el scratchpad de la sesión 72c41d2f (`ml.py`, `mlitem.py`, `pw_ml.py`, `pw_jlc7.py`).

**Para Gonza el martes 2 (B.6):** medir con calibre DevKit (separación de filas, silk), LM2596 ×2 tipos (4 agujeros), módulo relé (header + agujeros), level-shifter (filas), OLED, interior de la caja IP65 y batería vs Genrod; el breakout A7670 cuando llegue. Resultado a `DISENO.md §9`.

**Pendiente @hardware:** llenar `PENDIENTE` en cuanto ML responda; pegar el mensaje al vendedor; `PINOUT.md` con @firmware tras la rev B verificada; medir ripple de `+VMODEM` (5 V) bajo registro/TX del A7670 en el primer Premium.

## 2026-09-02 — GALGAS/Dreyfus: P8 (supercapacitor) y P9 (D4) CERRADOS — se destraba el layout del nodo
Entregado: sección **"9. Rev C — 2026-09-02"** (C14–C20) al final de
`C:\Proyectos\galgas\hardware\NOTAS_CALCULO.md`. Sin commit. No se tocó nada del §0 al §8.

**Hallazgo que cambia el problema (C14):** el enunciado de P8 pedía "1 F con ESR ≤ 1 Ω" y **se
olvidaba de la tensión**. Con la topología en serie de la rev B, CSC cuelga de `V_SC = VBAT − 1,6 mV`,
o sea que está **permanentemente a 3,67 V**, no a 3,0 V. → **ninguna celda suelta de 2,5/2,7/3,0 V
es candidata**; toda solución es de **dos celdas en serie** (o un pack de fábrica de 5 V), y eso
arrastra **resistencias de balanceo** y **dos huellas** que no estaban en el esquemático.

**P8 — elegido: 2× Eaton HV0810-2R7105-R en serie (CSC1+CSC2) + RB1/RB2 150 kΩ 1 % 0805.**
1 F 2,7 V c/u → 0,5 F 5,4 V; ESR 0,2 Ω/celda; fuga 10 µA máx.; ⌀8,5 × 13,5 mm, paso 3,5 mm.
Caída en el pulso de TX (120 mA, 150 ms) = **132 mV peor caso contra 420 mV de margen (3,2×)**, y
aguanta incluso si la ESR real fuera 4× la de catálogo. Derating 68 % de la nominal.
**Huella: `Capacitor_THT:CP_Radial_D10.0mm_P3.50mm` ×2** (D10, no D8: el cuerpo es de 8,5 mm) +
`Resistor_SMD:R_0805_2012Metric` ×2. Reemplaza al `CP_Radial_D13.0mm_P5.00mm` tentativo.
**Costo energético: +22,2 µA de reposo (10 de fuga + 12,2 de balanceo) = 13,7 % del budget** →
I_media 0,184 mA → **1,30 años** (antes 1,48). **Lo tiene que firmar @energia.** Hay compuerta de
medición a 72 h que, si la fuga real es < 1 µA, permite RB = 1 MΩ y devuelve la autonomía a 1,38 años.
Alternativa de producto (una sola pieza, sin balanceo, 1,38 años): **Eaton PB-5R0V105-R** 1 F 5,0 V,
ESR 0,5 Ω, fuga 12 µA — **no elegida hoy porque no tiene huella y no pude abrir el plano mecánico**.

**P9 — elegido: D4 = onsemi ESD5Z5.0T1G, SOD-523.** Unidireccional, **VRWM 5,0 V**,
**`IR` = 0,05 µA máx. especificada a 5,0 V** (el criterio pedía ≤ 1 µA @ 3,7 V: se cumple con una
condición más dura y **con número de hoja de datos**), VBR 6,2 V, VC 11,6 V, 80 pF.
Cuesta **0,44 mAh/año = 0,02 % de la pila**. **Huella: `Diode_SMD:D_SOD-523`** — reemplaza al
`SOT-23` tentativo, que además estaba **mal** (símbolo de 2 patas sobre huella de 3 pads).
LCSC **C82044**, USD 0,0164, 250k en stock, y está en la librería de JLCPCB → si la PCB va con
montaje, viene soldado. Descartado con motivo el candidato "obvio" **PESD5V0L1BA (SOD-323): es
BIDIRECCIONAL** — la "L" es de *low capacitance*, no de unidireccional. Trampa anotada.

**Otros hallazgos:**
- **El supercap 1 F 5,5 V del inventario (renglón 2026-07-10) NO sirve como CSC** y hay que corregir
  ese renglón: es de tipo moneda, clase **Eaton KW-5R5C105H-R, ESR 30 Ω @ 1 kHz** → ΔV 1,44 V, apagón.
  Queda liberado para backup de RTC. **Sigue sin comprarse nada para P8.**
- **CONFIRMADO el faltante de la guía de perfboard §8.2**: ni las resistencias de precisión (R1 348 Ω,
  R2/R3, RCAL 174k65, RS1/RS2, RGD), ni los C0G (CD 100 nF, CC1/CC2 10 nF), ni la bornera de paso
  **5,08 mm**, ni el perfboard de islas, ni el **cable de galga apantallado** figuran comprados ni en
  stock **en ningún documento**. Lista completa en C19. **Sin eso Matías no puede soldar el banco.**
- **Inconsistencia de bornera**: el `.kicad_pcb` usa huella MX126 de **paso 5,00** y el perfboard exige
  **5,08** → dos borneras distintas para el mismo proyecto. Recomendación DFM: estandarizar en 5,08. Dueño @pcb.
- **C8 cambia**: con 0,5 F, τ = 10 s y 3τ = 30 s (antes 20/60 s). El "minuto de despasivación" del
  checklist de instalación hay que reescribirlo (el pico de 184 mA no cambia). Para @energia con P5.
- **P2 sigue abierto** (D1/D2/D3 de entrada: hace falta un **bidireccional** con IR ≤ 10 nA @ 1,5 V;
  el ESD5Z5.0T1G no sirve ahí).

**Límite de la sesión (honestidad de datos):** no hubo red saliente (sólo buscador) y MercadoLibre
sigue bloqueando la IP desde el 2026-09-01 → **todos los precios quedaron `PENDIENTE`**; los datos
eléctricos salen de atributos de distribuidor (Farnell/DigiKey/RS/LCSC) y están marcados como tales,
sin ningún número inventado. Falta abrir las hojas de Eaton HV y de onsemi ESD5Z para confirmar la
frecuencia de la ESR y el plano mecánico.

**Pendiente @hardware:** (a) preguntar a GIMAP si tiene supercaps de baja ESR o diodos ESD antes de
importar; (b) llenar los `PENDIENTE` de precio cuando haya red; (c) pasar los 8 cambios de C18 a
@esquematico/@pcb y regenerar; (d) montar la compuerta de medición de fuga a 72 h; (e) comprar la
lista del banco (C19) — es lo único que separa a Matías de soldar la Placa A.

## 2026-09-02 (b) — GALGAS: G17 (LDO) y G13 (dropout + pila a fin de vida) — respuesta al RECHAZO de P6
Entregado: **"9-bis. Rev C (adenda)"** (C21–C23d) en `C:\Proyectos\galgas\hardware\NOTAS_CALCULO.md`,
a continuación de C14–C20. Sin commit. Origen: `hardware\VERIFICACION_P6_2026-09-02.md`.

**G17 — CONFIRMADO, pero la plata no se perdió.** `HT71xx-1` (Holtek) = **30 mA máx**, Iq 2,5 µA típ.
La TX del RA-02 pide **87 mA (+17 dBm) / 120 mA (+20 dBm)** — verificado hoy en la **tabla 6 de
`SX1276-77-78-79_Semtech.pdf`. Con el HT7130A el nodo no transmite.** PERO: la **Placa A** (banco,
sin radio) consume 10,4 mA → **los 2 HT7130A comprados son el LDO de la Placa A**, no descarte.
⚠ La guía de perfboard §8.1 dice lo contrario ("no hace falta en Placa A, es para la B") → **corregir**.
- **U4 se queda MCP1700-3002**: SOT-23-3 en la PCB (**@pcb no cambia nada, la huella `SOT-23` sigue**)
  y **TO-92-3 para el perfboard**. Mismo die, dos encapsulados.
- **COMPRAR: `MCP1700-3002E/TO` TO-92 ×5.** Candidato AR **`MLA-703690036`** (ADICHIP, "MCP1700
  regulador 3V LDO 250mA x5"). **Precio `PENDIENTE`** — el buscador devolvió $328,60, que es un
  cacheado viejo, y ML sigue bloqueando la IP desde el 2026-09-01; no se usa ese número.
  ⚠ **Casi todas las publicaciones de MCP1700 en AR son la 3302 = 3,3 V** (MLA-698527309,
  MLA-1107192763): hay que pedir la **3002 = 3,0 V** o rompe C6.
- ⚠⚠ **TRAMPA DE PINOUT (pág. 1 del datasheet, leída hoy):** `SOT-23: 1=GND 2=VOUT 3=VIN` pero
  `TO-92: 1=GND 2=VIN 3=VOUT` — **pines 2 y 3 invertidos**. El símbolo usa U4.3=VI (SOT-23). Soldar
  el TO-92 "según el esquemático" lo destruye. Y el pinout del HT7130A tampoco se puede asumir igual.
- **TPS7A02 descartado** (Iq 25 nA tentador, pero 1,35 Ω de pass FET = igual que el MCP1700, SOT-23-**5**
  cambia la huella con @pcb ruteando, y cero stock AR). Anti-sobre-ingeniería.

**G13 — CONFIRMADO y ampliado.** `MCP1700_Microchip.pdf` pág. 3: **178 mV es TÍPICO, 350 mV es el
MÁXIMO** @250 mA. Y **segundo error que nadie vio**: C6/C7 nunca aplicaron la Nota 1
(`VIN ≥ VR + 3,0 % + VDROPOUT`). Los dos errores tiraban para lados opuestos y se tapaban.
RDS(on) del pass PMOS peor caso = 350 mV/250 mA = **1,40 Ω** (escalado justificado con el texto de
TI en `TPS7A02_TI.pdf` §7.3.5; sigue siendo extrapolación → medición de banco asignada).
→ `VIN` mínimo real: **3,105 V midiendo · 3,212 V a +17 dBm · 3,258 V a +20 dBm** (C6 decía 3,18 V).

**Pila a fin de vida (OCV 3,20 V, R_pila 40 Ω, con el CSC de la rev C):**
medir 3 s hunde 67 mV + TX a +20 dBm otros 88 mV → `V_SC` 3,045 V → **el LDO sale de regulación** →
`VOUT` = 2,877 V. **Está por debajo de los 2,9 V del `VBOT` máximo del fusible `BODLEVEL=2,7 V`
(ATmega tabla 32-8) → reset justo en la última TX.** A +17 dBm quedan 2,948 V: pasa por 48 mV, o sea
por suerte. **El brownout es de FUSIBLES, no de hardware.**

**Hallazgo lindo:** con `R_pila = 100 Ω` en vez de 40 la caída del pulso **no cambia** (88 mV), porque
`Req = ESR ‖ (R_pila+RSC)` la domina la ESR de 0,4 Ω. **El supercap borra la resistencia interna de
la pila de la cuenta; lo que queda mandando es la OCV.** Confirma la topología de la rev B y P8.

**Las 3 reglas (ningún componente nuevo) — VEREDICTO: el riel aguanta la última TX SÓLO con R1+R3:**
- **R1** fusible **`BODLEVEL=110` (1,8 V)**, no 101 (2,7 V) → dueño **@firmware**.
- **R2** escalón de TX por VBAT con el divisor de C9 que ya existe (≥3,35 V → +20 dBm · <3,35 → +17 ·
  <3,05 → sólo trama "pila agotada") → **@firmware** + umbrales de **@energia**.
- **R3** transmitir **30 s después** de medir (el nodo ya duerme 293 s): recupera 47 mV, **gratis**.
  Con R1+R3 transmite hasta OCV ≈ 3,02 V a +20 dBm y 2,95 V a +17 dBm.

**Pendiente @hardware:** (a) **comprar el MCP1700-3002E/TO ×5** — es lo que bloquea la Placa B;
(b) medir el dropout real a 87/120 mA (10 min, INA219 + fuente) para cerrar la extrapolación de 1,40 Ω;
(c) medir el consumo del RA-02 en PA_BOOST por debajo de +17 dBm (Semtech no lo publica y R2 depende
de eso) — con @comms; (d) corregir la guía de perfboard §8.1; (e) pasar R1/R2/R3 a @firmware y las
correcciones de C6/C7 a @esquematico.
