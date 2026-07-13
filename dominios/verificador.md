# Dominio: verificador (agente @verificador)

Bitacora del evaluador independiente. Generator != evaluator: aca van los veredictos con evidencia observable. Definicion: ~/.claude/agents/verificador.md (backup en ../agentes/verificador.md).

## Bitacora

- 2026-07-13 [AUDITORIA 3 branches nocturnos FrioSeguro pre-merge a main] — repo C:\Proyectos\frioseguro. Entorno: Python 3.14.3, Node v24.14.0, deno AUSENTE, supabase CLI 2.90.0 (no toque nube). Volvi a main limpio, no mergee, no toque origin.

  ### Branch 1 `nocturno/local-2026-07-10-b-secret-scan` → VEREDICTO: MERGE-OK
  Evidencia:
  - `py_compile` scan_secrets.py + test → OK.
  - `python tools/test_scan_secrets.py` → **"OK: 13 checks pasaron, 0 fallaron"**, exit 0.
  - Corrida sobre el repo REAL: el nocturno declaro "34 coincidencias, 14 al nivel de fallo (>= high)". **Reproduce EXACTO**: 11 critical + 3 high + 20 info = 34 total, 14 failing, exit 1.
  - Cold-start OK: solo stdlib + `git ls-files`, corre `python tools/scan_secrets.py .` sin setup.
  - El scanner FUNCIONA de verdad: distingue anon(info) de service_role(critical), enmascara, respeta `scan-secrets: allow` e ignora `.example.*`.
  - Deudas menores (NO bloquean el merge de la herramienta): (a) FN latente — token de Telegram inline en URL `.../bot<token>` no se detecta por el `\b\d` (word boundary); el repo hoy usa concatenacion `"bot"+TOKEN` asi que no esta expuesto, pero es fragil. (b) FN latente — bot IDs de Telegram de 11+ digitos no matchean (`\d{8,10}`).
  - **HALLAZGO CRITICO DE DOMINIO (no del branch, del repo)**: el scanner CONFIRMA credenciales reales commiteadas y en la historia de git: `sbp_` management token (llave maestra de la cuenta) en 10 archivos `tests/*.js`, JWT service_role en `tests/recreate_clean.js:4`, token de bot Telegram en `firmware_modular/config.h:94` + `config_SANTA_CRUZ.h:44` + `DISPOSITIVOS.md:150`. SECURITY_AUDIT.md lo documenta honesto. **ROTAR antes del primer cliente pago** (ver RUNBOOK backend paso 5.x). Escala a Director.

  ### Branch 3 `nocturno/local-2026-07-12-lint-device-config` → VEREDICTO: MERGE-OK (1 deuda menor)
  Evidencia:
  - `py_compile` lint_device_config.py + test → OK.
  - `python tools/test_lint_device_config.py` → **"OK: 35 checks"**, exit 0 (coincide con lo declarado por el nocturno).
  - Corrida sobre `firmware_modular/config.h` REAL → detecta correcto OTA_OPEN (ERROR, exit 1), TELEGRAM_HARDCODED (warn), AP_OPEN + SIM_APN (info). `config_SANTA_CRUZ.h` → 0 errores (config bien formada: temps -40/-18/-10 presentes, sin OTA/PLACA definidos → checks de provisioning correctamente omitidos).
  - Cold-start OK: stdlib, `--from-header` / `--json-in` / stdin.
  - Deuda menor: `_coerce()` no parsea literales C comunes `-18.0f` (sufijo f) ni `(-18.0)` (parentesis) → los toma como string → dispara TEMP_PRESENT error. **Falla SEGURA** (bloquea el flasheo, no lo deja pasar), pero daria falso-error si algun config.h usa esos formatos. Los config.h actuales usan `-18.0` sin sufijo → OK hoy. Fix sugerido: strip trailing f/F y parentesis en `_coerce`.

  ### Branch 2 `nocturno/local-2026-07-11-b-resumen-mensual` → VEREDICTO: MERGE-CON-FIXES
  Evidencia (deno ausente, pero Node 24 corre el .test.ts via type-stripping — offline, no toca nube):
  - `node --check` de monthly_summary.ts + index.ts → parse OK.
  - `node --test` → **13 pass / 0 fail** (el doc declara "13 checks / pass 13" → reproduce EXACTO).
  - Logica revisada: `monthWindow` correcto (medianoche AR = 03:00Z; cruce de anio dic→ene ok). index.ts filtra por [from,to) en SQL (la funcion pura confia en el caller, correcto). Columnas/tablas referenciadas EXISTEN en el schema real: `readings.temp_over_critical` (SETUP_COMPLETO.sql:142), `power_events` (195), `door_events` (210), `devices.subscription_status` (95).
  - Migracion `migration_monthly_summaries.sql`: **IDEMPOTENTE** (CREATE TABLE/INDEX IF NOT EXISTS, UNIQUE inline no se duplica en re-run). SETUP_CRON: idempotente (guard `unschedule` antes de re-`schedule`) y coherente (`0 8 1 * *` = 05:00 AR, calcula mes anterior correcto).
  - **FIX 1 (bloqueante para prod) — RLS FALTANTE**: `monthly_summaries` NO tiene `ENABLE ROW LEVEL SECURITY` ni policy. TODAS las demas tablas del schema lo tienen (SETUP_COMPLETO.sql:969-983). Sin RLS + anon key embebida en la app Android → cualquiera con la anon key lee/escribe/borra los resumenes de TODOS los clientes (fuga cross-tenant). Corrobora el hallazgo ya anotado por @backend (backend.md:14, "tarea pendiente"). Fix: append a la migracion `ALTER TABLE monthly_summaries ENABLE ROW LEVEL SECURITY;` + policy por owner consistente con readings/alerts. El cron escribe con service_role (bypassa RLS) → no se rompe.
  - **FIX 2 (riesgo de confianza) — falso "protegida todo el mes" con 0% cobertura**: device sin datos → `verdict.sinPerdidas=true` → texto "0 perdidas: la mercaderia estuvo protegida todo el mes" aunque `coveragePct=0`. El test 187-198 lo consagra como intencional. Enganoso justo en el artefacto de retencion. Fix: si coveragePct < umbral, emitir "datos insuficientes este mes" en vez de afirmar proteccion (monthly_summary.ts:217 + 282-286).
  - DEUDA 3: `temp_over_critical` (ReadingRow, seleccionada en index.ts:85) y `temp_critical` (DeviceInfo) declaradas/traidas pero NUNCA usadas en `buildMonthlySummary`. El veredicto depende 100% de la tabla alerts e ignora el flag que el firmware computa. Data pull muerto + robustez perdida. Considerar usar temp_over_critical como respaldo del veredicto.
  - DEUDA 4: FN latente en veredicto — `severity === "critical"` no captura `"emergency"` (schema_v2.sql:114 lista info/warning/critical/emergency). El firmware HOY solo emite critical/warning (alerts.h:64) → no activo. Si algun dia emite emergency, el veredicto lo pierde. Considerar `["critical","emergency"].includes(sev)`.

  Resumen: **B1 MERGE-OK, B3 MERGE-OK**, ambos con deuda menor no bloqueante. **B2 MERGE-CON-FIXES** (RLS + mensaje de 0% cobertura antes de exponer a un cliente pago). El codigo de B2 compila y sus 13 tests pasan; los fixes son de hardening SQL y de mensaje, no de arquitectura.
