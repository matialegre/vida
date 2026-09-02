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
| galgas — detector A−B | 5 Hz alcanza (registro real de campo) | media móvil **2 s** + histéresis | — | Con motor ON el ruido por muestra pica 21,5 mV y pisa el evento (12–15 mV); promediando 2 s el peor ruido cae a 4,86 mV vs. 9,13 mV del evento. Umbral instantáneo = falsas alarmas. | 2026-09-02 |

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

- 2026-08-28 [galgas `esp_a_emisor`/`esp_b_emisor` — la calibracion se escribia en NVS y no la leia nadie · branch `nocturno/local-2026-08-28-la-calibracion-que-nadie-lee`, commit `c048b93`] — `adc_sampler.cpp` calculaba `const float k = DEFAULT_K; const float off = DEFAULT_OFFSET * OFFSET_SIGN;` — las constantes de compilacion de `config.h`. Del otro lado estaba TODO construido: el comando en la cola, la validacion de rangos, `nvsSaveCalibration()`, y hasta `nvsLoadCalK()`/`nvsLoadCalOffsetV()`, **que existian desde el primer dia y no las llamaba nadie**. `set_calibration` desde la nube contestaba `ack=OK`, la fila quedaba `executed` y la medicion salia identica. `force_calibration` peor: `sx->calibration_pending = true` en una struct de RAM que no consumia nadie y que el deep sleep de las lineas siguientes borraba — las **tres** etapas, `ack=OK` sin medir. Pega en QUE_FALTA #2 (bloqueante de octubre): el plan de la parada es calibrar contra la galga fisica **en sitio**, y este era el unico canal remoto; sin el, calibrar = recompilar y reflashear por cable con la caja montada en el REDLER.
  AGRAVANTE encontrado por el camino: las dos familias usaban **formulas distintas** — modular `v*k + off*OFFSET_SIGN` (offset DESPUES de la ganancia) vs. monolitico `ota_wm_pp` `(v-off)*k` (ANTES). El par `(k, offset)` que produce el procedimiento remoto que ya existe (`autoffset` → `cal_with_load`) esta definido para la del monolitico: con `v_raw=1.70 V, k=2.0, off=0.20 V` da **3.00 V** vs. **3.60 V**. O sea que aun cableando la calibracion tal cual estaba, el par calculado con el procedimiento existente habria quedado mal escalado.
  NUEVO `firmware/shared/cal_model.h`: una sola formula `(v_raw - offset)*k` en funciones puras (sin Arduino, sin NVS) — `calIsValid` (rangos **y finitud**), `calSanitize` (par invalido → identidad, medir crudo en vez de medir mal), `calTareOffset` (divide por `k`, por eso la tara es idempotente), `calSeedOffsetFromConfig` (**unico** lugar donde entra `OFFSET_SIGN`), `calStageImplemented`. La validacion previa importa porque una `k = NaN` propaga NaN a `v_pp` y `NaN > 0.040` es `false`: un par corrupto en NVS no haria medir mal, **apagaria el self-trigger de alerta en silencio**.
  CABLEADO: el sampler aplica `calApply()` en las dos ramas (real **y** `DEV_SIMULATE_ADC`, a proposito — si no, en banco la cadena no se ejerce nunca); el `.ino` carga NVS y se la pasa al sampler **ANTES** de `samplerStartBurst()` (una vez por wake: abrir `Preferences` cuesta ms y mAh); siembra en el primer boot; publica `cal_k`/`cal_offset_v` en el `metadata` del reading (antes no habia forma de saber desde la nube con que calibracion se midio); la tara (`force_calibration` stage 1) se persiste en NVS y la ejecuta el **wake siguiente**; las etapas 2 y 3 **fallan con error** en vez de fingir.
  SEGURO DE MERGEAR: con los defaults (k=1, off=0) la formula nueva es la **identidad** — un equipo sin calibrar mide exactamente lo mismo que antes, y hoy no hay ninguno calibrado justamente porque el comando no hacia nada.
  VERIFICADO SIN HARDWARE: `tools/test_cal_model.cpp` compila **el header real** y corre **35 checks OK**; `tools/check_calibration_wiring.py` **62/62** (verifica que el firmware la USE, no que exista); `tools/test_check_calibration_wiring.py` **18 tests** — 16 mutantes + uno que saca los archivos de `main` con `git show` y **exige que el checker repruebe el bug historico**. Un mutante encontro un defecto real del checker: comentar `// nvsClearCalPending();` dejaba el nombre en el archivo y la busqueda por subcadena la daba por hecha (ahora saca los comentarios antes de buscar llamadas). Compilacion real de **A y B**: `1237624 B (94%)`, RAM 18%; baseline `main` en worktree limpio `1235360 B` → **+2264 B, +8 B de RAM**. Doc: `docs/calibration-chain.md` (incluye el procedimiento de tara paso a paso para campo).
  PENDIENTE (banco, 15 min): bajar el periodo con `set_period`, mandar `force_calibration {"stage":1}` con la galga en reposo y verificar en `readings` que el wake siguiente trae `"cal_tared": true` y el posterior `v_mean ~ 0` con `cal_offset_v != 0`. **El `k` real sigue sin medirse** (peso conocido, QUE_FALTA #2): este branch da el canal, no el numero. Ojo: la tara tarda **un periodo de sueño** (10 min en `MODE_NORMAL`).
  AVISO: el sketch quedo al **94% de la particion de programa** — mismo problema que `firmware_modular` de FrioSeguro al 98% (ver `firmware.md`, 2026-08-27): un firmware que no entra no se puede actualizar por OTA. `min_spiffs`/`huge_app` es `--build-property`, no cambio de codigo; es decision de Matias porque afecta el espacio de datos.

## 2026-09-02 — DREYFUS: la evidencia de campo, y los 922 mV que NO son la rotura
Entregable para la reunión del 4-sep (defensa contra el sistema de cámaras). Todo en
`C:\Proyectos\galgas\hardware\evidencia_campo\`: 7 PNG a 200 dpi + `EVIDENCIA.md` +
`generar_evidencia.py` (regenera todo con `python generar_evidencia.py`; lee
`data/field_captures` en solo lectura, verificado `git diff` limpio en `data/`).

**EL HALLAZGO QUE CAMBIA EL DISCURSO — los 922 mV de `reposo_1.csv` son el offset, no la cadena.**
El salto ocurre a las **13:02:32,471**, que es *exactamente* el instante en que el
auto-offset pasa de −0,4199/+0,4199 V a **cero**. Reconstruyendo el crudo (`raw = v − OFF`):
el desbalance A−B vale **915,2 mV antes**, **915,7 mV durante** y **916,5 mV después** de la
supuesta reconexión de las 13:04 — y **914–921 mV toda la tarde**, incluidos los tramos que
el informe llama de "excelente simetría, 0,8 mV". Es un **desbalance eléctrico permanente
entre canales**, no una condición de máquina. El argumento que lo cierra: una desconexión
REAL de cadena, mismo día, mismo equipo, misma calibración, vale **16–19 mV**; 916 mV son
**50×** eso. Además `reposo_1.csv` NO cubre 08:17–13:10: son 23 s de ceros + **hueco de
4,74 h** + 313 s + 169 s, y el evento **ya está en curso en la primera muestra** del bloque
(no hay "antes", así que de ahí no sale ninguna latencia). Lo real de ese archivo: la galga
A derivó **+75,5 mV en 4 h 44 min** (la B no se movió) y esa deriva cruzó el umbral absoluto
de 1,58 V. **Marcado NO PRESENTABLE** (fig. `99_reposo1_NO_PRESENTABLE.png`, uso interno).

**Los 12 CSV son exportaciones ANIDADAS de la misma SQLite** (comparten `id` global):
`134127` ⊃ `133635` ⊃ `133354` ⊃ `133045`. Sumar filas cuenta hasta 4× la misma muestra.
Real: **16.752 muestras únicas** (no 34.563), **3.983 alertas** (no ~5.887), **56,1 min** de
adquisición continua (no ~6 h; la ventana de reloj es 5,83 h con 2 huecos). El parser
tampoco es trivial: `raw_json` está **sin comillar**, el JSON mete comas y rompe el conteo
(42 columnas en el header, 179 en las filas) — `DictReader`/`read_csv` devuelven columnas
corridas **sin avisar**. Se reconstruye por posición: `[0:3]` + `[-38:]`.

**Números duros medidos (van al dossier de @comercial):**
- **Latencia de detección 4,4 s** (evento 13:26: la señal se mueve 13:26:03,35, ALERTA
  13:26:07,755). El escalón dura 3,4 s ⇒ la alerta sale **1,0 s después de completarse**.
  Segundo evento (13:35:33): **2,8 s desde el 50 % del escalón**. El límite lo pone
  `HOLD_SEC=1,5 s`, no el sensor.
- **SNR**: evento sostenido 12,1 mV / σ. Con motor en marcha: **2,2× por muestra**, **6,9×
  promediando 2 s**, **9,9× a 10 s**. Con motor parado (σ=1,45 mV): 8,3× / 22,6× / 32,0×.
  El evento breve (14,7 mV): 2,7× / 8,4× / 12,0× y 10,1× / 27,4× / 38,9×.
- **0 falsas alarmas en 8.136 muestras = 27,2 min** de condición normal (5 tramos, uno de
  6,3 min **con motor en marcha**). Contado muestra a muestra, no citado del README.
- **16.752 muestras / 56,1 min**.

**Lección de DSP para la reunión y para octubre:** por muestra suelta con motor en marcha
el pico de ruido llega a **21,5 mV** — *pisa* al evento de 12–15 mV. Un umbral instantáneo
de 10 mV daría falsas alarmas; lo único que salva el tramo de motor ON con 0 alertas es la
**persistencia (`HOLD_SEC`)**. Promediando 2 s el peor ruido baja a 4,86 mV contra un mínimo
de 9,13 mV del evento: **separación limpia**. Recomendación firme: detector = media móvil de
2 s de |A−B| + histéresis, no muestra instantánea.

**Correcciones al informe de campo (que no cierran con los CSV):**
- `galgas_..._133045.csv` "0 alertas" → tiene **480** (22,5 %). Los 0 de `131538`, `131637`,
  `132005`, `132130` y `132330` **sí** se verifican.
- "EMISOR A APAGADO detectado en <2 s" → medido **10,0 s** (última muestra nueva de A
  14:05:03,739; alerta 14:05:13,752). Y A ya se había congelado **8,4 s** (43 muestras) a las
  14:04:58 **sin** alertar ⇒ el timeout de enlace del receptor es de ~10 s.
- Cronología: el informe pone la desconexión a las 13:43 y STAGE2 a las 13:49; en los datos
  los escalones de B están a las **13:26:04** y **13:35:33** y el `STAGE1→STAGE2` a las
  **13:31:36,9**. Las horas del informe no sirven para anclar figuras.
- "σ reposo ≈3 mV → motor 5 mV": hay **dos sigmas** y el informe los mezcla. σ de la serie
  registrada a 5 Hz: **0,97 / 1,09 mV** en reposo y **4,77 / 7,60 mV** con motor. σ
  *intra-ráfaga* (`stdevA`/`stdevB`, del muestreo interno de 500 Hz): **5,84 / 5,93 mV** y
  **6,95 / 9,70 mV**. Declarar cuál se cita (esto es material de Medidas Electrónicas 2).

**MUESTREO — lo que realmente quedó registrado:** `bufA` del JSON se desplaza **exactamente
1 muestra por fila** ⇒ el registro son **5 muestras/s por canal**, no las 500/s del README.
Las 500 Hz existieron dentro del emisor y solo sobreviven condensadas en `stdev`. Para el
fenómeno (sub-Hz) 5 Hz sobra; el punto es que **el dato crudo se tiró** — coherente con el
principio del dominio: el agregado se recalcula, la muestra perdida no.

**RIESGO ABIERTO PARA OCTUBRE (bloqueante de medición, no de la reunión):** la deriva de la
galga A de **+75,5 mV en 4,7 h es 4–5× el evento a detectar (16–19 mV)**. Con `K_A=K_B=1`
y sin calibración de ganancia **no se puede convertir a µε** ni separar térmica / adhesivo /
batería / máquina. Mientras no se acote: (1) el umbral absoluto sobre una galga es inusable,
(2) el diferencial A−B necesita **re-cero periódico**, (3) esto se ata con el canal de
calibración cableado el 2026-08-28 (`cal_model.h`) — el `k` real sigue sin medirse.

- 2026-08-31 [drive del torno — SISTEMAS_CONTROL/sim: gemelo digital, identificacion y diseno por LR · `C:\Proyectos\drive-torno-esp32s3\SISTEMAS_CONTROL\sim\`] — 5 scripts (`modelo_motor.py`, `identificar.py`, `banco_psim.py`, `diseno_pi.py`, `rango_placa.py`) + README con todos los numeros; 15 figuras PNG+SVG y 11 JSON en `figuras/` y `datos/`. Corren de punta a punta con `python x.py`.

  **HALLAZGO PRINCIPAL — el lazo INTERNO de corriente es inestable.** A Ts=20 ms el polo electrico (tau_e = La/Ra = 5 ms) se extingue DENTRO del periodo de muestreo: `a = e^(-Ts/tau_e) = 0,018`, o sea que el lazo interno ve una **ganancia pura** de 0,0496 A por cuenta de duty. Para |z|<1 hace falta `kpI < 20 cuentas/A`; en servicio hay **120 (5,9x el critico)** y el default del `.ino` es 30 (1,5x — tambien inestable). Robusto a la incertidumbre de La: el critico va de 19,8 (20 mH) a 20,8 (40 mH). Lo UNICO que contiene la divergencia es el clamp de +-40 cuentas por ciclo que el firmware puso "para que un error absurdo no patee el duty": con clamp el ciclo limite queda en 1,58 A p-p, sin clamp 5,43 A p-p con picos de 9,9 A. **AGRAVANTE de seguridad**: sin clamp la corriente pasa el trip de 8 A y **el trip NO dispara**, porque exige 5 muestras SEGUIDAS sobre iMaxTrip y el ciclo limite alterna alto/bajo cada muestra — la proteccion de sobrecorriente es ciega a una oscilacion a Nyquist del propio lazo. Con kpI=10: 0,059 A p-p (27x menos rizado). **NO tocar el clamp: es la red de seguridad que hoy sostiene el drive.** Bajar kpI primero, verificar con `TRAZA`, y recien ahi evaluar el clamp.

  **El PI de VELOCIDAD, en cambio, ya estaba bien.** Diseño formal por lugar de raices sobre la planta que ve el lazo externo (`P(s)=Kt/(Js+B)` — el lazo de corriente ROMPE la realimentacion de FEM, asi que el polo es -B/J y NO -1/tau_m): cero en z=5,0 rad/s y kpV=0,0253 / kiV=0,1267. El firmware tiene z=5,0 (identico) y kpV=0,020 / kiV=0,100 — a 27 %. El ajuste empirico habia encontrado practicamente el optimo REALIZABLE: la restriccion `wn <= 0,2/Ts = 10 rad/s` deja fuera los diseños mas rapidos (z=12 y z=20 dan wn*Ts de 0,33 y 0,56).

  **Identificacion (leccion de metodo para la cadena de medida).** La columna `rpm` de los CSV **no es una medicion**: es la salida del estimador FEM del propio firmware. Ajustar Ke/Ra sobre ella es CIRCULAR — el script lo demuestra: el ajuste libre devuelve Ke=0,14111 contra el 0,14000 cargado en el firmware (+0,79 %). Tampoco hay escalones de lazo abierto (el duty es siempre la salida del lazo) y a 10 Hz con tau_m~110 ms un escalon tendria ~1 muestra. Lo unico MEDIDO es la CORRIENTE. Por balance de pares (`Kt*i = J*dw/dt + B*w + Tc`, lineal, excitado por la propia rampa de setpoint, n=9905): **J = 0,0335 +- 0,0007 kg*m2, B = 0,00244 N*m*s, Tc = 0,792 N*m, tau_m = 112 ms**. R2=0,26 — modesto y explicado: la corriente util es 0,3-1 A sobre un sensor de 30 A, el ADC aporta ~18 mA por LSB, y encima la ondulacion residual del registro es el **aliasing del ciclo limite del lazo interno**. Creible porque J identificada es 2-3x la del rotor solo de un 1 HP (0,010-0,015): mide el TORNO entero (rotor+poleas+correa+husillo+plato). El output-error contra el gemelo NO confirma J (minimo en el borde del barrido) por tres razones estructurales que quedan escritas: lazo cerrado, iRef saturada en iLimite durante los arranques, y par de aceleracion al nivel del ruido.

  **PENDIENTE de medicion (marcado, no inventado):** (1) **La** — es el UNICO parametro sin respaldo experimental, se asumio 30 mH (rango 20-40); puente RLC o escalon a rotor trabado. (2) **Ke** con tacometro (`herramientas\medir_ke.py` ya hace el procedimiento). (3) **Un ensayo de LAZO ABIERTO** con `duty manual` + `TRAZA` a 50 Hz: con eso K y tau_m salen por respuesta al escalon sin depender del estimador, y de paso se mide el rizado real del lazo interno para confirmar el hallazgo en hardware.

  Otros numeros del banco: el estimador FEM se corre **+21,5 RPM (3,6 %)** si Ra sube 20 % por temperatura (coincide con la teoria I*dRa/Ke = +22 RPM) y ese error se transfiere entero a la velocidad real; rechazo de perturbacion 3 N*m: lazo abierto -95 RPM permanentes vs -1,0 RPM cerrado; sin integrador e_ss = 35 RPM ante 1,2 N*m; sin anti-windup 23,3 s de recuperacion contra 5,4 s. Rango de la placa: **61-310 V, 0,19-12 A, La >= 7 mH, tau_m >= 100 ms, solo excitacion independiente o iman permanente**. La amoladora Bosch pasa los cinco limites electricos y aun asi queda afuera por ser motor SERIE (Ke = f(i) rompe el estimador).
