# Dominio: TENDENCIAS (agente @tendencias)

Scout semanal de novedades IA/tech filtradas por utilidad real para los proyectos de Matías (FrioSeguro, ERP Modulia, datalogger octubre, workflow Claude Code). Definición completa: `~/.claude/agents/tendencias.md`. Reportes en `tendencias\AAAA-MM-DD.md`.

## Doctrina operativa
- Filtro único: ¿Matías lo usa en 30 días en un proyecto suyo? Si no, una línea o nada.
- Máx 5-7 ítems por reporte + 1 recomendación única. Todo repo se verifica vivo antes de recomendar.
- Registrar fuentes miradas para que la corrida siguiente no repita.
- Amenaza directa a un proyecto (ej: FrioSeguro open-source ajeno) → escalar URGENTE al Director.
- Frecuencia: domingos, antes de la revisión semanal.

## Estado del radar
- **Pendiente de re-chequeo:** spec final MCP (~28-jul: stateless, Tasks, MCP Apps) · promo Sonnet 5 vence 31-ago · posible launch week Supabase.
- **Vigilancia permanente:** competencia cold-chain low-cost (hoy: sin amenaza), releases Claude Code, Espressif (chips CES sin disponibilidad aún).

## Bitácora
- **2026-07-13 — Primera corrida.** Reporte: `tendencias\2026-07-13.md`. 6 hallazgos; top 3: (1) Sonnet 5 default en Claude Code con 1M ctx y promo $2/$10 hasta 31-ago → migrar agentes del ERP YA; (2) Claude Code 2.1.198-207: subagentes background por defecto + `/checkup` para limpiar MCP/skills muertos; (3) `ant` CLI oficial de Anthropic → 37 agentes del ERP como YAML versionado. Además: aviso TS 5.0 de supabase-js (mantenimiento dashboard FrioSeguro) y barrida de competencia cold-chain SIN amenaza. Recomendación única: Sonnet 5 en ERP + `/checkup` (<1h, plata directa). **Próximo paso:** corrida dom 19-jul; abrir con los re-chequeos del radar.
