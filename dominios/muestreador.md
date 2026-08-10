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

## 2026-07-21 — LOS 4 DATALOGGERS DE LA TAXONOMÍA, CODIFICADOS (sesión Director)
Un firmware, 4 misiones (`firmwares/pico2w-node/misiones/` en repo datalogger, commit da574c3 en main):
- **lab** (1 kHz): FIFO del MPU + WiFi UDP broadcast :50506, sin SD. Receptor PC `tools/lab_rx.py` (CSV + gaps por seq).
- **baja** (≤200 Hz, DLPF 94): SD con seq/gaps; fase RT LoRa 60-120 s (`mision_rt_min`) → después solo SD.
- **media** (333 Hz real): SD + **partes de la SD por LoRa** (SDLS/SDGET→SDCHK b64) + RT WiFi decimado 50 Hz :50507.
- **dreyfus** (5 Hz ADC): golpeteo REDLER — detector por histéresis (validado: 24 golpes/min y 0.390 Hz con señal sintética de 0.39 Hz), resumen RV1 c/60 s → cloud vía receptor. NO reemplaza al repo galgas (producción).
Se elige con `cfg mision <nombre>` + reset; `mision=off` = nodo clásico intacto (hook try/except en main.py).
**Evidencia**: `tools/test_misiones.py` (stubs de machine/network) — **9/9 OK**. Doc: `docs/MODOS_MISION.md`.
**Pendiente de banco**: fs efectiva real de cada misión en hardware, N horas de SD (QUE_FALTA #5), consumo INA219.

## 2026-08-10 — ⚠️ EL CANAL CONTINUO DEL DATALOGGER ALIASEA (auditoría nocturna, `QUE_FALTA` #15)
Branch `nocturno/local-2026-08-10-cadena-vibracion` · herramienta `tools/check_vibration_chain.py` (82 tests, 3 oráculos numéricos) · análisis: `docs/vibration-chain.md`. **Nada corregido: es tu decisión.**

**El hecho:** `mpu6050.py` nunca escribe `CONFIG` (0x1A) ⇒ **DLPF_CFG = 0 ⇒ ancho de banda del acelerómetro 260 Hz**. Y el `SMPLRT_DIV` tampoco. Tabla de rutas (criterio: ¿Nyquist > BW?):

| ruta | fs viene de | fs | Nyquist | BW | |
|---|---|---|---|---|---|
| clásico (`mision=off`) | `config.P1/P2.json` | 50 | 25,0 | 260 | **pliega 25-260** |
| clásico (`mision=off`) | `config.P3.json` | 10 | 5,0 | 260 | **pliega 5-260** |
| `baja` | nominal `FS_DEF` | 200 | 100,0 | 94 | ok |
| `baja` | `cfg["mpu_hz"]` de P1/P2 | 50 | 25,0 | 94 | **pliega 25-94** |
| `lab` | literal | 1000 | 500,0 | 184 | ok |
| `media` | divisor | 333 | 166,5 | 94 | ok |

- **Lo que corre hoy es el clásico** (ningún `config.P*.json` setea `mision`) con `sd_interval_s=0` = una fila de SD por muestra: **es el canal del DoD.** Un rodamiento a 3-10× rpm cae **siempre** dentro de 0-25 Hz; el 2× de una máquina a 1500 rpm cae en **DC**. Demostrado con números: la misma máquina da pico en 66 Hz a 1 kHz y en **16 Hz** a 50 Hz (`--demo-alias`).
- **Tu trabajo del 07-21 está bien hecho:** `lab` y `media` filtran correctamente y los valores de la taxonomía son los correctos. **Pero `mision_baja` deriva su fs de `cfg["mpu_hz"]`** (`self.fs = min(FS_DEF, cfg["mpu_hz"])`): filtra bien a 200 Hz y mal a los 50 que le dejan los nodos. **El DLPF y la fs se eligen en archivos distintos.** Bajar `mpu_hz` para ahorrar energía (lo que empuja @energia) rompe el anti-alias en silencio.
- **El DLPF vive en 4 copias privadas** (una por misión) y el driver compartido en ninguna ⇒ el registro es **del chip**: volver a `mision=off` sin cortar alimentación deja el filtro de la misión anterior. El mismo código mide distinto según lo que corrió antes y **nada lo registra** (ni el CSV ni el frame).
- **Integridad ≠ validez:** un CSV aliaseado tiene largo correcto, `seq` contiguo y cero gaps ⇒ **pasa los tres branches de `sd_integrity`**. Anotado en el `QUE_FALTA` #5.
- **Y no lo decide el runtime:** anotado en el bloqueante #1. Gane MicroPython o gane C, el canal sigue aliaseado. **Decidir antes o durante la misma sesión de banco.**

**LA DECISIÓN QUE TE TOCA:** ¿qué mide el canal continuo? (a) **espectro** ⇒ 50 Hz no alcanza: muestrear a 1 kHz y guardar **agregados** (RMS, pico, kurtosis) en vez de muestras crudas; (b) **orientación/inclinación** ⇒ `DLPF_CFG=5/6` (10/5 Hz) es lo correcto y hay que dejar de llamarlo canal de vibración (ojo con los 13,8-19,0 ms de retardo de grupo si se correlaciona entre nodos).

**Además, del mismo análisis:** `burst_hz` acepta 4000 Hz con la ODR del accel fija en **1 kHz** (cada muestra leída 4 veces; el default 1000 es *exactamente* la ODR ⇒ duplicados al azar) y `real_hz` mide el **lazo de lectura**, no la tasa de datos nuevos · el dashboard hace la FFT **sin ventana** (±36 % de amplitud según dónde caiga en el bin de 3,9 Hz) y `analysis.py` la hace con Hanning pero normalizada al pico ⇒ **las dos herramientas no son comparables**, que es exactamente lo que **Medidas Electrónicas 2** pide declarar (incertidumbre, resolución, trazabilidad). **Ahí hay material de final servido.**

**Verificación de banco pendiente (10 min, SIN instrumental):** capturar una ráfaga y **contar muestras consecutivas idénticas** — confirma y mide V2.
