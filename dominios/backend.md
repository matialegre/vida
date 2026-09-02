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
