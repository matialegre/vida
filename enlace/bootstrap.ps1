<#
.SYNOPSIS
ENLACE / BOOTSTRAP — deja una maquina nueva operativa como "el Claude de Matias".

.DESCRIPTION
Un solo comando. Hace, en orden:
  1. Chequea prerequisitos (git, node, python, claude CLI) y reporta lo que falta con el link oficial.
     NO instala nada pesado por su cuenta.
  2. Clona github.com/matialegre/vida en Documents\MATI-HQ (o hace pull si ya esta).
  3. Despliega el payload (CLAUDE.md, agents\, settings.json, memory\) a ~/.claude de ESTA maquina.
     La ruta de memory se CALCULA a partir del path real del repo (no esta hardcodeada).
  4. Registra la maquina en enlace\maquinas\<hostname>.md (rol, SO, rutas, herramientas).
  5. Escribe el primer latido.

Idempotente: correrlo dos veces no rompe nada. Si detecta divergencia entre lo vivo
y el repo, AVISA y PARA (salvo -Forzar).

.EXAMPLE
  # En una maquina nueva, desde PowerShell (sin repo todavia):
  iwr https://raw.githubusercontent.com/matialegre/vida/main/enlace/bootstrap.ps1 -OutFile $env:TEMP\bootstrap.ps1
  & $env:TEMP\bootstrap.ps1 -Rol servidor

  # Desde un repo ya clonado:
  .\enlace\bootstrap.ps1 -Rol escritorio
  .\enlace\bootstrap.ps1 -DryRun          # no escribe nada, muestra que haria
#>
[CmdletBinding()]
param(
    [ValidateSet('escritorio', 'servidor', 'movil', 'desconocido')]
    [string]$Rol = 'desconocido',
    [string]$RepoUrl  = 'https://github.com/matialegre/vida.git',
    [string]$RepoPath = (Join-Path $HOME 'Documents\MATI-HQ'),
    [string]$Notas    = '',
    [switch]$DryRun,
    [switch]$Forzar,
    [switch]$SinPull,      # el repo ya esta y no quiero que toque git (arbol sucio, trabajo en curso)
    [switch]$SoloChequeo
)

$ErrorActionPreference = 'Stop'
$script:Fallas = @()

function W-Paso { param($m) Write-Host "`n==> $m" -ForegroundColor Cyan }
function W-Ok   { param($m) Write-Host "  ok  $m" -ForegroundColor Green }
function W-Av   { param($m) Write-Host "  !!  $m" -ForegroundColor Yellow }
function W-Mal  { param($m) Write-Host "  XX  $m" -ForegroundColor Red; $script:Fallas += $m }

# ========================================================== 1. PREREQUISITOS
W-Paso "1/5  Prerequisitos"

$prereqs = @(
    @{ Cmd = 'git';    Nombre = 'Git';         Ver = 'git --version';    Link = 'https://git-scm.com/download/win';        Critico = $true }
    @{ Cmd = 'node';   Nombre = 'Node.js 18+'; Ver = 'node --version';   Link = 'https://nodejs.org/en/download';          Critico = $true }
    @{ Cmd = 'python'; Nombre = 'Python 3';    Ver = 'python --version'; Link = 'https://www.python.org/downloads/';       Critico = $false }
    @{ Cmd = 'claude'; Nombre = 'Claude Code'; Ver = 'claude --version'; Link = 'npm i -g @anthropic-ai/claude-code';      Critico = $true }
)

foreach ($p in $prereqs) {
    $c = Get-Command $p.Cmd -ErrorAction SilentlyContinue
    if ($c) {
        $v = try { (& $p.Cmd ($p.Ver -split ' ')[1] 2>&1 | Select-Object -First 1) } catch { '?' }
        W-Ok "$($p.Nombre): $v   [$($c.Source)]"
    } elseif ($p.Critico) {
        W-Mal "FALTA $($p.Nombre) -> $($p.Link)"
    } else {
        W-Av "falta $($p.Nombre) (opcional) -> $($p.Link)"
    }
}

# Herramientas del taller: se detectan y se registran, no se instalan.
$herramientas = [ordered]@{
    'KiCad'       = @('C:\Program Files\KiCad', "$env:LOCALAPPDATA\Programs\KiCad")
    'arduino-cli' = @('C:\Tools\arduino-cli\arduino-cli.exe')
    'LibreOffice' = @('C:\Program Files\LibreOffice')
    'OpenSCAD'    = @('C:\Program Files\OpenSCAD')
    'WinRAR'      = @('C:\Program Files\WinRAR')
    'LOGO!Soft'   = @('C:\Program Files\Siemens', 'C:\Program Files (x86)\Siemens')
    'Tailscale'   = @('C:\Program Files\Tailscale', 'C:\Program Files (x86)\Tailscale')
    'GitHub CLI'  = @('C:\Program Files\GitHub CLI')
    'PlatformIO'  = @("$HOME\.platformio")
}
$detectadas = [ordered]@{}
foreach ($h in $herramientas.Keys) {
    $hit = $null
    foreach ($ruta in $herramientas[$h]) { if (Test-Path -LiteralPath $ruta) { $hit = $ruta; break } }
    if (-not $hit) {
        $bin = Get-Command ($h.ToLower() -replace '[^a-z\-]', '') -ErrorAction SilentlyContinue
        if ($bin) { $hit = $bin.Source }
    }
    $detectadas[$h] = $hit
    if ($hit) { W-Ok "$h -> $hit" }
}

if ($script:Fallas.Count -gt 0) {
    Write-Host ""
    W-Mal "Faltan prerequisitos criticos. Instalalos y volve a correr bootstrap."
    if (-not $Forzar) { exit 1 }
    W-Av "-Forzar: sigo igual."
}
if ($SoloChequeo) { W-Av "-SoloChequeo: termino aca."; exit 0 }

# ================================================================ 2. REPO
W-Paso "2/5  Repo MATI-HQ en $RepoPath"

$repoExiste = Test-Path -LiteralPath (Join-Path $RepoPath '.git')
if (-not $repoExiste) {
    if ($DryRun) { W-Av "[dry-run] git clone $RepoUrl `"$RepoPath`"" }
    else {
        $padre = Split-Path $RepoPath -Parent
        if (-not (Test-Path $padre)) { New-Item -ItemType Directory -Path $padre -Force | Out-Null }
        & git clone $RepoUrl $RepoPath
        if ($LASTEXITCODE -ne 0) { W-Mal "clone fallo"; exit 1 }
        W-Ok "clonado."
    }
} elseif ($SinPull) {
    W-Av "-SinPull: el repo ya esta, no toco git."
} else {
    $sucio = & git -C $RepoPath status --porcelain
    if ($sucio) {
        W-Av "El repo tiene cambios locales sin commitear:"
        $sucio -split "`n" | Select-Object -First 10 | ForEach-Object { Write-Host "        $_" }
        if (-not $Forzar -and -not $DryRun) {
            W-Mal "PARADA: no hago pull sobre un arbol sucio. Commitea o descarta, o corre con -Forzar."
            exit 1
        }
    }
    if ($DryRun) { W-Av "[dry-run] git -C `"$RepoPath`" pull --ff-only" }
    else {
        $out = & git -C $RepoPath pull --ff-only 2>&1
        if ($LASTEXITCODE -ne 0) { W-Mal "pull fallo (divergencia). Resolve a mano:`n$out"; exit 1 }
        W-Ok "pull: $(( $out -split "`n" )[-1])"
    }
}

# El repo ya esta: a partir de aca usamos SU libreria comun.
$libPath = Join-Path $RepoPath 'enlace\lib\comun.ps1'
if (-not (Test-Path $libPath)) {
    if ($DryRun) { W-Av "[dry-run] (repo no clonado todavia; salteo pasos 3-5)"; exit 0 }
    W-Mal "No encuentro $libPath. El repo no tiene ENLACE?"; exit 1
}
. $libPath

# ============================================================= 3. PAYLOAD
W-Paso "3/5  Desplegar payload a ~/.claude"

$claudeHome = Get-ClaudeHome
$memDir     = Get-MemoryDir -ProjectPath $RepoPath
Write-Host "  ~/.claude    : $claudeHome"
Write-Host "  clave proyecto: $(ConvertTo-ProjectKey -Path $RepoPath)"
Write-Host "  memory       : $memDir"

$items = Get-PayloadItems -ProjectPath $RepoPath
$conflictos = @()
$copiados = 0

foreach ($it in $items) {
    $comp = Compare-PayloadItem -Item $it
    foreach ($c in $comp) {
        switch ($c.Estado) {
            'IGUAL'     { }
            'SOLO_VIVO' { W-Av "$($c.Item)/$($c.Archivo): existe solo en esta maquina (no se toca; usa sync.ps1 -Push para subirlo)" }
            'AUSENTE'   { W-Av "$($c.Item): no existe ni en el repo ni acá" }
            'SOLO_REPO' {
                if (Copy-Seguro -Origen $c.Repo -Destino $c.Vivo -DryRun:$DryRun) {
                    $copiados++; W-Ok "nuevo: $($c.Item)/$($c.Archivo)"
                }
            }
            'DISTINTO'  {
                if ($Forzar) {
                    if (Copy-Seguro -Origen $c.Repo -Destino $c.Vivo -DryRun:$DryRun) {
                        $copiados++; W-Av "pisado (-Forzar): $($c.Item)/$($c.Archivo)"
                    }
                } else { $conflictos += $c }
            }
        }
    }
}

if ($conflictos.Count -gt 0) {
    Write-Host ""
    W-Mal "DIVERGENCIA en $($conflictos.Count) archivo(s): lo vivo y el repo difieren. NO se pisa nada."
    foreach ($c in $conflictos) {
        Write-Host "        $($c.Item)/$($c.Archivo)"
        Write-Host "          git diff --no-index `"$($c.Repo)`" `"$($c.Vivo)`""
    }
    Write-Host "  Decidi: sync.ps1 -Push (esta maquina manda) | bootstrap.ps1 -Forzar (el repo manda)" -ForegroundColor Yellow
} else {
    W-Ok "payload al dia ($copiados archivo(s) escritos)."
}

# ============================================================ 4. REGISTRO
W-Paso "4/5  Registrar maquina"

$hostn   = Get-Hostname
$fichaDir = Join-Path $RepoPath 'enlace\maquinas'
$ficha    = Join-Path $fichaDir "$hostn.md"

$os  = try { (Get-CimInstance Win32_OperatingSystem).Caption } catch { $PSVersionTable.OS }
$ram = try { [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1) } catch { '?' }
$cpu = try { (Get-CimInstance Win32_Processor | Select-Object -First 1).Name.Trim() } catch { '?' }
$ipTs = ''
try {
    $tsExe = @("$env:ProgramFiles\Tailscale\tailscale.exe", "${env:ProgramFiles(x86)}\Tailscale\tailscale.exe") |
             Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($tsExe) { $ipTs = (& $tsExe ip -4 2>$null | Select-Object -First 1) }
} catch { }

# El rol: si la ficha ya existe y no se paso -Rol explicito, respetar el que estaba.
$rolFinal = $Rol
if ($Rol -eq 'desconocido' -and (Test-Path $ficha)) {
    $m = Select-String -Path $ficha -Pattern '^\- \*\*Rol\*\*: (.+)$' | Select-Object -First 1
    if ($m) { $rolFinal = $m.Matches[0].Groups[1].Value.Trim() }
}

$lineasHerr = ($detectadas.Keys | ForEach-Object {
    if ($detectadas[$_]) { "- $_`: ``$($detectadas[$_])``" } else { "- $_`: (no instalado)" }
}) -join "`n"

$contenido = @"
# Maquina: $hostn

> Ficha generada por ``enlace\bootstrap.ps1``. Ultima actualizacion: $(Get-Date -Format 'yyyy-MM-dd HH:mm')
> El estado en vivo (si esta despierta, en que anda) esta en ``$hostn.estado.json``.

- **Rol**: $rolFinal
- **SO**: $os
- **CPU**: $cpu
- **RAM**: $ram GB
- **Usuario**: $env:USERNAME
- **Tailscale IP**: $(if ($ipTs) { $ipTs } else { '(sin tailscale)' })
- **Notas**: $(if ($Notas) { $Notas } else { '—' })

## Rutas
- Repo MATI-HQ: ``$RepoPath``
- ~/.claude: ``$claudeHome``
- memoria del proyecto: ``$memDir``
- clave de proyecto: ``$(ConvertTo-ProjectKey -Path $RepoPath)``

## Herramientas detectadas
$lineasHerr

## Que corre acá
$(switch ($rolFinal) {
  'servidor'   { "- ``enlace\atender_buzon.ps1`` en loop (atiende el buzon)`n- ``enlace\latido.ps1`` cada 5 min" }
  'escritorio' { "- Sesiones interactivas de Claude Code (Director)`n- ``enlace\latido.ps1`` al abrir sesion" }
  default      { "- (definir)" }
})
"@

if ($DryRun) {
    W-Av "[dry-run] escribiria $ficha"
} else {
    if (-not (Test-Path $fichaDir)) { New-Item -ItemType Directory -Path $fichaDir -Force | Out-Null }
    $anterior = if (Test-Path $ficha) { Get-Content $ficha -Raw } else { '' }
    # Idempotencia: solo reescribir si cambio algo que no sea la marca de tiempo.
    # normalizar: sacar la marca de tiempo, unificar saltos de linea y espacios del final
    $norm = { param($t) (($t -replace 'Ultima actualizacion: [\d\- :]+', '') -replace "`r`n", "`n").Trim() }
    if ((& $norm $anterior) -ne (& $norm $contenido)) {
        Set-Content -Path $ficha -Value $contenido -Encoding UTF8
        W-Ok "ficha escrita: $ficha"
    } else {
        W-Ok "ficha ya al dia (sin cambios): $ficha"
    }
}

# ============================================================= 5. LATIDO
W-Paso "5/5  Primer latido"
$latido = Join-Path $RepoPath 'enlace\latido.ps1'
if (Test-Path $latido) {
    if ($DryRun) { W-Av "[dry-run] & `"$latido`" -Rol $rolFinal -EnQueAnda 'recien dada de alta por bootstrap'" }
    else { & $latido -Rol $rolFinal -EnQueAnda 'recien dada de alta por bootstrap' }
} else { W-Av "no encuentro latido.ps1" }

# ================================================================ CIERRE
Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
if ($script:Fallas.Count -eq 0 -and $conflictos.Count -eq 0) {
    Write-Host " ENLACE listo en $hostn ($rolFinal)." -ForegroundColor Green
} else {
    Write-Host " ENLACE con avisos en $hostn. Leelos arriba." -ForegroundColor Yellow
}
Write-Host @"

 Proximos pasos:
   1. claude                          (login OAuth — la credencial NUNCA viaja por git)
   2. cd "$RepoPath" && claude        (arranca la sesion Director con toda la doctrina)
   3. .\enlace\sync.ps1 -Estado       (verifica que lo vivo y el repo coincidan)
"@ -ForegroundColor Gray
Write-Host "======================================================" -ForegroundColor Cyan
