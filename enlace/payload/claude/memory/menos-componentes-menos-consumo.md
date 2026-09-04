---
name: menos-componentes-menos-consumo
description: "Doctrina de Matías para sus nodos a pila — cada componente tiene que justificarse por consumo o por falla evitada; el que no, sale"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: dd9e8ccc-c0fe-44c5-9ad5-cc4d9a676d23
  modified: 2026-09-03T22:20:29.522Z
---

Regla de Matías (2026-09-03, rediseñando el nodo de galga de Dreyfus): **"mientras menos tenga, menor consumo, y mejor todo."** Vio "muchos transistores" y pidió justificar cada uno. Pidió que lo recuerde explícitamente.

**Why:** los nodos van a pila (LiSOCl2, meta > 1 año). Cada componente es consumo, es fuga, es una soldadura más para armar a mano y un modo de falla más en planta. Matías prefiere un jumper manual a un transistor que "hace todo solo" si el transistor no paga su lugar en microamperes.

**How to apply:** en cualquier esquemático de sus nodos a pila (galgas/Dreyfus, RuView, FrioSeguro a pila, cosechador), cada pieza tiene que poder decir **cuánto consume o qué falla evita, en una línea con número**. La que no puede decir ninguna de las dos, sale. Protecciones "por las dudas" (clamps, TVS, redundancias) se sacan salvo que haya un número de fuga o un modo de falla concreto que las justifique. Preferir jumper/selección manual sobre automatismo cuando el automatismo cuesta reposo. Relacionado: [[ota-nunca-ladrillo]], [[pcb-placement-con-criterio]].
