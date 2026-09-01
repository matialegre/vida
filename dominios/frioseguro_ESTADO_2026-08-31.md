# FrioSeguro — ESTADO al 2026-08-31 (reconstrucción de @comercial para el Director)

> Fuentes: `diario/nocturno-local-2026-08-23..29.md`, `dominios/{firmware,frontend,hardware,comercial}.md`, `PORTFOLIO.md` §P1, `PLATA.md` L1, `C:\Proyectos\frioseguro` (git log, `QUE_FALTA.md`, `REVIVAL_2026-08.md`, `entrega_scz/docs/*`, `kit_santacruz/`), `git stash@{0}` de MATI-HQ (`SESION_1_FRIOSEGURO_SANTACRUZ.md`, sin commitear).

## 0. La "actualización grande de hace 4-5 días" (lo que Matías recuerda como "dos puntos MDI")
Casi seguro es **"2.6"**: la familia de firmware **`firmware_revival` v2.6.x** del reefer de Santa Cruz. Entre el 19 y el 27-ago pasó esto (todo en el working tree de `C:\Proyectos\frioseguro`, **sin commitear**):
- **19-ago**: kit `FRIOSEGURO_SANTACRUZ_KIT_v260.zip` + `kit_santacruz/` (runbook, `flashear.py` con backup obligatorio, guardián de red de la notebook, APK LOCAL v18) + `supabase/BOOTSTRAP_2026-08-19.sql` (**esquema de verdad del proyecto Supabase `vihxmqjjprtlzajlatvu`, vive solo en este disco**). El módulo viajó al sur y se enchufó el 21.
- **25-26-ago**: `panel-web/` (Vercel, "FrioSeguro — REEFER_01_SCZ"), `apk-panel/` (com.frioseguro.panel 1.0), `supabase/migration_device_logs.sql`.
- **26-ago — el documento grande**: `entrega_scz/docs/ESTADO_HONESTO.md` + `AUDITORIA_HALLAZGOS.md` + `SESION_2026-08-26_TELEGRAM_Y_COLUMNAS.md`. Revisión adversarial de 5 agentes sobre el equipo corriendo **2.6.21** en Cerro Moro. Veredicto: "prototipo que funciona de punta a punta, NO apto para venderse a una minera hasta endurecerlo". Sólido: elección de red abierta con internet real (128 ciclos), rollback OTA, comandos por nube, primera alerta real E2E (Telegram HTTP 200 auditado en `device_logs`). Crítico: anon key = llave maestra de escritura (sin RLS, sin multitenant), sin buffer offline, sin monitor de "equipo mudo", OTA vía CDN de Supabase que no propaga (cache pinneada 3h52+), ~40 bugs de firmware listados.
- **27-ago 22:31**: `git stash` "Teleport auto-stash" en MATI-HQ con `SESION_1_FRIOSEGURO_SANTACRUZ.md` (instructivo de puesta en marcha remota) — **está en stash, no en main**.

## 1. Qué hay construido y probado — DOS familias, dos Supabase
| Capa | Línea COMERCIOS (la que se vende por abono) | Línea SANTA CRUZ (reefer minero) |
|---|---|---|
| Firmware | `firmware_modular/` v3.0.x (ESP32, WiFi). Módulos en main: sondas DS18B20, `door_sensors.h` (hasta 3 reed), `alerts.h`, Telegram, Supabase, web UI embebida, `web_api.h`. **`power_monitor.h` y `current_sensor.h` existen pero NO están incluidos** (R5 pendiente, es de banco). Compila (65% flash con `min_spiffs`). | `firmware_revival/` **2.6.21 en campo**: redes abiertas + testigo dual, OTA desde Supabase Storage con SHA-256 y rollback, sondas por ROM en caliente + calibración, log remoto, cola de comandos. |
| Cloud | Supabase `cjdluhemschrynijzvap` (schema en `supabase/*.sql`; funciones `cron-device-alerts`, `send-push`, `cron-cleanup-*`, `create-user`, suscripciones/pagos). | Supabase `vihxmqjjprtlzajlatvu` (`BOOTSTRAP_2026-08-19.sql`). Free tier: **se pausa por inactividad**. |
| Front | `web-dashboard/` React+Vite en Netlify (dashboard cliente + panel admin) + `frioseguro-android/` (com.frioseguro.app, cambios sin commitear). | `panel-web/` (Vercel) + `apk-panel/` + APK LOCAL v18 (AlertaRift, directo al ESP32). |
| Hardware | 5 PCBs (3 WiFi + 2 SIM800 — **SIM800 descartado 2026-07-11**, van como WiFi), 20 DS18B20, 10 reed, ~10 módulos relé, 3 cajas IP65 + prensacables (`hardware.md`). | 1 ESP32 en zócalo + gabinete + relé sirena; **sin sondas conectadas todavía** (mide ambiente). |
| OTA | ArduinoOTA/LAN en código; **nunca probado en hardware** (`QUE_FALTA` #8). | **Probado** (rollback verificado al reloj), pero por aire de noche entró 1 de 4 intentos; las últimas versiones se flashearon por cable. |
| Probado E2E | Piloto casero en la heladera de Matías (jul). Ningún comercio instalado. | Sí: lecturas, comando `ALERTA_TEST`, Telegram, OTA. |

## 2. Branches nocturnos sin mergear (frioseguro: **24**, todos salen de `main`, ninguno colisiona)
Los que importan para vender (todos con tests offline, ninguno flasheado): `08-23-el-que-se-apaga-no-avisa` (**el freezer sin luz no avisaba** → vigía de silencio en nube), `08-26-el-hueco-y-el-reloj` (buffer offline 3 h + hora en las lecturas), `08-27-el-testigo-que-certificaba` (portal cautivo/ISP caído se veía como internet), `08-27-b-columnas-fantasma` (PostgREST rechazaba la fila entera), `08-29-la-sonda-que-se-cae` (aviso de sonda caída se perdía sin internet), `08-18-fix-alert-delay-defrost`, `08-21-b uptime`, `08-19-b frescura`, `07-11-b` + `07-13 resumen mensual` (**MERGE-CON-FIXES ya aplicados**, falta migración + deploy), `07-23-b retención`, `08-09 aislamiento-tenant`, `07-26-b provisión`. Lista completa: `git branch` en el repo y `COLA_MERGE_NOCTURNOS.md` (HQ).

## 3. Qué falta para VENDER/INSTALAR el primer abono (de `QUE_FALTA.md` + hallazgos de agosto)
1. **Mergear la cola** (con @verificador) y **flashear una placa WiFi** con `firmware_modular` + `OTA_PASSWORD` real + rotación de claves (`SECURITY_AUDIT.md`: 14 secretos) — QUE_FALTA #1/#4/#8.
2. **Banco (4 escenarios del 08-29 + R5 power_monitor)**: sonda desenchufada, router apagado, arranque sin sonda, corte de luz.
3. **Legal/comercial**: nombre de marca (OJO: "Frío Seguro Monitoreo del Frío S.R.L." existe, CUIT 30-71874481-0 — `PORTFOLIO.md` L70), monotributo, contrato validado (`comercial/CONTRATO_BORRADOR.md`), link de cobro.
4. **Deploy del resumen mensual** (migración + `functions deploy cron-monthly-summary`).
5. Aplicar a la línea comercial las lecciones de Santa Cruz: RLS real (anon solo lectura), backend con credencial por equipo, manifiesto OTA inmutable.

## 4. Precios y modelo ya definidos (fuente: `MATI-HQ/comercial/PRECIOS_FRIOSEGURO.md` 2026-07-07, escenario RECOMENDADO elegido en §3; Matías no confirmó todavía)
- **Instalación $70.000** (una vez, por local) · **abono $45.000/mes** 1er punto de frío · **$25.000** cada punto adicional. Premium (farmacia/regulatorio): $120.000 / $70.000 / $40.000 con SLA 24 h, sirena, puerta, informe mensual firmado.
- Hardware en **comodato**, cobro mes adelantado del 1 al 10, **ajuste trimestral IPC**, upsell sirena/puerta +$10-15k/mes. Piloto gratis: UNO, 30 días, precio pactado antes (`PLATA.md` L20-24). Costo BOM/kit: $30-45k (`PRECIOS` §2); en USD: `docs/LISTA_MATERIALES.md` (~USD 30/emisor).
- Material listo: `PITCH.md`, `guion_visita.md`, `hoja_mostrador*.html` (marca en placeholder `[NOMBRE]`), `plantillas_whatsapp.md`, `CONTRATO_BORRADOR.md`.

## 5. Leads y pipeline (`dominios/comercial.md`)
- **FrioSeguro: pipeline VACÍO hasta hoy.** Metas de PLATA (1 abono cobrado al 18-ago, 3-5 antes de octubre) **no cumplidas** — ninguna visita a comercio registrada; agosto se fue en Santa Cruz (minera, línea 17 de QUE_FALTA) y en EMSICA/marketing técnico (línea 2, 60 prospectos, EMSICA cliente activo).
- **Nuevo 2026-08-31: lead Venado Tuerto** (cámaras frías con exigencia de registro, 600 km) → propuesta en `C:\Proyectos\frioseguro\comercial\venado-tuerto\`.
- Panamerican Cerro Moro: instalación real en curso (1 reefer, 2.6.21), sin contrato ni cobro definido — **es referencia de venta ("desarrollado para / instalado en"), no un abono todavía**.

## 6. Riesgos que el Director tiene que ver
- **Trabajo de día sin commitear hace 10+ noches** en `frioseguro` (revival, kit, panel-web, apk-panel, BOOTSTRAP SQL, 2 zips de 7 MB) y **SESION_1 en un stash**. Un disco roto pierde el esquema de Santa Cruz.
- Dos firmwares que deciden distinto la misma cosa (drift `revival` <-> `modular`); los nocturnos vienen portando fixes de uno al otro.
- Secretos en binarios públicos y en `%TEMP%` (service_role, PAT) — `AUDITORIA_HALLAZGOS.md` CRÍTICO-4.
