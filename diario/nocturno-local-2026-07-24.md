# Nocturno LOCAL — 2026-07-24 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
El scanner de secretos de FrioSeguro (el que corre antes de vender, hueco #6) **tenía
un agujero justo en el formato de clave que Supabase usa AHORA**. Solo cazaba el
esquema viejo (JWT `anon`/`service_role` y `sbp_`); ignoraba por completo el par nuevo
`sb_secret_`/`sb_publishable_` — el que quedó horneado cuando bootstrapeaste el proyecto
nuevo el 13/07. Resultado: **3 claves `sb_secret_` (equivalen a service_role, bypass
total de RLS) estaban commiteadas y el scanner las daba por limpias.** Lo arreglé:
+2 patrones, +6 tests (**19/19 OK**), y corriéndolo ahora **aparecen las 3 críticas +
7 publishable**. No roté ni borré ninguna clave (eso es del día). Branch:
**`nocturno/local-2026-07-24-scan-secrets-sbkeys` (frioseguro), pendiente de merge.**

## Tarea elegida y por qué
**FrioSeguro — ampliar `tools/scan_secrets.py` al esquema nuevo de keys de Supabase.**
Razones:
- **Es PLATA** (categoría 1 de la jerarquía) y **seguridad antes de vender** = hueco #6
  del PORTFOLIO, el que bloquea el primer abono cobrado. Un scanner que dice "limpio"
  cuando hay una `service_role`-equivalente commiteada es peor que no tener scanner:
  da falsa tranquilidad.
- **Estaba teed-up por el turno anterior**: el nocturno 23/07-b lo detectó como
  observación ("punto ciego justo en el formato de key que Supabase usa ahora") y
  deliberadamente **no lo mezcló** con su branch de retención → quedó como tarea limpia,
  fresca y sin branch previo.
- **Software 100% puro** — stdlib de Python, sin red, sin hardware, sin cloud, sin
  descargas → cero riesgo de timeout (disciplina 07-07). No toca migraciones, ni
  firmware, ni la nube, ni rota/borra una sola clave.
- No apilo donde ya hay pila crítica: no toqué galgas (11 branches) ni el branch de
  retención de anoche. Este es el 7º branch nocturno de frioseguro, pero es el único
  camino para cerrar el agujero que el propio scanner dejaba abierto.

## Qué hice — branch `nocturno/local-2026-07-24-scan-secrets-sbkeys` (frioseguro)
Sale de `main` (commit `ef...` de origin/main, "Already up to date"). **3 archivos,
89 inserciones / 3 borradas.**

1. `tools/scan_secrets.py` — **+2 patrones** en `PATTERNS`:
   - `supabase_secret_key` → `sb_secret_[A-Za-z0-9_-]{16,}` → **CRITICAL** (reemplaza el
     JWT `service_role` desde la migración de keys 2025 de Supabase: bypass total de RLS).
   - `supabase_publishable_key` → `sb_publishable_[A-Za-z0-9_-]{16,}` → **INFO** (reemplaza
     el JWT `anon`: pública por diseño, la protege RLS — mismo trato que la anon key).
   - Decisión de diseño anotada en el código: **sin `\b` inicial a propósito**, para cazar
     también la copia corrupta `'Tsb_secret_...'` de `SETUP_COMPLETO.sql:933`.
   - Docstring actualizado (lista "Qué busca" + nota de que cubre AMBOS esquemas).
2. `tools/test_scan_secrets.py` — **+6 checks** (fixtures sintéticos armados en runtime,
   sin ningún secreto real en el fuente, igual que los existentes): `sb_secret_`→critical
   y falla con `--fail-on high`; copia corrupta `Tsb_secret_` igual se caza;
   `sb_publishable_`→info y **NO** falla con `--fail-on high`; y un negativo importante:
   la **mención en comentario** `"sb_secret_..."` (con puntos, sin clave real) **no**
   produce match. **13 → 19 checks, OK.**
3. `SECURITY_AUDIT.md` — addendum fechado 2026-07-24 (el audit original es de la era JWT):
   tabla de las 3 `sb_secret_` críticas nuevas + las 7 `sb_publishable_` INFO, y **paso 2b
   del runbook de rotación** (revocar/crear secret key nueva SOLO si pertenece al proyecto
   vivo). Nota de reproducción actualizada (34→44 coincidencias, 14→17 al nivel de fallo).
4. `QUE_FALTA.md` #4 → sub-bullet EN BRANCH con el detalle.

### El hallazgo (con evidencia real, no sintético)
Corriendo `python tools/scan_secrets.py` sobre el repo **con el fix**, aparecen claves que
**antes del fix eran invisibles**:

| Severidad | Regla | Archivo:línea |
|---|---|---|
| 🔴 CRITICAL | `supabase_secret_key` | `supabase/SETUP_COMPLETO.sql:901` (trigger `notify_alert_push`) |
| 🔴 CRITICAL | `supabase_secret_key` | `supabase/SETUP_COMPLETO.sql:933` (copia corrupta `'Tsb_secret_…'`) |
| 🔴 CRITICAL | `supabase_secret_key` | `tests/create_clients_sql.js:16` (`MGMT_TOKEN`) |
| 🟢 INFO | `supabase_publishable_key` | 7 archivos (`DISPOSITIVOS.md`, `GUIA_INSTALACION.md`, `desktop-viewer/app.py`, `docs/FRIOSEGURO_MEGAPROMPT.md` ×2, `firmware_modular/config_SANTA_CRUZ.h`, `supabase/test_supabase.py`) |

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-07-24-scan-secrets-sbkeys
python tools\test_scan_secrets.py        # -> "OK: 19 checks pasaron, 0 fallaron."
python tools\scan_secrets.py --json | more   # ver las 3 sb_secret_ CRITICAL nuevas
git diff main --stat                      # -> 3 archivos, 89+/3-
# Prueba de que ANTES no las cazaba (baseline):
git stash; git checkout main
python tools\scan_secrets.py . 2>$null | Select-String "sb_secret"   # -> sin resultados
git checkout nocturno/local-2026-07-24-scan-secrets-sbkeys
```
**Resultado de esta noche:** 19/19 tests OK; el scanner real caza 3 críticas + 7 info que
en `main` pasaban desapercibidas.

## Qué quedó SIN verificar / para el día (Matías — cloud + decisión, fuera de mi alcance)
1. **Confirmar a qué proyecto pertenecen las 3 claves `sb_secret_`**: ¿al vivo
   `cjdluhemschrynijzvap` o al muerto `nwugnhsktcihusopfldu` (el que borraste el 13/07)?
   - Si son del **vivo** → **rotar YA** (Supabase → Settings → API Keys → Secret keys →
     revoke + create). Runbook paso 2b en `SECURITY_AUDIT.md`.
   - Si son del **muerto** → borrarlas igual del working tree para no re-exponerlas ni
     confundir (no rotar, ya están muertas).
2. Verificar **RLS activo** en todas las tablas — con RLS, las 7 `sb_publishable_` son
   inofensivas (públicas por diseño); sin RLS, se vuelven críticas. Es el mismo chequeo
   pendiente que la anon key del audit del 10/07.
3. **Sugerido:** sumar `python tools/scan_secrets.py` como pre-commit hook (ya sugerido en
   `SECURITY_AUDIT.md`) — ahora que cubre el esquema nuevo, vale más.

## Observaciones para el día (no tareas mías)
- El scanner sigue corriendo solo sobre **archivos trackeados por git** (default correcto).
  Estas claves ya están en el repo y en la historia; el fix las **detecta**, no las purga.
- `frioseguro` quedó con **7 branches nocturnos sin mergear** (07-11-b, 07-13, 07-14,
  07-18, 07-20, 07-23-b + este). Igual que galgas (11): **el cuello de botella del
  portfolio ya no es producir trabajo de noche, es drenarlo de día con @verificador.**
  Este branch es chico (89 líneas, 3 archivos, tests verdes) → candidato fácil para
  arrancar la sesión de drenaje.

## Reglas respetadas
Solo software (Python stdlib) + docs. **Nada rotado, nada borrado, nada deployado**,
ninguna migración, `data/field_captures` de galgas ni tocado, sin compilaciones ni
descargas. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-24-scan-secrets-sbkeys` (frioseguro, pusheado a origin; sale de
`main`).

## Notas para @verificador
- DoD = *"el scanner ahora detecta el esquema nuevo de keys de Supabase con la severidad
  correcta, sin falsos positivos en menciones de documentación, y sin regresión de los
  patrones viejos"*.
- Ataques sugeridos: (a) correr los 19 tests + agregar casos raros (clave con `-` al final,
  clave de 15 chars que NO debería matchear, `sb_secret_` en un `.example` ignorado);
  (b) confirmar que `sb_publishable_` sigue en INFO y **no** hace fallar `--fail-on high`
  (si lo hiciera, rompería CI por claves públicas — falso alarma); (c) verificar que el
  fix **no** cambió el conteo de los patrones viejos (JWT/`sbp_`/telegram) corriendo el
  scanner en `main` vs el branch y diffeando; (d) atacar el regex `{16,}` — ¿entra basura
  que no sea una key? (es tolerable en un scanner: mejor un falso positivo suprimible con
  `scan-secrets: allow` que un falso negativo en una service_role).
