<#
.SYNOPSIS
ENLACE / PRESENCIA — escribe el latido de esta maquina en enlace\maquinas\<hostname>.estado.json

.DESCRIPTION
Cualquier sesion puede leer enlace\maquinas\*.estado.json para saber QUIEN esta despierto
antes de delegar trabajo. El archivo dice: hostname, rol, ultima vez viva, si hay una
sesion de Claude corriendo, IP de Tailscale (si hay) y una linea de "en que anda".

.EXAMPLE
  .\enlace\latido.ps1 -EnQueAnda "atendiendo el buzon"
  .\enlace\latido.ps1 -Loop -CadaSegundos 300      # late cada 5 min hasta Ctrl-C
  .\enlace\latido.ps1 -Commit                      # ademas commitea+pushea el latido
#>
[CmdletBinding()]
param(
    [string]$EnQueAnda = '',
    [ValidateSet('escritorio', 'servidor', 'movil', 'desconocido')][string]$Rol = '',
    [switch]$Loop,
    [int]$CadaSegundos = 300,
    [switch]$Commit
)

$ErrorActionPreference = 'Stop'
. "$PSScriptRoot\lib\comun.ps1"

$hostn    = Get-Hostname
$dir      = Join-Path (Get-EnlaceRoot) 'maquinas'
$archivo  = Join-Path $dir "$hostn.estado.json"
$ficha    = Join-Path $dir "$hostn.md"

if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }

function Get-RolDeFicha {
    if (Test-Path $ficha) {
        $m = Select-String -Path $ficha -Pattern '^\- \*\*Rol\*\*: (.+)$' | Select-Object -First 1
        if ($m) { return $m.Matches[0].Groups[1].Value.Trim() }
    }
    return 'desconocido'
}

function Get-IpTailscale {
    try {
        $exe = @("$env:ProgramFiles\Tailscale\tailscale.exe", "${env:ProgramFiles(x86)}\Tailscale\tailscale.exe") |
               Where-Object { Test-Path $_ } | Select-Object -First 1
        if ($exe) { return (& $exe ip -4 2>$null | Select-Object -First 1) }
    } catch { }
    return $null
}

function Get-IpLan {
    try {
        return (Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
                Where-Object { $_.IPAddress -notmatch '^(127\.|169\.254\.)' -and $_.PrefixOrigin -ne 'WellKnown' } |
                Select-Object -First 1).IPAddress
    } catch { return $null }
}

function Test-ClaudeCorriendo {
    # 1) proceso llamado claude
    if (Get-Process -Name 'claude' -ErrorAction SilentlyContinue) { return $true }
    # 2) node ejecutando el CLI de claude (el .Path del exe no alcanza: miramos la linea de comandos via CIM)
    try {
        $q = Get-CimInstance Win32_Process -Filter "Name='node.exe'" -ErrorAction SilentlyContinue |
             Where-Object { $_.CommandLine -and $_.CommandLine -match 'claude' }
        if ($q) { return $true }
    } catch { }
    return $false
}

function Escribir-Latido {
    $rolFinal = if ($Rol) { $Rol } else { Get-RolDeFicha }

    # Preservar "en que anda" si no se paso uno nuevo
    $anda = $EnQueAnda
    if (-not $anda -and (Test-Path $archivo)) {
        try { $anda = (Get-Content $archivo -Raw | ConvertFrom-Json).en_que_anda } catch { }
    }
    if (-not $anda) { $anda = 'idle' }

    $buzon = Join-Path (Get-EnlaceRoot) 'buzon'
    $pend  = @(Get-ChildItem (Join-Path $buzon 'pendiente') -Filter '*.md' -File -ErrorAction SilentlyContinue).Count
    $hac   = @(Get-ChildItem (Join-Path $buzon 'haciendo')  -Filter '*.md' -File -ErrorAction SilentlyContinue).Count

    $so = try { (Get-CimInstance Win32_OperatingSystem).Caption } catch { 'desconocido' }
    $tz = try { (Get-TimeZone).Id } catch { 'desconocido' }

    $estado = [ordered]@{
        hostname          = $hostn
        rol               = $rolFinal
        ultima_vez_viva   = (Get-Date).ToString('o')
        ultima_vez_legible= (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
        zona_horaria      = $tz
        claude_corriendo  = (Test-ClaudeCorriendo)
        ip_tailscale      = (Get-IpTailscale)
        ip_lan            = (Get-IpLan)
        so                = $so
        usuario           = $env:USERNAME
        repo              = (Get-HQRoot)
        buzon_pendiente   = $pend
        buzon_haciendo    = $hac
        en_que_anda       = $anda
    }
    $json = $estado | ConvertTo-Json -Depth 4
    Set-Content -Path $archivo -Value $json -Encoding UTF8
    Write-Ok "latido: $hostn ($rolFinal) — $anda   [pend=$pend hac=$hac]"

    if ($Commit) {
        Invoke-Git -GitArgs @('add', '--', "enlace/maquinas/$hostn.estado.json") | Out-Null
        $st = Invoke-Git -GitArgs @('status', '--porcelain', '--', "enlace/maquinas/$hostn.estado.json")
        if (-not [string]::IsNullOrWhiteSpace($st.Salida)) {
            Invoke-Git -GitArgs @('commit', '-m', "ENLACE latido $hostn", '--', "enlace/maquinas/$hostn.estado.json") | Out-Null
            $p = Invoke-Git -GitArgs @('push')
            if ($p.Codigo -ne 0) { Write-Aviso "push del latido fallo (no es grave)" }
        }
    }
}

if ($Loop) {
    Write-Paso "Latido en loop cada $CadaSegundos s. Ctrl-C para cortar."
    while ($true) {
        try { Escribir-Latido } catch { Write-Malo "latido fallo: $_" }
        Start-Sleep -Seconds $CadaSegundos
    }
} else {
    Escribir-Latido
}
