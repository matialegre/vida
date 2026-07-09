# Dominio: frontend (agente @frontend)

Doc de dominio + bitacora. El agente lo lee al arrancar y lo actualiza al cerrar. Backlog inicial: ver seccion "Tu backlog inicial" en ~/.claude/agents/frontend.md (copia en ../agentes/frontend.md).

## Bitacora
- 2026-07-07 - Agente creado por Claude Fable con backlog real de los repos migrados (C:/Proyectos).

- 2026-07-08 [BRIEFING GIMAP] — leer ../BRIEFING_EQUIPO_GIMAP.md y los 4 docs (PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO). Para vos: LAB streamea 1kHz a la PC (no nube); receptor sirve dashboard local en su AP (192.168.4.1) + cloud; mostrar edad del dato, batería, RSSI, A vs B.

## 🔵 TypeScript 7.0 salió (nota 2026-07-09, para el próximo agente)
Microsoft lanzó TS 7 = rewrite nativo en Go ("tsgo"): **8-12x más rápido** (VSCode 125s→10.6s; abrir archivo con errores en editor 17.5s→1.3s), 18-26% menos memoria. Anuncio: https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/
- **El ERP NO se toca** (es JSX/JavaScript puro por regla dura — TS7 no aplica).
- **SÍ sirve** para los dashboards TypeScript/Vite: `datalogger/vercel-dashboard`, `galgas/web`, `frioseguro/web-dashboard` → builds más rápidos.
- ⚠️ **Breaking changes fuertes** (`strict:true` default, adiós CommonJS, `types:[]` default) → NO instalar en proyecto que ande sin plan. Migrar gradual con el paquete `@typescript/typescript6` (side-by-side). Probar primero en proyecto nuevo/de juguete, no en producción.
- Instalación: `npm install -D typescript`. Evaluar cuando haya tiempo, no urgente.
