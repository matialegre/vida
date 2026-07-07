# Programas Analíticos UTN FRBB — Ingeniería Electrónica

Fuente oficial: https://www.frbb.utn.edu.ar/frbb/info/pages/electronica01.html
PDFs descargados de `https://www.frbb.utn.edu.ar/frbb/info/departamentos/electronica/programas_analiticos/` (y `progr_an23/` para la electiva de PCB).
Descargados y verificados: 2026-07-07. Todos son programas oficiales firmados (planes 1995/2023).

Proyectos de referencia para convergencia:
- **DL**: Datalogger de vibración (Raspberry Pi Pico + LoRa + MPU6050 + piezo)
- **FE**: Front-end analógico piezo / INA333
- **PCB**: PCB del datalogger
- **SCADA**: SCADA de galgas extensiométricas
- **REDLER**: Instrumentación industrial del REDLER (sistema Dreyfus)

---

## 1. Teoría de los Circuitos II (9-95-0432, 4to año, anual, 160 hs)
**Prof.: Oscar A. Rodríguez / Christian Galasso. Programa vigente 2022+.**

Unidades:
1. Modelos matemáticos de sistemas físicos, función de transferencia (5 hs)
2. Respuesta en frecuencia, diagramas de Bode (15 hs)
3. Teoría de cuadripolos (15 hs)
4. Filtros pasivos: atenuadores, k-constante, m-derivadas, Butterworth/Chebyshev/Bessel/Cauer (50 hs)
5. Filtros activos: síntesis con AO, celdas de 2do orden, sensibilidad (25 hs)
6. Sistemas discretos, transformada Z, FIR/IIR (10 hs)
7. Diseño de filtros digitales IIR y FIR (30 hs)

**Régimen de aprobación: LA JOYA.** Además de Ord. 1549 exige:
- Laboratorios 1 al 8 + seminarios con informes.
- **"Cumplir con un trabajo integrador (Laboratorio 9) A CONSENSUAR ENTRE EL ALUMNO Y LA CÁTEDRA durante el dictado, en el que deberá aplicarse los conocimientos teórico-prácticos adquiridos, el cual deberá ser presentado FUNCIONANDO, para su ensayo y aprobación antes de la finalización del ciclo lectivo."**
→ Acepta explícitamente proyecto integrador negociable.

**Convergencia:**
- **FE (piezo/INA333)**: cubre directo U4/U5 — el filtro pasa-banda/anti-aliasing del front-end piezo es un filtro activo de 2do orden (Butterworth/Bessel) con AO: diseño, aproximación, sensibilidad. U1/U2: función de transferencia y Bode del canal analógico completo.
- **DL**: U6/U7 — el procesamiento en el Pico (FFT/filtrado digital de la señal del MPU6050, filtros FIR/IIR anti-vibración) es literalmente la unidad 7. Un datalogger con filtrado digital + front-end con filtro activo cubre el programa de punta a punta y sirve como Laboratorio 9.
- **SCADA/REDLER**: marginal (solo modelado/FT de sensores).

## 2. Medidas Electrónicas II (9-95-0537, 5to año, anual, 160 hs)
**Prof.: Marcelo J. Bruno / Leandro Ortíz. Vigencia 2024–2026.**

Unidades (12):
1. Osciloscopios digitales DSO/DPO
2. Generadores sintetizados, DDS vs PLL (28 hs)
3. Generadores de pulsos y funciones (25 hs)
4. Medidor de distorsión, analizador de Fourier y de espectro (25 hs)
5. Mediciones de tiempo y frecuencia, frecuencímetros (9 hs)
6. Mediciones en amplificadores; **mediciones de un amplificador operacional: offset, bias, BW, slew rate, CMRR** (25 hs)
7. Analizador de redes, parámetros S
8. Reflectometría
9. Potencia en RF (10 hs)
10. Analizadores lógicos (8 hs)
11. EMC/EMI (3 hs)
12. **Automatización de las mediciones y medición de parámetros no eléctricos avanzados: transductores mecánicos, térmicos, ópticos, acústicos, magnéticos** (5 hs)

**Régimen:** solo remite a Ordenanza 1549 (no exige trabajo integrador propio; margen para negociar labs).

**Convergencia:**
- **DL**: U12 al 100% — un datalogger de vibración ES "automatización de mediciones + medición de parámetros no eléctricos (transductores mecánicos)". Además U4: análisis espectral de la vibración (FFT en el Pico = analizador de Fourier casero).
- **FE**: U6b — caracterizar el INA333 (offset, CMRR, BW, ruido) es exactamente el laboratorio de mediciones de AO.
- **REDLER/SCADA**: U12 (transductores + automatización) y U11 (EMI en ambiente industrial).

## 3. Tecnología Electrónica (9-95-0540, 5to año, anual, 160 hs)
**Prof.: Marcelo J. Bruno / Walter Correa. Vigencia 2024–2026.**

Unidades (11):
1. Materiales eléctricos; **d) Materiales piezoeléctricos: cristales, cortes, modos de vibración, circuito equivalente** (6 hs)
2. Materiales magnéticos (6 hs)
3. Inductores (30 hs)
4. Transformadores (35 hs)
5. Resistores; incluye **strain gages (galgas)**, termistores, varistores (15 hs)
6. Capacitores (15 hs)
7. Normas, fallas y **confiabilidad** (7 hs)
8. Otros pasivos: **componentes piezoeléctricos (cristales y resonadores)**, electromecánicos, **pilas y baterías** (20 hs)
9. **Tecnología constructiva: blindajes y puesta a tierra, CAD/CAM, montaje superficial** (10 hs)
10. Soldadura (7 hs)
11. **Tecnología microelectrónica: circuitos impresos, tipos, niveles de interconexión** (7 hs)

**Régimen:** remite a Ordenanza 1549 (sin trabajo integrador explícito, negociable).

**Convergencia:**
- **FE**: U1d — el sensor piezo (circuito equivalente, modos de vibración) es contenido explícito. U5: galgas (strain gage) están nombradas.
- **PCB**: U9 + U11 — blindaje, puesta a tierra, CAD/CAM, SMT, circuito impreso: el PCB del datalogger cubre estas unidades. U8e: dimensionar la batería del nodo LoRa.
- **SCADA de galgas**: U5 (strain gages) + U7 (confiabilidad).
- **REDLER**: U7 (fallas/confiabilidad, mantenimiento) aplica al análisis del sistema Dreyfus.

## 4. Sistemas de Control (5to año, anual, 128 hs)
**Prof.: Patricia Baldini / Pablo Fucile. Programa 2022.**

Temas:
1. Introducción: lazo abierto/cerrado, **relevancia de los sensores** (—)
2. Modelado de sistemas dinámicos (mecánicos, eléctricos, electromecánicos); AO en control
3. Respuesta dinámica, PID, Ziegler-Nichols, wind-up
4. Lugar de las raíces
5. Análisis y diseño en frecuencia (Bode, Nyquist, Lead/Lag, PID)
6. Variables de estado, observadores
7. **Sistemas de control en tiempo discreto: muestreo, aliasing, PID discreto, implementación algorítmica-digital**

**Régimen:** el PDF no detalla método de evaluación propio (remite al estándar); no exige proyecto, pero T7 se presta a implementación en microcontrolador.

**Convergencia:**
- **DL**: T7 — selección de período de muestreo y aliasing del MPU6050/piezo es contenido directo; PID discreto implementable en el Pico como extensión.
- **SCADA/REDLER**: T1–T3 — modelado del proceso (REDLER como sistema electromecánico), lazos de control con sensores de galga; el SCADA es la capa de supervisión de estos lazos.
- **FE/PCB**: marginal.

## 5. Electrónica Industrial (electiva, 9-95-0646, cuatrimestral, 64+16 hs)
**Prof.: Alfredo Conde. Programa 2022. "Denominación real: INSTRUMENTACIÓN INDUSTRIAL".**

Unidades (12): 1) Procesos/automatismos, P&ID, normas ISA; 2) Fluidos y variables de proceso; 3) Componentes medición/control/elementos finales; 4) **Transmisores de presión, temperatura (RTD/TC/termistor), caudal, nivel — hojas ISA, montaje en campo, puesta en marcha** (15 hs); 5) Controladores, lazos, alarmas, SIS (6 hs); 6) Válvulas de control (12 hs); 7) Analítica y cromatografía (6 hs); 8) **Calibraciones y confirmación metrológica** (4 hs); 9) Neumática/hidráulica; 10) **Redes de instrumentación: fieldbus, Profibus, HART, CAN, WirelessHART e ISA100** (4 hs); 11) Áreas clasificadas, antideflagrante (4 hs); 12) Roles del instrumentista, mantenimiento, comisionado.

**Régimen:** Ord. 1549; clases prácticas con material industrial real + **visitas a plantas del Polo Industrial de Bahía Blanca**.

**Convergencia (la materia más REDLER-céntrica):**
- **REDLER**: U1 (P&ID del Dreyfus), U4 (transmisores, montaje en campo, puesta en marcha), U5 (alarmas), U8 (calibración), U12 (mantenimiento/roles) — la instrumentación del REDLER cubre más de la mitad del programa tal cual.
- **DL**: U10 — el enlace LoRa del datalogger dialoga directo con "sistema wireless, WirelessHART/ISA100"; el monitoreo de vibraciones aparece nombrado en los objetivos ("Monitoreo de Vibraciones").
- **SCADA**: U5 (estrategias de control, alarmas, gestión de alarmas).

## 6. Sistemas de Control Industrial (electiva, 9-95-683, cuatrimestral, 48+32 hs)
**Prof.: Alfredo Conde. Programa 2022.**

Unidades (11): 1) Automatismos, señales, P&ID, I/O; 2) Lógicas cableadas, arranque de motores; 3) Diagrama de contactos (ladder), PLC; 4) **Armado de proyectos con PLC** (13 hs); 5) **IEC 61131** (10 hs); 6) Plataformas HW/SW del mercado; 7) **HMI** (4 hs); 8) **SCADA: definiciones, características, alternativas del mercado, ejemplos de implementación** (4 hs); 9) DCS (4 hs); 10) Sistemas instrumentados de seguridad SIS/SIL; 11) **Comunicaciones industriales, protocolos, RTU** (4 hs).

**Régimen:** Ord. 1549; prácticas en laboratorio con PLCs y simuladores; visitas a plantas.

**Convergencia:**
- **SCADA de galgas**: U7+U8 literal — definir HMI y SCADA, especificarlo e implementarlo. U11: el protocolo entre nodos (LoRa→gateway→SCADA, Modbus/MQTT como RTU) cubre comunicaciones industriales.
- **REDLER**: U1–U4 — el automatismo del REDLER (arranque de motores, ladder, PLC) más el SCADA de supervisión = proyecto integrador natural de la materia.
- **DL**: U11 (el datalogger como RTU de campo que reporta al SCADA).

## 7. Electrónica de Potencia (9-541, anual, 64+64 hs)
**Prof.: Claudio F. Rezzuti / Leandro Ortiz. Vigencia 2020–2025.**

Unidades (9): 1) Fundamentos, factor de potencia, distorsión; 2) Rectificadores no controlados; 3) Rectificación controlada (tiristores); 4) Apagado forzado; 5) **Fuentes conmutadas: buck, boost, buck-boost, Cúk, flyback, forward** (20 hs); 6) Inversores DC-AC, PWM; 7) Control de motor de CC; 8) **Control de motor de alterna: variadores V/f, control vectorial** (14 hs); 9) Calidad de energía, armónicas, EMI.

**Régimen (detallado en el PDF):** promoción con promedio ponderado ≥6 entre 3 parciales teórico-prácticos + evaluación oral final; laboratorios de diseño-armado-medición (fuente conmutada step-down, disparo de tiristores, control de velocidad de motor CC). No contempla proyecto integrador libre, pero los labs son de diseño.

**Convergencia:**
- **DL/PCB**: U5 — la fuente del datalogger (buck/boost desde batería, manejo de energía del nodo LoRa) es la unidad más pesada tras rectificación; Laboratorio 1 (fuente conmutada) alineable con la alimentación del datalogger.
- **REDLER**: U8 — los variadores de frecuencia de los motores del REDLER son contenido directo; U9: calidad de energía y EMI en planta (fuente de la vibración eléctrica que mide el datalogger).
- **SCADA/FE**: marginal.

## 8. Proyecto Final (9-650, cuatrimestral, 32+96 hs)
**Prof.: Guillermo Friedrich / Adrián Laiuppa. Vigencia 2020–2025.**

Unidades: I) **Elección del producto/sistema** — categorías admitidas: desarrollos originales, mejoras de equipos, investigación aplicada, **"desarrollos específicos para empresas públicas y/o privadas"**, equipos para la Facultad; II) Aspectos técnico-económicos; III) Anteproyecto y factibilidad; IV) Planificación (Gantt/PERT, MS-Project); V) Legislación; VI) **Desarrollo de ingeniería, implementación y ensayos** (88 hs — el grueso).

**Régimen:** grupos de hasta 3; exposiciones de propuesta/avance/final; el proyecto DEBE incluir diseño y desarrollo de hardware/software/simulación.

**Convergencia: el proyecto REDLER/Dreyfus entra perfecto como "desarrollo específico para empresa privada".** El paquete completo (datalogger de vibración + front-end + PCB + SCADA de galgas aplicado al REDLER) tiene la envergadura exacta que pide la cátedra: hardware + software + planificación + evaluación económica. Correlativas fuertes (para cursar: TD II, ME I, MIE, EA II aprobadas; TD III, ME II, EA III cursadas).

## 9. Introducción al Diseño y Manufactura de Circuitos Impresos (electiva, cuatrimestral, 64 hs cátedra)
**Prof.: Adrián Laiuppa. Vigencia 2025–2030. (La "Diseño y Manufactura de Circuitos Electrónicos" buscada — existe con este nombre, plan 2023.)**

Unidades: 1) Estado del arte, tipos de PCB y montaje; 2) **Factores de diseño: DFM, EMC, normas** (10 hs); 3) Herramientas EDA/CAD/CAM; 4) Dibujo del esquema eléctrico, librerías, ERC; 5) **Dibujo del circuito impreso: reglas, DRC, ruteo, DFM** (10 hs); 6) **Casos de estudio: TRABAJO FINAL PRESENTADO POR LOS ALUMNOS, evaluando diseño y manufacturabilidad** (20 hs).

**Régimen: acepta proyecto — la Unidad 6 ES un trabajo final de diseño de PCB propio.**

**Convergencia:**
- **PCB del datalogger**: cobertura total, unidad por unidad — esquema (U4), layout con DFM (U5), y el PCB terminado como trabajo final (U6). Es la materia donde el PCB del datalogger rinde al 100% sin adaptación.
- **FE**: U2 — EMC y diseño analógico/digital mixto del front-end INA333 en la misma placa.

## 10. (Bonus) Medidas Electrónicas I (9-95-0435, 4to año, anual)
**Prof.: Alfredo Conde / Martin Troilo. Vigencia 2025.** Errores e incertidumbre, métodos de medición, puentes (Wheatstone/Kelvin — base de galgas), fuentes de señal, instrumentos digitales, osciloscopios, **U10: acondicionamiento de señales y medición de parámetros no eléctricos (sensores, muestreo, amplificación, filtrado; temperatura/presión/desplazamiento)**, interferencias modo común/normal (relevante INA333). Régimen: Ord. 1549.
**Convergencia:** FE (puente de galgas + amplificación + rechazo de modo común) y SCADA (U5 puentes, U10 acondicionamiento).

---

## No encontrados online / pendientes de aula virtual
- Ninguno de los objetivos falló: los 9 programas objetivo existen y se descargaron.
- Ojo: los archivos de `programas_analiticos/` corresponden al plan 1995; el plan 2023 (carpeta `progr_an23/`) por ahora solo publica materias de los primeros años + electivas nuevas (la de PCB vino de ahí). Si Matías cursa plan 2023 en materias superiores, esas versiones aún no están publicadas y habrá que pedirlas en el aula virtual.
- También disponibles en el sitio (no descargados): `analisis_asignatura/*.pdf` (planificaciones por docente, con cronogramas y labs del año en curso) — útiles para negociar el trabajo integrador con cada cátedra.

## Las 3 conclusiones clave para la convergencia
1. **Teoría de los Circuitos II es la única materia que EXIGE por programa un trabajo integrador consensuado con la cátedra y presentado funcionando (Laboratorio 9)** — el front-end piezo con filtros activos + filtrado digital FIR/IIR en el Pico calza exacto. Es el punto de entrada más seguro para convertir el datalogger en nota.
2. **El ecosistema REDLER/Dreyfus mapea casi 1:1 sobre las dos electivas de Conde** (Electrónica Industrial = instrumentación de campo, transmisores, calibración, WirelessHART; Sistemas de Control Industrial = PLC + HMI + SCADA + comunicaciones). Cursándolas, el trabajo en Dreyfus se convierte en material de cátedra, y Conde también es titular de Medidas I — un solo docente concentra tres materias donde el proyecto rinde.
3. **Proyecto Final admite explícitamente "desarrollos específicos para empresas privadas"** con 88 hs de desarrollo de ingeniería: el sistema completo de monitoreo de vibración del REDLER (datalogger + front-end + PCB + SCADA) tiene la envergadura y las categorías exactas; además la electiva de PCB (Laiuppa, que es también profesor de Proyecto Final) toma el PCB del datalogger como trabajo final de la Unidad 6 — el mismo hardware suma en dos materias sin duplicar esfuerzo.
