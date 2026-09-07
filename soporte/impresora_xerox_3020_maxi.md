# Impresora Xerox Phaser 3020 — PC de Maxi (resuelto 2026-09-07)

**Síntoma**: andaba por red y a los pocos días dejó de imprimir. Estado `Error` en
Windows, sin más explicación.

**Causa real**: **el perfil de Wi-Fi guardado se corrompió** — en la impresora y,
por separado, también en la PC. Misma red, misma clave, 87 % de señal: lo que
falló fue la configuración guardada, no la red. No era el driver ni la IP.

**Solución final**: **imprime por Wi-Fi**, con la IP fija `192.168.100.100`
(puerto `IP_192.168.100.100`) **y el cable USB dejado puesto como respaldo**
(`USB001`). Quedó mejor que antes del problema, porque antes el puerto iba por
NOMBRE y ahora va por IP.

**El orden que funcionó**: (1) USB para que imprimiera ya y para confirmar que la
impresora estaba sana; (2) arreglar el Wi-Fi de la PC borrando y recreando su
perfil; (3) recargarle la red a la impresora con el asistente, por USB.

---

## Datos del equipo

| | |
|---|---|
| Modelo | Xerox Phaser 3020 (**solo Wi-Fi 2,4 GHz**, no tiene puerto de red) |
| MAC | `E8:4D:EC:28:5A:2A` |
| Nombre de red | `XRXE84DEC285A2A` (es `XRX` + la MAC, convención Xerox) |
| Driver | `Xerox_Phaser_3020_Windows_Print_Drivers_Utilities_V1.07` |
| Red del lugar | `192.168.100.x`, gateway `192.168.100.1` — **módem de BVC, sin router propio** |
| **Wi-Fi** | SSID **`BVNET-99aa`** · clave **`C80F709D`** (de fábrica) · WPA2-Personal/CCMP · 2,4 GHz canal 9 · 87 % de señal · BSSID `f0:63:f9:31:99:b0` |
| IP reservada | `192.168.100.100` — **VERIFICADA el 2026-09-07**: la impresora la tomó y el `arp -a` devolvió su MAC. BVC la hizo bien |
| Puerto en Windows | `IP_192.168.100.100` (por IP, no por nombre) + `USB001` de respaldo |
| Servicios abiertos | **9100** (RAW) · **631 (IPP)** · **80** (panel web, `http://192.168.100.100`) |
| Impresión desde celular | **SÍ, funciona** — el 631 está abierto y el cliente ya imprimía así antes. *(Yo había afirmado lo contrario de memoria; Matías lo desmintió con la experiencia del cliente y el `Test-NetConnection` le dio la razón. No afirmar capacidades de un modelo sin medirlas: un `Test-NetConnection` al 631 lo contesta en dos segundos.)* |
| PC | usuario `Maxi`, Windows 11, **Windows PowerShell 5.1** (no 7) |

**El SSID se dedujo de la MAC del gateway**: gateway `f0-63-f9-31-**99-aa**` →
red `BVNET-**99aa**`. Sirvió para descartar las otras cuatro redes `BVNET-0F8F-*`
que se veían en el lugar (son de otro equipo, probablemente el de las cámaras):
meter la impresora ahí la habría dejado en otra red, sin ver a la PC.

**No tienen usuario ni contraseña del módem**: cualquier cambio de red hay que
pedírselo a BVC. Esa es la limitación de fondo del lugar.

## Cómo se diagnosticó (el orden que sirvió)

```powershell
# 1. A qué apunta el puerto -> era un NOMBRE, no una IP
Get-Printer | Format-Table Name, PortName, DriverName, PrinterStatus -Auto
Get-PrinterPort | Where-Object PrinterHostAddress | Format-Table Name, PrinterHostAddress, PortNumber -Auto

# 2. En qué red está la PC
Get-NetIPConfiguration | Where-Object IPv4Address | Format-Table InterfaceAlias, @{n='IP';e={$_.IPv4Address.IPAddress}}, @{n='Gateway';e={$_.IPv4DefaultGateway.NextHop}} -Auto

# 3. Barrido de la subred (versión para PowerShell 5.1: -Parallel NO existe ahí)
$t = 1..254 | ForEach-Object { (New-Object System.Net.NetworkInformation.Ping).SendPingAsync("192.168.100.$_", 500) }
[Threading.Tasks.Task]::WaitAll($t)
$t | Where-Object { $_.Result.Status -eq 'Success' } | ForEach-Object { $_.Result.Address.ToString() }

# 4. ¿Está el cable USB puesto AHORA? (-PresentOnly = solo hardware conectado)
Get-PnpDevice -Class Printer,USB -PresentOnly | Where-Object FriendlyName -match "Xerox|Phaser" | Format-Table FriendlyName, Status -Auto
```

## El arreglo

```powershell
# PowerShell COMO ADMINISTRADOR
Get-PrintJob -PrinterName "Xerox Phaser 3020" | Remove-PrintJob    # vaciar la cola vieja
Set-Printer -Name "Xerox Phaser 3020" -PortName "USB001"
Get-Printer -Name "Xerox Phaser 3020" | Format-Table Name, PortName, PrinterStatus -Auto
Invoke-CimMethod -InputObject (Get-CimInstance Win32_Printer -Filter "Name='Xerox Phaser 3020'") -MethodName PrintTestPage
```

Estado pasó de `Error` a `Normal` y la página de prueba salió. **Confirmado en
papel por el cliente**, no solo por el `ReturnValue 0`.

### Paso 2 — el Wi-Fi de la PC (era un problema aparte, apareció en el camino)

La PC tampoco se conectaba a `BVNET-99aa`: la mostraba con una **X** en la lista.
Misma clave de siempre, 87 % de señal. **El perfil guardado estaba corrupto.** Se
arregló borrándolo y recreándolo:

```powershell
netsh wlan show networks mode=bssid | Select-String "BVNET-99aa" -Context 0,8   # señal y seguridad reales
netsh wlan delete profile name="BVNET-99aa"
# recrear por XML con la clave (ver el bloque completo en el historial) y:
netsh wlan connect name="BVNET-99aa"
```

**Hacerlo con red de seguridad**: se entró a la PC por el hotspot del celular del
cliente, se guardó ese SSID antes de tocar nada y el script volvía solo si en 20
segundos no conectaba. Sin eso, un intento fallido deja la máquina inaccesible.

### Paso 3 — el Wi-Fi de la impresora

Con la impresora **conectada por USB**, el asistente del paquete V1.07 →
**Conexión de red inalámbrica** → red `BVNET-99aa` → clave `C80F709D`. Al llegar a
"Configuración de red inalámbrica completa" pide desconectar el USB: se
desconecta y **se cancela el resto del asistente** (el driver ya estaba
instalado; seguir solo agrega puertos duplicados).

```powershell
# verificación: la impresora tomó .100 y el puerto pasa a ir por IP
Test-NetConnection 192.168.100.100 -Port 9100        # TcpTestSucceeded : True
arp -a | Select-String "e8-4d-ec"                     # 192.168.100.100  e8-4d-ec-28-5a-2a
Add-PrinterPort -Name "IP_192.168.100.100" -PrinterHostAddress "192.168.100.100"
Set-Printer -Name "Xerox Phaser 3020" -PortName "IP_192.168.100.100"
# y limpiar los duplicados, incluido el (2) que crea el asistente al pasar por acá
Remove-PrinterPort -Name "XRXE84DEC285A2A"
Remove-PrinterPort -Name "XRXE84DEC285A2A(0)"
Remove-PrinterPort -Name "XRXE84DEC285A2A(1)"
Remove-PrinterPort -Name "XRXE84DEC285A2A(2)"
```

Quedaron solo `IP_192.168.100.100` y `USB001`. **Papel confirmado.**

## Trampas que costaron tiempo (leer antes de repetir esto en otro lado)

- **El puerto era un NOMBRE, no una IP.** Por eso el diagnóstico inicial de "le
  cambió la IP" era errado: con nombre, un cambio de IP no rompe nada. Lo que
  fallaba era que la impresora no estaba.
- **Un `arp -a` sin barrer antes no prueba nada.** La tabla ARP solo guarda lo
  que la PC habló hace poco.
- **`ForEach-Object -Parallel` es de PowerShell 7**, no corre en el 5.1 que trae
  Windows. Usar el ping asincrónico de .NET (arriba).
- **Que un celular no responda al ping NO es aislamiento de clientes**: los
  teléfonos dejan de responder con la pantalla apagada.
- **Una reserva DHCP no sirve si el equipo no está conectado** — solo entrega la
  IP cuando el aparato la pide.
- **Durante horas la reserva estuvo SIN VERIFICAR y no había que darla por
  buena** — lo único que había era que BVC decía haberla hecho, y el `ping` daba
  "host inaccesible", que es lo contrario de una comprobación. Se verificó recién
  al final, cuando la impresora volvió al Wi-Fi y tomó la IP con su MAC. *Regla:
  una reserva no está hecha hasta que un `arp -a` muestra la MAC correcta en esa
  IP.*
- **`USB001` puede existir sin cable conectado** (queda de instalaciones
  anteriores). La prueba real es `Get-PnpDevice -PresentOnly`.
- **Reinstalar el driver deja puertos duplicados**: llegaron a ser cuatro
  (`XRXE84DEC285A2A`, `(0)`, `(1)` y `(2)`). Se borran con `Remove-PrinterPort`.
- **Un perfil de Wi-Fi corrupto se ve igual que un problema de red o de clave**:
  la PC mostraba la red con una X, con 87 % de señal y la clave correcta guardada.
  Ni alcance, ni banda, ni filtrado de MAC, ni contraseña cambiada — todas
  hipótesis que se probaron y cayeron. Se arregla borrando y recreando el perfil.
- **`break` dentro de `ForEach-Object` corta el script entero**, no solo el
  bucle: en el script de reconexión nunca se llegó a imprimir el resultado final.
  Usar `foreach` o una bandera.
- **`Test-Connection` tira "Error genérico"** si la placa de red está en
  transición (justo al cambiar de Wi-Fi). No significa que falló la conexión.
- **El nombre de la red se puede deducir de la MAC del gateway**: gateway
  `f0-63-f9-31-99-aa` → SSID `BVNET-99aa`. Útil cuando hay varias redes parecidas
  y hay que saber cuál es la del módem correcto.

## La lección de método

Se pasó una hora midiendo la red cuando la pregunta era **si la impresora estaba
viva**. El cable USB lo contestó en dos minutos y de paso resolvió el problema.
Ante un "andaba y dejó de andar": confirmar primero que el aparato funciona,
después buscar por qué no se lo ve.

## Si vuelven a llamar

- **Recomendación dada: dejarla por USB.** El 3020 pierde la configuración
  inalámbrica y ellos no tienen acceso al módem. Si necesitan imprimir desde otra
  PC, se comparte desde esta.
- Si insisten con Wi-Fi: **Xerox Easy Wireless Setup** (viene en el paquete
  V1.07), con la impresora conectada por USB. O WPS del módem + WPS de la
  impresora dentro de dos minutos. La reserva `192.168.100.100` ya está hecha.
- La hoja de configuración de la impresora sale manteniendo **WPS 10 segundos**:
  dice si tiene Wi-Fi asociado, a qué SSID y con qué IP.
