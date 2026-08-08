# ENLACE — PROTOCOLO

El contrato entre las maquinas de Matias. Si algo no esta escrito acá, no es parte del protocolo.

Repo unico de transporte: **`github.com/matialegre/vida`** (checkout local: `Documents\MATI-HQ`).
Tailscale es transporte de **acceso remoto** (entrar a la notebook), NO de sincronizacion.
La sincronizacion es git, siempre, porque deja historial y resuelve el caso "estaba apagada".

---

## 1. Modelo de datos

```
MATI-HQ/
└── enlace/
    ├── payload/claude/      IDENTIDAD  — lo que hace que un Claude sea "el Claude de Matias"
    │   ├── CLAUDE.md          doctrina Director (global)
    │   ├── agents/*.md        los 19 especialistas
    │   ├── settings.json      permisos, modelo, hooks
    │   └── memory/*.md        auto-memoria del proyecto MATI-HQ
    ├── buzon/               TRABAJO    — pedidos asincronicos entre maquinas
    │   ├── pendiente/  haciendo/  hecho/  fallado/
    ├── maquinas/            PRESENCIA  — quien existe y quien esta despierto
    │   ├── <hostname>.md          ficha estable (rol, SO, rutas, herramientas)
    │   └── <hostname>.estado.json latido (se reescribe seguido)
    └── lib/comun.ps1        manifiesto unico de que viaja y que no
```

**Regla de oro**: `lib\comun.ps1` (funcion `Get-PayloadItems` + lista `$NuncaViaja`) es la
**unica fuente de verdad** de que se sincroniza. Ningun script duplica esa lista.

---

## 2. Que se sincroniza (los 4 items)

| # | Vivo | Repo | Por que viaja |
|---|------|------|---------------|
| 1 | `~/.claude/CLAUDE.md` | `enlace/payload/claude/CLAUDE.md` | Sin esto, la maquina nueva no sabe que es el modo Director |
| 2 | `~/.claude/agents/*.md` | `enlace/payload/claude/agents/` | Los 19 especialistas |
| 3 | `~/.claude/settings.json` | `enlace/payload/claude/settings.json` | Permisos, modelo, hooks, tema |
| 4 | `~/.claude/projects/<clave>/memory/*.md` | `enlace/payload/claude/memory/` | Lo que Claude aprendio de Matias |

### La clave de proyecto NO se hardcodea
Claude Code guarda la memoria bajo una clave derivada de la ruta absoluta del proyecto:
reemplaza `\ / : . _` y espacios por `-`.

```
C:\Users\Pandemonium\Documents\MATI-HQ  ->  C--Users-Pandemonium-Documents-MATI-HQ
C:\Users\mati\Documents\MATI-HQ         ->  C--Users-mati-Documents-MATI-HQ
```

En la notebook el usuario puede llamarse distinto. Por eso `ConvertTo-ProjectKey`
la **calcula** en cada maquina. Hardcodearla romperia el despliegue de memoria en silencio.

### Lo que YA estaba y sigue igual
`agentes/` en la raiz del repo es el backup historico de los agentes (regla del CLAUDE.md de
proyecto, dueño @cronista). ENLACE **no lo reemplaza**: `enlace/payload/claude/agents/` es
la copia *operativa* que se despliega automaticamente. Si divergen, `sync.ps1 -Estado` lo canta.

---

## 3. Que NO se sincroniza — y por que

| Item | Motivo |
|------|--------|
| `.credentials.json` | **Token OAuth de Anthropic**. Es una credencial personal. Si se filtra, cualquiera actua como Matias y le gasta la cuota. Cada maquina hace su propio `claude` + login. |
| `history.jsonl` | Transcript completo de todas las sesiones: MBs, secretos pegados, ruido puro. |
| `sessions/`, `session-env/` | Estado de sesion atado al PID y al filesystem de esa maquina. |
| `cache/`, `paste-cache/`, `file-history/`, `shell-snapshots/` | Cache regenerable. |
| `debug/`, `backups/`, `uploads/`, `downloads/`, `tasks/` | Basura local. |
| `plugins/` | Se reinstalan solos desde `settings.json` (`enabledPlugins`). |

Defensa en 3 capas:
1. **`lib\comun.ps1`** — `$NuncaViaja`; `Copy-Seguro` se niega a copiar cualquier nombre de esa lista.
2. **Manifiesto positivo** — `sync.ps1` copia solo los 4 items nombrados. No hace `robocopy` de `~/.claude`.
3. **`.gitignore`** — red de contencion por si alguien copia a mano.

> Auditoria del historial (`git log --diff-filter=A --name-only`): **no hay credenciales
> ni tokens commiteados** en la historia de `vida.git` a la fecha 2026-08-07.

---

## 4. Formato de tarea del buzon

Un `.md` con frontmatter YAML simple + el pedido en prosa. Nombre sugerido:
`AAAA-MM-DD-tema-corto.md` (el nombre no es semantico; manda el `id`).

```yaml
---
id: 2026-08-07-galgas-consumo     # unico; si falta se usa el nombre del archivo
de: matias                        # quien pide (informativo)
para: cualquiera                  # cualquiera | <HOSTNAME> | <rol>  (rol: servidor/escritorio/movil)
prioridad: alta                   # urgente | alta | normal | baja   (default: normal)
creado: 2026-08-07T14:30:00-03:00 # ISO8601; desempata dentro de la misma prioridad
agente: energia                   # OPCIONAL: sugerencia de especialista
---

<el pedido en prosa, como se lo escribirias a una persona>
```

**Solo `para` y el cuerpo son realmente necesarios**; todo lo demas tiene default.
Ejemplo completo y realista: [`buzon/EJEMPLO.md`](buzon/EJEMPLO.md).

### Estados y transiciones

```
pendiente/ ──(la servidora la toma)──> haciendo/ ──(claude -p termina)──> hecho/
                                            └──(exit≠0 o timeout)───────> fallado/
```

- Cada transicion es un `git mv` + commit + push. Matias ve el avance desde el celular.
- Al pasar a `haciendo/` se anexa quien la tomo y cuando.
- Al cerrar se anexa una seccion `## Resultado` con estado, duracion y la salida de Claude.
- **Nada se borra.** `hecho/` y `fallado/` son el archivo historico.
- `EJEMPLO.md` y cualquier archivo que empiece con `_` son ignorados por el atendedor.

### Reintento
Mover el `.md` de `fallado/` a `pendiente/` a mano (o desde el celular). Se vuelve a ejecutar.

---

## 5. Quien puede escribir que

| Ruta | Escribe | Regla |
|------|---------|-------|
| `enlace/payload/**` | cualquier maquina, via `sync.ps1 -Push` | nunca a mano |
| `enlace/buzon/pendiente/` | Matias (celular, web, cualquier maquina) | crear tareas |
| `enlace/buzon/{haciendo,hecho,fallado}/` | **solo `atender_buzon.ps1`** | no mover a mano salvo reintento |
| `enlace/maquinas/<host>.md` | **solo esa maquina**, via `bootstrap.ps1` | nadie edita la ficha ajena |
| `enlace/maquinas/<host>.estado.json` | **solo esa maquina**, via `latido.ps1` | idem |
| `enlace/lib/`, `*.ps1`, `*.md` | cualquiera, con commit normal | son codigo |

Como cada maquina toca solo *su* ficha y *su* estado, el particionado por hostname hace
que la presencia **nunca** genere conflictos de merge.

---

## 6. Conflictos

**Principio: ENLACE nunca resuelve solo. Muestra el diff y para.**

### 6.1 Identidad (`payload/`)
`sync.ps1` clasifica cada archivo en `IGUAL | DISTINTO | SOLO_VIVO | SOLO_REPO`.

- `SOLO_REPO` en `-Pull` → se copia (es material nuevo de otra maquina).
- `SOLO_VIVO` en `-Push` → se sube.
- `SOLO_VIVO` en `-Pull` → **no se borra nada**; solo se avisa.
- `DISTINTO` → conflicto:
  - `-Estado` lo lista.
  - `-Push` muestra fechas + `--stat` y pide confirmacion `s/N`.
  - `-Pull` **para en seco** y ofrece: `-Push` (esta maquina manda) / `-Pull -Forzar` (el repo manda) / editar a mano.
  - `bootstrap.ps1` con divergencia: no pisa nada, imprime el `git diff --no-index` exacto.

Regla de oro para conflictos de doctrina (`CLAUDE.md`, agentes): **fusionar a mano**.
Son documentos de prosa; una eleccion automatica pierde una decision de Matias.

### 6.2 Git
Todos los scripts usan `git pull --ff-only`. Si hay divergencia real, **abortan** y lo dicen.
Nunca hay merge automatico dentro de un script desatendido.

### 6.3 Dos maquinas atendiendo la misma tarea
El `git mv pendiente/ -> haciendo/` + push es la señal de claim. La que pierde la carrera
falla el push, y en la pasada siguiente ya no ve la tarea en `pendiente/`.
Mitigacion practica: **una sola maquina con rol `servidor` corre `atender_buzon.ps1 -Loop`.**

---

## 7. Presencia

`latido.ps1` escribe `maquinas/<hostname>.estado.json`:

```json
{
  "hostname": "DESKTOP-RK8DH7C",
  "rol": "escritorio",
  "ultima_vez_viva": "2026-08-07T09:12:03.4+00:00",
  "claude_corriendo": true,
  "ip_tailscale": "100.x.y.z",
  "ip_lan": "192.168.0.15",
  "buzon_pendiente": 0,
  "buzon_haciendo": 1,
  "en_que_anda": "buzon: ejecutando 2026-08-07-galgas-consumo"
}
```

**Como se lee**: una maquina esta "despierta" si `ultima_vez_viva` tiene menos de
**2x su intervalo de latido** (con el default de 300 s: menos de 10 minutos).
Mas viejo que eso = apagada o sin red; no le delegues.

El latido **no** se commitea por defecto (seria ruido de commits cada 5 min).
Corre `latido.ps1 -Commit` cuando querés que las otras maquinas lo vean;
`atender_buzon.ps1` ya lo arrastra en sus commits de transicion de tarea.

---

## 8. Seguridad — reglas duras

1. `.credentials.json` **jamas** entra al repo. Verificado con `git check-ignore`.
2. Cada maquina hace su propio `claude` + login OAuth. La sesion no se comparte.
3. `atender_buzon.ps1` corre con `--permission-mode acceptEdits`: puede editar archivos,
   **no** puede saltarse permisos peligrosos. No usar `--dangerously-skip-permissions`
   en el atendedor: son prompts que llegan desde internet (GitHub) sin supervision.
4. Cualquiera con acceso de escritura a `vida.git` puede meter una tarea en `pendiente/`
   y la notebook la ejecuta. **El repo es privado y ese es el limite de confianza.**
   Si algun dia se hace publico, hay que firmar las tareas antes de ejecutarlas.
5. Si aparece un secreto commiteado: **avisar, no reescribir el historial por cuenta propia.**
