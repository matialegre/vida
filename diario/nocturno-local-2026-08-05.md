# Nocturno local — 2026-08-05

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (P1 — PLATA, la palanca de abonos).
**Branch:** `nocturno/local-2026-08-05-contrato-config` (pusheado, commit `3d1d4da`).

## Tarea elegida y por qué

Rotación: los últimos tres turnos fueron galgas (08-04), datalogger (08-04-b) y
datalogger (08-03). FrioSeguro es el repo activo que más tiempo llevaba sin
tocar, **y la jerarquía lo pone empatado en la cima** (PLATA).

Repasé sus ítems sin branch. Los 🔴 que quedan son flashear, el piloto en la
heladera, comprar la caja IP65 y decidir precio/contrato: hardware, compras o
decisiones de Matías. Nada de software puro. Así que fui a lo que el
`QUE_FALTA` **no nombraba**:

> **el contrato de configuración.**

Un umbral de FrioSeguro se escribe por **cuatro vías**, se persiste en **una**, y
se declara en **otras dos**:

| Fuente | Qué decide |
|---|---|
| `types.h` — `struct Config` | la lista canónica |
| `storage.h` — `loadConfig`/`saveConfig` | **la única que persiste** (NVS) |
| `web_api.h` — `POST /api/config` | el portal local del instalador |
| `serial_api.h` — `RESET_CONFIG`, `SET_TEMP` | la consola USB |
| `supabase.h` — `supabaseRefreshDeviceName()` | **lo que toca el cliente en el dashboard** |
| `SETUP_COMPLETO.sql` + `DevicesAdminTable.jsx` | columnas y defaults de la nube |

Lo elegí porque **los modos de falla no son equivalentes, y los caros son mudos**:

| Falla | ¿Se nota? |
|---|---|
| Valor fuera de rango | sí — lo caza `lint_device_config.py` (branch 07-12) |
| Columna inexistente | sí, PostgREST 400 — lo caza `check_schema_drift.py` (branch 08-03-b) |
| **Writer sin `saveConfig()`** | **NO** — vive en RAM, vuelve solo al reboot |
| **Campo que nadie lee** | **NO** — perilla muerta |
| **Defaults en desacuerdo** | **NO** — gana el camino que escribió primero |

**No duplica ningún branch.** Los 12 de FrioSeguro son secretos, resumen
mensual, lint de provisioning, vista de estabilidad, modelo de alerta, modelo de
puerta, retención, gate de Telegram y schema drift. Ninguno mira el **camino** de
un parámetro. Los tres tools ahora se reparten el territorio limpio:
`lint_device_config` valida **valores**, `check_schema_drift` valida **columnas**,
éste valida **el camino**.

## Qué hice

1. **`tools/check_config_contract.py`** (stdlib, read-only, sin nube ni hardware).
   Cruza las 6 fuentes. Lo que hizo falta resolver:
   - **Clasificar cada `config.<campo>`** en `write` / `persist` (dentro de un
     `prefs.put*`) / `echo` (alimenta un `doc["k"] = …`) / `read`. Sin esa
     distinción, un campo que sólo se serializa parece "usado".
   - **Atribuir cada lectura a su función**, y declarar cuáles son de *plomería*
     (`loadConfig`, `saveConfig`, los dos handlers de `/api/config`,
     `processCommand`, el pull remoto, `printStatusJSON`). Una lectura que sólo
     ocurre ahí adentro significa que el parámetro **no cambia la conducta del
     equipo**. Es el único juicio subjetivo del checker y vive en una sola
     constante (`PLUMBING_FUNCS`), no repartido.
   - **Medir el alcance del `saveConfig()`** en tres niveles (`block` /
     `function` / `none`) con tracking de llaves. Sólo `none` se reporta, y hay
     un test que fija que el `saveConfig()` de la función de al lado **no
     cuenta** — que es justo el error que haría parecer persistido al pull remoto.
   - **Derivar el mapa `clave_json ↔ campo` del propio código** (`web_api.h`), no
     hardcodearlo: es la lección de "una sola fuente de verdad".

   Exit 0/1/2 como gate antes de tocar cualquier parámetro. `--json`, `--fail-on`.

2. **`tools/test_check_config_contract.py`** — **85 tests** en 7 capas: helpers
   puros de parseo de C, los parsers del firmware, la clasificación de usos y el
   alcance del save, los parsers de la nube, **cada código de hallazgo por
   separado** con fuentes sintéticas, la **regresión sobre el repo real** (la
   evidencia) y el CLI.

3. **`docs/config-contract.md`** + ítem **#19** nuevo en `QUE_FALTA.md` y una
   nota en el **#18**.

## Hallazgos (con test que los demuestra — NO corregidos, generator ≠ evaluator)

Corrida real: **18 campos, 18 load / 18 save, 64 escrituras, 15 claves JSON, 33
columnas SQL → 16 hallazgos (7 error, 9 warn).**

- **H1 — el grande: el pull de config remota no persiste NADA.**
  `supabaseRefreshDeviceName()` (`supabase.h:251-254`) escribe **cuatro**
  parámetros — `tempCritical`, `alertDelaySec`, `doorOpenMaxSec`,
  `defrostCooldownSec` — y **nunca llama `saveConfig()`**. Es el único writer del
  firmware que no persiste. La secuencia, como la vive el cliente: baja su umbral
  en el dashboard → la placa lo toma y lo usa → la placa se reinicia (watchdog,
  corte, OTA — el firmware **cuenta reboots** justamente porque pasan) →
  `loadConfig()` lee NVS, que nunca se enteró, y **vuelve al umbral viejo**
  mientras el dashboard sigue mostrando el nuevo. **Nadie ve un error.** El
  equipo termina oscilando entre dos umbrales según cuándo fue el último reboot,
  y la única capa que podría avisar de la discrepancia está mostrando el valor
  que **no** se usa. Fix candidato: **una línea**, con guarda para no gastar
  ciclos de NVS en cada refresh.
  **Deuda de la misma función:** `state.lastLocalConfigChange` existe en
  `types.h:71` con el comentario *"para no pisar con Supabase"*, lo escribe
  `web_api.h:166` — y **no lo lee nadie**. La protección que el struct declara no
  está implementada.

- **H2 — tres perillas muertas.** Campos que se escriben y ninguna lógica lee:
  `tempMax` (el dashboard lo ofrece como **"Temp máx alerta"**; `alerts.h` decide
  sólo con `tempCritical` — el label miente), `sensor1Enabled` (la sonda 2 **sí**
  se consulta en `sensors.h:151`; la 1 no — es una asimetría, no un patrón), y
  `doorOpenMaxSec` — que **ya lo había reportado el branch 07-20** con otra
  herramienta y otro razonamiento. Que dos análisis independientes caigan en el
  mismo campo es corroboración, y me sirvió de control de que el checker detecta
  el patrón.

- **H3 — el dashboard edita dos cosas que la placa nunca baja.** El `select=` del
  pull trae 4 parámetros; el panel del cliente edita 2 más que son del `struct
  Config`: `temp_max` (coherente con H2) y **`telegram_enabled`** — hay un toggle
  "📱 Telegram" (`DevicesAdminTable.jsx:736`), la columna existe
  (`SETUP_COMPLETO.sql:88`) y se guarda, pero **la placa nunca la consulta**. El
  cliente apaga las notificaciones, la UI le dice que quedaron apagadas, y le
  siguen llegando. Es un ticket de soporte servido en bandeja.

- **H4 (warn) — dos defaults en desacuerdo entre las tres capas:** `temp_max`
  (firmware **-18.0** / SQL -15.0 / dashboard -15) y `door_open_max_sec`
  (firmware **180** / SQL 120 / dashboard 120). Hoy no hacen daño porque son
  perillas muertas — pero cuando se arreglen H2/H3 pasan a decidir conducta.
  **Arreglarlos antes del fix de firmware es más barato que después.**

- **H5 (warn) — dos `#define` que no usa nadie.**
  `DEFAULT_DEFROST_COOLDOWN_SEC` (storage.h hardcodea `1800` en vez de usarlo;
  hoy coinciden, así que es mudo) y `DEFAULT_TEMP_MIN`. Este último importa
  porque `lint_device_config.py` valida la invariante
  `temp_min < temp_max < temp_critical` sobre un valor que **el firmware no
  consulta**: esa invariante vale para el resumen mensual de la nube, no para la
  conducta de la placa.

- **H6 — el "reset de fábrica" no deja el equipo como un arranque limpio.**
  `RESET_CONFIG` escribe 15 literales; cuatro difieren del default de un primer
  arranque y **no restaura tres campos** (`simTemp1`, `simTemp2`, `simDoorOpen`).
  El que importa: **`supabaseEnabled = false`** → un reset **deja el equipo sin
  reportar a la nube**. Se recupera solo, pero **recién en el próximo reboot**
  (`firmware_modular.ino:170-173` lo fuerza a `true` en cada `setup()`), y un
  equipo que anda bien puede pasar semanas sin reiniciarse. La ventana de
  "cliente sin servicio" la define un evento que no tiene nada que ver con la
  causa.

**Lo que está BIEN y queda fijado por test** (tan importante como lo anterior):
**los 18 campos del struct se cargan y se guardan**, sin faltantes ni huérfanos;
**ninguna clave NVS está desalineada** entre load y save, ninguna excede los 15
caracteres de ESP-IDF, ningún accessor de tipo está cruzado; **el portal local y
la consola serial sí persisten** (el instalador que configura por el AP no pierde
lo que puso); y **`temp_critical` — el umbral que efectivamente dispara la alerta
— cierra de punta a punta**: mismo default en las tres capas, lo baja el pull
remoto, lo lee `alerts.h`. **El camino que se cobra está sano; lo roto es lo que
se le montó alrededor.**

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-05-contrato-config
python tools/check_config_contract.py                   # -> 16 hallazgos, exit 1
python tools/check_config_contract.py --json
python tools/check_config_contract.py --fail-on warn
python -m unittest tools.test_check_config_contract     # -> Ran 85 tests, OK
```

Los tests de `TestRepoReal` **fijan los 16 hallazgos actuales**: si alguien
arregla uno, el test falla y avisa que hay que actualizar el doc en el mismo
commit. Es la red de seguridad, no una foto.

## Qué quedó sin verificar (banco / nube — trabajo de día)

- **Que H1 sea realmente silencioso en la placa.** Está leído del código (no hay
  `saveConfig()` en esa función), no observado. **Demostración de 5 minutos:**
  cambiar `temp_critical` desde el dashboard, esperar el refresh, ver por serial
  que la placa lo tomó, apretar EN, y ver que vuelve al viejo con el dashboard
  mostrando el nuevo. Ese par de hechos juntos es el hallazgo entero.
- **La base VIVA.** El checker compara el **repo**. Si alguien alteró `devices` a
  mano desde el SQL Editor, el repo miente.
- **La placa flasheada.** Si corre firmware no commiteado, el repo miente:
  verificar la versión antes de concluir.
- **Los fixes son de firmware, de SQL y de UI** → se confirman en banco. Ninguno
  aplicado.
- **No corrí `npm run build`**: no toqué `web-dashboard/` (sólo lo leo).
- El checker mira `firmware_modular/` (la familia v4). `emisor/`, `receptor/` y
  `config_SANTA_CRUZ.h` quedan fuera a propósito.

## Estado

- Branch `nocturno/local-2026-08-05-contrato-config` pusheado (1 commit,
  `3d1d4da`). frioseguro volvió a `main` limpio.
- `QUE_FALTA.md` de frioseguro: ítem **#19** nuevo + nota en el **#18** (en el
  branch).
- 4 repos intactos salvo el branch de trabajo. `data/field_captures` de galgas
  **no tocado** (este trabajo ni entra a ese repo). Jamás mDNS: no toqué nada de
  descubrimiento.
- ℹ️ **`C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main`** (estado previo, no
  lo hice yo). **No lo cambié.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las cinco
  noches anteriores: `agentes/{esquematico,pcb}.md`,
  `dominios/{diseno,esquematico,firmware,hardware,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md` y
  `dominios/diseno3d.md`). **No los toqué ni los commiteé** — no es trabajo mío.
  Matías: commitealos, o la rutina cloud choca en el próximo `git pull`.
- La cola de merge suma **42 branches** en origin (galgas 15, datalogger 13,
  frioseguro 13, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo
  y sin usar: falta la sesión humana.
  **Nota de prioridad:** este branch toca la cara operativa del **primer abono** —
  H1 y H3 son dos formas de "el cliente configura algo y el sistema le miente",
  que es exactamente lo que rompe un abono nuevo. Si Matías drena poco, éste y el
  08-04 (comandos de galgas) son los que cambian qué se prueba en banco.
