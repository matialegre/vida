---
name: visor-sin-datos-no-miente
description: "Regla de diseño para todo dashboard de Matías - sin datos frescos hay que vaciar la pantalla, no dejar la última ventana dibujada"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: de2b697f-5084-4f7c-90b0-1c562a8239e5
  modified: 2026-09-04T02:28:45.010Z
---

**Un dashboard que deja de recibir datos NO puede seguir dibujando la última ventana.**
Tiene que vaciarse y decir que no hay dato, distinguiendo "nunca llegó nada" de "se
cortó hace X". Y siempre tiene que mostrar **de qué fuente** viene lo que se ve.

**Why:** el repo `datalogger` ya se quemó dos veces con la misma clase de error.
Primero con un `sim_data` que venía en `True` por defecto e **inventaba** lecturas del
MPU: se veía señal moviéndose y el hardware podía estar muerto. Después con
`visor_gimap.py`, que al cortarse el nodo dejaba los 4 gráficos y los chips (uptime,
seq, batería) congelados con la última ventana recibida — lo único que cambiaba era un
texto rojo chico. Las dos veces el síntoma es el mismo y es el peor posible en
instrumentación: **una pantalla convincente de un sistema que no está funcionando**.
Choca de frente con la doctrina de "evidencia o no pasó": si la pantalla no distingue
dato fresco de dato viejo, no es evidencia de nada.

**How to apply:** al construir o revisar cualquier visor, panel o dashboard (galgas,
FrioSeguro, datalogger, los de Vercel/Netlify), verificar SIEMPRE los tres estados, no
sólo el feliz: (a) con datos llegando, (b) la fuente se corta a mitad, (c) nunca llegó
nada. El arreglo va del lado del server cuando se puede — no entregar la ventana vieja
es más robusto que pedirle al JS que se acuerde de no dibujarla. Y si existe un
generador de datos de prueba, que sea imposible confundirlo con la fuente real (nombre
explícito, banner, marca visible en pantalla).

Caso concreto y trampas del hardware: [[nodo-gimap-visor]].
