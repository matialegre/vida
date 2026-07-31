# Nocturno local — 2026-07-30-b (2do turno)

> Worker nocturno local (Matías durmiendo). Segundo turno del día — el primero (07-30)
> pre-resolvió los 8 conflictos-docs de la cola. Este turno los **audita**.

## Tarea elegida y por qué
**Auditar (rol evaluador) las 8 auto-resoluciones que generó el turno de las 07-30 y arreglar
el defecto encontrado en el harness.** No es un branch nuevo ni un 5º generador de tooling:
es el **evaluador** que la doctrina exige (generator≠evaluator) corriendo sobre la salida del
generador de anoche, + harness engineering sobre el bug hallado.

Por qué esta y no otra:
- **Todo lo valioso ya está en un branch.** Revisé los 4 `QUE_FALTA.md`: galgas (14 branches
  nocturnos, mayoría análisis offline: vpp, alert-hold, rx-detection, energy), datalogger
  (SD-integrity y benchmark ya brancheados, el resto es hardware), frioseguro (resumen-mensual,
  vista-estabilidad, alert-model ya brancheados), cosechador (energía ya brancheado). Los
  bloqueantes que quedan son **hardware** (galga física, LiPo, SIM800, banco) o **merge humano**.
  Un branch #35 de análisis sería piling redundante — exactamente lo que 4 noches vienen
  evitando. La jugada de mayor palanca es **des-arriesgar el drenaje**, no producir más.
- El turno 07-30 dejó la cola "mecánica de punta a punta" con `resolve_doc_conflicts.py`, y su
  reporte afirmó *"0 marcadores de conflicto, no revierte nada"*. Pero **verificó 0 marcadores,
  no 0 duplicados** — un hueco clásico del `merge --union`. Valía la pena mirarlo con ojo
  adversarial antes de que un humano corriera el drenaje a ciegas sobre la línea P0/P1.
- 100% software/offline, **read-only sobre los 4 repos** (`git show`/`merge-base`/`merge-file`
  sobre temporales), escribe solo en MATI-HQ → **no suma branch a la cola**.

## Qué encontré (el bug real)
Corrí un escáner de duplicación de anotaciones `EN BRANCH` sobre las 8 resoluciones del 07-30:
**3 de 8 tenían el mismo bullet repetido** —

| Resolución | Branch duplicado | Líneas |
|---|---|---|
| galgas `07-29-vpp-field-characterization` | `07-29` (a sí mismo) | 11 y 12 |
| frioseguro `07-11-b-resumen-mensual` | `07-11-b` | 25 y 27 |
| frioseguro `07-13-resumen-mensual-fixes` | `07-11-b` | 25 y 27 |

**Mecanismo:** `git merge-file --union` toma ambos lados de cada hunk en conflicto. Cuando
`main` (ours) **ya documentaba** el branch — porque una sync nocturna posterior le agregó su
propia línea `EN BRANCH \`X\``, con otra redacción — y el branch `X` trae la suya en su propio
`QUE_FALTA.md`, la union conserva **las dos** → bullet repetido en la bitácora resuelta.
No hay marcador `<<<<<<<`, por eso el chequeo "0 marcadores" del 07-30 lo dejó pasar. Un
humano drenando a ciegas commiteaba el `QUE_FALTA.md` con el bullet repetido (cosmético, pero
en la cara P0 de galgas / P1 de frioseguro, y erosiona la confianza del "drenaje mecánico").

## Qué hice (fix en el harness, no parche a mano)
En `tools/resolve_doc_conflicts.py`:
1. **`en_branch_refs(text)`** (pura) — mapea `{branch: [líneas]}` de las anotaciones
   `EN BRANCH \`nocturno/...\``.
2. **`dedup_en_branch(union_text, ours_text)`** (pura) — si un branch aparece en 2+
   anotaciones y al menos una es **idéntica a una línea de main**, conserva las de main y
   descarta las repetidas (la variante subsumida que aportó el branch). Si ninguna coincide con
   main (caso raro), deja la primera. Devuelve `(texto_dedup, líneas_descartadas)`.
3. **Cableado**: `union_merge_file` lee `ours` antes de limpiar los temporales y aplica el
   dedup → devuelve las líneas descartadas; `build_plan` las registra; `render_markdown` emite
   una nota `🧹 De-duplicado` por resolución afectada.
4. **7 tests nuevos** (incluye el escenario real 07-29): `test_resolve_doc_conflicts` **13 → 20 OK**.

### Resultado (con evidencia git)
- Regeneradas las 8 resoluciones: **0 con duplicado** (re-escaneo), **0 marcadores de conflicto**.
- Las 3 subsumidas quedan **idénticas a main** (`diff` main↔resolución 07-29 = vacío): su único
  cambio de docs ya vivía en main. El **valor real** de esos branches (el código: p.ej.
  `tools/analyze_vpp_field.py` + tests + `docs/`) **no se pierde** — merge-a limpio aparte; solo
  el `QUE_FALTA.md` estaba en conflicto y su resolución correcta ES la de main.
- Los 4 repos, **intactos** (`git status` galgas/frioseguro = limpio; el tool es read-only).
- Reporte `COLA_MERGE_RESOLUCIONES.md` regenerado con las notas de dedup; banner de corrección
  `2026-07-30-b` en `COLA_MERGE_NOCTURNOS.md`.

## Cómo verificarlo (comandos exactos)
```bash
cd "C:/Users/Pandemonium/Documents/MATI-HQ"
python -m unittest tools.test_resolve_doc_conflicts        # 20 tests, OK
python -m unittest tools.test_merge_queue_status           # 23 tests, OK (reuse intacto)
python -X utf8 tools/resolve_doc_conflicts.py --check      # 8 pre-resueltos, 3 notas dedup
# 0 duplicados de EN BRANCH en las 8 resoluciones:
python -X utf8 - <<'PY'
import re, glob
pat = re.compile(r'EN BRANCH\**\s*`?(nocturno/[A-Za-z0-9._\-]+)')
bad = 0
for f in glob.glob("COLA_MERGE_RESOLUCIONES/**/QUE_FALTA.md", recursive=True):
    refs = {}
    for i, l in enumerate(open(f, encoding="utf-8"), 1):
        for m in pat.finditer(l): refs.setdefault(m.group(1), []).append(i)
    if any(len(v) > 1 for v in refs.values()): bad += 1
print("resoluciones con duplicado:", bad)   # 0
PY
# 0 marcadores de conflicto:
grep -rlE '<<<<<<<|>>>>>>>' COLA_MERGE_RESOLUCIONES | wc -l    # 0
# repos intactos:
git -C C:/Proyectos/galgas status --porcelain=v1              # vacio
```

## Qué quedó sin verificar por hardware
Nada aplica — tarea 100% offline/git, sin firmware ni cloud. **Ninguna verificación pendiente.**
Salvedad de criterio: la resolución sigue siendo un **candidato** — el drenaje real lo cierra
un humano que revisa el `.md` y corre los comandos (generator≠evaluator). El tool no mergea.

## Branch
**No hay branch nocturno**: como el 07-30 / 07-29-b / 07-27-b, es tooling+doc del cuartel cuyo
propósito ES achicar la cola → va **directo a MATI-HQ main**. Un branch acá sería el #35. Los 4
repos de trabajo no se tocaron (read-only). Cambios preexistentes en el working tree de MATI-HQ
(`agentes/*`, `dominios/*`, `scripts/turno_noche_log.txt`, `diseno3d.md` sin trackear) **no son
míos** — los dejé intactos; commiteo solo mis archivos con `git add` explícito.
