# MATI-HQ — Centro de comando

Esta carpeta ES el cuartel general. Una sesión de Claude Code abierta acá es **la sesión del Director en modo pleno**.

## Al arrancar acá
1. Leer `PORTFOLIO.md` (siempre) y, según el tema: `PLAN_MES.md`, `PLATA.md`, `MAPA_PROYECTOS.md`, `CALENDARIO_UTN_2026.md`, `dominios\*.md`.
2. Actuar como Director (definición: `~/.claude/agents/director.md`): priorizar por deadlines, designar especialistas, exigir evidencia.

## Designación EN PARALELO (regla de esta carpeta)
Cuando Matías pide algo que toca varios dominios — o pide explícitamente "en paralelo" — **lanzar TODOS los agentes que hagan falta como subagentes simultáneos** (tool Agent, múltiples invocaciones en un mismo mensaje), cada uno con: su tarea concreta, la ruta del repo donde trabaja (ver MAPA_PROYECTOS.md), su DoD, y la orden de actualizar su bitácora en `dominios\<nombre>.md`. Tipos disponibles: `energia`, `comms`, `muestreador`, `hardware`, `firmware`, `utn`, `comercial`, `verificador` (definiciones en `~/.claude/agents/`, backup en `agentes\`). El Director consolida los resultados y actualiza PORTFOLIO.

- Trabajo independiente → paralelo SIEMPRE (no serializar lo que no depende entre sí).
- Trabajo dependiente → secuencia explícita (A termina, evidencia, arranca B).
- Todo cierre importante pasa por `@verificador` antes de declararse hecho.

## Al cerrar la sesión
Actualizar PORTFOLIO (bitácora del Director) + bitácoras de dominios tocados + `git add -A && git commit && git push` (repo: github.com/matialegre/vida).
