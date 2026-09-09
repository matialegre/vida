# Nocturno local — 2026-09-08-b

**Trabajador:** worker nocturno local (Matías durmiendo). **Segundo turno** de la
noche — el primero fue `nocturno-local-2026-09-08.md` (frioseguro, el compresor
que no se contaba).
**Repo tocado:** `C:\Proyectos\galgas` (**P0 octubre**, con el frente comercial
abierto: hay cámaras compitiendo adentro de Dreyfus).
**Branch:** `nocturno/local-2026-09-08-b-la-version-que-nunca-sube`
(pusheado, `f7df5a2`).
**Sale de `origin/main` (`49c238d`) limpio**, sin ningún otro branch mergeado
adentro.
**No toca** SQL, ni el bucket de Storage, ni `data/field_captures/`, ni el nodo
v3 (ATmega), ni `hardware/`, ni el panel web. **No colisiona con ningún branch
abierto.**

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_galgas_0908b`, ya
eliminado). **Verificado al terminar: el árbol de `galgas` quedó idéntico**, en
el branch `nocturno/local-2026-09-05-la-potencia-que-nadie-cambio` donde estaba
y sin archivos sueltos.

---

## TL;DR

> **El OTA decidía con `strcmp`.** Compara letra a letra lo que es un número:
> `"0.10.0"` es **menor** que `"0.9.0"`, así que **la décima release nunca se
> instalaba sobre la novena**. El RX ya corre `3.6.7-RX-palways` — `3.6.10` le
> sería invisible, y sin ningún síntoma: el nodo contesta "no hay update" y
> sigue durmiendo, sano en el dashboard, con la única vía de mantenimiento
> remoto muerta. Y la segunda mitad es peor: **nada miraba para quién era el
> `.bin`**. A y B comparten `device_type` `"emisor"`, así que una fila global
> les servía a los dos, y sus binarios difieren en `DEVICE_ID` y en
> `OFFSET_SIGN` (+1 / −1). El `.bin` de A en la placa B da **dos nodos que dicen
> llamarse "A"** y una galga con el signo dado vuelta: **la comparación A-vs-B,
> que ES la detección, compara un nodo contra sí mismo.**

## Por qué esta tarea

1. **Es un ítem del `QUE_FALTA` que nadie había abierto.** El **5** dice textual:
   *"OTA que distinga A/B en `firmware_versions` (hoy comparten target
   `emisor`)"*. Estaba sin branch desde julio, con una sola nota debajo —
   apuntando al rescate post-OTA del 09-01 — que dice *"un push mal targeteado a
   un emisor en planta no tiene vuelta atrás remota"*. Eso es el síntoma; esto
   es la causa.
2. **Es la mitad que faltaba del trabajo de OTA ya hecho.** Las noches del 09-01
   (`ota_rescue.h`) y del 07-31 cubrieron *qué pasa si el `.bin` no arranca*.
   Ninguna cubrió *si el `.bin` es el correcto y si es más nuevo*. Un rollback
   perfecto no ayuda contra un binario que arranca **bien** y mide **al revés**.
3. **Se hace entera sin hardware** y no colisiona con nada abierto.
4. **La ventana se cierra.** Después de octubre las tres cajas están atornilladas
   al REDLER, y el eje gira. La vuelta atrás de un OTA equivocado deja de ser un
   comando y pasa a ser una subida con un cable USB.
5. **Frioseguro ya tuvo el turno de esta noche** (es PLATA, prioridad #1). El
   segundo turno le toca a octubre, y galgas es el que tiene competencia adentro
   del cliente.

## Lo que encontré, en orden de gravedad

### 1. El `.bin` del hermano entraba sin que nadie chequeara nada

El cliente pregunta por su fila propia o, si no hay, por la global de su tipo:

```
or=(device_id.eq.<id>, and(device_id.is.null, device_type.eq.emisor))
```

`protocol.h` le da a A y a B **el mismo `device_type`**. Así que una fila
publicada como global para `emisor` **le aplica a los dos**. Y los binarios no
son intercambiables:

| | ESP-A | ESP-B |
|---|---|---|
| `DEVICE_ID` | `"A"` | `"B"` |
| `OFFSET_SIGN` | `+1` | `−1` |

Cross-flashear no rompe nada visible. Los dos nodos siguen despertando,
midiendo y publicando a `readings`; sólo que ahora **hay dos filas firmadas
"A"** y la deflexión de uno viene con el signo invertido. La lógica de detección
de cadena cortada **es** la comparación entre A y B. Con esto adentro compara
cualquier cosa, con números que siguen siendo plausibles.

> Es el mismo patrón que el `CMD_SET_POTENCIA` del 09-05 y el "OK vacío" del
> 08-28: el sistema no falla, contesta bien y hace otra cosa.

### 2. La décima release nunca llegaba

```c
if (strcmp(latest_version, current_version) <= 0) return false;   // las 2 rutas
```

`strcmp("0.10.0", "0.9.0")` da negativo porque `'1' < '9'`. Un nodo en `0.9.0`
no ve `0.10.0`, ni `0.11.0`, ni `0.20.0`: el orden alfabético las entierra a
todas hasta que aparezca un `1.x`. **El RX ya está en el séptimo escalón de la
serie 3.6.x**, así que `3.6.10` es la cuarta release desde hoy.

Y el sufijo lo empeora: con `strcmp`, `3.6.7-RX-palways` acepta cualquier
sufijo que empiece con letra mayor que `'p'` y rechaza los menores. `-lora` no
entraría; `-rc1` sí. La decisión de flashear dependía de una letra del nombre.

### 3. `FirmwareUpdate` sin inicializar

Los tres sketches declaran `FirmwareUpdate fw;` en el stack. Si la fila no traía
`sha256`, el cliente no lo escribía y `supabaseDownloadFirmware()` le hacía
`strlen()` a basura de stack. Hoy las dos rutas hacen
`memset(out, 0, sizeof(*out))` al entrar.

## Qué se entregó

`firmware/shared/fw_version.h` — **puro** (sin Arduino, sin HTTPClient, sin
ArduinoJson, sin `Serial`) e **incluido** por `supabase_client.cpp`: no es un
espejo, lo que se testea es lo que se flashea. Mismo criterio que `ota_rescue.h`,
`trama_revd.h` y los `*_model.h` de FrioSeguro.

**Dos reglas, en un solo `fwUpdateDecide()` que usan las dos rutas del cliente:**

- **R1 — el orden es numérico.** Es update sólo si la terna
  `(major, minor, patch)` es **estrictamente mayor**. Misma terna con distinto
  sufijo **no** es update: si lo fuera, dos builds del mismo número se
  instalarían uno al otro para siempre.
- **R2 — el destino se ancla en la identidad ya flasheada.** Si la versión que
  corre lleva etiqueta (`-A-`, `-B-`, `-RX-`), el candidato tiene que llevar la
  misma. Se evalúa **antes** que R1: que el `.bin` del hermano además sea más
  nuevo lo empeora, no lo mejora.

R2 **no necesita columna nueva, ni migración, ni parámetro nuevo**: la etiqueta
ya viajaba dentro de `version` en los tres sketches (`0.8.1-A-otatest`,
`0.8.1-B-otatest`, `3.6.7-RX-palways`), sólo que nadie la leía. Un nodo
etiquetado no puede recibir el binario de otro; uno sin etiquetar no queda
encerrado.

**Ante cualquier duda, no actualizar**, con el motivo impreso en el log serie
(`no es mas nueva`, `es el .bin de otro device`, `version ofrecida no parsea`,
`version demasiado larga`…). Un OTA que no ocurre se reintenta el próximo wake;
uno equivocado sobre una caja en planta se arregla subiendo al REDLER.

## ⚠️ Cambio operativo al mergear — leer antes de publicar el próximo firmware

Los tres nodos corren versiones etiquetadas, así que **una fila sin etiqueta ya
no les entra**. Para actualizar A se publica `0.9.0-A-<algo>`; para B,
`0.9.0-B-<algo>`; para el RX, `3.7.0-RX-<algo>`.

Es exactamente lo que el ítem 5 pedía, pero es un cambio de procedimiento.
**Antes del merge conviene mirar si en `firmware_versions` del proyecto real ya
hay filas sin etiqueta**: después del merge dejan de aplicarse, y eso es lo
correcto, pero mejor saberlo que descubrirlo como "el OTA no anda". Es una query
de una línea. [@backend]

## Cómo verificarlo (comandos exactos, sin hardware, ~8 minutos)

```bash
cd C:\Proyectos\galgas
git fetch origin
git checkout nocturno/local-2026-09-08-b-la-version-que-nunca-sube

# 1) la decision, contra el header que se flashea
g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_fw_version.exe tools/test_fw_version.cpp
./tools/test_fw_version.exe

# 2) que los tests sirvan: reimplantar los defectos y ver que mueran
python tools/mutantes_fw_version.py

# 3) que la regla R2 este sostenida por los config.h reales del repo
python tools/check_fw_version_tags.py --mutantes

# 4) y que el mismo checker REPRUEBE main (donde el strcmp sigue vivo)
python tools/check_fw_version_tags.py --root <otro-checkout-en-main>

# 5) las tres familias compilando
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_a_emisor
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_b_emisor
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_rx_receptor
```

El paso 5 necesita `firmware/<sketch>/secrets.h` (está en `.gitignore`; esta
noche lo copié del checkout de trabajo y **no viaja en el commit**).

**Resultados obtenidos esta noche:**

- `test_fw_version.exe` → **84 checks, 0 fallos, sin warnings**. Cuatro bloques
  están escritos como **regresión**: fallan contra el `strcmp`.
- `mutantes_fw_version.py` → **12/12 mutantes muertos**, header restaurado y
  suite re-corrida en verde después. El mutante 1 es literalmente la línea vieja.

  | mutante | qué reimplanta | checks que fallan |
  |---|---|---|
  | 1 | vuelve el `strcmp`: la versión se compara alfabéticamente | 8 |
  | 2 | el orden mira sólo el major | 13 |
  | 3 | la misma terna cuenta como update (un rebuild se instala a sí mismo) | 6 |
  | 4 | se acepta el downgrade | 8 |
  | 5 | R2 desaparece: el `.bin` del hermano entra | 13 |
  | 6 | R2 se evalúa después de R1 | 1 |
  | 7 | la fila global sin etiqueta se acepta en un nodo etiquetado | 2 |
  | 8 | una versión que no parsea se toma como update igual | 3 |
  | 9 | el parser acepta menos de tres componentes | 2 |
  | 10 | el parser acepta sufijo sin guion (`0.9.0rc1`) | 2 |
  | 11 | la etiqueta se detecta sin distinguir mayúsculas | 1 |
  | 12 | no se chequea que la versión entre en el buffer | 1 |

- `check_fw_version_tags.py --mutantes` → **37 chequeos, 0 fallas** y **5/5**
  etiquetas rotas detectadas (A sin etiqueta · A etiquetado como B · etiqueta en
  minúscula · versión fuera de gramática · versión que no entra en el buffer).
  `config.h` restaurado y re-chequeado en verde.
- El mismo checker con `--root` contra un checkout de `main` → **31 chequeos,
  5 fallas**. Lo reprueba, que es lo que tiene que hacer.
- **Compilación de las tres familias** → exit 0, **0 warnings**:

  | sketch | main | branch | delta flash | delta RAM |
  |---|---|---|---|---|
  | esp_a_emisor | 1.237.004 B | 1.237.748 B | **+744 B** | 0 |
  | esp_b_emisor | — | 1.237.748 B | — | 0 |
  | esp_rx_receptor | 1.235.860 B | 1.236.584 B | **+724 B** | 0 |

  Los tres al 62 % de flash y 18 % de RAM.

## Qué quedó SIN verificar (pide banco)

1. **Un OTA real de punta a punta con la regla puesta.** Publicar
   `0.9.0-A-<algo>` para A y verlo descargar; publicar una fila **sin etiqueta**
   y ver en el log serie `es el .bin de otro device`. Media hora con un ESP32 y
   el bucket. [@firmware + @backend]
2. **El caso `0.10.0` sobre una placa.** La aritmética está testeada en el host;
   falta verlo instalar sobre un nodo que corre `0.9.0`.
3. **Qué hay hoy en `firmware_versions` del proyecto real.** Ver el punto
   "cambio operativo" de más arriba. [@backend]

## Lo que NO hice, a propósito

- **El bucket sigue público** (ítem 6 del `QUE_FALTA`: `firmware` sin URL firmada
  ni TTL). Es un hueco de seguridad, no de correctitud, es de `@backend` y toca
  políticas de Storage: su propio branch.
- **No agregué una columna `target` a `firmware_versions`.** Sería una migración,
  un cambio de contrato y **otra copia del dato que se puede desincronizar** con
  la que ya viaja dentro de `version`. Si algún día hace falta un destino que la
  versión no puede expresar, ahí sí.
- **Nada ata el `.bin` descargado a un `device_id`.** El `sha256` de la fila se
  verifica byte a byte (eso ya estaba y está bien), pero si alguien sube el
  binario de B con la versión `0.9.0-A-x`, entra en A. **La etiqueta protege del
  error de publicación, no de un `.bin` mal armado.** La barrera que faltaría es
  que el propio binario declare su `DEVICE_ID` y el nodo lo mire antes de
  `Update.end()`. Escribirlo esta noche era inventar un formato de metadato en el
  binario sin nadie del otro lado que lo produzca. [@firmware]

## Anotado y NO tocado

- **`main` tiene cinco `.exe` de test commiteados** en `tools/`
  (`test_cal_model`, `test_forward_queue`, `test_gateway_route`,
  `test_ota_rescue`, `test_potencia_tx`). El de esta noche **no** viaja en el
  commit (se regenera con g++). Sacar los otros del repo es una limpieza de un
  minuto que no hice para no mezclarla con esto. **Segunda noche que se anota
  lo mismo** — el 09-08 lo anotó para frioseguro. [@bibliotecario]
- **El ítem 3 del `QUE_FALTA` de galgas sigue duplicado como 3 y como 4b**, con
  el mismo texto (lo dejó anotado el 09-05). No lo toqué: arreglarlo garantiza
  un conflicto con el branch `09-03`. Se resuelve al mergear ése. [@cronista]
- **`fw_version.h` es candidato a la biblioteca.** Es genérico —"¿esta versión
  es una actualización para mí?"— y FrioSeguro tiene su propio OTA con el mismo
  problema latente. No lo coseché para no cosechar algo que todavía no se probó
  en hardware. Cuando pase el punto 1 de "sin verificar", va. [@bibliotecario]

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-08-b-la-version-que-nunca-sube`
  (`f7df5a2`), sobre `origin/main` (`49c238d`).
- `QUE_FALTA.md` de galgas actualizado (ítem 5, con el aviso del cambio
  operativo).
- Worktree `C:\Proyectos\_noche_galgas_0908b` eliminado; el árbol de `galgas`
  quedó **idéntico**, en `nocturno/local-2026-09-05-la-potencia-que-nadie-cambio`
  y sin archivos sueltos.
- Ni el `.exe` del test ni los `secrets.h` viajan en el commit.
- En MATI-HQ quedaron **sin commitear, tal como los encontré**,
  `comercial/panamerican/PRESUPUESTO_CERRO_MORO_INTERNO.html`, `dominios/pcb.md`
  y `scripts/turno_noche_log.txt`: son de otro trabajo y no me corresponde
  firmarlos.
- Nada corriendo, nada abierto.
