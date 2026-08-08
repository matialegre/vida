# Nocturno local — 2026-08-07 (2do turno, "-b")

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-07-b-contrato-schema` (pusheado, commit `90f583d`).

## Tarea elegida y por qué

El 1er turno de hoy fue a frioseguro (superficie LAN del REVIVAL), los de ayer a
galgas y datalogger. Por rotación tocaba galgas, y ahí revisé los ítems del
`QUE_FALTA` que **no** están ya esperando en un branch: el #1 (RX completo), el
#2 (galga física), el #3 (LiPo) y el #4 (reflashear B) son firmware+hardware. Los
🟡 sin branch eran el **#5 (OTA que distinga A/B)**, el **#6 (bucket público)** y
el **#8 (migración SQL pendiente de correr)** — los tres del mismo dominio.

Los tres son la misma pregunta sin responder:

> **¿qué schema tiene realmente esta base, y coincide con lo que el código
> supone?**

Elegí auditar eso. La base es la única pieza de galgas que **tres consumidores
tocan a la vez sin verse entre sí**:

```
backend/supabase/migrations/*.sql  ──▶  schema efectivo
                                         ▲            ▲
            firmware (POST/PATCH ────────┘            └──── dashboard web
            /rest/v1/…, anon key                            (.from().select(),
            en el flash del ESP32)                           anon key en el bundle)
```

Y el modo de falla de esa cadena **no es un crash**:

| Falla | ¿Se nota? |
|---|---|
| El firmware manda una columna que no existe | sí — 400 PGRST204… si alguien mira el código de retorno |
| **Un CHECK constraint rechaza un comando** | **NO** — el botón existe en la UI y el error se lo come un catch |
| **Una columna que el dashboard dibuja nunca se llena** | **NO** — muestra un guion, que se lee como "todavía no llegó" |
| **Un grant no restringe lo que su comentario dice** | **NO** — todo funciona, y por eso nadie lo revisa |

**Encaja con el trabajo previo sin pisarlo.** Los 16 branches anteriores de
galgas son vpp/umbrales, energía, alertas, linaje y OTA, readme-drift, contrato
de comandos e identidad de binarios. Ninguno mira **el schema**. El del 08-04
(contrato de comandos) audita el flujo de un comando; **éste empieza un escalón
antes**: si la tabla acepta el comando siquiera.

## Qué hice

1. **`tools/check_schema_contract.py`** (stdlib, solo lectura, sin red ni
   hardware). Lo que hizo falta resolver:
   - **Replayar las 15 migraciones en orden, no leer la última.** El schema
     efectivo sale de aplicarlas: `add column if not exists` múltiple en un solo
     `alter`, policies que se crean y se dropean, grants de columna, y sobre todo
     el `drop constraint` + `add constraint` que **reescribe el CHECK completo**.
     Guardar el **historial** de esa reescritura es lo que hace visible el H4 — un
     checker que sólo mira el estado final no puede saber que algo estuvo antes.
   - **`supabase.storage.from('firmware')` no es una tabla.** Sin esa distinción
     el checker inventa una tabla `firmware`, le cuelga el insert de la línea de
     abajo (que es de `firmware_versions`) y reporta un error grave que no existe.
     Lo tuve puesto y lo saqué: era el hallazgo más ruidoso de la primera corrida.
   - **Las claves de un sub-objeto `jsonb` no son columnas, pero el sub-objeto
     sí.** `createNestedObject("metadata")` **crea** la columna `metadata`;
     `meta["firmware_version"]` vive adentro del jsonb. Contar mal cualquiera de
     los dos lados produce hallazgos falsos en direcciones opuestas: columnas
     inexistentes por un lado, columnas muertas por el otro.
   - **`out->campo` cuenta igual que `r.campo`.** `samplerComputeReading()` recibe
     `Reading*` y escribe con flecha. Buscando sólo el punto, el checker daba por
     "nunca calculadas" a `v_mean`, `v_rms` y `v_pp`: **media tabla acusada por un
     carácter.** Con la flecha, el hallazgo se reduce a lo que efectivamente no se
     calcula.
   - **Sacar comentarios sin romper strings** (misma lección que las noches del
     contrato de la nube y del REVIVAL): `config.h` tiene `"https://…"` y ese `//`
     no es un comentario. Y en SQL, los cuerpos `$$…$$` de plpgsql tienen `;`
     adentro que **no** separan statements.

   Exit 0/1/2, `--json`, `--fail-on`, `--root`. Sirve de gate antes de correr una
   migración nueva o de re-deployar el dashboard.

2. **`tools/test_check_schema_contract.py` — 85 tests en 7 capas:** utilidades de
   texto, replay de migraciones, parser del firmware, parser del dashboard, **un
   test por código de hallazgo con repos sintéticos armados en disco**, la
   **regresión sobre el repo real** y el CLI. Verificados **por mutación**: no
   distinguir el bucket de Storage, no podar `build/`, no sacar las claves del
   jsonb, tratar el inicializador del struct como una medición real, y buscar sólo
   `.campo` sin `->campo` — **las cinco hacen fallar la suite.**

3. **`docs/schema-contract.md`** + ítem **#16** en `QUE_FALTA.md` y notas en los
   **#5, #6 y #8**.

## Hallazgos (con test que los demuestra — NO corregidos, generator ≠ evaluator)

Corrida real: **15 migraciones, 5 tablas, 69 columnas, 15 escrituras del
firmware, 7 lecturas del dashboard, 12 policies → 3 error / 5 warn / 2 info.**

- **H1 (error) — el modelo de permisos de `devices` no puede ser el que dice el
  comentario.** La migración `20260427230000` hace
  `grant update (local_ip, local_ip_at) on devices to anon` y escribe al lado,
  textual: *«Otras (mac, firmware_version, etc) siguen bloqueadas»*. El RX, **con
  la misma anon key**, PATCHea en cada heartbeat ocho columnas
  (`esp_rx_receptor.ino:296-304`), y **siete están fuera del grant**. Las dos
  cosas no pueden ser ciertas a la vez, y cuál es la verdadera cambia por
  completo qué hay que hacer:
  - **(a) si el grant manda**, Postgres rechaza el UPDATE **entero** — no ignora
    las columnas de más — y con él se cae `local_ip`, que es **cómo los emisores
    encuentran al RX sin mDNS**: el bloqueante #1.
  - **(b) si el PATCH viene funcionando**, es porque el rol ya tenía UPDATE a
    nivel tabla y el `grant` de columna **no revocó nada** — un GRANT suma, nunca
    resta. Entonces la restricción prometida no existe y cualquiera con la anon
    key reescribe toda la fila, incluida `mac`.

  Supabase concede `GRANT ALL … TO anon` por default sobre las tablas nuevas de
  `public`, así que **(b) es lo más probable** — pero eso lo leí de la doc, no lo
  observé. Se decide con `select has_table_privilege('anon','devices','UPDATE');`
  **Detalle que el checker deja fijado:** `connected_ssid` se agregó **sin** su
  `grant update`, a diferencia de `local_ip` y de los `cal_*` que sí lo tienen. El
  patrón de la migración anterior no se siguió — lo cual sólo pasa inadvertido si
  el grant nunca importó.

- **H2 (error) — el OTA por device choca contra el unique. Es el ítem #5, y no
  falta lo que el ítem dice que falta.** `20260426170000` agregó `device_id` a
  `firmware_versions` para apuntar una versión a un equipo concreto, pero el
  `unique (device_type, version)` del schema inicial **quedó igual y no lo
  incluye**. Subir la versión `3.6.4` para A y después la misma para B **falla con
  23505** en el segundo — y el dashboard ya manda `device_id` en cada subida, así
  que el camino roto es el que se usa. Para distinguir A de B hay que inventar
  versiones distintas del mismo binario, **que es exactamente lo que la columna
  venía a evitar**. El ítem #5 no está esperando una columna: está esperando un
  `drop constraint` + `unique (device_id, device_type, version)`.

- **H3 (error) — el dashboard dibuja ΔV y el firmware nunca la manda.** `App.jsx`
  muestra un metric **ΔV** alimentado por `readings.delta_v`, y el `select` la pide
  explícitamente. Del otro lado,
  `supabase_client.cpp:113` la escribe sólo dentro de
  `if (!isnan(r.delta_v))` — y el único valor que ese campo recibe **en todo el
  firmware** es `NAN` (`adc_sampler.cpp:135`, ídem B), más el `0.0f` del
  inicializador. **La condición nunca es verdadera.** El guard está bien escrito y
  el sampler documenta quién debería calcularla: *«eso lo hace la Edge Function»*
  — **esa Edge Function no existe en el repo**. El dato tiene dueño asignado y el
  dueño no fue creado. Lo que importa no es el NULL sino cómo se lee: el widget no
  dice "sin dato", dice un guion, y un guion en un tablero se lee como *"todavía
  no llegó"*. Delante de Dreyfus, ΔV es **la comparación entre las dos galgas**: el
  número que a un tercero le va a resultar natural pedir. (`ratio` está igual y no
  se reporta sólo porque el dashboard todavía no la dibuja.)

- **H4 (warn) — `set_config` quedó inalcanzable.** El CHECK de `commands.cmd` se
  reescribió **entero** cinco veces. En la quinta
  (`20260428000000_add_calibration_columns.sql`) la lista se reordenó por familias
  —legacy / ota_wm_pp / calibración— y en el reordenamiento **se perdió
  `set_config`**. El firmware lo sigue entendiendo (`protocol.h:189` y `:210`), así
  que el código se lee como si el comando existiera; no hay forma de encolarlo.
  Reemplazar un CHECK completo es justamente la operación que hace fácil perder un
  valor sin notarlo, y no había test que lo agarrara: **el constraint vive en el
  SQL y el handler en C++.**

- **H5 (warn ×2) — `commands` y `firmware_versions` aceptan cualquier insert de
  `anon`** (`with check (true)`). La anon key está en el bundle público del
  dashboard y en el flash de los ESP32: es pública de hecho. Con ella se pueden
  **encolar comandos a los devices de Dreyfus** (`reboot`, `factory_reset`, `ota`)
  y **publicar filas en `firmware_versions`**. Vale la comparación interna: la
  policy de `readings` del mismo repo al menos exige que el `device_id` exista.
  **El criterio existía y no se aplicó acá.**

- **H6 (warn) — la policy de ack no acota columnas, aunque su comentario dice que
  sí.** `update_commands_anon_ack` promete: *«Solo permitimos cambiar status,
  ack_at, error_msg, delivered_at. No permitimos cambiar device_id ni cmd ni
  payload (eso sería spoofing)»*. La policy no implementa nada de eso: **una
  policy de UPDATE decide qué FILAS se tocan, nunca qué COLUMNAS** (para columnas
  hacen falta grants, y `commands` no tiene ninguno). Cualquier fila que pase el
  filtro se puede reescribir entera: cambiarle el `cmd` a un pending, cambiarle el
  `payload`, reasignarlo a otro device. **Es literalmente el spoofing que el
  comentario dice estar previniendo** — el mismo error de razonamiento que H1, en
  la otra tabla.

- **H7 (warn) — el bucket de firmware es `for all`**, o sea **DELETE y UPDATE**
  también, no sólo lectura y subida. Cualquiera con la anon key puede borrar o
  reemplazar un binario publicado mientras `storage_path` sigue apuntando ahí: el
  ESP32 pide el archivo y recibe lo que haya quedado, o un 404 en medio de un OTA.
  El ítem #6 lo tenía anotado como "bucket PÚBLICO"; queda documentado que es más
  ancho que eso.

- **H8 (info ×2) — columnas muertas:** `events.acknowledged_at`/`acknowledged_by`
  (el flujo de reconocer alertas no existe en ningún lado) y
  `readings.waveform_path`.

**Lo que está BIEN y queda fijado por test** (tan importante: es lo que NO hay
que ir a revisar):

- **No hay ninguna columna inventada.** Las 15 escrituras del firmware y las 7
  lecturas del dashboard nombran **sólo columnas que existen**. El contrato de
  nombres está sano en las dos direcciones: no hay ningún PGRST204 esperando.
- **Ningún botón del dashboard encola un comando que el CHECK rechace.** Los 22
  comandos de `defaultPayload()` están todos en la lista del constraint final.
- **`metadata` viaja de verdad**, y con ella `firmware_version` — que es lo que el
  trigger `touch_device_on_reading` lee para reflejar el OTA en `devices` sin
  comando dedicado. La cadena reading → trigger → `devices.firmware_version`
  cierra.
- **El PATCH que publica `local_ip` existe y manda lo que promete el PLAN v5**: el
  descubrimiento sin mDNS está cableado. Es justo lo que H1 pone en duda, y por eso
  H1 es error y no warn.
- **`v_pp`, `v_rms`, `v_mean`, `sigma`, `battery_v`, `rssi`, `in_alert` y `stage`
  cierran de punta a punta**: los calcula el sampler, los postea el sketch, los
  guarda la tabla, los dibuja el dashboard. **La telemetría que sostiene la
  detección de alerta está completa**; lo roto es lo que se le montó alrededor.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-07-b-contrato-schema
python tools/check_schema_contract.py                  # -> 3 error / 5 warn / 2 info, exit 1
python tools/check_schema_contract.py --json
python tools/check_schema_contract.py --fail-on warn
python -m unittest tools.test_check_schema_contract    # -> Ran 85 tests, OK
```

Gate antes de correr una migración nueva:
`python tools/check_schema_contract.py && supabase db push`

H2 se comprueba sin la herramienta, leyendo dos líneas:
`unique (device_type, version)` en `20260425000001_initial_schema.sql` contra
`add column … device_id` en `20260426170000_firmware_per_device.sql`, y
preguntándose **qué pasa cuando A y B comparten versión**.

Los tests de `TestRepoReal` **fijan los 10 hallazgos de hoy**: si alguien arregla
uno, el test falla y obliga a actualizar `docs/schema-contract.md` en el mismo
commit.

## Qué quedó sin verificar (nube — trabajo de día)

Todo está **leído del código, no observado**. En orden de valor:

1. **H1, la pregunta que cambia todo:**
   `select has_table_privilege('anon','devices','UPDATE');` — decide si el modelo
   de permisos documentado existe o es ficción. **Es la primera que haría.**
2. **H2 en un minuto:** subir el mismo `version` para A y para B desde la pestaña
   Firmware. Si el segundo tira 23505, el ítem #5 tiene fix conocido.
3. **H3 en una consulta:** `select count(*) from readings where delta_v is not null;`
   Si da 0, el ΔV del dashboard nunca mostró nada.
4. **H4:** `insert into commands (device_id, cmd) values ('TEST','set_config');`
   → 23514 esperado.
5. **⚠️ El límite de esta auditoría, escrito para no confundirlo:** la herramienta
   audita **lo que las migraciones dicen**, no lo que está corrido en el proyecto
   Supabase. El ítem #8 del `QUE_FALTA` dice justamente que hay migración
   pendiente de correr, así que **los dos pueden no coincidir**. `supabase db diff`
   o `\d devices` desde el SQL Editor lo dirime — y hasta entonces, el schema
   efectivo de `docs/schema-contract.md` es el del repo, no el de producción.

- **No compilé firmware ni bajé toolchains** (regla de disciplina de tiempo). La
  auditoría es estática.
- **No corrí `npm run build`**: no toqué `web/`. Sólo lo leo.
- **No entré a `data/field_captures`** (sagrado, read-only). No lo necesita.
- **Los fixes son de SQL y de firmware.** **Ninguno aplicado** — generator ≠
  evaluator, y H1 en particular no se puede arreglar bien sin la consulta de
  arriba.

## Estado

- Branch `nocturno/local-2026-08-07-b-contrato-schema` pusheado (1 commit,
  `90f583d`: 4 archivos). galgas volvió a `main` limpio.
- `QUE_FALTA.md` de galgas: ítem **#16** + notas en el **#5**, el **#6** y el
  **#8** (en el branch).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Cuarta noche que lo reporto, y ahora con urgencia:** es un firmware que va a
  un equipo a 2000 km esta semana y hoy vive **sólo en este disco**. **No lo
  toqué.**
- ℹ️ **`C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main`** (estado previo, no lo
  hice yo). **No lo cambié.**
- ⚠️ **Queda el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota`** en
  galgas (0 commits; su contenido ya está adentro del branch del 08-06).
  `git branch -d` cuando Matías quiera.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las nueve
  noches anteriores: `agentes/{esquematico,pcb}.md`,
  `dominios/{comms,diseno,esquematico,firmware,hardware,logo_acceso_remoto,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md`,
  `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html`,
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- La cola de merge suma **46 branches** en origin (galgas 17, datalogger 14,
  frioseguro 14, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo y
  sin usar: falta la sesión humana.
  **Nota de prioridad:** de los 17 de galgas, éste es el único que **desbloquea un
  ítem del `QUE_FALTA` sin escribir firmware**. H2 es el ítem #5 completo y el fix
  son dos líneas de SQL; H1 es una consulta que hay que hacer **antes** de darle a
  Dreyfus el número de qué puede tocar quién esté en la red de planta.
