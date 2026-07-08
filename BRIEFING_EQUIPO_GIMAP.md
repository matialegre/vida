# BRIEFING CRUZADO DEL EQUIPO — aprendizajes GIMAP 2026-07-08

> Orden de Matías: TODOS los agentes (software, firmware, backend, frontend, diseño, esquemático, PCB, energía, comms, muestreador, hardware) leen esto para estar al tanto y mejorar. Docs fuente: `PARTE_GIMAP_2026-07-08.md`, `PRESUPUESTO_ENERGIA_GIMAP.md`, `PROTOCOLO_CALIBRACION_GALGAS.md`, `INGENIERIA_NODO_1ANO.md`.

## Los hechos que todos deben saber
1. **4 variantes del datalogger** (ver PARTE): (1) LAB — WiFi, MPU 1kHz + PIEZO, batería pelada con botón on/off, datos a la PC (sin SD); (2) PUENTES/MOLINO — baja frecuencia, transmite un rato → botón "listo" → solo SD; (3) DREYFUS — galga Wheatstone, golpeteo 0.33Hz, LoRa, 1 AÑO de batería; (4) a confirmar (¿cosechador?).
2. **Arquitectura Dreyfus = 3 unidades:** 2 EMISORES a batería (1 año) + 1 RECEPTOR a 220V con internet de LDC (ya conseguido). **El ESP32 va SOLO en el receptor.**
3. **Dato de realidad:** una LiPo de 8800mAh duró 1 DÍA (=367mA prom) por ESP32+WiFi+boost. La teoría no miente; el stack estaba mal. **Regla de oro: medir el sleep con INA219 ANTES de creer cualquier cuenta.**
4. **CSV real de campo:** K_A=K_B=1 → nunca hubo calibración de GANANCIA, solo offsets. Canal A más ruidoso que B. Falta el protocolo de calibración shunt-cal.
5. **Compras de hoy:** 2 cajas estancas grandes, 10 precintos, 2 tomas (para relé si hiciera falta). **Relé = solo aprendizaje, sin caso de negocio claro en FrioSeguro.**

## Qué significa para CADA dominio (marching orders)
- **@firmware:** emisores NO ESP32 → ATmega328P@8MHz o STM32L bare-metal con sleep REAL (µA), todo gateado. Receptor SÍ ESP32. "Retomar TX sin tocar el nodo" = ventana RX periódica Class A (ya en branch ECO) + reed/imán. Verificar sleep, no asumirlo.
- **@energia:** dueño de la disciplina "medir sleep primero". LiSOCl2 3.6V + supercap (para el pulso TX) + LDO bajo Iq, JAMÁS boost. Presupuesto real en los docs; recrear escenarios en el GIMAP con el INA219.
- **@comms:** LoRa para emisores (0.33Hz + batería entran sobrados), WiFi solo receptor. MACs para red LDC en `galgas/docs/MAIL_DREYFUS_IT.md`/`SOLICITUD_IT_DREYFUSS.md`.
- **@muestreador:** galga = señal chica → ADC de puente 24-bit (HX711/ADS1232), no el ADC del micro. Implementar/formalizar el shunt-cal (calibración por resistor) y la verificación A=B. Filtro fc≈0.3Hz orden 2 (ya probado en campo, sirve para el golpeteo).
- **@hardware:** BOM del emisor de 1 año = ATmega/STM32L + HX711 + LoRa RA-02 + LiSOCl2 + supercap + LDO + MOSFET de gateo del puente. NO boost. Enclosures: estancas (ya compradas). Relé: solo si aparece caso real.
- **@esquematico:** "la peluda" analógica pendiente → (a) front-end del Wheatstone con shunt-cal (resistor + relay/MOSFET por canal, INA de ganancia de precisión) y gateo del puente; (b) front-end del PIEZO del lab (op-amp O puente de diodos + cap para leer envolvente). Protecciones (TVS).
- **@pcb:** cuando el esquemático cierre → placa del emisor de bajísimo consumo (ruteo con el gateo, supercap cerca del LoRa para el pulso, sin planos que filtren) + placa del receptor ESP32+LoRa (220V). Convergencia UTN: Diseño y Manufactura / Tecnología.
- **@backend:** la telemetría es LIVIANA (0.33Hz + batería) por LoRa → receptor → internet → cloud. Poca data, muchos años. Los 3 modos (campo/lab/ráfaga) definen qué llega.
- **@frontend:** el LAB streamea 1kHz a la PC (NO a la nube). El receptor sirve dashboard local en su AP (`http://192.168.4.1`) además del cloud. Mostrar edad del dato, batería, RSSI, y la comparación A vs B.
- **@diseno:** SCADA del receptor (planta) + vista de la PC para el lab. Que se entienda el estado de cada emisor y su batería de un vistazo.
- **@verificador / @tester:** exigir que el consumo en sleep se MIDA (no se asuma) y que la calibración A=B se PRUEBE con shunt-cal antes de confiar en los datos.

## La lección transversal (para todos)
"Las cuentas son lindas pero la realidad come la batería" = casi siempre el firmware no duerme de verdad o hay un analógico prendido (boost, puente, LED, regulador). **Nada se declara eficiente sin el número del INA219.** Generator ≠ evaluator también en energía.
