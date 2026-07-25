# COLA DE MERGE — branches nocturnos pendientes de drenar

> Generado 2026-07-24 (turno nocturno local, worker de la PC) con datos **reales de git**
> (`merge-tree --write-tree`, `rev-list`, `merge-base`) tomados esa noche.
> **Por qué existe:** los últimos ~8 nocturnos vienen diagnosticando lo mismo — *"el cuello
> de botella ya no es producir trabajo de noche, es drenarlo de día con @verificador"*.
> Hoy hay **25 branches nocturnos útiles sin mergear** (26 ramas, una subsumida) repartidos
> en 4 repos, y **ningún diario individual sabe cómo se comporta su branch contra el main de
> HOY ni contra los otros branches**. Este doc es esa vista cruzada: el plan de drenaje.
>
> **Este es el análisis de la noche, no un branch nuevo** (hubiera sido el #27). Es 100 %
> software/análisis, no destructivo, no toca ninguno de los 4 repos.

## TL;DR para Matías / @verificador (si leés una sola cosa)
1. **galgas (10 branches)** y **cosechador (1)** están **sanos**: salen del mismo main, 0
   commits atrás, mergean limpio. Drenaje mecánico — el único cuidado es `QUE_FALTA.md`
   (lo tocan casi todos → conflicto **garantizado** después del primer merge de cada repo:
   resolver a mano, no es un error). **Empezá por acá: es la victoria más barata.**
2. **datalogger (8 branches)** 🔴 **están STALE**: main avanzó **6-8 commits** (trabajo de
   día) y **ninguno de los 8 branches se rebaseó nunca**. `merge-tree` los da "limpios" pero
   eso es engañoso: son estado viejo del firmware. **NO mergear naïve — `git rebase main` +
   re-correr tests por branch antes de tocar main.**
3. **2 pares redundantes ya detectados** (no drenar los dos):
   - frioseguro `07-11-b` está **subsumido** en `07-13` (es su ancestro) → mergear **solo 07-13**.
   - datalogger `07-09-sd-integrity` y `07-15-sd-integrity` son **dos versiones competidoras**
     del mismo trabajo (mismos 4 archivos, ramas independientes) → elegir **una** (07-15 es
     más completa), descartar la otra.
4. **1 branch arrastra basura**: galgas `07-09` trae **6 binarios de build** (`.bin/.elf/.map`,
   ~144k líneas). Sacarlos del árbol antes de mergear (o cherry-pick solo del source).

---

## Estado por repo (números reales al 2026-07-24)

| Repo | Branches pend. | Main (commits) | Salud | Acción global |
|---|---|---|---|---|
| **galgas** | 10 | 2 | ✅ sano (todos base 07-07, 0 atrás, merge limpio) | drenar en orden; resolver `QUE_FALTA.md` a mano |
| **datalogger** | 8 | 10 | 🔴 STALE (6-8 commits atrás) | **rebasear c/u** antes de mergear |
| **frioseguro** | 7 (6 útiles) | 13 | 🟡 mixto (2 viejos conflictúan, 1 subsumido) | drenar los nuevos; decidir los 2 viejos |
| **cosechador** | 1 | 2 | ✅ sano | drenar directo |

Convención de la columna **merge**: `LIMPIO` = `merge-tree` sin conflictos contra el main de
hoy · `STALE-N` = mergea limpio pero está N commits atrás (revisar/rebasear) · `CONFLICTO` =
conflicto textual real.

---

## galgas — ✅ drenaje mecánico (P0 octubre)
Todos salen de `main` (07-07), **0 commits atrás**, **merge LIMPIO**. Orden sugerido: docs
primero (bajan ruido), luego los modelos+tests, RX al final (el más pesado).

| # | Branch | Qué | Archivos / líneas | Nota |
|---|---|---|---|---|
| 1 | `nocturno/local-2026-07-16-b-docs-entrada` | Docs de entrada (README/INDEX/CLAUDE/QUE_FALTA) | 4 / +152-99 | — |
| 2 | `nocturno/local-2026-07-17-linaje-firmware` | Linaje/estado de firmware (act.md, ESTADO_FIRMWARE) | 3 / +214-4 | — |
| 3 | `nocturno/local-2026-07-22-readme-drift` | Fix drift README vs código | 2 / +57-45 | — |
| 4 | `nocturno/local-2026-07-11-vpp-threshold-audit` | Modelo+tests umbral Vpp de alerta | 4 / +683 | test: `tools/test_vpp_threshold_audit.py` |
| 5 | `nocturno/local-2026-07-15-energy-budget` | Presupuesto de energía del nodo galga | 4 / +700 | test: `tools/test_energy_budget.py` |
| 6 | `nocturno/local-2026-07-16-alert-hold-replay` | Modelo hold/replay de alertas | 4 / +720 | test: `tools/test_alert_hold_replay.py` |
| 7 | `nocturno/local-2026-07-19-rx-detection-replay` | Modelo detección RX (replay) | 4 / +683 | test: `tools/test_rx_detection_replay.py` |
| 8 | `nocturno/local-2026-07-20-b-ota-decision-model` | Modelo decisión OTA A/B | 4 / +554 | test: `tools/test_ota_decision_model.py` |
| 9 | `nocturno/local-2026-07-23-firmware-check-edge` | Edge Function firmware-check + tests | 5 / +553 | test: `logic.test.ts` (Deno/node) |
| 10 | `nocturno/local-2026-07-09-rx-deuda-verificador` | RX receptor (Task 08) firmware + migración set_config | 12 / +144775-90 | ⚠️ **incluye 6 binarios de build** en `build/esp_rx_371/` — sacarlos antes de mergear |

**Cuidado transversal galgas:** los 10 tocan `QUE_FALTA.md`. Tras el primer merge, los otros 9
conflictúan ahí → resolución trivial a mano (quedarse con la unión de los ítems marcados
"EN BRANCH"). No es un bug del branch.

---

## datalogger — 🔴 STALE: rebasear antes de mergear (P0 octubre)
Main tiene **10 commits**; **los 8 branches salen de 07-07/07-08 y están 6-8 atrás** — nunca
se rebasearon. El "+X-1591" de casi todos es porque el branch **no tiene** cambios que el main
de día ya incorporó. `merge-tree` los da limpios, pero es estado viejo del firmware:
**`git rebase main` + re-correr tests por branch**; si el rebase toca `firmwares/pico2w-node/*`
que main ya cambió, revisar a mano.

| Branch | Qué | Atrás | Nota |
|---|---|---|---|
| `nocturno/local-2026-07-21-eco-schedule-model` | Modelo duty-cycle nodo ECO + 23 tests | 6 | el más nuevo; rebase probablemente barato |
| `nocturno/local-2026-07-19-b-rv1-mesh-model` | Modelo ruteo mesh RV1 + tests | 6 | — |
| `nocturno/local-2026-07-17-b-ssid-casing` | Casing SSID `Gimap`/`GIMAP` + wifi_nets | 6 | — |
| `nocturno/local-2026-07-15-sd-integrity` | Integridad SD (seq/gaps) + tests | 6 | ⚠️ **duplica** al 07-09 (ver abajo) — **preferir éste** (+785 vs +464) |
| `nocturno/local-2026-07-10-rssi-calib` | Calibración RSSI↔distancia + tests | 6 | — |
| `nocturno/local-2026-07-09-sd-integrity` | Integridad SD (versión previa) | 6 | ⚠️ **redundante** con 07-15 → **descartar** salvo que tenga algo único |
| `nocturno/local-2026-07-08-ecolora-fixes` | Fixes eco-LoRa (grande) | 8 | 56 archivos, +986-4266; rebase pesado |
| `nocturno/local-2026-07-07-ina219-ecolora` | Driver INA219 + eco-LoRa (base) | 8 | 54 archivos; el más viejo y stale |

**Decisión pendiente (día):** los `07-09` vs `07-15` sd-integrity son ramas independientes que
tocan los mismos 4 archivos → son dos intentos del mismo entregable. Diffearlas y quedarse con
una sola. Igual con `07-07`/`07-08` (eco-LoRa base + fixes): probablemente el 08 subsume al 07.

---

## frioseguro — 🟡 mixto (P1 = PLATA, categoría 1 de la jerarquía)
Los **nuevos** (base ≥07-14) mergean limpio; los **dos viejos** (07-11-b, 07-13) son
pre-reconstrucción del 13/07, están 10 atrás y conflictúan en `QUE_FALTA.md`.

| Branch | Qué | Atrás | Merge | Acción |
|---|---|---|---|---|
| `nocturno/local-2026-07-24-scan-secrets-sbkeys` | Scanner secrets esquema `sb_secret_/sb_publishable_` | 0 | LIMPIO | drenar (chico, tests verdes) |
| `nocturno/local-2026-07-23-b-retencion-datos` | Retención datos cron + oráculo + 25 tests | 0 | LIMPIO | drenar |
| `nocturno/local-2026-07-20-door-alert-model` | Modelo alerta de puerta + tests | 0 | LIMPIO | drenar |
| `nocturno/local-2026-07-18-alert-model` | Modelo de alertas + tests | 1 | LIMPIO | drenar |
| `nocturno/local-2026-07-14-vista-estabilidad-comercio` | Vista estabilidad comercio (dashboard) | 2 | LIMPIO | drenar (rebase trivial) |
| `nocturno/local-2026-07-13-resumen-mensual-fixes` | Resumen mensual #11 + fixes @verificador | 10 | 🔴 CONFLICTO `QUE_FALTA.md` | **contiene al 07-11-b**; rebasear + resolver + decidir si el feature sigue vigente |
| ~~`nocturno/local-2026-07-11-b-resumen-mensual`~~ | (subsumido: es ancestro de 07-13) | 10 | 🔴 CONFLICTO | **NO drenar por separado** — ya está dentro de 07-13 |

---

## cosechador — ✅ (P2)
| Branch | Qué | Atrás | Merge |
|---|---|---|---|
| `nocturno/local-2026-07-18-modelo-energia` | Modelo energía harvester (Tablas 5/6 del paper) + 18 tests | 0 | LIMPIO |

---

## Los 4 peligros transversales (lo que un merge apurado rompería)
1. 🔴 **datalogger stale (6-8 commits atrás × 8 branches).** `merge-tree` "limpio" ≠ seguro:
   son estado viejo del firmware. Rebasear + re-testear cada uno. Es el mayor riesgo de la pila.
2. 🟡 **`QUE_FALTA.md` es un imán de conflictos** en los 4 repos (casi todos lo tocan). Tras el
   primer merge de cada repo, el resto conflictúa ahí. Trivial de resolver (unión de ítems),
   pero hay que esperarlo. Alternativa de fondo: dejar de tocar QUE_FALTA en los branches.
3. 🟡 **2 pares redundantes**: frioseguro 07-11-b⊂07-13 (subsumido) y datalogger
   07-09≈07-15 sd-integrity (competidores). Drenar el par completo duplicaría/pisaría trabajo.
4. 🟢 **Binarios de build en galgas 07-09** (`build/esp_rx_371/*.bin/.elf/.map`, ~144k líneas).
   No deben entrar a main. Sacarlos del árbol o cherry-pick solo del source; sumar `build/` al
   `.gitignore` de galgas si no está.

## Cómo verificar cada branch antes de mergear
Cada branch tiene su **diario** con los comandos exactos (tests, `--demo-hallazgo`, etc.):
`diario/nocturno-local-<fecha>.md` (o `-b`). El patrón general de los branches "modelo+tests":
```powershell
cd C:\Proyectos\<repo>
git checkout <branch>
python -m unittest <el test_*.py listado arriba>   # o el comando exacto del diario de esa fecha
git diff main --stat                                # confirmar archivos/líneas
```
Para los STALE de datalogger, **antes**: `git rebase main` y recién ahí correr los tests.

## Cómo se generó este doc (reproducible)
```bash
# por cada branch nocturno de cada repo:
git -C C:/Proyectos/<repo> rev-list --count <branch>..main      # cuántos commits atrás está
git -C C:/Proyectos/<repo> merge-tree --write-tree --name-only main <branch>   # conflictos vs main HOY
git -C C:/Proyectos/<repo> diff --shortstat main..<branch>      # tamaño
git -C C:/Proyectos/<repo> merge-base --is-ancestor <A> <B>     # detectar subsunciones
```

## Higiene detectada de paso (no la toqué)
- **frioseguro** y **cosechador** quedaron con el working tree **checkouteado en un branch
  nocturno** (no en `main`) de turnos previos. Inofensivo, pero conviene volverlos a `main`
  al terminar de drenar para que el próximo worker cree branches desde main fresco.

---
*Mantener este doc: al mergear un branch, tacharlo/borrar su fila. Cuando la cola llegue a 0,
borrar el archivo — su trabajo estará hecho.*
