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
