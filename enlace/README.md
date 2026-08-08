# ENLACE

**El problema**: instalar Claude Code en una maquina nueva significa re-enseñarle todo — los
agentes, la doctrina, donde van las cosas, como se trabaja. Y cuando Matias esta en el taller
sin la PC, no hay forma de pedirle trabajo a un Claude que tenga el contexto del proyecto.

**ENLACE lo resuelve con archivos y git. Sin GUI, sin servidor, sin servicio pago.**

Una maquina nueva corre un comando y queda siendo "el Claude de Matias".
Una maquina que esta despierta atiende pedidos que Matias deja desde el celular.

---

## Las 4 piezas

| Pieza | Archivo | Que hace |
|---|---|---|
| **BOOTSTRAP** | `bootstrap.ps1` | Da de alta una maquina: chequea prerequisitos, clona el repo, despliega la identidad a `~/.claude`, registra la maquina. |
| **SYNC** | `sync.ps1` | Mantiene `~/.claude` igual en todas las maquinas: `-Push`, `-Pull`, `-Estado`. |
| **BUZON** | `buzon/` + `atender_buzon.ps1` | Trabajo asincronico. Matias deja una tarea, la maquina despierta la ejecuta con `claude -p`. |
| **PRESENCIA** | `latido.ps1` + `maquinas/` | Quien existe, quien esta despierto, en que anda. |

Todo se apoya en `lib\comun.ps1`: el manifiesto unico de que viaja y que no.

---

## Dar de alta una maquina nueva — 3 minutos

En la maquina nueva, PowerShell:

```powershell
# 1. Traer el bootstrap (todavia no hay repo)
iwr https://raw.githubusercontent.com/matialegre/vida/main/enlace/bootstrap.ps1 -OutFile $env:TEMP\bootstrap.ps1

# 2. Correrlo diciendo que rol cumple esta maquina
&  $env:TEMP\bootstrap.ps1 -Rol servidor -Notas "notebook por Ethernet al router, siempre prendida"

# 3. Login (la credencial NUNCA viaja por git — es lo unico manual)
claude
```

Eso ya:
- verifico git / node / python / claude y avisa lo que falte con el link oficial;
- clono `vida.git` en `Documents\MATI-HQ`;
- copio `CLAUDE.md`, los 19 agentes, `settings.json` y la memoria a `~/.claude` **de esa maquina**
  (calculando la clave de proyecto, que depende del usuario de Windows);
- detecto que herramientas tiene (KiCad, arduino-cli, LibreOffice, OpenSCAD, WinRAR, LOGO!Soft,
  Tailscale...) y escribio `enlace\maquinas\<hostname>.md`;
- dejo el primer latido.

Si la maquina es la **servidora**, agregar el atendedor de buzon (ver abajo).

```powershell
# Verificar
cd $HOME\Documents\MATI-HQ
.\enlace\sync.ps1 -Estado
claude              # y preguntarle: "quien sos y que maquinas hay?"
```

Prueba en seco antes de tocar nada: `.\enlace\bootstrap.ps1 -DryRun` (o `-SoloChequeo`
para ver solo prerequisitos y herramientas).

---

## Uso diario

```powershell
.\enlace\sync.ps1 -Estado    # que difiere entre lo vivo y el repo (no toca nada)
.\enlace\sync.ps1 -Push      # cambie un agente aca -> subilo
.\enlace\sync.ps1 -Pull      # arranco el dia -> traeme lo de la otra maquina
```

Si difiere el mismo archivo en dos maquinas, ENLACE **no elige**: muestra el diff y para.
Ver [PROTOCOLO.md § 6](PROTOCOLO.md#6-conflictos).

---

## El caso del taller: pedir trabajo desde el celular

Matias esta en la planta con el celular. La notebook esta prendida en casa.

### Desde la app de GitHub (o github.com en el navegador del celular)

1. Abrir `matialegre/vida` → carpeta **`enlace/buzon/pendiente/`**.
2. Tocar **`+` / "Create new file"** (en la app: el lapiz / "Add file").
3. Nombre: `2026-08-07-lo-que-sea.md`.
4. Contenido — copiar esta plantilla y cambiar el pedido:

```
---
id: 2026-08-07-lo-que-sea
de: matias
para: cualquiera
prioridad: alta
creado: 2026-08-07T14:30:00-03:00
---

Necesito que revises X. Los datos estan en dominios/energia.md.
Dejame la conclusion ahi y el proximo paso escrito.
```

5. **Commit** directo a `main`.

### Que pasa despues (solo)

- Hasta 5 minutos despues, la notebook hace `git pull`, ve la tarea, y como `para: cualquiera` la toma.
- La mueve a `buzon/haciendo/` con un commit → **Matias ve en el celular que arranco**.
- La ejecuta con `claude -p` en el repo, con toda la doctrina y los agentes cargados.
- La mueve a `buzon/hecho/` con el resultado anexado al final del mismo archivo → **commit + push**.
- Si falla o pasa el timeout, va a `buzon/fallado/` con el error. Para reintentar: moverla de vuelta
  a `pendiente/` desde el celular.

Matias vuelve del taller, abre el archivo en `hecho/`, y ahi esta el trabajo hecho.

> El formato solo necesita `para:` y el cuerpo. Todo lo demas tiene default.
> Ejemplo real completo: [`buzon/EJEMPLO.md`](buzon/EJEMPLO.md).

---

## Poner la servidora a atender — las 2 formas

### A) `/loop` de Claude Code (mientras hay una sesion abierta)

En una sesion de Claude Code en `MATI-HQ`:

```
/loop 5m corre .\enlace\atender_buzon.ps1 y contame si hizo algo
```

Ventaja: Claude ve los resultados y puede reaccionar.
Desventaja: vive mientras vive la sesion. Sirve para una tarde de taller.

### B) Tarea programada de Windows (24/7, sobrevive reinicios) — recomendada para la servidora

```powershell
$ps  = (Get-Command powershell.exe).Source
$hq  = "$HOME\Documents\MATI-HQ"
$acc = New-ScheduledTaskAction -Execute $ps `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$hq\enlace\atender_buzon.ps1`"" `
        -WorkingDirectory $hq
$trg = New-ScheduledTaskTrigger -Once -At (Get-Date).Date `
        -RepetitionInterval (New-TimeSpan -Minutes 5)
$set = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew `
        -ExecutionTimeLimit (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName "ENLACE-buzon" -Action $acc -Trigger $trg -Settings $set `
        -Description "ENLACE: atiende enlace\buzon\pendiente cada 5 min"

# y el latido, mas seguido y liviano:
$acc2 = New-ScheduledTaskAction -Execute $ps `
        -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$hq\enlace\latido.ps1`"" -WorkingDirectory $hq
$trg2 = New-ScheduledTaskTrigger -Once -At (Get-Date).Date `
        -RepetitionInterval (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName "ENLACE-latido" -Action $acc2 -Trigger $trg2 -Settings $set
```

Comprobar / sacar:
```powershell
Get-ScheduledTask -TaskName "ENLACE-*"
Start-ScheduledTask -TaskName "ENLACE-buzon"     # forzar una pasada ahora
Unregister-ScheduledTask -TaskName "ENLACE-buzon" -Confirm:$false
```

Alternativa mientras se prueba (una consola abierta):
```powershell
.\enlace\atender_buzon.ps1 -Loop -CadaSegundos 300
```

**Probar sin gastar sesiones de Claude**: `.\enlace\atender_buzon.ps1 -Simular`
hace todo el ciclo `pendiente → haciendo → hecho` pero no invoca el modelo.

---

## Ver quien esta despierto

```powershell
Get-ChildItem .\enlace\maquinas\*.estado.json |
  ForEach-Object { Get-Content $_ -Raw | ConvertFrom-Json } |
  Select-Object hostname, rol, ultima_vez_legible, claude_corriendo, buzon_pendiente, en_que_anda |
  Format-Table -AutoSize
```

Una maquina cuenta como despierta si su `ultima_vez_viva` tiene menos de ~10 minutos.

---

## Roles

| Rol | Quien | Que corre |
|---|---|---|
| `escritorio` | La PC del trabajo | Sesiones interactivas de Claude (Director). Latido al abrir. |
| `servidor` | La notebook por Ethernet | `atender_buzon.ps1` en loop + latido cada 5 min. La que labura cuando Matias no esta. |
| `movil` | La futura de Santa Cruz | Sesiones interactivas; puede atender buzon si esta prendida. |

---

## Que NO viaja (y por que)

`.credentials.json`, `history.jsonl`, `sessions/`, `cache/`, `paste-cache/`, `file-history/`,
`debug/`, `session-env/`, `backups/`. Son **credenciales** o **basura de maquina**.
Cada maquina hace su propio login. Detalle y las 3 capas de defensa:
[PROTOCOLO.md § 3](PROTOCOLO.md#3-que-no-se-sincroniza--y-por-que).

---

## Cuando algo se rompe

| Sintoma | Que hacer |
|---|---|
| `sync.ps1 -Pull` dice DIVERGENCIA | Es a proposito. Mira el `git diff --no-index` que imprime y decidi: `-Push` (esta maquina manda) o `-Pull -Forzar` (el repo manda). |
| La memoria no aparece en la maquina nueva | La clave de proyecto depende de la ruta. Corre `.\enlace\sync.ps1 -Estado` y fijate la linea `memory:`. Si el repo no esta en `Documents\MATI-HQ`, pasale `-RepoPath` a bootstrap. |
| El buzon no levanta la tarea | `para:` no coincide con el hostname ni el rol; o el archivo empieza con `_`; o el `git pull` fallo (lo dice). |
| `claude` no existe en la servidora | `npm i -g @anthropic-ai/claude-code`, despues `claude` para el login. |
| Tarea en `fallado/` | Abrila: la seccion `## Resultado` tiene exit code y stderr. Corregi el pedido y movela a `pendiente/`. |
