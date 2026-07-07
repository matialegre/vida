# Dominio: UNIVERSIDAD (agente @utn)

Doc de dominio + bitácora. El agente lo lee al arrancar y lo actualiza al cerrar.

## Estado del dominio (nacimiento, 2026-07-07)
- ⏰ 1-AGO-2026: cierre cuadernillos TP de SCI. TP desarrollado; falta verificación + formato docx + entrega.
- Electrónica Industrial: TP A–F resuelto; falta cierre formal. Extra ganador: `P3_Esquemas_Neumaticos_Interactivo.html` (simulador ISO 1219 interactivo — al profe le gustó; este formato es un diferencial a repetir).
- 2° cuatri (últimas 5): Sist. de Control, Elec. de Potencia, Economía, Inglés 2, Diseño y Manufactura de Circuitos Electrónicos.
- Finales por proyecto (conseguir requisitos con profesores): TC2, Medidas 2, Tecnología, SCI, Elec. Industrial. Sin material en disco de las 3 primeras.
- Proyecto Final 2027: sin definir. Candidatos convergentes: datalogger vibración/galgas (aval GIMAP + Dreyfus) o harvesting piezo aplicado.

## Calendario académico (tabla viva)
| Fecha | Qué | Estado |
|---|---|---|
| 2026-08-01 | Cierre cuadernillos TP SCI | ⚠️ abierto |
| ~2026-08-10 | Arranque 2° cuatri | — |
| fin 2026 | Proyecto de LABORATORIO de Sistemas de Control (cursada) | sin consigna aún |

**Convergencia candidata para el labo de Sistemas de Control:** control de lazo cerrado sobre hardware propio — p.ej. banco de vibración con actuador para excitar la galga/datalogger (sirve a GIMAP como banco de calibración), o control de temperatura de un reefer simulado (sirve a FrioSeguro), o puente H + STM32 que ya tiene material en la carpeta. Validar consigna del laboratorio primero.

## 🛡️ Protocolo anti-"no" de profesores (definido 2026-07-07)
El riesgo de la convergencia: presentar un proyecto real y que el profesor diga "esto no encaja en mi materia". Defensa en 3 capas:
1. **PROPUESTA ANTES DE CONSTRUIR (regla de oro).** Nunca armar el envoltorio académico sin el OK previo. Por cada final-por-proyecto: 1 página de propuesta ("Propongo presentar X, que cubre los temas A, B, C de tu programa, con estos entregables y estas mediciones — ¿te sirve así o le falta algo?"). El profesor que dice "no" a un trabajo terminado dice "sí, pero agregale D" a una propuesta — y ese "agregale D" es LA vuelta de tuerca exacta que pedía, dicha por él.
2. **El proyecto real es el NÚCLEO, no el proyecto académico entero.** Cada materia exige su envoltorio propio: TC2 = análisis formal completo (transferencia, polos, transitorio, simulación vs medición del front-end piezo — el circuito solo es "chico", el análisis lo hace materia); Medidas 2 = metodología metrológica en serio (incertidumbre, trazabilidad, GUM) sobre el datalogger; Tecnología = DFM/materiales/procesos de la PCB; SCI = el SCADA con su ingeniería documentada (P&I, lógicas); Elec. Industrial = instrumentación del REDLER con normas ISA. El agente @utn evalúa CADA propuesta contra el programa de la materia y avisa si falta profundidad ANTES de presentarla.
3. **Plan B por materia, sin drama.** Si un profesor dice "no" igual: (a) versión ajustada con lo que él pida, o (b) final tradicional rindiendo — Matías rinde bien, la convergencia AHORRA tiempo cuando encaja, no es religión. Nunca forzar un encaje que el profesor no compra: un final normal cuesta menos que pelear una propuesta rechazada.
Ventajas a jugar SIEMPRE en la propuesta: cliente real (Dreyfus/GIMAP), aval de un grupo de investigación de la propia UTN, y el formato interactivo que ya gustó (P3). Eso convierte el "no" en "contame más".

## Bitácora
- 2026-07-07 — Agente creado por Claude Fable con mapa completo. Próximo paso: (1) verificar TP SCI contra cuadernillo + pasar a plantilla docx; (2) Matías consigue consignas/reglamento de los 5 finales-por-proyecto.
