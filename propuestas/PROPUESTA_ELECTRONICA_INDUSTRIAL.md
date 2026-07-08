# Propuesta de Final por Proyecto — Electrónica Industrial (Instrumentación Industrial)

- **Para**: Ing. Alfredo Conde (prof. responsable) — según programa oficial 9-95-0646 (plan 1995, programa 2022).
- **De**: Matías Alegre, legajo 19074.

## Propuesta
**Ingeniería de instrumentación del transportador REDLER de Louis Dreyfus (caso real, trabajo que estoy haciendo vía GIMAP)**: P&ID de la instalación, especificación de los puntos de medición (deformación por galgas y vibración), hojas de especificación estilo ISA, plan de calibración y arquitectura de comunicación inalámbrica de los nodos de campo comparada contra WirelessHART/ISA100. Todo documentado como lo haría un instrumentista, con la instalación real de la parada de planta de octubre como evidencia de campo.

## Cobertura del programa (unidades del programa analítico oficial)
| Unidad | Qué parte del proyecto la cubre |
|---|---|
| **U1** — Procesos/automatismos, normas y simbología, diagramas P&ID, el profesional instrumentista | P&ID del REDLER con simbología ISA e identificación de lazos de medición |
| **U3** — Componentes de la instrumentación según su función (medición/control/elementos finales) | Arquitectura del sistema: sensores (galgas, acelerómetro), transmisores (nodos), supervisión |
| **U4** — El instrumento como caja negra, acondicionamiento, hojas ISA, montaje en campo, puesta en marcha | Hoja de especificación de cada punto de medición, detalle de montaje en campo sobre el REDLER y procedimiento de puesta en marcha (el de la parada de octubre) |
| **U5** — Controladores, estrategias, alarmas y gestión de alarmas, sistemas instrumentados de seguridad | Esquema de alarmas por umbral de deformación/vibración y su gestión; discusión FIS aplicada al caso |
| **U8** — Definiciones y normas, confirmación metrológica, calibración, exactitud/precisión/repetibilidad | Procedimiento de calibración y verificación de los canales de galga (patrón, verificación en campo y taller) |
| **U10** — Redes de comunicación de instrumentación: fieldbus, HART, wireless, WirelessHART e ISA100 | Comparativa fundada: enlace LoRa propio vs. WirelessHART/ISA100 (topología, consumo, coexistencia), con hojas de datos de fabricantes |
| **U12** — Roles del profesional: mantenimiento, ingeniería, precomisionado y comisionado | Informe de comisionado y plan de mantenimiento del sistema instalado |

*Las unidades 2, 6, 7, 9 y 11 (fluidos, válvulas, analítica, neumática, áreas clasificadas) no son el eje del proyecto; quedan para el coloquio teórico si la cátedra lo considera.*

## Entregables
1. Carpeta de ingeniería en PDF: P&ID, hojas de especificación, plan de calibración, informe de comisionado.
2. Evidencia de campo: fotos/mediciones de la instalación real en la planta.
3. Presentación interactiva HTML (el formato del TP de neumática) con la arquitectura navegable.
4. Demo del nodo de campo funcionando en vivo.

## Cronograma tentativo
- **Fines de agosto**: consenso de alcance con la cátedra.
- **Fines de septiembre**: P&ID + hojas de especificación + plan de calibración (pre-parada).
- **Octubre**: instalación y puesta en marcha en la parada de planta → evidencia de campo.
- **Noviembre / llamados de diciembre (9-11 o 14-18)**: carpeta completa + presentación final.

**¿Te sirve así o le falta algo?** Si preferís que profundice alguna unidad (por ejemplo válvulas o áreas clasificadas) la sumo al coloquio.
