# Nocturno LOCAL — 2026-07-24-c (3er turno del día, worker de la PC, Matías durmiendo)

> Turnos previos de hoy: `nocturno-local-2026-07-24.md` (frioseguro, scan_secrets sbkeys).
> Este es el turno posterior. **No produje un branch nuevo a propósito** (ver abajo).

## TL;DR para Matías (si leés una sola cosa)
Conté los branches nocturnos sin mergear y son **26 ramas (25 de trabajo útil) en 4 repos**,
prácticamente **ninguna en main**. Los últimos ~8 informes vienen gritando lo mismo: *el cuello
de botella ya no es producir de noche, es drenar de día*. Así que en vez de escribir el branch
**#27**, hice el trabajo que **ningún diario individual puede hacer**: la **vista cruzada** de
toda la pila con datos reales de git — cuáles mergean limpio contra el main de HOY, cuáles están
**stale** (main se les adelantó), cuáles son **redundantes entre sí**, y en qué orden drenarlos.
Quedó en **`MATI-HQ/COLA_MERGE_NOCTURNOS.md`**. Hallazgos que ahorran plata y evitan romper main:
- 🔴 **datalogger: los 8 branches están 6-8 commits ATRÁS** (nunca se rebasearon). `merge-tree`
  los da "limpios" pero es estado viejo del firmware → **rebasear + re-testear**, no merge naïve.
- ♻️ **2 pares redundantes**: frioseguro `07-11-b` está **subsumido** en `07-13` (mergear solo
  uno); datalogger `07-09` y `07-15` son **dos sd-integrity competidores** (elegir uno).
- 🗑️ galgas `07-09` arrastra **6 binarios de build** que no deben entrar a main.
- ✅ galgas (10) y cosechador (1) están **sanos** → drenaje mecánico, la victoria más barata.

## Tarea elegida y por qué
**Construir la cola de merge consolidada de los branches nocturnos (artefacto del Director).**
Razones:
- **Es el hueco que el propio sistema viene marcando**: cada nocturno desde el 07-19 cierra con
  "la pila de branches necesita sesiones de día con @verificador". Nadie había producido el
  **plan de drenaje**. El Director *"persigue los huecos hasta cerrarlos"* (doctrina) — éste es
  suyo, y estaba abierto.
- **Producir el branch #27 es de valor negativo**: agranda la pila que ya es el problema. WIP=1
  y anti-sobre-ingeniería (¿hace falta otro modelo+tests? no; ¿hace falta poder drenar? sí).
- **Información NUEVA, no un resumen**: ningún diario sabe cómo se comporta su branch contra el
  main de HOY ni contra los otros. La staleness de datalogger, las 2 redundancias y los binarios
  del 07-09 **solo se ven mirando la pila entera con git**, que es lo que hice.
- **100 % software/análisis**, stdlib de git, sin red, sin hardware, sin compilar, sin descargas
  → cero riesgo de timeout (disciplina 07-07). **No toqué ninguno de los 4 repos** (solo lectura
  de git); no borré, moví ni mergeé nada.

## Qué hice
1. Enumeré los 26 branches nocturnos de los 4 repos (`git branch -a`) y verifiqué que **ninguno**
   está mergeado a su main (`git branch --merged`).
2. Por cada branch calculé con datos reales:
   - tamaño (`git diff --shortstat main..branch`) y archivos tocados,
   - **conflictos contra el main de hoy** (`git merge-tree --write-tree --name-only main branch`),
   - **cuántos commits atrás está** (`git rev-list --count branch..main`) → así salió la staleness
     de datalogger (6-8) y de los 2 frioseguro viejos (10),
   - **subsunciones** (`git merge-base --is-ancestor A B`) → 07-11-b⊂07-13 confirmado; los dos
     sd-integrity confirmados independientes (competidores, no ancestro).
3. Escribí **`MATI-HQ/COLA_MERGE_NOCTURNOS.md`**: tabla por repo con estado de merge y acción,
   orden de drenaje sugerido (por prioridad de PORTFOLIO: PLATA/uni → P0-octubre → P2), los 4
   peligros transversales, cómo verificar cada branch, y cómo se reproduce el análisis.

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```powershell
# El doc:
Get-Content C:\Users\Pandemonium\Documents\MATI-HQ\COLA_MERGE_NOCTURNOS.md
# Spot-checks de los hallazgos clave:
git -C C:\Proyectos\datalogger rev-list --count nocturno/local-2026-07-21-eco-schedule-model..main   # -> 6 (stale)
git -C C:\Proyectos\frioseguro merge-base --is-ancestor nocturno/local-2026-07-11-b-resumen-mensual nocturno/local-2026-07-13-resumen-mensual-fixes; $?   # -> True (subsumido)
git -C C:\Proyectos\frioseguro merge-tree --write-tree --name-only main nocturno/local-2026-07-13-resumen-mensual-fixes   # -> CONFLICT en QUE_FALTA.md
git -C C:\Proyectos\galgas diff --name-only main..nocturno/local-2026-07-09-rx-deuda-verificador | Select-String '\.(bin|elf|map)$'   # -> 6 binarios
```
**Resultado de esta noche:** todos los números del doc salieron de estos comandos, corridos en
vivo. Sin compilaciones ni descargas — cero riesgo de timeout.

## Qué quedó SIN verificar / para el día (Matías + @verificador)
1. **El drenaje en sí** (mergear los branches) es del día con @verificador — este doc es el plan,
   no la ejecución. No mergeé nada (fuera del mandato nocturno y requiere criterio humano).
2. **Rebase de los 8 branches de datalogger**: hay que hacerlo y re-correr sus tests; recién ahí
   se sabe si algún firmware de día pisó lo que el branch asumía.
3. **Decidir los pares redundantes**: diffear datalogger 07-09 vs 07-15 sd-integrity y quedarse
   con uno; confirmar que frioseguro 07-13 todavía es un feature vigente (o descartar el par).

## Observaciones para el día (no tareas mías)
- **frioseguro** y **cosechador** quedaron con el working tree en un branch nocturno (no en main)
  de turnos previos. Volverlos a `main` al cerrar el drenaje para que el próximo worker cree
  branches desde main fresco.
- **Raíz del problema de datalogger**: los branches se cortan de main pero main avanza de día y
  nunca se mergea de vuelta → la deriva crece. La cura no es más noche, es una **sesión de
  drenaje**. Este doc la hace tractable (de 26 diarios sueltos a 1 plan ordenado).

## Reglas respetadas
Solo lectura de git + un doc nuevo en MATI-HQ. **Nada mergeado, borrado, movido ni deployado**;
no toqué ninguno de los 4 repos; `data/field_captures` de galgas ni mirado; sin compilaciones ni
descargas. No creé branch (decisión deliberada: el valor de la noche era NO agrandar la pila).

## Entregable
`MATI-HQ/COLA_MERGE_NOCTURNOS.md` (nuevo) + este informe. Se commitean a MATI-HQ `main` (igual
que cualquier diario del cuartel). **No hay branch nocturno nuevo** en los repos de proyecto.

## Notas para @verificador / @director
- **@verificador:** el DoD del doc es *"cada número (atrás/adelante/merge/subsunción) coincide con
  lo que devuelve git hoy"*. Reproducí los 4 spot-checks de arriba + un branch al azar de cada
  repo. Ataque útil: ¿algún branch que marqué "LIMPIO" en realidad conflictúa por algo que
  `merge-tree` no ve (p.ej. semántico)? Los STALE de datalogger son justo ese riesgo.
- **@director:** decisión pendiente para vos: ¿vale la pena una **sesión de drenaje** ya (media
  mañana), o se sigue produciendo de noche? Mi lectura: con 25 branches útiles trancados, la
  mañana de drenaje rinde más que cualquier branch #27. El orden del doc respeta la jerarquía
  (frioseguro=PLATA y galgas/datalogger=octubre primero; cosechador último).
