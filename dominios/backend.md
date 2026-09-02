# Dominio: backend (agente @backend)

Doc de dominio + bitacora. El agente lo lee al arrancar y lo actualiza al cerrar. Backlog inicial: ver seccion "Tu backlog inicial" en ~/.claude/agents/backend.md (copia en ../agentes/backend.md).

## Bitacora
- 2026-07-07 - Agente creado por Claude Fable con backlog real de los repos migrados (C:/Proyectos).

- 2026-07-08 [BRIEFING GIMAP] — leer ../BRIEFING_EQUIPO_GIMAP.md y los 4 docs (PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO). Para vos: telemetría LIVIANA (0.33Hz+batería) LoRa→receptor→internet→cloud; poca data, muchos años; los 3 modos campo/lab/ráfaga definen qué llega.

- 2026-07-13 [RUNBOOK cierre bloque backend FrioSeguro] — Escrito `C:\Proyectos\frioseguro\docs\RUNBOOK_backend_2026-07-13.md` para que Matías corra con SU login (login/link, migración, deploy function, cron, rotación de claves, smoke E2E). NO ejecuté nada contra la nube. Hallazgos clave del código:
  - **project-ref FrioSeguro = `nwugnhsktcihusopfldu`** (NO confundir con galgas `wtjjxhoyoqeicrydsppg`). Sale de los headers `--project-ref` en supabase/functions/*/index.ts.
  - **NO usar `supabase db push`**: el repo no tiene `supabase/migrations/` versionado, son .sql sueltos aplicados a mano. Runbook recomienda **SQL Editor** (migración `migration_monthly_summaries.sql` es idempotente, `CREATE ... IF NOT EXISTS`).
  - **`cron-monthly-summary` NO necesita secrets**: sólo usa `SUPABASE_URL`/`SUPABASE_SERVICE_ROLE_KEY` (reservados, auto-inyectados). VAPID es de las functions de push, no de ésta.
  - **HUECO RLS detectado**: `migration_monthly_summaries.sql` crea la tabla SIN RLS → fuga cross-tenant si el dashboard la lee con anon. Runbook incluye paso 2.3 de hardening (ENABLE RLS + policy por owner) — OJO: hay que confirmar si tenant en `devices` es `owner_id` vs `user_id` antes de aplicar. **Tarea pendiente: agregar la RLS a la migración en el repo (append-only, migración nueva).**
  - **GOTCHA de la rotación JWT (paso 5.2, único destructivo)**: invalida anon+service_role de golpe → tira dashboard Netlify (`VITE_SUPABASE_KEY`), firmware (anon horneada en config.h → reflashear), Android, y **`app.settings.service_role_key`** que los cron llevan congelado por `ALTER DATABASE` (migration_cron_jobs.sql:189) — NO se auto-actualiza, hay que re-correr el ALTER con la key nueva (paso 5.6) o mueren todos los cron. Coordinar rotación con reflasheo v4 (QUE_FALTA #1) para no flashear dos veces.
  - Secretos a rotar (SECURITY_AUDIT): (1) mgmt token `sbp_…2e47` en 10 tests/*.js, (2) JWT secret → anon+service_role, (3) bot Telegram `817516…RdGnI` en config.h/config_SANTA_CRUZ.h/DISPOSITIVOS.md, (4) `OTA_PASSWORD` vacío.
  - Pendiente cierre: Matías corre el runbook → evidencias (6.1 JSON 200 + fila, 6.3 succeeded, 6.4 401 con claves viejas) → @verificador antes de declarar producción.

- 2026-07-13 [CAMBIO DE PLAN → BOOTSTRAP proyecto Supabase NUEVO] — Se abandona prod viejo (`nwugnhsktcihusopfldu`), se levanta uno de 0. El runbook de rotación (RUNBOOK_backend_2026-07-13.md) queda OBSOLETO (ya no se rota nada). Escrito `C:\Proyectos\frioseguro\docs\RUNBOOK_bootstrap_2026-07-13.md`. NO ejecuté nada. Hallazgos verificados contra el firmware (`firmware_modular/supabase.h` + `config.h` L85-86):
  - **SCHEMA CANÓNICO = `supabase/SETUP_COMPLETO.sql`** (1087 líneas). Descartar los otros 4: schema.sql/schema_unified.sql tienen tablas que el firmware NO usa (temperature_logs/device_config); schema_v2/_clean son subconjunto sin auth/RLS/sensor_probes/payments. Verificado columna a columna: `devices` de SETUP_COMPLETO tiene EXACTO lo que lee `supabaseRefreshDeviceName` (device_id,name,config_version,temp_critical,alert_delay_sec,door_open_max_sec,defrost_cooldown_sec) + las v4+ (connection_mode,gsm_signal,uptime_sec,free_heap) YA horneadas; `readings` matchea `supabaseSendReading`; cooldown y last_temp_c ya foldeados.
  - **SETUP_COMPLETO es el snapshot consolidado**: las migration_* viejas (auth, payments, push, sensor_probes, subscriptions, admin, resilience, cooldown, patches, cron_jobs) YA están adentro → NO re-correr. Solo posteriores al snapshot: `migration_ota_updates.sql` (IMPRESCINDIBLE, crea ota_updates+bucket firmware-ota, self-contained idempotente) y `migration_monthly_summaries.sql` (OPCIONAL).
  - **FIX RLS incluido en el bootstrap**: única tabla sin RLS era `monthly_summaries`; el runbook la activa con policies usando el helper `user_has_device_access` (consistente con el resto). Todas las demás (15 de SETUP_COMPLETO + ota_updates) ya traen RLS. Cero tablas sin policy.
  - **Caveat de diseño anotado**: policies device-tables usan `auth.role()='anon' OR ...` a propósito (firmware auth con anon key). Aislamiento por cliente vive en capa `authenticated` (dashboard). Aislamiento duro a nivel firmware = token por device = tarea futura, no bloquea.
  - **Gap menor OTA (backlog)**: firmware PATCHea progreso con `progress_pct/progress_bytes/updated_at` pero la tabla ota_updates solo tiene `progress` → PATCH de progreso falla en silencio; descarga/flash/status OK. No bloquea.
  - Secuencia: crear proyecto sa-east-1 → pg_cron+pg_net → SETUP_COMPLETO (reemplazar TU_SERVICE_ROLE_KEY x3 si push) → ota_updates → monthly_summaries+fix RLS → ALTER DATABASE app.settings → login/link+deploy functions → SETUP_CRON_JOBS → firmware config.h L85-86 (URL+ANON nuevas)+reflash → smoke E2E → @verificador.
  - Espero project-ref nuevo de Matías para arrancar.

- 2026-08-27 [EMSICA — investigación mail automatizado] — Informe entregado en `C:\Proyectos\emsica-comercial\entregables\informe_mail_automatizado.md`. Verificación DNS real (nslookup 2026-08-27):
  - **MX = M365** (`emsica-com-ar.mail.protection.outlook.com`), SPF `v=spf1 include:spf.protection.outlook.com -all` (estricto), DMARC `p=none; rua=rua@dmarc.brevo.com`.
  - **Hallazgo clave: Brevo YA empezado** — TXT `brevo-code:2099c07c...` plantado + DMARC reportando a Brevo. Falta DKIM de Brevo (`mail._domainkey` no existe). Averiguar de quién es esa cuenta Brevo.
  - **DKIM de M365 tampoco activo** (selector1/selector2 no existen) → los mails de EMSICA ya hoy tienen riesgo spam. TXT basura en el apex (`"@"`, `"@1"`, DMARC pegado como texto plano) = carga manual fallida, limpiar.
  - Web ≠ mail: A `107.180.50.171` = `host.secureserver.net` (GoDaddy compartido), FTP `emsica@control-bay.com` → Control Bay LLC (control-bay.com, "Sistemas de Control Industriales", Next.js) administra el hosting. SMTP del hosting DESCARTADO para campañas.
  - **Recomendación: Brevo** (free 300/día o Starter USD 9-25/mes) para campañas a los 596 contactos; **Graph API `Mail.Read`** para el detector de contactos nuevos → CSV para revisión humana + autorización escrita de gerencia. Piloto: completar DKIM (Brevo + M365) → 10 mails de prueba → tandas 50-100/día.
  - Pendiente del cliente: acceso cuenta Brevo, acceso DNS (Control Bay/GoDaddy), admin M365, casilla a usar, CSV del Access, autorización escrita.

## 2026-08-27 — Paradise (Eduardo): backend completo montado
Schema `paradise` en la Supabase del kiosco (`egdlgprnanrlvmjfshrv`) — TEMPORAL por límite free (migración documentada en `C:\Proyectos\tienda-cosmetica\README.md`). Tablas categorias/productos/pedidos/ventas_local + vista clientes, RLS (anon solo lectura de catálogo), RPCs security definer transaccionales (`crear_pedido`, `vender_local`, `ajustar_stock` — validan y descuentan stock con `for update`), bucket público `paradise` con políticas de escritura solo authenticated, usuario auth del negocio, Realtime en productos, búsqueda GIN en español. Verificado por REST end-to-end. Mail serverless `api/nuevo-pedido.js` (Gmail SMTP) esperando app password.

## 2026-08-28 — EMSICA mail_html: upload de imágenes con Vercel Blob
Objetivo: el generador de mails (`C:\Proyectos\emsica-comercial\entregables\mail_html`) permite subir
fotos directo desde el formulario en vez de exigir que el cliente hostee la imagen aparte.

- **`api/upload.js`** (Vercel Function): firma permisos de subida con `handleUpload` de `@vercel/blob/client`
  (**no** `put()` directo). Motivo del cambio de plan respecto a lo pedido originalmente: Vercel tiene un
  límite DURO de 4.5 MB en el body de cualquier función serverless normal, no configurable; el requisito
  era aceptar hasta 8 MB, así que un POST multipart directo habría fallado con 413 en fotos grandes. El
  patrón oficial de Vercel para esto es "client upload": el archivo va del navegador DIRECTO al store, la
  función solo firma un token de corta duración y valida ahí `allowedContentTypes` (jpeg/png/webp) y
  `maximumSizeInBytes` (8 MB) — la validación queda igual de dura, solo cambia el transporte.
- **GOTCHA de `@vercel/node` que costó tiempo de debug**: exportar `module.exports = async function(request){}`
  (default export, un solo parámetro) NO lo detecta como "Web handler" — cae al modo Node clásico
  `(req,res)` y `request.json()` cuelga porque `req` ahí es un `IncomingMessage`, no un `Request`. Hay que
  exportar por método HTTP: `module.exports.POST = async function(request){}` (o `export function POST(){}`
  en ESM). Sin esto la función cuelga 30s+ y Vercel la mata sin error claro en el log.
- **`vendor/vercel-blob-client.mjs`**: el sitio es estático sin bundler propio, pero `@vercel/blob/client`
  importa `node:crypto`/`undici` (remapeados a versión browser vía el campo `"browser"` de su package.json,
  que solo respetan los bundlers). Se agregó `esbuild` como devDependency y `build.js` lo bundlea
  (`platform: 'browser'`) a este archivo — es un artefacto generado, se commitea igual que `generador_mails.html`.
- **`vercel.json`**: se agregó `"outputDirectory": "."`. Al aparecer `package.json` con un script `"build"`,
  Vercel pasa de "sitio estático plano" a "Other framework con build command" y por defecto espera el output
  en `public/` → sin este flag el deploy entero se hubiera roto (`Error: No Output Directory named "public"`).
  Verificado con `vercel dev` antes y después del fix.
- **Verificación E2E real** (no solo "compila"), con `vercel dev` local + credenciales reales de `.env.local`:
  token de subida real generado, foto real subida al store `emsica-fotos`, URL pública confirmada con `curl`
  (200, `Content-Type: image/png`), rechazo real de un `.txt` disfrazado de imagen (`Content type mismatch`)
  y de un archivo de 9 MB (`File is too large`, límite real 8 388 608 bytes) — la validación es server-side
  vía el scope del token firmado, no solo un chequeo de JS en el navegador. Con Playwright sobre
  `generador_mails.html` real: elegir archivo en el campo de logo y en el de un bloque de producto completa
  solo el campo de URL correspondiente, dispara el re-render de la vista previa (la URL aparece en el
  `srcdoc` del iframe), y no rompió nada existente (cambiar de preset, agregar bloque, Descargar, Copiar
  HTML — sin errores de consola). Blobs de prueba borrados del store al terminar.
- **Pendiente**: correr el mismo flujo contra el deploy real de `emsica-mailer.vercel.app` (el Director
  hace el `vercel --prod` o el deploy automático de git); local con `vercel dev` usa las mismas credenciales
  pero es proceso distinto. Repo `emsica-comercial` no tiene remote configurado — commit local únicamente,
  falta push/deploy.
- Archivos tocados: `C:\Proyectos\emsica-comercial\entregables\mail_html\api\upload.js` (nuevo),
  `generador_plantilla.html` (UI de subida + wiring), `generador_mails.html` (regenerado), `build.js`
  (bundlea vendor/), `vendor\vercel-blob-client.mjs` (nuevo, generado), `package.json`/`package-lock.json`
  (nuevos), `vercel.json` (outputDirectory), `.gitignore` (node_modules), `LEEME_generador.md` (sección
  nueva para el cliente).

## 2026-09-01 — TERMOVIGÍA: plan de plataforma (`C:\Proyectos\frioseguro\PLAN_PLATAFORMA_TERMOVIGIA.md`)
Plan ejecutable pedido por el Director para el relanzamiento (5 equipos de demo en septiembre, Dreyfus en octubre, primer cobro después). Nada se ejecutó contra la nube. Hallazgos y decisiones:
- **`BOOTSTRAP_2026-08-19.sql` (Santa Cruz) es una copia de `SETUP_COMPLETO.sql` + `device_logs`**: las "dos familias" ya comparten esquema, solo difieren en proyecto. Decisión: **UNA Supabase multi-tenant** reusando `cjdluhemschrynijzvap` (el dashboard en prod ya apunta ahí — y está en **Vercel**, `frioseguro-dashboard.vercel.app`, no Netlify como dice el estado del 08-31). Pro USD 25/mes al primer cobro. Santa Cruz (`vihxmqjjprtlzajlatvu`) queda vivo hasta que el reefer reciba por OTA un firmware con credencial propia. Staging = segundo proyecto free (reemplaza `supabase start`, no hay Docker en esta máquina).
- **Modelo**: `organizations → org_members(owner/manager/auditor) → sites → chambers → sensor_probes.chamber_id / doors`; `probe_readings` por trigger fan-out desde `readings` (contrato del firmware intacto); admin Termovigía = `user_profiles.role='admin'` que ya existe.
- **Credencial por equipo = header `X-Device-Key` + función `device_auth()` (pgcrypto, STABLE, lee `request.headers`)** usada por las policies. Elegida sobre Auth-user-por-device (refresh en ESP32) y sobre Edge Function `ingest` (432k invocaciones/mes con 10 equipos, cold start). Un `addHeader` más en `_sbHeaders()` de `supabase.h`. Anon queda solo SELECT de `firmware_releases`.
- **OTA**: bucket privado + `firmware_releases` (nombre inmutable `fw_<v>_<sha8>.bin`, SHA en la base) + Edge `ota-manifest` que devuelve URL firmada 600 s. Cierra CRÍTICO-2/3 y ALTO-1/2 de la auditoría SCZ.
- **Módulos con horas**: vigía+escalado 14 h (reusa branch 08-23, 28 tests; outbox `notifications` + `notification_rules`; SMS Twilio **USD 0,1034/SMS a AR + USD 1,15/mes número**, fuente twilio.com/sms/pricing/ar 2026-09-01; SMS desde el propio equipo Premium ante corte), umbrales por cámara con horario/defrost 10 h (`chamber_thresholds` + `effective_threshold()` + `cron-evaluate` redundante al firmware), **reporte PDF/CSV con SHA-256 + `verify-report` público 20 h** (pdf-lib en Deno, reusa `_shared/monthly_summary.ts`, `reports.verify_code` impreso en el pie), `events` con inicio/fin 8 h, portal/admin 30-40 h @frontend + 6 h backend, relay HTTP 6 h solo si @firmware demuestra que el A7670 no hace TLS.
- **Upsells** (§4 del plan): TV de estado 4 h/$5k, apertura fuera de horario 6 h/$5k, HACCP 16 h/$10k, SCT-013 + predictivo 12 h/$8k (bloqueado por R5 banco), API + webhooks para Modulia 10 h/$15k, WhatsApp 8 h/$8k, sirena con lógica 4 h/$3k.
- **Sprints**: S1 (2-15 sep) seguridad + tenancy + vigía + rebrand; S2 (16-29 sep) umbrales + reporte con hash + events + SMS + ADR 4G; S3 (30 sep-13 oct, Matías en Dreyfus) solo subagente contra staging: upsells 4.1/4.2/4.7, WhatsApp, HACCP, admin nuevo, cosecha a biblioteca.
- **Solo Matías**: rotar PAT `sbp_`, JWT secret (un solo día junto con el flasheo de los 5 para no reflashear dos veces; re-correr `ALTER DATABASE app.settings.service_role_key` o mueren los cron), BotFather, borrar `%TEMP%\sb*.txt`, Pro, flasheo/banco, precios, **registrar `termovigia.com.ar` antes del 1-oct** (la URL de verificación va impresa en cada PDF).
- Nota dejada a @frontend en `dominios/frontend.md`. Próximo paso mío: S1 del sprint 1 (staging + `0000_baseline.sql` + migración de tenancy) cuando el Director lo designe.

## 2026-09-02 — TERMOVIGÍA: servidor propio en `C:/Proyectos/frioseguro/servidor/`
Encargo: autohospedar la plataforma. **Nada se ejecutó contra la nube ni se commiteó.**

**Cambio de destino a mitad de tarea (Director)**: el relevamiento mostró que la PC propuesta es la MISMA que corre el ERP de 13 locales (Win 11 Home, Ryzen 5 5600G, 23,3 GB, Postgres 18 con 4 bases y `max_connections=100` compartido entre :8000/:8010/:8050 — **ya tumbó el ERP dos veces**; sin UPS, uptime 4,9 días; sin Docker/WSL2/Hyper-V). **Descartada.** Destino: host Linux genérico (VPS USD 5-8 recomendado, o mini PC con UPS). El motivo con números quedó escrito en `LEEME.md` §1 "Por qué no en la PC del ERP" y `preflight.ps1` **se niega a seguir** (exit 2) si detecta esa máquina (Postgres como servicio + puertos 8000/8010/8050/3456 escuchando).

**Stack** (5 servicios, `docker compose up -d`): Postgres 16 + PostgREST 12 + `api` propio (Python/FastAPI) + Caddy + backup. **Solo Caddy publica puertos** (80/443); Postgres sin `ports` salvo `127.0.0.1:5433` para mirar local. Variante `docker-compose.tunel.yml` con **Cloudflare Tunnel** (cero puertos en el router) para el caso mini PC en oficina; `caddy/Caddyfile.tunel` con `auto_https off` porque con túnel el ACME no puede validar.
- **La decisión que ordena todo**: mantener la superficie **PostgREST** (`/rest/v1/...`) → migrar un equipo es cambiar 3 `#define` + 2 `addHeader`, no reescribir firmware. La `SUPABASE_ANON_KEY` pasa a ser un JWT HS256 propio (mismo secreto que `PGRST_JWT_SECRET`), generado por `herramientas/generar_secretos.py --tokens`.
- **Shim de compatibilidad `auth`** (`sql/000`): `auth.users`, `auth.uid()`, `auth.role()`, `auth.jwt()` + roles `anon/authenticated/service_role/authenticator` con los nombres de Supabase → todo el SQL heredado se porta sin traducir. Sin GoTrue: `POST /auth/login` emite el JWT y bcrypt lo valida `pgcrypto` como allá.
- **Sin pg_cron** (decisión, documentada): no está en `postgres:16-alpine` y las tareas igual necesitan salir a internet. Planificador en `api/tareas.py`, trabajo pesado en SQL (`sql/060`).
- **Migraciones APPEND-ONLY** con corredor propio (`api/base.py`): guarda SHA-256 por archivo y **falla el arranque** si alguien editó una vieja. No se usa `docker-entrypoint-initdb.d` porque solo corre al crear el volumen.

**HALLAZGOS del código real (verificados línea a línea contra `firmware_modular/supabase.h`)**
1. **El firmware POSTea 7 columnas que NO existen** en `SETUP_COMPLETO.sql` ni en `BOOTSTRAP_2026-08-19.sql`: `any_door_open`, `local_ip`, `firmware_version`, `public_ip`, `wifi_ssid`, `wifi_password`, `ping_ms` (supabase.h:263-299), + `wifi_scan_results`/`wifi_scan_at` en el PATCH a `devices`. PostgREST rechaza el insert **entero** con 400/PGRST204 → contra un esquema creado desde el repo **no entraría ni una lectura**. En la nube se deben haber agregado a mano. Creadas en `sql/010`, y `POST /ingest` descarta lo desconocido en vez de tirar la lectura.
2. **`wifi_commands` no existe en ningún `.sql` del repo** y `supabase.h:767` la consulta → el cambio remoto de red venía recibiendo 404 en silencio. Creada.
3. **El firmware no valida el certificado TLS** (`http.begin(url)` sin CA = insecure en el core ESP32). No es regresión (con Supabase es igual), pero con servidor propio **se puede pinnear** la ISRG Root X1: tarea para @firmware.
4. **`wifi_password` del cliente viaja en cada lectura**. El servidor la descarta por defecto (`TV_GUARDAR_PASSWORD_WIFI=0`); pedido a @firmware: dejar de mandarla.

**Seguridad**: `device_auth()` con `X-Device-Key` (bcrypt, STABLE) + RLS por `org_id` en las 22 tablas, grants por columna en `devices`, DELETE de anon restringido **solo** a la fila fantasma `00:00:00:00:00:00`. Puente `devices.legacy_anon` para no dejar mudo al reefer de SCZ; `v_salud.equipos_sin_credencial` tiene que llegar a 0. OTA con nombre inmutable `fw_<v>_<sha8>.bin` + URL firmada HMAC atada a `(archivo, vencimiento, device_id)`, TTL 600 s (el bucket público se elimina). Rate limit propio (Caddy stock no trae `rate_limit`): login 5 + 1/30 s.

**Vigía externo**: **healthchecks.io Hobbyist = USD 0** (20 checks, 3 personas; el pago arranca en USD 20/mes — verificado hoy). Dead-man's switch: `_latir()` **consulta la base antes de pinguear**. Canal primario de aviso a Matías = la línea de WhatsApp propia (**OpenClaw :3456**) vía `canales.notificar_matias()`, con Telegram de respaldo. **Contrato del webhook SIN CONFIRMAR**: el docstring de `api/canales.py` lista qué preguntar (ruta, nombres de campo, auth, y si es alcanzable desde fuera de la LAN — decisivo si el server va a un VPS).

**Backups**: `pg_dump -Fc` diario, nombre definitivo solo al terminar, mensual el día 1, + **prueba de restauración** (`restaurar_prueba.sh`/`.ps1`) que levanta un Postgres descartable, restaura y verifica filas Y funciones. Un backup no restaurado es un archivo.

**Costos (COSTOS.md, con el tiempo de Matías adentro)**: Supabase Pro USD 25 ≈ **$50.000/mes** vs VPS ≈ **$63.000/mes** vs mini PC amortizada ≈ **$89.000/mes** — porque las 2-2,5 h/mes de mantenimiento a $25.000/h pesan más que los USD 25. Puesta en marcha: 9 h ≈ $225.000 vs 0 h. **Recomendación: quedarse en Supabase Pro por ahora** y dejar este stack listo como (a) respuesta a un cliente que exija datos propios, (b) plan B, (c) el `sql/` multi-tenant que **también hay que aplicar en Supabase** — el trabajo sirve en los dos lados. Reconsiderar con criterios medibles (cliente lo exige · >8 GB · hace falta host propio para el relay 4G · Matías con >10 h/semana).

**Evidencia**: 42 tests de lógica pura pasan (`python -m unittest discover -s api/tests -t api`) — JWT (incluye rechazo de `alg:none`), firma OTA (vencida / otro equipo / otro archivo / path traversal), vigía de silencio (9 casos), filtro de lecturas DS18B20 (-127/85), limitador y retención. Los 15 `.py` compilan. **No hay Docker ni psql en esta máquina**: los dos compose validan con parser YAML (solo caddy publica puertos; todas las variables `${}` documentadas en `.env.example`, ninguna sobrante) y los 7 `.sql` pasan un chequeo de dólar-quoting/paréntesis, pero **no se corrieron contra una base**. Comando exacto pendiente en el host: `docker compose up -d && docker compose logs -f api` y después `python herramientas/verificar_e2e.py https://DOMINIO --anon <JWT> --equipo <MAC> --clave <KEY>`.

**Falta y bloquea**: elegir host. **Falta y no bloquea**: dominio (`termovigia.com.ar` sin registrar; puente DuckDNS), contrato del webhook de OpenClaw, VAPID para push, reporte mensual PDF, y Realtime — el panel usa websockets que PostgREST no tiene (`MIGRACION.md` §5: arrancar con polling 5-10 s, después SSE con LISTEN/NOTIFY, ~50 líneas).

## 2026-09-02 — TERMOVIGÍA: cuentas de personas y contrato del portal (Vercel → servidor propio)
Encargo del Director: *"deployo en Vercel una página ligada a esta PC con cuentas y contraseñas para
las personas"*. Mi parte = autenticación y modelo de acceso; el portal lo hace @frontend contra
`C:\Proyectos\frioseguro\servidor\API_PORTAL.md`. **Nada se ejecutó contra una base ni se commiteó.**

**Migración nueva `sql/070_cuentas_personas.sql`** (append-only, idempotente, no toca 000-060):
- **bcrypt, no Argon2id** — decisión argumentada en la cabecera del archivo. Argon2 exigiría (a)
  construir imagen propia de Postgres (`postgres:16-alpine` no trae argon2/pgsodium → duplica la deuda
  de parcheo que SEGURIDAD.md ya cuenta como el costo real del autohospedaje), (b) `argon2-cffi` en el
  api (dependencia con binario C en el camino de auth + el hash sale de la base), o (c) hashear en el
  navegador (nunca). bcrypt de `pgcrypto` **ya está**, es el mismo que usa GoTrue → **los hashes de
  Supabase se importan tal cual** con `password_algo='bcrypt'` (nadie resetea nada), y compara dentro
  de Postgres igual que `device_key_hash`. Coste 12.
- **El detalle que casi nadie mira: bcrypt trunca en silencio a 72 bytes.** Se hashea
  `base64(sha256(clave))` (44 chars). Hay test que lo demuestra: dos claves de 80 caracteres que
  comparten los primeros 72 NO abren la misma cuenta.
- Roles: `org_members.role` owner/manager/auditor (ya existían en 020) + admin en `user_profiles`. Se
  **aprietan** las policies de escritura de 030 (que eran "cualquier miembro de la org"):
  `auth.puede_configurar()` (owner|admin) y `auth.puede_operar()` (owner|manager|admin). El auditor de
  bromatología no escribe.
- `auth.refresh_tokens` (SHA-256 del token, familia, rotación + **detección de reuso** → revoca la
  familia entera), `auth.login_attempts`, bloqueo escalonado 5→15 min / 10→1 h / 15→24 h, y
  `token_generation` para poder **revocar un JWT** (que por definición no se revoca) al cambiar la
  clave o desactivar a alguien.
- `auth.autenticar()` hace validación + bloqueo + registro **en una sola función**: evita el bug de
  "validé bien pero me olvidé de contar el intento fallido" en algún camino del código. Incluye un
  `crypt()` contra salt fijo cuando el usuario no existe, para que "no existe" y "clave mala" tarden lo
  mismo (si no, se enumeran los mails de los clientes con un cronómetro).
- Cerradas con RLS `events`/`notification_rules`/`notifications`, que 050 había dejado sin policy.

**CLAIM EXACTO del JWT** (documentado en 070 y en API_PORTAL.md):
`{sub, role:"authenticated", email, org_id, org_rol, es_admin, gen, typ:"acceso", iat, exp(15 min)}`.
- `role` es el rol de **Postgres** (PostgREST hace `SET ROLE` con él): el rol de negocio va aparte en
  `org_rol`. Hay un test que lo fija para que nadie lo "mejore".
- **Regla de oro: `org_id` ACOTA, NUNCA OTORGA.** `user_org_ids()` se redefinió como
  `org_members ∩ claim`; `is_admin()` como `claim AND user_profiles`. Un token con el `org_id` ajeno da
  **cero filas**, no las del otro. Vale también si mañana se filtrara el secreto de firma.

**`api/identidad.py` — el archivo delicado.** El api se conecta con el **dueño de las tablas**, que NO
está sujeto a RLS (las tablas son ENABLE, no FORCE). Si el portal leyera con esa conexión vería a
todos los clientes. `como_persona()` hace `SET LOCAL request.jwt.claims` + `SET LOCAL ROLE authenticated`
—exactamente lo que hace PostgREST— dentro de la transacción del pool. Por eso las consultas de
`rutas_portal.py` **no llevan `WHERE org_id`**: si el filtro dependiera de que el programador se
acuerde, un día no se va a acordar. 070 concede la membresía de rol al dueño para poder hacer ese SET.

**Endpoints nuevos**: `POST /auth/login` (limitador de **dos cubetas**: por IP y por email — con una
sola, el ataque distribuido contra una cuenta pasa por el hueco de la otra), `/auth/refresh` (rota el
token), `/auth/logout` (revoca de verdad; `{"todas":true}` cierra todos los dispositivos), `GET /yo`,
`/auth/cambiar-clave` (cierra todas las sesiones), `/admin/usuarios` (alta/listado/reseteo/desactivar/
desbloquear, **solo admin, sin registro público**), y los de datos: `/portal/resumen`,
`/portal/camaras` (con última lectura y `estado` calculado en el SERVIDOR para que web, app y PDF digan
lo mismo), `/portal/camaras/{id}/historial` (auto: cruda ≤7 días, `hourly_stats` más allá — 30 días
crudos son 86.000 puntos para dibujar 900 px), `/portal/equipos` (expone `mudo` calculado por reloj:
`is_online` lo escribe el equipo y queda en `true` para siempre si le cortan la luz de golpe),
`/portal/eventos`, `/portal/alertas`, `POST /portal/alertas/{id}/reconocer`, `PATCH /portal/camaras/{id}`.

**CORS**: `TV_ORIGENES_PORTAL` (lista exacta, **se rechaza `*`** — con `allow_credentials` el navegador
lo ignora igual, así que aceptarlo no es "permisivo": es "roto y difícil de diagnosticar") +
`TV_ORIGEN_PATRON` anclado para los previews de Vercel. **Decisión que hay que tomar antes del deploy**:
con el portal en `*.vercel.app` la cookie del refresh es de terceros y Safari/Firefox la descartan →
hace falta `TV_REFRESH_EN_CUERPO=1` y la sesión se pierde al recargar. Con `portal.termovigia.com.ar` +
`api.termovigia.com.ar` (mismo sitio registrable) la cookie es `SameSite=Lax` y funciona en todos.
**Otro motivo para registrar `termovigia.com.ar` antes del 1-oct.** `AJUSTES.revisar()` avisa en el
arranque si quedó en la combinación mala.

**SEGURIDAD.md §6 nueva**: por qué el access token va **en memoria** y no en `localStorage` (cualquier
dependencia npm comprometida o un `dangerouslySetInnerHTML` se lleva la sesión entera, y un JWT no se
revoca), por qué el refresh sí va en cookie `httpOnly` con `Path=/auth`, por qué CORS no protege el
servidor (lo aplica el navegador; `curl` llega igual), y qué NO hay (MFA, recuperación por mail).

**`wifi_password` (hallazgo abierto) — camino escrito en SEGURIDAD.md §4.2, tres pasos**: (1) ya hecho,
el servidor la descarta y no loguea el cuerpo; (2) **@firmware: borrar la línea 296 de `supabase.h`** —
es UNA línea, el servidor ignora los campos que faltan y los desconocidos, así que firmware viejo y
nuevo conviven y no hace falta coordinar despliegue; seguir mandando `wifi_ssid`, que sirve para
diagnosticar y no es secreto; (3) si algún día hace falta verificar la credencial cargada, comando
puntual `WIFI_DIAG` que responde **enmascarada** (`Casa1234`→`Ca****34`). Recién **después** del paso 2
se dropea la columna: hacerlo antes haría que PostgREST rechace la **lectura entera** de todo equipo
con firmware viejo, y perderíamos temperaturas por proteger un dato que ya estábamos tirando.
Las 7 columnas del firmware y `wifi_commands` ya estaban creadas en `sql/010` (sesión anterior) —
verificado hoy: contra este esquema la lectura entra.

**Evidencia**: **77 tests de lógica pura en verde** (`python -m unittest discover -s api/tests -t api`;
eran 42 → +35: forma exacta del claim, contraseña inicial dictable —el test encontró una `Z` que se
confunde con el 2 y se sacó del alfabeto—, generador que pasa su propio validador, hash del refresh,
permisos por rol, y CORS incluido el patrón de previews sin anclar que dejaría pasar
`...vercel.app.malo.com`). Los 18 `.py` compilan; los 8 `.sql` pasan el chequeo de dólar-quoting y
paréntesis. **No hay Docker, psql ni fastapi en esta máquina**: nada se corrió contra una base.
`api/tests_base/test_aislamiento.py` (25 tests) es la evidencia real del aislamiento — se **saltea con
motivo escrito** si no hay base, para que "saltado" no se confunda con "pasó". Comando exacto en
`api/tests_base/__init__.py`:
`TV_DSN_TEST="postgres://termovigia:PASS@127.0.0.1:5433/termovigia" python -m unittest discover -s api/tests_base -t api -v`
Cubre: tabla por tabla en los dos sentidos, claim `org_id` falsificado, `es_admin` falsificado, sin
claims, cambio de identidad en caliente (el caso del pool), auditor que no escribe, bcrypt no truncado,
bloqueo al 5º intento, y dos tests **contra el catálogo** (`pg_class`/`pg_policy`) que encuentran
cualquier tabla futura sin RLS o con RLS y sin policy, sin que nadie tenga que acordarse de agregarla a
una lista. Incluye `test_00` que verifica que `SET ROLE` funciona de verdad: sin eso, todos los demás
pasarían en falso viendo todo como dueño de las tablas.

**Archivos**: `sql/070_cuentas_personas.sql`, `api/identidad.py`, `api/rutas_auth.py`,
`api/rutas_portal.py`, `api/logica/cuentas.py`, `api/tests/test_cuentas.py`, `api/tests_base/` (2),
`herramientas/crear_usuario.py`, `API_PORTAL.md` (nuevo, 8 secciones con curl reales); tocados
`api/principal.py` (CORS + routers; se quitó el `/auth/login` viejo, que daba 8 h sin refresh, sin
`org_id` en los claims —la RLS no podía acotar por organización—, sin bloqueo y sin registro de
intentos), `api/ajustes.py`, `api/tareas.py` (higiene de sesiones), `caddy/Caddyfile*`,
`docker-compose.yml`, `.env.example`, `SEGURIDAD.md`, `LEEME.md` §10, `MIGRACION.md`.

**Falta y bloquea el deploy**: elegir el host (sigue pendiente) y decidir dónde vive el portal (dominio
propio vs `*.vercel.app` — cambia la configuración de la cookie).
**Falta y no bloquea**: Realtime (polling 5-10 s mientras tanto, `MIGRACION.md` §5), push VAPID,
reporte PDF. **Para @verificador**: correr `test_aislamiento.py` contra base real y los pasos 5 y 6 de
`API_PORTAL.md` §8 (token basura y sin token → 401) antes de darle acceso a ningún cliente.

## 2026-09-02 (b) — TERMOVIGÍA: ruta Windows nativo + NOTIFICADOR (cambio de arquitectura)
Dos encargos encadenados. **Nada se ejecutó contra la nube. Sin commit.**

**1) Docker no es viable en la máquina destino.** El diagnóstico de allá: SVM
deshabilitado en firmware → habilitar Docker exige BIOS + reinicio de la máquina que corre
el ERP de 13 locales. Descartado con razón. Lo que SÍ hay: PostgreSQL 18 como servicio
(data dir `D:\ERP MUNDO OUTDOOR\BASE DE DATOS`, puerto 2048, `max_connections=100` con ~40
backends del ERP), Caddy por winget, Python, 80 y 443 libres. Escrita la **segunda ruta de
despliegue** en `servidor\WINDOWS_NATIVO.md` + `servidor\windows\` (13 scripts .ps1). La de
Docker NO se tocó: sigue siendo la buena para VPS/mini PC Linux, y `LEEME.md` ahora abre con
un índice de **dos arquitecturas × dos rutas**.

**2) A mitad de tarea, cambio de prioridad de Matías que simplifica todo**: el motivo real
del servidor propio era **poder avisar por WhatsApp y mail**. No quiere ser el servidor
público. Arquitectura de arranque:
`equipos → Supabase → esta máquina TIRA (solo salientes) → avisa + copia local`.
**Cero puertos abiertos, cero certificado, cero dominio, cero IP fija.** Todo Caddy/TLS/
firewall entrante quedó recortado a §9 "para cuando se quiera exponer" (no borrado).

**Decisiones con fundamento escrito**
- **Postgres: segundo cluster con `initdb` sobre el binario de PG 18 del ERP** (no instalar
  PG 16 aparte). Tabla comparativa en §2: lo que se evita es **mantener dos versiones de
  Postgres** en la misma máquina; el precio es que comparten los .exe (un upgrade del ERP
  arrastra, pero es evento planificado). Data dir `D:\Termovigia\pgdata`, puerto **5433**,
  servicio `termovigia-pg` con `pg_ctl register` + `sc.exe failure` (3 reintentos), cuenta
  `NT AUTHORITY\NetworkService`, y **`listen_addresses='localhost'` + `pg_hba` solo
  127.0.0.1/::1 scram-sha-256 desde el minuto cero**.
- **Tres redes independientes contra el error irreversible** (escribir en el cluster del
  ERP): `preflight_windows.ps1` sale **2** si el data dir es / contiene / está contenido en
  el de un servicio existente (lo saca del `ImagePath` `-D "…"`), si la ruta menciona
  ERP / BASE DE DATOS, o si el puerto es 2048/8000/8010/8050/3456; `migrar.ps1` pregunta
  `SHOW data_directory` antes de migrar; `AlmacenPostgres` lo pregunta antes de escribir una
  fila. Probado acá: exit 2 en los dos casos.
- **Servicios: Programador de tareas, NO NSSM ni sc.exe.** `sc.exe create` con un .exe común
  muere con error 1053 (no es service-aware); NSSM es una dependencia más que no está. Se
  sigue el patrón `ERP_Watchdog_8000` que Matías ya mantiene: `TV_Notificador` (al inicio),
  `TV_Watchdog` (cada 5 min, **verifica 15 s después de arrancar**), `TV_Backup` (3:30).
  Solo toca tareas `TV_*`.
- **PostgREST SÍ tiene binario Windows** (verificado contra la API de releases): se fija
  **v12.2.3**, la misma versión que el compose →
  `https://github.com/PostgREST/postgrest/releases/download/v12.2.3/postgrest-v12.2.3-windows-x64.zip`
  (ojo: el asset cambió de nombre — hasta v14 `-windows-x64`, desde v16 `-windows-x86-64`;
  la última es v16.2). Se configura **solo por `PGRST_*`** (la doc dice que arranca sin
  archivo de configuración) → ninguna contraseña de la base en disco. No hizo falta
  alternativa; si no la hubiera, el trabajo extra sería exponer los GET del portal en el api
  propio (≈6-8 h).

**El notificador (`servidor\notificador\`, lo que ahora importa)**
- `origen.py` tira de Supabase por PostgREST con `urllib` (cero dependencias nuevas).
  **Marca de agua con solape de 120 s**: cubre la fila insertada con `created_at` anterior a
  nuestro corte (reloj atrasado / commit tardío) que un `>` estricto se comería. Repetir es
  inofensivo porque el guardado es `ON CONFLICT DO UPDATE`: **idempotente por construcción**.
  La marca **se avanza al final**; si muere en el medio, se rehace el tramo.
- `almacen.py` guarda **`espejo.filas(tabla, clave, orden, datos JSONB)`** en vez de tablas
  espejo columna a columna. Motivo: el esquema de la nube cambia (el firmware ya manda 7
  columnas que no estaban en el repo) y una copia con 40 columnas se rompería justo cuando
  más se la necesita. Además `marcas`, `estado`, `entregas`, `descartes`, `vueltas`.
- `reglas.py` (lógica pura): **silencio 30 min por (equipo, tipo)** —con excepción: una
  alerta **más grave atraviesa** el silencio, que "puerta abierta" no tape "temperatura
  crítica"—, **agrupación 120 s** en un solo mensaje, y **techo 6/hora por equipo** con
  **un** aviso de contención. Se registra también **por qué NO salió** cada aviso
  (`espejo.descartes`).
- Canales con una sola interfaz y los reintentos en la clase base: `telegram.py`,
  `correo.py` (SMTP; gotcha de la contraseña de aplicación de Gmail documentado),
  `whatsapp.py` (POST HTTP genérico configurable). **Un canal se apaga vaciando su variable
  del `.env`**, y hay test que lo fija. Si ningún canal entregó, **no se marca como avisado**
  → se reintenta ("no salió" ≠ "se perdió").
- `latido.py`: healthchecks.io (Hobbyist gratis). **El ping de éxito va DESPUÉS de una
  vuelta buena**, nunca al principio: si no, un proceso que arranca y falla siempre seguiría
  reportando "vivo".
- `probar_canales.py`: un mensaje real por canal, distinguiendo "no configurado" / "falló
  con este error" / "el servidor lo aceptó — andá a mirar que haya llegado".

**HALLAZGOS**
- **`delivered_via` NO existe** en `supabase/SETUP_COMPLETO.sql`: hay `telegram_sent`,
  `sms_sent`, `push_sent` booleanos. El registro fino de por qué canal salió cada aviso vive
  en `espejo.entregas`; opcionalmente se marca el booleano en la nube
  (`NOTI_MARCAR_EN_NUBE`). Agregar `delivered_via` = migración nueva cuando se quiera.
- **`core.autocrlf=true`** en el repo: un clon en Windows tiene los `.sql` con CRLF, y
  `api/base.py` hashea el texto **normalizado** (Python abre en modo texto). `migrar.ps1`
  replica esa normalización (`Get-Sha256Migracion`); sin eso, migrar por psql y después
  arrancar el api daría "la migración cambió después de aplicada".
- **Riesgo WhatsApp, con datos** (WebSearch 2026-09-02): automatizar una línea personal
  (whatsapp-web.js / Baileys) viola los ToS y Meta banea; el detector 2026 suma el
  **contador de mensajes sin respuesta**, que es el perfil exacto de un aviso de
  temperatura; ~68 % de los negocios con herramientas no oficiales reportan al menos un
  bloqueo en 12 meses. **Ese número está publicado en el sitio y en el folleto.** Oficial =
  WhatsApp Business Cloud API con plantillas **utility**: Argentina ≈ **USD 0,0120 por
  conversación de 24 h** (marketing 0,0618, auth 0,0220) y **desde el 1-oct-2026 Meta cobra
  por mensaje**, no por ventana. **Recomendación: Telegram + mail como columna vertebral,
  WhatsApp como extra apagable**, y API oficial cuando haya abonos que la paguen. Escrito en
  `WINDOWS_NATIVO.md` §4.5.
- **Contrato de OpenClaw (:3456) sigue SIN CONFIRMAR**: los 7 puntos a preguntar están en el
  encabezado de `notificador/canales/whatsapp.py`, incluido el más traicionero — **cómo se
  entera uno de que la sesión de WhatsApp se cayó**, porque estos servicios contestan 200 y
  no mandan nada durante días (el adaptador ya trata un 200 con `"error"` en el cuerpo como
  fallo).

**Recomendaciones sobre la máquina del ERP (§11 del documento)**
- `listen_addresses='*'` en el Postgres del ERP → pasar a `'localhost'`. **Hoy no hay
  exposición real** (pg_hba solo loopback + sin regla de firewall para el 2048): es una capa
  de defensa caída. **Requiere reiniciar el servicio** = segundos de corte para los 13
  locales → ventana planificada. **Higiene, no urgencia.** Termovigía no lo toca.
- **Router: borrar las redirecciones de 9000 y 9050**, que apuntan a esa máquina donde no
  escucha nada. Hoy inofensivas; el día que cualquier proceso levante algo en 9000 queda
  publicado en internet sin que nadie lo decida. No requiere ventana ni reinicio.

**Evidencia (en ESTA máquina, que es Windows pero NO tiene el ERP; todo read-only salvo
archivos propios)**: los **13 `.ps1` pasan el parser de PowerShell**;
`preflight_windows.ps1` corrido de punta a punta (detecta correctamente que acá faltan PG y
Caddy, y **aborta con exit 2** tanto con `TV_PGDATA` apuntando al ERP como con
`TV_PG_PUERTO=2048`); `watchdog.ps1` y `copiar.ps1` ejercitados en sus caminos de falla con
`TV_RAIZ` desviado al scratchpad (no se tocó nada de esta PC). **109 tests en verde**: 32
nuevos del notificador (`python -m unittest discover -s notificador/tests -t .`) — que no
duplique, que no pierda si estuvo apagado, que el solape se aplique, que el aviso no se
marque si ningún canal entregó, que un canal caído no impida el otro, que un mensaje
multilínea con comillas no rompa el JSON de WhatsApp — más los 77 de `api/tests`, que
siguen pasando. **No hay Postgres ni Caddy acá**: `crear_cluster.ps1`, `migrar.ps1`,
`instalar_postgrest.ps1`, `restaurar_prueba_nativo.ps1` y `tests.ps1 -ConBase` **no se
corrieron contra una base**.

**Para @verificador, en la máquina destino**: `preflight_windows.ps1` (esperar 0) →
`crear_cluster.ps1` → `migrar.ps1` → **`tests.ps1 -ConBase`** (los 25 de aislamiento entre
clientes son el punto que más importa) → `probar_canales.py` → `servicio.py --una` →
`restaurar_prueba_nativo.ps1`. Nada se declara producción antes de eso.

**Archivos**: `servidor\WINDOWS_NATIVO.md` (nuevo); `servidor\windows\` (13 .ps1 nuevos:
config, preflight_windows, crear_cluster, instalar_api, instalar_postgrest, migrar,
arrancar_notificador, watchdog, instalar_tareas, copiar, restaurar_prueba_nativo, firewall,
tests); `servidor\notificador\` (nuevo: ajustes, origen, almacen, reglas, latido, servicio,
probar_canales, canales/{base,telegram,correo,whatsapp}, tests/{reglas,canales,vuelta});
`servidor\caddy\Caddyfile.windows` (nuevo); tocados `servidor\.env.example` (sección
`NOTI_*`) y `servidor\LEEME.md` (índice de las dos arquitecturas y las dos rutas + nota en
§1).

## 2026-09-02 (c) — TERMOVIGÍA: PRIMER DESPLIEGUE REAL contra una base (Neon)
Hasta hoy todo `servidor/` se había verificado con lógica pura porque **no había
base**. Ahora sí: proyecto Neon `Termovigia` (`rough-sunset-46764733`,
`aws-sa-east-1`, plan gratuito, **PostgreSQL 18.6**). Documento nuevo:
`C:\Proyectos\frioseguro\servidor\NEON.md`. Nada de secretos commiteado: el DSN
sale de `neon connection-string` y vive en `servidor\.env` (gitignoreado).

**LO QUE SE HIZO (todo verificado, no declarado)**
- **8 migraciones aplicadas en orden** (000→070) con el corredor de siempre
  (`api/base.py`, mismo camino que Docker y Windows nativo — no se escribió un
  segundo corredor). **29 tablas** en `public`, las 28 de negocio con RLS **y**
  policy; 3 en `auth`; 3 vistas. Sin `psql` en la máquina: venv + `psycopg[binary]`.
- **25/25 tests de aislamiento entre clientes en verde** contra Neon
  (`api/tests_base/`, 47 s). Incluye el `test_00` que prueba que `SET ROLE`
  actúa de verdad — sin eso los otros 24 pasarían en falso.
- **Aislamiento probado también por HTTP**, con la api levantada contra Neon:
  José ve sus 2 cámaras, Ana la suya; José pidiendo el historial de la cámara de
  Ana → **404**; auditor haciendo PATCH de umbrales → **403**; sin token y con
  token basura → **401**. Login completo: 401 con clave mala, 200 + JWT con la
  buena, `/yo` devuelve identidad + organización + permisos.
- **Datos de demo**: 2 clientes (carnicería con 2 cámaras / pescadería con 1),
  1 equipo cada uno **con credencial bcrypt propia**, 97 lecturas de 24 h cada
  uno, alerta resuelta y evento de descarche. 4 personas (2 owners, 1 auditor de
  bromatología, 1 admin). Script nuevo `herramientas/datos_demo.py`.

**TRES BUGS QUE SOLO PODÍA ENCONTRAR UNA BASE DE VERDAD**
1. **`060_tareas_periodicas.sql` NO aplicaba**: `WITH viejos AS (SELECT … LIMIT n
   UNION ALL SELECT … LIMIT n)` es SQL inválido (`syntax error at or near
   "UNION"`; el LIMIT se lee como límite de la UNION entera). **Esa migración no
   habría entrado en ninguna base, nunca.** Corregida con paréntesis por rama.
   No viola append-only: no estaba aplicada ni registrada en ningún lado. Las
   000-050 ya habían quedado aplicadas, así que la base nunca estuvo a medias.
2. **El sembrado de los tests chocaba con el trigger de fan-out**: el `INSERT` en
   `readings` dispara `repartir_lectura_por_sonda()`, que ya escribe
   `probe_readings` con `ts = created_at`; dentro de una transacción `NOW()` es
   siempre el mismo instante → el insert manual siguiente violaba la PK
   `(probe_id, ts)`. 10 de los 25 tests morían en `setUp`. Ahora el test
   **verifica el fan-out** en vez de duplicarlo.
3. **Agujero de seguridad en `api/principal.py`**: la contraseña del rol
   `authenticator` caía por defecto a **la del dueño sacada del DSN**. En Docker
   es inofensivo; en Neon, con endpoint público, le regalaba credencial de login
   a un rol que puede `SET ROLE service_role` (BYPASSRLS). Ahora solo se pone si
   viene `POSTGRES_PASSWORD` explícita. Además `ALTER ROLE authenticator NOLOGIN`
   en Neon: los 4 roles quedaron sin login y sin contraseña.

**LO QUE NEON NO BANCA (dicho, no tapado)**
- **`pg_cron` figura en el catálogo pero es inservible**: sólo se puede crear en
  la base `postgres` y nuestros datos están en `neondb`. Cero cambios: `060` ya
  había decidido planificar desde `api/tareas.py`. Verificado corriendo:
  `hourly_stats: 12 filas` + retención, solas, al arrancar.
- **Sin superusuario**, pero `neondb_owner` es miembro de `neon_superuser`
  (CREATEROLE + BYPASSRLS) → `CREATE ROLE … BYPASSRLS`, `pgcrypto`, `citext`,
  `SECURITY DEFINER` y `SET ROLE` funcionan todos. Nada de `ALTER SYSTEM` ni
  `shared_preload_libraries`, que no se usan.
- **PG 18.6 y no 16**: las 8 migraciones aplicaron sin un cambio (bcrypt de
  pgcrypto incluido). Deuda anotada: `docker-compose.yml` fija `postgres:16` →
  un `pg_dump` de Neon no restauraría ahí.
- **Sin PostgREST** en esta ruta: el firmware tendría que entrar por
  `POST /ingest`, no por `/rest/v1`. **Neon reemplaza el contenedor de Postgres,
  no el stack**: api, PostgREST y Caddy siguen necesitando un host.
- `LISTEN/NOTIFY` **sí** funciona en el endpoint directo (sirve para el SSE que
  falta), pero mantener esa conexión abierta es justo lo que impide que la base
  se suspenda (ver abajo).

**LÍMITES DEL PLAN GRATUITO, CON NÚMEROS MEDIDOS** (`NEON.md` §7)
Medido sobre la base real: `readings` 155,8 B de columnas (~300 B/fila con
cabeceras e índices), `probe_readings` 79,0 B (~200 B/fila). Esquema + demo =
10,9 MB. Techo duro **512 MiB por rama** (`branch_logical_size_limit_bytes`),
PITR **6 h**, 10 ramas, 5 GB de transferencia.
- **5 equipos cada 60 s = ~5,1 MB/día ≈ 155 MB/mes → ≈ 98 días (3 meses) hasta
  chocar.** Con 1 sonda por equipo, ~4,5 meses.
- **La retención por defecto NO entra**: en régimen, 90 días de `readings`
  (194 MB) + **400 días de `probe_readings` (1 152 MB)** = 1,35 GB = 2,6× el
  límite. Con 30/90 días queda en ~335 MB (68 %) y es sostenible; los 13 meses
  de HACCP los cubre `hourly_stats` (~11 MB/año), que no se borra.
- **El límite que muerde ANTES es el cómputo**: mínimo 0,25 CU y la base se
  suspende sola, pero el pool (`min_size=2`) + `tareas.py` cada 60 s la
  mantienen despierta 24/7 → 0,25 × 730 h = **182,5 CU-h/mes** contra los ~100
  (o 50, según la revisión de precios de ago-2026 — **confirmar en la consola**)
  del plan gratuito: la bolsa se agota en **~2 semanas**. Gratis alcanza para
  demo/desarrollo (api levantada a demanda); producción 24/7 = **Neon Launch
  USD 19/mes** (10 GB + PITR 7 días). Contra `COSTOS.md`: sigue ganando Supabase
  Pro (USD 25) para producción porque trae Auth/Storage/Realtime/Edge; Neon gana
  como demo/staging gratis y como plan B con datos propios.

**Gotcha que costó una corrida**: el DSN de Neon trae un `&`
(`channel_binding`). Sin comillas en el `.env`, un `set -a; . .env` lo corta ahí
y el proceso se queda en "esperando la base (1/30)…" sin decir por qué.
Documentado en `.env.example` y en `NEON.md` §1.

**Restauración**: `neon branches create` antes de tocar nada (copy-on-write,
instantáneo, gratis) = el reemplazo directo de "probar la migración contra una
copia" que pide la doctrina; `neon branches restore production ^self@<ts>` para
PITR de 6 h. **Falta y no se hizo**: `pg_dump` fuera de Neon — no hay
herramientas cliente de PG 18 en esta máquina, y **un backup que no se restauró
es un archivo**.

**Archivos**: `servidor/NEON.md` (nuevo), `servidor/herramientas/datos_demo.py`
(nuevo); tocados `servidor/sql/060_tareas_periodicas.sql` (fix del UNION),
`servidor/api/principal.py` (contraseña de `authenticator`),
`servidor/api/tests_base/test_aislamiento.py` (fan-out),
`servidor/herramientas/crear_usuario.py` (lee `TV_DSN` del `.env`),
`servidor/LEEME.md` (tres rutas), `servidor/.env.example` (sección Neon),
`QUE_FALTA.md` (ítems 3 y 12).
**Para @verificador**: `TV_DSN_TEST=<neon> python -m unittest discover -s
api/tests_base -t api -v` (esperar 25 OK) + los pasos de `API_PORTAL.md` §8.
Nada es producción hasta eso y hasta que se decida dónde vive el dato real.
