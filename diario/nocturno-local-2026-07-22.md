# Nocturno LOCAL — 2026-07-22 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
El turno de anoche a las 22:00 (21/07) **murió a los 3 minutos** (lo dice
`scripts/turno_noche_log.txt`: arrancó 22:00:01, terminó 22:03:07) y dejó galgas colgado:
branch `nocturno/local-2026-07-21-b-readme-drift` **sin commits, sin push, sin diario**, con
la mitad de un README editado en el working tree. Esta noche **rescaté y terminé ese
trabajo**: el README de galgas (QUE_FALTA #14 — "el README miente sobre el estado") quedó
sincronizado con la realidad de punta a punta, **cada afirmación verificada contra
`act.md`/`QUE_FALTA.md`/el disco**. Branch nuevo:
**`nocturno/local-2026-07-22-readme-drift` (galgas), pendiente de merge.**

## Tarea elegida y por qué
**galgas #14 (P0 octubre) — drift de docs raíz.** No fue elección libre: había un turno
interrumpido con trabajo a medio hacer en el working tree. La regla dice "una tarea bien
hecha por noche" y la opción obvia era terminar la que quedó huérfana antes de abrir un
frente nuevo:
- El README de galgas decía "🟡 Scaffolding creado, esperando contexto" cuando el sistema
  está **desplegado, validado E2E en banco y con OTA andando** — es LA doc de entrada del
  repo P0 de octubre, y mentía.
- datalogger recibió el turno completo de anoche (eco-schedule-model) → no apilo.
- frioseguro/cosechador tienen pilas de branches esperando merge.
- Es 100 % docs: cero riesgo, cero hardware, cero descargas (disciplina del 07-07 intacta).

## Qué hice — branch `nocturno/local-2026-07-22-readme-drift` (galgas)
Sale de `main`, commit `cfec290`. **2 archivos, 57 inserciones / 45 borradas (solo texto
del README + nota en QUE_FALTA). No toca código, ni firmware, ni data/.**

1. **Herencia auditada, no aceptada a ciegas**: la mitad superior del README (estado 🟢,
   Supabase `wtjjxhoyoqeicrydsppg` sa-east-1, `dreyfus-gimap.netlify.app`, A/B posteando,
   RX heartbeat-only, OTA 0.1.2→0.1.3, flags `DEV_SIMULATE_ADC`/`DEV_BENCH_NO_BATTERY`)
   venía del turno muerto — **verifiqué cada dato contra `act.md`** (líneas 239-244, 913,
   929, 575-576 para RLS) antes de commitearla.
2. **Mitad inferior (lo que faltaba)**:
   - **Árbol de estructura real**: antes listaba `docs/PLAN_v2_DEFINITIVO.md` (no existe;
     hoy son `PLAN_v3.md` vigente + `PLAN_v5_GATEWAY.md` + `PLAN_v2_HISTORICO.md`),
     `backend/config.toml` (real: `backend/supabase/config.toml`, ADR-0002) y omitía
     `redler/` (mockup SCADA, QUE_FALTA #9), `bins_ota_*` y los sketches de prueba OTA.
   - **Quick start**: fuera el "(cuando esté todo migrado)" — ya está migrado y SETUP.ps1
     ya corrió; ahora dice qué correr hoy (npm run dev, arduino-cli con Core 3.3.1).
   - **"Relación con el workspace"**: apuntaba a `Documents\GALGAS CON SUPABASE\` — el
     repo vive en `C:\Proyectos\galgas` desde el 07-07 con remoto matialegre/galgas.
     Paths absolutos reales para legacy y FrioSeguro.
   - Fuera el principio "8 carpetas top-level" (hoy hay ~20 — era mentira estructural).
3. **QUE_FALTA #14**: nota EN BRANCH pendiente de merge.

## Cómo verificarlo (comandos exactos, sin hardware)
```bash
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-07-22-readme-drift
git diff main --stat            # -> 2 archivos, 57+/45-
git diff main -- README.md      # leer: cada claim tiene respaldo en act.md / QUE_FALTA.md
ls docs/ firmware/ backend/supabase/   # -> coincide con el árbol nuevo del README
```
**Resultado esta noche:** árbol/paths/IDs cotejados contra el disco y `act.md` (grep de
`wtjjxhoyoqeicrydsppg`, `dreyfus-gimap`, `0.1.3`, RLS). Nada quedó afirmado sin fuente.

## Qué quedó SIN hacer / para el día
1. **Branch huérfano `nocturno/local-2026-07-21-b-readme-drift`** (galgas, local, SIN
   commits — apunta a main): lo dejé porque no borro nada de noche. Matías lo puede borrar
   con `git branch -d nocturno/local-2026-07-21-b-readme-drift` (es vacío, sin riesgo).
2. **¿Por qué murió el turno de las 22:00 del 21/07?** El log solo muestra arranque y fin a
   los 3 min; el de hoy (22:00:01 del 22/07) soy yo. Si vuelve a pasar, mirar el harness
   del scheduler (script `scripts/` de MATI-HQ).
3. **Drift restante en galgas `CLAUDE.md` §9**: paths relativos del workspace viejo
   (`../GALGAS POST DREY (2)`, `../AgenteBahia-master (1)`). Lo dejé anotado EN el propio
   README (nota al pie) en vez de reescribir el archivo de reglas de noche — decisión
   consciente, es quirúrgico tocarlo con Matías despierto.
4. QUE_FALTA #14 menciona también "docs raíz" en plural — `CONTEXTO_USO_REAL.md` sigue
   parcial (eso es de Matías, no de un agente).

## Reglas respetadas
Solo docs. Nada borrado (ni el branch huérfano). No toqué firmware, ni `data/field_captures`
(ni lo leí), ni la nube. Sin descargas ni compilaciones — cero riesgo de timeout. El branch
**no se mergea** hasta @verificador.

## Branch
`nocturno/local-2026-07-22-readme-drift` (galgas, pusheado a origin; sale de `main`, commit `cfec290`).

## Notas para @verificador / @cronista / @director
- **@verificador:** DoD = *"ninguna afirmación del README nuevo es falsa"*. Ataque
  sugerido: tomar 5 claims al azar del README y buscar su respaldo (`act.md` §Sesión 2/5,
  `QUE_FALTA.md`, `ls` del disco). Ojo especial a la mitad superior: la heredé del turno
  muerto y la verifiqué yo — segunda mirada bienvenida.
- **@cronista:** el ítem #14 era tuyo — con este branch queda el grueso hecho; falta solo
  el CLAUDE.md §9 (arriba).
- **@director:** noche de rescate — un turno crasheado no se convirtió en trabajo perdido
  ni en trabajo duplicado. Sigue en pie: las pilas de branches nocturnos (galgas ya tiene
  9) necesitan sesiones de día con @verificador para mergear en orden; el drift del
  scheduler de las 22:00 merece una mirada al harness.
