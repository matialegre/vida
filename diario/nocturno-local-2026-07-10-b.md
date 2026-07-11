# Nocturno LOCAL — 2026-07-10 (segunda tarea de la noche, "-b")

> La primera corrida de esta misma noche hizo el calibrador RSSI↔distancia del
> datalogger — ver `nocturno-local-2026-07-10.md` (branch
> `nocturno/local-2026-07-10-rssi-calib`). Este informe es de una **segunda**
> corrida del worker, con OTRA tarea.

## Tarea elegida y por qué
**FrioSeguro — barrida de secretos hardcodeados (PLATA, hueco #6 del PORTFOLIO).**

Recorrí los 4 QUE_FALTA + los 5 nocturnos previos (07-08 ECO-LoRa, 07-09 RX
galgas, 07-09-b SD-integrity, 07-10 RSSI-calib) buscando **UNA** tarea de
**software** prioritaria que **no** esté en un branch nocturno, con la jerarquía
**PLATA y UNIVERSIDAD primero, octubre segundo**. Razonamiento:

- **FrioSeguro es PLATA (tope de la jerarquía).** Los workers previos dijeron que
  no tenía tarea de software nocturna limpia — y para los ítems que miraron
  (migración #3 ya escrita, resiliencia #10 ya renderizada, resumen/retención
  #11-12 prematuros) es cierto. **Pero nadie había tocado el #4 (credenciales) ni
  el hueco #6 del PORTFOLIO** ("Seguridad antes de vender: credenciales
  hardcodeadas en repos … **barrida de higiene antes del primer cliente pago**").
  Eso **es software puro, 100% verificable sin hardware, y es un bloqueante real
  de PLATA** (no se le entrega un sistema a un cliente pago con la llave maestra
  de la cuenta pública en GitHub). Encaja con "UNA tarea bien hecha por noche".
- **UNI** vive fuera de los 4 repos del worker.
- **datalogger/galgas** — sus wins de software limpios ya están en branches
  (ECO-LoRa, INA219, SD-integrity, RSSI-calib, RX×2). Son octubre (2º), además.

Verifiqué en el código, no de memoria, que la filtración es **real y presente**
(no un supuesto): `git grep` + el propio scanner sobre archivos trackeados.

## Qué encontré (evidencia — masked)
El scanner sobre el repo: **34 coincidencias, 14 al nivel de fallo**, exit 1.

- 🔴 **10 × Management API token de Supabase** (`sbp_35…2e47`) en `tests/*.js`
  (`recreate_clean.js`, `fix_users_admin_api.js`, `fix_and_create_users.js`,
  `check_auth_hooks.js`, `diagnose_auth.js`, `find_broken_policy.js`,
  `fix_auth_complete.js`, `fix_device_names.js`, `fix_identities.js`,
  `fix_is_admin.js`). **Controla la cuenta Supabase entera** (proyectos, billing,
  puede leer el service_role). Llave maestra, commiteada y pusheada a GitHub.
- 🔴 **1 × JWT `service_role`** (`eyJhbG…EArQc`) en `tests/recreate_clean.js:4`.
  Bypass total de RLS.
- 🟠 **3 × token de bot de Telegram** (`817516…RdGnI`) en `firmware_modular/config.h:94`,
  `firmware_modular/config_SANTA_CRUZ.h:44`, `DISPOSITIVOS.md:150`. Control del bot
  de alertas (enviar/silenciar alertas a clientes).
- 🟠 **`OTA_PASSWORD ""`** (`config.h:176`) — flasheo remoto abierto en la LAN del
  comercio. Es el QUE_FALTA #4 textual. (Config débil, no filtración → anotado a
  mano, no lo marca el scanner.)
- 🟢 **20 × JWT `anon`** — **público por diseño** (lo protege RLS). El scanner lo
  marca INFO y NO falla. Único pendiente sobre la anon: **verificar que RLS esté
  activo** (día). Clasificar bien esto es lo que evita la falsa alarma que haría
  descartar la barrida entera.

## Qué hice (branch `nocturno/local-2026-07-10-b-secret-scan`, sale de `main`)
Software **aditivo**, sin romper nada, sin tocar la cuenta cloud:

| Archivo | Qué |
|---|---|
| `tools/scan_secrets.py` | Barredor stdlib (sin deps). Escanea **archivos trackeados por git** (los que se filtran al pushear), clasifica por severidad y **distingue anon (ok) de service_role / `sbp_` (crítico) decodificando el payload del JWT**. Patrones curados de alta señal: Management token `sbp_`, JWT Supabase (role-aware), token Telegram, AWS key, clave privada PEM. Salida humana o `--json`, `--fail-on {info..critical}` (def. high), marcador `scan-secrets: allow` por línea, ignora `*.example.*`/binarios. **Exit 0/1/2** para usar en CI/pre-commit. |
| `tools/test_scan_secrets.py` | 13 checks sintéticos — fixtures **fake armados en runtime** (ningún secreto real ni literal en el fuente): service_role→critical, anon→info (no falla), `sbp_`→critical, telegram→high, limpio→nada, allow marker, `.example` ignore, y exit codes de `main()` + `--json` por subprocess. |
| `SECURITY_AUDIT.md` | Hallazgos **enmascarados** (no re-expone) + **runbook de rotación** ordenado (Management token → JWT secret que rota anon+service_role → bot Telegram → OTA_PASSWORD → recién ahí sacar del working tree) + verificar RLS. Marca claramente qué es día/cloud/hardware de Matías. |
| `.gitignore` | Endurecido: `**/secrets.h`, `tests/.env`, `*.pem`, `*.key`, `config.local.h`, `*service_role*`, `__pycache__/` — para que **futuros** secretos no se trackeen. No afecta archivos ya trackeados. |
| `QUE_FALTA.md` (#4) | Anotado "EN BRANCH … pendiente de merge" con el detalle. |

## Cómo verificarlo (comandos exactos, sin hardware)
```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-07-10-b-secret-scan

# 1) Sintaxis
python -m py_compile tools/scan_secrets.py tools/test_scan_secrets.py

# 2) Self-test (fixtures sintéticos, sin secretos reales)
python tools/test_scan_secrets.py            # -> "OK: 13 checks", exit 0

# 3) Barrida real del repo (DEBE fallar: hay secretos que rotar)
python tools/scan_secrets.py .               # -> exit 1, 14 failing
python tools/scan_secrets.py . --json        # para parseo
```
**Resultado obtenido esta noche:** `py_compile` **OK**; self-test **OK: 13 checks**
(exit 0); scan real **exit 1** con **34 total / 14 failing** (10 `sbp_` + 1
service_role + 3 telegram), anon correctamente en INFO (no falla). Sin self-trip
del audit ni del QUE_FALTA (valores enmascarados no matchean). Python 3.14.3.

## Qué quedó SIN hacer (día — Matías; cloud/hardware/decisión, fuera de alcance nocturno)
**El worker NO rota claves ni toca la cuenta de Supabase/Telegram** — es acción de
cuenta cloud + reflasheo, fuera de su alcance. La detección/prevención está hecha;
la **rotación** la hace Matías con el runbook de `SECURITY_AUDIT.md`:
- Rotar Management token `sbp_` (Supabase → Access Tokens → Revoke).
- Regenerar el JWT secret (rota anon **y** service_role) → actualizar Netlify env
  + **reflashear** placas con la nueva anon + apps Android. Coordinar con el
  reflasheo del QUE_FALTA #1 para no flashear dos veces.
- Revocar el bot de Telegram (@BotFather `/revoke`).
- Setear `OTA_PASSWORD`.
- **Verificar que RLS esté activo** en todas las tablas (hace inofensiva la anon).
- Purga de historia (BFG/filter-repo): opcional, decide Matías — una vez rotadas,
  las viejas están muertas.

## Reglas respetadas
Nada borrado. NO se rotaron/tocaron claves ni la cuenta cloud. NO se tocó firmware
funcional (el `OTA_PASSWORD` sigue como estaba — cambiarlo requiere reflasheo, es
día), ni `field_captures` (es de galgas), ni mDNS, ni migraciones. **Los secretos
NO se copiaron en cleartext a ningún archivo nuevo** (todo enmascarado). Solo
software aditivo en un branch nuevo salido de `main`. El branch se puede mergear
apenas @verificador lo revise (no depende de hardware — la rotación sí, pero es
posterior e independiente del merge de la herramienta). Timeouts: sin compilación
pesada (Python puro), verificación instantánea.

## Branch
`nocturno/local-2026-07-10-b-secret-scan` (pusheado a origin, 1 commit). Sale de
`main`.

## Nota para el @director / @verificador / @backend
- **Es la primera vez que se cuantifica el hueco #6 con evidencia.** No es teórico:
  hay una **Management API token de la cuenta Supabase** commiteada y pusheada a
  GitHub — es la exposición más grave del portfolio de electrónica, y bloquea de
  hecho entregarle el sistema a un cliente pago. La **rotación es prioritaria**
  (día). Sugerencia: sumar `python tools/scan_secrets.py .` como pre-commit hook y,
  a futuro, correr el scanner también en galgas/datalogger (hueco #6 los nombra:
  "Supabase anon en RuView, CREDENCIALES.txt"). El scanner es genérico, sirve en
  los 3 repos.
- La misma clase de filtración (anon key hardcodeada) en galgas/RuView es
  **INFO** si RLS está activo — no confundir con esto. Lo grave acá es el
  **Management token + service_role**, que NO son públicos por diseño.
