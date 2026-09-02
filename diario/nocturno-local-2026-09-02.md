# Nocturno local — 2026-09-02

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (**P0** — "terminarlo primero, antes del
trabajo Dreyfus", orden tuya del 07-07).
**Branch:** `nocturno/local-2026-09-02-el-ota-que-si-brickea` (pusheado, `8d0d72b`).
**Sale de:** `main` (`9c63a2b`). **No depende de ningún otro branch nocturno.**
Toca `firmwares/pico2w-node/ota.py` y `main.py`, y agrega 3 archivos.
**Colisión conocida (una sola):** `07-17-b-ssid-casing`, que cambia la línea `NETS`
de este mismo `ota.py`. Ver "al mergear" abajo. Ninguno de los otros 25 branches
abiertos toca estos archivos.

---

## TL;DR

> **El OTA del nodo dice en su encabezado "si algo falla no toca nada (no brickea)".
> Las tres cosas que sostendrían esa frase no estaban — y la red de recuperación
> estaba enganchada en el único lugar donde no podía atrapar la caída.**

Tu regla escrita es *OTA nunca ladrillo: hash + `.bak` + rollback por arranques
fallidos*. `ota.py` no tenía ninguna de las tres. Y no es código dormido:
`wifi_push.poll()` lo llama **cada 30 s** y `eco.py` una vez por ciclo.

**H1 — el swap borraba el archivo bueno y seguía de largo.**

```python
for name in got:
    try:
        try: os.remove("/" + name)        # se borra el bueno
        except OSError: pass
        os.rename("/" + name + ".new", "/" + name)
    except Exception as e:
        print("[ota] swap %s fallo: %s" % (name, e))   # se traga la falla
_set_ver(ver)                                          # y la version avanza igual
machine.reset()
```

El `except` imprimía y el `for` **seguía con el siguiente archivo**. Después
`_set_ver(ver)` corría igual y el nodo reiniciaba sin `nodo.py`. Lo peor es la
segunda vuelta: con la versión ya anotada, `check_update()` entra por
`if ver <= local_ver(): return False` y **no reintenta nunca**. La falla se
auto-sella y queda esperando que un humano publique una versión más alta.

Es la **cuarta** aparición del mismo patrón en el portfolio, después de
`lastSupabaseSync` (`08-26`), `faultAlerted1` (`08-29`) y `lastTelegramAlert`
(`09-01-b`): **el estado avanza aunque la acción no haya ocurrido.**

**H2 — un corte de energía a mitad del swap no dejaba rastro.** Es un nodo a
batería. Entre el `remove` del archivo 1 y el `rename` del archivo 4 hay ventana
real; el FS quedaba mezclado y nadie se enteraba.

**H3 — la red de recuperación no cubría el caso para el que existe.** `main.py`
terminaba con un `except` que llama a `ota.recovery_loop()`… pero arriba de todo,
**fuera de cualquier `try`**:

```python
from config import cfg
from nodo import Nodo, apply_profile, HAS_WIFI
```

`config.py` y `nodo.py` son exactamente los archivos que el OTA reemplaza. Si el
que entró tiene un `SyntaxError`, la excepción sale **del import de `main.py`**, no
de `main()`: cae al REPL y `recovery_loop()` no corre. **El rescate por aire cubría
todo menos la única falla que el OTA puede causar.**

Es el mismo drift que el `09-01` de galgas ("el rollback estaba escrito y nunca se
armaba") y el `08-28` ("la calibración se escribía en NVS y no la leía nadie"): el
mecanismo existe, el cable no.

**H4 — nada revertía por arranques fallidos**, y `_get()` hacía `except Exception:
break` en el `recv`, así que **un timeout a mitad de la descarga se veía igual que
un body completo**. Lo tapaba la comparación de tamaño… salvo con `size: -1`, que es
justo lo que publica `handleOtaSetver()` del ESP32 cuando no tiene el archivo
(`esp32_dashboard.ino:1074`) — y ahí el chequeo se salteaba entero
(`if size >= 0 and ...`).

## Por qué esta tarea y no otra

1. **Desbloqueé datalogger, que llevaba dos noches parado.** Los turnos del `09-01`
   y `09-01-b` lo saltearon (con razón) porque su checkout está sucio y tiene el
   branch `08-31-el-csv-que-no-avisa` sin un solo commit. **Lo resolví sin tocar
   nada de eso**: trabajé en un `git worktree` aparte sacado de `main`, que deja el
   checkout de esa carpeta intacto. Lo verifiqué al cerrar: sigue en el mismo
   branch, con los mismos 6 modificados y 4 sin trackear, byte por byte. El worktree
   ya se borró.
2. **Jerarquía + rotación.** Anoche fueron galgas y frioseguro. Datalogger es el P0
   que pediste terminar **antes** del trabajo Dreyfus. Cosechador sigue bloqueado por
   la compra.
3. **No estaba en ningún branch.** De los 26 abiertos, el único que toca `ota.py` es
   `07-17-b-ssid-casing`, y son 3 líneas de SSID. Nadie auditó el camino de instalación.
4. **Es tu regla dura, y estaba declarada sin implementar** en el repo — igual que
   pasó en galgas anteanoche. Cierra el mismo hueco en el otro proyecto.
5. **Software puro**, verificable sin banco hasta el último tramo.

## Qué hice

La instalación pasa a ser una **transacción**:

| Archivo | Para qué |
|---|---|
| `/ota_swap.jrn` | swap en curso. Si sobrevive a un reboot, hubo corte → revertir |
| `/<name>.bak` | el archivo bueno. El swap **renombra**, no borra |
| `/ota_boot.txt` | `"<arranques> <ver_previa> <archivos>"` — verificación pendiente |
| `/ota_bad.txt` | versión que se revirtió sola. No se reinstala |

- `_install()` escribe el journal y ante **el primer** rename fallido revierte lo ya
  swapeado y devuelve `False`. **`_set_ver(ver)` quedó afuera**, condicionado a ese
  `True`: si falla, la versión no se mueve y el poll de 30 s **reintenta**.
- `boot_check()` es **lo primero de `main.py`, antes de importar `config` y `nodo`**,
  y no importa ningún módulo del proyecto a propósito (el checker lo verifica). Si ve
  el journal, revierte; si hay verificación pendiente, cuenta el arranque.
- Los imports riesgosos quedaron en un `try` cuyo `except` llama a `on_crash()` y
  después a `recovery_loop()`.
- Tras 3 arranques sin confirmar, o ante un crash con la verificación abierta:
  rollback desde los `.bak`, **se devuelve la versión previa**, y la mala va a
  **cuarentena**. Sin la cuarentena el nodo revierte, ve el mismo manifest 30 s
  después y **reinstala el mismo firmware roto para siempre**.

**Dos decisiones que aparecieron al mirar de cerca, y las dos son bugs que me evité:**

- **La lista de archivos se guarda explícita**, no se deduce escaneando `*.bak`. Mi
  primera versión escaneaba, y tiene dos fallas reales que ahora son test: un `.bak`
  huérfano de un OTA anterior se restauraría **encima de una instalación sana** (test
  16), y un archivo que el OTA **agregó** no deja `.bak` y hay que borrarlo igual en el
  rollback (test 15).
- **`mark_ok()` borra los `.bak`.** Mientras existen son la única vuelta atrás; si
  sobreviven a la confirmación son basura restaurable por error, y el FS del Pico es chico.

## Cómo verificarlo (comandos exactos, sin hardware)

⚠️ **El checkout de `C:\Proyectos\datalogger` está sucio**, así que un `git checkout`
directo te va a arrastrar los cambios del `08-31`. Usá un worktree (que es como
trabajé yo) o commiteá/descartá eso primero:

```bash
cd C:\Proyectos\datalogger
git worktree add /c/Proyectos/_rev nocturno/local-2026-09-02-el-ota-que-si-brickea
cd /c/Proyectos/_rev

# 1. la transaccion, sobre el ota.py REAL (shims de MicroPython + ROOT en un tmpdir)
python tools/test_ota_install.py
#    -> OK -- 88 checks, 0 fallas

# 2. el CABLEADO en main.py + 16 mutantes de ota.py
python tools/check_ota_wiring.py --mutants
#    -> OK -- 48 checks, 0 fallas; los 16 mutantes mueren

# 3. la prueba de que el checker sirve: contra main tiene que REPROBAR
cd C:\Proyectos\datalogger && git worktree add /c/Proyectos/_main main
cp /c/Proyectos/_rev/tools/{test_ota_install,check_ota_wiring}.py /c/Proyectos/_main/tools/
python /c/Proyectos/_rev/tools/check_ota_wiring.py --root /c/Proyectos/_main
#    -> FALLO -- 28 checks, 18 fallas (rc=1)

git worktree remove --force /c/Proyectos/_rev; git worktree remove --force /c/Proyectos/_main
```

Los tres corrieron esta noche y dieron eso. También `python -m py_compile` sobre los
4 archivos.

El punto 3 es el que le da valor al resto: un checker que no reprueba el bug que dice
cazar no vale nada. Y los 16 mutantes existen porque un test verde sobre un módulo que
no se puede romper tampoco prueba nada: borrar el viejo sin `.bak`, avanzar la versión
con el install fallido, no escribir el journal, no consultar la cuarentena, que el
rollback no restaure, que no borre lo agregado, que no devuelva la versión previa…

El test corre **el archivo que se flashea**, no un espejo en Python: `ota.ROOT` es la
única concesión (una constante que en el nodo vale `"/"`).

> **Un mutante sobrevivió en la primera pasada** — el que saca la validación de
> `size < 0` — y tenía razón: ese guard lo tapa igual la comparación de tamaño
> post-descarga, así que el valor de retorno no cambia. Lo que sí cambia es que sin él
> se gasta la radio bajando un archivo condenado y se suma `-1` al total del chequeo de
> espacio libre. El test ahora afirma **que no se pidió ningún archivo**, y el mutante
> muere por el motivo correcto. No lo encontré yo; lo encontró el mutante.

## Qué quedó SIN verificar (necesita banco)

Todo lo de arriba prueba la **decisión** y el **cableado**, no el **efecto**: ningún
Pico real ejecutó esto.

1. **El rollback ocurriendo.** Publicar por `/ota/setver` un `nodo.py` con un
   `SyntaxError` a propósito y ver por serie `los modulos del nodo NO cargan` →
   `REVIERTO` → el nodo volviendo solo. Éste es el bug principal.
2. **El corte de energía real**: desenchufar durante el swap (la ventana es de decenas
   de ms; conviene forzarla con archivos grandes) y confirmar `el swap quedo a medias`
   en el arranque siguiente.
3. **`os.statvfs` en el puerto rp2** — el chequeo de espacio libre asume `f_bsize *
   f_bavail`. Si el puerto no lo tiene, `_free_bytes()` devuelve `None` y el chequeo se
   saltea sin romper nada, pero hay que ver cuál de las dos pasa. **En Windows
   `os.statvfs` no existe, así que los tests no ejercitan la rama real** (el test 14
   inyecta el valor).
4. **Costo en flash del nodo**: 4 archivos de estado más los `.bak` transitorios, que
   duplican el tamaño de lo que se actualiza durante la ventana de verificación. En un
   FS de Pico casi lleno eso importa y no está medido.

## Limitaciones declaradas (no son omisiones)

- **Si el OTA rompe `ota.py` mismo, no hay red.** `main.py` lo importa en un `try`, así
  que no explota, pero sin `ota.py` no hay ni rollback ni `recovery_loop()`: solo USB.
  Lo correcto es no incluirlo nunca en un manifest, o instalarlo último y aparte. **No
  lo bloqueé en código**: es decisión tuya y toca el flujo de publicación del ESP32.
- **`mark_ok()` confirma al construir el `Nodo()`, no después de N ticks buenos.** Un
  rollback de archivos `.py` puede distinguir código que *no carga o no construye*, que
  es lo que produce un `SyntaxError` o un import roto. Un bug de lógica adentro del
  `tick()` no se distingue de un MPU desoldado o una SD ausente, y revertir por eso
  convertiría la red de seguridad en la falla. Misma frontera que dejó anotada el
  `09-01` de galgas con el watchdog.
- **No hay hash, hay tamaño.** Un `sha256` por archivo requiere que
  `handleOtaSetver()` del ESP32 lo publique, y cambiar el contrato del manifest sin
  poder probarlo contra el ESP real es justo lo que no se hace de noche. Lo que sí se
  cerró es el agujero de transporte que hacía que el tamaño no alcanzara.
- **Hay 3 copias de `ota.py`** (`pico2w-node`, `pico2w-eco-com14`,
  `pico2w-wifi-com13`). Toqué solo la canónica — la que flashea `flash_node.ps1`.
  `check_ota_wiring.py` avisa de la divergencia en cada corrida; sincronizarlas a
  ciegas, sin saber cuál está en qué placa, sería peor que la deuda.
- **Al mergear con `07-17-b-ssid-casing`**: ese branch reemplaza la línea `NETS` por
  `from wifi_nets import NETS`. Son líneas distintas, pero git va a pedir resolución
  manual porque el archivo se reescribió. **Quedate con el import y borrá el
  `NETS = [...]` literal.**

**Cosecha a biblioteca:** el patrón journal + `.bak` + verificación por arranques es
candidato claro — galgas acaba de construir su gemelo en C para ESP32 (`ota_rescue.h`,
el `09-01`) y FrioSeguro lo quiere igual. **No se cosecha todavía**: la regla del
`@bibliotecario` es que ningún módulo entra sin decir dónde se probó, y esto no vio un
Pico real. Cuando pasen el punto 1 de acá y el punto 1 del `09-01`, van juntos y de
paso se decide si comparten ficha.

## Hallazgos colaterales — dos cosas para un minuto tuyo

1. **`C:\Proyectos\datalogger` sigue con el árbol sucio**, tercera noche. El branch
   `nocturno/local-2026-08-31-el-csv-que-no-avisa` sigue **sin un solo commit y sin
   pushear**, con 6 archivos modificados en `firmwares/pico2w-node/` y 4 sin trackear
   (`firmwares/nodo-gimap/`, `tools/check_sd_integrity.py`,
   `tools/test_integridad_sd.py`, `visor.log`). Esta noche **ya no bloquea** (el
   worktree lo esquiva), pero es trabajo de alguien colgando: o se commitea en su
   branch, o se tira.
2. **`MATI-HQ` sigue con cambios sin commitear de antes de esta sesión**: `PORTFOLIO.md`,
   6 bitácoras de dominios, `scripts/turno_noche_log.txt`, y `comercial/` +
   `logs/` sin trackear. No los toqué: el commit de esta noche stagea **solo** el
   informe y nada más.

---

## Estado del branch

`nocturno/local-2026-09-02-el-ota-que-si-brickea` → `8d0d72b`, pusheado a `origin`.
`QUE_FALTA.md` de datalogger actualizado (ítem **#15**). Documento largo:
`C:\Proyectos\datalogger\docs\ota-sin-ladrillo.md`.
Los dos worktrees temporales se borraron; `git worktree list` en datalogger vuelve a
tener una sola entrada.
