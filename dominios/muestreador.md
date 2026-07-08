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

- 2026-07-08 [BRIEFING GIMAP] — leer ../BRIEFING_EQUIPO_GIMAP.md y los 4 docs (PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO). Para vos: galga=señal chica → ADC de puente 24-bit (HX711/ADS1232). CSV real: K=1 sin cal de ganancia, canal A más ruidoso. Implementar shunt-cal + verificación A=B. Filtro fc 0.3Hz orden 2.

## Análisis CSV real de campo (galgas_20260213_133045, 2026-07-08)
2134 muestras, 428s, fs=5Hz. HALLAZGOS MEDIDOS:
- Ruido en reposo: **~1.1 mV std** por canal sobre señal de 1.55V. Evento pp=20mV. **SNR del evento ~4.7×** (pobre).
- **Frecuencia del golpeteo confirmada: ~0.39 Hz** (Matías estimó 0.33) → filtro fc=0.3Hz orden 2 correcto. 5Hz de muestreo sobra (Nyquist).
- El evento "toque" (amarilla arriba, azul=cadena cortada) SE VE: A-B std crece 4× (1.6→6.6mV) durante el evento. Pero A-B mean=0 forzado por offset simétrico → NO hay valores calibrados.
- CONCLUSIÓN: para octubre hace falta (1) ADC de puente 24-bit (HX711/ADS1232) → bajar ruido ~10× → SNR 40-50× → detectar cortes chicos/lentos, no solo el toque grande; (2) shunt-cal obligatorio (sin K_A/K_B reales el A-vs-B no es confiable). 5Hz alcanza; el problema es RESOLUCIÓN + CALIBRACIÓN, no tasa.
