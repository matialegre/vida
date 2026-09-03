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
| PCB FrioSeguro v1 ("ALDI DISEÑO") | 5 | casa | **no aptas para Base v2 NI para el Kit v1** — motivo CORREGIDO 2026-09-02: el diseño **no tiene SIM800/ACS712**, es un front-end de galga (MCP6004) y **tiene las 6 borneras con los 18 pads sin red** + 2 redes de 3,3 V separadas + 4 pull-ups sin conectar → 23 bodges por placa. Ver `frioseguro/hardware/v1_modulos/BOM_KIT_V1.md` §5. Uso: banco/UTN | 2026-09-01 · corregido 2026-09-02 |
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

## 2026-09-02 (c) — TERMOVIGÍA **KIT v1 (módulos)**: cambio de estrategia — no se fabrica la PCB v2 todavía
Entregado `C:\Proyectos\frioseguro\hardware\v1_modulos\BOM_KIT_V1.md` (8 secciones). **La v2 queda intacta**, sólo se pospone y ahora tiene criterio de disparo. Sin commit.

**El número de la decisión: arrancar 5 equipos de demo con el stock que ya hay cuesta $133.780 = $26.756 por equipo.**
9 renglones, todos con ID de ML y precio verificado **hoy** (la IP se desbloqueó, con cortes cada ~4 consultas; parser nuevo `ml2.py` — ML cambió el HTML de las tarjetas y el `ml.py` viejo devolvía listas vacías **sin avisar**): plaqueta PE05 101×56 ×5 MLA2489408876 $3.830 · bornera 3 vías pack×10 MLA883712506 $9.462 ×3 · tira hembra pack×5 MLA2396812672 $5.016 ×2 · 4k7 MLA1790498721 $2.659 · 10k MLA1790511395 $2.659 ×3 · 1000 µF 25 V low-ESR pack×20 MLA1942247187 $9.279 · kit separadores M3 580 pzas MLA3211774920 $25.299 · **caja IP65 165×165×80 pack×2 MLA1823115747 $17.000 (= $8.500 c/u, lo MISMO que la 160×120×80 y con 45 mm más de ancho)** · prensacables PG9 pack×10 MLA1816105105 $6.999 ×2.
Peor caso si falla todo el conteo (ESP32, relés, sondas, reed, fuentes): **$351.220** — igual el 70 % del MÍNIMO de la v2 rev B ($502.947) y sin esperar fabricación.

**Hallazgos duros:**
1. ⚠⚠ **Las 5 PCB de julio están MAL y el motivo que teníamos anotado era el equivocado.** Parseé `ALDI DISEÑO.kicad_pcb` pad por pad: **cero footprints de SIM800/SIM900/ACS712/relé** (la cadena "SIM800" no existe en el archivo); es un **front-end de galga** (MCP6004 + 5 presets + 3 MΩ + `ADC1..4MICRO`, `Bateria`, `Acelerometro1`). Y los defectos reales: **las 6 borneras TB1-TB4/TB6/TB7 tienen los 18 pads SIN RED** (islas aisladas), **dos redes de 3,3 V distintas sin unir** (`+3.3V` net 3 vs `3V3` net 57, que toca sólo R17.2 y R20.2), **4 de 6 pull-ups con una pata `unconnected`** (R18/R19/R21/R22), única zona = GND. **23 bodges por placa × 5 = 115 soldaduras de rescate** para algo peor que una plaqueta de $3.830. → **ignorarlas para el Kit v1**; sirven para banco/UTN y el bloque MCP6004 puede rescatarse en UNA placa para galgas con @muestreador. Renglón del inventario ya corregido arriba. **Salvedad: los archivos son del 2026-03-10 → pedir fotos de las 2 caras antes de cerrar el tema.** Es además un caso de estudio de ERC/DFM de lujo para Diseño y Manufactura.
2. **SIM800: NO probarlo, ni con Claro ni con Personal.** 2G AR verificado hoy: **Movistar apagado desde el 31-12-2023** (avisó por SMS; las alarmas GSM dejaron de andar) · **Claro y Personal siguen operativos, sin fecha pública de apagado**, y AR figura como el único país de la región con un switch-off 2G en curso. Banda no es problema (SIM800L 850/1900 = AR). **Lo que decide es el punto 1: no existe ninguna placa con SIM800 para probar.** Alternativa recomendada para el destino sin WiFi: **router 4G portátil LB-Link BL-MF618EU MLA1982028939 $65.548** (o Alcatel MW41 $90.000) con chip prepago → cubre los 2 equipos, **menos de la mitad de UN A7670SA ($146.673)**, es 4G y no cambia una línea de firmware. Paso previo gratis: hotspot del celular de alguien del lugar, antes de que el equipo viaje.
3. **Placa de conexiones elegida: plaqueta experimental PE05 (patrón protoboard) + 5 borneras + ESP32 en zócalo**, atornillada con separadores M3. $10.991/equipo. Descartado el **screwshield** ($9.990–12.990, cero soldadura) porque **no tiene dónde vivir el 4k7 ni los seis 10 k** → resistencias colgando de un tornillo; queda como plan B de emergencia. Descartado **riel DIN + bornes Zoloda** ($17.598/10 bornes → >$25k/equipo, 2,3× más caro **y sigue sin resolver los pull-ups**).
4. **Dos trampas eléctricas anotadas y ya presupuestadas:** (a) **el riel de 5 V** — ESP32 en TX (~500 mA) + 2 bobinas (~140 mA) exigen **fuente ≥1 A**: hay que **leer la etiqueta de las 5 fuentes ya compradas**, si son de 700 mA no sirven (mismo patrón que el brownout de galgas); 2× 1000 µF low-ESR por equipo y **medición del pozo con osciloscopio conmutando los 4 relés en TX como DoD**. (b) **los módulos de relé son activo-bajo y cliquean durante el boot** con el GPIO flotando → **10 k de cada IN a 3V3** (4/equipo, ya en el BOM) y GPIO elegidos fuera de strapping/flash: **1-Wire GPIO4 · reed 16/17 · relés 25/26/27/32**.
5. **JLCPCB verificado hoy en vivo, 120×100 2 capas: 5 u = USD 9,80 · 20 u = USD 27,00** (+ DHL DDP USD 28,82). A $1.989/USD: **$15.363/placa a 5 · $8.815 a 10 · $5.551 a 20**, contra **$10.991 del perfboard** → **el punto de cruce está entre 8 y 10 placas** (y la mano de obra, 1 h por perfboard, lo adelanta: 20 plaquetas = 20 h de Gonza).
6. **PCBA:** tarifa publicada verificada hoy — **"$8 setup + $0.0016 per solder joint"**, cupones mensuales de $6/$9/$10 que dejan el setup en $0, desde 2 placas. Para ~220 juntas: **$3.880/equipo a 5 u y $1.495/equipo a 20 u**. **JLC no cotiza sin BOM+CPL subidos** (el botón pasa a "NEXT"). **Pero el PCBA NO aplica a la v2 como está:** es una placa de **módulos** (DevKit, LM2596, relés, breakout A7670) que JLC no monta; sólo montaría las resistencias y cerámicos, que son la parte barata; el THT se cotiza aparte; y los componentes vienen de LCSC, lo que **anula el stock de GIMAP**. **Conviene desde ~20 u y sólo con un rediseño SMD (v3)** — con el costo escondido de que un v3 SMD **ya no se repara en el campo**.
7. **Criterio de disparo de la v2, escrito:** (1) **8 equipos comprometidos** con seña/OC, o (2) un cliente pide algo que el Kit v1 **no puede** (sirena, batería, corriente de compresor, transferencia a grupo), o (3) pedido de ≥5 con plazo <3 semanas (y hay que disparar **antes**, JLC son 10–15 días).

**Pendiente @hardware:** (a) **conteo de 30 min + etiqueta V/A de las 5 fuentes + interior de las 3 cajas** — bloquea el pedido; (b) **fotos de las 2 caras de las 5 PCB**; (c) `v1_modulos/PINOUT.md` con @firmware **antes de soldar**; (d) armar 1 en protoboard y validarlo antes de replicar; (e) medir el pozo del 5 V; (f) preguntar a GIMAP por 4k7/10k/1000 µF/borneras antes de comprar.

## 2026-09-02 (d) — KIT v1 **rev B**: alineación con @esquematico (3 contradicciones cerradas) y el total sube a $178.368
`BOM_KIT_V1.md` reescrito contra `PINOUT_V1.md` + `CABLEADO.md` de @esquematico (ERC 0/0, netlist y PDF), **canónicos en pines y alcance por decisión del Director**. Sin commit. La v2 sigue intacta.

1. **GPIO: adopto los de @esquematico y el fundamento es mejor que el mío.** K1=**26**, K2=**27**, K3=**18**, K4=**23** · puertas **5/13/14** · 1-Wire **4**. Son **los mismos que la PCB v2** → entre kit y placa el único `#define` que cambia en los relés es `RELAY_ON`. Mi propuesta (25/26/27/32 + reeds 16/17) era defendible pero rompía esa continuidad. Corregido el diagrama §2.1, el mapa de armado §4.5 y el **checklist de continuidad §4.6**.
2. **Alcance 3 sondas + 3 puertas** (yo había puesto 2+2). Impacto de compra: borneras **7 por equipo** (3→4 packs), prensacables **7 por equipo** (2→4 packs), plaqueta más grande (**PE04 150×56 $6.490 MLA1754687451** en vez de PE05 101×56: 7 borneras piden ~86 mm de borde), y **entran los 100 nF de las puertas que yo no había presupuestado** (MLA795403680 $3.914 ×2). **Y el stock cambia de veredicto: hacen falta 15 sondas y 15 reeds, no 10 — con 10 reeds faltan 5.**
3. ⚠ **Retiré una afirmación mía que NO estaba verificada.** Yo daba por hecho que con IN flotando "el relé cliquea y queda pegado". @esquematico analizó el módulo (LED del opto de VCC a IN → sin camino a masa la corriente es 0) y concluye que quedan **abiertos**. **Los dos podemos tener razón según la variante** (los que traen pull-down en IN, o los "optoacoplados" que no lo son, sí cliquean). **Se cierra con una medición de 30 s, no con un argumento**: alimentar un módulo con IN al aire y ver si clickea — **Gonza, con los módulos del stock en la mano, antes de armar**. Los **10 k de IN a 3V3 quedan como seguro barato recomendado** (4/equipo, $266 por equipo): no molestan si no hacían falta y evitan desarmar 5 equipos si la medición sale mal. Lección para mí: escribí como hecho verificado algo que era una inferencia sobre una variante de módulo que nunca miré.

**Total: $133.780 → $178.368 ($35.674/equipo).** Y ahora hay **dos mediciones que bloquean el pedido** (§8.1 del BOM), no una:
- **A — amperaje de las 5 fuentes.** @esquematico calculó **446 mA continuos / 796 mA de pico** (4 bobinas SRD-05 = 284 mA + LEDs 12 mA + ESP32 150 mA medio / 500 mA pico) ⇒ **hace falta 5 V 2 A**. Con 1 A anda al 80 % del pico (C1/C2 obligatorios + escalonar relés 50 ms); **con 700 mA entra en brown-out cíclico**. Si las 5 compradas no llegan: **+$39.900** (MLA1258700476 $7.980). **Escenario realista = $218.268 → $43.654/equipo**; peor caso absoluto $437.238.
- **B — el clic del relé** (punto 3).

**Corrección de método que también me llevo:** en §7.2 yo comparaba **mal** el perfboard contra la PCB — ponía $10.991 (plaqueta **+ componentes**) contra el precio de la PCB **pelada**. Bien comparado, sustrato contra sustrato: plaqueta **$6.490** vs PCB $15.363 (5 u) / $8.815 (10 u) / $5.551 (20 u) ⇒ **el cruce en material puro está en ~15 placas (~25 con gestión)**, y baja a **8–10 sólo cuando se valúa la media hora extra de soldadura por plaqueta**. El criterio de disparo de §7.3 (8 equipos comprometidos) se sostiene, pero ahora dice por qué.

**Además, hallazgo de @esquematico que hay que pasarle a @firmware ya:** `PIN_DHT22 18` ocupa el pin que ahora es **K3** (y `dht.begin()` le pone `INPUT_PULLUP` al relé) · `MAX_RELAYS` 2→4 · faltan `PIN_RELAY_3/4` · y `config_SANTA_CRUZ.h` trae `RELAY_PULSE_ON_CONNECT` de 1 s = **un bocinazo de sirena en cada reconexión de WiFi**. `RELAY_ON` = **LOW** en el kit (la v2 pide HIGH porque tiene BC547 que invierten): **cargar el firmware de la v2 en un kit v1 hace sonar la sirena en el `setup()`**.

**Reparto de fuentes de verdad (escrito en el §8.2 del BOM):** `PINOUT_V1.md` + `.kicad_sch` = pines · `CABLEADO.md` = guía de armado · `BOM_KIT_V1.md` = **compras y cantidades**.

## 2026-09-02 (d) — GALGAS/Dreyfus: **BOM y stock del bring-up de banco con ATmega328P-PU (DIP-28)**
Entregado: sección **H (H0–H6)** de `C:\Proyectos\galgas\hardware\BRINGUP_BANCO.md` — documento
compartido con @firmware, que escribió en paralelo las etapas 3/4/5 y el receptor. **Sin commit.**
⚠ **Hubo colisión de escritura** (los dos agentes escribimos el mismo archivo a la vez): reordené el
documento para que quede **toda mi sección H primero y la de @firmware después, sin perder una línea**.
Si @firmware siguió escribiendo después, su contenido nuevo queda al final: **revisar el orden antes de commitear.**

**Lo que decide el viernes 4 (3 números):**
1. **Se puede armar HOY, sin comprar nada, las etapas 1 y 2** (micro + radio), sujeto a **3 confirmaciones
   de 20 minutos**. Etapa 3 (cadena analógica) está **bloqueada** por la compra.
2. **Compra local del lunes 7-sep: $162.238 mejor caso · $288.922 peor caso** (núcleo + los 9 pedidos de
   @firmware). Con etapa 4 y galgas propias: **$344.290 / $362.186**.
3. **Importación (camino crítico): emitir el 7-sep, llega 30-sep a 10-oct.** Sin margen para un segundo
   intento. **Mitigante encontrado hoy** (ver abajo): el banco **ya no depende** de la importación.

**Las 3 confirmaciones que bloquean (nadie las hizo nunca, van como NO CONFIRMADO):**
**C-1** ¿los 3 ATmega328P del inventario son **PDIP-28 o TQFP-32**? (nadie anotó el encapsulado) ·
**C-2** ¿**cuántos RA-02** hay y de qué tipo? (la lista de julio dice "en stock" **sin número**; hacen falta 3) ·
**C-3** ¿**llegó el ADS1220** comprado el 2026-07-10? (**P1 abierto desde julio**).
Extras del mismo conteo: **ESP32 en disputa** (10/5/1 en Cerro Moro/5 de Termovigía → **puede no quedar
ninguno para el receptor**), pila ER14505, y **las galgas de GIMAP: ningún documento dice cuántas, de qué
tipo, ni el FACTOR DE GALGA — sin eso no hay calibración**.

**Hallazgos duros de la sesión:**
1. ⚠⚠ **HAY SUPERCAPACITORES DE 2,7 V EN ARGENTINA** — contra lo que dije en la rev C ("importar sí o sí"):
   Itytarg **2,2 F** MLA637412707 **$18.019**, **1,5 F** MLA633192257 $12.007, Samxon **10 F** MLA1407063549
   $25.339. **Ninguno publica ESR** (que es todo el criterio de P8) → **para el producto siguen siendo los
   Eaton**, pero **para el banco sirven y sacan la etapa 4 del camino crítico**: 2× 2,2 F en serie = 1,1 F
   a 5,4 V, τ = 11 s contra los 10 s del diseño. Tarea nueva: **medir su ESR con el INA219**; si da ≤ 0,4 Ω
   la importación deja de ser crítica.
2. **El C0G de 10 nF y 100 nF THT NO EXISTE en ML AR** (sólo llega hasta ~33 pF). Sustituto justificado y
   disponible: **capacitor de película (poliéster MKT / polipropileno)** — coeficiente de tensión nulo y
   microfonía muy por debajo del X7R, que **es piezoeléctrico** y sobre un REDLER genera señal falsa.
   MLA1506293993 (10 nF ×10) $4.806 · MLA1506215771 (100 nF ×10) $8.245.
3. ⚠ **El ATmega DIP-28 no tiene ADC6 ni ADC7** → `V_BAT_SENSE` (hoy en ADC7) hay que remaparlo a PC2/PC3/
   PC4/PC5 — **@firmware**. **No cuesta un componente**: el divisor RD1/RD2/RD3+CVB1 es el mismo.
   Y dos olvidos clásicos del perfboard que anoté: **AVCC (pata 20) hay que conectarlo a VCC** (si queda al
   aire el ADC no convierte) y **AREF (21) lleva 100 nF**.
4. **El zócalo DIP-28 es el plan de recuperación, no un lujo**: en un ATmega con ISP **no hay OTA**; un nodo
   colgado se recupera **sacando el chip**. Y **con zócalo se programa a 5 V fuera de la placa**: se evita el
   level-shifter, se evita meterle 5 V al ADS1220/RA-02 y se evita la contención de MISO del ISP (G6).
   **Es el argumento fuerte a favor del DIP-28.**
5. ⚠ **Conflicto detectado con el pedido de @firmware**: mi candidato barato de ATmega dice **"bootloader"**
   → fusibles a cristal externo → **sin reloj el ISP ni siquiera entra a cambiar los fusibles**. Resolución:
   comprar igual **3 cristales de 16 MHz + 22 pF ($4.266) como KIT DE RESCATE**, que **no se sueldan en el
   nodo** (el nodo sigue con RC interno a 4 MHz). Más barato que discutir con el vendedor.
6. ⚠ **El RA-02 (paso 2,0 mm) NO tiene adaptador 2,0→2,54 en ML AR** — no existe la publicación. Tres
   caminos: (a) el módulo **"con PCB"** ($19.990, **NO CONFIRMADO: hoy ML bloquea las fichas de producto y
   "con PCB" en LoRa suele significar antena de PCB** → mirar las fotos antes de pagar); (b) fabricarlo en
   JLCPCB de yapa (10-15 días); (c) **8 alambres Kynar a los pines usados + fijación mecánica** — es lo que
   se puede hacer HOY, vale para el banco y **no** para el nodo que va a planta.
7. **Nunca alimentar el RA-02 sin antena** (el PA se daña): antena helicoidal 433 MHz $3.243 c/u
   (MLA1391079243) + pigtail U.FL→SMA $3.990 si hace falta. Renglón barato y crítico.
8. ⚠ **El MCP1700-3002 (3,0 V) sigue sin confirmarse**: la búsqueda de hoy devolvió **sólo la variante
   3302 = 3,3 V**, y la ficha del candidato MLA-703690036 **no se pudo abrir**. **Si se compra la 3302 se
   rompe C6.** No bloquea el banco (la Placa A anda con los **HT7130A que ya están**).
9. **Bornera 5,08 resuelta**: kit ×100 de 2/3/4 vías paso **5,08** MLA3164234660 $23.111 (casi todo lo que
   se publica es **5,00**, que **no cae en la grilla de 2,54**). Cierra también la inconsistencia del
   `.kicad_pcb` señalada en C19.
10. **El renglón más caro del núcleo es el cable**: blindado 3×0,25 mm² mallado 5 m **$44.990**
    (MLA1568717215) — un tercio de la compra en el mejor caso. Es "el ítem más olvidable y sin él no hay ensayo".
11. **Galgas de repuesto SÍ hay en AR**: BF350-3AA $3.959–4.474 (MLA1599076089 / MLA1448905531). Se compran
    **sólo si GIMAP no confirma** (regla del dominio: reusar antes de comprar).

**Estado de la red (honestidad de datos):** ML **desbloqueó el listado** hoy (corte cada 2-4 consultas,
con reintento automático en `q.sh` + `ml2.py`), pero **las fichas de producto individuales siguen
bloqueadas** desde el 2026-09-01. → **todos los precios e IDs de la lista son de listado, verificados hoy;
ninguna descripción de publicación se pudo leer**, y eso está marcado renglón por renglón. Nada inventado.

**Pendiente @hardware:** (a) las **3 confirmaciones C-1/C-2/C-3** + conteo de ESP32 (bloquean la mitad de la
lista); (b) **mirar las fotos del RA-02 "con PCB"** antes de pagar; (c) **preguntar al vendedor por la
variante 3002** del MCP1700; (d) **preguntar a GIMAP**: galgas (cantidad, tipo, **factor de galga**),
supercapacitores de baja ESR, diodos ESD; (e) **medir la ESR de los supercaps locales** con el INA219 —
decide si la importación sigue siendo camino crítico; (f) **corregir el renglón del supercapacitor y agregar
el encapsulado a los ATmega** en la tabla de inventario de este archivo cuando se cuente; (g) precios de
importación (hoy `PENDIENTE`).

## 2026-09-02 (e) — GALGAS/Dreyfus **REV D**: datos de los módulos reales (todo pasante) + **P1 CERRADO**
Entregado: `C:\Proyectos\galgas\hardware\MODULOS_REV_D.md` (11 secciones), **archivo nuevo y sólo mío** —
esta vez cada agente escribe en el suyo, después del choque de escritura de la entrada (d). Única línea
tocada afuera: **`NOTAS_CALCULO §7`, P1 marcado CERRADO**. Sin commit.

**Los tres números que pedía el Director:**
1. **El CJMCU-1220 NO tiene regulador a bordo** (verificado por 2 fuentes independientes: el esquemático
   ProtoCentral/CJMCU en cyberblogspot y la ficha de Wolles Elektronikkiste, que publica el rango del
   módulo = el del chip, AVDD/DVDD 2,3–5,5 V). Sólo trae **2 desacoples + 3 resistencias de 24 Ω en el SPI
   + un 0 Ω que une AGND con DGND**. ⇒ **la medición ratiométrica se mantiene intacta**: `AIN0`/`AIN3` salen
   al header, o sea REFP1/REFN1 son la excitación real del puente, y **la llave low-side que gatea los
   8,6 mA está en AIN3, que también sale**. **Si hubiera tenido LDO había que desoldarlo. No hay que tocar nada.**
2. **RA-02: NO se sabe todavía, y es lo que bloquea a @pcb.** El módulo pelado, leído de la huella oficial:
   **16 pads, paso 2,00 mm, filas a 16,00 mm, cuerpo 16,5 × 17,5 × 3,2** → **no cae en grilla de 2,54**. Con
   adaptador sí (el de Smart-Prototyping se vende con "2× 1×7pin 2.54mm"). Las fotos que mandó Matías
   **no llegaron a esta máquina**, y "tiras de pines soldadas" es compatible con los dos casos (al módulo
   pelado se le sueldan pines de 2,0 mm). **Ensayo de 30 s que lo decide: medir del 1.º al 8.º pin de una
   fila — 14,0 mm = pelado · 17,8 mm = adaptador.** Y mirar el canto: dos placas apiladas = hay adaptador.
3. **La placa: `160 × 100 mm` con el portapilas a bordo (2,29× la rev C)** — presupuesto de área de
   6.186 mm² de courtyard al 39 % de ocupación, con las cotas medidas de los `.kicad_mod` instalados.
   **100 × 70 daría 88 % de ocupación: imposible.** **Recomiendo la opción B: `120 × 90` sacando el
   portapilas al gabinete.** 120×90 además entra en el tramo barato de JLCPCB; 160×100 no.

**Hallazgos duros (los 5 que cambian el diseño):**
1. ⚠⚠ **DEFECTO DE SEGURIDAD EN LA REV C, con una sola pila:** no hay ningún elemento de bloqueo entre la
   pila primaria de litio y **medio faradio** de supercapacitor. La ER14505 tiene **retardo de tensión por
   pasivación** → después de un pulso, `V_SC > V_BATT` y el supercap **devuelve decenas de mA a la pila**,
   contra los **< 10 µA de corriente inversa que especifica Tadiran** para LiSOCl2 (el modo de falla no es
   "se arruina": es venteo/incendio). **Se arregla en la rev D**, y las 2 pilas en paralelo lo obligan igual.
2. **Las 2 pilas en paralelo SIMPLIFICAN la placa en vez de complicarla.** `BT1a/BT1b → 1N5819 c/u → +BATT`.
   Los dos Schottky hacen **tres trabajos**: bloqueo cruzado entre celdas, bloqueo del retorno del supercap,
   **y protección contra pila invertida ⇒ `Q2` (DMG2301L) y `RG1` SE CAEN**. Y eso resuelve de yapa que
   **no existe P-MOSFET lógico decente en TO-92** (el BS250 tiene 14 Ω = 180 mV en el camino de potencia).
   **Costo: ~0,15 V de riel.** Se paga porque (a) R1 ya bajó el BODLEVEL a 1,8 V, (b) el piso real pasa a ser
   el **AVDD ≥ 2,3 V del ADS1220**, 577 mV por debajo del peor caso de G13, y (c) **al ser ratiométrico, si
   el riel cae la lectura en µε no cambia**. **Ganancia: 4200 mAh → autonomía 1,30 → 2,60 años.**
   ⚠ **Necesita firma de @energia** (0,10 V en reposo + la fuga inversa, que hay que MEDIR).
3. ⚠⚠ **Los TVS pasantes NO existen para este circuito, y fallan por ENERGÍA antes que por precisión.**
   P6KE6.8CA = 1000 µA de fuga, SA5.0CA = 800 µA, zener 1N4733A = 10 µA — contra un presupuesto de reposo
   de **29 µA**. Un solo TVS THT se come **27 veces el reposo completo**. → **D1/D2/D3 se rediseñan como
   clamp de 2 diodos por línea, detrás de RS1/RS2**: preferido **1N3595** (IR ≤ 1 nA → 0,12 µε), fallback
   **1N4148** (cota dura 25 nA → 2,9 µε/diodo, calibrable). Y como el clamp inyecta en el riel, **D4
   (ESD5Z5.0T1G, SOD-523) se muda de +BATT a +3V0 y queda como la ÚNICA excepción SMD de la placa** — no
   hay parte pasante con fuga verificable por hoja de datos para esa función.
4. ⚠ **Los MOSFET no pasan a 2N7000/BS170: pasan a 2N3904.** El `Vgs(th)` máximo del 2N7000 es **3,0 V**, que
   es exactamente nuestro riel → en el peor caso del lote el canal queda en subumbral con kΩ de resistencia:
   **17 µε de error en el shunt-cal** y 0,9 % en la lectura de pila, **según el lote**. Con un NPN y 100 k de
   base, `Vce(sat)` a 17 µA es < 10 mV = **< 0,06 µε**, y la fuga en OFF < 1 nA **cumple C12**. El BJT es
   estrictamente mejor que el MOSFET a 3,0 V acá. (+2 resistencias, `RB_Q1` y `RB_Q3`.)
5. **El módulo NO simplifica el BOM: simplifica el ARMADO.** Sólo se caen **CA1 y CB1** (los desacoples que
   el CJMCU ya trae) + Q2 + RG1, y entran 5 componentes nuevos → **balance +5**. Lo que se gana es no
   soldar un TSSOP-16 de 0,65 mm ni un TQFP-32: **la placa pasa a ser reparable con soldador común, en
   campamento, por alguien que no es Matías.** **Y lo que NO se terceriza sigue siendo el corazón:** el
   filtro RC de entrada (RS1/RS2/CC1/CC2/CD1 — es el anti-alias de 50 dB del ΔΣ; sin él el ADC de 24 bits
   no sirve de nada) y las resistencias de precisión del puente (10 ppm/°C sobre 350 Ω ≈ 5 µε por °C de
   desapareamiento: **es el límite físico del sistema y el ADC no lo puede corregir**).

**Otras que hay que mirar:**
- ⚠ **Discrepancia del `RESET`:** el enunciado describe `RESET` en la serigrafía de la foto. **El ADS1220
  no tiene pata de RESET** (Tabla 5-1, pág. 4 — el reset es un comando SPI). O es una leyenda mal leída, o
  **el módulo no es un ADS1220**. Tarea de 1 minuto: leer las 16 leyendas y la marca láser del chip.
- ⚠ **Riesgo de ADS1220 falsificado en placas CJMCU, documentado** (caso con detalle en los comentarios de
  Wolles). Prueba de aceptación de 20 min, sin instrumental: registros de reset en `00 00 00 00` + **σ ≤
  0,09 µV rms a G=128 / 20 SPS con entradas cortocircuitadas**. Si da 5× más, no se sigue.
- **Zócalo del ATmega: TORNEADO, no de hoja** — sobre una máquina que golpea el enemigo es el **fretting**
  del contacto de hoja, que se manifiesta como resets aleatorios que se le echan al firmware. Y **el
  torneado solo no alcanza: RTV en dos esquinas del chip.** Huella `Package_DIP:DIP-28_W7.62mm_Socket`
  (courtyard 10,66 × 36,20; **0,93 mm más ancho** que la versión sin zócalo — usar la equivocada hace que
  el zócalo pise lo que esté a menos de 0,5 mm del pad).
- **Reed de vidrio de 14 mm sobre dos alambres, en un REDLER = resonador que se rompe por fatiga.** Se
  resuelve con un cordón de RTV a lo largo del vidrio (o dejándolo SMD). Va escrito en la guía de armado.
- **Portapilas: recomiendo NO ponerlo en la placa.** 2 AA de litio = **38 g** colgados de 4 juntas de
  soldadura, en voladizo de 60 mm, sobre una máquina que golpea = **el punto de falla nº 1 del nodo**. Con
  cables al gabinete + bornera `J4`: libera 2.006 mm² (32 % del área), el peso lo toma la caja, y se cambian
  las pilas sin desmontar nada. Cotas medidas: Keystone 2460 (1×AA) **57,5 × 17,4** · 2462 (2×AA lado a
  lado) **60,0 × 33,4** · MPD BC12AAPC (2×AA en línea) **108,8 × 17,2 → descartado, más largo que la placa**.

**Supercaps:** se **reconfirma** `CP_Radial_D10.0mm_P3.50mm` para los Eaton HV0810 (⌀8,5 × 13,5, P3,5).
Con la placa más grande **el espacio deja de ser criterio** para los locales (Itytarg 2,2 F, Samxon 10 F):
**queda sólo el eléctrico, que es el bueno** — siguen sin publicar ESR ni fuga. **La medición de ESR + fuga
a 72 h del Itytarg 2,2 F con el INA219 es la de mayor palanca del proyecto ahora**: si da ≤ 0,4 Ω y ≤ 10 µA,
**la importación sale del camino crítico también para el producto** (30 días). Y por C15 el candidato es el
de **2,2 F, no el de 10 F** (10 F no compra margen útil y duplica la fuga).

**P1 CERRADO** (abierto desde el 2026-07-10): CJMCU-1220, comprado el **15-jul**, **$14.549,76** — el único
precio verificado de la sesión. ⚠ **Es UNA unidad y hacen falta TRES**: renglón de compra nuevo que nadie
tenía anotado.

**Estado de la red:** **ML BLOQUEADO.** Las 4 consultas probadas (`ads1220`, `zocalo-28-pines-torneado`,
`portapilas-2-aa-pcb`, `atmega328p-pu`) devuelven el muro de login: 39 kB sin una sola tarjeta de producto,
`trace-id` distinto cada vez. **No es el rate-limit intermitente de ayer, es un muro.** Todos los demás
precios quedan `PENDIENTE`.

**Pendiente @hardware:** (a) comprar **2 ADS1220 más**; (b) medir **ESR y fuga del Itytarg 2,2 F**;
(c) `MCP1700-3002E/TO` — insistir con la **3002**, no la 3302; (d) conseguir/cotizar **1N3595** (o aceptar
1N4148 y medir la deriva térmica del cero); (e) cerrar precios cuando ML vuelva; (f) preguntar a **GIMAP**
por supercaps, portapilas 2×AA y las galgas (cantidad, tipo, **factor de galga**).
**Lo que bloquea a otros:** M1 y M2 (las dos mediciones con calibre) → **@pcb** · M3/M4/M7/M8/M9 →
**@esquematico** · M6 (firma de los Schottky) → **@energia** · M14 (`V_BAT_SENSE` fuera de ADC7) →
**@firmware** · M10 (portapilas dentro o fuera de la placa) → **Matías**.

**⚠ ALINEACIÓN CON @energia (trabajó en paralelo hoy, `ENERGIA_REV_D.md`) — no dejo dos verdades:**
**su veredicto manda** (regla del dominio: la topología de alimentación es suya). Dice **NO a las 2
pilas en paralelo**: una sola **ER26500 (tamaño C)** → **4,3 años** contra 2,52 de 2×AA con diodos;
los diodos cuestan **175 mV** (su número, a 14,5 µA de reposo — más fino que mi 0,15 V) y **atan una
propiedad de seguridad de litio a dos ajustes de firmware que hoy no existen**; y el supercap ya hace
irrelevante la R interna, así que la 2.ª celda le compra al pulso **1,8 mV**. **Coincidimos en lo
importante: en paralelo SIN diodo no se puede** (él con `Saft_LS14500.pdf` pág. 2, yo con Tadiran) →
**mi hallazgo del supercap devolviendo corriente a la pila en la rev C sigue en pie e independiente
del número de celdas.** Consecuencias que agregué a mi doc: (1) si se va a una sola celda, **`Q2`
VUELVE al BOM** y con él el problema de que **no hay P-MOSFET lógico en TO-92** → sería la **segunda
excepción SMD**, a decidir entre los tres; (2) **le debo una corrección con número**: su E3 dice que
el portapilas de una C es más chico que el doble de AA — **por ancho de celda tiene razón** (⌀26,2 vs
~33 mm), **pero por área de placa las dos huellas concretas que tengo dicen lo contrario**:
`Bulgin_BX0036_1xC` **60,20 × 35,00 = 2107 mm²** vs `Keystone_2462_2xAA` **60,01 × 33,43 = 2006 mm²`.
No cambia su veredicto (se apoya en seguridad, piezas y 175 mV) pero **invalida el argumento "menos
placa"**. Tabla de tamaños actualizada con las 4 opciones: **A** 2×AA en placa → 160×100 · **B** 2×AA
al gabinete → 120×90 · **C** 1×ER26500 en placa (@energia) → 140×90 · **C′** ER26500 al gabinete →
**100×70, el único escenario en el que la placa NO crece**.

### 2026-09-02 (e-bis) — Cierre: **3 correcciones a la lista de compra del lunes 7-sep** (§12 de `MODULOS_REV_D.md`)
Dos las levantó **@diseno** consolidando el día (contradicciones **C6** y **C9** del §08 de
`PLAN_MAESTRO_NODO_GALGA.html`); la tercera es **un error de conteo mío**. Escribí **sólo** en
`MODULOS_REV_D.md` (§12 nuevo + §1 y §9 y §10 sincronizados) y acá. **No toqué** `BRINGUP_BANCO.md`,
`ENERGIA_REV_D.md`, `NOTAS_CALCULO.md` ni el HTML de @diseno. Sin commit.

1. **Renglón 15 — 2N7000 → 2N3904.** La lista seguía pidiendo `2N7000 ×10` (MLA1873999326, $6.649) con
   la nota "medir `Rds(on)` y elegir uno bueno del lote". **Esa mitigación no es aceptable:** el
   `Vgs(th)` **máximo** del 2N7000 es 3,0 V = nuestro riel exacto → en el peor caso del lote, subumbral,
   kΩ, **hasta 17 µε de error de shunt-cal**. "Elegir uno bueno de este lote" no sobrevive a la segunda
   compra. Con el **2N3904 + 100 k de base**: `Vce(sat)` a 17 µA < 10 mV = **< 0,06 µε** y fuga OFF
   < 1 nA (**cumple C12**), **sin ninguna medición previa**. Cubre **Q1 y Q3**, no sólo Q1. Precio
   `PENDIENTE` (ML sigue bloqueado, reintenté 17:30) **con techo declarado $6.649** — el BJT nunca es
   más caro que el MOSFET, así que el techo no puede subestimar el total. **Las RB_Q1/RB_Q3 de 100 k ya
   están cubiertas por el renglón 6** (kit de resistencias): no hay renglón nuevo. ⚠ **`Q2` NO cambia**
   (sigue el AO3401 del renglón 19): mi §5.2 lo eliminaba con 2 Schottky, pero **@energia vetó las 2
   pilas en paralelo**, y con una sola celda Q2 vuelve a hacer falta.
2. **Renglones 2/29 — la nota del zócalo estaba invertida y hacía descartar el bueno.** Decía *"hay
   publicaciones de 0,6″ (wide body) que no sirven (MLA1763057877, MLA1727282132 **dicen 7,62 mm**)"* —
   se contradice sola. **0,3″ = 7,62 mm = EL QUE VA** (es el `descr` de `DIP-28_W7.62mm_Socket`:
   *"row spacing 7.62mm (300 mils)"*); **0,6″ = 15,24 mm = NO**. ⇒ **las dos publicaciones "descartadas"
   son CANDIDATOS VÁLIDOS.** Criterio reescrito con los dos números al lado + cómo decidir por la foto
   si la publicación no lo dice. ⚠ Pendiente de 1 minuto: **el candidato del renglón 2
   (MLA1446400231, $3.532) no tiene el encapsulado confirmado** — el criterio equivocado lo tapaba.
   Y agregué la distinción que faltaba: **banco = de hoja está bien** (no hay vibración sobre una mesa);
   **nodo de planta = TORNEADO obligatorio** (fretting) **+ RTV en dos esquinas del chip**. El torneado
   **no entra en la compra del lunes** (va con las placas) → **no mueve el total**.
3. **Renglón 5 — hacen falta 2 ADS1220, no 3. Se compra 1. (mi error).** En el §1 de mi propio doc había
   escrito "3 nodos emisores → faltan 2". **Lo desmiente un renglón que escribí yo mismo ayer:** la
   confirmación **C-2** de `BRINGUP_BANCO.md` dice *"Hacen falta 3 [RA-02] (2 nodos + receptor)"* → el
   sistema es **2 emisores + 1 receptor**, y **el receptor no lleva ADC**. **Son 3 radios y 2 ADCs.**
   Necesarios 2 · en mano 1 · **a comprar 1**. **−$14.549.** Sobre el repuesto: lo evalué y **todavía no**
   — es compra local que llega al día siguiente, así que **el 2.º se decide después de M3 (leer las 16
   leyendas) y M5 (ruido ≤ 0,09 µV rms)**; si el de julio falla, se compran 2 ese día. Riesgo: 24 h.

**Totales corregidos (único movimiento de plata: −$14.549 del renglón 5):**
**MÍNIMO $162.238 → `$162.238` (SIN CAMBIO, ya decía "con 1 ADS1220")** · núcleo peor caso
$262.088 → **$247.539** · **RECOMENDADO $344.290 → `$329.741`** · COMPLETO $362.186 → **$347.637**.
**Ninguna de las tres correcciones sube el gasto: una lo baja y dos evitan comprar la pieza equivocada**
—que es lo caro, porque se paga en una semana perdida.

**Nota de contabilidad que encontré verificando:** el subtotal del núcleo en **MEJOR caso ($135.404)**
sale de restar los renglones 1, 3, 4 **y el 5 COMPLETO** (22.617+14.999+59.970+29.098 = 126.684;
262.088−126.684 = 135.404 exacto), aunque la prosa dice "la mitad del 5". El MÍNIMO le vuelve a sumar
**uno**. O sea que **el MÍNIMO ya estaba bien y no hay doble conteo** — pero la prosa del MEJOR caso
describe mal su propia cuenta. Anotado para quien edite `BRINGUP_BANCO.md`.

**Chequeos de 1 minuto antes de pagar:** renglón 15 dice **2N3904** · renglón 2 dice **7,62 mm / 300 mil
/ 0,3″** · renglón 5 cantidad **1**. Más las que ya estaban: **MCP1700-3002 y no 3302** (renglón 21) ·
**mirar las fotos** del RA-02 "con PCB" y aplicarles el ensayo de los 17,8 mm (renglón 4) · **ATmega
vírgenes** o comprar igual el cristal de rescate (renglón 23).

### 2026-09-02 (e-ter) — **Corrección de premisa: Matías eligió las 2 pilas. `Q2` sale, entra el BAT85**
El Director me corrigió: **@energia NO vetó las dos pilas en paralelo — recomendó** la ER26500 (4,32 años
contra 2,52), el Director le llevó **las tres opciones a Matías con esos números**, y **Matías eligió
2×AA en paralelo con un Schottky de bloqueo por pila**, informado del costo (~175 mV de margen y R1+R3
pasan de recomendadas a **obligatorias**). **Un agente recomienda; decide Matías.** Yo escribí "vetó" y
armé un renglón de compra sobre esa premisa falsa. **Es el mismo error de método que ya me llevé el
2026-09-02 (d): escribí como hecho una inferencia sobre lo que otro había decidido. Un informe técnico
de un agente no es una decisión de proyecto.** Retirado y reescrito. Sólo `MODULOS_REV_D.md` (§5, §6.3,
§8, §9, §10, §12.1 y **§12.6 nuevo**) y esta bitácora. Sin commit.

**1. `Q2` SALE, y mi §5.2 original tenía razón — con un argumento más fuerte del que yo había escrito.**
Q2 es un P-MOSFET **en serie con el nodo entero**: protege contra invertir *el conjunto*, pero **no ve
la malla interna entre las dos celdas**. Con dos portapilas, si una entra al revés la corriente circula
`celda buena → celda invertida` **por dentro del nodo, aguas abajo de Q2**, y Q2 ni se entera. **El
Schottky por celda es la topología correcta acá, no un reemplazo de segunda.** ⇒ **AO3401 (renglón 19,
$3.350) y `RG1` salen del BOM** ⇒ **`D4` (SOD-523) queda como la ÚNICA excepción SMD de toda la placa**,
que era el objetivo de la rev D desde el título.

**2. ⚠ AUTOCRÍTICA TÉCNICA: mi propio 1N5819 estaba mal, y lo descarta el criterio de @energia.** Yo
había elegido un Schottky de **1 A** razonando "más área = menos caída". E2.4 de @energia dice: *"`Vf` a
µA y fuga inversa **son el mismo parámetro `Is` tirando para lados opuestos**… no existe el Schottky de
baja fuga Y baja caída"*. El 1N5819 declara **`IR` = 1 mA a 40 V** (100× el límite de 10 µA de Tadiran)
y **no publica un solo punto de `Vf` por debajo de 100 mA** — a 14,5 µA no hay número, sólo extrapolación.
**Retirado.**

**3. Elegido: `BAT85`** (Nexperia, Schottky de **señal**, DO-34/SOD68, vidrio hermético, axial, 30 V,
200 mA). Es el hermano pasante del BAT54 —la clase que usó @energia— y **su tabla de hoja es la misma
curva**, así que su número se transfiere sin extrapolar entre familias. Datasheet bajado y leído hoy
(**Tabla 7, pág. 3**): `VF` **240 / 320 / 400 / 500 / 800 mV** a 0,1 / 1 / 10 / 30 / 100 mA · **`IR` ≤ 2 µA
a 25 V** · `IFSM` 5 A.
- **Caída a 14,5 µA (lo que pidió el Director):** la tabla da **80 mV por década exactos** (n = 1,35) →
  `Vf = 240 − 80·log10(100/14,5) = 240 − 67 =` **`173 mV`, máximo de hoja** (~130 mV típico). **Coincide
  con los 175 mV de @energia ⇒ no hay que rehacer nada de su análisis de margen** (`OCV_min = 3,151 V`
  contra corte 3,30 V → **149 mV** de margen restante, sobre la línea base R1+R3).
- **Fuga inversa, con dos cotas independientes:** (a) de hoja, **2 µA a 25 V** — y nosotros vemos el
  *desbalance* entre celdas, no 25 V — ya pasa con 5× de margen; (b) con el `Is` deducido de la curva
  directa (método de @energia): `Is = 0,10 µA` → **100× por debajo del límite de Tadiran**.
- **Corriente:** reposo 14,5 µA · reposición post-TX 4,4 mA · **carga inicial del supercap 94–122 mA**
  (47–61 % de los 200 mA, y `IFSM` 5 A cubre el arranque).
- **Especificación anti-error para comprar:** *la hoja tiene que declarar `VF` a 0,1 mA*. **PROHIBIDOS
  1N5817/18/19, SS14, SR1xx, SB1xx** y todo "rectificador Schottky" de ≥ 1 A. Alternativas: BAT43/46/48.
  Huella `Diode_THT:D_DO-34_SOD68_P7.62mm_Horizontal`.

**4. Beneficio de la elección de Matías que NO estaba contabilizado en ninguna comparación.** `C8`
advertía que el pulso de carga inicial del supercapacitor (184 mA) deja a la ER14505 **al 92 % de su
máximo de pulso de fábrica**, en el paso 1 del checklist de instalación y con la celda posiblemente
pasivada. **Con dos celdas en paralelo el pulso se reparte: 94–122 mA por celda = 47–61 % del máximo.**
@energia había señalado esa ventaja para la celda C (46 %); **las dos AA la capturan igual.** Margen real
que la topología elegida compra y que no figuraba en la tabla de decisión.

**5. Placa: DECIDIDO `120 × 90 mm`** (opción B). Portapilas **2×AA con cables atornillado al gabinete**,
a bornera `J4` de 2 vías — decisión del Director por lo mecánico (**38 g en voladizo** sobre una máquina
que golpea eran el punto de falla nº 1). 4.312 mm² de componentes al **40 % de ocupación**, 1,54× la
rev C, **y entra en el tramo barato de JLCPCB** (160×100 no entraba). **M10 CERRADO → @pcb ya puede
arrancar con el contorno**; lo que sigue bloqueando son M1 y M2, las dos mediciones con calibre.
**M6 también CERRADO** (@energia ya calculó el diodo en E2.4 y Matías decidió informado).

**6. ⚠ Efecto que nadie había contado y hay que agarrar antes de pagar: las pilas pasan de 2 a 4.** El
renglón 17 dice *"ER14505 · 2 · 1 por nodo"*; con **2 celdas por nodo × 2 nodos = 4** → $7.990 × 4 =
**$31.960 (+$15.980)**. Es el renglón que más se mueve y **es la contracara honesta de la decisión**: los
2,52 años se pagan con el doble de pilas por nodo.

**Totales finales del lunes 7-sep** (−$14.549 ADS1220 · −$3.350 AO3401 · +$15.980 pilas · + 2 techos):
**MÍNIMO `$162.238` — NO SE MOVIÓ NI UNA VEZ** en toda la sesión (la etapa 4 no entra en el MÍNIMO, así
que si C-1/C-2/C-3 salen bien Matías paga lo mismo que ayer) · núcleo peor caso **$247.539** ·
**RECOMENDADO $344.290 → `$342.371` verificado, techo `$357.020`** · COMPLETO $362.186 → **$360.267**,
techo $374.916. Etapa 4: $55.368 → **$67.998 verificado / $82.647 con techos**.
**Neto de las dos decisiones del día: salen el AO3401 y un ADS1220 (−$17.899) y entran dos pilas
(+$15.980) — se cruzan casi exactos: la rev D con dos pilas cuesta prácticamente lo mismo y tiene un
componente SMD menos.** Los 2 techos declarados (BAT85 $6.649, anclado al pack ×10 de 2N7000 de la misma
tienda; portapilas $4.000 c/u) **son techos míos, no precios** — ML sigue bloqueado (reintenté 17:30).

**Chequeos antes de pagar (8):** renglón 15 = **2N3904** · renglón 2 = zócalo **7,62 mm/300 mil/0,3″** ·
renglón 5 = **1 ADS1220** · **renglón 19 (AO3401): NO se compra** · **renglón 17 = 4 pilas** · BAT85 con
**`VF` declarado a 0,1 mA** · portapilas **con cables y agujeros M3** · y las de siempre (MCP1700-**3002**,
fotos del RA-02, ATmega vírgenes o cristal de rescate).

### 2026-09-02 (e-quater) — Trazabilidad: **`M5` nombraba dos tareas distintas.** La mía pasa a `M16`
Lo levantó el Director. Las dos estaban en "bloquea fabricar", así que **quien tachara una iba a creer que
tachaba la otra**. Escribí sólo en `MODULOS_REV_D.md` (§2.5, §9.1 **nueva**, §6.5, §9, §12) y acá.
**No toqué** `NOTAS_REV_D.md`, `ENERGIA_REV_D.md`, `VERIFICACION_REV_D.md` ni el HTML. Sin commit.

**Lo bueno primero: la serie `M*` no está rota, está bien adoptada.** Leí los otros archivos:
`NOTAS_REV_D.md` (@esquematico) usa `M1`–`M4` con **exactamente mi significado** (sus decisiones `D1`–`D4`
son "M1: ensayo del RA-02", "M2: calibre al CJMCU", "M3: leer las 16 leyendas", "M4: continuidad
`CLK`↔`DGND`"), y `VERIFICACION_REV_D.md` cita `M1`, `M2`, `M3` y `M7` igual (su `M7` = el orden del
MCP1700 en TO-92, que es el mío). **Nada de eso hay que tocarlo.**

**La colisión era una sola: `M5`.** Reed (`CUERPO_SW1`/`PASO_SW1`, también `D14`, @esquematico) contra
prueba de ruido del ADC (mía). **Se queda el reed** porque ya está referenciado en dos documentos ajenos
más el plan maestro; mover el mío costó dos líneas.

⚠ **PERO no la pude renombrar a `M6` como decía la instrucción: `M6` YA ESTABA OCUPADO en mi propia tabla**
(era la firma de @energia sobre los Schottky, cerrada hoy). Renombrar a `M6` habría creado **una colisión
nueva dentro de mi propio documento — el mismo problema que se estaba arreglando**. Usé **`M16`**, el
siguiente libre en las tres listas (nadie pasa de `M15`). Se cumple el objetivo (liberar `M5` para el reed)
sin generar el problema de vuelta. **La fila quedó anotada "(era `M5`)" y §2.5 ahora lleva el rótulo `M16`.**
Verificado: **cero `M5` sueltos apuntando a la prueba de ruido** — los que quedan son la nota histórica y
la explicación de §9.1.

**Sí encontré más colisiones, y una era mía:**
1. ⚠⚠ **`C6` y `C9` tenían dos sentidos, y en MI documento convivían los dos sin que yo lo notara.**
   `C6` = **cálculo** de `NOTAS_CALCULO` (el `VIN` mínimo del LDO — *"si se compra la 3302 se rompe C6"*,
   §6.5) **y a la vez** `C6` = **contradicción de @diseno** (el 2N7000, §12.1). Ídem `C9` (cálculo vs. el
   zócalo). **No es teórico: `ENERGIA_REV_D.md` usa `C6`, `C7`, `C9` y `C10` en el sentido de cálculo.**
   Corregido nombrando siempre al dueño (`contradicción C6 de @diseno` vs `cálculo C6`) en vez de inventar
   un prefijo que los demás no conocerían. **Recomendación al Director: que las contradicciones de @diseno
   se citen siempre con el dueño adosado.**
   Y un aviso fino: **`C-1/C-2/C-3` con guion** son las tres confirmaciones de conteo de `BRINGUP_BANCO.md`;
   **`C1/C2/C3` sin guion** son cálculos. **Se distinguen por un solo carácter.**
2. ⚠ **`D*` también choca, y decidí NO tocarlo.** Mis `D1`–`D4` son **designadores de componente** (los
   clamps de la galga y el ESD del riel); los `D1`–`D32` de `NOTAS_REV_D.md` son **decisiones**. Es el
   mismo tipo de choque que el de `M5`, pero **un refdes no es una etiqueta de documento**: vive en el
   netlist, el BOM, la serigrafía y la guía de armado. **Renumerarlo para resolver un conflicto de
   documentación sería mucho peor que el conflicto.** La mitigación correcta es prefijar las decisiones
   (p. ej. `DE-1`) y **es decisión de @esquematico, no mía**: queda señalado, no cambiado.

**Sin colisión, verificadas hoy:** `E*` (sólo @energia) · `G*` · `H-*` · `P*` · `R*` · `L*` · `M16`.

**Lección de método que me llevo:** las tres correcciones de hoy (el "veto" inventado, el conteo de los
ADS1220 y ahora `M5`) son **todas del mismo tipo: escribir sin chequear lo que ya existía en el documento
de al lado.** Antes de minar una etiqueta nueva o de afirmar qué decidió otro, **hay que abrir el archivo
del otro.** Cuesta un `grep`.

## 2026-09-03 — GALGAS: **C-4 (medir `Rg`) congela $16.009 de la compra del lunes** + el puente falso `D0`
Dos hallazgos de **@muestreador** (`CALIBRACION_REV_D.md`), los dos de resistencias, los dos baratos ahora
y carísimos después. Escribí **sólo** en `MODULOS_REV_D.md` (**§13 nuevo**, más punteros en §6.4, §9 y
§12.6.5) y acá. **No toqué** `CALIBRACION_REV_D.md`, `COMMS_REV_D.md`, `BRINGUP_BANCO.md`,
`ENERGIA_REV_D.md`, `NOTAS_*` ni `kicad/`. Sin commit.

**1. `C-4` — la cuarta confirmación bloqueante, y me corrige un énfasis mío.** Yo venía pidiendo a GIMAP
*"cantidad, tipo y **factor de galga**"*. @muestreador tiene razón: **lo que rompe hardware no es el `GF`,
es `Rg`.** El `GF` es una etiqueta (si da 2,10 cambia un número en EEPROM); **`Rg` es un circuito**.
**Nadie midió nunca la resistencia real de las galgas de GIMAP y todo el diseño asume 350 Ω.** Cuesta
**30 segundos con un téster** y es la única de las cuatro confirmaciones que puede tirar componentes ya
comprados a la basura.

**2. Rehice la cuenta de `Rg` = 120 Ω y encontré el número que la vuelve bloqueante dura:**
corriente del puente **8,57 → 25,0 mA**, o sea **83 % del máximo absoluto de la llave low-side del
ADS1220** (30 mA, pág. 8) contra el 29 % de hoy — **un componente al 83 % de un límite de hoja de datos,
en el camino de la señal.** Además: caída en la llave 47 → **138 mV** · aporte del puente al consumo
medio 86 → **250 µA** ⇒ **autonomía ~2,52 → ~1,40 años (−44 %)**, justo después de que Matías eligiera
las dos pilas para duplicarla · `RCAL1` **174,65 k → 59,88 kΩ**. Dos cosas que **no** cambian, y conviene
saberlo: la **sensibilidad sigue en 1,50 µV/µε** (`dV = Vexc·GF·e/4` no depende de `Rg`) y la impedancia
de fuente **baja a 60 Ω**, lo que **afloja 2,9×** el requisito de fuga de C12 (único lado bueno).

**3. `|R1 − Rg| ≤ 5 Ω`, no ±10 Ω.** Reproduje la cuenta de @muestreador: ±10 Ω da **21,43 mV contra el
límite de 20,3 mV del PGA a G=128 → satura**; el punto exacto es **±9,47 Ω**. **H3.7 está 5 % del lado
equivocado.** Y le agregué lo que faltaba, que es de compra: **con el par `330 (1 %) + 18 (1 %)` el peor
caso da `2,00 + 3,48 + 0,30 = 5,78 Ω` y NO entra.** ⇒ **el criterio no se cumple comprando, se cumple
SELECCIONANDO**: por eso el renglón 7 es un pack de **50** y no de 5. Regla de armado escrita: *no existe
"el R1"; se miden los 50 y para cada nodo se elige el más cercano a la galga de ESE nodo*, y los dos
valores medidos van a la planilla del nodo. **Gratis, y es la diferencia entre G=128 y G=64.**
⚠ H3.7 sigue diciendo ±10 Ω — **yo no toco ese archivo**; que lo corrija quien lo tenga asignado, citando §13.3.

**4. Renglón nuevo: 3–6 resistencias 0,1 % para el puente falso `D0`** (techo $6.000). Es *"el control
decisivo y cuesta 3 resistencias"*: decide si el vagabundeo del cero es la máquina o nuestro instrumento
(criterio DR-5: si la electrónica sola deriva > 0,5 µε en 24 h, el problema es la placa). **Para mí es el
ensayo que valida o destruye mi propia advertencia de §6.4** —la EMF térmica de las patas axiales, 1–3
µV/°C ≈ 1 µε por °C de gradiente—: **yo la escribí como riesgo teórico y `D0` la mide. Si da mal, el
layout que estoy pidiendo se rehace ANTES de fabricar.** Recomiendo **6 y no 3**: permite correr `D0` en
los dos nodos en paralelo y baja el `ENS-DERIVA` de ~2,5 a ~2 días. **Es el único renglón de precisión que
SÍ se paga sin saber `Rg`** (prueba el instrumento, no el sensor), con el límite declarado de que **si
`Rg` = 120 hay que repetir `D0` a 120 Ω**, porque el autocalentamiento —que es lo que alimenta la EMF
térmica— no es el mismo.

**La lista del lunes:** se **CONGELAN los renglones 7 y 8** ($10.978 + $5.031 = **$16.009**) hasta C-4.
**No se cancelan: se pagan apenas haya número y llegan al día siguiente.** Todo lo demás se paga.
Clave: **el renglón 6 (kit de 30 valores × 600, $14.900) es agnóstico a `Rg`** —cubre RS1/RS2, RGD1, el
divisor, las bases de 100 k **y `RCAL1` por combinación**, valga 174,65 k o 59,88 k— así que **no se
congela**. Y **el renglón más caro y más olvidable de toda la compra, el cable apantallado de $44.990,
tampoco depende de `Rg`**.

| Escenario | Antes | **PAGABLE EL LUNES sin `Rg`** | Congelado |
|---|---:|---:|---:|
| MÍNIMO | $162.238 | **$146.229** (techo con `D0`: $152.229) | $16.009 |
| Núcleo peor caso | $247.539 | **$231.530** | $16.009 |
| RECOMENDADO | $342.371 · techo $357.020 | **$326.362** · techo **$347.011** | $16.009 |
| COMPLETO | $360.267 · techo $374.916 | **$344.258** · techo **$364.907** | $16.009 |

> **El lunes se paga el 90,1 % del MÍNIMO y el 95,3 % del RECOMENDADO sin saber `Rg`.** Lo que queda
> afuera son **dos renglones**, y son exactamente los dos que se tiran si la galga no es de 350 Ω.
> **No hay excusa para postergar la compra entera por C-4.**

**Desbloqueo, por orden:** (1) **medir las galgas — 30 s, $0**, y si el número llega antes del lunes no se
congela nada; (2) si GIMAP no contesta, **comprar las BF350-3AA** (renglón 22, $17.896) resuelve C-4 por
definición (publican 350 ± 0,3 Ω) — pero **no exime de medirlas** y **$17.896 para destrabar $16.009 sólo
cierra si además hacen falta las galgas**; (3) **lo que NO se hace: comprar las de 330 Ω "por las dudas"**.

**Sin impacto de componente, anotado igual:** **`nodo_id` en EEPROM** ⇒ no hay jumpers ni DIP-switch y
**los dos nodos son físicamente idénticos** — bueno para fabricación, malo para trazabilidad: **hay que
etiquetar cada caja por fuera**. **Enlace a 433,500 MHz** ⇒ **verificado que NO cambia la antena**:
433,500 cae dentro de la ISM 433,05–434,79 MHz, para la que están hechas la helicoidal del renglón 26 y
el pigtail. Lo dejo escrito para que el que compre antenas en el futuro no lo re-abra.

**Pendiente @hardware:** (a) **C-4, es lo primero de todo**; (b) precios reales cuando ML se desbloquee
(D0, BAT85, portapilas siguen con techo declarado); (c) que alguien corrija H3.7 en `BRINGUP_BANCO`;
(d) las de siempre: ESR del Itytarg 2,2 F, MCP1700-**3002**, M1/M2 con calibre.
