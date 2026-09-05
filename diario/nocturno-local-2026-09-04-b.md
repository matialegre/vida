# Nocturno local — 2026-09-04-b

**Trabajador:** worker nocturno local (Matías durmiendo). Segundo turno de la
noche (el primero fue `nocturno-local-2026-09-04.md`, datalogger / el nodo que
se queda mudo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la
jerarquía), zonas `firmware_modular/` + `servidor/`.
**Branch:** `nocturno/local-2026-09-04-b-la-temperatura-que-no-se-midio`
(pusheado, `4d861a2`; el trabajo es `c1a1a64`, arriba sólo el resultado del
compile anotado en `QUE_FALTA`).
**Sale de `main` (`2ac3a7d`) con `nocturno/local-2026-08-29-la-sonda-que-se-cae`
ya mergeado adentro** — depende de su `sensor_fault_model.h`. Al mergear este
entra también aquél; **no hace falta mergear el 08-29 por separado**.
**No colisiona con ninguno de los 34 branches abiertos**: no toca
`web-dashboard/`, ni el notificador, ni `alerts.h`, ni el panel.
**Migración append-only e idempotente** (sólo `ADD COLUMN IF NOT EXISTS`).
**No se tocó nada del trabajo sin commitear de Matías en `hardware/`** (KiCad
mini_lite, `generar_sch.py`) — quedó exactamente como estaba.

---

## TL;DR

> **Con la sonda caída, el equipo seguía publicando la última temperatura
> buena, cada ciclo, como si recién la hubiera medido. El comerciante abría el
> panel y veía −18,2 °C en verde, quieto, mientras la heladera se calentaba.
> Una pantalla en blanco asusta y hace llamar por teléfono; un número viejo
> tranquiliza. El equipo dejó de vigilar y el panel seguía diciendo que todo
> estaba bien.**

## Por qué esta tarea

Es la deuda que el propio branch del 29-ago (`la-sonda-que-se-cae`) dejó
anotada y no tocó. Es **PLATA** — el núcleo de lo que se cobra en el abono es
"el servicio avisa" —, es 100 % software y es verificable sin hardware. Y no
había ningún branch abierto trabajándola.

## El agujero, y por qué nadie lo veía

`readSensors()` sólo pisa la temperatura cuando la lectura salió bien:

```c
if (cls1 == SC_OK) {
  sensorData.temp1 = t1;
  sensorData.valid = true;
}
```

Eso está **bien**: no guarda un −127 °C como si fuera una temperatura. Pero la
consecuencia no estaba escrita en ningún lado — con la sonda caída, `temp1` y
`tempAvg` conservan el último valor bueno **para siempre**, y
`supabaseSendReading()` los publicaba tal cual en cada POST.

Lo interesante es **por qué el servidor no podía taparlo solo**.
`servidor/api/logica/lecturas.py` ya se defiende de las sondas rotas:

```python
# -127.0 = sonda desconectada · 85.0 = valor de reset del sensor
if v <= TEMP_MIN_VALIDA or v >= TEMP_MAX_VALIDA:
    return False
```

Pero **el firmware nunca manda esos códigos**. Manda −18,2. Las dos capas están
bien escritas, cada una hace exactamente lo suyo, y el agujero queda justo en
el medio: **el servidor filtra la sonda que grita, no la que se queda callada.**
Y como `sondas_con_falla()` se apoyaba en la misma función, la caída tampoco
abría un `probe_fault`. Sin sonda no había ni número real, ni alerta.

### Dos casos más que aparecieron tirando del mismo hilo

1. **La sonda fantasma.** `SensorData sensorData;` es global → arranca en cero.
   Un equipo de **una** sonda publica `temp2 = 0.0` toda su vida, y 0 °C pasa
   cualquier validación de rango que se le ponga. El panel dibuja `T2: 0.0°C`
   de una sonda que no existe (`App.jsx:597` sólo se defiende de `null`, y
   `(0.0).toFixed(1)` es `"0.0"`, que es truthy).
2. **La ventana de arranque.** `faulted` tarda 3 ciclos de debounce en ponerse
   en `true`. En esos ciclos la sonda todavía no está "caída", pero si nunca
   leyó bien, lo que hay en `temp1` es el cero de la inicialización — no una
   medición vieja: **ninguna medición**.

## Qué hice

**La regla: por lo que no midió, el equipo no responde.**

- **`firmware_modular/temp_report_model.h`** (nuevo) — decide, por campo, si el
  equipo puede responder por el número. Puro: sin Arduino, sin HTTP, sin
  OneWire. `sensors.h` lo **incluye** — no es un espejo ni una copia, así que
  lo que testea `tools/test_temp_report.cpp` es exactamente lo que se flashea.
  - Una sonda sirve si **ya midió bien alguna vez** (mata el cero de fábrica y
    la ventana de arranque) **y todavía no se dio por caída** (mata el valor
    congelado).
  - `tempAvg` con **OR, no AND**: `readSensors()` ya colapsa el promedio a la
    única sonda viva cuando la otra se cae. Pedir las dos habría tirado una
    medición buena a la basura.
  - **Simulación publica los tres**: los valores salen de la config, viajan con
    `simulation_mode: true` y son deliberados. Si mandara `null`, la demo de
    venta mostraría `--.-°C` y no habría cómo mostrarle una heladera al cliente.
- **`supabase.h`** — lo que no se puede afirmar viaja como `null`, más los
  flags explícitos `temp1_valid` / `temp2_valid` / `temp_avg_valid`. Buffer
  `StaticJsonDocument` **1280 → 1536**: ArduinoJson no avisa cuando se queda
  sin lugar, **descarta el campo en silencio** — y acá eso significaría publicar
  la lectura sin el flag que dice si el número sirve.
- **`temp2_valid` se OMITE si no hay sonda 2.** El campo significa *"la tengo y
  se cayó"*, no *"no tengo"*. Si un equipo de una sola sonda mandara
  `temp2_valid: false`, el servidor le abriría un `probe_fault` del slot 2 **en
  cada lectura, para siempre**. Una tormenta de falsas alarmas es la forma más
  rápida de perder un abono — el fix habría sido peor que el bug.
- **Migraciones** en las dos bases (`servidor/sql/070_validez_temperatura.sql` y
  `supabase/migration_2026-09-04_validez_temperatura.sql`), append-only e
  idempotentes: sólo `ADD COLUMN IF NOT EXISTS`.
- **`sondas_con_falla()`** ahora abre `probe_fault` también por el flag.
  **Tres estados, no dos:** `true` = lo midió · `false` = caída, abrir alerta ·
  **ausente/`NULL` = firmware viejo, NO es falla** (un parque sin actualizar no
  puede empezar a tirar alertas por omisión).

### Lo que decidí NO tocar

**El panel ya estaba listo.** `App.jsx` dibuja `--.-°C` ante un `null` (líneas
591, 839, 846). El problema nunca fue que no supiera mostrar "no sé": era que
**nadie se lo decía**. Por eso el branch no toca `web-dashboard/` y no choca con
los cuatro branches abiertos que sí lo tocan.

Tampoco inventé un número de versión de firmware: `FIRMWARE_VERSION` es **por
placa** (`3.0.1-p1`, `8.0.0-p5`…), no hay un "3.1.1" global. Bumpear versiones
tiene consecuencias de OTA y es decisión tuya, así que los docs y el SQL
referencian `temp_report_model.h`, no una versión.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-09-04-b-la-temperatura-que-no-se-midio

# 1) el modelo puro — 21 checks, los 3 casos escritos como REGRESIÓN
g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_temp_report.exe tools/test_temp_report.cpp
./tools/test_temp_report.exe

# 2) el modelo de la sonda caída (branch base) sigue verde
g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_sensor_fault.exe tools/test_sensor_fault.cpp
./tools/test_sensor_fault.exe

# 3) el servidor
cd servidor/api && python -m unittest discover -s tests -t .

# 4) el firmware compila
cd C:\Proyectosrioseguro
arduino-cli compile --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" firmware_modular
```

**Resultados de esta noche:** (1) **21 ok, 0 fail, sin warnings** ·
(3) **48 tests OK** · (4) **exit 0, 65 % flash, 16 % RAM, sin warnings**.

Sobre el (4): lo lancé temprano y a los ~15 min todavía no había terminado, así
que escribí este informe dándolo por pendiente y seguí (disciplina de tiempo).
Terminó solo poco después, y **lo volví a correr sobre el commit ya pusheado
(`c1a1a64`)** para que el número corresponda al árbol que vas a mergear y no a
una versión intermedia. Las dos corridas dieron lo mismo.

## Qué quedó SIN verificar

**Los 6 escenarios de banco** (detalle en `docs/temperature-validity.md`):
desenchufar la sonda en caliente y ver el panel pasar de `-18.2°C` a `--.-°C` ·
volver a enchufarla · equipo de 2 sondas con una sola caída (el promedio sigue
siendo real) · equipo de 1 sonda (se acabó el fantasma de 0,0 °C y `temp2_valid`
no aparece en el JSON) · arrancar sin sonda · y que se abra **un** `probe_fault`
por caída, no uno por lectura.

**De día, en la base:** aplicar `servidor/sql/070_validez_temperatura.sql` y
`supabase/migration_2026-09-04_validez_temperatura.sql`.

## Deuda anotada, no tocada

- **`temp_dht`** tiene exactamente la misma enfermedad
  (`if (!isnan(t)) sensorData.tempDHT = t;`). No lo toqué porque la humedad no
  es parte del kit que se vende hoy, pero el fix es el mismo patrón.
- **`supabaseSendDefrostStart(sensorData.tempAvg, ...)`** manda el promedio sin
  mirar el flag. Toca el contrato de `defrost_sessions`: otra tabla, otra
  conversación.
- **`/api/status` local** publica `sensor.valid`, que es sólo la sonda 1.
- **El parque ya flasheado** sigue publicando el número congelado hasta que se
  actualice. No hay defensa server-side que no sea heurística ("el valor no
  cambió en 30 min") y **un freezer estable la haría saltar**: no la implementé
  a propósito.

## Estado del repo

Limpio salvo el trabajo sin commitear de Matías en `hardware/` (KiCad
`mini_lite`, `generar_sch.py`), que quedó **intacto y sin tocar**. El branch
está pusheado y el `QUE_FALTA.md` actualizado (ítem 20).
