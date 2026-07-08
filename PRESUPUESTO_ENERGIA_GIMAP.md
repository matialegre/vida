# PRESUPUESTO DE ENERGÍA — nodos GIMAP (cuentelío posta, 2026-07-08)

> Objetivo: números REALES de cuánto dura la batería y cuánto puede transmitir cada nodo, y **cómo medirlo en el GIMAP** (Matías puede recrear todas las situaciones ahí). Crítico para octubre (Dreyfus, 1 año). Todo lo estimado se REEMPLAZA por medido con el INA219.

## ⚠️ La regla que domina todo: el que manda es el CONSUMO PROMEDIO
Autonomía (h) = Capacidad_batería(mAh) / Consumo_promedio(mA). El consumo promedio lo definen tres cosas, en orden de peso:
1. **El puente de Wheatstone SIEMPRE PRENDIDO = muerte.** Un puente de 350Ω a 3.3V chupa **~9.4 mA continuos** → mata cualquier batería en días. **OBLIGATORIO: gatear el puente** (MOSFET que lo alimenta SOLO durante la muestra) y/o usar puente de alta resistencia (1k–3.3kΩ).
2. **El TX de LoRa** (~120 mA a 17 dBm) — corto pero caro. Menos frecuente y menos potencia = más batería.
3. **El sleep** (µA) — importa para el piso, pero lo tapan los dos de arriba si no se gatean.

## 📊 Nodo DREYFUS (ATmega328P@8MHz/3.3V + SX1276 + Wheatstone/INA333) — el de 1 AÑO
Perfil: dormir → cada T_report despertar → gatear puente+INA → muestrear ventana corta (capturar el golpeteo 0.33Hz basta con ~5-10Hz por 3s) → calcular → TX LoRa → dormir.

Consumos por fase (a MEDIR con INA219; valores de arranque):
| Fase | Corriente | Duración |
|---|---|---|
| Sleep (ATmega power-down + WDT + SX1276 sleep, puente OFF) | ~6.5 µA | casi todo T_report |
| Muestra (puente gateado 3.3kΩ ~1mA + INA333 ~50µA + ATmega activo 3.5mA) | ~4.55 mA | ~3 s |
| Cálculo | ~3.5 mA | ~0.5 s |
| TX LoRa 17dBm | ~120 mA | ~0.15 s |

**Escenario A — reporte cada 60 s:** promedio ≈ **0.56 mA** → 1 año pide ~4.900 mAh.
**Escenario B — reporte cada 5 min (300s):** promedio ≈ **0.12 mA** → 1 año pide ~1.030 mAh.

### ¿Cuántas baterías?
- **1× LiSOCl2 AA (Saft LS14500, 2.6 Ah):** Escenario B → **~2 años**. Escenario A → ~6 meses. → **con reporte cada 5 min, UNA sola pila de litio-tionilo AA hace el año con margen.**
- **1× LiSOCl2 tipo C o D (LSH14 5.8Ah / LSH20 13Ah):** años, sobra para cualquier escenario. Ideal si el gabinete lo permite.
- **NADA de step-down (buck):** su corriente quiescente arruina el promedio en sleep. LDO de bajo Iq (MCP1700 ~1.6µA) o directo desde los 3.6V (el SX1276 aguanta 3.9V).

**Conclusión Dreyfus:** 1 año es MUY alcanzable con **1 LiSOCl2 AA** si (a) se gatea el puente, (b) se reporta cada 3-5 min, (c) sleep real del ATmega. La decisión fina la dan las mediciones del INA219 en el GIMAP.

## 📊 Nodo PUENTES/MOLINO (baja frecuencia, transmite-un-rato luego SD)
- Fase "transmitiendo en vivo" (10-60 min): consumo alto tipo streaming/telemetría frecuente — se banca porque es corto y estás ahí.
- Fase "solo SD + ventana RX" (meses): igual que Dreyfus pero con escritura a SD periódica + ventana RX cada N min para poder reactivar (ver PARTE_GIMAP R1). Presupuesto ≈ Dreyfus + costo de la SD (la SD en escritura pincha 20-100mA en ráfagas cortas; gatearla también ayuda).

## 📊 Nodo LAB (WiFi 1kHz, batería pelada + botón on/off)
- SIN ahorro por diseño. WiFi + streaming 1kHz. Consumo alto (~80-150 mA sostenido, medido hoy: los Picos daban 75-120mA). Autonomía de HORAS, y está bien: es sesión corta o enchufado. El botón on/off corta todo. No hay cuentelío de años acá, hay "que aguante la sesión".

## 🔬 QUÉ PROBAR EN EL GIMAP para tener números REALES (no estimados)
Con el **INA219 en serie con la batería** (driver ya está en el branch ECO):
1. **Consumo por fase:** `power bench` mide idle/muestra/SD/TX por separado. Anotar mA de cada uno.
2. **Consumo promedio real de un ciclo completo** (sleep→muestra→TX→sleep) a cada T_report (60s, 300s). De ahí sale la autonomía real = capacidad / promedio.
3. **Descarga real acelerada:** correr el nodo con una batería CHICA conocida (ej. 200mAh) hasta que muera, medir horas, extrapolar a la pila final. Recrea el año en un día.
4. **Costo real del TX LoRa** a distintas potencias (11/14/17/20 dBm) y del puente gateado vs continuo → ver cuánto ahorra cada palanca.
5. **Alcance vs potencia:** cuánto cuesta en batería subir potencia para llegar más lejos (el trade-off de campo).

Con esos 5 números, el "cuentelío" deja de ser estimación y se vuelve dato. Todo va a la bitácora de @energia.
