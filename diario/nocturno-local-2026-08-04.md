# Nocturno local — 2026-08-04

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada de planta OCTUBRE).
**Branch:** `nocturno/local-2026-08-04-contrato-comandos` (pusheado, commit `a617960`).

## Tarea elegida y por qué

Los dos turnos de ayer fueron a datalogger (P0) y FrioSeguro (P1 PLATA);
galgas no se tocaba desde el 07-31. Repasé sus ítems sin branch y los que quedan
son hardware (galga física, LiPo, brownout, montaje), nube (bucket firmado) o
decisiones de Matías. El único hueco de software puro y verificable offline no
era un ítem del `QUE_FALTA` — era algo que el `QUE_FALTA` no nombraba:

> **el contrato de comandos remotos.**

Un comando de galgas atraviesa **cuatro listas escritas a mano, en tres
lenguajes, en tres archivos que nadie compara**:

| Lista | Dónde | Qué decide |
|---|---|---|
| `CMD_META` | `web/src/App.jsx` | qué botón ve el operario |
| `defaultPayload()` / `CmdSpecificForm()` | `web/src/App.jsx` | qué claves manda |
| `commands_cmd_check` | `backend/supabase/migrations/*.sql` | qué INSERT acepta la base |
| `strcmp(cmd, "…")` | `firmware/ota_wm_pp/ota_wm_pp.ino` | qué ejecuta la placa |

Lo elegí porque **los tres modos de falla no son equivalentes**, y el peor es
mudo. Si el CHECK rechaza un comando, el INSERT explota con `23514` y el
operario ve el error. Pero si el **firmware** no conoce el comando, cae en el
`else` final del dispatch (`ota_wm_pp.ino:1556`) y hace
`ackCommand(cid, "ack", "no implementado")` → la fila queda `status='ack'` y **el
dashboard la pinta verde**. En una parada de planta eso es: se aprieta un botón,
la UI dice que salió bien, y la placa no hizo nada.

Esto no duplica ningún branch: los 6 branches de galgas son v_pp de campo,
umbral del SCADA, versionado OTA, README, detección RX y energía. Ninguno mira
comandos.

## Qué hice

1. **`tools/check_command_contract.py`** (stdlib, solo lectura, sin nube ni
   hardware). Parsea las cuatro fuentes y las cruza:
   - **SQL**: recorre las migraciones **en orden de nombre** respetando
     `drop constraint` + `add constraint` — el CHECK se **reescribe entero** cada
     vez, así que sólo la última definición vale (y ya pasó **5 veces**).
   - **Dashboard**: `CMD_META` (nombre + `kind`), `defaultPayload()` y las claves
     que escribe `CmdSpecificForm`. Hizo falta un scanner consciente de strings:
     las descripciones tienen llaves adentro (`'Payload: {offset_v, k}'`) y un
     brace-matching ingenuo corta en el lugar equivocado.
   - **Firmware**: las ramas `strcmp(cmd, "x")` con las claves `pl["k"]` que cada
     una lee. Los `strcmp` de la **misma línea** son una sola rama
     (`force_ota_check || ota`) y comparten claves.
   - **RX**: si el sketch consulta `/rest/v1/commands` (hoy: no).

   Exit 0/1/2 para usarlo como gate antes de tocar comandos. `--json`.

2. **`tools/test_check_command_contract.py`** — **57 tests** en 6 capas: los tres
   parsers contra fuentes sintéticas, cada código de hallazgo por separado, la
   **regresión sobre el repo real** (la evidencia de los hallazgos) y el CLI.

3. **`docs/command-contract.md`** + ítem **#16** nuevo en `QUE_FALTA.md` y una
   nota en el **#1** (RX).

## Hallazgos (con test que los demuestra — NO corregidos, generator ≠ evaluator)

Corrida real: **26 comandos en el CHECK, 26 ofrecidos por el dashboard (15
activos), 14 implementados por el firmware → 7 hallazgos.**

- **H1 — el grande: 4 botones marcados `active` no existen en el firmware.**
  `locate`, `set_log_level`, `pause_reports`, `resume_reports`. Los cuatro caen
  en el catch-all y **se ackean como OK**. El más caro es `pause_reports`: es el
  botón que uno apretaría para callar un nodo durante una intervención en el
  REDLER. La UI va a decir "pausado" y el nodo va a seguir posteando.
- **H2 — `locate` e `identify` están invertidos en la UI.** El firmware
  implementa **`identify`** (`:1398`, lee `pl["duration_ms"]`). El dashboard
  ofrece `locate` como el bueno ("Localizar (LED)", activo, manda `{seconds:5}`)
  y a `identify` como "legacy alias". Doble falla: nombre que no existe **y**
  clave de payload distinta.
- **H3 — el form de `ota` deja elegir versión y el firmware la ignora.**
  `defaultPayload('ota')` manda `{version: ''}`; la rama `force_ota_check || ota`
  no lee `pl["version"]` y siempre baja la última del suffix actual. No falla:
  hace otra cosa que la pedida.
- **H4 — el RX no consulta `/rest/v1/commands`** → todo comando enviado al RX
  queda `pending` para siempre, y el dashboard le ofrece el mismo panel que a
  A/B (su cmd por default para RX es `force_ota_check`). Había un rastro en
  `act.md` §Sesión 8, pero como nota de sesión, no como algo que el sistema
  chequee.
- **H5 (warn) — 8 comandos legacy que sólo ackean.** Están marcados ⚠ en la UI,
  así que es esperado; el problema es que en el historial de comandos de un
  device **no se distinguen** de los que sí se ejecutaron.
- **Nota aparte:** `set_config` estaba en el `CREATE TABLE` original y no fue
  copiado en la redefinición del CHECK de `20260426200000`. Sigue vivo en
  `firmware/shared/protocol.h`. Hoy no molesta, pero muestra que "copiar la lista
  entera de nuevo" pierde entradas en silencio. Hay un test que lo fija.

**Lo que está BIEN y queda fijado por test** (tan importante como lo anterior):
**ningún botón del dashboard es rechazado por el CHECK** (cero `23514` al
apretar), **ningún comando de la placa es inalcanzable**, y **los 6 comandos de
calibración (3.6.0) + `set_profile` + `set_burst_samples` cierran de punta a
punta con las mismas claves** — que son justo el camino que se usa en banco y los
dos comandos que mueven perfil de energía y ventana de muestreo.

**Fix candidato más barato** (en el doc, no aplicado): que el catch-all ackee
`status='error'` en vez de `'ack'`. Es **una palabra** y convierte los cuatro
hallazgos silenciosos en ruidosos para siempre.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-04-contrato-comandos
python tools/check_command_contract.py               # -> 7 hallazgos, exit 1
python tools/check_command_contract.py --json
python -m unittest tools.test_check_command_contract # -> Ran 57 tests, OK
```

Los tests de `TestRepoReal` **fijan los 7 hallazgos actuales**: si alguien
arregla uno, el test falla y avisa que hay que actualizar el doc. Es la red de
seguridad, no una foto.

## Qué quedó sin verificar (nube / hardware — trabajo de día)

- **El CHECK de la base VIVA.** El checker compara el **repo**. Si alguien tocó
  el constraint a mano desde el SQL Editor, el repo miente. La query
  (`pg_get_constraintdef` sobre `commands_cmd_check`) está en el doc.
- **Confirmar H1 en placa:** mandar `pause_reports` a A y ver que (a) la fila
  queda en `ack` y (b) el nodo sigue posteando. Es la demostración de 2 minutos
  del hallazgo entero.
- **Los fixes candidatos son de firmware y de UI** → se confirman en banco.
- **No corrí `npm run build`**: no toqué `web/`.
- El checker mira `ota_wm_pp` (lo que corre en A y B hoy, 3.6.x). La familia
  vieja (`esp_a_emisor` + `firmware/shared/protocol.h`) queda fuera; si se vuelve
  a ella hay que apuntarle `--firmware`.

## Estado

- Branch `nocturno/local-2026-08-04-contrato-comandos` pusheado (1 commit,
  `a617960`). galgas volvió a `main` limpio.
- `QUE_FALTA.md` de galgas: ítem **#16** nuevo anotado EN BRANCH + nota en el #1.
- 4 repos intactos salvo el branch de trabajo. `data/field_captures` de galgas
  **no tocado** (este checker ni lo abre).
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las tres
  noches anteriores: `agentes/{esquematico,pcb}.md`,
  `dominios/{diseno,esquematico,firmware,hardware,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md` y
  `dominios/diseno3d.md`). **No los toqué ni los commiteé** — no es trabajo mío.
  Matías: commitealos, o la rutina cloud choca en el próximo `git pull`.
- La cola de merge suma **37 branches**. El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo
  y sin usar: falta la sesión humana. **Nota de prioridad:** de los últimos tres
  branches, éste y el del 08-03-b son los que tocan la cara operativa de octubre
  y del primer abono — si Matías drena poco, que drene esos.
