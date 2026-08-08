<#
.SYNOPSIS
ENLACE / SYNC — mantiene la identidad de Claude (~/.claude) sincronizada entre maquinas via git.

.DESCRIPTION
Los 4 items que viajan (definidos en lib\comun.ps1):
  1. ~/.claude/CLAUDE.md                    (doctrina Director)
  2. ~/.claude/agents/*.md                  (los 19 especialistas)
  3. ~/.claude/settings.json                (permisos, modelo, hooks)
  4. ~/.claude/projects/<clave>/memory/*.md (auto-memoria del proyecto MATI-HQ)

Lo que NUNCA viaja: .credentials.json, history.jsonl, sessions/, cache/,
paste-cache/, file-history/, debug/, session-env/, backups/  (secretos o basura de maquina).

.EXAMPLE
  .\enlace\sync.ps1 -Estado      # que difiere, sin tocar nada
  .\enlace\sync.ps1 -Push        # lo vivo -> repo -> commit -> push
  .\enlace\sync.ps1 -Pull        # git pull -> repo -> lo vivo
  .\enlace\sync.ps1 -Push -DryRun
#>
[CmdletBinding(DefaultParameterSetName = 'Estado')]
param(
    [Parameter(ParameterSetName = 'Estado')][switch]$Estado,
    [Parameter(ParameterSetName = 'Push')]  [switch]$Push,
    [Parameter(ParameterSetName = 'Pull')]  [switch]$Pull,
    [switch]$DryRun,
    [switch]$Forzar,        # en -Pull: pisa lo vivo aunque haya divergencia
    [string]$Mensaje        # mensaje de commit para -Push
)

$ErrorActionPreference = 'Stop'
. "$PSScriptRoot\lib\comun.ps1"

$HQ    = Get-HQRoot
$items = Get-PayloadItems

function Show-Estado {
    param([switch]$Silencioso)
    $todo = @()
    foreach ($it in $items) { $todo += Compare-PayloadItem -Item $it }

    if (-not $Silencioso) {
        Write-Paso "Estado ENLACE en $(Get-Hostname)"
        Write-Host "  repo:  $HQ"
        Write-Host "  vivo:  $(Get-ClaudeHome)"
        Write-Host "  memory:$(Get-MemoryDir)"
        Write-Host ""
        $grupos = $todo | Group-Object Item
        foreach ($g in $grupos) {
            $dist = @($g.Group | Where-Object { $_.Estado -ne 'IGUAL' })
            if ($dist.Count -eq 0) {
                Write-Ok "$($g.Name) — $($g.Count) archivo(s), todo igual"
            } else {
                Write-Aviso "$($g.Name) — $($dist.Count)/$($g.Count) difieren:"
                foreach ($d in $dist) { Write-Host "        $($d.Estado.PadRight(10)) $($d.Archivo)" }
            }
        }
        Write-Host ""
        $g = Invoke-Git -GitArgs @('status', '--porcelain', '--', 'enlace')
        if ([string]::IsNullOrWhiteSpace($g.Salida)) { Write-Ok "git: enlace/ sin cambios pendientes" }
        else { Write-Aviso "git: cambios sin commitear en enlace/"; $g.Salida -split "`n" | ForEach-Object { Write-Host "        $_" } }
    }
    return $todo
}

function Resolver-Conflictos {
    param([array]$Todo, [ValidateSet('Push','Pull')][string]$Direccion)
    # Conflicto = el archivo difiere Y el lado destino tiene cambios que el origen no conoce.
    # Heuristica sin estado extra: si difiere, mostramos el diff y pedimos decision explicita.
    $dist = @($Todo | Where-Object { $_.Estado -eq 'DISTINTO' })
    if ($dist.Count -eq 0) { return $true }

    Write-Aviso "$($dist.Count) archivo(s) difieren entre lo vivo y el repo."
    foreach ($d in $dist) {
        Write-Host ""
        Write-Host "  --- $($d.Item)/$($d.Archivo) ---" -ForegroundColor Magenta
        $vivoT = (Get-Item -LiteralPath $d.Vivo).LastWriteTime
        $repoT = (Get-Item -LiteralPath $d.Repo).LastWriteTime
        Write-Host "      vivo: $vivoT   repo: $repoT"
        $diff = & git --no-pager diff --no-index --stat -- "$($d.Repo)" "$($d.Vivo)" 2>&1
        $diff | Select-Object -First 5 | ForEach-Object { Write-Host "      $_" }
        Write-Host "      diff completo: git diff --no-index `"$($d.Repo)`" `"$($d.Vivo)`""
    }
    Write-Host ""
    if ($Forzar) {
        Write-Aviso "-Forzar activo: se pisa el destino ($Direccion)."
        return $true
    }
    if ($Direccion -eq 'Push') {
        # Push es la direccion natural de "esta maquina manda": pedimos confirmacion.
        $r = Read-Host "  Pisar el repo con lo vivo de esta maquina? (s/N)"
        return ($r -match '^[sSyY]')
    } else {
        Write-Malo "PARADA. -Pull pisaria cambios locales no guardados en el repo."
        Write-Host "  Opciones:" -ForegroundColor Yellow
        Write-Host "    a) .\enlace\sync.ps1 -Push        (esta maquina manda; sube lo local)"
        Write-Host "    b) .\enlace\sync.ps1 -Pull -Forzar (el repo manda; se descarta lo local)"
        Write-Host "    c) editar a mano el archivo en conflicto y reintentar"
        return $false
    }
}

function Desplegar-Payload {
    param([switch]$DryRun)
    $n = 0
    foreach ($it in $items) {
        if ($it.Tipo -eq 'archivo') {
            if (Test-Path -LiteralPath $it.Repo) {
                if (Copy-Seguro -Origen $it.Repo -Destino $it.Vivo -DryRun:$DryRun) { $n++ }
            }
        } else {
            $filtro = if ($it.PSObject.Properties.Name -contains 'Filtro' -and $it.Filtro) { $it.Filtro } else { '*' }
            if (Test-Path -LiteralPath $it.Repo -PathType Container) {
                Get-ChildItem -LiteralPath $it.Repo -Filter $filtro -File | ForEach-Object {
                    if (Copy-Seguro -Origen $_.FullName -Destino (Join-Path $it.Vivo $_.Name) -DryRun:$DryRun) { $n++ }
                }
            }
        }
    }
    return $n
}

function Recolectar-Payload {
    param([switch]$DryRun)
    $n = 0
    foreach ($it in $items) {
        if ($it.Tipo -eq 'archivo') {
            if (Test-Path -LiteralPath $it.Vivo) {
                if (Copy-Seguro -Origen $it.Vivo -Destino $it.Repo -DryRun:$DryRun) { $n++ }
            }
        } else {
            $filtro = if ($it.PSObject.Properties.Name -contains 'Filtro' -and $it.Filtro) { $it.Filtro } else { '*' }
            if (Test-Path -LiteralPath $it.Vivo -PathType Container) {
                Get-ChildItem -LiteralPath $it.Vivo -Filter $filtro -File | ForEach-Object {
                    if (Copy-Seguro -Origen $_.FullName -Destino (Join-Path $it.Repo $_.Name) -DryRun:$DryRun) { $n++ }
                }
            }
        }
    }
    return $n
}

# ---------------------------------------------------------------- MAIN ----
switch ($PSCmdlet.ParameterSetName) {

    'Estado' { Show-Estado | Out-Null }

    'Push' {
        Write-Paso "PUSH — lo vivo de $(Get-Hostname) hacia el repo"
        $todo = Show-Estado -Silencioso
        $cambios = @($todo | Where-Object { $_.Estado -ne 'IGUAL' })
        if ($cambios.Count -eq 0) { Write-Ok "Nada que subir: el repo ya refleja lo vivo."; return }

        # SOLO_REPO en push = alguien borro el archivo local o vino de otra maquina -> avisar
        $soloRepo = @($cambios | Where-Object { $_.Estado -eq 'SOLO_REPO' })
        if ($soloRepo.Count -gt 0) {
            Write-Aviso "Existen en el repo pero no en esta maquina (NO se borran del repo):"
            $soloRepo | ForEach-Object { Write-Host "        $($_.Item)/$($_.Archivo)" }
        }
        if (-not (Resolver-Conflictos -Todo $todo -Direccion 'Push')) { Write-Malo "Push cancelado."; return }

        $n = Recolectar-Payload -DryRun:$DryRun
        Write-Ok "$n archivo(s) copiados al payload."
        if ($DryRun) { Write-Aviso "-DryRun: no se commitea ni pushea."; return }

        $msg = if ($Mensaje) { $Mensaje } else { "ENLACE sync desde $(Get-Hostname): $($cambios.Count) cambio(s) en la identidad de Claude" }
        Invoke-Git -GitArgs @('add', '--', 'enlace') | Out-Null
        $st = Invoke-Git -GitArgs @('status', '--porcelain', '--', 'enlace')
        if ([string]::IsNullOrWhiteSpace($st.Salida)) { Write-Ok "git no ve cambios reales. Listo."; return }
        $c = Invoke-Git -GitArgs @('commit', '-m', $msg, '--', 'enlace')
        if ($c.Codigo -ne 0) { Write-Malo "commit fallo:`n$($c.Salida)"; return }
        Write-Ok "commit hecho."
        $p = Invoke-Git -GitArgs @('push')
        if ($p.Codigo -ne 0) { Write-Malo "push fallo (hace -Pull primero?):`n$($p.Salida)" } else { Write-Ok "push hecho." }
    }

    'Pull' {
        Write-Paso "PULL — repo hacia lo vivo de $(Get-Hostname)"
        if (-not $DryRun) {
            $p = Invoke-Git -GitArgs @('pull', '--ff-only')
            if ($p.Codigo -ne 0) {
                Write-Malo "git pull fallo (divergencia). NO se toca nada.`n$($p.Salida)"
                return
            }
            Write-Ok "git pull ok."
        }
        $todo = Show-Estado -Silencioso
        $cambios = @($todo | Where-Object { $_.Estado -ne 'IGUAL' })
        if ($cambios.Count -eq 0) { Write-Ok "Nada que desplegar: lo vivo ya refleja el repo."; return }
        if (-not (Resolver-Conflictos -Todo $todo -Direccion 'Pull')) { return }

        $n = Desplegar-Payload -DryRun:$DryRun
        Write-Ok "$n archivo(s) desplegados a $(Get-ClaudeHome)."
        if ($DryRun) { Write-Aviso "-DryRun: nada se escribio de verdad." }
        else { Write-Aviso "Reinicia la sesion de Claude Code para que tome la doctrina nueva." }
    }
}
