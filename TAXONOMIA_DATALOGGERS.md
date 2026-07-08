# Taxonomía de dataloggers — refinada con Sebastián Machado (GIMAP, 2026-07-08)
> Sebastián Machado = referente GIMAP, autor del paper MEAS-D-25-07766 (base del cosechador). Su input define las tasas.

## Los 4 productos (división acordada)
| # | Datalogger | Tasa MPU | Comunicación | Almacenamiento |
|---|---|---|---|---|
| 1 | **Laboratorio** | hasta 1 kHz | **WiFi streaming** a PC; todos en la red GIMAP lo ven | a la PC (sin SD) |
| 2 | **Baja frecuencia** | **≤ 200 Hz** (Sebastián) | **LoRa tiempo real** (envía c/60-120 s) → luego SOLO SD | SD |
| 3 | **Media (300 Hz)** | **300 Hz** (Sebastián) | LoRa transmite PARTES de la SD, o WiFi para tiempo real | SD |
| 4 | **Dreyfus (galgas)** | ~5 Hz (golpeteo 0.39 Hz) | LoRa | SD + cloud vía receptor. **Candidato a PROYECTO FINAL de Matías** |

## MPU6050 — capacidades (respuesta a Sebastián)
- Acelerómetro: rate interno FIJO 1 kHz (techo real).
- Giroscopio: 8 kHz (DLPF off) / 1 kHz (DLPF on).
- Sample rate: SR = base/(1+SMPLRT_DIV) → 4 Hz a 1 kHz con DLPF on.
- DLPF (anti-alias): 5/10/21/44/94/184/260 Hz. Elegir ≤ Nyquist de la tasa.
- FIFO 1024 B para ráfaga sin pérdida.

## Lo MEDIDO hoy (Pico 2 W MicroPython, 6 ejes)
- Techo de lectura: 881 Hz (profile normal) / 995 Hz (max). Ráfaga a SD: 993 Hz efectivos @ max.
- **Conclusión: a 200 y 300 Hz MicroPython alcanza de sobra** (margen 3-4×, sin gaps). El debate MicroPython-vs-C solo aplica al de 1 kHz (lab). Para #2 y #3, MicroPython es viable.
- DLPF sugerido: #2 (200Hz)→94Hz; #3 (300Hz)→94Hz; #1 (1kHz)→184/260Hz.

## Nota estratégica
Matías definió que **Dreyfus va como Proyecto Final** (cliente real LDC, aval GIMAP, el paper v3 ya está borrador — PAPER_DREYFUS_V3.html). Los 3 dataloggers (lab/baja/media) son productos GIMAP derivados del mismo firmware con presets de misión (ver docs/MODOS_MISION.md en el repo datalogger).
