---
name: pcb-placement-con-criterio
description: Matías rechazó un PCB con DRC 0 porque el placement no tenía criterio — pasar el DRC no es hacer una placa
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3c2ffe10-96cb-49dc-a097-78e5ec79d3b8
---

Un PCB con **DRC 0 puede ser un espanto igual**. Matías rechazó `interfaz_laser_dremel` (2026-07-30)
con estas palabras: *"un espanto la posición de los componentes, no tenés ningún tipo de concepto
ni criterio"*. Y tenía razón: los componentes estaban repartidos en una grilla uniforme, con el
único criterio de que no se solaparan los courtyards.

**Why:** verificar solapes y DRC es verificar que la placa sea *fabricable*, no que sea *buena*.
Un buen placement se juzga por: componentes de un mismo bloque funcional AGRUPADOS y cerca, flujo
de señal claro (entrada → proceso → salida), pistas cortas entre componentes conectados, y
capacitores de desacople pegados al pin que desacoplan. Optimizar para que el DRC pase es
exactamente el error de "generator ≠ evaluator" aplicado a hardware.

**How to apply:** antes de colocar un solo componente, agrupar por bloque funcional y ubicar
primero lo que tiene posición forzada (conectores en los bordes, componentes con requisito
mecánico). Después los ICs de cada bloque, y los pasivos PEGADOS a su IC. Recién al final verificar
solapes. Y mirar el render preguntándose "¿un revisor con experiencia diría que esto está bien
pensado?", no solo "¿el DRC pasa?".

La doctrina completa está en `C:\Proyectos\laser-pcb\docs\DOCTRINA_PCB.md` y
`DOCTRINA_ESQUEMATICO.md`, y se incorporó a los agentes [[agentes-pcb-y-esquematico]].
