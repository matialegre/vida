# Nocturno local — 2026-08-27 (segunda pasada, "-b")

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la jerarquía).
**Branch:** `nocturno/local-2026-08-27-b-columnas-fantasma` (pusheado, `b76a4f1`).
**Sale de:** `main` (`ddf5134`). **No colisiona con el `08-27` de la primera pasada de
esta misma noche** (`el-testigo-que-certificaba`): archivos distintos, los dos salen de
`main`, se mergean en cualquier orden.

## TL;DR

> **La primera pasada de esta noche arregló la compuerta. Esta encontró que del
> otro lado la base rechaza la fila entera.**

El firmware manda campos que no son columnas. PostgREST **no ignora la clave de
más**: contesta **HTTP 400** (`PGRST204`) y descarta la fila **completa**. No
inserta "lo que puede": no inserta nada.

Y del lado del equipo, todo lo que queda es esto:

```c
Serial.printf("[SUPABASE] ✗ Lectura error: %d\n", code);
```

Un `printf` por el puerto serie. A 1500 km no lo lee nadie. El equipo se ve
**verde** en el panel (el heartbeat a `devices` es un PATCH aparte y ése sí
entra), la fila de `readings` no llega nunca, y el gráfico simplemente no crece.

**Verificado contra la base VIVA, no contra los `.sql` del repo:**
`firmware_modular` —**la familia que se flashea para los abonos**— **no puede
insertar una sola lectura** en `vihxmqjjprtlzajlatvu`.

## Por qué esta tarea y no otra

1. **Es PLATA y es el bloqueante #3 del `QUE_FALTA`** ("Migración SQL de columnas
   nuevas"), abierto desde el 7-jul y sin un solo branch en 7 semanas.
2. **Ya se cobró tres veces, y las tres se encontraron a mano.** El propio
   `entrega_scz/docs/SESION_2026-08-26_TELEGRAM_Y_COLUMNAS.md` (informe de Santa
   Cruz, de anteayer) lo dice: `door_open` (~24-ago), `buzzer_on` en `alerts`
   (26-ago, **la primera alerta real de la vida del sistema no se escribió**), y
   nombra el patrón. Nadie había construido el guardarraíl: se sigue descubriendo
   mirando filas y preguntándose por qué la última id no cambia.
3. **Es la continuación exacta de la pasada anterior.** Aquélla arregló el testigo
   de internet (`internetAvailable`, la compuerta de todo lo que se cobra). Esta
   noche quedó demostrado que abrir la compuerta **no alcanza**: el POST sale y
   muere del otro lado, por otro camino, con el mismo final.
4. **Es 100 % software y se verifica sin encender nada.**

## Qué hice

### 1. Fui a la fuente de verdad (y no al papel)

El repo tiene 24 archivos `.sql` que se contradicen. Así que consulté
`information_schema.columns` **de la base viva** por la Management API (token del
CLI de Supabase, Credential Manager; **consulta de sólo lectura, nada de DDL**) y
lo crucé con `backup_supabase/01_columnas.json` (dump del 19-ago). Coinciden:
`readings` tiene **36 columnas** y sigue sin las que hacen falta.

### 2. `tools/check_payload_schema.py` (nuevo, stdlib)

Cruza **cada payload que el firmware escribe** contra el esquema. Corta los
`.ino/.h` en bloques por llave de cierre en columna 0 —que en estilo Arduino es
una función— y de cada bloque saca la tabla (`/rest/v1/<tabla>`), el método y las
claves (`doc["x"] =` de ArduinoJson **y** `\"x\":` del JSON armado a mano).

Tres decisiones que valen la pena:

- **La unidad es el bloque, no "de la URL para abajo".** `log_remoto.h` arma el
  body *antes* de nombrar el endpoint: un parser que mirara sólo hacia abajo no
  encontraría un campo y cantaría "todo OK". Ese falso negativo tiene su test.
- **Los `GET` se ignoran.** Un `?select=` nombra columnas y no inserta; reportarlo
  sería ruido, y un reporte ruidoso no lo mira nadie.
- **Dos modos, y la diferencia entre los dos es el hallazgo.** Contra la base viva
  da 11 columnas fantasma; contra `supabase/*.sql`, 4. Los 7 de diferencia son
  **los que están escritos en un `.sql` del repo y no existen en ninguna base**:
  la definición operativa de "migración sin correr", visible sin abrir Supabase.

### 3. Lo que encontró

**Pérdida de datos** — el equipo mide y no se guarda:

| Familia | Campos sin columna en `readings` |
|---|---|
| `firmware_modular` — **la de los abonos** | `any_door_open`, `local_ip`, `firmware_version` (en **toda** lectura) + `public_ip`, `wifi_ssid`, `wifi_password`, `ping_ms` (**condicionales**) |
| `firmware_revival/` (copia vieja) | `door_open` |
| `kit_santacruz/firmware/…` (copia vieja) | `door_open` |

Lo de **condicional** importa y por eso el checker lo marca: esos cuatro salen de
`if (g_publicIP.length() > 0) …`, así que sólo viajan cuando el equipo ya aprendió
su IP pública / SSID / ping. El 400 **no es permanente: empieza cuando el equipo
termina de arrancar bien**. *"Andaba y de golpe dejó de guardar"* es la firma de
un campo condicional, y es de los síntomas más caros de perseguir.

**Funciones muertas** — los dos extremos escritos, falta el medio:

- **`wifi_commands` no existe como tabla.** El panel la escribe
  (`sendWifiCommand()`), el firmware la lee y la marca
  (`supabaseCheckWifiCommands()` / `_sbUpdateWifiCmd()`). Es **la función que
  evita un viaje cuando al comercio le cambian el router**, y no puede funcionar.
- `devices.wifi_scan_results` / `wifi_scan_at` tampoco existen (firmware
  `_sbUploadScanResults()` → panel `DevicesAdminTable.jsx`).
- `sim800_status` y `at_commands`: línea minera, hoy apagada (`#if HAS_SIM800`).

**Y una familia hablándole a una base que no existe:**

```
firmware_modular   ->  cjdluhemschrynijzvap     <-- uno de los tres refs MUERTOS
```

O sea que hoy tiene **dos fallas apiladas**: le habla a un host que no resuelve
en DNS **y**, si se le corrige la URL, el 400 la espera del otro lado.

### 4. Por qué volvieron

`BOOTSTRAP_2026-08-19.sql` se armó como `SETUP_COMPLETO.sql` +
`migration_ota_updates.sql`. **No incluyó `migration_fixes_2026-07-13.sql`**, que
era la que había agregado esos 7 campos — escrita para el proyecto viejo
(`xhdeacnwdzvkivfjzard`, hoy muerto). Al mudarse de ref, la base se rehízo desde
el setup y **las migraciones sueltas quedaron atrás**.

> La regla que sale: cuando se bootstrapea un proyecto nuevo, el setup tiene que
> ser el **estado final**, no la foto vieja. Una migración que no se pliega al
> setup se pierde en la próxima mudanza.

### 5. `supabase/migration_2026-08-27_columnas_fantasma.sql`

Idempotente: repone las 7 de `readings` + las 2 de `devices` y crea
`wifi_commands` con **el mismo molde y la misma RLS que `commands`** (las columnas
salen de los dos usos que ya existen, no de un diseño nuevo).

**Lo que NO hace, a propósito:**

- **No agrega `door_open`.** Esa columna *no falta*: **sobra en el firmware**. La
  copia buena del revival (`entrega_scz/firmware`, 2.6.19) ya manda `door1_open`.
  Crearla enterraría el bug en el esquema.
- No crea `sim800_status` ni `at_commands` (línea apagada).

**La herramienta reporta el desacuerdo; de qué lado se arregla es una decisión**,
y está escrita en el doc.

`readings.wifi_password` va **porque sin ella la fila entera se rechaza**, no
porque esté bien: el firmware sube la clave WiFi del cliente en cada lectura y el
panel la muestra. Viene marcada como deuda desde el 07-13. El orden correcto es
**sacarla del firmware primero y dropearla después** — al revés se rompe la
familia entera. El `DROP` está escrito y comentado en la migración.

### 6. Los tests son los incidentes

`tools/test_check_payload_schema.py`, **20 tests, OK**. Los **tres primeros son
los tres incidentes reales del proyecto escritos como fixture**: `door_open`,
`buzzer_on` en `alerts`, y el de las migraciones sueltas. Si el checker deja de
cazarlos, se rompe la suite. El resto cubre el parser, que es donde un checker se
vuelve mentiroso: si no encuentra el payload reporta "todo OK" y da tranquilidad
falsa (por eso hay un test que **exige** que haya encontrado el sitio, y otro que
mete payloads rotos en `build/` y `node_modules/` para confirmar que se ignoran).

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-27-b-columnas-fantasma

# 1) los tests
python -m unittest tools.test_check_payload_schema -v      # 20 OK

# 2) el checker sobre el repo, contra la base viva dumpeada
python tools/check_payload_schema.py                       # exit 1
#    -> 11 columnas fantasma, 3 tablas fantasma, 1 divergencia

# 3) el mismo checker contra el papel (los .sql del repo)
python tools/check_payload_schema.py --schema-sql          # exit 1
#    -> 4 columnas fantasma. La diferencia (7) = migraciones sin correr.

# 4) contra un esquema fresco, que es lo que corresponde antes de flashear
python tools/check_payload_schema.py --schema-json esquema_hoy.json
```

Para bajar el esquema fresco:
`select table_name, column_name from information_schema.columns where table_schema='public';`

**Hecho esta noche:** los 20 tests pasan; el checker corre sobre el repo real y
devuelve exit 1; y simulando el esquema **con la migración aplicada**, los 9
hallazgos de base desaparecen y quedan **sólo los que son del firmware** (los dos
`door_open` de las copias viejas y las tablas del SIM800) — que es exactamente lo
que la migración dice que no arregla.

## Lo que quedó sin verificar

- **Que el 400 sea exactamente el que digo.** La cadena está deducida del contrato
  de PostgREST y del historial del proyecto (los dos incidentes de Santa Cruz se
  comportaron así), **no** de un POST hecho esta noche contra la base. Cuesta un
  `curl` con una clave de más: la fila no tiene que aparecer.
- **Que la migración corra limpia.** Es SQL idempotente y las políticas copian las
  de `commands`, pero **no la ejecuté**: tocar el esquema de la base viva no es
  algo que haga un worker nocturno solo.
- **`wifi_commands` punta a punta** (panel → tabla → equipo → `executed`) necesita
  un equipo prendido.

## ⚠️ Cosas que vi y NO toqué (son decisiones tuyas)

1. **Hay tres copias del firmware revival en el árbol**, y no mandan lo mismo:
   `entrega_scz/firmware` (2.6.19, **la buena**, manda `door1_open`) vs.
   `firmware_revival/` (2.6.0) y `kit_santacruz/firmware/firmware_revival/`, que
   siguen con `door_open`. **Un OTA compilado desde la carpeta equivocada
   reintroduce el incidente 1.** Es una línea (`firmware_revival.ino:1108`), pero
   son **archivos sin commitear** y decidir cuál copia sobrevive es tuyo. El
   checker ahora lo reporta como "copias del mismo archivo que mandan cosas
   distintas", que es como se ve una copia vieja **sin mirar el número de versión**.
2. **Sigue habiendo mucho de Santa Cruz sin commitear**: `firmware_revival/`,
   `kit_santacruz/`, `panel-web/`, `entrega_scz/`, `backup_supabase/`,
   `supabase/BOOTSTRAP_2026-08-19.sql`, `supabase/migration_device_logs.sql`, los
   dos ZIP del kit. Es el **hueco #1 del PORTFOLIO** (git + backup offsite) en
   vivo: el trabajo de la semana más importante del proyecto existe en un solo
   disco. Lo mismo que anoche.
3. **La URL de `firmware_modular`** apunta a un ref muerto. Antes de flashear para
   un abono hay que corregirla **y volver a correr el checker**.

## Próximo paso sugerido

1. **@verificador** audita el branch (doctrina: antes de merge).
2. **Correr la migración** en el SQL Editor de `vihxmqjjprtlzajlatvu`. Es
   idempotente. Después, volver a dumpear el esquema y correr el checker: tienen
   que quedar sólo los hallazgos de firmware.
3. **Alinear las copias viejas del revival** y decidir cuál es la canónica.
4. **Plegar las migraciones sueltas al bootstrap**, o el próximo cliente repite
   todo esto desde cero.
5. Sumar `python tools/check_payload_schema.py` al **gate previo a cada flasheo**,
   junto a `tools/lint_device_config.py` (branch 07-12). Los dos contestan la
   misma pregunta desde distinto ángulo: *¿esta placa, tal como está, sirve para
   un cliente?*
