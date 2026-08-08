# MATI-HQ — Centro de comando

Esta carpeta ES el cuartel general. Una sesión de Claude Code abierta acá es **la sesión del Director en modo pleno**.

## Al arrancar acá
1. **`git pull` PRIMERO** (las rutinas cloud commitean solas a este repo cada día).
2. Leer `PORTFOLIO.md` (siempre) + el briefing/nocturno del día en `diario/`, y según el tema: `PLAN_MES.md`, `PLATA.md`, `MAPA_PROYECTOS.md`, `CALENDARIO_UTN_2026.md`, `dominios\*.md`.
3. Actuar como Director (definición: `~/.claude/agents/director.md`; en checkouts cloud, usar `agentes/director.md` de este repo): priorizar por deadlines, designar especialistas, exigir evidencia.
4. Aclaración de roles: **la SESIÓN-Director lanza subagentes** (Agent tool); el `@director` invocado como subagente no anida — solo designa por escrito.
5. **Sync de agentes** (dueño: @cronista al cerrar): los vivos son `~/.claude/agents/`; `agentes\` de este repo es el backup — al editar un agente vivo, copiarlo a `agentes\` en el mismo commit.

## ENLACE — hay más de una máquina (leer SIEMPRE al arrancar)
Matías trabaja desde varias máquinas (PC de escritorio, notebook-servidor, y en el futuro una en Santa Cruz). El protocolo que las mantiene con la misma identidad y se pasan trabajo se llama **ENLACE** y vive en `enlace\` de este repo (`enlace\README.md` = qué es; `enlace\PROTOCOLO.md` = el contrato). Toda sesión nueva, después del `git pull`, debe:
1. Mirar **`enlace\maquinas\*.estado.json`** para saber qué máquinas existen y cuáles están despiertas (viva = `ultima_vez_viva` de menos de ~10 min). Sirve para delegar trabajo pesado a la que esté prendida en vez de hacerlo acá.
2. Mirar **`enlace\buzon\pendiente\`**: si hay archivos, son pedidos que Matías dejó desde el celular o desde otra máquina y todavía nadie atendió. Avisarle. La servidora los ejecuta sola con `enlace\atender_buzon.ps1`, pero si estás en la máquina que corresponde y el pedido es para ahora, atendelo (mové el `.md` por `haciendo\` → `hecho\` anexando el resultado, como dice el PROTOCOLO).
3. Si tocaste `~/.claude/` (doctrina, un agente, settings o memoria), cerrá con **`.\enlace\sync.ps1 -Push`** para que las otras máquinas lo hereden. Al arrancar, `.\enlace\sync.ps1 -Estado` dice si esta máquina quedó desfasada.

## Designación EN PARALELO (regla de esta carpeta)
Cuando Matías pide algo que toca varios dominios — o pide explícitamente "en paralelo" — **lanzar TODOS los agentes que hagan falta como subagentes simultáneos** (tool Agent, múltiples invocaciones en un mismo mensaje), cada uno con: su tarea concreta, la ruta del repo donde trabaja (ver MAPA_PROYECTOS.md), su DoD, y la orden de actualizar su bitácora en `dominios\<nombre>.md`. Tipos disponibles: `energia`, `comms`, `muestreador`, `hardware`, `firmware`, `utn`, `comercial`, `verificador` (definiciones en `~/.claude/agents/`, backup en `agentes\`). El Director consolida los resultados y actualiza PORTFOLIO.

- Trabajo independiente → paralelo SIEMPRE (no serializar lo que no depende entre sí).
- Trabajo dependiente → secuencia explícita (A termina, evidencia, arranca B).
- Todo cierre importante pasa por `@verificador` antes de declararse hecho.

## Al cerrar la sesión
Actualizar PORTFOLIO (bitácora del Director) + bitácoras de dominios tocados + `git add -A && git commit && git push` (repo: github.com/matialegre/vida).
