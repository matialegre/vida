# Nocturno local — 2026-07-30

> Worker nocturno local (Matías durmiendo, laburo solo en la PC). Turno único del día.

## Tarea elegida y por qué
**Pre-resolver los 8 conflictos solo-docs de la cola de merge** — el paso que faltaba después
de *clasificarla*. No es un branch nuevo: es tooling+doc del cuartel que hace **mecánico** el
drenaje de día.

Por qué esta y no otra:
- El espacio de análisis offline de los 4 repos sigue **saturado**: 34 branches nocturnos sin
  mergear (galgas 6 en CONFLICTO, todos por `QUE_FALTA.md`). Cada branch nuevo AGRANDA el
  cuello #1 (drenaje humano), no lo achica → habría sido el #35. Mismo criterio que 07-27-b y
  07-29-b: cuando la cola está saturada, la jugada de mayor palanca es **drenar**, no producir.
- El tool `merge_queue_status.py` (07-27-b/07-29-b) ya *clasifica* la cola y descubrió el
  hallazgo clave: **de 8 CONFLICTO, los 8 son SOLO `QUE_FALTA.md`** — bitácora, no firmware.
  Pero "trivial" ≠ "gratis": alguien tenía que sentarse a resolver 8 merges a mano. Esta noche
  automatizo ese trabajo mecánico.
- 100% software/análisis, offline, **read-only sobre los 4 repos** (solo `git show` /
  `merge-base` / `merge-file` sobre temporales — sin checkout/merge/reset/push) y escribe solo
  dentro de MATI-HQ → **no suma un branch a la cola**. Va directo a MATI-HQ main.
- Jerarquía: sirve a P0-octubre (galgas: 6 de las 8 resoluciones) y a P1-PLATA (frioseguro:
  las otras 2, resumen-mensual) — desbloquea el drenaje de ambas líneas.

## Qué hice
Escribí **`tools/resolve_doc_conflicts.py`** (MATI-HQ, stdlib, reutiliza los helpers ya
testeados de `merge_queue_status.py` — DRY):

1. Para cada branch `nocturno/*` cuyo merge da **CONFLICTO 100% en docs**
   (`collision_kind == 'doc'`), reconstruye las 3 versiones (`main` = ours, `merge-base` =
   base, `branch` = theirs) y las fusiona con **`git merge-file -p --union`** → union 3-way:
   conserva las líneas nuevas de **ambos** lados, sin marcadores de conflicto. Es "tomar ambos
   lados" hecho bien (no pisa el avance de main como haría un "tomar theirs").
2. Escribe el archivo fusionado en `COLA_MERGE_RESOLUCIONES/<repo>/<branch>/QUE_FALTA.md` y
   genera, por branch, los **comandos exactos de drenaje** (checkout main → merge --no-commit →
   `cp` de la resolución → add → commit). El humano los corre tras revisar; **el tool nunca
   mergea ni ejecuta nada**.
3. Si un branch chocara en código/config/SQL, lo **SALTEA** y lo marca para revisión humana
   real — jamás auto-resuelve código. (Hoy: 0 salteados, los 8 son solo-docs.)
4. Modos: default (escribe + reporte a stdout), `--check` (dry-run, no escribe), `--repo`,
   `--outdir`.
5. Reporte fresco → **`COLA_MERGE_RESOLUCIONES.md`** + banner 2026-07-30 en
   `COLA_MERGE_NOCTURNOS.md`.

### Resultado (con evidencia git)
**8 branches pre-resueltos** (6 galgas + 2 frioseguro), **0 salteados**. Verificado sobre las
resoluciones escritas:
- **0 marcadores de conflicto** (`<<<<<<<`/`=======`/`>>>>>>>`) en las 8.
- Cada resolución contiene **su propia** línea `EN BRANCH …` del branch.
- Y **conserva el avance de main**: p.ej. la resolución del branch 07-11 tiene 38 líneas =
  main (37) + el bullet nuevo del branch, e incluye **también** los bullets 07-28-b y 07-29
  que main agregó *después* de que nació ese branch → la union no revierte nada.
- Los 4 repos quedaron **intactos** (`git status` de galgas/frioseguro = `main`, sin cambios).

Con esto los 8 "conflictos" de la cola pasan de *merge manual* a *revisar-y-copiar*. Sumado a
los 9 LIMPIO-ADITIVO + 10 stale-docs que ya identificaba `merge_queue_status`, **el drenaje de
día queda mecánico casi de punta a punta** — el único trabajo humano real que queda es mirar
los ~2-3 branches que tocan código (datalogger `07-08-ecolora`, galgas `07-09-rx` con
binarios, frioseguro `07-13-resumen` código).

## Cómo verificarlo (comandos exactos)
```bash
cd "C:/Users/Pandemonium/Documents/MATI-HQ"
python -m unittest tools.test_resolve_doc_conflicts        # 13 tests, OK
python -m unittest tools.test_merge_queue_status           # 23 tests, OK (no se rompió el reuse)
python -X utf8 tools/resolve_doc_conflicts.py --check      # dry-run: 8 pre-resueltos, 0 escritos
python -X utf8 tools/resolve_doc_conflicts.py              # escribe COLA_MERGE_RESOLUCIONES/
# Propiedades de las resoluciones (deben dar 0 y luego 8 "OK"):
grep -rl -e '<<<<<<<' -e '>>>>>>>' COLA_MERGE_RESOLUCIONES | wc -l          # 0 marcadores
# Que los repos NO se tocaron:
git -C C:/Proyectos/galgas status --porcelain=v1 --branch   # ## main...origin/main, sin cambios
```

## Qué quedó sin verificar por hardware
Nada aplica — tarea 100% offline/git, sin firmware ni cloud. **Ninguna verificación pendiente.**
Salvedad de criterio (no de hardware): la union 3-way es una **resolución candidata** — el
drenaje real lo cierra un humano que revisa el `.md` y corre los comandos (generator≠evaluator).
El tool no mergea por su cuenta.

## Branch
**No hay branch nocturno**: como el tooling del 07-27-b/07-29-b (`merge_queue_status.py`), esto
es tooling+doc del cuartel cuyo propósito ES achicar la cola → va **directo a MATI-HQ main**.
Crear un branch nocturno acá sería contraproducente (sería el #35). Los 4 repos de trabajo no
se tocaron (read-only).

## Nota para @cronista (drift menor, ya venía del 07-29-b, NO tocado)
Sigue pendiente: `dominios/comercial.md` → sección "Material producido" tiene PITCH.md,
PRECIOS_FRIOSEGURO.md, `hoja_mostrador*.html` y CONTRATO_BORRADOR.md como `[ ]` sin marcar
aunque existen completos. Marcarlos `[x]` en una pasada de sync.
