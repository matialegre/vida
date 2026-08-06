# Nocturno local — 2026-08-06

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus octubre).
**Branch:** `nocturno/local-2026-08-06-identidad-ota` (pusheado, commit `7a45f00`).

## Tarea elegida y por qué

Arranqué encontrando algo que no esperaba: **el repo de galgas estaba
checkouteado en un branch `nocturno/local-2026-08-05-b-identidad-ota` con CERO
commits y un archivo sin trackear de 700 líneas** (`tools/check_ota_identity.py`),
y **no hay `diario/nocturno-local-2026-08-05-b.md`**. O sea: un turno anterior
escribió la herramienta y se cortó antes de commitear, testear y reportar. Ese
trabajo estaba a un `git clean` de perderse.

Lo verifiqué antes de adoptarlo (corría, y los hallazgos daban contra las
fuentes reales, no eran artefactos del parser), así que la tarea de la noche fue
**terminarlo bien** en vez de empezar algo nuevo: tests, doc, hallazgos
verificados, `QUE_FALTA`, commit, push. Una tarea bien hecha, que además rescata
una noche que ya estaba pagada.

Encaja igual por rotación (los últimos turnos fueron frioseguro 08-05,
datalogger 08-04-b, galgas 08-04) y por jerarquía: galgas es octubre.

### De qué se trata

Un ESP32 de este sistema sabe quién es en *compile time*:

```c
#define FW_VERSION   "3.6.5-" DEVICE_ID "-" PROFILE_SUFFIX   // ota_wm_pp.ino:151
```

El preprocesador concatena los tres literales en **uno solo**, así que el `.bin`
lleva adentro la cadena exacta `3.6.5-A-pmax`, salida del mismo
`-DDEVICE_TARGET_x -DPROFILE_y` con el que se compiló. **Esa cadena no puede
mentir.** Las cuatro etiquetas que la rodean, sí:

| Etiqueta | Quién la escribe |
|---|---|
| el dir de build `build/pp_<DEV>_<prof>_v<NNN>/` | un humano |
| el archivo `bins_ota/<ver>/<ver>-<DEV>-<suf>.bin` | un humano |
| la fila de `firmware_versions` | `sync_firmware.ps1`, **derivada del dir** |
| la ruta en Storage `firmware/<DEV>/<version>.bin` | `sync_firmware.ps1`, **derivada del dir** |

**Por qué esta clase de bug es más cara que un bug común:** el `sha256` que
verifica el firmware después de bajar prueba **integridad, no identidad** —
confirma que el archivo llegó entero, no que sea el del device correcto. Y el
guard de MAC (`dreyfusInitIfNeeded`, `ota_wm_pp.ino:435`, activo con
`EN_DREYFUS 1`) corre en `setup()` **antes** del chequeo de OTA: si la MAC no es
la esperada, `esp_deep_sleep_start()` de 1 h, y al despertar falla igual. La
placa **nunca llega a consultar `firmware_versions`**, así que publicar después
el binario bueno no la rescata. **Una etiqueta equivocada no se corrige por
aire: se corrige con un cable USB.** En octubre, en planta, eso es un viaje.

No duplica ningún branch de galgas: los 15 previos son OTA versioning, contrato
de comandos, v_pp de campo, umbral del SCADA, drift de README, modelo de
decisión de OTA. Ninguno mira **para quién es cada binario**.

## Qué hice

1. **Verifiqué la herramienta heredada** antes de darla por buena — a mano,
   contra las fuentes: leí la cadena embebida del `.bin` acusado con un
   one-liner independiente, leí `sync_firmware.ps1:77-103` para confirmar que
   reconstruye todo desde el nombre del dir sin abrir el binario, y confirmé que
   `EN_DREYFUS` está en `1` (si no, el hallazgo del deep sleep sería teórico).

2. **`tools/test_check_ota_identity.py` — 128 tests en 8 capas:** helpers de
   parseo de C, el parser del `.ino` (el alfabeto sale del firmware, no
   hardcodeado), `label_from_path` (las 3 convenciones de ruta y **quién es
   publicable**), los parsers de los dos `.ps1`, `collect_bins`, **cada código de
   hallazgo con repos sintéticos**, la **regresión sobre el repo real** (la
   evidencia) y el CLI.

   Tres cosas que los tests fijan porque son juicio, no mecánica, y se pueden
   romper sin que nadie note:
   - el **`.merged.bin` se ignora** — lleva la misma app adentro; contarlo
     aparte inventaría un duplicado falso en cada build;
   - el match de dir es **case-insensitive porque `-notmatch` de PowerShell lo
     es** — compararlo case-sensitive escondería justo los mislabels buscados;
   - **`v3610` no es versión**: `sync_firmware.ps1` exige 3 dígitos y saltea el
     resto con un `[skip]` mudo; el checker replica la regla exacta.

3. **Encontré un hallazgo nuevo, mío, escribiendo el doc** (H6 abajo) y lo
   agregué como chequeo (`W-IDENTITY-HARDCODED`) con sus 5 tests.

4. **`docs/ota-identity.md`** + nota en **`QUE_FALTA` #5** con el detalle y el
   colateral para @firmware.

## Hallazgos (con test que los demuestra — NO corregidos, generator ≠ evaluator)

Corrida real: **132 binarios, 129 con identidad, 16 publicables, 4 devices, 5
perfiles → 3 errores / 45 warns.**

- **H1 (error) — hay un binario con la etiqueta cambiada, hoy, en `build/`.**
  `build/test_pnorm_v364/ota_wm_pp.ino.bin` dice **TEST-pnorm** y adentro tiene
  **`3.6.4-A-psim`**: mal el device *y* mal el perfil. **Hoy no se publica** —
  al dir le falta el prefijo `pp_`, así que `sync_firmware.ps1` no lo levanta.
  El daño está **latente**: alcanza con que alguien renombre la carpeta a
  `pp_TEST_pnorm_v364` — que es exactamente lo que haría quien quiera
  publicarlo — para que la fila diga `TEST` sobre un binario de `A`. Hay un test
  que fija que hoy **no** es publicable: si empieza a fallar, el hallazgo subió
  de categoría.

- **H2 (error) — la etiqueta publicada no está atada al binario.**
  `sync_firmware.ps1` arma `version`/`device_id`/`storage_path` desde el nombre
  del directorio y **nunca abre el `.bin`**. Es la vía por la que un H1 llega a
  la nube. Fix candidato barato: buscar la cadena `\d+\.\d+\.\d+-<DEV>-<suf>` en
  el binario y **abortar la subida** si no coincide con la carpeta — el script
  **ya lee el archivo entero** para el `sha256` (`:103`), así que no cuesta ni
  una lectura de disco extra.

- **H3 (error) — dos binarios distintos dicen ser `3.6.2-A-palerta`.** Distinto
  `sha256`, misma identidad declarada. `firmware_versions` guarda **un** sha por
  versión: el otro es indistinguible por etiqueta y falla la verificación
  post-descarga si se sube el equivocado. Ninguno es publicable hoy.

- **H4 (warn) — el canal OTA está atrasado en TODO, y esto pega en el ítem #4.**
  De las 18 combinaciones device-perfil compiladas: **8 atrasadas**, **8 que
  nunca se publicaron**, y **2 "al día"** (`RX-pnorm`, `RX-psim`) que lo están
  **por abandono** — nadie las recompila desde 3.3.1. El número que lo resume:
  el banco está en **3.6.5** y lo único que `sync_firmware.ps1` subiría hoy desde
  `build/` son **dos** binarios de A en **3.6.4**. Al lado hay **21 binarios
  3.6.5 con identidad válida que ningún publicador levanta**, por
  **tres caracteres** en el nombre de la carpeta (`pp_`).
  **Consecuencia concreta para `QUE_FALTA` #4 (re-flashear ESP-B):** B no sólo
  está atrás en el chip — **ninguna versión de B posterior a 3.3.1 está
  publicada**, así que hoy B **no se puede poner al día por aire aunque uno
  quiera**. Es cable USB sí o sí hasta que alguien publique. Eso cambia el orden
  de la tarea: primero publicar, después ir al banco.

- **H5 (warn) — los dos publicadores no se ponen de acuerdo.**
  `sync_firmware.ps1` cubre A/B/RX con `SERVICE_ROLE`; `BUILD_ALL_PROFILES.ps1`
  cubre A/B/TEST con `ANON`. Escriben **la misma tabla**. Qué se puede publicar
  depende de **cuál de los dos corriste**. Y que uno funcione con `ANON` es
  información sobre las RLS de `firmware_versions` que conviene mirar de día —
  la anon key está en el bundle del dashboard. Se cruza con el ítem **#6**
  (bucket `firmware` público).

- **H6 (warn) — el hallazgo que salió escribiendo el doc, y que se muerde la
  cola: para RX, la identidad embebida TAMBIÉN es una etiqueta a mano.**
  Todo lo anterior se apoya en que la cadena del `.bin` no puede mentir porque
  la arma el preprocesador. **Para RX no es cierto:**
  `firmware/esp_rx_receptor/config.h:13` hace
  `#define FW_VERSION "3.6.7-RX-palways"` — **un literal entero, tipeado**, no
  compuesto con `DEVICE_ID`/`PROFILE_SUFFIX`. Un `.bin` de RX compilado con otro
  perfil, o con la constante sin actualizar, **sale con la identidad vieja y
  nadie lo nota** — ni este checker, que para RX está leyendo la misma clase de
  etiqueta humana que dice auditar. Es también la razón de que `3.6.7` aparezca
  sólo en los binarios de RX: las dos ramas versionan por separado. **Fix de una
  línea** (componerla como `ota_wm_pp`), y el warn desaparece solo.

- **H7 (warn) — tres binarios de nomenclatura vieja sin identidad embebida**
  (`bins_ota/<DEV>/0.7.5-<DEV>-direct.bin`, pre-3.x): nadie sabe qué son sin
  flashearlos.

**Lo que está BIEN y queda fijado por test** (tan importante: es lo que NO hay
que ir a revisar): **ningún binario publicable está mislabeleado** — el error
caro **no está pasando hoy**; **todo lo publicable tiene identidad embebida y
una sola**; **todo lo publicable es alcanzable por la query real del firmware**
(`?device_id=eq.<DEV>&version=like.*-<DEV>-<suf>`), no hay binario publicado e
invisible; y **ningún device del firmware quedó sin publicador**. Lo roto es el
proceso alrededor del canal, no el canal.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-06-identidad-ota
python tools/check_ota_identity.py                  # -> 3 error / 45 warn, exit 1
python tools/check_ota_identity.py --json
python tools/check_ota_identity.py --fail-on warn
python -m unittest tools.test_check_ota_identity    # -> Ran 128 tests, OK
```

Sirve como **gate antes de publicar**:
`python tools/check_ota_identity.py && pwsh scripts/sync_firmware.ps1`.

H1 se comprueba a mano, sin la herramienta, en una línea:

```
python -c "import re; d=open('build/test_pnorm_v364/ota_wm_pp.ino.bin','rb').read(); print(set(m.decode() for m in re.findall(rb'[0-9.]+-(?:A|B|RX|TEST)-p[a-z]+', d)))"
# -> {'3.6.4-A-psim'}   (la carpeta dice TEST-pnorm)
```

Los tests de `TestRepoReal` **fijan los hallazgos de hoy**: si alguien arregla
uno, el test falla y obliga a actualizar `docs/ota-identity.md` en el mismo
commit. Es la red de seguridad, no una foto. (Ya funcionó: cuando agregué H6, el
test de totales falló solo y me obligó a actualizar el doc.)

## Qué quedó sin verificar (nube / banco — trabajo de día)

- **La tabla VIVA.** El checker compara el **repo**: sabe qué se publicaría, no
  qué está publicado. La query para contrastar está en `docs/ota-identity.md`
  (§ "Para confirmar de día") — para cada fila: ¿el `version` termina en
  `-<device_id>-<suf>`? ¿el `storage_path` empieza con `<device_id>/`? ¿el
  `sha256` matchea algún `.bin` del repo? (los 132 sha salen del `--json`). Una
  fila cuyo sha no matchea **ninguno** es un binario que ya no existe.
- **El orden de la query no es semver** — es
  `&order=released_at.desc&limit=1` (`ota_wm_pp.ino:1063-1069`) y recién después
  compara semver. La placa mira **una sola** fila, la más reciente *por fecha*.
  Si un rollback se publica como fila nueva, es la única que la placa ve y
  `compareSemver` la descarta por menor → **el rollback no baja y nadie avisa.**
  **Está leído del código, no observado**, y depende de si el upsert de
  `sync_firmware.ps1` (`merge-duplicates`, sin `released_at` en el payload)
  refresca o conserva `released_at`. Lo dejé documentado como pregunta, **no lo
  conté como hallazgo**.
- **Las RLS de `firmware_versions`** (H5): ¿cualquiera con la anon key puede
  insertar una fila de firmware?
- **Qué corre realmente cada placa**: `select id, firmware_version from devices`.
  Si un chip reporta una versión que no está en `firmware_versions`, se flasheó
  por USB con algo que nunca se publicó.
- **Los fixes son de PowerShell, de firmware y de proceso** → se confirman en
  banco. **Ninguno aplicado.**
- **No corrí `npm run build`**: no toqué `web/`.
- **No toqué `data/field_captures/`** — este trabajo ni entra ahí.

## Estado

- Branch `nocturno/local-2026-08-06-identidad-ota` pusheado (1 commit,
  `7a45f00`: 4 archivos, +1.500 líneas). galgas volvió a `main` limpio.
- `QUE_FALTA.md` de galgas: nota en el ítem **#5** + el colateral de RX para
  @firmware (en el branch).
- ⚠️ **Queda un branch local vacío: `nocturno/local-2026-08-05-b-identidad-ota`**
  (0 commits, apunta a main, nunca se pusheó) — es el resto del turno que se
  cortó. **No lo borré** (regla: no borrar nada fuera de un branch de trabajo).
  Matías: `git branch -d nocturno/local-2026-08-05-b-identidad-ota` cuando
  quieras, su contenido ya está adentro del branch de hoy.
- ℹ️ **`C:\Proyectos\cosechador` sigue checkouteado en
  `nocturno/local-2026-07-18-modelo-energia`, no en `main`** (estado previo, no
  lo hice yo). **No lo cambié.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las seis
  noches anteriores: `agentes/{esquematico,pcb}.md`,
  `dominios/{diseno,esquematico,firmware,hardware,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`, + sin trackear `agentes/diseno3d.md` y
  `dominios/diseno3d.md`). **No los toqué ni los commiteé** — no es trabajo mío.
  Matías: commitealos, o la rutina cloud choca en el próximo `git pull`.
- La cola de merge suma **43 branches** en origin (galgas 16, datalogger 13,
  frioseguro 13, cosechador 1). El tooling de drenaje
  (`tools/merge_queue_status.py` + `tools/resolve_doc_conflicts.py`) sigue listo
  y sin usar: falta la sesión humana.
  **Nota de prioridad:** de los 16 de galgas, éste es el que **cambia una tarea
  del plan de octubre** — H4 dice que el ítem #4 (re-flashear B) tiene un paso
  previo que no estaba escrito: **publicar**, porque hoy B no tiene ninguna
  versión posterior a 3.3.1 en el canal. Y H1+H2 juntos son el único hallazgo de
  todo el mes cuyo modo de falla **no se arregla por aire**.
