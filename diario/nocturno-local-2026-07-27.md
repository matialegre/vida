# Nocturno LOCAL — 2026-07-27 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
Las últimas ~10 noches vienen diciendo lo mismo: **el cuello ya no es producir branches, es
drenarlos** (COLA_MERGE = 25 branches sin mergear). Datalogger quedó 100% triado (07-25/-25-b/-26)
y el pipeline de provisioning de FrioSeguro quedó completo (07-26-b). Producir un modelo+tests #28
tendría **valor negativo**. Así que esta noche tomé el **fallback honesto y explícitamente
documentado**: arreglar un **README que miente** — el **item #14 de `galgas/QUE_FALTA.md`**
(*"docs raíz desactualizadas vs act.md, el README miente sobre el estado"*).

El `README.md` de galgas decía **"🟡 Scaffolding creado, esperando contexto de uso real"** y
apuntaba a la ruta vieja `C:\Users\Pandemonium\Documents\GALGAS CON SUPABASE\` + a
`docs/PLAN_v2_DEFINITIVO.md` (que **no existe**). El sistema hace tiempo está **validado E2E en
banco** (A 0.1.3 vía OTA / B 0.1.1 / RX heartbeat-only). Reescrito para reflejar la realidad,
designar **`act.md` como fuente de verdad** (como manda PORTFOLIO), corregir ruta y pointers, y
aclarar que `build/`/`bins_*`/sketches experimentales NO son estructura canónica.
**Branch: `nocturno/local-2026-07-27-readme-drift` (galgas).** Solo docs, cero riesgo.

## Tarea elegida y por qué
**Fix del drift del README raíz de galgas** (item #14 de `QUE_FALTA.md`).
- **Es el fallback explícito del protocolo (paso 5):** "si no hay tarea útil nueva, arreglá drift
  de docs (README que mienten vs código)". No lo inventé — está listado como pendiente con dueño.
- **La tarea correcta dado el estado del sistema.** El propio sistema lleva ~10 noches gritando
  que **el valor nocturno de producir modelos/tests está agotado** (datalogger triado, provisioning
  de FrioSeguro completo; lo que falta en todos es **merge humano o hardware**). Un branch #28 de
  otro oráculo offline sería exactamente el antipatrón que la COLA_MERGE advierte. Un README que
  miente, en cambio, **estorba al merge humano** que es el cuello real: quien haga cold-start
  (Matías, @verificador, un agente) arranca por el README y hoy le dice "esto es scaffolding sin
  empezar" cuando en verdad está a punto para octubre.
- **Prioridad:** galgas es **P0 octubre** (categoría 2). PLATA/UNIVERSIDAD (cat. 1) no tienen tarea
  de software-sin-hardware genuinamente nueva esta noche (FrioSeguro: bloqueantes restantes son
  hardware/humano; UTN está fuera de los 4 repos del worker).
- **100% software (docs)**, sin red/nube/compilación/hardware → **cero riesgo de timeout**
  (disciplina 07-07). No toca firmware, backend ni `data/field_captures` (ni mirado).
- **NO está en ningún branch.** Genuinamente pendiente (era el item #14, sin tocar desde 07-07).

## Qué hice
1. **Confirmé que el drift era REAL** antes de tocar nada (no manufacturar trabajo): comparé el
   `README.md` contra `act.md` (fuente de verdad), `PORTFOLIO.md`, `QUE_FALTA.md`, `CLAUDE.md` y la
   estructura real del repo (`ls`). Hallazgos concretos de mentira:
   - **Estado falso:** "🟡 Scaffolding creado, esperando contexto de uso real" + "antes de empezar
     la refactorización, completar CONTEXTO_USO_REAL.md". Realidad (act.md + PORTFOLIO): validado
     E2E en banco, refactor hecho, CONTEXTO completado en sus secciones bloqueantes.
   - **Ruta muerta:** apuntaba a `C:\Users\Pandemonium\Documents\GALGAS CON SUPABASE\`; el repo vive
     en `C:\Proyectos\galgas` desde el 07-07.
   - **Pointer roto:** "Seguí con `docs/PLAN_v2_DEFINITIVO.md`" — ese archivo **no existe** (es
     `PLAN_v2_HISTORICO.md`; el vigente es `PLAN_v3.md` + `PLAN_v5_GATEWAY.md`).
   - **Estructura idealizada:** describía 8 carpetas limpias; el árbol real además tiene `build/`,
     `bins_*`, `redler/`, `esp_rx_receptor/` top-level y sketches experimentales de firmware.
2. **Reescribí `README.md`** (quirúrgico, veraz, sin sobre-documentar):
   - **Estado real** con tabla de los 3 nodos (A 0.1.3 vía OTA / B 0.1.1 pendiente re-flash / RX
     heartbeat-only 0.1.1-rx-minimal) tomada del cierre de `act.md`.
   - **`act.md` designado fuente de verdad** (consistente con PORTFOLIO: "las docs raíz están
     desactualizadas") y "Cómo leer" reordenado: CLAUDE.md → act.md → QUE_FALTA → PLAN_v3/v5 →
     CONTEXTO → INDEX.
   - Ruta corregida a `C:\Proyectos\galgas`; sección "Relación con el workspace" (que citaba la
     ruta muerta) reemplazada por "Ubicación en el disco" con repo + cuartel + legacy.
   - Bloque de estructura con **nota honesta**: `build/`/`bins_*`/sketches experimentales NO son
     canónicos; el mapa autoritativo es `CLAUDE.md §4` (no dupliqué el mapa, apunté a él).
   - Quick start real (arduino-cli con Core 3.3.1 + `min_spiffs`, `sync_secrets.ps1`), TLS GTS Root
     R4 y mDNS-descartado en Principios (lecciones ya pagadas del QUE_FALTA).
3. **Verifiqué que los 14 pointers del README nuevo existen en disco** (script de check: act.md,
   QUE_FALTA, CLAUDE, CONTEXTO, PLAN_v3, PLAN_v5_GATEWAY, INDEX, SETUP.ps1, sync_secrets.ps1,
   redler, firmware/shared, firmware/esp_a_emisor, web, data/field_captures) → **14/14 OK**. Un fix
   de drift no debe introducir otro drift.
4. **`QUE_FALTA.md` #14** (en el branch) apunta al fix con la evidencia. `main` de galgas quedó
   **prístino** (pointer en el branch, como 07-25/-26).

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-27-readme-drift
git diff main --stat                        # -> README.md (~59+/75-) + QUE_FALTA.md (+1)
# El drift que se corrige (en el README de MAIN, la version vieja):
git show main:README.md | Select-String "Scaffolding|GALGAS CON SUPABASE|PLAN_v2_DEFINITIVO"
#   -> 3 lineas mentirosas
git show HEAD:README.md | Select-String "Scaffolding|GALGAS CON SUPABASE|PLAN_v2_DEFINITIVO"
#   -> VACIO (ya no miente)
# Los pointers del README nuevo existen:
'act.md','QUE_FALTA.md','CLAUDE.md','CONTEXTO_USO_REAL.md','docs/PLAN_v3.md','docs/PLAN_v5_GATEWAY.md','docs/INDEX.md','scripts/SETUP.ps1','scripts/sync_secrets.ps1','redler','firmware/shared','web','data/field_captures' | % { if (Test-Path $_) {"OK  $_"} else {"MISSING  $_"} }
git checkout main
```
**Resultado de esta noche:** README reescrito reflejando el estado real; 14/14 pointers verificados;
`main` de galgas prístino. Solo docs — no hay tests que correr ni build (es un README).

## Qué quedó SIN verificar / para el día (Matías + @verificador)
1. **Otras docs raíz** pueden seguir con drift menor (el item #14 dice "docs raíz", plural). Foco de
   esta noche fue el `README.md` (el que hace más daño en cold-start). `CLAUDE.md §2` todavía dice
   "PLAN_v3.md vigente" sin mencionar `PLAN_v5_GATEWAY.md` — revisable en una pasada futura, pero
   **no lo toqué** (WIP=1, quirúrgico; y CLAUDE.md es delicado, mejor con criterio de día).
2. **Mergear el branch** `07-27-readme-drift` (aditivo/docs: README reescrito + 1 línea en
   QUE_FALTA; no toca código, firmware ni backend). Acción humana con criterio — no la hago yo.
3. El README afirma el estado de los nodos "al último cierre de act.md" — si Matías flasheó/movió
   algo entre esa sesión y hoy, ajustar la tabla de nodos (fuente sigue siendo act.md).

## Observaciones para el día (no tareas mías)
- **El README era una trampa de cold-start.** El PORTFOLIO ya avisaba "las docs raíz están
  desactualizadas; fuente de verdad = act.md", pero el README no lo decía — quien empezara por él
  (lo natural) creía que galgas estaba sin arrancar. Ahora el propio README manda a `act.md`.
- **La COLA_MERGE de galgas ahora tiene 11 branches** (los 10 previos + este). El cuello sigue
  siendo drenaje humano + @verificador, no producción nocturna. Este branch es el más barato de
  drenar de todos: solo docs, sin tests, sin riesgo de romper nada.
- No toqué datalogger, frioseguro ni cosechador. `data/field_captures` de galgas: ni mirado.

## Reglas respetadas
Solo software (docs) + análisis + git. **Nada mergeado, borrado, movido ni deployado**; no borré
ninguna rama; `main` de galgas quedó **prístino**; sin `rm -rf`, `reset --hard` ni `push --force`;
sin migraciones; sin mDNS; `data/field_captures` intacto; sin tocar firmware/backend; sin
compilaciones ni descargas → cero riesgo de timeout. El branch **no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-27-readme-drift` (galgas, pusheado a origin; sale del `main` de hoy;
1 commit: `README.md` reescrito + pointer en `QUE_FALTA.md`).

## Notas para @verificador
- **DoD** = *"el `README.md` de galgas ya no afirma estado/ruta/pointers falsos (scaffolding,
  `GALGAS CON SUPABASE`, `PLAN_v2_DEFINITIVO.md`), refleja el estado real de los 3 nodos, designa
  `act.md` como fuente de verdad, y los 14 pointers que referencia existen en disco"*.
- Ataques sugeridos: (a) `git show HEAD:README.md | Select-String "Scaffolding|GALGAS CON SUPABASE|
  PLAN_v2_DEFINITIVO"` → vacío; (b) cada pointer del README nuevo con `Test-Path` → todos OK;
  (c) contrastar la tabla de nodos del README contra el §"Estado al cierre" de `act.md` → consistente
  (A 0.1.3 / B 0.1.1 / RX heartbeat); (d) confirmar que NO tocó código: `git diff main --stat` solo
  lista `README.md` + `QUE_FALTA.md`.
