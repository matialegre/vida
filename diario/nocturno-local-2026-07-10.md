# Nocturno LOCAL — 2026-07-10 (worker de la PC, Matías durmiendo)

## Tarea elegida y por qué
**Datalogger #7 — calibrador distancia↔RSSI de la malla RV1: la mitad de
software.** `tools/rssi_calibrate.py` ajusta el modelo log-distancia y devuelve
`n` y RSSI@1m a partir de mediciones de campo.

Recorrí los 4 QUE_FALTA + los 3 nocturnos previos (07-08 ECO-LoRa, 07-09 RX
galgas, 07-09-b SD-integrity) buscando **UNA** tarea de **software** prioritaria
que **no** esté ya en un branch nocturno, con la jerarquía **PLATA y UNIVERSIDAD
primero, octubre segundo**. El razonamiento (por qué esta y no otra):

- **FrioSeguro (PLATA)** — **no tiene tarea de software nocturna limpia hoy**, y
  lo verifiqué en el código, no de memoria:
  - #3 (migración SQL de columnas nuevas): **el archivo ya existe** —
    `supabase/migration_resilience_v1.sql` cubre `connection_mode`, `gsm_signal`,
    `uptime_sec`, `free_heap` + las de `readings`. Lo que falta es **aplicarla**
    en Supabase (cloud + credenciales), no escribirla. No es tarea de software
    nocturna.
  - #10 (renderizar bloque resiliencia): **ya está hecho** en el dashboard React.
    `supabaseClient.js` parsea los campos (`systemState`, `connectionMode`,
    `gsmSignal`, `uptimeSec`, `cooldownRemainingSec`, `freeHeap`…) y **se
    muestran**: `App.jsx` (state con color/ícono, uptime, timers de cooldown) y
    `DevicesAdminTable.jsx` (barra GSM, modo, uptime, free heap). El único
    remanente es la "vista mobile de un vistazo", UI **especulativa** que rinde
    con verificación visual → es del @tester/@frontend de día, no a ciegas de
    noche. El QUE_FALTA #10 quedó **desactualizado** (anotado abajo para el
    @cronista).
  - #4 (credenciales) y #7/#8/#9 (SIM800/OTA/NTP) necesitan **flasheo/hardware**.
- **UNI** vive fuera de los 4 repos del worker.
- **galgas** — los ítems de software ya se pagaron en branches (RX 3.7.1) o son
  hardware/UI-grande/octubre (SCADA redler). Nada nuevo y limpio de noche.
- **datalogger** es **PRIORIDAD #1 de banco** (PORTFOLIO: "terminarlo PRIMERO").
  ECO-LoRa (#3), INA219 (#4) y SD-integrity (#5) ya están en branches. Quedaba
  libre el **#7 (calibrar distancia↔RSSI)**, cuya **mitad de software** es
  **100% verificable sin hardware** (ajuste sobre datos sintéticos) y **converge
  con Medidas Electrónicas 2** (caracterización/incertidumbre de una medición).
  Encaja con el patrón que funcionó (herramienta offline stdlib + tests, como
  `sd_integrity` del 09-b) y con "UNA tarea bien hecha por noche".

## Qué hice (branch `nocturno/local-2026-07-10-rssi-calib`, sale de `main`)

Herramienta nueva, **aditiva** (NO toqué firmware — hoy nadie convierte RSSI en
metros; esto produce las constantes para cuando se implemente):

| Archivo | Qué |
|---|---|
| `tools/rssi_calibrate.py` | Ajusta el modelo path-loss log-distancia `RSSI(d) = A − 10·n·log10(d)` por **mínimos cuadrados en forma cerrada** (sin numpy, solo stdlib) sobre un CSV `(distancia_m, rssi_dbm)`. Devuelve **A = RSSI@1m**, **n** (exponente de pérdida), **R²**, **RMSE**, más la inversa `d(RSSI) = 10^((A−RSSI)/(10·n))` y las opciones `--predict d1,d2` (RSSI por distancia) / `--invert r1,r2` (distancia por RSSI). Detecta header por nombre o usa las 2 primeras columnas; ignora `#`/blancos/no-numéricas/distancias ≤0; lee de stdin con `-`. Da una pista del ambiente según `n` y avisa de ajustes frágiles (pocos puntos, `n<1.8`). **Exit 0** = ajuste confiable (R² ≥ `--min-r2`, def. 0.7), **1** = dudoso/insuficiente, **2** = error. |
| `tests/test_rssi_calibrate.py` | 11 tests sintéticos sin hardware: recuperación exacta de `A`/`n` de datos limpios (R²=1), recuperación con ruido determinista, round-trip de la inversa, múltiples muestras por distancia, una sola distancia → `ValueError`, parseo de header por nombre y por posición (con skips), y exit codes de `main()` (0 con buen ajuste, 1 con pocos puntos, 1 con R² bajo). |
| `docs/rssi-calibration.md` | Protocolo de campo: qué medir (1,2,4,8,16,30 m; ≥3 distancias, 5+ recomendado; varias muestras por punto), cómo armar el CSV, cómo ajustar e interpretar `n`/R²/RMSE, y la convergencia con Medidas Electrónicas 2. |
| `QUE_FALTA.md` | #7 anotado "EN BRANCH … pendiente de merge" con el detalle. |

## Cómo verificarlo (comandos exactos, sin hardware)
```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-10-rssi-calib

# 1) Sintaxis
python -m py_compile tools/rssi_calibrate.py tests/test_rssi_calibrate.py

# 2) Self-test (genera datos sintéticos y valida ajuste/inversa/exit codes)
python tests/test_rssi_calibrate.py            # -> "OK: 11 tests", exit 0

# 3) Smoke con datos realistas
printf "distancia_m,rssi_dbm\n1,-38\n2,-46\n4,-53\n8,-61\n16,-70\n30,-77\n" \
  | python tools/rssi_calibrate.py - --predict 1,5,25 --invert -60,-80
```
**Resultado obtenido esta noche:** `py_compile` **OK** en los 2 archivos;
self-test **OK: 11 tests** (exit 0, 27 asserts internos). El smoke realista da
`RSSI@1m=−37.72 dBm`, `n=2.645` ("semi-obstruido"), `R²=0.9989`, `RMSE=0.45 dB`,
VEREDICTO **OK**, exit 0; y las predicciones/inversas son coherentes
(−60 dBm → 6.96 m, −80 dBm → 39.68 m). Python 3.14.3.

## Qué quedó SIN verificar (necesita el hardware + medir en campo)
- **La toma de datos real**: colocar un nodo a distancias conocidas en el
  ambiente de despliegue (galpón/planta), anotar el RSSI reportado por el
  gateway/vecinos y pasar el CSV por la herramienta. El ajuste está probado con
  datos sintéticos; falta alimentarlo con **medidas reales** y confirmar que `n`
  y R² den físicamente sensatos (multipath del ambiente real → puede bajar R²;
  si pasa, medir en más puntos o revisar setup, ya está documentado).
- **La otra mitad de #7 y su consumo**: implementar en firmware/dashboard la
  conversión RSSI→metros usando `A`/`n` (hoy no existe). NO lo hice: sería
  especulativo y no verificable sin hardware. La herramienta deja las constantes
  listas.

## Reglas respetadas
Nada borrado. NO toqué firmware (los `seq`/RSSI ya se emiten; el mapa de
distancias sigue guardando RSSI crudo), ni `field_captures` (es de galgas), ni
mDNS, ni migraciones. Solo software aditivo en un branch nuevo salido de `main`.
El branch NO se mergea hasta correr la calibración con datos de campo. Timeouts:
no hubo compilación pesada (Python puro), verificación instantánea.

## Branch
`nocturno/local-2026-07-10-rssi-calib` (pusheado a origin, 1 commit). Sale de
`main`.

## Nota para el @director / @cronista (drift detectado)
- **FrioSeguro `QUE_FALTA.md` #10 está desactualizado**: dice "renderizar bloque
  resiliencia que el firmware ya emite" como pendiente, pero el dashboard React
  **ya lo renderiza** (systemState/uptime/connectionMode/GSM/free heap/cooldown
  en `App.jsx` + `DevicesAdminTable.jsx`). Lo único vivo de #10 es la "vista
  mobile de un vistazo". Convendría reescribir el ítem así cuando alguien lo
  toque, para no volver a evaluarlo cada noche.
- Recordatorio (ya anotado el 09-b): en `main` del datalogger el `QUE_FALTA` no
  refleja los branches ECO-LoRa (#3), INA219 (#4) ni SD-integrity (#5) — cada
  anotación vive en su branch; se consolidan al mergear.
