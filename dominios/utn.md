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

## ⛔ REGLA DURA de convergencia (Matías, 2026-07-08)
**Las materias de Conde (Sistemas de Control Industrial + Electrónica Industrial/Instrumentación) exigen PLC + INSTRUMENTO INDUSTRIAL real. JAMÁS proponerle un proyecto basado en microcontroladores (ESP32/Pico/datalogger/galgas) — lo rechaza.**
- **Electrónica Industrial** → lazo de instrumentación: transmisor real (Rosemount 3051, 4-20mA/HART, PACTware) + PLC del lab. Calibración zero/span, ISA, LRV/URV/Span.
- **SCI** → lazo de control cerrado sobre PLC real (WPLSoft/S7-200/SLC500/TSX) + instrumento 4-20mA + SCADA/HMI. Extensión natural del TP Integrador.
- El REDLER/Dreyfus sirve solo como CONTEXTO/experiencia de campo, no como el trabajo entregado.
- El datalogger/galgas (micros) va SOLO a: TC2 (front-end analógico), Medidas 2 (metrología), Tecnología (PCB), Proyecto Final. NO a Conde.
Las propuestas corregidas están al final de `propuestas/PROPUESTA_SCI.md` y `PROPUESTA_ELECTRONICA_INDUSTRIAL.md` (sección "PROPUESTA CORREGIDA").

## 🎯 Dirección elegida para los finales de Conde (Director, 2026-07-08)
**Base = LABORATORIO de la UTN, NO una empresa.** Menos riesgo, sin dependencia de terceros, Conde es dueño del lab, fierro ya disponible. La empresa de Bahía queda como garnish OPCIONAL (calibrar 1 instrumento real allá si un contacto dice sí fácil), nunca como núcleo del que dependa el final.
**Jugada maestra: proponerle a Conde MONTAR/INTEGRAR el laboratorio de PLCs** como el proyecto — cubre las DOS materias (Elec.Ind = lazo de instrumento con transmisor+calibración; SCI = control+SCADA+PLCs en red), le deja algo permanente a la cátedra (Conde lo ama → mejor vínculo → firma el Proyecto Final), cero plata, cero coordinación externa. Confirmar alcance con Conde en el mensaje de reserva de lab.

## Bitácora
- 2026-07-13 (c) — **A.2 y B.1.b Elec. Industrial CERRADOS:** los 8 diagramas P&I ISA ya dibujados (`EI_A2_*.png`: PIC/TIC/LIC/LIC-cascada × electrónico/neumático) quedaron embebidos como base64 con epígrafes A.2.1–A.2.4 en ambos HTML y en el docx (verificado: 13 imágenes insertadas, 8 epígrafes A.2). Cuadro de presión B.1 → 6×6 (filas de partida mmHg e inH₂O calculadas en Python) + 2 correcciones de factores preexistentes: 1 bar→401,46 inH₂O (decía 401,86) en el HTML fuente, y kg/cm²→psi 14,223 (decía 14,696, que es el factor de atm) en el HTML principal. Docx regenerado 17:01 (999 KB) y verificado con python-docx. Checklist: 18✅·2⚠️·1❌ — Secciones A y B COMPLETAS; pendientes solo E.a (HART en laboratorio) y FMT.2 (confirmar formato de entrega con Conde).
- 2026-07-13 (b) — **A.1 Elec. Industrial INTEGRADO y ENTREGABLE regenerado:** los 6 listados reales del P&ID (152 filas: 50 instrumentos + 12 PSV, 25 E/S, 7 lazos, 16 alarmas, BMS/ESD/DCS, 17 equipos + 12 límites de batería) quedaron en `TP_Electronica_Industrial.html` (debajo de cada método, títulos "Aplicación al P&ID I-GIO-730-102248-PL-M-133") y en `Resolucion_Cuadernillo_TP_EI.html` (fuente del docx); `TP_Cuadernillo_EI_Alegre_19074.docx` regenerado y verificado con python-docx (tags reales presentes, 20 tablas). Los 11 ⚠ del md quedaron como 5 notas al pie "(a confirmar en revisión con cátedra)"; A.1 pasó a ✅ en el checklist. De la Sección A falta SOLO A.2: los 8 diagramas P&I dibujados con símbolos ISA (PIC/TIC/LIC/LIC-cascada × electrónico/neumático — los PNG EI_A2_*.png ya existen en la carpeta, falta embeberlos).
- 2026-07-13 — **A.1 Electrónica Industrial: listados del P&ID real EXTRAÍDOS.** Fuente: `Downloads\Diagrama de P&ID nro 0.pdf` (I-GIO-730-102248-PL-M-133, CONFORME A OBRA — skid de regeneración/inyección de MEG: separador PV-17.29 A, calentador HR-15.02 A con BMS/quemador Q-5101, filtros, bombas dosificadoras PM-18.14). Método: PDF vectorial → 12 mosaicos 6x + 5 zooms de verificación 8-10x, transcripción tag por tag sin inventar ninguno. Entregable: `UNIVERSIDAD UTN\electronica industrial\A1_Listados_PID.md` con los 6 listados en el formato del TP (50 instrumentos + 12 PSV con seteo, 25 E/S, 3 lazos + 4 PCV, 16 alarmas, BMS+ESD completos, 17 equipos, 12 límites de batería) + 11 pendientes ⚠ VERIFICAR con coordenada de grilla. Próximo paso: volcar las tablas al HTML del TP (reemplazan los ejemplos genéricos de la sección A.1) y chequear los 11 pendientes con zoom manual.
- 2026-07-08 — Decisión: finales de Conde vía LAB (montar/integrar PLCs), no empresa. Empresa = opcional.
- 2026-07-07 — Agente creado por Claude Fable con mapa completo. Próximo paso: (1) verificar TP SCI contra cuadernillo + pasar a plantilla docx; (2) Matías consigue consignas/reglamento de los 5 finales-por-proyecto.

## 🔑 CORRECCIÓN CLAVE — chat real con Conde (2026-07-08, del historial de WhatsApp)
1. **NO HAY FECHA DE ENTREGA DURA.** Conde (6-jul): "me olvidé de ponerle fecha... una vez que completen el TP, lo suben y ahí les paso el cursado". → El "1-ago" del calendario NO es deadline de Conde. Flujo: completar → subir a plataforma → Conde revisa → cursado. Menos presión, pero hay que COMPLETARLO bien igual.
2. ⚠️ **La evaluación es ORAL/presentación INDIVIDUAL en clase** (Conde 22-jun): refinó las preguntas CONTRA la IA; hay que "explicar el desarrollo de los problemas en clase, con medios propios". → El cuadernillo generado es PUNTO DE PARTIDA y GUÍA DE ESTUDIO; Matías DEBE entender y poder defender cada problema. No subir sin estudiar.
3. **HART (E.a) — software exacto** (Conde 15-may): PactWare 5.0 o 4.1 + librería Pepperl&Fuchs (o Vega) + driver módem HART Viator + DTM genérico HART. Todo gratis. INSTALAR EN NOTEBOOK = escritorio (se puede YA); configurar instrumento real = lab. "El hart lo tenemos en el laboratorio".
4. **A.1 (P&ID):** Conde compartió links Emerson (caudal + dimensionamiento de placas orificio "como les mostré en clase"). El P&ID/datos de A.1 PUEDEN estar ya en material de clase — Matías revisa apuntes/aula virtual antes de pedirlo.
5. Clases a veces por Zoom (utn.zoom.us). Instancias evaluatorias ya habilitadas desde 22-jun.
CONSECUENCIA: baja la urgencia de deadline; SUBE la importancia de que Matías ESTUDIE el cuadernillo para defenderlo. El mensaje a Conde ahora es para: coordinar lab (HART) + pedir P&ID si no lo tiene + confirmar formato de entrega.

## Avances 2026-07-10 (Matías)
- ✅ Mensaje a Conde ENVIADO. **Reunión LUNES ~18:15 en la universidad CON Conde**: (1) terminar/entregar el cuadernillo (EI + lo que sea del lab), (2) **hablar del PROYECTO a hacer en el LABORATORIO** (la propuesta de armar/integrar el lab de PLCs). Ir con notebook + PactWare instalado por si se hace el HART.
- ✅ Aclaración: NO hay que "estudiar" el cuadernillo — solo entregarlo (la defensa oral se verá, pero el TP se entrega). Menos carga de la pensada.
- Próximo paso @utn: preparar para el lunes la propuesta del proyecto de laboratorio (1 página, ver PROPUESTA_SCI/EI corregidas) para presentarle a Conde en persona.

## Avance 2026-07-13 (nocturno)
- ✅ TP SCI Sección A: dibujados los 3 diagramas P&I faltantes (Fig. A.1 LIC-101 domo+LALL+TON 10s, Fig. B.1 TSH-201 on/off, Fig. C.1 PIC-301+PSH/PSL) en SVG inline al estilo del Lazo D; HTML validado y verificado en navegador; backup TP_Sistema_Control_Industrial.BACKUP-2026-07-13.html.
