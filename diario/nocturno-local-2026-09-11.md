# Nocturno local — 2026-09-11

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\datalogger` (**P0** — RuView/GIMAP, *"terminarlo
primero, antes del trabajo Dreyfus"*, orden de Matías del 07-07), zona
`firmwares/nodo-gimap/` + `visor_gimap.py` + `tools/` + `docs/`.
**Branch:** `nocturno/local-2026-09-11-el-piezo-que-se-calibra-mudo`
(pusheado, `a8bf1ab`).
**⚠ Sale de `nocturno/local-2026-09-09-el-acelerometro-que-dice-cero`
(`222663a`)**, que sale del 09-06, que sale del 09-04, que sale de
`nodo-gimap/wifi-y-flasheo-2026-08-24`. **Al mergear éste entran los cuatro**:
no hace falta mergearlos aparte.
**Nunca hubo mDNS de por medio.** No se tocó nada de galgas ni de frioseguro, ni
`data/`, ni el gateway ESP32, ni el firmware de misiones.

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_dl_0911`, ya
eliminado) porque el árbol de `datalogger` tiene 6 archivos modificados y 4 sin
trackear de Matías, y un `checkout` los habría tocado. **Verificado al
terminar: los dos árboles (`datalogger` y `datalogger-gimap`) quedaron
idénticos**, en los branches donde estaban.

---

## TL;DR

> **El canal de piezo no tiene bus que preguntar.** No hay `WHO_AM_I`, no hay
> `OSError`: es un pin de ADC, y un pin de ADC **siempre contesta**. Y el nodo
> mide la línea de base **una sola vez, al arrancar** (`Piezos.cero()` promedia
> 200 lecturas) para después mandar `max(0, crudo - base)` a 200 Hz. Si el
> front-end está muerto —MCP6004 sin alimentación, cable cortado, entrada en
> corto— el ADC igual entrega un número, siempre el mismo, y **`cero()` lo
> adopta como línea de base**. La resta da exactamente cero, el `max(0, ...)` lo
> deja en cero, y el canal transmite un silencio perfecto para siempre.
>
> **Un canal de piezo muerto no se *parece* a uno en reposo: se CALIBRA A SÍ
> MISMO para ser indistinguible de uno en reposo.** Es peor que el caso del MPU
> del 09-09, donde el chip ausente por lo menos se delataba en el bus.

## Por qué esta tarea

1. **La dejó anotada el informe del 09-09**, en "lo que NO hice, a propósito":
   *"No toqué los piezos. `Piezos.leer()` no puede fallar (es un ADC interno)
   pero **sí puede quedar clavado** un front-end del MCP6004 sin alimentación...
   distinguirlo necesita mirar el ruido de la línea de base, y eso es otra noche
   y otro modelo."* Ésta es esa noche, y el modelo está escrito.
2. **Cierra la doctrina en el único canal que le faltaba.** El acelerómetro se
   autodiagnostica desde el 09-09, el enlace desde el 09-06, el WiFi desde el
   09-04. Los piezos eran el último canal que podía mentir sin que nada lo
   dijera — y son **la mitad del alcance declarado del proyecto** ("datalogger
   de 2 canales: MPU + PIEZO").
3. **Es la cadena que Matías va a enchufar**: el nodo GIMAP + el visor son lo
   que se usa en el banco de vibraciones.
4. **Se hace entera sin hardware** y no colisiona con ningún branch abierto.
5. Le tocaba a `datalogger` por rotación: las dos noches anteriores fueron
   frioseguro (PLATA) y galgas (octubre).

## Los tres modos de falla, que no son el mismo

| | qué pasa | qué se veía antes |
|---|---|---|
| **clavado** | el crudo no cambia **ni un bit**: front-end muerto, sin alimentación o en corto | nada. El cero salía por el aire como silencio |
| **saturado** | el crudo pegado al tope: ganancia de más o falla de continua | nada. Con la base también tomada contra el riel, otra vez cero |
| **base_alta** | el crudo vive **debajo** de la base: todo se recorta a cero y el canal queda sordo | nada |

`base_alta` llega por dos caminos y los dos son reales: **el banco ya estaba
vibrando cuando el nodo arrancó** y `cero()` capturó un reposo inflado, **o** la
caída del rectificador se movió con la temperatura durante una corrida larga
(unos −2 mV/°C en los diodos).

> Es el mismo patrón que el acelerómetro que decía cero (09-09), la sonda
> congelada de FrioSeguro (09-04-b) y el "OK vacío" de galgas (08-28): el
> sistema no falla, contesta bien y dice otra cosa.

## El discriminador que ordenó el diseño

**No se puede decidir por amplitud**: un canal en reposo tiene amplitud chica y
está perfectamente sano. Lo que distingue vivo de muerto es el **temblor**.

El ADC del RP2350 es de 12 bits y ruidoso, y `read_u16()` escala ese código a 16
bits: **1 LSB del ADC son 16 cuentas** de las que se leen. Una cadena analógica
alimentada, por más quieta que esté la mesa, **no entrega dos lecturas bit a bit
idénticas durante segundos**. Una muerta entrega siempre el mismo número, exacto.

Entonces la regla no es *"varía poco"* sino **"no varía NADA, ni un bit, durante
N segundos"**.

Misma trampa que el MPU y misma respuesta: el umbral está en **segundos**, no en
muestras, así sigue solo a la `fs` del lazo. Y es mucho más laxo —**10 s contra
los 2 s del acelerómetro**— porque una envolvente rectificada en reposo es
genuinamente más quieta que un giróscopo: hay que darle lugar antes de acusarla.

## El atajo que regala el arranque

`sensores.cero()` ahora devuelve **cuatro** valores: `(base1, base2, disp1,
disp2)`. La dispersión es el `max − min` de las 200 lecturas que promedió. Si da
**cero**, las 200 salieron idénticas: **el canal ya estaba muerto antes de
empezar**, y no hay que esperar 10 s para decir lo que el arranque ya vio.
`cero()` además lo grita por el log serie.

## Qué se entregó

`firmwares/nodo-gimap/salud_piezo.py` — **puro** (sin `machine`, sin ADC, sin
reloj, sin `print`) e **importado** por `main.py`: no es un espejo, lo que se
testea es lo que se flashea. Un objeto por canal, porque **una cadena muerta no
dice nada de la otra**.

La salud se juzga sobre el **crudo**, nunca sobre `p1/p2`: después de la resta y
del `max(0, ...)` los tres modos de falla dan todos el mismo cero y ya no se
distinguen. Eso está verificado por AST en el test, no confiado al comentario.

Y los consumidores hacen algo con eso:

- **el nodo**: LED `ERR_PIEZO` (5 destellos; 3 = MPU, 4 = SD) y una línea en el
  log serie cada 2 s. El MPU tiene prioridad en el LED porque es el único de los
  tres que se recupera solo, así que su destello cuenta una historia que cambia;
- **el visor**: vacía **el panel del canal caído y sólo ése**, con el motivo
  textual del nodo. Chips `piezo 1` / `piezo 2` con estado y `recorte %`;
- **`rx_gimap.py`**: columnas **`p1_ok` / `p2_ok`** al final del CSV — `si` /
  `no` / **`?`** para nodos anteriores a 1.0.8, porque *no saber* no es lo mismo
  que *estar bien*.

**El formato del paquete NO cambió**, por la misma razón que el 09-09: tocar la
trama toca el firmware, `rx_gimap.py`, el visor, el emisor y el test de
protocolo, y es una decisión de contrato. El nodo **sigue mandando ceros**; lo
que cambia es que esos ceros dejaron de afirmar algo.

## Un bug que encontró el test, no yo

Escribí la alerta del visor leyendo `a.className` para saber si ya había otra
puesta y acumular en vez de pisar. El test del JavaScript real falló en el caso
"los tres sensores caídos": el `motivo` del piezo tapaba al del MPU. **Leer una
propiedad del DOM que uno mismo acaba de escribir es frágil y no se puede
testear**; ahora se lleva en una variable del tick. Con los tres caídos se ven
los tres motivos.

## Cómo verificarlo (comandos exactos, sin hardware, ~5 minutos)

```bash
cd C:\Proyectos\datalogger
git fetch origin
git checkout nocturno/local-2026-09-11-el-piezo-que-se-calibra-mudo

# 1) la decision, contra el modulo que se flashea
python tools/test_salud_piezo.py

# 2) que los tests sirvan: reimplantar los defectos y ver que mueran
python tools/test_salud_piezo.py --mutantes

# 3) el JAVASCRIPT REAL del visor, corrido con node (sin navegador)
python tools/test_visor_js.py

# 4) las 11 suites del repo, sin regresion
for %t in (tools\test_*.py) do python %t

# 5) de punta a punta, sin desoldar nada (dos ventanas)
python visor_gimap.py
python emisor_prueba_SIN_HARDWARE.py --destino 127.0.0.1 --piezo1 clavado
#   -> panel del PIEZO 1 vacio con el cartel, PIEZO 2 latiendo, MPU dibujando
#   -> probar tambien --piezo2 base_alta y --piezo1 saturado
```

**Resultados obtenidos esta noche:**

- `test_salud_piezo.py` → **72 chequeos, 0 fallos**. Los bloques marcados
  REGRESIÓN fallan contra el código viejo. Hay **cableado real** verificado por
  AST: que `main.py` le pase `c1`/`c2` (crudo) y no `p1`/`p2`, que desempaquete
  las cuatro de `cero()`, y que `flashear_nodo.py` copie el archivo nuevo.
- `--mutantes` → **15/15 muertos**. Dos no murieron en la primera vuelta y hubo
  que endurecer el test primero.

  | mutante | qué reimplanta |
  |---|---|
  | 1, 2 | el clavado no se detecta nunca (el canal muerto vuelve a ser silencio) |
  | 3 | dos repetidas ya son clavado (un ADC quieto las produce solo) |
  | 4 | el umbral de clavado deja de seguir a la `fs` |
  | 5 | un golpe fuerte que satura 0,2 s se declara falla |
  | 6 | saturado no se detecta: queda como clavado, que dice menos |
  | 7 | el ruido de reposo se declara base_alta (el 50 % de recorte es SANO) |
  | 8 | la base alta no se detecta: el canal queda sordo en silencio |
  | 9 | el estado publica `ok` siempre (la mentira que esto vino a arreglar) |
  | 10 | histéresis asimétrica: un solo cambio lo declara sano otra vez |
  | 11 | una lectura repetida cuenta como prueba de vida |
  | 12 | la dispersión cero del arranque se ignora |
  | 13, 14 | la racha de idénticas no se corta / `iguales_max` no se registra |
  | 15 | el recorte se cuenta mal y el 50 % sano se ve como 0 % |

- **`test_visor_js.py` → 26 chequeos, 0 fallos** (eran 14). Corre el mismo
  `PAGINA` que se le manda al navegador con **node v24.14.0**, con un DOM y un
  `fetch` de mentira, y mide **qué le llegó a cada canvas**: con el piezo 1
  clavado, ese canvas sale con **0 tramos de señal** y el cartel; el piezo 2, con
  **1798**. Cubre también los dos casos donde **no hay que afirmar nada**: nodo
  viejo que no manda el campo, y JSON de estado rancio.
- **De punta a punta** contra `127.0.0.1`: `/datos` devolvió `piezo1.ok=false`
  con `estado="clavado"` y su motivo, `p1` en cero y `p2` picando 24999. El CSV
  de `rx_gimap.py` salió con `?,?,?` antes del primer estado y `si,si,no`
  después, con la línea de aviso en el log.
- **Sin regresión**: las **11** suites de `tools/` en verde. Dos hubo que
  arreglarlas y las dos fallaban por buenas razones: el doble de `Piezos` del
  test de reenganche devolvía **siempre el mismo número**, así que con esto
  puesto se declaraba clavado solo (ahora varía, igual que el doble del MPU), y
  el test del MPU miraba dos strings del visor que este cambio movió.

## ⚠️ Al publicar el OTA va el LOTE — leer antes de flashear

`salud_piezo.py` es **archivo nuevo**, y además cambiaron `sensores.py` (la
firma de `cero()`) y `led.py` (el patrón nuevo). Un OTA parcial deja al nodo
importando algo que no está o desempaquetando dos valores donde hay cuatro.

```
python publicar_ota.py 1.0.8 main.py salud_piezo.py sensores.py led.py
```

Por USB no hay nada que recordar: `flashear_nodo.py` ya lo tiene en la lista, y
el test lo verifica por AST.

## Qué quedó SIN verificar (pide el nodo enchufado)

1. **⚠️ `iguales_max` con los dos canales sanos y la mesa quieta.** Es el único
   número de todo esto que **no se puede estimar desde la PC**. El razonamiento
   dice que un ADC de 12 bits con ruido no da 2000 lecturas idénticas seguidas,
   **pero eso no está medido**. Si diera cerca de 2000, el umbral hay que
   subirlo o el nodo se va a declarar muerto a sí mismo. [@muestreador]
2. **El `recorte %` real en reposo.** El razonamiento dice ~50 % (el ruido cruza
   la base para los dos lados). Si diera muy lejos de eso, la línea de base no
   está donde se cree y hay que revisar la ganancia del MCP6004. [@muestreador]
3. **Desenchufar la alimentación del MCP6004 con el nodo andando** y ver la
   transición entera: panel vacío, cartel, chip, LED de 5 destellos, y la
   recuperación sola al volver.
4. **El costo del `leida()` en el lazo.** Son dos llamadas más por muestra a
   200 Hz. Cada una es un puñado de bytecodes sin armar texto (los `motivo` se
   construyen sólo en las transiciones), pero **el costo no está medido**; se
   mira contando `gaps` en una corrida larga contra una del 1.0.7.

## Lo que NO hice, a propósito

- **No re-anclé la línea de base.** Sería el arreglo "obvio" para `base_alta` y
  es exactamente el que no va: el nodo vive en un **banco de vibraciones**,
  donde la señal es continua **por diseño**. Un seguidor lento de la línea de
  base se comería la vibración que se vino a medir, y lo haría en silencio. La
  base se vuelve a tomar **reiniciando el nodo**, que es una decisión del que
  opera el ensayo, no del firmware. El visor lo dice con todas las letras en la
  alerta. [@muestreador]
- **No le puse un bit de validez a la trama.** Sigue valiendo lo que dijo el
  09-09: es una decisión de contrato, y si algún día se abre la trama van juntos
  los tres cambios pendientes (validez del MPU, validez de cada piezo, y
  microsegundos). [@muestreador]
- **No toqué el ADC ni el muestreo.** Este cambio no lee nada nuevo del
  hardware: mira el mismo crudo que ya se leía.

## Anotado y NO tocado

- **`main` de `datalogger` sigue con `visor.log` y dos herramientas sin trackear
  en el árbol de Matías** (`tools/check_sd_integrity.py`,
  `tools/test_integridad_sd.py`) más `firmwares/nodo-gimap/` sin trackear. Es
  trabajo suyo a medio hacer, no lo toqué. **Cuarta noche que se anota.**
- **La numeración de `QUE_FALTA.md` de este repo va por letras** (5b, 5c, 5d y
  ahora **5e**) para no correr las referencias a `#14`. Al mergear los cuatro
  conviene renumerar de una vez. [@cronista]
- **`salud_piezo.py` es candidato a la biblioteca junto con `salud_mpu.py`**, y
  `test_visor_js.py` más todavía: el harness de correr el JS de una página con
  node y medir qué le llegó a cada canvas sirve para el panel de FrioSeguro y
  para el dashboard de galgas, que hoy no tienen nada parecido. No los coseché
  porque ninguno se probó en hardware. **Segunda noche que se anota.**
  [@bibliotecario]
- **El ítem #4 del `QUE_FALTA` (driver INA219) sigue abierto** y es el bloqueante
  del DoD que menos depende de otros. Lo dejé de lado porque escribir un driver
  a ciegas contra un datasheet es lo más parecido a código especulativo que hay
  en la lista: se escribe en una tarde con el módulo en la mano. **Candidato
  para cuando Matías confirme que el INA219 está en el cajón.** [@energia]

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-11-el-piezo-que-se-calibra-mudo`
  (`a8bf1ab`), sobre `nocturno/local-2026-09-09-el-acelerometro-que-dice-cero`
  (`222663a`).
- `QUE_FALTA.md` de datalogger actualizado (ítem 5e). Detalle técnico en
  `docs/piezo-que-se-calibra-mudo.md`. README del nodo corregido (lista de
  archivos y línea del OTA).
- Worktree `C:\Proyectos\_noche_dl_0911` eliminado; `datalogger` quedó
  **idéntico** (los 6 modificados + 4 sin trackear de Matías, intactos, en el
  branch `08-31`) y `datalogger-gimap` limpio en `3491b72`.
- En MATI-HQ quedaron **sin commitear, tal como los encontré**,
  `comercial/panamerican/PRESUPUESTO_CERRO_MORO_INTERNO.html`,
  `dominios/{backend,comercial,diseno,frontend,pcb}.md` y
  `scripts/turno_noche_log.txt`: son de otro trabajo y no me corresponde
  firmarlos.
- Nada corriendo, nada abierto.
