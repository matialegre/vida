# Propuesta de Final por Proyecto — Sistemas de Control Industrial

- **Para**: Ing. Alfredo Conde (prof. responsable) — según programa oficial 9-95-683 (plan 1995, programa 2022).
- **De**: Matías Alegre, legajo 19074.

## Propuesta
**SCADA de supervisión del transportador REDLER de Louis Dreyfus** (sistema real que estoy desarrollando vía GIMAP): especificación e implementación de un SCADA con HMI para los nodos de medición de galgas/vibración, donde cada nodo de campo actúa como RTU que reporta por enlace inalámbrico a un gateway y de ahí a la capa de supervisión, con gestión de alarmas. Complementa el TP Integrador 2026 ya entregado (WPLSoft, LOGO!, TSX Micro, S7-200, SLC500, CODESYS) llevándolo a un caso industrial real.

## Cobertura del programa (unidades del programa analítico oficial)
| Unidad | Qué parte del proyecto la cubre |
|---|---|
| **U1** — Automatismos industriales, señales analógicas y digitales, P&ID, especificación de I/O | Especificación de I/O del sistema (señales de galga, vibración, estados) y P&ID simplificado del REDLER |
| **U3** — Diagrama de contactos, implementación en controladores, dispositivos de E/S (sensores/instrumentos) | Lógica de adquisición y alarmas; los sensores/instrumentos reales como dispositivos de entrada |
| **U4** — Armado de proyectos con controladores lógicos programables, alternativas tecnológicas | Análisis de alternativas para el controlador de la solución (PLC comercial vs. controlador dedicado) y justificación técnica de la elegida |
| **U6** — Plataformas de HW y SW disponibles en el mercado | Comparativa de plataformas SCADA/controladores del mercado aplicable al caso |
| **U7** — Definiciones de HMI, elementos, tecnologías de paneles, especificaciones | Diseño y especificación del HMI del sistema (pantallas, jerarquía, señalización) |
| **U8** — Definiciones de SCADA, características, alternativas del mercado, ejemplos de implementación | Núcleo del proyecto: el SCADA especificado e **implementado**, contrastado con alternativas comerciales |
| **U9** — Características de los DCS, diferencias comparativas | Discusión SCADA vs. DCS para este proceso |
| **U10** — Sistemas instrumentados de seguridad: SRS, SIF, SIL | Análisis de qué funciones del sistema serían candidatas a SIF y por qué la supervisión no reemplaza un SIS |
| **U11** — Comunicaciones industriales, protocolos, RTU | Arquitectura de comunicaciones: nodo RTU → gateway → servidor (protocolos usados y su comparación con los industriales clásicos) |

*U2 (lógicas cableadas/arranque de motores) y U5 (IEC 61131) quedaron cubiertas en el TP Integrador de la cursada; las repaso en coloquio si hace falta.*

## Entregables
1. Documento de especificación (I/O, arquitectura, HMI, alarmas) en PDF.
2. **SCADA funcionando en vivo** con datos reales de los nodos de galgas.
3. Presentación interactiva HTML (mismo formato del P3 de neumática).
4. Comparativa de plataformas de mercado con hojas de datos.

## Cronograma tentativo
- **Fines de agosto**: consenso de alcance con la cátedra.
- **Fines de septiembre**: especificación completa (I/O, HMI, comunicaciones) + prototipo del SCADA.
- **Octubre**: sistema corriendo con datos reales de planta (parada de octubre en Dreyfus).
- **Noviembre / llamados de diciembre (9-11 o 14-18)**: demo final + defensa.

**¿Te sirve así o le falta algo?** Si querés que lo implemente además sobre una plataforma SCADA comercial específica para comparar, lo agrego al alcance.
