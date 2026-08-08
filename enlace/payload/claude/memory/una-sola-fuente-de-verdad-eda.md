---
name: una-sola-fuente-de-verdad-eda
description: "En KiCad generado por scripts, todo dato duplicado a mano (netlist, valores, keepouts, anchos) se desincroniza y el DRC no lo ve"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3c2ffe10-96cb-49dc-a097-78e5ec79d3b8
---

En el PCB `interfaz_laser_dremel` (2026-07-30) **todos** los defectos graves fueron el mismo bug:
un dato escrito a mano en un script, duplicando algo que ya vivía en otro lado. Ninguno lo vio el
DRC — la placa daba **DRC 0 estando eléctricamente muerta**.

- El **netlist** estaba tipeado en `gen_pcb_interfaz.py`, sin relación con el `.kicad_sch`. Tenía
  el emisor de los optos a GND y los pines 1/2/4 de K1 cambiados. Yo se lo atribuí al esquemático;
  el esquemático estaba bien desde la rev A. **La placa se habría fabricado muerta.**
- Los **valores** también: R6 había pasado de 1k a 2k2 y el PCB seguía rotulando 1k.
- Los **keepouts de aislación** estaban en coordenadas de un placement viejo → el plano de masa
  pasaba por debajo de los dos optos.
- Los **anchos de pista**: al regenerar desde el netlist, `MOT_P` pasó a llamarse `Net-(D2-K)`, la
  netclase POTENCIA dejó de enganchar nada y **las pistas de 6 A volvieron a 1 mm en silencio**.

**Why:** el DRC verifica que la placa sea *fabricable*, no que sea *correcta*. Ninguna de estas
cosas produce una violación. Un dato duplicado no está "duplicado": está esperando divergir, y
cuando diverge nadie se entera.

**How to apply:** derivar, nunca copiar. Conexiones y valores → del `.net` exportado del
esquemático. Keepouts y franjas → de la posición real de los pads (ojo: las coordenadas de un
footprint son su ORIGEN, que en un DIP-4 cae sobre el pin 1, no el centro). Borde → de los
courtyards. Netclases → de los PADS que llevan la corriente, no del nombre de la net.
Y donde no se pueda derivar, poner un **guardia que aborte**: si una netclase no engancha ninguna
net, cortar antes de rutear potencia con pistas de señal.

Corolario: cada chequeo nuevo tiene que **autovalidarse y tener control negativo**, o miente. Dos
de mis chequeos daban falsos positivos y casi les creo; el comparador de netlist se probó
saboteando la placa a propósito. Ver [[pcb-placement-con-criterio]].
