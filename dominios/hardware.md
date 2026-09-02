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
| Supercapacitor 1F 5.5V | 1+ | casa | pulso TX LoRa emisor Dreyfus | 2026-07-10 |
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
