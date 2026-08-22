# Nocturno local — 2026-08-21-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la jerarquía).
**Branch:** `nocturno/local-2026-08-21-b-cuanto-hace-que-esta-prendido` (pusheado, `53f8f2c`).
**Sale de:** `main`. **No depende de ningún otro branch nocturno** — toca
`web-dashboard/src/lib/uptime.js`, archivo nuevo que no pisa el
`lib/freshness.js` del `08-19-b`. Los dos branches crean `src/lib/`; git lo
resuelve solo.

## TL;DR

> **El equipo que mejor está era el que peor se veía.**

FrioSeguro se cobra como servicio de continuidad. El número que dice si un
equipo es confiable —hace cuánto que está prendido sin reiniciarse— mentía en
dos capas independientes, y las dos mentían **en contra del equipo estable**.

**Capa 1, el número.** `millis()` en el core ESP32 es `uint32_t`: da la vuelta a
los **49,7 días**. El firmware publicaba `uptime_sec` en **cuatro** sitios y con
**dos definiciones distintas**:

| dónde | qué calculaba | desde |
|---|---|---|
| `supabase.h:213` (PATCH a `devices`) | `millis() / 1000` | el boot |
| `supabase.h:288` (POST a `readings`) | `millis() / 1000` | el boot |
| `firmware_modular.ino:300` (payload nube) | `(millis() - state.uptime) / 1000` | el **setup** |
| `web_api.h:70` (`/api/status`, página local) | `(millis() - state.uptime) / 1000` | el **setup** |

Las dos dan la vuelta. A los 60 días el panel informaba 10. Y **además difieren
entre sí**: `state.uptime` se sellaba en `setup()` *antes* de conectar el WiFi,
así que **la fila de Supabase y la página local del propio equipo nunca decían
exactamente lo mismo** — la diferencia es lo que tarde el arranque.

**Capa 2, el texto.** El mismo número se formateaba en **tres** lugares, con
tres criterios, y **ninguno tenía unidad de días**:

| dónde | 60 días se veían |
|---|---|
| `App.jsx::formatUptime` — **la vista del comercio** | `1440:00:00` |
| `html_ui.h::formatUptime` — página local del ESP | `1440h 0m` |
| `DevicesAdminTable.jsx::fmtUptime` | `60d 0h` ← el único correcto |

Y un cuarto hueco que aparece solo cuando se ponen los tres al lado: los tres
empezaban con `if (!sec)`. **Un equipo que arrancó recién (`uptime_sec === 0`)
se mostraba idéntico a un equipo del que no hay dato.** Es exactamente al revés
de lo útil: que se acaba de reiniciar es la información más importante que ese
campo puede dar.

## Tarea elegida y por qué

Por rotación tocaba **frioseguro**: los tres turnos previos fueron galgas
(08-21), datalogger (08-20) y frioseguro (08-19-b) — el más viejo de los cuatro
repos era frioseguro, y encima es **PLATA = prioridad #1** de la jerarquía. Sin
conflicto entre rotación y jerarquía.

Descarté `cosechador` por la misma razón de las últimas siete noches, que dejo
dicha de nuevo para no re-decidirla: es **P2**, todo su `QUE_FALTA` está
bloqueado por la compra, el repo no tiene una línea de código (4 docs y 2 PDFs)
y ya acumula cuatro análisis sobre el mismo material.

**Quinta noche seguida en que la tarea la elige un pendiente ya nombrado.** La
auditoría `08-16-b-cadena-tiempo` dejó siete hallazgos con dueño y número. `T4`
y `T5` los cerró el turno del 08-19-b. De los que quedaban:

- `T1`, `T2`, `T3` son **la misma pregunta de fondo** —*¿el equipo necesita
  reloj?*— y el propio informe la marca como **decisión de `@firmware`, no
  bug**. No se decide de noche.
- `T7` es una línea de doc de `@backend`.
- **`T6` es software puro, es un número que miente, y el informe ya midió su
  daño**: *«el equipo más estable del parque es el que peor se ve»*.

Elegí `T6`. Fui a buscar sólo la capa 1 (el rollover) y la capa 2 apareció al
abrir los formateadores — que es la misma forma que tuvo la noche del 08-19-b
con la frescura, y por la misma causa: **la cuenta duplicada en N lugares que no
se conocen entre sí.** Este repo tiene ese patrón instalado.

## Lo que hay ahora

### `firmware_modular/uptime.h` (nuevo)

```c
inline uint32_t uptimeSec() { return (uint32_t)(esp_timer_get_time() / 1000000LL); }
inline uint32_t uptimeMin() { return uptimeSec() / 60; }
```

`esp_timer_get_time()` es **API nativa del ESP-IDF que ya viene con el core**:
microsegundos desde el boot en `int64_t`, no da la vuelta (~292.000 años). Cero
dependencias, cero código nuevo de mi parte.

**La decisión de diseño que conviene revisar** es que descarté el contador de
rollover hecho a mano, que es la respuesta de manual:

```c
if (now < last) high++;   // <- NO
```

Ese exige ser llamado **al menos una vez cada 49,7 días** o pierde una vuelta en
silencio, y encima no es seguro llamarlo desde una ISR. Es una invariante que
hay que sostener para siempre, a cambio de nada, cuando el chip ya trae el
contador de 64 bits hecho. *(Anti-sobre-ingeniería: nativo antes que código
nuevo. Chequeé `C:\Proyectos\biblioteca` primero — `esp32\` está vacío y no hay
nada de uptime; tampoco vale la pena cosechar tres líneas que envuelven una API
del sistema.)*

Los cuatro sitios llaman ahora a la misma función, y **eliminé
`SystemState.uptime`**: era el campo que sostenía la segunda definición. Un dato
duplicado que no se puede desincronizar porque ya no existe.

### `web-dashboard/src/lib/uptime.js` (nuevo)

Una sola función, con **la misma regla que `freshness.js`** del 08-19-b:

> Si no se puede afirmar el dato, se dice que no se sabe. Nunca se inventa un cero.

`uptimeInfo(raw)` clasifica en `missing` / `invalid` / `ok`, y acepta `number` o
**string numérico** — porque PostgREST devuelve las columnas `int8` como string,
así que si algún día `uptime_sec` se ensancha esto no se rompe.

`formatUptime(raw)`: dos unidades como máximo, la más grande primero.

```
2d 3h  ·  5h 12m  ·  7m  ·  45s  ·  0s (arrancó recién)  ·  — (sin dato)
```

**Para todo valor ≥ 60 s da exactamente lo mismo que el `fmtUptime` viejo de la
tabla admin.** Hay un test que lo barre de 60 s a 400.000 s comparando contra
una copia literal del formateador viejo. El cambio de conducta está sólo donde
estaba el bug.

### `firmware_modular/html_ui.h`

El formateador de la página local del ESP, reescrito con las mismas reglas.
⚠️ **Son dos copias de la misma regla y no hay import posible entre ellas** (una
va en el bundle, la otra vive dentro de un string de C). Queda escrito en el doc
que se tocan juntas, con la comprobación de paridad para verificarlo.

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-21-b-cuanto-hace-que-esta-prendido

cd web-dashboard
node --test src/lib/uptime.test.js     # 12 tests, < 1 s, sin red
npm run build

cd ..
arduino-cli compile --fqbn esp32:esp32:esp32 firmware_modular
```

**Lo que verifiqué yo, corriendo:**

- **12/12 tests OK** (`node --test`).
- **`npm run build` OK** (vite, 4,4 s).
- **eslint**: `src/lib/` **limpio**; los dos `.jsx` tocados dan **exactamente**
  los mismos **4 errores / 4 warnings** que sus versiones de `main` (comparado
  archivo por archivo contra `git show main:...`). **Cero nuevos.** El total del
  repo sigue en 31 errores / 7 warnings preexistentes.
- **`arduino-cli compile` OK.** Contra el baseline de `main` compilado antes de
  tocar nada (**1288696 B**, el mismo número que registró el informe del 08-18):
  **+132 B de flash** y **−8 B de RAM**. De los 132, **124 son los caracteres
  del JS embebido** en `html_ui.h` — o sea el C++ propiamente dicho pesa ~**+8
  bytes**. Los −8 de RAM son el campo eliminado del `SystemState`.
  ⚠️ **Ojo: el sketch está al 98 % del flash** (1288828 / 1310720). No lo causa
  este branch, pero cualquier cosa que se agregue de acá en más va a chocar
  contra ese techo. **Vale como aviso para `@firmware`.**
- **Paridad ESP ↔ dashboard**: extraje el `formatUptime` de `html_ui.h` y lo
  corrí contra `lib/uptime.js` en **17.332 valores de 0 a 200 días** →
  **0 divergencias**. La única diferencia deliberada es el marcador de sin-dato:
  `--` en la página del ESP (el placeholder que ya usaba `html_ui.h:76`) y `—`
  en el dashboard.
- **Mutación** — que los tests sean red y no decorado. Seis mutantes, los seis
  caen:

  | mutante | tests que fallan |
  |---|---|
  | sacar la unidad de días (**el bug T6**) | **7** |
  | cambiar el formato de minutos | 4 |
  | volver al `!sec` (0 == sin dato) | 2 |
  | aceptar uptime negativo | 1 |
  | no validar `NaN`/`Infinity` | 1 |
  | no truncar fraccionarios | 1 |

- Neto **−14 líneas** en los archivos tocados (sin contar los nuevos).

## Qué quedó sin verificar por hardware

1. **Que una placa flasheada informe el uptime correcto.** Es una placa WiFi, el
   monitor serie y `curl http://<ip>/api/status`. Se ve en un minuto.
2. **Que el número coincida entre `/api/status` y la fila de Supabase.** Es la
   mitad del arreglo que no se puede ver de otra forma: antes diferían por lo
   que tardaba el arranque, ahora tienen que dar igual (±1 s por el redondeo).
3. **Los 49,7 días de verdad** no se pueden esperar. Lo que sí se puede es
   confirmar que `esp_timer_get_time()` devuelve lo mismo que `millis()` en los
   primeros minutos, que es lo que dice que la base está bien.

Nada de esto necesita nube ni cliente: una placa y el monitor serie.

## Lo que este branch NO hace (a propósito)

- **No agrega un contador de arranques.** `T6` lo sugería como alternativa
  (*«publicar el rollover o un contador de boots»*). El rollover ya no existe,
  así que esa mitad se cae sola; el contador de boots implica **escrituras a NVS
  y su desgaste** → es una decisión de `@firmware`, no la corrección de un
  número que miente.
- **No toca `HistoryPoint.timestamp`**, que también guarda `millis()` crudo.
  Puede: ese buffer se escribe en `updateHistory()` pero **no lo lee ni lo sirve
  nadie** en todo el firmware. Es código muerto. Sacarlo o servirlo es una
  decisión, no un bug — y mezclarla acá habría ensuciado el commit.
- **No toca ninguna columna de Supabase** ni ningún nombre de campo del JSON.
- **No arregla T1/T2/T3** (el firmware sigue sin reloj). Esto arregla *hace
  cuánto que el equipo está prendido*, que se mide con el reloj interno; no
  *cuándo pasó algo*, que necesita hora real.

## Copy que cambia y necesita ojos

**La vista del comercio pasa de `HH:MM:SS` a `2d 3h`.** Es el punto entero de
T6 —`1440:00:00` no lo lee nadie— pero es **texto que ve el cliente que paga**:

- **`@diseno`**: aprobar (o corregir) la forma. Está en un solo lugar ahora, así
  que cambiarla es una línea de `lib/uptime.js`.
- **`@tester`**: verlo con un device reportando. La tabla admin no debería
  cambiar en nada visible; la vista del comercio sí.

## Hallazgo lateral, para el que mergee el branch del 08-18

Sin relación con este arreglo, pero lo encontré revisando qué archivos publican
el uptime y corrige una instrucción de verificación ya escrita:

> **`firmware_modular/serial_api.h` no está `#include`-ado en ningún lado.** No
> se compila. Es código muerto.

El informe del **08-18** dice, en el paso 1 de su verificación en hardware:
*«se cierra flasheando una placa WiFi y forzando defrost (`serial_api.h` ya
tiene el comando…)»*. **Ese comando no existe en una placa flasheada.** La otra
mitad de la frase sí vale: `web_api.h:221` togglea el defrost desde la página
local, y ése es el camino que funciona.

No lo arreglé: incluir un archivo de ~400 líneas que nunca se compiló es un
cambio grande, con el flash al 98 %, y no tiene nada que ver con esta tarea.
**Queda para `@firmware`: o se incluye y se compila, o se borra.**

## Estado del repo al cerrar

`frioseguro` tiene ahora **14 branches nocturnos sin mergear**. Este sale de
`main` limpio y no depende de ninguno. Dejé sin tocar todo lo que Matías tiene
sin commitear en el working tree (`firmware_revival/`, `kit_santacruz/`,
`backup_supabase/`, los zips de Santa Cruz, `supabase/BOOTSTRAP_2026-08-19.sql`,
`supabase/migration_device_logs.sql`): **nada de eso entró al commit**.

En **MATI-HQ** sí commiteé los `dominios\` que habían quedado modificados del
turno de día (`comercial`, `diseno`, `frontend`, `pcb` — la entrada de EMSICA de
`@frontend`, entre otras) para que no quedaran colgando: mi propia entrada va en
`dominiosrontend.md` y `dominiosirmware.md`, y no podía separarlas del
resto del archivo.

`scripts/turno_noche_log.txt` **no lo pude escribir**: el `.bat` que lanza el
turno lo tiene abierto con lock exclusivo (es su redirección de salida), así que
`Permission denied`. El resumen de la noche está acá y en las dos bitácoras.
