# Nocturno LOCAL — 2026-07-23 (turno 02:00, worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
El bucket `firmware` de galgas es público **y anon tiene ALL sobre él**: cualquiera con
la anon key (que viaja en cada ESP32 y en la web) puede **reemplazar los binarios que la
flota instala por OTA**. Esta noche construí la salida planificada que nunca se había
hecho (Task 09): la **Edge Function `firmware-check`** — 1 request, decisión de OTA
resuelta en el servidor, **URL firmada con TTL 600 s** — con la lógica pura testeada
offline (**20/20 `node --test` OK**) y un runbook con el orden obligatorio del lockdown.
Branch: **`nocturno/local-2026-07-23-firmware-check-edge` (galgas), pendiente de merge.**
De paso cierra server-side el hallazgo strcmp del 07-20-b (el gate que se cuelga en
0.9→0.10) y cubre la selección per-device A/B (QUE_FALTA #5).

## Tarea elegida y por qué
**galgas #6 (P0 octubre + hueco de seguridad #6 del PORTFOLIO) — bucket firmware con URL
firmada + TTL.** Razones:
- Era el único ítem P0 de software puro **sin branch nocturno previo** que lo cubra
  (galgas ya tiene 9 esperando merge, pero todos son modelos/replays/docs; esto es la
  pieza de backend que la Task 09 dejó planificada y nadie escribió).
- Verifiqué el hueco antes de elegir: `20260426180000_storage_firmware_policies.sql`
  da a anon `for all` sobre el bucket, y `supabase_client.cpp:352` descarga de la URL
  pública. No es "lectura abierta": es **escritura del vector de ejecución de código**.
- datalogger recibió el 07-21, frioseguro tiene 5 branches apilados, cosechador es P2.
- 100 % backend/offline: cero hardware, cero descargas, cero riesgo de timeout.
- Descarté como tarea el crash del scheduler del 21/07: el turno de las 22:00 del 22/07
  corrió completo y cerró bien (lo dice `scripts/turno_noche_log.txt`), así que no hay
  falla reproducible que arreglar esta noche — queda como observación abajo.

## Qué hice — branch `nocturno/local-2026-07-23-firmware-check-edge` (galgas)
Sale de `main`, commit `9ce7bfb`. **5 archivos, 553 inserciones, 0 borrados. No toca
firmware C++, ni migraciones (deliberado, ver runbook), ni data/, ni la nube.**

1. `backend/supabase/functions/firmware-check/logic.ts` — lógica PURA (sin Deno APIs):
   - `validateRequest` con whitelist (el `device_id` se interpola en la query PostgREST
     → bloquea coma/paréntesis/punto = inyección en el `or=()`).
   - `compareVersions` **semver numérico** con regla prerelease — el fix server-side del
     hallazgo del branch 07-20-b (`strcmp` lexicográfico: `0.10.0 < 0.9.9` → flota
     clavada). Sin downgrade silencioso.
   - `selectFirmwareRow` — per-device gana a global, luego `released_at` desc: misma
     semántica que el cliente actual y que el oráculo `tools/ota_decision_model.py`.
   - `decideUpdate` — flujo completo con `reason` trazable en cada salida.
2. `index.ts` — wrapper `Deno.serve` (solo I/O): query `firmware_versions` con
   service_role → decisión pura → firma `POST /storage/v1/object/sign/firmware/<path>`
   con `expiresIn: 600`. Respuestas de error con status y razón.
3. `logic.test.ts` — **20 tests** corridos con Node 24 (type stripping nativo): el caso
   0.9→0.10, prerelease, per-device A no toma la fila de B, sin downgrade, whitelist, etc.
4. `docs/ota-firmware-check.md` — runbook completo: deploy + smoke curl, **ORDEN
   OBLIGATORIO del lockdown** (deploy → migrar firmware A y B → recién ahí cerrar el
   bucket; el SQL del lockdown va EN el doc y NO como migración, para no dejar una
   migración-mina que brickee la OTA si se corre antes de tiempo), y la spec exacta de
   migración del cliente para @firmware (el `signed_url` cabe en el buffer de 512 de
   `types.h:78`; eliminar el gate strcmp local; ojo lección WDT de Sesión 8).
5. `QUE_FALTA.md` #6 → nota EN BRANCH.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-23-firmware-check-edge
node --test backend/supabase/functions/firmware-check/logic.test.ts   # -> 20/20 pass
node -e "import('./backend/supabase/functions/firmware-check/index.ts').catch(e=>console.log(e.message))"
#   -> "Deno is not defined" (parsea bien; solo falta el runtime Deno, esperado)
git diff main --stat   # -> 5 archivos, 553+
```

## Qué quedó SIN verificar (día, con nube — detalle en el runbook)
1. `supabase functions deploy firmware-check` + smoke con curl (anon Bearer) — la
   función nunca corrió contra el proyecto real (no hay deno local y el deploy es
   trabajo de día). Errores posibles a cazar en el smoke: nombre exacto de los env vars
   inyectados y el shape de la respuesta del endpoint de firma.
2. Migración del cliente C++ (`supabaseFirmwareCheckForDevice`) + OTA de A y B — @firmware, banco.
3. El lockdown del bucket (SQL en el doc) — **SOLO después de 1 y 2**, si no se brickea
   la OTA actual.

## Observaciones para el día (no tareas mías)
- El crash del scheduler del 21/07 22:00 **no se repitió** (22/07 22:00 corrió y cerró
  bien; yo soy el turno 02:00 del 23/07 — ahora hay DOS turnos por noche, 22:00 y 02:00:
  ¿es intencional? Si no, sobra uno en el Programador de tareas). El `.bat` sigue sin
  loguear exit code de claude — una línea `echo EXITCODE %ERRORLEVEL%` diagnosticaría el
  próximo crash silencioso.
- Branch huérfano vacío `nocturno/local-2026-07-21-b-readme-drift` en galgas sigue ahí
  (borrarlo es de día, yo no borro).
- Al mergear, `QUE_FALTA.md` de galgas puede dar conflicto trivial con el branch del
  07-22 (notas en ítems distintos, #6 vs #14).

## Reglas respetadas
Solo software backend + docs. Nada borrado, nada deployado, migraciones intactas
(append-only respetado no agregando ninguna peligrosa), `data/field_captures` ni tocado
ni leído. Sin descargas ni compilaciones pesadas. El branch **no se mergea** hasta
@verificador.

## Branch
`nocturno/local-2026-07-23-firmware-check-edge` (galgas, pusheado a origin; sale de
`main`, commit `9ce7bfb`).

## Notas para @verificador / @firmware / @backend / @director
- **@verificador:** DoD = *"la decisión que devuelve la función es exactamente
  per-device>global + semver, y el runbook no permite brickear la flota"*. Ataques
  sugeridos: (a) correr los 20 tests y agregar casos propios raros (`0.1.3` vs
  `0.1.3.1`, versiones no numéricas); (b) cotejar `selectFirmwareRow` contra el oráculo
  del branch 07-20-b fila por fila; (c) buscar en el runbook un orden de pasos que deje
  la flota sin OTA.
- **@backend (día):** deploy + smoke es ~15 min con la CLI linkeada; el doc tiene los curl.
- **@firmware:** la spec del cliente está en el doc — al migrar, actualizar también el
  oráculo `tools/ota_decision_model.py` en el mismo commit.
- **@director:** con este ya son **10 branches nocturnos en galgas** esperando merge —
  la sesión de día con @verificador para drenar la pila ya es urgente en sí misma.
