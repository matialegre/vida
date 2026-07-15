# LOGO! en casa — programar + acceso LAN/WiFi/Internet (anotado 2026-07-14)

Matías se trajo a casa el/los kit(s) de LOGO! (panel de entrenamiento UTN-BHI, rótulo "Sistemas de Control Industrial · Acosta Demis, Leonhardt Federico"). Quiere: **programar los 2 LOGO! y poder meterse por LAN / por WiFi / por internet** vía el router TP-LINK.

## Hardware identificado (de las fotos)
| Equipo | Modelo exacto | Notas |
|---|---|---|
| Fuente | **Siemens LOGO!Power 6EP1332-1SH52** | 100-240 Vca → 24 Vcc. Alimenta ambos LOGO |
| Protección | SASSIN 3SB1-63 C16 2P | térmica de entrada |
| **LOGO! #1 (base)** | **LOGO! 12/24RCE — 6ED1 052-1MD00-0BA7** | Generación **0BA7**. 8 DI (I1/I2 e I7/I8 usables como AI 0-10V), 4 salidas relé 10A. Con Ethernet RJ45 |
| Módulo exp. | **DM8 12/24R — 6ED1 055-1MB00-0BA1** | +4 DI / +4 DO relé 5A |
| Módulo exp. | **AM2 RTD — 6ED1 055-1MD00-0BA1** | +2 entradas RTD (PT100/PT1000) |
| **LOGO! #2 (base)** | **LOGO! 24RCE — 6ED1 052-1HB08-0BA0** | Generación **0BA8** (la nueva). MAC E0-DC-A0-32-EC-1B. Con Ethernet + **servidor web integrado** |
| Display | **LOGO! TDE** (Text Display Ethernet) | pantalla externa del 0BA8 |
| Router | **TP-LINK** (single antena, 2.4 GHz — TL-WR74x) | el "router" para LAN/WiFi |
| Panel | Tablero UTN: 12 switches (I1-I12), 2 pots (AI1/AI2), 8 luces (Q1-Q8) | simula entradas/salidas |

⚠️ **Los dos LOGO son de generación distinta (0BA7 vs 0BA8)** — importa para la versión de software y el servidor web (el 0BA8 tiene web server completo; el 0BA7 es más limitado).

## Lo que se NECESITA — checklist

### A) Software (en la PC)
- [ ] **LOGO!Soft Comfort V8.3** (última). Programa AMBAS generaciones. Es pago pero hay **demo** que programa y simula; la transferencia al PLC requiere la licencia (verificar si Matías ya la tiene / si está en la PC del labo). Descarga: siemens.com (SIOS).
- [ ] (Opcional monitoreo) app **LOGO! App** (Android/iOS) para ver/operar desde el celu por WiFi.

### B) Red — direcciones IP (lo primero a definir)
- [ ] Entrar al TP-LINK (típico `192.168.0.1` o `192.168.1.1`, admin/admin) → anotar su subred y clave WiFi.
- [ ] Asignar **IP fija a cada LOGO** dentro de esa subred, distintas entre sí. Ej. si el router es `192.168.0.1`:
      - LOGO #1 (0BA7): `192.168.0.10`
      - LOGO #2 (0BA8): `192.168.0.11`
      - máscara `255.255.255.0`, gateway = IP del router
- [ ] La IP del LOGO se setea desde el propio LOGO (menú Network) o desde LOGO!Soft (Tools → Ethernet Connections).
- [ ] Cablear: PC y ambos LOGO al router por Ethernet (el router da también el WiFi).

### C) Programar (por LAN)
- [ ] En LOGO!Soft: elegir el modelo correcto por generación (0BA7 para el #1, 0BA8 para el #2 — NO se puede mezclar en un mismo programa).
- [ ] Diagrama de bloques FBD → Tools → Transfer → PC→LOGO, apuntando a la IP de cada uno.
- [ ] Probar con el panel UTN (switches = entradas, luces = salidas).

### D) Acceso por WiFi (misma red)
- [ ] Cualquier PC/celu conectado al WiFi del TP-LINK está en la misma subred → llega a los LOGO.
- [ ] **LOGO #2 (0BA8): servidor web integrado** → habilitarlo en LOGO!Soft (Online Settings → Web Server, poner usuario/clave) → abrir `http://192.168.0.11` desde el navegador del celu/PC en WiFi. Se ve y opera sin instalar nada.
- [ ] LOGO #1 (0BA7): web server más limitado; si no alcanza, se monitorea con LOGO!Soft en modo online o la app.

### E) Acceso por INTERNET (lo más delicado — SEGURIDAD)
Dos caminos:
1. **Port forwarding en el TP-LINK** (rápido, INSEGURO): redirigir un puerto externo → IP:80 del LOGO 0BA8. Queda el LOGO expuesto en internet → **solo con clave fuerte en el web server y, idealmente, puerto no estándar**. No recomendado a largo plazo.
2. **Túnel/VPN (recomendado)**: WireGuard/Tailscale en una PC de la red, o reverse-tunnel a través del server propio de Mundo Outdoor (IP fija). Te metés a la red como si estuvieras ahí, sin exponer el LOGO. Más seguro y es la jugada "Ponytail" (usar infra que ya existe).
- [ ] Definir cuál. Para demo rápida: port forwarding con clave. Para algo estable: túnel.
- [ ] Averiguar si el TP-LINK tiene IP pública o está detrás de NAT del ISP (si es NAT de carrier, port forwarding NO sirve → sí o sí túnel).

## 🎓 CONVERGENCIA (importante para el Director)
Este es el **kit de LOGO! del laboratorio de SCI**. Tenerlo en casa **desbloquea las secciones D y E del TP de Sistemas de Control Industrial SIN depender del labo**: programar las lógicas digitales y analógicas en LOGO!Soft, cargarlas al PLC físico y grabar evidencia (video/fotos del panel andando) — que era justo lo que el checklist mandaba "hacer en el laboratorio con la cátedra". Un solo esfuerzo = TP avanzado + este pedido resuelto.

## Próximo paso
1. Matías entra al TP-LINK y pasa: subred, clave WiFi, y si tiene o no IP pública.
2. Confirmar si LOGO!Soft Comfort está instalado (o instalar la demo).
3. Definir qué lógica programar primero (¿la del TP de SCI? ¿otra para GIMAP?).

## ✅ 2026-07-14 — LOGO CONECTADO AL PLC (hecho por el Director vía GUI automation)
Matías se fue a dormir la siesta y pidió verlo conectado al volver. LOGRADO.

**Cómo se hizo (el camino que SÍ funciona):**
1. LOGO!Soft Comfort V8.0.0 **COMPLETO** (no demo — verificado en Ayuda→Acerca de; instalado en `C:\Program Files\Siemens\LOGOComfort_V8`).
2. Pestaña **"Proyecto de red"** (NO "Modo de diagrama").
3. **Agregar nuevo dispositivo** → seleccionar **LOGO! 0BA7** (el modelo físico real; el software venía en 0BA8 por defecto) → IP **192.168.0.2** (autocompletada) → Aceptar.
4. **Establecer conexión online** → enlace establecido: tilde verde ✔, cable verde PC↔LOGO, puerto Ethernet verde.

**Aprendizajes:**
- "Determinar LOGO!" (F2) NO es conectar — es análisis offline de recursos. El connect real es "Proyecto de red → Establecer conexión online".
- El sondeo COTP crudo por socket reseteaba porque no usaba el perfil de conexión correcto del 0BA7; LOGO!Soft nativo conecta bien.
- PLC físico = LOGO! 0BA7 (12/24RCE), MAC 00-1C-06-26-AD-4C, IP 192.168.0.2.
- Evidencia: `Desktop\LOGO_CONECTADO_2026-07-14.png`.

**PRÓXIMO PASO (con Matías despierto):** leer el programa del PLC (LOGO!→PC / online) como BACKUP antes de tocar nada; después programar y/o prender el web server para acceso por WiFi/celular.

## 🔍 2026-07-14 (2) — Identificación + intento de bajar el programa
Matías pidió bajar el programa del PLC. Hallazgos DEFINITIVOS (vía Config online):
- **Comunicación TOTAL confirmada**: se leyó la versión de firmware EN VIVO del dispositivo.
- **Modelo real: LOGO! 0BA7.ES4 · firmware V1.03.37** (variante "Economy" — NO el 0BA7.Standard). Esto explica el diálogo "el tipo de dispositivo es diferente del conectado" que aparecía al leer (yo lo había agregado como 0BA7 genérico=Standard).
- **NO tiene contraseña**: se leyó versión/config sin ningún prompt de password.
- **Estado: Modo normal** (standalone, no esclavo de red).
- **La lectura del programa (LOGO!→PC) volvió VACÍA** tras aceptar la sustitución de tipo. Interpretación más probable: **el LOGO de entrenamiento no tiene programa de usuario cargado** (kit UTN, seguramente borrado entre usos). Alternativa: la lectura necesita el proyecto tipado EXACTO como 0BA7.ES4 (el add del proyecto de red ofrece 0BA7 genérico).

**Para bajar el programa limpio (si existe)**: Archivo→Nuevo eligiendo modelo **0BA7.ES4**, luego Herramientas→Transferir→LOGO!→PC (sin mismatch). Si vuelve vacío → confirmado: no hay programa, se puede programar libremente.
- Evidencia: `Desktop\LOGO_0BA7-ES4_identificado.png`.
