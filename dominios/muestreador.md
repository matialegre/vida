# Dominio: MUESTREO Y DSP (agente @muestreador)

Doc de dominio + bitácora. El agente lo lee al arrancar y lo actualiza al cerrar.

## Estado del dominio (nacimiento, 2026-07-07)
- galgas-supabase: pipeline agregados (v_mean/v_rms/v_pp/sigma/delta_v) corriendo con `DEV_SIMULATE_ADC` — validación con galga física + INA333 real PENDIENTE. Ground truth: `data/field_captures/` (READ-ONLY).
- Legacy: NO repetir `analogRead()` en ISR. Filtros IIR (EMA/biquad) ya diseñados y portables.
- RuView: MPU6050 50Hz→SD+FFT en MicroPython; para datalogger fino evaluar límites de MicroPython (benchmark pendiente con @firmware).
- Umbral de alerta actual: v_pp > 40mV (self-trigger) — revalidar con señal real.

## Decisiones de adquisición (tabla viva)
| Sistema | fs | Ventana | Filtro | Justificación | Fecha |
|---|---|---|---|---|---|
| galgas-supabase | ráfagas (ver act.md) | — | agregados | heredado legacy | pre-2026-07 |

## Bitácora
- 2026-07-07 — Agente creado por Claude Fable. Próximo paso sugerido: banco con galga real + INA333, inyectar deflexión conocida y comparar contra field_captures.
- 2026-07-07 — ALCANCE DATALOGGER (Matías): 2 canales — MPU6050 + PIEZO como sensor de vibración con puente de diodos + caps (envolvente/energía, no forma de onda cruda del piezo). Diseñar el acondicionamiento con @hardware: divisor + clamp + TVS (piezo pica >20V). Dreyfus se mide SOLO con galgas (otro sistema). Datalogger primero, galgas después.
