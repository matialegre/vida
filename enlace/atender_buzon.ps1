<#
.SYNOPSIS
ENLACE / BUZON — la maquina servidora levanta tareas de enlace\buzon\pendiente\ y las ejecuta
con Claude Code en modo headless (claude -p).

.DESCRIPTION
Ciclo por tarea:
  pendiente\  --(la tomo)-->  haciendo\  --(claude -p)-->  hecho\   (o fallado\)
Cada transicion se commitea y pushea, asi Matias ve el avance desde el celular.

Elegibilidad: una tarea se atiende si su frontmatter `para:` es el hostname de esta
maquina, `cualquiera`, o el rol de esta maquina (ej. `servidor`).

.EXAMPLE
  .\enlace\atender_buzon.ps1                    # una pasada
  .\enlace\atender_buzon.ps1 -Loop -CadaSegundos 300
  .\enlace\atender_buzon.ps1 -Simular           # todo el ciclo pero SIN gastar una sesion de Claude
  .\enlace\atender_buzon.ps1 -SinPush           # no toca el remoto
#>
[CmdletBinding()]
param(
    [switch]$Loop,
    [int]$CadaSegundos = 300,
    [int]$MaxTareas = 3,
    [int]$TimeoutMinutos = 30,
    [switch]$Simular,
    [switch]$SinPush
)

$ErrorActionPreference = 'Stop'
. "$PSScriptRoot\lib\comun.ps1"

$HQ      = Get-HQRoot
$hostn   = Get-Hostname
$buzon   = Join-Path (Get-EnlaceRoot) 'buzon'
$dirs    = @{
    pendiente = Join-Path $buzon 'pendiente'
    haciendo  = Join-Path $buzon 'haciendo'
    hecho     = Join-Path $buzon 'hecho'
    fallado   = Join-Path $buzon 'fallado'
}
foreach ($d in $dirs.Values) { if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null } }

function Get-Rol {
    $f = Join-Path (Get-EnlaceRoot) "maquinas\$hostn.md"
    if (Test-Path $f) {
        $m = Select-String -Path $f -Pattern '^\- \*\*Rol\*\*: (.+)$' | Select-Object -First 1
        if ($m) { return $m.Matches[0].Groups[1].Value.Trim() }
    }
    return 'desconocido'
}
$rol = Get-Rol

<# Parsea el frontmatter YAML simple (clave: valor) de una tarea. #>
function Read-Tarea {
    param([string]$Path)
    $texto = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
    $meta  = @{}
    $cuerpo = $texto
    if ($texto -match '(?s)^\s*---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$') {
        $fm = $Matches[1]; $cuerpo = $Matches[2]
        foreach ($linea in ($fm -split "`r?`n")) {
            if ($linea -match '^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$') {
                $meta[$Matches[1].ToLower()] = $Matches[2].Trim().Trim('"', "'")
            }
        }
    }
    return [pscustomobject]@{
        Path = $Path; Nombre = (Split-Path $Path -Leaf); Meta = $meta
        Cuerpo = $cuerpo.Trim(); Texto = $texto
    }
}

function Test-EsParaMi {
    param([psobject]$T)
    $para = if ($T.Meta.ContainsKey('para')) { $T.Meta['para'] } else { 'cualquiera' }
    $para = $para.ToLower()
    return ($para -eq 'cualquiera' -or $para -eq $hostn.ToLower() -or $para -eq $rol.ToLower())
}

function Get-Prioridad {
    param([psobject]$T)
    $p = if ($T.Meta.ContainsKey('prioridad')) { $T.Meta['prioridad'].ToLower() } else { 'normal' }
    switch ($p) { 'urgente' { 0 } 'alta' { 1 } 'normal' { 2 } 'baja' { 3 } default { 2 } }
}

function Git-Sync {
    param([string]$Mensaje, [string[]]$Rutas)
    if ($SinPush) { Write-Aviso "-SinPush: no commiteo ($Mensaje)"; return }
    Invoke-Git -GitArgs (@('add', '--') + $Rutas) | Out-Null
    $st = Invoke-Git -GitArgs (@('status', '--porcelain', '--') + $Rutas)
    if ([string]::IsNullOrWhiteSpace($st.Salida)) { return }
    $c = Invoke-Git -GitArgs @('commit', '-m', $Mensaje)
    if ($c.Codigo -ne 0) { Write-Aviso "commit fallo: $($c.Salida)"; return }
    $p = Invoke-Git -GitArgs @('push')
    if ($p.Codigo -ne 0) { Write-Aviso "push fallo: $($p.Salida)" } else { Write-Ok "pusheado: $Mensaje" }
}

function Mover-Tarea {
    param([string]$Origen, [string]$DestinoDir)
    $destino = Join-Path $DestinoDir (Split-Path $Origen -Leaf)
    $r = Invoke-Git -GitArgs @('mv', '-f', '--', $Origen, $destino)
    if ($r.Codigo -ne 0 -or -not (Test-Path $destino)) {
        Move-Item -LiteralPath $Origen -Destination $destino -Force
    }
    return $destino
}

function Invoke-Tarea {
    param([psobject]$T)

    $id = if ($T.Meta.ContainsKey('id')) { $T.Meta['id'] } else { [IO.Path]::GetFileNameWithoutExtension($T.Nombre) }
    Write-Paso "Tarea $id  ($($T.Nombre))"

    # 1) pendiente -> haciendo
    $enHaciendo = Mover-Tarea -Origen $T.Path -DestinoDir $dirs.haciendo
    Add-Content -LiteralPath $enHaciendo -Value "`n---`n`n## Tomada`n- por: $hostn ($rol)`n- inicio: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n" -Encoding UTF8
    Git-Sync -Mensaje "ENLACE buzon: $hostn toma $id" -Rutas @('enlace/buzon')
    & (Join-Path (Get-EnlaceRoot) 'latido.ps1') -EnQueAnda "buzon: ejecutando $id" | Out-Null

    # 2) ejecutar
    $inicio = Get-Date
    $prompt = @"
Sos el Director de MATI-HQ atendiendo una tarea del BUZON de ENLACE (pedido remoto de Matias).
Repo: $HQ. Segui el CLAUDE.md del proyecto y la doctrina de ~/.claude/CLAUDE.md.
Trabaja de forma autonoma: no podes preguntarle nada a Matias, no esta.
Al terminar, escribi un resumen corto (que hiciste, evidencia, que quedo pendiente).

--- PEDIDO (tarea $id) ---
$($T.Cuerpo)
--- FIN DEL PEDIDO ---
"@

    $salida = ''; $ok = $false
    if ($Simular) {
        Start-Sleep -Milliseconds 300
        $salida = "[SIMULADO] No se ejecuto Claude. El prompt que se habria enviado tiene $($prompt.Length) caracteres.`nComando real: claude -p <prompt> --permission-mode acceptEdits"
        $ok = $true
    }
    else {
        $tmpOut = Join-Path $env:TEMP "enlace_$id.out.txt"
        $tmpErr = Join-Path $env:TEMP "enlace_$id.err.txt"
        $tmpIn  = Join-Path $env:TEMP "enlace_$id.prompt.txt"
        Set-Content -LiteralPath $tmpIn -Value $prompt -Encoding UTF8
        try {
            # claude -p : modo headless (confirmado con `claude --help`).
            # El prompt entra por stdin para no romperse con comillas/saltos de linea.
            $psi = New-Object System.Diagnostics.ProcessStartInfo
            $psi.FileName = (Get-Command claude).Source
            $psi.Arguments = '-p --permission-mode acceptEdits --output-format text'
            $psi.WorkingDirectory = $HQ
            $psi.UseShellExecute = $false
            $psi.RedirectStandardInput = $true
            $psi.RedirectStandardOutput = $true
            $psi.RedirectStandardError = $true
            $proc = [System.Diagnostics.Process]::Start($psi)
            $proc.StandardInput.Write($prompt)
            $proc.StandardInput.Close()
            $tOut = $proc.StandardOutput.ReadToEndAsync()
            $tErr = $proc.StandardError.ReadToEndAsync()
            if (-not $proc.WaitForExit($TimeoutMinutos * 60 * 1000)) {
                try { $proc.Kill($true) } catch { }
                $salida = "TIMEOUT tras $TimeoutMinutos minutos."
            } else {
                $salida = $tOut.Result
                $err    = $tErr.Result
                if ($err) { $salida += "`n`n[stderr]`n$err" }
                $ok = ($proc.ExitCode -eq 0)
                $salida = "exit=$($proc.ExitCode)`n`n$salida"
            }
        } catch {
            $salida = "EXCEPCION lanzando claude: $_"
        } finally {
            Remove-Item $tmpIn, $tmpOut, $tmpErr -ErrorAction SilentlyContinue
        }
    }
    $dur = [math]::Round(((Get-Date) - $inicio).TotalMinutes, 1)

    # 3) haciendo -> hecho | fallado
    $destDir = if ($ok) { $dirs.hecho } else { $dirs.fallado }
    $anexo = @"

---

## Resultado
- maquina: $hostn ($rol)
- estado: $(if ($ok) { 'HECHO' } else { 'FALLADO' })
- fin: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  (duracion: $dur min)
- modo: $(if ($Simular) { 'SIMULADO' } else { 'claude -p' })

``````
$salida
``````
"@
    Add-Content -LiteralPath $enHaciendo -Value $anexo -Encoding UTF8
    $final = Mover-Tarea -Origen $enHaciendo -DestinoDir $destDir
    Git-Sync -Mensaje "ENLACE buzon: $id -> $(Split-Path $destDir -Leaf) ($hostn, $dur min)" -Rutas @('enlace')
    if ($ok) { Write-Ok "$id HECHO ($dur min) -> $final" } else { Write-Malo "$id FALLADO -> $final" }
    return $ok
}

function Pasada {
    if (-not $SinPush) {
        $p = Invoke-Git -GitArgs @('pull', '--ff-only')
        if ($p.Codigo -ne 0) { Write-Malo "git pull fallo, no atiendo esta vuelta:`n$($p.Salida)"; return }
    }

    $tareas = @(Get-ChildItem $dirs.pendiente -Filter '*.md' -File -ErrorAction SilentlyContinue |
                Where-Object { $_.Name -ne 'EJEMPLO.md' -and $_.Name -notlike '_*' } |
                ForEach-Object { Read-Tarea $_.FullName } |
                Where-Object { Test-EsParaMi $_ } |
                Sort-Object @{ E = { Get-Prioridad $_ } }, @{ E = { $_.Meta['creado'] } })

    if ($tareas.Count -eq 0) {
        Write-Ok "buzon vacio para $hostn ($rol)."
        & (Join-Path (Get-EnlaceRoot) 'latido.ps1') -EnQueAnda 'buzon vacio, esperando' | Out-Null
        return
    }
    Write-Paso "$($tareas.Count) tarea(s) para mi. Atiendo hasta $MaxTareas."
    foreach ($t in ($tareas | Select-Object -First $MaxTareas)) { Invoke-Tarea -T $t | Out-Null }
    & (Join-Path (Get-EnlaceRoot) 'latido.ps1') -EnQueAnda 'buzon atendido' | Out-Null
}

if ($Loop) {
    Write-Paso "Atendiendo buzon en loop cada $CadaSegundos s en $hostn ($rol). Ctrl-C para cortar."
    while ($true) {
        try { Pasada } catch { Write-Malo "pasada fallo: $_" }
        Start-Sleep -Seconds $CadaSegundos
    }
} else {
    Pasada
    # git mv puede fallar (archivo no trackeado) y dejar $LASTEXITCODE sucio: no es un error del script.
    exit 0
}
