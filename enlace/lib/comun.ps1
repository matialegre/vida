# enlace/lib/comun.ps1 — funciones compartidas por todos los scripts de ENLACE
# Dot-source: . "$PSScriptRoot\lib\comun.ps1"
# Sin GUI, sin dependencias externas. PowerShell 5.1+ / 7+.

Set-StrictMode -Version Latest

# --- Rutas canonicas -------------------------------------------------------

function Get-EnlaceRoot {
    # .../MATI-HQ/enlace
    return (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
}

function Get-HQRoot {
    # .../MATI-HQ  (el repo git)
    return (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
}

function Get-ClaudeHome {
    if ($env:CLAUDE_CONFIG_DIR) { return $env:CLAUDE_CONFIG_DIR }
    return (Join-Path $HOME '.claude')
}

function Get-PayloadRoot {
    return (Join-Path (Get-EnlaceRoot) 'payload\claude')
}

function Get-Hostname {
    if ($env:COMPUTERNAME) { return $env:COMPUTERNAME }
    return [System.Net.Dns]::GetHostName()
}

<#
.SYNOPSIS
Traduce una ruta de proyecto a la clave que usa Claude Code en ~/.claude/projects/.
.DESCRIPTION
Claude Code codifica la ruta absoluta del proyecto reemplazando los separadores
y caracteres no alfanumericos-ni-guion por '-'.
  C:\Users\Pandemonium\Documents\MATI-HQ  ->  C--Users-Pandemonium-Documents-MATI-HQ
NO hardcodear: en la notebook el usuario puede llamarse distinto.
#>
function ConvertTo-ProjectKey {
    param([Parameter(Mandatory)][string]$Path)
    $p = $Path.TrimEnd('\', '/')
    return ($p -replace '[\\/:._ ]', '-')
}

function Get-MemoryDir {
    param([string]$ProjectPath = (Get-HQRoot))
    $key = ConvertTo-ProjectKey -Path $ProjectPath
    return (Join-Path (Get-ClaudeHome) "projects\$key\memory")
}

# --- Manifiesto: QUE viaja y QUE no ---------------------------------------
# Unica fuente de verdad. bootstrap.ps1 y sync.ps1 leen de aca.

function Get-PayloadItems {
    param([string]$ProjectPath = (Get-HQRoot))
    $claude  = Get-ClaudeHome
    $payload = Get-PayloadRoot
    return @(
        [pscustomobject]@{
            Nombre = 'CLAUDE.md'
            Tipo   = 'archivo'
            Vivo   = (Join-Path $claude 'CLAUDE.md')
            Repo   = (Join-Path $payload 'CLAUDE.md')
        }
        [pscustomobject]@{
            Nombre = 'agents'
            Tipo   = 'carpeta'
            Vivo   = (Join-Path $claude 'agents')
            Repo   = (Join-Path $payload 'agents')
            Filtro = '*.md'
        }
        [pscustomobject]@{
            Nombre = 'settings.json'
            Tipo   = 'archivo'
            Vivo   = (Join-Path $claude 'settings.json')
            Repo   = (Join-Path $payload 'settings.json')
        }
        [pscustomobject]@{
            Nombre = 'memory'
            Tipo   = 'carpeta'
            Vivo   = (Get-MemoryDir -ProjectPath $ProjectPath)
            Repo   = (Join-Path $payload 'memory')
            Filtro = '*.md'
        }
    )
}

# Lista negra explicita. Nada de esto entra JAMAS al repo.
$script:NuncaViaja = @(
    '.credentials.json', 'history.jsonl', 'sessions', 'cache', 'paste-cache',
    'file-history', 'debug', 'session-env', 'backups', 'shell-snapshots',
    'uploads', 'downloads', 'tasks', 'plugins', 'statsig', 'todos',
    'mcp-needs-auth-cache.json', '.last-update-result.json', '.last-cleanup'
)
function Get-NuncaViaja { return $script:NuncaViaja }

function Test-EsSecreto {
    param([Parameter(Mandatory)][string]$Path)
    $nombre = Split-Path $Path -Leaf
    foreach ($x in $script:NuncaViaja) { if ($nombre -ieq $x) { return $true } }
    return $false
}

# --- Comparacion de archivos ----------------------------------------------

function Get-HashArchivo {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

<#
.SYNOPSIS
Compara un item del payload entre lo vivo (~/.claude) y el repo.
.OUTPUTS
Objetos con Item, Archivo, Estado: IGUAL | DISTINTO | SOLO_VIVO | SOLO_REPO
#>
function Compare-PayloadItem {
    param([Parameter(Mandatory)][psobject]$Item)

    $res = @()
    if ($Item.Tipo -eq 'archivo') {
        $hv = Get-HashArchivo $Item.Vivo
        $hr = Get-HashArchivo $Item.Repo
        $estado = if ($null -eq $hv -and $null -eq $hr) { 'AUSENTE' }
                  elseif ($null -eq $hv) { 'SOLO_REPO' }
                  elseif ($null -eq $hr) { 'SOLO_VIVO' }
                  elseif ($hv -eq $hr)   { 'IGUAL' }
                  else                   { 'DISTINTO' }
        $res += [pscustomobject]@{
            Item = $Item.Nombre; Archivo = $Item.Nombre; Estado = $estado
            Vivo = $Item.Vivo; Repo = $Item.Repo
        }
    }
    else {
        $filtro = if ($Item.PSObject.Properties.Name -contains 'Filtro' -and $Item.Filtro) { $Item.Filtro } else { '*' }
        $nombres = @{}
        foreach ($base in @($Item.Vivo, $Item.Repo)) {
            if (Test-Path -LiteralPath $base -PathType Container) {
                Get-ChildItem -LiteralPath $base -Filter $filtro -File -ErrorAction SilentlyContinue |
                    ForEach-Object { if (-not (Test-EsSecreto $_.FullName)) { $nombres[$_.Name] = $true } }
            }
        }
        foreach ($n in ($nombres.Keys | Sort-Object)) {
            $pv = Join-Path $Item.Vivo $n
            $pr = Join-Path $Item.Repo $n
            $hv = Get-HashArchivo $pv
            $hr = Get-HashArchivo $pr
            $estado = if ($null -eq $hv) { 'SOLO_REPO' }
                      elseif ($null -eq $hr) { 'SOLO_VIVO' }
                      elseif ($hv -eq $hr)   { 'IGUAL' }
                      else                   { 'DISTINTO' }
            $res += [pscustomobject]@{
                Item = $Item.Nombre; Archivo = $n; Estado = $estado
                Vivo = $pv; Repo = $pr
            }
        }
    }
    return $res
}

function Copy-Seguro {
    param(
        [Parameter(Mandatory)][string]$Origen,
        [Parameter(Mandatory)][string]$Destino,
        [switch]$DryRun
    )
    if (Test-EsSecreto $Origen) {
        Write-Warning "BLOQUEADO (lista negra): $Origen"
        return $false
    }
    $dir = Split-Path $Destino -Parent
    if ($DryRun) {
        Write-Host "  [dry-run] $Origen -> $Destino" -ForegroundColor DarkGray
        return $true
    }
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    Copy-Item -LiteralPath $Origen -Destination $Destino -Force
    return $true
}

# --- Salida ----------------------------------------------------------------

function Write-Paso { param([string]$m) Write-Host "==> $m" -ForegroundColor Cyan }
function Write-Ok   { param([string]$m) Write-Host "  ok  $m" -ForegroundColor Green }
function Write-Aviso{ param([string]$m) Write-Host "  !!  $m" -ForegroundColor Yellow }
function Write-Malo { param([string]$m) Write-Host "  XX  $m" -ForegroundColor Red }

# --- Git helpers -----------------------------------------------------------

function Invoke-Git {
    param([Parameter(Mandatory)][string[]]$GitArgs, [string]$RepoPath = (Get-HQRoot))
    $salida = & git -C $RepoPath @GitArgs 2>&1
    return [pscustomobject]@{ Codigo = $LASTEXITCODE; Salida = ($salida -join "`n") }
}

function Test-RepoLimpio {
    param([string]$RepoPath = (Get-HQRoot))
    $r = Invoke-Git -GitArgs @('status', '--porcelain') -RepoPath $RepoPath
    return [string]::IsNullOrWhiteSpace($r.Salida)
}
