# Nocturno LOCAL — 2026-07-27-b (2do turno, worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
Escribí **`tools/merge_queue_status.py`** (en MATI-HQ): regenera la cola de merge de los 32 branches
nocturnos con git EN VIVO y la **métrica correcta de merge**. Al correrlo apareció el hallazgo de la
noche: **la alarma central de la `COLA_MERGE_NOCTURNOS.md` del 07-24 es FALSA.** El doc decía que los
8 branches STALE de datalogger *"borrarían todo `misiones/`"* — eso salió de medir con
`git diff main..branch` (two-dot), que muestra las adiciones POSTERIORES de main como falsos "borrados".
Con la métrica real (merge 3-way: `merge-tree --write-tree` → diff contra main), **ninguno de los 32
branches, en los 4 repos, borra un solo archivo** (0 borrados, verificado). Reporte fresco:
`COLA_MERGE_STATUS_2026-07-27.md`. Tool + tests en `tools/`. **En MATI-HQ main** (no branch — es cuartel,
igual que la COLA_MERGE original).

## Tarea elegida y por qué
**Herramienta que regenera la cola de merge con métrica correcta** — ataca directo el cuello #1.
- **El cuello real está documentado hace ~10 noches:** *"ya no es producir branches, es drenarlos"*
  (COLA_MERGE = 25→32 branches sin mergear). Producir otro modelo+tests #28 tendría valor negativo.
  Lo más útil que puede hacer un worker nocturno hoy es **hacer el drenaje humano más barato y seguro**.
- **La COLA_MERGE a mano (07-24) ya drifteó en 3 días:** le falta `07-21-b-readme-drift` (galgas), no
  refleja los 07-25/-26 de datalogger, y —lo grave— **clasifica mal por usar la métrica equivocada**.
  Un tool que la regenera en 2 segundos con git vivo elimina la staleness de raíz.
- **100% software/git, solo lectura** (`rev-list`, `merge-tree --write-tree`, `diff`, `merge-base` — sin
  checkout/merge/reset, no toca refs ni working-tree) → **cero riesgo de timeout** y cero riesgo de romper
  nada. No toca firmware, backend ni `data/field_captures`.
- **Genuinamente nueva** — no está en ningún branch.
- **Prioridad:** sirve el drenaje de TODOS los repos, incluyendo PLATA (frioseguro) y octubre (galgas),
  que son categorías 1 y 2 de la jerarquía.

## Qué hice
1. **Confirmé el bug de métrica con git real** (antes de escribir el tool): mergeé por 3-way
   (`merge-tree --write-tree`) los 8 branches STALE de datalogger y diffeé el árbol resultante contra
   main → **CLEAN, 0 borrados, `misiones/` intacto en los 8**. El "-1591 deletions" del doc es el
   two-dot `git diff main..branch`, que NO modela un merge (muestra lo que main agregó DESPUÉS como si
   el branch lo borrara). Esto es lo que hizo marcar 8 branches sanos como "tóxicos que nukean el firmware".
2. **Escribí `tools/merge_queue_status.py`** (stdlib pura, sin deps). Por cada branch `nocturno/*` de los
   4 repos calcula, con la métrica correcta:
   - `behind`/`ahead` vs main.
   - Resultado del merge 3-way: limpio o conflicto (con archivos en conflicto).
   - Impacto REAL sobre main: archivos **agregados / modificados / borrados** por el merge (árbol
     mergeado vs main, no diff de tips).
   - Flags: **binarios/artefactos de build** arrastrados (numstat `-\t-` o extensión `.bin/.elf/.map/...`),
     **subsunción** (branch ancestro de otro → drenar solo el otro), y **ya-en-main** (rama sin commits
     nuevos → borrar el ref).
   - Clasifica con una función **pura** `classify()`: `YA-EN-MAIN` / `CONFLICTO` / `BORRA-ARCHIVOS` /
     `BINARIOS` / `SUBSUMIDO` / `REVISAR-STALE` / `LIMPIO-ADITIVO` (prioridad de más peligrosa a más segura).
   - Salida markdown (default) o `--json`.
3. **Tests offline de la lógica pura** (`tools/test_merge_queue_status.py`, `unittest`, **12 tests OK**):
   cubren el orden de prioridad de las señales y los casos borde (ya-en-main gana sobre subsumido, borra
   gana sobre binarios, conflicto sobre borra, modifica-al-día ≠ stale, etc.).
4. **Corrí el tool contra los 4 repos reales** → `COLA_MERGE_STATUS_2026-07-27.md`. Dos hallazgos que la
   corrida contra la realidad atrapó y mejoraron el tool:
   - `galgas/07-21-b-readme-drift` **apunta al mismo commit que main** (`36b6b94`, `ahead=0`): rama huérfana,
     no un branch pendiente → agregué la etiqueta `YA-EN-MAIN` (antes caía mal en `SUBSUMIDO`).
   - `datalogger/07-07-ina219-ecolora` **es ancestro de `07-08`** → `SUBSUMIDO` (drenar solo 07-08).
5. **Puse un banner de corrección** en `COLA_MERGE_NOCTURNOS.md` apuntando al tool y desmintiendo la alarma
   de "borra misiones/" (conservo el análisis viejo abajo como registro histórico del 07-24).

## Resultado (reporte del 07-27, 32 branches)
| Estado | # | Qué significa |
|---|--:|---|
| `LIMPIO-ADITIVO` | 19 | solo agrega — drenaje mecánico seguro |
| `REVISAR-STALE` | 8 | limpio+sin borrar, pero modifica archivos desde base vieja — revisar que no reviertan main |
| `CONFLICTO` | 2 | conflicto textual real (frioseguro resumen-mensual 07-11-b y 07-13, en `QUE_FALTA.md`) |
| `BINARIOS` | 1 | galgas `07-09-rx` arrastra 6 binarios de build — sacarlos antes de mergear |
| `SUBSUMIDO` | 1 | datalogger `07-07` ⊂ `07-08` |
| `YA-EN-MAIN` | 1 | galgas `07-21-b` — rama huérfana en el tip de main, borrar el ref |

**Verificación independiente:** `--json` + suma de borrados sobre los 32 merges = **0**.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
cd C:\Users\Pandemonium\Documents\MATI-HQ
python -m unittest tools.test_merge_queue_status          # -> 12 tests OK
python tools\merge_queue_status.py                        # -> tabla markdown de los 4 repos
python -X utf8 tools\merge_queue_status.py --json | python -c "import sys,json; d=json.load(sys.stdin); print('borrados:', sum(len(b.get('deleted',[])) for r in d for b in r['branches']))"
#   -> borrados: 0   (desmiente el 'borra misiones/' del doc viejo)
```
Prueba puntual de la métrica (un branch STALE de datalogger que el doc daba por tóxico):
```bash
repo=C:/Proyectos/datalogger; br=nocturno/local-2026-07-15-sd-integrity
tree=$(git -C $repo merge-tree --write-tree main $br)      # merge 3-way real, exit 0 = limpio
git -C $repo diff --stat main $tree                        # -> solo +4 archivos, 0 borrados
git -C $repo diff --diff-filter=D --name-only main $tree | grep -c misiones/   # -> 0
```

## Qué quedó SIN verificar / para el día (Matías + @verificador)
1. **El tool no decide el merge, lo informa.** `REVISAR-STALE` (8 branches, sobre todo el cluster de
   datalogger) NO significa "mergear a ciegas": un merge 3-way limpio puede aplicar un *delta viejo* de
   firmware que semánticamente ya no corresponde. Para esos, revisar los archivos modificados. Los que
   solo tocan `QUE_FALTA.md` (07-09-sd, 07-15-sd, 07-19-b, 07-21) son de bajísimo riesgo.
2. **Matiz honesto sobre el trabajo previo:** los branches de extracción `07-25/-25-b/-26` siguen siendo
   la vía **limpia** para los deliverables que estaban entrelazados con firmware (`07-07`/`07-08`). Pero
   para los que eran modelos puros (p.ej. `07-15-sd-integrity`), la extracción fue *redundante* — se
   podían haber mergeado directo. La corrección no invalida los deliverables; corrige la **razón** ("nukea
   misiones/") que era falsa. Confirmar con @verificador antes de borrar los 8 viejos.
3. **Higiene detectada (no la toqué):** `cosechador` sigue checkouteado en `nocturno/local-2026-07-18-modelo-energia`
   (no en main). Inofensivo; volverlo a main antes de crear el próximo branch. No cambié working-trees.
4. **Mergear nada** — el tool es análisis. Drenaje = acción humana con criterio + @verificador.

## Observaciones para el día (no tareas mías)
- **La lección de fondo:** un doc de estado a mano se pudre en días. La reproducibilidad (el tool) es la
  que sobrevive. La COLA_MERGE del 07-24 ya listaba los comandos "reproducibles" — esto los convierte en
  un script y de paso arregla que usaban la métrica equivocada.
- **El cuello sigue siendo drenaje humano.** 27 de 32 branches son mergeables sin drama (19 aditivos +
  8 a revisar rápido); 2 conflictos triviales (`QUE_FALTA.md`); 1 con binarios; 1 huérfano a borrar.
  Con el reporte fresco, una sola sesión de @verificador + Matías puede bajar la cola fuerte.

## Reglas respetadas
Solo software (tool + tests + docs) + análisis + git de solo lectura. **Nada mergeado, borrado, movido ni
deployado**; no borré ninguna rama ni cambié ningún working-tree (cosechador quedó como estaba); sin
`rm -rf`, `reset --hard` ni `push --force`; sin migraciones; sin mDNS; `data/field_captures` intacto; sin
tocar firmware/backend de ningún repo; sin compilaciones ni descargas → cero riesgo de timeout.

## Entregable (dónde)
En **MATI-HQ, rama `main`** (es cuartel, mismo criterio que `COLA_MERGE_NOCTURNOS.md`: análisis cross-repo,
no toca ninguno de los 4 repos → no va a branch nocturno):
- `tools/merge_queue_status.py` — el tool (stdlib pura).
- `tools/test_merge_queue_status.py` — 12 tests de `classify()`.
- `COLA_MERGE_STATUS_2026-07-27.md` — reporte fresco generado.
- Banner de corrección en `COLA_MERGE_NOCTURNOS.md`.

## Notas para @verificador
- **DoD** = *"existe un tool que regenera la cola de merge con la métrica correcta (merge 3-way real, no
  two-dot), sus tests pasan, y su reporte demuestra con git que 0/32 branches borran archivos —
  desmintiendo el 'borra misiones/' del doc del 07-24"*.
- Ataques sugeridos: (a) `python -m unittest tools.test_merge_queue_status` → 12 OK; (b) elegir 2-3
  branches STALE de datalogger y repetir a mano `merge-tree --write-tree main <br>` + `diff --diff-filter=D`
  → 0 borrados; (c) confirmar que el tool NO hace checkout/merge (grep del código: solo `rev-list`,
  `merge-tree --write-tree`, `diff`, `merge-base`, `rev-parse`, `branch --list`); (d) verificar que el
  working-tree de los 4 repos y de MATI-HQ no cambió (solo se agregaron archivos nuevos en MATI-HQ).
```

## Branch
Ninguno — entregable en **MATI-HQ main** (cuartel). Los 4 repos de proyecto quedaron intactos.
