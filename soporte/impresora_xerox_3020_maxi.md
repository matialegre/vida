# Impresora Xerox Phaser 3020 — PC de Maxi (resuelto 2026-09-07)

**Síntoma**: andaba por red y a los pocos días dejó de imprimir. Estado `Error` en
Windows, sin más explicación.

**Causa real**: la impresora **se cayó del Wi-Fi**. No era el driver, ni la PC, ni
la IP. No estaba en la red en absoluto.

**Solución**: quedó **conectada por cable USB** (puerto `USB001`). Imprime y no
depende del módem del proveedor.

---

## Datos del equipo

| | |
|---|---|
| Modelo | Xerox Phaser 3020 (**solo Wi-Fi 2,4 GHz**, no tiene puerto de red) |
| MAC | `E8:4D:EC:28:5A:2A` |
| Nombre de red | `XRXE84DEC285A2A` (es `XRX` + la MAC, convención Xerox) |
| Driver | `Xerox_Phaser_3020_Windows_Print_Drivers_Utilities_V1.07` |
| Red del lugar | `192.168.100.x`, gateway `192.168.100.1` — **módem de BVC, sin router propio** |
| IP reservada | `192.168.100.100` — **BVC dice haberla reservado (2026-09-07). SIN VERIFICAR**: ver abajo |
| PC | usuario `Maxi`, Windows 11, **Windows PowerShell 5.1** (no 7) |

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
- **La reserva de `192.168.100.100` NUNCA SE VERIFICÓ y no hay que darla por
  buena.** Lo único que hay es que BVC dijo haberla hecho. Como la impresora
  jamás volvió al Wi-Fi, nunca pidió IP y la reserva nunca se puso a prueba: el
  `ping 192.168.100.100` dio "host de destino inaccesible", que es lo contrario
  de una comprobación. Puede estar bien, mal, o cargada con otra MAC.
  **Se comprueba así**, y recién el día que la impresora vuelva al Wi-Fi:
  `Test-NetConnection 192.168.100.100 -Port 9100` y `arp -a | Select-String
  "192.168.100.100"` — la MAC que aparezca tiene que ser `e8-4d-ec-28-5a-2a`. Si
  es otra, esa IP se la quedó otro equipo y hay que volver a hablar con BVC.
- **`USB001` puede existir sin cable conectado** (queda de instalaciones
  anteriores). La prueba real es `Get-PnpDevice -PresentOnly`.
- **Reinstalar el driver deja puertos duplicados**: quedaron tres
  (`XRXE84DEC285A2A`, `(0)` y `(1)`). Se borran con `Remove-PrinterPort`.

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
