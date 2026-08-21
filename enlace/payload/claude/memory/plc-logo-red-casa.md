---
name: plc-logo-red-casa
description: Los PLC LOGO! de casa - sus IP/MAC reales y la trampa de subredes que los hace invisibles a un barrido normal
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c2ffe10-96cb-49dc-a097-78e5ec79d3b8
  modified: 2026-08-07T12:58:59.903Z
---

Los tres equipos Siemens del kit UTN-BHI en casa de Matías, **verificados el 2026-08-07**:

| Equipo | IP | MAC | Estado |
|---|---|---|---|
| LOGO! #1 (0BA7, `6ED1 052-1MD00`) | 192.168.0.2 | `00-1C-06-26-AD-4C` | puerto 102 abierto |
| LOGO! #2 (0BA8, `6ED1 052-1HB08`) | 192.168.0.3 | `E0-DC-A0-32-EC-1B` | puerto 102 + **servidor web HTTP 200** |
| LOGO! TDE | 192.168.0.4 | `E0-DC-A0-F3-A1-79` | web abierta |

Gateway configurado en los equipos: `192.168.0.0` — **inválido** (es la dirección de red). En la
práctica funcionan sin gateway: solo hablan dentro de 192.168.0.x. Hay que corregirlo a
`192.168.0.1` antes de intentar acceso remoto.

**⚠️ LA TRAMPA que costó una tarde entera:** el router TP-LINK (TL-WR740N v4) está en **modo
router**, sirviendo DHCP en `192.168.1.x`. Los tres LOGO están enchufados a sus **puertos LAN** pero
con IP **estática 192.168.0.x**. O sea: mismo segmento físico (mismo switch), subredes lógicas
distintas. Resultado — un barrido ARP/ping desde una PC con IP DHCP `192.168.1.x` **no los ve**, y
la lista de clientes DHCP del router tampoco los muestra (no piden DHCP). Parecen apagados y no lo
están.

**Cómo se destrabó:** desde PowerShell **como administrador** en la notebook —
`netsh interface ip add address "Ethernet" 192.168.0.6 255.255.255.0` — y ahí aparecieron los tres
por ARP directo. Claude Code **no se puede auto-elevar**: la terminal tiene que abrirse como
administrador ANTES de lanzarlo.

**El síntoma que delata que están vivos:** el LED del puerto Ethernet del LOGO titila. Si titila,
hay alimentación y enlace — el problema es de direccionamiento, no de hardware.

**Why:** dos barridos completos dieron "no hay ningún LOGO en la red" y la conclusión fue
"están sin alimentación". Era falso negativo: un barrido solo encuentra lo que responde en SU
subred. Ausencia de evidencia no es evidencia de ausencia.

**How to apply:** ante cualquier equipo industrial "que no aparece", antes de suponer que está
apagado: mirar el LED del puerto, y verificar en qué subred está parado el que barre.
Ver también [[una-sola-fuente-de-verdad-eda]] — mismo patrón de confiar en una herramienta sin
entender qué mide.
