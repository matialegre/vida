# Nocturno local — 2026-08-03 (2do turno, "-b")

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (P1 — PLATA, la palanca de abonos).
**Branch:** `nocturno/local-2026-08-03-b-schema-drift` (pusheado, commit `9c14b5f`).

## Tarea elegida y por qué

El 1er turno de hoy fue a datalogger (P0 octubre). La jerarquía manda **PLATA y
UNIVERSIDAD primero**, así que este turno fue a FrioSeguro — y esta vez a un ítem
🔴 **bloqueante del PRIMER abono**, no a un 🟡:

> **#3 — Migración SQL de columnas nuevas** (`connection_mode`, `gsm_signal`, `free_heap`…)

Es el único 🔴 sin branch que es software puro (los otros son flashear, el piloto en la
heladera, comprar la caja IP65, y decidir precio). Y es el ítem donde el repo **ya se
quemó una vez**: `supabase/migration_fixes_2026-07-13.sql` lo dice textual —

> *"FIX 1 — El firmware manda columnas que SETUP_COMPLETO.sql no creaba → PostgREST 400
> → CERO lecturas guardadas."*

PostgREST **no ignora** una columna desconocida: rechaza el request entero y **pierde la
fila**. Una sola clave de más y el nodo deja de guardar. La defensa contra eso, hasta
esta noche, era **acordarse**. Eso es lo que arreglé: no la nube — el guardarraíl.

Cuidado con el falso amigo: el que lea el ítem #3 va a llegar a
`migration_resilience_v1.sql` y va a creer que ahí está la respuesta. **No.** Ese archivo
apunta al proyecto **viejo** (`xhdeacnwdzvkivfjzard`, que Matías eliminó) y todas sus
columnas **ya vienen dentro de `SETUP_COMPLETO`**. Hay un test que lo fija.

## Qué hice

1. **`tools/check_schema_drift.py`** (stdlib, sin nube ni hardware). Compara:
   - **lado firmware** (`firmware_modular/supabase.h`): `doc["col"] = …`, los bodies JSON
     armados a mano como string, y los `select=` (una lectura de columna inexistente
     también es 400). Cada acceso se atribuye a la tabla del `/rest/v1/<tabla>` **más
     cercano dentro de la misma función** — acotar por función es lo que evita que
     `door1_open` (final de `supabaseSendReading`) se le adjudique al `/alerts` de la
     función siguiente, y medir en valor absoluto es lo que hace que también funcione
     `supabaseSyncSIM800`, donde el doc se arma **antes** del `http.begin`.
   - **lado schema**: los `.sql` que el `RUNBOOK_bootstrap_2026-07-13.md` declara
     canónicos, **en orden de aplicación** (`SETUP_COMPLETO` → `migration_ota_updates` →
     `migration_fixes_2026-07-13`), respetando `DROP`+`CREATE`.

   Exit 0/1/2 como gate pre-flash / pre-bootstrap, `--json`. Verifiqué a mano las 11
   tablas atribuidas: todas correctas.

2. **`supabase/migration_2026-08-03_schema_drift.sql`** — append-only, idempotente,
   con RLS. **NO aplicada** (es cambio de nube).

3. **`tools/test_check_schema_drift.py`** — **37 tests**, en 5 capas: los dos parsers
   contra fuentes sintéticas, el diff, la **regresión sobre el repo real** (la evidencia
   de los hallazgos) y el CLI.

4. **`docs/schema-drift.md`** + ítem #3 del `QUE_FALTA.md` anotado EN BRANCH.

## Hallazgos (con test que los demuestra)

**3 tablas + 5 columnas faltantes.**

- **H1 — el grande: tres tablas que usan firmware Y dashboard no existen en NINGÚN `.sql`
  del repo.** No es que falten en el canónico: no están en ninguna parte. El bootstrap
  del 07-13 armó la base sin ellas y nadie lo notó porque nada falla ruidosamente.

  | Feature | Firmware | Dashboard | Estado real |
  |---|---|---|---|
  | WiFi remoto / scan de redes | consulta cada **10 s** (`supabase.h:767`) | `sendWifiCommand()` (`supabaseClient.js:707`) | **no existe** de los dos lados |
  | Panel SIM800 | sube **19 campos** cada 30 s (`supabase.h:1000`) | `getSIM800Status()` (`:1106`) | se pierde entero; panel siempre vacío |
  | Terminal AT remota | `at_commands` (`supabase.h:1013`) | `sendATCommand()` (`:1116`) | muerta |

  Lo desagradable: son features **escritas, compiladas y con UI**. El costo ya se pagó;
  lo que falta son tres `CREATE TABLE`. La línea minera (Cerro Moro, SIM800) depende de dos.

- **H2 — la barra de progreso del OTA nunca avanza.** El firmware reporta avance cada
  10 % del flasheo (`supabase.h:675-677`) con `progress_pct` / `progress_bytes` /
  `updated_at`; la tabla tiene **`progress`** — otro nombre — y no tiene las otras dos.
  El OTA **sí funciona** (los `PATCH` de `status` usan columnas que existen; por eso el
  E2E del 07-13 pasó), pero es justo el dato que se mira cuando un update parece colgado
  y hay que decidir si cortar o esperar, con la placa en el comercio de un cliente.

- **H3 — `devices` no tiene `wifi_scan_results` / `wifi_scan_at`.** Fallan los dos lados:
  el PATCH del firmware (`:757`) y el `select=` del dashboard (`:718`).

**Lo que está BIEN y queda fijado por test** (tan importante como los hallazgos):
`readings` está **intacta** — 29 columnas escritas, ninguna falta: el incidente del 07-13
quedó realmente cerrado, y hay un test dedicado porque si esa falla, el nodo deja de
guardar *toda* lectura. Y las 7 columnas de config que el firmware **lee** con `select=`
existen todas → la sincronización de umbrales no está rota.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-03-b-schema-drift
python tools/check_schema_drift.py                  # -> 8 hallazgos, exit 1
python -m unittest tools.test_check_schema_drift    # -> Ran 37 tests, OK

# la migración propuesta cierra el drift COMPLETO (ni de menos ni de más):
python tools/check_schema_drift.py --schema supabase/SETUP_COMPLETO.sql supabase/migration_ota_updates.sql supabase/migration_fixes_2026-07-13.sql supabase/migration_2026-08-03_schema_drift.sql
                                                    # -> OK, exit 0
```

Regresión de las suites previas: `python tools/test_scan_secrets.py` **13 OK**,
`python tools/test_lint_device_config.py` **35 OK**.

## Qué quedó sin verificar (nube / hardware — trabajo de día)

- **Contrastar contra la base VIVA.** El checker compara contra el schema **del repo**.
  Si alguien agregó columnas a mano por el dashboard de Supabase, el repo miente en el
  sentido opuesto. La query de `information_schema.columns` está en `docs/schema-drift.md`;
  toda diferencia se trae al repo (la regla del 07-13 era *"dejar el repo = la nube"*).
- **Aplicar la migración** en `cjdluhemschrynijzvap` + sus 4 verificaciones (a-d).
- **Confirmar en placa** que SIM800 y WiFi remoto arrancan a funcionar E2E. El drift
  explica por qué no andaban; que anden se ve en hardware.
- La migración **no se corrió contra ningún Postgres** — se validó por parser, no por
  ejecución. Un typo de sintaxis SQL saltaría recién en el SQL Editor.

## Deuda anotada, NO cerrada

- **`wifi_commands.password` guardaría la clave WiFi del comercio en claro** — misma deuda
  que `readings.wifi_password` (ya anotada en `migration_fixes`). No se arregla acá
  (habría que sacarlo del firmware primero). @firmware + @backend, antes del primer
  cliente pago. Se cruza con el **hueco #6 del PORTFOLIO**.
- **`door_sensors`**: el dashboard la usa (`supabaseClient.js:732`) y tampoco existe en
  ningún `.sql`. **No la creé a propósito** — el firmware no la toca, así que su forma no
  se puede derivar de los dos lados como las otras tres. Que la defina @backend.

## Estado

- Branch `nocturno/local-2026-08-03-b-schema-drift` pusheado (1 commit, `9c14b5f`).
  frioseguro volvió a `main` limpio.
- `QUE_FALTA.md` de frioseguro: ítem **#3** anotado EN BRANCH.
- 4 repos intactos salvo el branch de trabajo. `data/field_captures` de galgas no tocado.
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de anoche y de
  anteanoche: `agentes/{esquematico,pcb}.md`, `dominios/{diseno,esquematico,firmware,hardware,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md` y `dominios/diseno3d.md`).
  **No los toqué ni los commiteé** — no es trabajo mío. Matías: commitealos, o la rutina
  cloud choca en el próximo `git pull`.
- La cola de merge suma **36 branches**. El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo y sin
  usar: falta la sesión humana. **Nota de prioridad:** este branch y el de anoche son de
  los pocos que tocan un 🔴, no un 🟡 — si Matías drena poco, que drene estos.
