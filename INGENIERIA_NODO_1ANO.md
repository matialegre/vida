# INGENIERÍA DEL NODO DE 1 AÑO — análisis comparativo REAL (2026-07-08)

> Matías pidió el cálculo posta, comparando micros y protocolos, y con el dato de realidad: **una LiPo de 8800mAh le duró 1 DÍA.** Acá está por qué, y qué se cambia.

## 🔬 AUTOPSIA: por qué 8800mAh murieron en 1 día
8800 mAh / 24 h = **~367 mA de consumo PROMEDIO.** Eso NO es "bajo consumo" — es un nodo prácticamente despierto todo el tiempo. Culpables (todos juntos):
1. **ESP32 con WiFi activo** = 120–260 mA sostenidos. Si el emisor mantenía WiFi para reportar, ya solo eso te da el número. El deep-sleep del ESP32 es 10µA, pero si el WiFi/loop no se apagan de verdad, no dormís nunca.
2. **El STEP-UP (boost)** = doble condena. Boosteás 3.7→5V y después el ESP32 baja 5→3.3V con su LDO: **dos conversiones, ~70% de eficiencia combinada**, MÁS la corriente quiescente del boost que corre 24/7 aunque el ESP duerma.
3. **El puente de Wheatstone siempre prendido** = otros mA continuos.
> Moraleja: **la teoría no mintió; el ESP32+WiFi+boost es el anti-patrón.** Las cuentas dan lindo cuando el sleep es de verdad µA. Con este stack el sleep nunca fue µA.

## 📐 CÓMO SE CALCULA (la metodología, sin humo)
```
Autonomía(h) = Capacidad_útil(mAh) / Consumo_promedio(mA)
Consumo_promedio = Σ(I_fase × t_fase) / T_ciclo
Capacidad_útil = Capacidad_nominal × derate
```
Y el `derate` es lo que la realidad te cobra (por eso las cuentas "se comen la batería"):
- **Autodescarga:** LiSOCl2 ~1%/AÑO (excelente). **LiPo ~5%/MES → perdés ~50% en un año solo por estar guardada.** (Por eso la LiPo es pésima para 1 año.)
- **Temperatura:** frío baja capacidad; la LiPo sufre mucho, la LiSOCl2 aguanta -40°C.
- **Peukert / pulsos:** el TX de LoRa pincha 120mA de golpe. La LiSOCl2 tiene **alta impedancia interna → el pulso le hace caer la tensión → brownout.** ⚠️ Solución obligatoria: **supercapacitor o HLC en paralelo** a la LiSOCl2 para bancar el pulso de TX (esto es estándar en sensores LoRaWAN de años y es EXACTAMENTE el tipo de detalle que te come el proyecto si no lo sabés).
- **Tensión de corte:** no usás el último ~15-20%.
- **Conversor:** cada step-up/down se lleva su parte + quiescente.

## 🏗️ LA ARQUITECTURA (3 unidades — como la planteaste, y está BIEN)
- **2 EMISORES** (galga + acondicionamiento + LoRa): a BATERÍA, deben durar 1 año. → NO ESP32.
- **1 RECEPTOR** (LoRa RX + ESP32/similar + Internet, a 220V): enchufado, con internet de LDC ya conseguido. → **acá el ESP32 SÍ va** (está a la pared, no importa el consumo). Este es el lugar correcto del ESP32.

El error del sistema viejo fue poner ESP32+WiFi en los EMISORES. El ESP32 va solo en el receptor.

## 🔀 COMPARACIÓN DE MICROS (para el emisor de 1 año)
| Micro | Sleep | Activo | ADC | ¿1 año? | Notas |
|---|---|---|---|---|---|
| **ESP32** | 10µA (si dormís de verdad) | WiFi 120-260mA / LoRa ~40mA | 12-bit (ruidoso) | ❌ | tu prueba lo confirma; va al RECEPTOR |
| **ATmega328P @8MHz/3.3V** | **~1-6µA** | ~3.5mA | 10-bit (flojo) | ✅ | simple, barato, probado; ADC pobre → usar ADC externo |
| **STM32L0/L4** | ~1µA (STOP) | 1-5mA | 12-bit + | ✅ | más capaz (filtros/FFT), mejor ADC, más laburo |
| **RP2040/Pico** | ~180µA (dormant malo) | — | 12-bit | ❌ | MicroPython no hace deep sleep fino |
| **nRF52** | ~1-3µA | bajo | 12-bit | ✅* | radio BLE (corto alcance); necesitaría LoRa externo |

**Recomendado emisor: ATmega328P @3.3V/8MHz** (simple y probado) **o STM32L0** (mejor ADC). NO ESP32, NO Pico.

## 🎯 EL ADC ES CLAVE (la galga es una señal chica)
La galga da microvolts; el INA333 amplifica, pero **el ADC de 10-bit del ATmega o el de 12-bit del ESP32 son ruidosos para esto.** Los sistemas de galgas serios usan un **ADC de puente dedicado de 24-bit**: **HX711** (barato, el de las balanzas) o **ADS1232/ADS1220** (industrial, mejor). Ventajas: 24 bits resuelven la microdeformación, tienen ganancia interna (a veces te ahorrás el INA), consumo bajísimo, y se GATEAN (encienden solo al medir). → **Emisor = ATmega/STM32L + HX711/ADS1232 + LoRa.**

## 📡 COMPARACIÓN DE PROTOCOLOS (emisor)
| Protocolo | Alcance | Consumo | Data | ¿Sirve? |
|---|---|---|---|---|
| **LoRa 433MHz** | km | bajo (TX pulso corto) | baja (perfecto p/ 0.33Hz + batería) | ✅ **el elegido** |
| WiFi | ~50m + infra | ALTO (mató la batería) | alta | ❌ solo receptor |
| BLE | 10-50m | bajo | media | ❌ corto en planta metálica |
| NRF24 2.4GHz | 10-100m | bajo | media | ❌ 2.4GHz muere entre fierros |
LoRa gana claro. Ya lo tenías bien.

## 🔋 BATERÍA RECOMENDADA (emisor 1 año)
- **LiSOCl2 3.6V** (Saft LS14500 AA 2.6Ah, o LSH14 C 5.8Ah) — autodescarga ~1%/año, aguanta frío, tensión estable. **+ supercap/HLC en paralelo** para el pulso de TX.
- **LDO de bajo Iq** (MCP1700 ~1.6µA) a 3.3V, o directo (el SX1276 aguanta 3.9V). **NADA de boost/step-up.**
- Con el puente gateado + reporte cada 3-5 min → **1 año con 1-2 celdas AA de LiSOCl2** (ver `PRESUPUESTO_ENERGIA_GIMAP.md`). Tu idea de 2 celdas por nodo es sana y da margen.

## ⚡ LA DISCIPLINA QUE EVITA EL "1 DÍA" OTRA VEZ
**Antes de creerle a ninguna cuenta: medí el consumo en SLEEP con el INA219.**
- Si el sleep da **µA** → las cuentas valen, vas a llegar al año.
- Si el sleep da **mA** → algo quedó prendido (WiFi, boost, puente, un LED, un regulador, el firmware que no duerme). Ese número te delata al instante.
El 90% de los "me comió la batería" son eso: el sleep real no es µA. La regla: **el INA219 no miente, la hoja de cálculo sí.** Medir sleep primero, siempre.

## 📊 Lo que dice tu CSV real de campo (galgas_20260213, leído hoy)
- Señales A y B ~1.554-1.557V en reposo, MUY estables. Ruido: stdevA 0.004-0.027, stdevB 0.002-0.013 → **canal A a veces más ruidoso que B** (confirma que los canales NO son iguales).
- **K_A=1, K_B=1** → ¡nunca hiciste calibración de GANANCIA! Solo offsets simétricos (OFF_A=-0.4614, OFF_B=+0.4614 = centraste ambos a un punto común). → Confirma que falta el protocolo de calibración real (ver `PROTOCOLO_CALIBRACION_GALGAS.md`).
- vbat: A~3.97-4.01V, B~4.12V → eran **LiPo ~4V** (la batería equivocada para 1 año).
- Reporte cada ~256ms (~4Hz) con buffers de 50 muestras → los emisores muestrean rápido y mandan estadística. filtro fc=0.3Hz orden 2 (justo para el golpeteo 0.33Hz — bien pensado).

## 📁 Código del MAC/red LDC (lo que buscabas)
- `C:/Proyectos/galgas/docs/MAIL_DREYFUS_IT.md`, `SOLICITUD_IT_DREYFUSS.md`, `DEPLOYMENT_DREYFUS.md` — registro de MACs para la red industrial LDC.
- `GALGAS POST DREY (2)/.../PLAN_AHORRO_ENERGIA_Y_CLOUD.md` — tu plan de ahorro previo.
(Están en el repo galgas y en la carpeta archivada; los MACs de emisores+receptor para LDC salen de ahí.)

Dominios: @energia (presupuesto+medición), @hardware (LiSOCl2+supercap+LDO+HX711, NO boost), @firmware (ATmega bare-metal, sleep real), @esquematico (front-end galga+ADC de puente).
