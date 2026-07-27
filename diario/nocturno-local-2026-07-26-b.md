# Nocturno LOCAL — 2026-07-26-b (2º turno, worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
El 1er turno de hoy (`-26`) cerró el cluster STALE de datalogger (octubre, cat. 2) y dejó dicho
que **lo que falta en datalogger es merge humano/hardware, no más branches nocturnos**. Así que
este 2º turno subió a **PLATA (categoría 1, la prioridad más alta)**: FrioSeguro.

Construí **`tools/provision_device.py`** — el **generador de config por cliente**, la otra mitad
del pipeline de provisioning. Contexto: la noche del 12/07 ya había hecho `lint_device_config.py`
que **valida** un `config.h` antes de flashear (y encontró defectos reales: `OTA_PASSWORD ""`, chat
de Telegram compartido). Faltaba lo simétrico: **generar** un config correcto. Ahora onboardear un
comercio es un comando en vez de editar `config.h` a mano (que es lo que produce esos defectos):

```
python tools/provision_device.py --client "Carniceria La Esquina" --placa 1 \
    --telegram-chat 111222333 --show-secret
# -> provisioning/carniceria-la-esquina/config.h  (APTO, listo para flashear)
```

**El contrato:** antes de escribir, pasa el config generado por el linter y **se niega a emitir si
no queda apto**. Un config salido de este tool está garantizado a pasar el gate pre-flasheo.
**Evidencia:** el `config.h` real HOY es **NO apto** (OTA_OPEN); tras provisionar queda **APTA** con
password OTA única generada. **Branch: `nocturno/local-2026-07-26-b-provision-device` (frioseguro).**
Cierra parcialmente el **bloqueante 🔴 #4 del primer abono** ("credencial única por cliente").

## Tarea elegida y por qué
**Generador de config por cliente para FrioSeguro** (`provision_device.py`).
- **Prioridad máxima disponible:** PLATA y UNIVERSIDAD están empatadas en la cima (octubre es 2ª).
  El 1er turno ya agotó el valor nocturno de datalogger (octubre); lo honesto era subir a
  categoría 1. FrioSeguro es la palanca de PLATA, y el #4 es 🔴 **bloqueante del PRIMER abono**.
- **Necesidad evidenciada, no especulativa:** `lint_device_config.py` (12/07, ya en main) corre
  sobre el `config.h` real y encuentra defectos concretos (`OTA_OPEN` = `OTA_PASSWORD ""`, chat de
  Telegram propio de Matías compartido a todos los clientes). Hoy nadie los previene al onboardear
  a mano. Faltaba el **generador** que produzca un config que *pase* ese linter.
- **Compone con lo existente** (anti-sobre-ingeniería: reusar `lint_device_config` como librería,
  no reescribir). Es el par generate/validate, no un duplicado.
- **100% software, offline-verificable** (git + Python stdlib; el linter es el oráculo). Cero red,
  nube, hardware o compilación → cero riesgo de timeout (disciplina 07-07).
- **NO está en ningún branch.** Genuinamente nueva.

## Qué hice
1. **Estudié el terreno** antes de escribir una línea: los 4 `QUE_FALTA.md`, la cola de merge, el
   informe `-26`, el `lint_device_config.py` (contrato/severidades) y el `config.h` real (molde
   exacto: `#if PLACA_NUM==N`, `DEVICE_NAME`, `OTA_PASSWORD`, `TELEGRAM_CHAT_ID` + array
   `TELEGRAM_CHAT_IDS[]`, `DEFAULT_TEMP_*`).
2. **`tools/provision_device.py`** (stdlib): toma el `config.h` del repo como **plantilla** y
   parcha **solo** los campos por-cliente dejando el resto **byte-idéntico** —
   - `DEVICE_NAME` = nombre del comercio,
   - `OTA_PASSWORD` = única (generada con `secrets.token_urlsafe`, o explícita con `--ota-password`),
   - `TELEGRAM_CHAT_ID` + array `TELEGRAM_CHAT_IDS[]` + `TELEGRAM_CHAT_COUNT` = chat del cliente,
   - overrides opcionales de umbral (`--temp-max`, `--alert-delay-sec`, …).
   `set_define` preserva indentación y el comentario `// …` de cada línea; `provision()` es una
   **función pura** (no toca disco) → tests deterministas.
3. **El contrato:** antes de escribir, `lint_generated()` corre `lint_device_config.lint()` sobre
   el resultado y, si hay algún hallazgo ≥ `--fail-on` (default `error`), **no escribe nada** y
   sale con exit 1. Exit codes: 0 apto/escrito · 1 no apto/no escrito · 2 error de uso/plantilla.
4. **Seguridad:** salida por defecto bajo `provisioning/<slug>/` (agregué `provisioning/` al
   `.gitignore` — el config lleva secretos por cliente); OTA password enmascarada salvo
   `--show-secret`; el tool **no toca** el `config.h` del repo ni secretos existentes.
5. **Tests** `tools/test_provision_device.py` (**36 checks, OK**): parcheo (valor + preservación de
   comentario + define inexistente→KeyError), `provision` (nombre/OTA/chat/array/placa/token/
   umbrales/umbral-desconocido), helpers de render/slug, **el contrato** (lo generado pasa el
   linter), **el rechazo** (un override que rompe `temp_min<temp_max<temp_critical` → no escribe),
   before/after sobre el **config.h REAL** (hoy NO apto → tras provisionar APTA), y exit codes de
   `main()` por subprocess (éxito escribe, dry-run no escribe, override malo no escribe, plantilla
   ausente → exit 2).
6. **Doc** `docs/provision-device.md` (uso, flags, contrato, por qué el WARN de Telegram es
   esperado y no bloquea, seguridad, verificación, pendientes de día/hardware).
7. **`QUE_FALTA.md` #4** (en el branch) apunta al nuevo tool con la evidencia.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-07-26-b-provision-device
python tools\test_provision_device.py                 # -> OK: 36 checks
python tools\test_lint_device_config.py               # -> OK: 35 checks (regresion, no lo rompi)
# End-to-end sobre el config.h REAL (dry-run, NO escribe secretos a disco):
python tools\provision_device.py --client "Comercio Demo" --placa 1 --telegram-chat 12345 --dry-run
#   -> VEREDICTO: config APTA ... [dry-run] APTO
# Contraste: el config.h real HOY NO es apto (por eso hace falta el generador):
python tools\lint_device_config.py --from-header firmware_modular\config.h | Select-String "OTA_OPEN|VEREDICTO"
#   -> [ERROR] OTA_OPEN ...  /  VEREDICTO: config NO apta
git diff main --stat                                  # -> 2 tools nuevos + doc + .gitignore(+3) + QUE_FALTA(+1)
git checkout main
```
**Resultado de esta noche:** 36/36 tests OK; el `config.h` real pasa de NO-apto (OTA_OPEN) a APTA
tras provisionar; el generador se niega a escribir configs no aptos (probado); regresión del linter
existente verde. `main` de frioseguro quedó **prístino** (el pointer va en el branch).

## Qué quedó SIN verificar / para el día (Matías + @verificador)
1. **Flashear un config generado en hardware real** y confirmar OTA (con la password única) +
   alertas al chat del cliente. El generador garantiza que el config es *apto por el linter*, no
   que el firmware se comporte — eso es banco. [@firmware]
2. **Fuente de los `chat_id` por cliente**: hoy se pasan por CLI (`--telegram-chat`). Definir de
   dónde salen en el alta comercial, y si a futuro conviene **rutear por `device_id` en el backend**
   en vez de compilar el chat en el firmware (eso haría desaparecer el WARN `TELEGRAM_HARDCODED`).
   [@backend + @comercial]
3. **Mergear el branch** `07-26-b-provision-device` (aditivo: 2 archivos nuevos en `tools/` + doc +
   `.gitignore` + 1 línea en `QUE_FALTA`; 36 tests verdes; no toca firmware ni el `config.h`).
   Acción humana con criterio — no la hago yo.

## Observaciones para el día (no tareas mías)
- **Con esto FrioSeguro tiene el pipeline de provisioning completo:** `scan_secrets` (higiene de
  secretos, 07-10-b, en main) + `lint_device_config` (valida, 07-12, en main) + **`provision_device`
  (genera, esta noche)**. Onboardear un cliente pasa de "editar config.h a mano y rezar" a
  "un comando que produce un config garantizado-apto". Alineado con la definición de "vendible"
  ("credenciales únicas por cliente") y con el objetivo "que quede andando solo".
- El WARN `TELEGRAM_HARDCODED` **persiste a propósito**: su premisa es "el mismo config en varias
  placas" — lo que el generador evita dándole a cada cliente su chat. No bloquea (es WARN, no error).
- No toqué galgas, datalogger ni cosechador. `data/field_captures` de galgas: ni mirado.
- Higiene: dejé frioseguro de nuevo en `main` (venía checkouteado en `07-24-scan-secrets`).

## Reglas respetadas
Solo software (git + Python stdlib) + docs + análisis. **Nada mergeado, borrado, movido ni
deployado**; no borré ninguna rama; `main` de frioseguro quedó **prístino**; no escribí ningún
config generado a git (solo `--dry-run`); `provisioning/` gitignoreado; sin `rm -rf`, `reset --hard`
ni `push --force`; sin migraciones; sin mDNS; sin tocar secretos existentes; sin compilaciones ni
descargas → cero riesgo de timeout. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-26-b-provision-device` (frioseguro, pusheado a origin; sale del `main` de
hoy; 1 commit: `provision_device.py` + su test + doc + `.gitignore` + pointer en `QUE_FALTA`).

## Notas para @verificador
- **DoD** = *"`provision_device.py` genera un `config.h` por-cliente parchando SOLO campos
  por-cliente (resto byte-idéntico), con OTA_PASSWORD única y chat del cliente, y SE NIEGA a
  escribir si el resultado no pasa `lint_device_config`; los 36 tests pasan; el config.h real pasa
  de NO-apto (OTA_OPEN) a APTA tras provisionar"*.
- Ataques sugeridos: (a) `python tools\test_provision_device.py` → 36 OK; (b) romper el contrato:
  pasar `--temp-critical -50` (rompe el orden) y confirmar **exit 1 + archivo NO escrito**;
  (c) confirmar que un config generado no filtra: `git status` tras un run real **no** debe mostrar
  nada bajo `provisioning/` (gitignore); (d) verificar que el resto del `config.h` queda idéntico:
  `diff` del real vs el generado debe tocar SOLO `DEVICE_NAME`/`OTA_PASSWORD`/`TELEGRAM_*`
  (+ umbrales si se pasaron); (e) regresión: `python tools\test_lint_device_config.py` → 35 OK.
