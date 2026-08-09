# Nocturno local — 2026-08-09

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (P1 — PLATA).
**Branch:** `nocturno/local-2026-08-09-aislamiento-tenant` (pusheado, commit `3fb5e33`).

## Tarea elegida y por qué

Por rotación tocaba frioseguro (las tres noches previas fueron datalogger,
galgas y datalogger; la última de frioseguro fue el 08-07). Y la jerarquía manda
PLATA.

Repasé el `QUE_FALTA`: los 🔴 sin branch son hardware (flashear, caja estanca),
piloto casero o decisiones de precio de Matías. Los 🟡 sin branch son banco
(SIM800, OTA, NTP) o comercial. Todo lo que era software puro y offline ya tiene
branch.

Así que fui a la pregunta que el documento **da por respondida sin haberla
verificado nunca**. La definición de "vendible" de la primera página dice:

> *"…con **credenciales únicas por cliente**…"*

y el ítem #4 la lista como pendiente. Pero nadie midió **qué cuesta no tenerla**.
FrioSeguro se vende como abono a varios comercios **contra una sola base**: no hay
un Supabase por cliente. Lo único que separa los datos del comercio A de los del
comercio B es el RLS del proyecto.

La pregunta que elegí responder:

> **¿Qué puede hacer con los datos de un comercio alguien que sólo tiene la anon
> key pública —está en el bundle de Netlify y en el flash de cada ESP32— o que es
> un cliente logueado de otro comercio?**

Es la pregunta que hay que poder contestar **antes del segundo abono**, no
después: con dos comercios en la misma base, esto deja de ser deuda técnica y
pasa a ser un problema con un tercero adentro.

**No pisa ningún branch previo.** Los 14 de frioseguro son resumen mensual, vista
de estabilidad, secretos, lint de provisioning, modelo de alertas, gate de
Telegram, drift de columnas y superficie LAN del REVIVAL. El del 08-03-b audita
**qué columnas** existen; éste empieza un escalón antes: **quién puede tocarlas**.

## Qué hice

**`tools/check_tenant_isolation.py`** (stdlib, solo lectura, sin nube ni
hardware). Replaya el SQL canónico en el orden del RUNBOOK de bootstrap, arma el
modelo efectivo de RLS —policies **y** grants— y lo cruza con lo que el firmware
y el dashboard realmente ejercen. Exit 0/1/2/3, `--json`, `--fail-on`, `--root`.

Lo que hubo que resolver, y las tres cosas cambian el resultado:

- **`migration_fixes_2026-07-13.sql` es canónico y la checklist del RUNBOOK no lo
  incluye.** Su encabezado dice *«YA APLICADOS en ese proyecto vía Management
  API»*. Sin él, el checker reporta que el auto-registro del firmware está
  denegado: **un hallazgo falso**. Con él aparece el verdadero
  (`anon_insert_devices` es `WITH CHECK (true)`). **Y el problema no es sólo del
  checker:** el «Resumen de orden (checklist copy-paste)» del RUNBOOK lista los
  pasos 1-10 y no lo nombra — un bootstrap nuevo hecho al pie de la letra se come
  otra vez el `42501` del auto-registro, que es justo lo que ese archivo dice
  existir para evitar. Fix de una línea, anotado.
- **El idioma `DO $$ BEGIN CREATE POLICY … EXCEPTION … END $$;`.** Si el cuerpo
  `$$` no se abre, la policy que crea es invisible: el checker dice `denied` donde
  hay acceso libre. Es la diferencia entre "cerrado" y "abierto de par en par"
  leyendo el mismo archivo.
- **Una policy decide QUÉ FILAS, un grant decide QUÉ COLUMNAS** — hacen falta los
  dos. Por eso el modelo sigue `GRANT`/`REVOKE`, y respeta que **un GRANT suma,
  nunca resta**: un `GRANT UPDATE (status)` sin `REVOKE` previo no acota nada.
  (Mismo razonamiento errado que el H1 de la noche del contrato de schema de
  galgas, en la otra base.) Sin esto, la migración propuesta no tendría oráculo.
- **El verbo del firmware no vive cerca de su URL.** El `POST` de `readings` está
  ~40 líneas debajo del `http.begin()` (en el medio se arma el JSON). Con una
  ventana fija de 25 líneas el checker concluye que **el firmware no inserta
  readings** — justo al revés de la verdad, y encima en la dirección que absuelve.
  Hay que cortar por la URL siguiente, no por un número.
- **Las columnas no vienen una por línea.** Partir el `CREATE TABLE` por saltos de
  línea pierde todas menos la primera, y sin `device_id` una tabla **deja de
  parecer multi-tenant**: los hallazgos de fuga desaparecen solos, en silencio.
  Hay que partir por comas de nivel 0 (`DECIMAL(5,2)` tiene una coma que no
  separa nada).

**`tools/test_check_tenant_isolation.py` — 71 tests en 7 capas:** utilidades de
texto SQL, semántica de policies, replay del schema, lectura del uso real del
firmware y del dashboard, **un test por código de hallazgo con repos sintéticos
armados en disco** (más un **control negativo**: un repo limpio no dispara nada),
la regresión sobre el repo real y el CLI.

**`supabase/migration_2026-08-09_tenant_isolation.sql`** — propuesta, **NO
aplicada**. **`docs/tenant-isolation.md`** — el análisis completo.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **16 tablas, 16 con RLS, 37 policies → 18 error / 6 warn / 7 info.**

### H1 — la anon key es una llave maestra, no una credencial de dispositivo

Las policies de las tablas de datos son
`auth.role() = 'anon' OR user_has_device_access(device_id)`, o directamente
`true`. La rama tenant es correcta y **se ejerce de verdad** cuando el usuario
está logueado (el dashboard manda su JWT, no la anon key — eso está bien hecho).
Pero la rama `anon` la anula para cualquiera que use `curl` en vez del navegador:
un GET a `/rest/v1/devices?select=*` con la key del bundle devuelve **los devices
de todos los comercios**. Ídem `readings`, `alerts`, `commands`, `sensor_probes`.
**El aislamiento entre clientes existe en la aplicación, no en la base** — y para
vender el segundo abono hay que poder afirmarlo al revés.

### H2 — con la anon key se le puede cambiar el firmware a toda la flota

`migration_ota_updates.sql:45`: `FOR UPDATE USING (true)`, **sin `WITH CHECK`** —
y Postgres reusa el `USING` para la fila nueva: escritura libre de cualquier
columna de cualquier fila. `file_url` es de donde cada placa baja el binario
(`supabase.h:597`, `dlHttp.begin(fileUrl)`), **sin validación de host, sin firma y
sin SHA** (el REVIVAL sí compara SHA; este camino, el de las placas de comercio,
no). Un `PATCH` con la key pública y en ≤30 s —el período de chequeo— las placas
flashean lo que se les indique. **Es ejecución de código arbitrario sobre el
equipo instalado en el comercio del cliente, sin credencial.** Mismo hallazgo que
el H1 de la noche del REVIVAL, por el otro lado: allá se entra por la LAN del
sitio, acá por internet contra la nube.

### H3 — los umbrales de alerta y la suscripción son escribibles

El mismo UPDATE libre sobre `devices` alcanza `temp_max`, `temp_critical` y
`alert_delay_sec` → **el servicio deja de avisar, que es literalmente lo que se
cobra**, y sin rastro visible: el dashboard muestra la config nueva como si
siempre hubiera sido esa. Y `subscription_status` / `subscription_expires_at` →
el `suspend_expired_devices()` queda decorativo. (Detalle: el firmware ya se
auto-asigna `subscription_status = "active"` al registrarse, `supabase.h:162`.)

### H4 — seis tablas de historial: cualquiera lee y **borra**

`door_events`, `power_events`, `defrost_sessions`, `maintenance_logs`,
`config_history`, `daily_stats` tienen `FOR ALL USING (true) WITH CHECK (true)`.
`FOR ALL` cubre los cuatro verbos: incluye **DELETE**, que ningún consumidor del
repo ejerce. El historial de puertas y de cortes de luz —el respaldo de *"el
servicio avisa"* si alguna vez hay un reclamo— se puede vaciar con la key
pública. Y sin filtro de tenant, **un cliente logueado ve el historial de los
demás**: es la fuga que sobrevive aunque mañana el firmware deje de usar la anon
key.

### H5 — dos operaciones que informan éxito y afectan cero filas

PostgREST no devuelve error cuando una operación toca 0 filas, así que el caller
lo lee como éxito:

- **`DELETE devices` del firmware** (`supabase.h:112-118`), la limpieza del
  registro fantasma `00:00:00:00:00:00`: no hay ninguna policy de DELETE sobre
  `devices`. El firmware chequea `if (delCode == 204 || delCode == 200)` e imprime
  **`[SUPABASE] Fantasma 00:00:00 eliminado`**. El fantasma sigue ahí.
- **`PATCH readings` del dashboard** (`supabaseClient.js:428`), el paso 3 del
  botón SILENCE: `readings` tiene policy de SELECT y de INSERT, **ninguna de
  UPDATE**. (Hoy ese paso ni se alcanza: el paso 2 patchea
  `devices.alert_acknowledged_remote`, columna que no existe → 400 → el `catch` se
  lo come. Eso es drift de columna, dominio del branch del 08-03-b; se anota
  porque explica por qué H5 nunca se notó.)

Es el mismo patrón que el H2 del REVIVAL y el H3 de la nube del datalogger: **el
sistema le informa éxito al operador por un camino que no verificó.**

### H6 / H7 / H8

- **H6 (warn ×2)** — `readings` y `alerts` aceptan INSERT `WITH CHECK (true)`: se
  pueden **fabricar lecturas y alertas a nombre de cualquier device** (una de
  +5 °C tapa una real). Sin credencial por dispositivo **no hay fix**: el firmware
  se autentica con la misma key que el atacante. Es el ítem #4, y esto es su
  costo.
- **H7 (warn ×4)** — `wifi_commands`, `sim800_status`, `at_commands`,
  `door_sensors`: el código las usa y el SQL canónico no las crea (ya
  inventariadas por el 08-03-b). Se listan porque **una tabla que no existe no
  tiene RLS**: el día que se creen a mano hay que crearlas con policy o nacen
  abiertas.
- **H8 (info ×7)** — superficie que **nadie usa**: el SELECT/UPDATE/DELETE de las
  seis tablas de historial y el INSERT de `sensor_probes`. Se cierran sin romper
  nada: es la parte gratis.

### Lo que está BIEN y queda fijado por test

Tan importante: es lo que **no** hay que ir a revisar.

- **Ninguna tabla se quedó sin RLS.** Las 16 lo tienen; el bootstrap del 07-13 no
  se salteó ninguna.
- **El lado de cuentas y plata está bien aislado:** `user_profiles`,
  `user_device_access` y `payments` no tienen **ninguna** rama anon — todo pasa
  por `is_admin()` o `auth.uid()`. Un cliente no ve los datos ni los pagos de
  otro.
- **El dashboard manda el JWT del usuario** (`supabaseClient.js:40`), no la anon
  key: la rama tenant se ejerce de verdad. El problema es la otra rama.
- **`ota_updates` sólo acepta INSERT de autenticados**: crear una campaña de OTA
  nueva requiere sesión. Lo que falta es acotar el UPDATE.
- **Ningún `.sql` suelto del repo afloja el RLS actual** (control positivo):
  correr por error una de las `migration_*` viejas que el RUNBOOK manda no correr
  sería un no-op, no un agujero nuevo.

## La migración propuesta (NO aplicada)

`supabase/migration_2026-08-09_tenant_isolation.sql`, idempotente y con sus 5
verificaciones escritas. Cierra lo que se puede cerrar hoy: parte las 6 policies
`FOR ALL` en INSERT-anon + SELECT-tenant (H4), y acota por **columna** el UPDATE
de `ota_updates` (H2) y de `devices` (H3) con `REVOKE` + `GRANT` de las columnas
que el firmware realmente escribe.

Con ella en la lista canónica el checker baja de **18 a 14 errores** y de 7 a 3
info. **Lo que queda, dicho con todas las letras:** H1, H6 y el SELECT abierto
siguen ahí — son el ítem #4, no una policy. Y **H2 baja de severidad pero no
desaparece**: con `file_url` protegida ya no se puede servir un binario propio,
pero `status` sigue siendo escribible por necesidad (la placa reporta su
progreso), y poner en `pending` una fila vieja **fuerza un downgrade de la flota a
un firmware ya publicado**.

**No la apliqué**: cambiar RLS es tocar producción.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-09-aislamiento-tenant
python tools/check_tenant_isolation.py                  # -> 18 error / 6 warn / 7 info, exit 1
python tools/check_tenant_isolation.py --json
python tools/check_tenant_isolation.py --fail-on info
python -m unittest tools.test_check_tenant_isolation    # -> Ran 71 tests, OK
```

H2 se comprueba sin la herramienta, leyendo dos líneas:
`migration_ota_updates.sql:45` contra `firmware_modular/supabase.h:597`, y
preguntándose **de dónde salió ese `fileUrl`**.

`TestRepoReal` **fija los 31 hallazgos**: si alguien arregla uno, el test falla y
obliga a actualizar `docs/tenant-isolation.md` en el mismo commit.

**Verificado por mutación** (las 4 hacen fallar la suite): no abrir el bloque
`DO $$`, ventana fija de 25 líneas para el verbo del firmware, no reusar `USING`
cuando falta `WITH CHECK` en un UPDATE, y sacar `migration_fixes_2026-07-13.sql`
del set canónico.

## Qué quedó sin verificar (nube — trabajo de día)

Todo está **leído del repo, no observado**. En orden de valor:

1. **La primera consulta, la que dirime todo:**
   ```sql
   select tablename, policyname, cmd, qual, with_check
   from pg_policies where schemaname = 'public' order by tablename, policyname;
   ```
   La herramienta audita **lo que el repo dice**, no lo que está corrido en
   `cjdluhemschrynijzvap`. Hasta esa consulta, la tabla de capacidades es la del
   repo.
2. **H2 en un minuto, con una placa de banco (NO con una instalada):** PATCHear
   `file_url` de una fila de `ota_updates` con la anon key y ver si responde 204.
   **No hace falta llegar a flashear nada para confirmarlo** — con que el PATCH
   sea aceptado, está.
3. **H5 en dos comandos:** `DELETE /rest/v1/devices?device_id=eq.00:00:00:00:00:00`
   con la anon key → si devuelve 204 con 0 filas borradas, el mensaje del firmware
   miente. Ídem `PATCH /rest/v1/readings?...` con `Prefer: return=representation`
   → `[]`.
4. **Aplicar la migración** + sus 5 verificaciones, con la placa prendida para
   confirmar que el heartbeat sigue avanzando (si se congela, quedó una columna
   fuera del GRANT: PostgREST rechaza el UPDATE **entero**, no ignora la columna).
5. **Agregar `migration_fixes_2026-07-13.sql` a la checklist del RUNBOOK de
   bootstrap** (una línea).

- **No compilé firmware ni bajé toolchains** (regla de disciplina de tiempo). La
  auditoría es estática.
- **No corrí `npm run build`**: no toqué `web-dashboard/`. Sólo lo leo.
- **No ejecuté ningún `curl` contra la nube.** Los ejemplos del doc son lo que el
  modelo predice, no lo que se observó.
- **No toqué el trabajo de día sin commitear** (`firmware_revival/`,
  `kit_santacruz/`, `REVIVAL_2026-08.md`, el `.zip`): no lo commiteé ni lo
  modifiqué.
- **Ningún fix aplicado** — generator ≠ evaluator, y el más importante (H1) es una
  decisión de arquitectura con dueño.

## Estado

- Branch `nocturno/local-2026-08-09-aislamiento-tenant` pusheado (1 commit,
  `3fb5e33`: 5 archivos). frioseguro volvió a `main` limpio.
- `QUE_FALTA.md` de frioseguro: ítem **#20** + nota en el **#4** (en el branch).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Sexta noche que lo reporto:** es un firmware que va a un equipo a 2000 km y
  vive **sólo en este disco**. **No lo toqué.**
- ℹ️ `C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main` (estado previo, no lo
  hice yo). **No lo cambié.**
- ℹ️ `C:\Proyectos\datalogger` tiene sin trackear `docs/CONEXIONES_LAB.html`
  (previo, no lo hice yo). **No lo toqué.**
- ⚠️ Queda el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando Matías quiera.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las once
  noches anteriores: `agentes/{esquematico,pcb}.md`,
  `dominios/{comms,diseno,esquematico,firmware,hardware,logo_acceso_remoto,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md`,
  `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html`,
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- La cola de merge suma **48 branches** en origin (galgas 17, datalogger 15,
  frioseguro 15, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo y
  sin usar: falta la sesión humana.
  **Nota de prioridad:** de los 15 de frioseguro, éste es el único que responde
  una pregunta que **caduca con el segundo cliente**. La migración es de una
  sesión de SQL Editor y no toca firmware; H1 es lo que hay que decidir **antes**
  de prometerle a un comercio que sus datos están separados de los del de al
  lado.
