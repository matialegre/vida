---
name: juegos-del-viaje
description: "App Android \"Juegos del Viaje\" (C:\\Proyectos\\batalla-naval-lan) — suite de juegos offline multijugador para el auto"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c2ffe10-96cb-49dc-a097-78e5ec79d3b8
---

Proyecto personal de Matías para viajar en auto con [[familia-aldi-ainho]]. Repo: `C:\Proyectos\batalla-naval-lan` (una sola APK, `bash build.sh` compila y firma; toolchain propia en `C:\Proyectos\android-toolchain`, sin Android Studio).

**Arquitectura**: WebView + assets HTML autocontenidos; puente JS nativo `BN` (batalla naval TCP/UDP); **servidor web embebido puerto 8080** en la app ("🌐 Compartir") que sirve los juegos a cualquier navegador de la red (iPhone incluido) y tiene **relay WebSocket `/ws`** con salas (JOIN/ID/JOINED/BYE + broadcast con id prefijado) para multijugador lockstep con seed determinista (mulberry32). Host = id más chico.

**Cómo se juega**: celu de Matías da hotspot → tablet/iPhone entran a `http://IP:8080` por navegador. En PC: `pc/pc_bridge.py` (:8010 batalla) y `pc/test_relay.py` (:8080, gemelo python del relay para testear multi con pestañas).

**Why**: en el auto no hay internet — todo offline. **How to apply**: juegos nuevos = un HTML en `assets/` + tarjeta en `index.html` + subir versionCode + `bash build.sh`; multijugador copiando la clase `Sala` de `carrera.html`; personajes fijos 1=Ainho👧 2=Mati🧔 3=Aldi👩.
