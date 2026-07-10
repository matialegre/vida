# ESTUDIO DE INGENIERÍA — sistema Dreyfus (galgas) para octubre 2026
> Cómo lo haría el equipo, consolidado. Fuentes: PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO + análisis del CSV real de campo.

## 1. El problema, en una frase
Detectar la rotura de una cadena en un eje que gira a 20 RPM (golpeteo de eslabones ~0.39 Hz medido), comparando la deformación de 2 galgas (A y B), con nodos que deben durar **1 año** a batería, y que se pueda **calibrar y verificar in situ** en la planta.

## 2. Arquitectura (3 unidades) — confirmada
```
[EMISOR A: galga+ADC+LoRa, batería 1año] --\
                                            >--LoRa 433MHz--> [RECEPTOR: LoRa RX + ESP32 + Internet LDC, a 220V]
[EMISOR B: galga+ADC+LoRa, batería 1año] --/                        |
                                                                    +--> dashboard local (AP) + cloud
```
- **Emisores (2):** a batería, 1 año, SOLO LoRa. NO ESP32 (probado: mató 8800mAh en 1 día).
- **Receptor (1):** a 220V, ESP32+LoRa+Internet (LDC ya autorizó). Acá el ESP32 SÍ va (enchufado).

## 3. Lo que la DATA REAL de campo ya nos enseñó (CSV 133045)
- Golpeteo **0.39 Hz** → 5 Hz de muestreo sobra. **El problema NO es velocidad.**
- Ruido **1.1 mV** sobre eventos de 7-20 mV → **SNR ~4.7×, POBRE.** El evento grande se ve; un corte chico/lento NO.
- **A-B mean=0 forzado** por offset simétrico → sin K_A/K_B reales el A-vs-B no es confiable.
- **CONCLUSIÓN: los dos problemas de octubre son RESOLUCIÓN y CALIBRACIÓN, no tasa ni radio.**

## 4. 🔬 EL ADC — el corazón del rediseño analógico
La galga en puente de Wheatstone da microvolts. Hoy se amplifica con INA333 y se lee con el ADC de 12-bit del ESP32 (ruidoso, no lineal) → 1.1mV de ruido. La solución profesional: **ADC sigma-delta de 24-bit dedicado a puente (bridge/load-cell ADC)**, que además **excita el puente y amplifica** — reemplaza al INA333 Y al ADC, y se gatea para ahorrar.

| ADC | Bits | Canales | PGA | Excitación puente | SPS | Consumo | $ | Para Dreyfus |
|---|---|---|---|---|---|---|---|---|
| ESP32 interno (actual) | 12 (ruidoso) | — | no | no | alto | — | — | ❌ 1.1mV ruido |
| **HX711** | 24 σΔ | 2 (A g128/64, B g32) | 32/64/128 | **sí (E+/E-)** | 10/80 | ~1.5mA act / <1µA PD | ~$1-2 | ✅ prototipo YA (se consigue en todos lados, el de las balanzas) |
| **ADS1232** | 24 σΔ | **2 diferenciales** | 1-128 | **sí** | 10/80 | ~3mW, power-down | ~$4-6 | ✅✅ **el elegido**: 2 canales MATCHED en 1 chip (ayuda al A=B), + sensor de temp, mejor ruido |
| ADS1220 | 24 σΔ | 4 mux | 1-128 | IDAC | ≤2k | bajo | ~$5 | ✅ si se quiere flexibilidad/más sensores |

**Recomendación:**
- **Camino rápido (esta semana, para probar):** HX711 — lo conseguís hoy, lo enchufás al puente, y ya ves el salto de resolución. Un HX711 por galga (o los 2 canales del mismo con cuidado por la ganancia).
- **Camino final (octubre):** ADS1232 — un chip, 2 canales igualitos (clave para que A y B arranquen parejos), sensor de temperatura integrado (para compensar deriva), y se pone en power-down entre muestras.
- **Ganancia esperada:** de 12-bit ruidoso (1.1mV) a ~19-20 bits libres de ruido → **ruido ~0.1mV o menos → SNR de 40-50× → detectás cortes chicos y lentos, no solo el toque grande.**
- **BONUS:** el bridge-ADC EXCITA el puente él mismo y se apaga → el "gateo del puente" (el que mata la batería si queda prendido) sale gratis: el ADC prende el puente solo cuando mide.

## 5. El nodo emisor completo (BOM y por qué)
| Bloque | Elección | Por qué |
|---|---|---|
| MCU | **ATmega328P @8MHz/3.3V** (o STM32L0) | sleep µA real; el ESP32 no llega a 1 año |
| ADC/puente | **ADS1232** (o HX711 proto) | 24-bit, excita+amplifica+gatea, reemplaza INA333 |
| Radio | **LoRa RA-02/SX1276** 433MHz | largo alcance, TX pulso corto, 0.39Hz+batería sobran |
| Batería | **LiSOCl2 3.6V** (Saft LS14500 AA ×1-2) | autodescarga 1%/año (la LiPo pierde 5%/mes) |
| Pulso TX | **supercap/HLC en paralelo** | la LiSOCl2 tiene alta impedancia; sin esto, brownout en cada TX |
| Regulación | **LDO bajo Iq** (MCP1700) o directo | NADA de boost (su quiescente mató la batería vieja) |
| Calibración | **shunt-cal**: R precisión + relay/MOSFET por canal | verificar A=B in situ sin instrumental |
| Sensor extra | temp (del ADS1232 o dedicado) | compensar deriva de galga+ADC |
| Wake sin tocar | **reed switch + imán** | retomar TX en lugar sellado pasando un imán |

## 6. Presupuesto de energía (resumen, ver PRESUPUESTO_ENERGIA)
Con puente gateado (lo hace el ADS1232) + reporte cada 3-5 min → **~0.12 mA promedio → 1 LiSOCl2 AA (2.6Ah) ≈ 2 años.** 1 año con margen holgado. **Pero se MIDE con el INA219 antes de creerlo** (el sleep tiene que dar µA; si da mA, algo quedó prendido).

## 7. Calibración (resumen, ver PROTOCOLO_CALIBRACION)
Shunt-cal: resistor de precisión en paralelo a un brazo → deformación simulada calculable → ajustar K de cada canal para que A y B lean lo mismo. En planta: disparás el shunt-cal, si A y B dan lo esperado → cadena sana y muestras confiables. Persistir K_A/K_B/offsets en EEPROM.

## 8. Plan de construcción (orden)
1. **Banco (esta semana/receso):** puente + HX711 + ATmega → medir el ruido real vs el ESP viejo (validar el salto de SNR). Con el INA219, medir sleep.
2. **Front-end analógico** (@esquematico): shunt-cal + gateo + protecciones. Es "la peluda" pendiente.
3. **Firmware ATmega bare-metal** (@firmware): sample→ADC→stats→LoRa→sleep, ventana RX Class A, persistencia de cal.
4. **PCB** (@pcb): emisor bajo consumo (supercap cerca del LoRa) + receptor. Convergencia UTN.
5. **Calibración de las 2 galgas** con shunt-cal + verificación A=B.
6. **Prueba de autonomía** (descarga acelerada con pila chica) + **prueba de alcance** en planta.
7. Receptor: el RX 3.7.0 (branch rx/task08-completo, ya compilado) + registro de MACs para red LDC (docs/MAIL_DREYFUS_IT.md).

## 9. Riesgos / lo que NO hay que olvidar
- Medir sleep con INA219 ANTES de confiar en cuentas (la lección del 8800mAh).
- Supercap para el pulso de TX (o la LiSOCl2 da brownout).
- Deriva térmica: registrar temp, compensar.
- Verificar A=B con shunt-cal en planta antes de confiar en datos.
- Alcance real emisor→receptor en el entorno metálico de la planta.

---
# 🔄 REVISIÓN CRÍTICA (2026-07-08, pedida por Matías — generator≠evaluator aplicado al propio diseño)

## Corrección estratégica: DOS ETAPAS en vez de rediseño total para octubre
El diseño original (ATmega clean-sheet) es correcto como destino pero ARRIESGADO como plan de octubre (firmware desde cero + cursada desde 18-ago). Corrección:
- **v2.5 → OCTUBRE (bajo riesgo):** REUSAR el firmware ESP32 validado de galgas-supabase (deep sleep + OTA + cal NVS ya probados E2E) con 4 cambios quirúrgicos: (1) ADC 24-bit (HX711/ADS1232) en lugar del ADC interno, (2) shunt-cal, (3) power chain corregida (sin boost, puente gateado por el ADC, batería correcta), (4) emisores reportando por **LoRa (SPI)** en vez de WiFi — el wake WiFi (~600mAs/conexión) era el asesino; el TX LoRa (~20mAs) no. Con eso el ESP32 promedia ~0.15mA → 1 año alcanzable. El "NO ESP32" absoluto era incorrecto: es "NO ESP32-con-WiFi-en-el-emisor".
- **v3 → PROYECTO FINAL (sin deadline encima):** el clean-sheet ATmega/STM32L del paper, alimentado con los datos de campo que la v2.5 traiga de octubre. Mejor tesis: comparación real v2 → v2.5 → v3.

## Correcciones técnicas al paper
1. **INA333 NO queda "reemplazado"**: dos caminos válidos — (A) mantener INA333 + ADS1220 (máxima performance, reusa lo conocido) o (B) ADS1232 integrado (menos partes). El paper debe mostrar ambos.
2. **Verificar DISPONIBILIDAD EN ARGENTINA antes de fijar BOM**: HX711 = en todos lados; ADS1232 y LiSOCl2 Saft = confirmar MercadoLibre/TodoMicro/DigiKey-AR ANTES. Si el ADS1232 no se consigue: INA333+ADS1220 o HX711 seleccionado. Alternativas de batería si LiSOCl2 es cara/escasa: evaluar con números (una LiPo grande con presupuesto medido, pack alcalino D — con sus contras de autodescarga/frío documentados).
3. El paper queda VÁLIDO como diseño v3/Proyecto Final; agregar sección de estrategia en dos etapas.

# 🔄 REVISIÓN 2 (2026-07-08, mismo día): CAMBIO DE CONTEXTO → GO a la v3
Dato nuevo de Matías: está DE VACACIONES (hasta ~18-ago) y sumó un COMPAÑERO CRACK EN ANALÓGICA. Eso invierte el cálculo de riesgo de la Revisión 1:
- **DECISIÓN: GO al clean-sheet v3 para octubre**, con división de trabajo: compañero = front-end analógico completo + power chain (su fuerte, era "la peluda"); Matías = firmware + sistema + radio + calibración + integración cloud.
- Corrección: el firmware del ATmega NO es "bare-metal desde cero" — ATmega328P = chip de Arduino (Pro Mini): framework Arduino + LowPower lib (ya planeado en el cosechador). Territorio conocido.
- **RED DE SEGURIDAD (no negociable): la v2.5 (ESP32 validado + ADC 24-bit) queda como plan B vivo.** Checkpoint duro ~15-SEP: si el nodo v3 pasa banco (ruido, sleep µA MEDIDO, shunt-cal A=B, autonomía proyectada) → v3 a la parada; si no → v2.5 a la parada y v3 sigue como Proyecto Final. Octubre garantizado en ambos escenarios.
- Plan 6 semanas (de a 2): S1-2 validar bloques (ruido ADC con galga real, sleep µA, LoRa, pulso TX sobre LiSOCl2+supercap) · S3-4 integrar + shunt-cal + A=B · S5-6 endurecer + resistencia + descarga acelerada + checklist campo.
- UTN: verificar si el Proyecto Final admite equipo de 2 (el compañero como co-autor lo fortalece).
- PENDIENTE: nombre del compañero → RED_HUMANA.md (roster).

# 🔬 RE-EVALUACIÓN del amplificador/ADC (pedida por Matías 2026-07-10: "la deformación es MUY chiquita")
Números reales: galga 350Ω, GF=2, ¼ de puente, Vexc=3.3V → 100µε=165µV, 10µε=16.5µV, 1µε≈1.6µV. **Es medición de microvolts, cerca del ruido térmico (~7nV en BW de trabajo).** Con señal así, el enemigo NO es la resolución del ADC sino el **OFFSET, el DRIFT térmico y el RUIDO** del amplificador.

**Corrección:** el HX711 baja de "opción final" a "solo prototipo barato". Ranking real para señal minúscula:
- **HX711** → SOLO prototipar rápido esta semana (grado balanza, conocido, barato). No para el sistema final.
- **ADS1232/ADS1220 (TI)** → muy buenos, baratos, ratiométricos.
- **🏆 AD7124-8 / AD7190 (Analog Devices)** → EL mejor para galgas de precisión. Gana por: (1) PGA de ruido bajísimo integrado (gain ≤128), (2) **medición RATIOMÉTRICA** = excitar el puente con la misma tensión que la referencia del ADC → el drift de excitación se cancela solo (EL truco para señal DC chica que sobrevive cambios de temperatura en planta), (3) corrientes de excitación + buffers + filtros digitales integrados (menos puntos de drift), (4) chopping interno que cancela offset.

**Decisión de dos etapas:** para exprimir aún más → INA333 (chopper, bajo drift, 1ª ganancia) + ADS1220/AD7124. Pero el AD7124 solo ya alcanza y simplifica.
**Regla nueva:** con galga, medición RATIOMÉTRICA obligatoria (excitación = referencia del ADC) — resuelve el drift térmico que si no te obliga a recalibrar. Verificar disponibilidad AR: HX711 (fácil), ADS1220/ADS1232 (Mouser/DigiKey), AD7124 (importar). @esquematico + @hardware.

## ⭐ DECISIÓN FINAL del ADC (Matías 2026-07-10): la POSTA, sin prototipo barato
Matías define: NADA de HX711 ni "prototipar barato" → se diseña DIRECTO con el ADC definitivo de precisión. Razón: es para Dreyfus + Proyecto Final + durar años en planta; arrancar con HX711 obliga a rediseñar la PCB entera al pasar al bueno. Se diseña UNA vez, con el componente final.
**COMPONENTE ELEGIDO: AD7124-8** (Analog Devices) — o AD7190 / ADS1220 como equivalentes de respaldo si disponibilidad AR lo pide. 24-bit sigma-delta, PGA bajo ruido integrado (≤128), medición RATIOMÉTRICA (cancela drift térmico), corrientes de excitación + buffers + filtros digitales, chopping. Es EL estándar de instrumentación de galgas.
Consecuencia: @esquematico diseña el front-end con AD7124 desde el arranque. @hardware confirma stock/importación del AD7124 (Mouser/DigiKey Argentina o import) + el INA333 solo si se hace pre-ganancia. El banco de esta semana con galga real ya se hace con el AD7124, no con HX711.

## Consumo del AD7124-8 (aclaración 2026-07-10)
El AD7124-8 es SOLO el ADC (no un micro; el MCU es aparte). Consumo: full-power ~930µA, mid ~255µA, **low-power ~90µA (usar este)**, standby ~1-2µA, power-down ~1µA. Como el nodo mide en ráfagas cortas (3s cada 3-5min) y duerme el resto, el ADC aporta **µA promedio, insignificante para el año de batería.** El consumo REAL a vigilar es el PUENTE DE WHEATSTONE excitado (350Ω@3.3V=9.4mA; 1kΩ=3.3mA; 3.3kΩ=1mA) → el AD7124 tiene corrientes de excitación integradas que se apagan solas entre medidas = gatea el puente automáticamente (prende solo en la ráfaga). Esto es CLAVE: sin gatear el puente, muere la batería (fue asesino del 8800mAh). Preferir galga/puente de alta resistencia (1k-3.3kΩ) para bajar aún más el consumo de excitación.

## ⚠️ CORRECCIÓN LDO (Matías 2026-07-10: "cuál es el voltaje mínimo que le entra?")
El MCP1700 tiene dropout ~178mV → necesita entrada ≥3.478V para dar 3.3V. PROBLEMA: la LiSOCl2 (3.6V nom) cae a ~3.3-3.4V al descargarse → el MCP1700 deja de regular ANTES de agotar la pila = desperdicia batería. MALO para nodo de 1 año.
SOLUCIÓN: (a) **directo sin LDO desde 3.6V** — el SX1278 aguanta 3.9V y el ATmega@8MHz anda con 3.6V → cero pérdida, cero Iq, lo más simple y mejor para batería; o (b) **LDO ultra-low-dropout**: TPS7A02 (dropout ~40mV, Iq ~25nA, el ideal) o XC6206/HT7333 (dropout ~100-250mV, fáciles en ML). El AD7124 sí puede tener su LDO chico dedicado para alimentación estable de precisión.
Regla: para nodo de años con LiSOCl2, JAMÁS un LDO de dropout alto (MCP1700) que corta antes de agotar la pila. Directo o ULDO.
