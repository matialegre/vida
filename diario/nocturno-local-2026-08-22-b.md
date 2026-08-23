# Nocturno local — 2026-08-22-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-22-b-una-medicion-una-fila` (pusheado, `ccd4a7a`).
**Sale de:** `main`. **No depende de ningún otro branch nocturno** — toca
`firmware/shared/`, los dos emisores, una migration nueva y dos archivos nuevos
en `tools/`. No pisa nada del `08-21-presupuesto-silencio` (ese es `web/`).

## TL;DR

> **El emisor tenía un intento por medición y ninguna forma de saber si ese
> intento había entrado.**

Los dos lados de esa frase fallan para lados opuestos, y ninguno se veía desde
afuera:

| si el POST no se podía hacer | si el POST se hizo pero no volvió la respuesta |
|---|---|
| deep sleep, y la medición **dejaba de existir** | el reintento inserta una **segunda fila** |

El primero es un hueco en la serie que parece "el nodo estaba durmiendo". El
segundo son dos filas igual de legítimas a los ojos de la base, separadas por
unos segundos de `ts`. Son los hallazgos **D2** y **D3** de la auditoría del
08-11, que nadie había tocado.

Y el hallazgo de paso, que es el que más me sorprendió:

> **El POST del emisor corría con el timeout que viene de fábrica.** 5000 ms
> para conectar y 5000 para leer (`HTTPCLIENT_DEFAULT_TCP_TIMEOUT`, Core 3.3.8)
> porque **nadie llamó nunca a `setTimeout()`**. Contra Supabase esos 5 s tienen
> que cubrir el handshake TLS entero — y este mismo repo lo documenta en 5-10 s,
> en `gateway_discovery.h`, escrito ahí como la razón por la que el gateway
> rompía el OTA. El emisor se cortaba solo antes de que el servidor contestara.

## Tarea elegida y por qué

Por rotación tocaba galgas (el turno de anoche fue datalogger). De los
pendientes de `QUE_FALTA`, elegí D2+D3 y no otro por tres motivos:

1. **No están en ningún branch esperando merge.** El branch `08-11-cadena-entrega`
   los *encontró* y los dejó anotados; nadie los implementó.
2. **Es un problema de datos, y los datos de octubre son el entregable.** Un
   hueco silencioso y una fila duplicada silenciosa corrompen igual cualquier
   análisis que Dreyfus mire.
3. **D2 y D3 son la misma tarea.** No se puede agregar un reintento sin
   idempotencia (la cola sería una fábrica de duplicados) y no tiene sentido la
   idempotencia sola si la medición ni siquiera se guarda. Hacer uno sin el otro
   deja el trabajo peor que antes.

## Qué hice

**1. La medición no se tira más** — `firmware/shared/reading_backlog.h` (nuevo).
Cola circular de 12 mediciones en RTC slow memory (~768 B de los 8 KB), la única
memoria que sobrevive al deep sleep sin gastar flash. Se encola en tres casos que
antes terminaban en dato perdido: sin WiFi (`no_wifi`), POST que no volvió 2xx
(`post_fail`), batería en hard cutoff (`batt_low`).

El caso `no_wifi` obligó a un cambio de orden en `setup()`: antes, si `wifiBoot()`
fallaba, el emisor volvía a dormir **sin siquiera calcular el reading**. Ahora
termina de medir siempre (no cuesta radio) y recién después decide.

Drena hasta 3 atrasadas por wake y **solo si la entrega de ese wake funcionó** —
si la nube no contesta, gastar radio reintentando lo viejo es tirar batería.
Desborde: pisa la más vieja, con contador. En `MODE_NORMAL` (600 s) los 12 slots
son **2 h de corte cubiertas enteras**.

Lo que **no** cubre, y está escrito en el header para que no se lea como olvido:
corte de energía / batería agotada / watchdog. La RTC memory se va con el 3V3.
NVS aguantaría eso, pero cuesta un ciclo de escritura de flash por wake fallido
—un día sin cobertura son ~144 escrituras— para tapar el modo de falla que menos
pasa.

**2. El reintento no puede duplicar.** Cada medición lleva ahora un
`reading_uid` = `<device>-<run_id hex>-<boot_count>`, generado **cuando la
medición existe** y reusado en todo reintento posterior. Del lado del servidor:
columna + índice único (migration `20260822000000`). Del lado del POST:
`?on_conflict=reading_uid` + `Prefer: resolution=ignore-duplicates`, que
PostgREST traduce a `INSERT ... ON CONFLICT DO NOTHING`.

Tres detalles que parecen menores y no lo son:

- **El `run_id` no es decoración.** Es `esp_random()` una vez por corte de
  energía. Sin ese salt, `boot_count` vuelve a 0 después de un power cycle y los
  uids de la campaña nueva chocan con los de la vieja — y con `DO NOTHING` una
  colisión **no da error**: descarta la fila nueva en silencio. Sin el salt, el
  remedio era peor que la enfermedad.
- **El índice único es total, no parcial.** Un `where reading_uid is not null`
  ocupa menos y suena más prolijo, pero `ON CONFLICT (reading_uid)` no puede
  inferir un índice parcial sin repetir el predicado y PostgREST no lo emite →
  error `42P10`. Con el total no hace falta: en Postgres los NULL son distintos
  entre sí, así que las filas históricas conviven sin chocar.
- **`ignore-duplicates`, no `merge-duplicates`.** El primero es un INSERT puro y
  le alcanza la policy `insert_readings_anon` que ya existe. El segundo sería un
  UPDATE y pediría una policy que hoy no está.

**3. Los timeouts** — 12 s de connect y de read (`SB_CONNECT_TIMEOUT_MS` /
`SB_READ_TIMEOUT_MS`), contra los 5 s de fábrica. Esto **no** cierra la ventana
de duplicado: la capa de abajo siempre puede sobrevivir a la de arriba, correr el
número solo mueve la ventana. Lo que la cierra es el uid. Los 12 s arreglan otra
cosa: que el emisor deje de inventar fallas que no existían.

**4. El auditor** — `tools/check_reading_idempotency.py` (read-only, sin nube ni
hardware). Saca las constantes reales de las fuentes (no las hardcodea, así
detecta drift), y corre 7 checks. Modos demo: `--demo-timeouts`,
`--demo-duplicados`, `--demo-backlog`, más `--sql` que imprime la consulta para
buscar duplicados ya acumulados en la base.

Una fila drenada llega con `metadata.backlog` y `metadata.age_s` (hace cuánto se
**midió**), porque `readings.ts` es la hora de **llegada**. Sin eso, una lectura
de hace dos horas entra al histórico como si fuera de recién. Arreglar `ts` de
raíz sigue siendo **D4**, abierto.

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-22-b-una-medicion-una-fila

# auditoría: 7 checks, 0 fallando
python tools/check_reading_idempotency.py

# 35 tests
python -m unittest discover -s tools -p "test_check_reading_idempotency.py" -v

# las tres tablas del informe, generadas del código real
python tools/check_reading_idempotency.py --demo-timeouts
python tools/check_reading_idempotency.py --demo-duplicados
python tools/check_reading_idempotency.py --demo-backlog

# compilan los dos emisores
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_a_emisor
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_b_emisor
```

**Corrido esta noche:** los 35 tests pasan; la auditoría da 7/7; A y B compilan.
Costo en el binario: **+2196 B de flash** (1235392 → 1237588, 62 % de la
partición) y **0 B de RAM dinámica** — la cola vive en RTC slow memory, que no
entra en la cuenta de variables globales. El baseline lo saqué compilando `main`
en un worktree temporal, ya removido.

**Mutación (que el auditor no se apruebe solo):** probé 9 mutaciones —
`READING_UID_ENABLED` en 0, índice parcial, timeout de vuelta en 5000, sacar
`applyTimeouts`, sacar el `on_conflict` de la URL, sacar el `resolution=`, sacar
`r.uid`, `BACKLOG_SLOTS` en 0, y renombrar la columna en la migration. **Las 9
hacen fallar los tests, ninguna sobrevive.** La primera vuelta, una sí
sobrevivía: el auditor buscaba `on_conflict=reading_uid` como texto y lo
encontraba en un **comentario**. Se estaba aprobando leyendo su propia
documentación. Ahora saca los comentarios antes de buscar.

## ⚠️ Lo primero al mergear: el orden importa

1. Correr `backend/supabase/migrations/20260822000000_readings_idempotency.sql`.
2. **Después** flashear / OTA el firmware.

Al revés, PostgREST contesta `400 PGRST204` ("column readings.reading_uid does
not exist") a **todos** los POST y se pierde el 100 % de las lecturas. Si hay que
flashear primero por lo que sea, `READING_UID_ENABLED 0` en el `config.h` del
emisor: queda la cola local sin la clave.

## Lo que NO pude verificar (necesita hardware / la nube)

- La migration corrida de verdad y una fila real con `reading_uid` no nulo.
- **El duplicado a mano**: postear dos veces el mismo body con el mismo uid y
  confirmar que queda 1 fila y que el segundo POST vuelve 2xx (no 409).
- **La cola punta a punta**: apagar el AP, dejar pasar 3 wakes, prenderlo y ver
  llegar las 3 con `backlog=true` y `age_s` creciente.
- **El desborde**: 15 wakes sin cobertura → llegan 12, `rtc_backlog_lost` = 3.
- **El salt**: cortar la alimentación (no un reset) y confirmar que cambia el
  `run_id` del uid.
- Duplicados ya acumulados en la base:
  `python tools/check_reading_idempotency.py --sql`.

Detalle completo en `docs/reading-idempotency.md` del branch.
