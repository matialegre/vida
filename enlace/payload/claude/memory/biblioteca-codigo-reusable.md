---
name: biblioteca-codigo-reusable
description: REGLA PERMANENTE - todo código nuevo chequea primero C:\Proyectos\biblioteca; todo código probado se cosecha ahí vía @bibliotecario
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3c2ffe10-96cb-49dc-a097-78e5ec79d3b8
  modified: 2026-08-21T17:58:29.464Z
---

Matías estableció (2026-08-21) que la forma de laburar de ahora en más es con
**librerías reutilizables**: existe el agente `@bibliotecario` (definición en
`~/.claude/agents/bibliotecario.md`) y el repo `C:\Proyectos\biblioteca`
(micropython\ / esp32\ / pc\ / protocolos\, catálogo en LEEME.md).

**Why:** en una sola conversación se generan 30+ códigos (firmware hasta
sistemas); sin biblioteca se reescribe lo mismo (OTA, WiFi+AP, UDP broadcast,
batería Pico, buscar micro por serial) y se re-pisan las mismas minas
(ej. VSYS/ADC29 vs WiFi en Pico 2 W).

**How to apply:** antes de escribir código nuevo, chequear el catálogo
`C:\Proyectos\biblioteca\LEEME.md` (cadena: ¿hace falta? → stdlib → nativo →
dependencia → biblioteca → recién ahí código nuevo). Cuando un módulo queda
probado en su proyecto, lanzar `@bibliotecario` para cosecharlo con su FICHA
(ORIGEN/PROBADO/USO/DEPENDE/GOTCHAS). "PROBADO" exige evidencia real; las
adaptaciones se marcan "solo sintaxis". Incluir esta directiva en los prompts
de los subagentes que escriben código. Relacionado: [[pcb-placement-con-criterio]]
