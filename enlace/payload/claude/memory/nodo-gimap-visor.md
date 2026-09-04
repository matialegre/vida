---
name: nodo-gimap-visor
description: "Dónde vive el firmware que muestra giroscopio y piezos en vivo, por qué no está en main, y las tres trampas que impiden arrancarlo"
metadata: 
  node_type: memory
  type: project
  originSessionId: de2b697f-5084-4f7c-90b0-1c562a8239e5
  modified: 2026-09-04T02:27:55.947Z
---

El firmware que muestra **giroscopio + 2 canales de piezo en vivo en el navegador**
NO es el que documenta el README del repo `datalogger`, ni el de misiones
(`firmwares/pico2w-node/`, que no tiene canal piezo ni vista en vivo de señal).

Es **`nodo-gimap`**, y vive en el branch **sin mergear**
`nodo-gimap/wifi-y-flasheo-2026-08-24` del repo `C:\Proyectos\datalogger`.
Desde el 2026-09-03 está montado como worktree en **`C:\Proyectos\datalogger-gimap`**
(el repo principal quedó parado en otro branch nocturno con trabajo sin commitear —
por eso worktree y no checkout).

**Qué es:** Pico 2 W + MPU6050 + 2 piezos por GP26/GP27, 200 Hz, UDP broadcast
(50507 datos / 50508 estado). En la PC, `visor_gimap.py` levanta `127.0.0.1:8080`
con 4 gráficos en vivo. Sólo stdlib — regla del proyecto, no meter flask.
Punto de entrada: `ARRANCAR_GIMAP.bat`; guía: `MANANA.md`.

**Why:** el repo tiene ~30 branches nocturnos sin mergear y dos firmwares distintos
para el mismo hardware. Buscar "el datalogger del GIMAP" sin esto lleva al firmware
equivocado y a concluir que hay que escribir un visor que ya existe.

**How to apply:** ante cualquier pedido de "ver las señales del nodo GIMAP", ir al
worktree, no a `main`. Y verificar el branch antes de flashear.

## Las tres trampas (verificadas el 2026-09-03)

1. **`wifi.json` gana sobre `secrets.py`** (`red.py:64`) y no lo borra nadie. Lo que
   se carga desde el AP de rescate queda pegado: reconfigurar desde la PC y
   reflashear no cambia la red. El flasheo ahora lo borra si hay `secrets.py`, pero
   un nodo actualizado por OTA sigue expuesto. **Deuda viva.**
2. **En modo AP el nodo NO mide ni transmite** (`main.py:132-135`): `red.modo_ap()`
   no retorna, sólo sirve la página para elegir red. El nodo tiene que entrar a una
   red real, y la PC estar en la misma (el broadcast no cruza subredes). Pico 2 W es
   **sólo 2,4 GHz**.
3. **El piezo mide sucio por hardware**, no por software: 50 Hz de red (entrada
   flotando en GP27) y ganancia del MCP6004 fuera de rango. Objetivo ~1,65 V en
   reposo, se ajusta con el preset mirando `ajustar_ganancia.py` (los valores crudos
   NO se ven en el visor).

Regla que salió de acá y aplica a todo visor: una ventana vieja dibujada como si
fuera de ahora es una mentira — ver [[visor-sin-datos-no-miente]].
