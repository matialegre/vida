# PARTE DEL DÍA — GIMAP 2026-07-08 (dictado por Matías en campo)

Los proyectos del GIMAP se separaron en **variantes distintas del datalogger**, cada una con requisitos propios. Capturado textual + análisis técnico del equipo.

## Proyecto 1 — Datalogger de LABORATORIO (alta fidelidad)
- **Comunicación:** WiFi (se engancha a la red del lugar).
- **Muestreo:** MPU a **1 kHz** (6 ejes).
- **Ahorro:** NINGUNO. Batería pelada + **botón on/off que corta la batería/alimentación** (interruptor físico, no sleep).
- **Almacenamiento:** NO quiere SD → los datos van a una **COMPUTADORA** (streaming a PC). El destino es la notebook, no una tarjeta.
- **EXTRA — canal PIEZOELÉCTRICO:** el de lab también mide un piezo. Dos formas de acondicionar (a decidir):
  - (a) señal tratada por un **amplificador operacional**, o
  - (b) **rectificada con puente de diodos + capacitor** y leer el voltaje (envolvente).
- → Es el `modo lab` que ya está flasheado (streaming WiFi 1kHz 6 ejes). Falta el frontend del piezo (dominio @esquematico).

## Proyecto 2 — Datalogger para PUENTES y MOLINO EÓLICO
- **Muestreo:** NO necesita frecuencia alta del MPU.
- **Flujo de operación:** el micro arranca → **mide y TRANSMITE** un rato (10/15/20 min, hasta 1 hora) para que puedan ver los datos en vivo → **botón "listo"** → pasa a modo "solo guardar en SD, no transmitir más" hasta que lo vayan a buscar.
- **⚠️ PROBLEMA ABIERTO (Matías no encontró la forma):** cómo hacer que **RETOME la transmisión** una vez que dejó de transmitir, en un lugar donde **no se puede volver a tocar nunca más**. Necesita reactivar la TX remotamente. → **SOLUCIÓN PROPUESTA abajo.**

## Proyecto 3 — DREYFUS / galgas (MUY IMPORTANTE)
- **Física confirmada en campo:** el eje gira a **20 RPM**, pero el **golpeteo de las cadenas es 0.33 Hz**. → Nyquist: con muestrear a unos pocos Hz sobra. **LoRa cubre perfectamente** transmitir ese dato + telemetría de batería.
- **Sensor:** puente de **Wheatstone** (galga).
- **Requisito duro:** la batería debe **durar UN AÑO**.
- **Encrucijada de Matías:** el LoRa necesita 3.3V. ¿Usar **ATmega328P + LoRa** (con step-down para el LoRa) o **Pico + LoRa**? Si usa ATmega cree que necesita una fuente step-down mínima. → **RECOMENDACIÓN abajo.**

## Proyecto 4 — (a confirmar con Matías)
Matías dijo "cuatro proyectos" pero detalló tres. El 4º probablemente sea el **cosechador de energía / harvesting piezo** (GIMAP-relacionado, ver repo cosechador) o una variante más. CONFIRMAR.

---

# 🔧 Respuestas del equipo a las dos encrucijadas

## R1 — Cómo RETOMAR la transmisión sin poder tocar el nodo (Proyecto 2)
El error conceptual es "dejar de transmitir = dejar de escuchar". La solución: **el nodo nunca deja de ESCUCHAR, aunque deje de TRANSMITIR.**
- **Software (el que ya diseñamos): ventana RX periódica tipo LoRaWAN Class A.** El nodo en modo "solo SD" igual **despierta cada N minutos, abre una ventana corta de RX** para oír si le mandan el comando "retomá transmisión", y vuelve a dormir. Cuesta poquísima energía (la ventana es de ms). Cuando volvés a estar en rango LoRa, le mandás `transmitir on` y retoma. **Esto es exactamente el ECO-LoRa que ya está en el branch `nocturno/local-2026-07-07-ina219-ecolora`** (ventana RX garantizada + failsafe). El "botón listo" no apaga la radio: la pasa a modo escucha-periódica.
- **Hardware (a prueba de todo): reed switch + imán.** Un sensor magnético sellado dentro del gabinete: pasás un **imán por fuera** (sin abrir ni tocar la electrónica) y el nodo despierta y retoma TX. Robusto para "no se toca nunca más" — no hay botón que se moje ni conector que se corroa. Cuesta centavos (ya tenés 10 reed switches en stock). Combinable con la ventana RX.
- **Recomendación:** las dos. Ventana RX para reactivación remota por LoRa + reed/imán como respaldo físico infalible.

## R2 — ATmega328P vs Pico + LoRa, para 1 AÑO de batería (Proyecto 3 Dreyfus)
**Ganador claro: ATmega328P.** El Pico (RP2040/RP2350) tiene corriente de sleep alta y MicroPython no hace deep sleep fino (ya lo comprobamos) → imposible 1 año. El ATmega328P bare duerme a **<1 µA** (power-down + WDT). Para 1 año, ATmega.

**Y OJO — la encrucijada del step-down tiene truco:**
- **NO necesitás un step-down (buck).** El ATmega328P corre **directo a 3.3V** si lo clockeás a **8 MHz** (el interno; el 16MHz sí pide 5V, el 8MHz@3.3V anda perfecto). Entonces **un solo riel de 3.3V alimenta el ATmega Y el LoRa** — no hay que convertir entre dos voltajes.
- **La batería correcta para 1+ año: LiSOCl2 (cloruro de tionilo), 3.6V** — tipo Saft LS14500 (tamaño AA, 2.6Ah, autodescarga bajísima, la batería de los IoT de años). El SX1276/RA-02 tolera hasta 3.9V → **con 3.6V andás casi directo**; si querés 3.3V exactos, un **LDO de ultra-bajo Iq** (MCP1700 ~1.6µA, o TPS7A02 ~25nA), NO un buck.
- **Clave de bajo consumo:** a corrientes de µA en sleep, **un buck (step-down) es PEOR que un LDO de bajo Iq** — el buck tiene corriente quiescente que se come la batería durmiendo. Regla: para nodos de µA, LDO de bajo Iq o directo, jamás un step-down conmutado.
- **Arquitectura Dreyfus recomendada:** LiSOCl2 3.6V → (LDO bajo Iq 3.3V opcional) → ATmega328P @8MHz + RA-02/SX1276. INA amp para el Wheatstone (bajo consumo, alimentado por gate cuando muestrea). Deep sleep entre muestras a pocos Hz. TX LoRa periódica del valor + batería. **1 año es totalmente alcanzable así.**

Dominios: @firmware (ATmega bare-metal, no MicroPython), @hardware (LiSOCl2 + LDO, no buck), @energia (presupuesto), @esquematico (front-end Wheatstone + piezo del lab).
