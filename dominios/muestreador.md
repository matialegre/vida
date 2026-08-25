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

## 2026-08-24 — Nodo GIMAP en el aire: el piezo llega, pero lo que se ve es red de 50 Hz
Sesión con el nodo enchufado por USB (Matías no podía conectar batería ni MPU6050: cableado mal puesto). Objetivo: **ver el piezo en vivo por web**. Repo: `C:\Proyectos\datalogger`.

**Estado alcanzado (con evidencia, no fe):** nodo v1.0.3 en `192.168.0.233`, rssi −23, UDP 50507 a 200 Hz + estado 50508, **`gaps: 0`**, visor sirviendo en `:8080` con `/datos` devolviendo 600 puntos vivos. Servidor OTA arriba en `http://192.168.0.232:8000` (publicado 1.0.3, así que no dispara update en loop).

**Dos bugs reales encontrados y corregidos:**
1. `flashear_nodo.py` copiaba 7 archivos y hacían falta **8**: faltaba `celda.py`. El nodo moría en `ImportError: no module named 'celda'` — es decir, **la v1.0.3 nunca pudo haber arrancado con ese script**. Corregida la lista `ARCHIVOS`.
2. `red.py` hacía **un solo intento** de WiFi y al fallar imprimía *"no apareció 'Pazos 2.4GHz'"* — mentira: el scan desde el propio nodo la veía a **−24 dBm** y la conexión manual entraba en 4 s. El CYW43 recién arrancado no engancha al primer try. Ahora: 3 intentos reciclando la radio (`active(False)/active(True)`) y **traduce el status real** (`-2` no se encontró / `-3` clave rechazada / `1` asociando). Conectó al primer intento del código nuevo. **Un timeout no es un diagnóstico.**

**El hallazgo de señal — el piezo está dominado por la red eléctrica:**
- Frecuencia dominante medida por DFT: **exactamente 50,0 Hz** en los dos canales.
- **50,0 % de las muestras en cero**, porque el firmware hace `p1 = max(0, c1 - base1)`: **recorta el semiciclo negativo**. Con 50 Hz muestreado a 200 Hz salen 4 muestras por ciclo ⇒ el patrón "un valor, tres ceros" que se ve como un peine en el gráfico. **Se está tirando la mitad de la señal, y el campo del protocolo es `H` (sin signo), así que arreglarlo toca el protocolo y el visor.**
- Amplitudes de reposo: **p1 (GP26) hasta 9.593 ≈ 0,48 V** — usable. **p2 (GP27) hasta 40.725 ≈ 2,05 V** — prácticamente inservible. Un zumbido así de grande es lo típico de una entrada **flotando** (sin resistencia de polarización a masa); encaja con que Matías dijo que el cableado quedó mal.

**Lo que NO se pudo comprobar:** que el piezo **responda a un golpe**. 150 s grabados en dos tandas (60 s + 90 s con detección de eventos): **cero transitorios**, señal planísima (p1 entre 6.328 y 10.985 todo el tiempo). Probablemente Matías no llegó a golpear, pero **no está verificado**. Queda `probar_piezo.py` (nuevo, en el repo) que mide el reposo 10 s, calcula umbral y avisa cuándo golpear — para que lo corra él frente al sensor.

**Pendiente / próximo paso:**
1. Correr `python probar_piezo.py` y golpear. Si da 0 golpes con `gaps: 0`, el problema es el piezo o el MCP6004, **no el enlace** (ya descartado).
2. Decidir qué hacer con el 50 Hz: polarización de entrada en el MCP6004 y/o filtro notch. **Es problema de hardware, no de firmware.**
3. Sacar el `max(0, ...)` y mandar la desviación **con signo** (toca `FMT_MUESTRA`, `main.py` y `visor_gimap.py` a la vez).
4. Prueba en batería (`probar_bateria.py`) y MPU6050 en 0x68: **ambas bloqueadas por el cableado**.

**Límite del OTA que hay que tener presente:** `publicar_ota.py`/`ota.py` actualizan **solo `main.py`**. Si se rompe `red.py`, `sensores.py` o `celda.py` no hay rescate sin cable. Por eso la corrección de WiFi se flasheó por USB mientras estaba enchufado.

## 2026-08-25 (madrugada) — OTA por aire confirmado, y el nodo se apaga sin poder decir por que
Continuacion de la sesion anterior. Matias conecto **bateria y MPU6050**. Repo: `C:\Proyectos\datalogger`, branch `nodo-gimap/wifi-y-flasheo-2026-08-24`.

**Lo que se gano (con evidencia):**
- **Prueba en bateria: PASO.** `en_usb=False`, WiFi −17 dBm, uptime creciendo 13→71 s, `gaps 0`. Era el DoD pendiente.
- **MPU6050 vivo** (`az` variando 543..655): quedo bien conectado.
- **OTA aplicado POR AIRE**, con bateria y sin cable: 1.0.3 → 1.0.4, uptime reiniciado. **El OTA funciona.**
- **El zumbido de 50 Hz desaparecio al sacar el USB** (p1 pasa de 9.593 de pico a 0 fijo). O sea: **entraba por la masa de la PC**, no por el sensor. Dato util para el informe.

**Correccion importante a lo que dije antes:** dije que el OTA solo bajaba `main.py` y que hacia falta el cable. **Es falso.** `ota.py:115` era `info.get("archivo", "main.py")`: baja el archivo que le pidas. El que asumia uno solo era `publicar_ota.py`, un script de la PC. Fue una suposicion mia sin leer la linea.

**Lo que se construyo (y se probo antes de mandarlo):**
- `ota.py` multi-archivo: **lote atomico** (baja todo a temporales, verifica todos los hashes, y recien ahi pisa) + **`.bak` de cada archivo antes de reemplazarlo**. Lee `manifest.json` y cae a `version.json`.
- **`boot.py` (nuevo)**: la red de seguridad que faltaba. El hash cubre la descarga rota; **no cubre el archivo que baja perfecto y no anda** — que es exactamente como el `celda.py` faltante casi deja el nodo mudo. Cuenta arranques, `main.py` lo pone en cero al llegar a operativo, y a los 3 fallidos restaura los `.bak` solo.
- `tools/test_ota_gimap.py`: **16 checks, todos verdes**, con filesystem del Pico emulado, `http.server` real y `machine` doble. Incluye el control negativo que importa: con UN hash malo en el lote, `main.py` no se toca aunque su propio hash este bien.
- `ajustar_ganancia.py`: barra en vivo con las cuentas crudas del ADC contra el objetivo de media escala.

**El hallazgo de la ganancia** (gracias a que la v1.0.4 publica `crudo1/crudo2` en el canal de estado, sin tocar el protocolo de 200 Hz):

| canal | reposo medido | objetivo | |
|---|---|---|---|
| p1 (GP26) | 16.820 = **0,847 V** | 32.768 = 1,650 V | hay que **subir** |
| p2 (GP27) | 52.524 = **2,645 V** | 32.768 = 1,650 V | **contra el riel de arriba** |

Correccion a lo que se anoto antes: **p2 no esta muerto, esta saturado.** Por eso no se movia ni un LSB. Y `crudo1 < base1` explica por que p1 daba 0 en reposo: el `max(0, c-base)` recorta todo lo negativo y **se pierde medio golpe**.

**EL PROBLEMA QUE MANDA AHORA — el nodo se apago y no hay forma de saber por que.**
Se quedo sin transmitir a los **276 s** de uptime (antes de la ventana de OTA de 10 min, asi que la v1.0.5 quedo publicada sin aplicar). No hay AP `NODO-GIMAP`, no hay ARP, no hay USB: **sin alimentacion**, no colgado. Duro ~10 min de bateria en total.

**Y `bat_v` es `null`**, asi que no se puede distinguir celda agotada / conector suelto / cuelgue. **Ese es el costo real del bug de VSYS**: al arrancar (antes del WiFi) mide bien — leyo 4,54 V —, pero con el WiFi activo el ADC29 da basura y `main.py` la descarta como implausible. Peor: el corte por bateria baja es `V_MIN_PLAUSIBLE < v_bat < V_CORTE`, y con `v_bat≈0` **nunca se cumple: la proteccion de la celda es codigo muerto.**

Dato adicional sospechoso: `crudo2` derivo de 52.524 a **65.535 (3,300 V, tope del ADC)** justo antes de morir, y `crudo1` subio de 0,847 a 0,980 V. Consistente con la alimentacion cayendose y arrastrando el punto de reposo del MCP6004.

**Proximo paso (en este orden):**
1. **Arreglar la lectura de VSYS con WiFi activo** en `bateria.py`. Ya se puede mandar por aire. Sin esto se vuela a ciegas y no se puede cerrar ninguna medicion de autonomia (@energia depende de esto).
2. Que entre la v1.0.5 (`ota.py` + luego `boot.py`+`main.py`): **entra sola en el proximo arranque**, porque `main.py` consulta el OTA tambien al bootear. Requiere que el servidor OTA de la PC este levantado.
3. Recien ahi, ganancia del MCP6004 con `ajustar_ganancia.py`, y el golpe con `probar_piezo.py`.

**Nota de metodo (costo dos veces hoy):** el visor toma los puertos 50507/50508, y cualquier script que se ponga a escuchar ahi le roba o le pierde los paquetes. Un monitor reporto "el nodo esta muerto" cuando en realidad el visor se estaba comiendo el trafico. **Los monitores tienen que consultar al visor por HTTP (`/datos`), no bindear el puerto.** Mismo error que hacia fallar `test_red_gimap.py`.
