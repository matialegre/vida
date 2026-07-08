# Propuesta de Trabajo Integrador (Laboratorio 9) — Teoría de los Circuitos II

- **Para**: Ing. Oscar Alberto Rodríguez (prof. responsable) / Ing. Christian Galasso (docente auxiliar) — según programa oficial 9-95-0432 (plan 1995, vigencia 2022+).
- **De**: Matías Alegre, legajo 19074.

## Propuesta
Cadena completa de medición de vibraciones: **front-end analógico para sensor piezoeléctrico (INA333 + filtro activo anti-aliasing de 2º orden) + filtrado digital FIR/IIR y FFT implementados en Raspberry Pi Pico**, presentado **funcionando** con señal real de vibración. Es hardware que ya estoy desarrollando para un cliente industrial real (Louis Dreyfus, vía GIMAP), adaptado como trabajo integrador según lo que pide el propio programa: *"un trabajo integrador (Laboratorio 9) a consensuar entre el alumno y la cátedra... el cual deberá ser presentado funcionando, para su ensayo y aprobación"*.

## Cobertura del programa (unidades del programa analítico oficial)
| Unidad Temática | Qué parte del proyecto la cubre |
|---|---|
| **UT1** — Modelos matemáticos, función de transferencia | Modelo eléctrico del sensor piezo + FT del canal analógico completo (analogía sistema mecánico–eléctrico, que la unidad nombra explícitamente) |
| **UT2** — Respuesta en frecuencia, diagramas de Bode | Bode teórico vs. medido del front-end (simulación + medición con generador y osciloscopio) |
| **UT3** — Teoría de los cuadripolos | Caracterización del canal de acondicionamiento como cuadripolo en cascada (parámetros, impedancias de entrada/salida). *Cobertura parcial: se complementa con los Laboratorios 1–8 ya cursados* |
| **UT4** — Filtros pasivos, teoría de la aproximación | Plantilla del filtro real, normalización, aproximación Butterworth/Bessel y transformación de frecuencia aplicadas al diseño del anti-aliasing; red pasiva de entrada del piezo |
| **UT5** — Filtros activos | Diseño y síntesis de la celda de 2º orden con AO (Sallen-Key/MFB): factores de 2º orden, Q, análisis de sensibilidad |
| **UT6** — Sistemas discretos, transformada Z | FT digital del filtro implementado, plano Z, relación frecuencia digital–analógica en el muestreo del MPU6050/piezo |
| **UT7** — Diseño de filtros digitales IIR y FIR | Diseño (warping/precombado para IIR, ventaneo para FIR) e implementación en el Pico, con comparación medida entre ambos |

## Entregables
1. Informe de diseño (FT, Bode, plantillas, aproximación, sensibilidad, diseño digital) en PDF.
2. Mediciones: respuesta en frecuencia del filtro activo y del digital, teórico vs. simulado vs. medido.
3. **Demo funcionando en el laboratorio**: señal de vibración real → front-end → Pico → espectro filtrado.
4. Presentación interactiva HTML + código fuente documentado.

## Cronograma tentativo (2º cuatrimestre 2026)
- **Fines de agosto**: consenso de alcance con la cátedra (esta propuesta, ajustada).
- **Fines de septiembre**: diseño analógico cerrado (UT1–UT5) + informe parcial.
- **Mediados de noviembre**: filtros digitales implementados y medidos (UT6–UT7).
- **Fines de noviembre / llamados de diciembre (9-11 o 14-18)**: ensayo funcionando ante la cátedra, antes del cierre del ciclo lectivo como pide el programa.

**¿Te sirve así o le falta algo?** Cualquier unidad que quieran ver con más profundidad la incorporo al alcance antes de arrancar.
