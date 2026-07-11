# Nocturno LOCAL — 2026-07-11 (worker de la PC, Matías durmiendo)

## Tarea elegida y por qué
**galgas #2 — revalidar el umbral `v_pp>40mV` de auto-disparo del emisor contra la
señal REAL de campo (mitad de software).** `tools/vpp_threshold_audit.py` reconstruye
el mismo `v_pp` que calcula el firmware y caracteriza su distribución sobre las 12
capturas del REDLER en planta.

Recorrí los 4 QUE_FALTA + los 6 nocturnos previos (07-08 ECO-LoRa, 07-09 RX galgas,
07-09-b SD-integrity, 07-10 RSSI-calib, 07-10-b secret-scan) buscando **UNA** tarea de
**software** prioritaria que **no** esté ya en un branch nocturno, con la jerarquía
**PLATA y UNIVERSIDAD primero, octubre segundo**. Razonamiento:

- **FrioSeguro (PLATA)** — verifiqué en código (no de memoria): el próximo paso que
  dejó el 07-10-b era "correr el secret-scanner también en galgas/datalogger, el hueco
  #6 los nombra". **Lo verifiqué y NO rinde una noche**: en galgas hay **0** `sbp_`, **0**
  `service_role` JWT, **0** claves privadas — solo **1 anon JWT** (público por diseño,
  INFO) en una carpeta `ejemplo supabase/`; en datalogger, **cero** secretos trackeados.
  El hueco #6 **sobreestima** el riesgo de esos 2 repos (detalle abajo, para @cronista).
  Los demás ítems de FrioSeguro son hardware/comercial o prematuros (ya descartados 3
  noches). **No hay tarea de software nocturna limpia de PLATA hoy.**
- **UNI** vive fuera de los 4 repos del worker — **pero** esta tarea **converge con
  Medidas Electrónicas 2** (caracterización de umbral, tasa de falsos positivos vs
  detección, incertidumbre de una medición): crédito doble (PORTFOLIO §CONVERGENCIA).
- **galgas** es P0 de octubre. El #2 (revalidar umbral) tiene una **mitad de software
  100% verificable sin hardware**: las `field_captures` **son** la señal real (incluyen el
  evento CADENA B ROTA + reposo + motor ON, con los buffers crudos `bufA`/`bufB` y la
  etiqueta ground-truth `in_alert`). Nadie la había tocado; no está en ningún branch.
  Encaja con el patrón que funciona (herramienta offline stdlib + tests + docs) y con
  "UNA tarea bien hecha por noche".

## Qué hice (branch `nocturno/local-2026-07-11-vpp-threshold-audit`, sale de `main`)
Software **aditivo**, **READ-ONLY** sobre las capturas sagradas (regla #3 de su README:
"procesar con un script en `tools/` que lee de ahí en read-only"). No toqué firmware.

| Archivo | Qué |
|---|---|
| `tools/vpp_threshold_audit.py` | Analizador offline (solo stdlib). Extrae el `raw_json` de cada fila por **balance de llaves** (va sin comillas y con comas → el CSV estándar lo rompe), reconstruye `v_pp = max(buf) − min(buf)` **idéntico al firmware** (`adc_sampler.cpp:169`), descarta buffers todo-cero (filas v1/v2 pre-buffer), y caracteriza por archivo/canal: `p50/p95/p99/max` en mV + **% de bloques que superan el umbral** (= auto-disparos) + `in_alert` ground-truth. `--baseline GLOB` marca los archivos de reposo y **gobierna el exit code** (0 ok / 1 si un baseline supera `--max-false-rate`, def 1% / 2 error). `--sweep MIN,MAX,STEP` barre el umbral; `--json`. |
| `tools/test_vpp_threshold_audit.py` | **29 checks** sintéticos (tempdir, sin tocar las capturas reales): extracción por llaves con JSON embebido con comas, `v_pp=max-min` exacto, descarte de todo-cero/vacío/<8, percentiles, glob de baseline, parseo de sweep, y **exit codes** de `main()` (0/1/2) + `--json` por subprocess. |
| `docs/vpp-threshold-audit.md` | Contexto, cómo correrla, los hallazgos de esta noche interpretados, la distinción self-trigger-del-emisor vs alerta-diferencial-del-RX, y la convergencia con Medidas 2. |
| `QUE_FALTA.md` (#2) | Anotado "EN BRANCH … pendiente de merge" con el resumen de hallazgos. |

## Cómo verificarlo (comandos exactos, sin hardware)
```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-11-vpp-threshold-audit

# 1) Sintaxis
python -m py_compile tools/vpp_threshold_audit.py tools/test_vpp_threshold_audit.py

# 2) Self-test (sintético, NO toca las capturas reales)
python tools/test_vpp_threshold_audit.py            # -> "OK: 29 checks", exit 0

# 3) Auditoría real (READ-ONLY sobre las 12 capturas)
python tools/vpp_threshold_audit.py data/field_captures/ \
  --baseline "galgas_20260213_131538.csv" --baseline "galgas_20260213_131637.csv" \
  --baseline "galgas_20260213_132005.csv" --baseline "galgas_20260213_132130.csv" \
  --sweep 20,80,10                                    # -> VEREDICTO: OK, exit 0
```
**Resultado obtenido esta noche** (Python 3.14.3): `py_compile` **OK**; self-test
**OK: 29 checks** (exit 0); auditoría real **exit 0**. Hallazgos:

- **Reposo real (los 4 baseline): 0.00 % de auto-disparos a 40 mV en AMBOS canales**,
  `p99 ≤ 12.6 mV` → umbral a **>3× del ruido p99**, cero falsos en reposo.
- **Eventos de rotura reales cruzan con margen:** `reposo_1.csv` (CADENA B ROTA) llega a
  **1555 mV** → el auto-disparo detecta (margen ~38×).
- 🔎 **Hallazgo para @muestreador:** con **motor encendido**, el **canal B** tiene
  **2.0–2.5 %** de bloques > 40 mV (`max 49.4 mV`) mientras el **canal A queda en 0.00 %**.
  Es la "alerta espuria por vibración" que advirtió el informe §9.2. → decidir en banco
  subir el self-trigger de B a ~50 mV o revisar su front-end/montaje (B es más ruidoso
  también en reposo).
- 🔎 **Anomalía** en `132330.csv` (rotulado "motor estable"): pico de **1557 mV** en ~2.4 %
  de bloques — mismo orden que el evento de rotura. ¿Evento no rotulado o artefacto?
- **Barrido:** baseline queda 0.00 % de 20 a 80 mV; el "no-baseline" cae de 12.9 % @20mV a
  1.3 % @40mV y mesetea en 0.8 % @50mV (solo eventos reales). **40 mV es la rodilla**; **50
  mV** borra la cola de vibración del canal B sin perder detección.

## Qué quedó SIN verificar (necesita el hardware — @muestreador)
- **Revalidar con galga física + INA333 en banco** (el #2 completo): confirmar que el
  `v_pp` del hardware real reproduce estos rangos y **fijar el umbral final** (40 vs 50 mV,
  y si el canal B necesita atención). La herramienta ya deja la evidencia para decidir.
- **Resolver la anomalía de `132330.csv`** contra `docs/INFORME_ENSAYOS_CAMPO_DREYFUS.txt`.
- Las capturas son topología v1/v2 (AP `BELT_AP`, UDP); el front-end analógico es el mismo,
  pero conviene una toma de control en banco con el diseño v3.

## Reglas respetadas
Nada borrado. **`data/field_captures/` NO se tocó** (0 cambios en `git status` — la
herramienta abre solo para lectura). No se tocó firmware, ni migraciones, ni mDNS. No se
copiaron secretos a ningún archivo. Solo software aditivo en un branch nuevo salido de
`main`. Timeouts: sin compilación pesada (Python puro), verificación instantánea. El
branch NO se mergea hasta que @muestreador revalide en banco (pero la herramienta y el
análisis son mergeables ya — no dependen de hardware).

## Branch
`nocturno/local-2026-07-11-vpp-threshold-audit` (pusheado a origin, 1 commit). Sale de `main`.

## Nota para el @director / @cronista (drift detectado)
- **El hueco #6 del PORTFOLIO sobreestima el riesgo de galgas/datalogger.** El 07-10-b
  sugirió correr el secret-scanner en esos repos "porque el hueco #6 los nombra (Supabase
  anon en RuView, CREDENCIALES.txt)". Lo verifiqué con `git grep`: en **galgas** hay **0**
  Management tokens `sbp_`, **0** `service_role` JWT, **0** claves privadas — solo **1 anon
  JWT** (público por diseño → INFO, no crítico) en `ejemplo supabase/firmware_modular/config.h`;
  en **datalogger**, **cero** secretos trackeados. La exposición grave (Management token +
  service_role) es **exclusiva de FrioSeguro** (ya cuantificada el 07-10-b). Sugerencia:
  cuando alguien toque el hueco #6, aclarar que galgas/datalogger solo tienen anon (INFO si
  RLS activo) — no repetir la barrida ahí de noche.
- Como el 07-09-b/07-10: en `main` de galgas el `QUE_FALTA` no refleja los branches RX ni
  este; cada anotación vive en su branch hasta el merge.
