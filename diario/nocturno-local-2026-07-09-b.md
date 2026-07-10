# Nocturno LOCAL — 2026-07-09 (segunda tarea de la noche, "-b")

> La primera tarea de esta misma noche (deuda del @verificador sobre el RX de
> galgas) ya está hecha y commiteada — ver `nocturno-local-2026-07-09.md` +
> commit `e5fbcd7`. Este informe es de una **segunda** corrida del worker.

## Tarea elegida y por qué
**Datalogger #5 (integridad SD): construir el DETECTOR DE GAPS** — la
herramienta que *prueba* la prueba de N horas del DoD ("canal MPU logueando a SD
**sin gaps**").

Recorrí los 4 QUE_FALTA buscando UNA tarea de **software** prioritaria que **no**
esté ya en un branch nocturno esperando merge, con la jerarquía **PLATA y
UNIVERSIDAD primero, octubre segundo**:

- **FrioSeguro (PLATA)** — sus ítems de software restantes NO dan un win nocturno
  limpio hecho a ciegas: #11 (resumen mensual) y #12 (retención) son **prematuros**
  (cero abonos hoy, misma razón que anotó el worker del 8-jul); #10 tiene dos
  mitades: "renderizar el bloque resiliencia que el firmware ya emite" está
  **bloqueado por la migración SQL #3** (las columnas `connection_mode`,
  `gsm_signal`, `free_heap` todavía no están en Supabase → el dashboard no tiene
  qué leer), y la "vista mobile de un vistazo" es una UI **especulativa grande**
  que rinde con verificación visual (la haría el @tester/@frontend de día, no a
  ciegas de noche). Anti-sobre-ingeniería: no construir eso ahora.
- **UNI** vive fuera de los 4 repos del worker.
- **galgas** — el RX ya se pagó (tarea "a" de esta noche); el resto de sus ítems
  es hardware/backend/UI-grande (#9 SCADA redler es octubre + UI grande).
- **datalogger** es **PRIORIDAD #1 de banco** (PORTFOLIO: "terminarlo PRIMERO").
  ECO-LoRa (#3) e INA219 (#4) ya están en branches del 7/8-jul. Quedaba libre el
  **#5 (integridad SD)**, que es 🔴 bloqueante del DoD y **software puro,
  100% verificable esta noche sin hardware**. Descubrimiento clave al leer el
  código: los `seq` y `t_ms` **ya se escriben** en el CSV (`nodo.py:171,189`) —
  lo que faltaba de #5 no era instrumentar el firmware sino el **detector de
  gaps** que analiza los CSV y dictamina PASS/FAIL. Encaja perfecto con "UNA
  tarea bien hecha por noche" y con la convergencia **Medidas Electrónicas 2**
  (integridad/trazabilidad de datos).

## Qué hice (branch `nocturno/local-2026-07-09-sd-integrity`, sale de `main`)

Herramienta nueva, **aditiva** (no toqué firmware — no hace falta):

| Archivo | Qué |
|---|---|
| `tools/sd_integrity.py` | Analizador offline (solo stdlib) que corre en la PC sobre `/sd/logs/*.csv`. Detecta: **gaps de tiempo** (primario, sirve en modo continuo e intervalo: `dt` de `t_ms` > `--gap-factor`×período nominal auto); **drops de seq** (extra, modo continuo `sd_interval_s=0`: salto de `seq` = escritura SD perdida sin salto de tiempo); **reboots** (`seq` que decrece → parte en sesiones, no cuenta como gap); **wrap de `ticks_ms`** (`dt`<0 con `seq` creciente = envolvimiento, no gap); **filas corruptas/truncadas** (corte de energía a mitad de `write`). Emite resumen humano + `--json`, y **exit code 0 (sin gaps) / 1 (gaps) / 2 (error)** para usarlo como pass/fail. |
| `tests/test_sd_integrity.py` | 8 casos sintéticos (tempdir, sin dependencias): intervalo limpio, continuo limpio, gap de tiempo, drop de seq, reboot, wrap de ticks, filas corruptas, y exit codes sobre una carpeta. |
| `docs/sd-integrity.md` | Protocolo de la prueba de N horas: cómo configurar el nodo, correr, bajar `/sd/logs/`, analizar e interpretar (ojo con las pausas legítimas de las ráfagas FFT). |
| `QUE_FALTA.md` | #5 anotado "EN BRANCH … pendiente de merge". |

Dos sutilezas que el detector maneja bien (por eso no da falsos positivos):
- **Modo intervalo** (default `sd_interval_s=1`): `seq` salta legítimamente → el
  chequeo por seq NO aplica, se usa el de tiempo. **Modo continuo**
  (`sd_interval_s=0`): `seq` avanza de a 1 → el salto de seq sí es un write perdido.
- Las **ráfagas FFT** (`fft_auto`) pausan el muestreo ~1-3 s: aparecen como gaps
  de tiempo *legítimos* → documentado cómo cruzarlos contra `fft_period_s` (o
  correr la prueba con `fft_auto=false` para integridad pura de SD).

## Cómo verificarlo (comandos exactos, sin hardware)
```bash
cd C:\Proyectos\datalogger
git checkout nocturno/local-2026-07-09-sd-integrity

# 1) Sintaxis
python -m py_compile tools/sd_integrity.py tests/test_sd_integrity.py

# 2) Self-test (genera CSVs sintéticos y valida cada detección)
python tests/test_sd_integrity.py            # -> "OK: 8 tests", exit 0

# 3) Smoke manual: analizar cualquier CSV real cuando exista
python tools/sd_integrity.py /ruta/a/logs/   # PASS/FAIL + exit 0/1
```
**Resultado obtenido esta noche:** `py_compile` **OK** en los 2 archivos;
self-test **OK: 8 tests** (exit 0). En el test que ejercita `main()` sobre una
carpeta se ve el flujo real: detecta un gap de `9020 ms (~450 muestras
perdidas)`, imprime `VEREDICTO: FAIL` y devuelve exit 1; carpeta limpia →
`PASS`, exit 0. Python 3.14.3.

## Qué quedó SIN verificar (necesita el nodo + SD en mano)
- **La prueba de N horas real**: correr un Pico 2 W con SD `sd_enabled=true`
  N horas, bajar `/sd/logs/` y pasar los CSV por la herramienta. El detector está
  probado con datos sintéticos; falta alimentarlo con datos REALES del muestreo a
  la fs objetivo (y confirmar que el período nominal auto-detectado y el
  `--gap-factor` por defecto (3) no den falsos positivos con el jitter real —
  ajustar el factor si hace falta, ya es parámetro).

## Reglas respetadas
Nada borrado. NO toqué firmware (los `seq`/`t_ms` ya estaban), ni
`field_captures` (es de galgas), ni mDNS, ni migraciones. Solo software aditivo
en un branch nuevo salido de `main`. El branch NO se mergea hasta correr la
prueba de N horas con hardware. Timeouts: no hubo compilación pesada (Python
puro), verificación instantánea.

## Branch
`nocturno/local-2026-07-09-sd-integrity` (pusheado a origin, 1 commit `b070fab`).
Sale de `main`.

## Nota para el @director / mañana
En `main` de datalogger, el `QUE_FALTA.md` NO refleja los branches ECO-LoRa (#3)
e INA219 (#4) — esas anotaciones viven en sus propios branches del 7/8-jul,
pendientes de merge. No es un bug, es que esos branches aún no se mergearon; al
mergearlos se consolidan las 3 anotaciones (#3, #4, #5).
