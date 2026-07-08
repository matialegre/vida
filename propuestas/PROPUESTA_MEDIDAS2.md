# Propuesta de Final por Proyecto — Medidas Electrónicas II

- **Para**: Mg. Ing. Marcelo J. Bruno (prof. responsable) / Ing. Leandro Ortíz (docente auxiliar) — según programa oficial 9-95-0537 (plan 1995, vigencia 2024–2026).
- **De**: Matías Alegre, legajo 19074.

## Propuesta
**Caracterización metrológica completa de un datalogger de vibración de desarrollo propio** (Raspberry Pi Pico + MPU6050 + sensor piezo + front-end INA333 + enlace LoRa, en uso real en un proyecto GIMAP para Louis Dreyfus): medición de los parámetros del amplificador de instrumentación, análisis espectral de la cadena de medición, verificación de la frecuencia de muestreo real y automatización del ensayo. El equipo se convierte en el objeto de medición y a la vez en un caso de "automatización de las mediciones".

## Cobertura del programa (unidades del programa analítico oficial)
| Unidad Temática | Qué parte del proyecto la cubre |
|---|---|
| **UT1** — Osciloscopios digitales (DSO/DPO) | Uso justificado del DSO en todas las mediciones: captura de transitorios, elección de instrumento, velocidad de muestreo, tipos de disparo |
| **UT4** — Mediciones en el dominio de la frecuencia: analizador de Fourier, analizador de espectro | Espectro de la señal de vibración: FFT del propio datalogger contrastada con analizador de laboratorio; distorsión de la cadena analógica |
| **UT5** — Mediciones de tiempo y frecuencia | Verificación de la frecuencia de muestreo real y de la base de tiempo del sistema (jitter del muestreo del MPU6050) |
| **UT6b** — Mediciones de un amplificador operacional: tensión de desbalance, corriente de polarización, ancho de banda, slew rate y CMRR | Caracterización completa del INA333 del front-end con esos cinco parámetros, medido vs. hoja de datos |
| **UT10** — Analizadores de estados lógicos | Análisis del bus I2C/SPI del MPU6050 con analizador lógico (equipo propio) para validar temporización y tramas |
| **UT11** — Mediciones de EMC/EMI | Ensayo básico de interferencias sobre el canal analógico en ambiente ruidoso (el escenario industrial real del equipo) |
| **UT12** — Automatización de las mediciones y medición de parámetros no eléctricos avanzados: transductores mecánicos | Cobertura central: el datalogger ES medición automatizada de un parámetro no eléctrico (vibración mecánica) — transductor piezo/MEMS, calibración y trazabilidad del canal |

*Las UT2, 3, 7, 8 y 9 (generadores, redes/parámetros S, reflectometría, potencia RF) no son el eje del proyecto: el generador de funciones aparece como herramienta de ensayo (UT3) y el resto lo preparo para el coloquio teórico.*

## Entregables
1. Informe de caracterización en PDF: método, instrumento, incertidumbre y resultado de cada medición.
2. Tabla comparativa medido vs. especificado (INA333, fs, ruido, respuesta en frecuencia).
3. **Demo funcionando**: banco de ensayo en vivo (vibración → espectro en el datalogger vs. instrumento patrón).
4. Presentación interactiva HTML con las capturas del DSO y del analizador lógico.

## Cronograma tentativo
- **Fines de agosto**: consenso de alcance y de qué instrumental del laboratorio puedo usar.
- **Fines de septiembre**: mediciones del AO (UT6) + buses digitales (UT10).
- **Fines de octubre / principios de noviembre**: análisis espectral, fs y EMI (UT4, UT5, UT11) con el equipo ya probado en campo.
- **Llamados de diciembre (9-11 o 14-18)**: informe final + demo + defensa.

**¿Te sirve así o le falta algo?** Si la cátedra quiere sumar alguna unidad (por ejemplo reflectometría sobre el cableado del sensor) la incorporo.
