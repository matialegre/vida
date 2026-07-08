# Propuesta de Final por Proyecto — Tecnología Electrónica

- **Para**: Mg. Ing. Marcelo J. Bruno (prof. responsable) / Ing. Walter Correa (docente auxiliar) — según programa oficial 9-95-0540 (plan 1995, vigencia 2024–2026).
- **De**: Matías Alegre, legajo 19074.

## Propuesta
**Ingeniería de componentes y construcción del PCB de un datalogger de vibración de desarrollo propio** (proyecto real GIMAP/Louis Dreyfus): estudio tecnológico de cada componente crítico — sensor piezoeléctrico, galgas extensiométricas, resonador del micro, batería del nodo — más el diseño constructivo de la placa (blindaje, puesta a tierra, CAD, SMT, soldadura) y el análisis de confiabilidad del conjunto para operar en planta.

## Cobertura del programa (unidades del programa analítico oficial)
| Unidad Temática | Qué parte del proyecto la cubre |
|---|---|
| **UT1d** — Materiales piezoeléctricos: cristales, cortes, modos de vibración, circuito equivalente | Estudio del sensor piezo del datalogger: circuito equivalente medido, modo de vibración, especificaciones |
| **UT5** — Resistores; no lineales y strain gage | Galgas extensiométricas del sistema de medición de deformación: características, comportamiento térmico, especificación |
| **UT6** — Capacitores: circuito equivalente, factor de disipación vs. frecuencia | Selección justificada de los capacitores del front-end analógico y del desacople (tipos, ESR, comportamiento en frecuencia) |
| **UT7** — Normas, especificaciones, fallas y confiabilidad | Análisis de confiabilidad del datalogger (régimen de fallas, disposición serie de la cadena de medición, eficiencia del mantenimiento) para servicio industrial |
| **UT8a/e** — Componentes piezoeléctricos (cristales y resonadores) y pilas y baterías: capacidad, régimen de carga/descarga, vida útil | Resonador/cristal del reloj del microcontrolador; dimensionamiento de la batería del nodo LoRa a partir del perfil de consumo medido (deep sleep) |
| **UT9** — Tecnología constructiva: blindajes y puesta a tierra, CAD/CAM, montaje superficial | Diseño del PCB: estrategia de tierras analógica/digital, blindaje del canal del piezo, flujo CAD y decisión THT/SMT |
| **UT10** — Soldadura: métodos, soldabilidad, influencia sobre la confiabilidad | Proceso de armado de la placa, inspección y su impacto en la confiabilidad del equipo |
| **UT11** — Tecnología microelectrónica: circuitos impresos, tipos, niveles de interconexión | Especificación del impreso (capas, niveles de interconexión, limitaciones del proceso de fabricación elegido) |
| UT2/UT3/UT4 — Materiales magnéticos, inductores, transformadores | Cobertura menor: ferrites/choques de filtrado de alimentación; el grueso lo preparo para el coloquio teórico |

## Entregables
1. Informe tecnológico en PDF: hoja de justificación de cada componente crítico + análisis de confiabilidad.
2. Mediciones: circuito equivalente del piezo, perfil de consumo/batería, verificación post-soldadura.
3. **El PCB armado y funcionando** como pieza central de la defensa.
4. Presentación interactiva HTML con esquemático, layout y fotos del proceso constructivo.

## Cronograma tentativo
- **Fines de agosto**: consenso de alcance con la cátedra.
- **Fines de septiembre**: estudio de componentes (UT1d, UT5, UT6, UT8) con mediciones.
- **Fines de octubre / principios de noviembre**: PCB fabricado, armado y verificado (UT9–UT11) + análisis de confiabilidad (UT7), con evidencia de uso en campo.
- **Llamados de diciembre (9-11 o 14-18)**: informe final + placa funcionando + defensa.

**¿Te sirve así o le falta algo?** Si la cátedra quiere más peso en magnéticos (UT2–UT4) puedo sumar el estudio del transformador/inductor de la etapa de alimentación.
