# Nocturno local — 2026-08-21

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (P0 — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-21-presupuesto-silencio` (pusheado, `0e90168`).
**Sale de:** `main`. **No depende de ningún otro branch nocturno.**

## TL;DR

> **El emisor que se flashea para octubre se veía OFFLINE en el dashboard,
> siempre, aunque estuviera perfecto.**

El SCADA decide si un device está caído con una sola cuenta: *¿hace cuánto que
no habla, y cuánto silencio es normal para él?* El segundo número —el
**presupuesto de silencio**— estaba escrito en **cuatro lugares** que no se
conocían entre sí, y **tres de los cuatro lo adivinaban parseando el string de
versión del firmware** con `/-(p[a-z]+)$/`.

Los emisores modulares versionan `0.8.1-A-otatest`. No matchea. Cae al fallback.
Y el fallback (**300 s** en `App.jsx`) es **más corto que el período real del
device** (600 s en `MODE_NORMAL`). No hace falta que se rompa nada: un emisor
sano, reportando puntualmente, se pinta rojo para siempre.

Las dos tablas de perfiles, además, discrepaban en **los cinco**:

| perfil | sleep real | App.jsx | PlantaView | ahora |
|---|---|---|---|---|
| pmax | 3600 s | 5460 s | 5400 s | 5460 s |
| pnorm | 600 s | 960 s | 900 s | 960 s |
| psim | 60 s | 150 s | 90 s | 150 s |
| palerta | 10 s | 75 s | 30 s | 75 s |
| palways | sin sleep (hb 30 s) | 105 s | **60 s** | 105 s |
| (modular, sin sufijo) | según modo | **300 s** | 600 s | según modo |

Los dos números en negrita son los que muerden hoy: el de abajo es el emisor de
octubre, y el `palways` de 60 s es el **RX**, que manda heartbeat cada 30 s —
**dos heartbeats exactos de presupuesto, sin margen para un reintento de WiFi.**

## Tarea elegida y por qué

Por rotación tocaba `galgas` (el último fue 08-19; después vinieron frioseguro y
datalogger). Descarté `cosechador` por la misma razón de las últimas seis
noches, que dejo dicha para no re-decidirla: es P2, todo su `QUE_FALTA` está
bloqueado por la compra y ya acumula cuatro análisis sobre el mismo material.

**Cuarta noche seguida en que la tarea la elige un pendiente ya nombrado.** La
auditoría de la cadena de entrega (08-11) dejó dos hallazgos de `@frontend` con
nombre y número, D7 y D5, y los dejó escritos en el `QUE_FALTA`:

> *«**D7** — el `FW_VERSION` de los emisores modulares (`0.8.1-A-otatest`) no
> matchea el regex de perfil de las dos vistas → **un emisor modular sano se ve
> permanentemente OFFLINE**, y es la familia que se flashea para octubre.
> **D5** — el presupuesto de silencio está escrito tres veces y las dos vistas
> discrepan en los 5 perfiles.»*

Elegí esos dos. Son de la vista que mira Dreyfus, son software puro y **el
branch que los descubrió es una auditoría: nadie los había arreglado.**

## Lo que la auditoría no había visto

El hallazgo escrito hablaba de **un regex y dos tablas**. En el repo eran
**cuatro copias, tres regex y un bug de CSS**:

- La **cuarta** copia no estaba en ninguna tabla: `PlantaView.seenClass` usaba
  `ageMs/1000 > 60 → ámbar`, **60 s fijos para todos**. Le pintaba de amarillo
  el "hace 45m" a un device `pmax` que está durmiendo su hora reglamentaria.
- El **tercer** regex vivía en `FirmwareView.jsx` y era distinto: `/-(p\w+)$/`,
  con `\w` en vez de `[a-z]`. Un criterio propio de qué cuenta como perfil.
- `App.jsx` tenía además `TIMEOUT_S = 300` con el comentario *"5 min sin
  contacto = emisor apagado"* — **una constante muerta**, no la leía nadie.
- Y el de CSS, que apareció al ir a agregar una clase:

  ```jsx
  <span className={`word ${(stage || 'normal').toLowerCase()}`}>{stage || 'OFFLINE'}</span>
  ```

  Sin `stage`, el **texto** dice `OFFLINE` y la **clase** es `normal`, que en
  `redler.css` es verde. **OFFLINE pintado de verde.** Es literalmente el mismo
  patrón que el `Sin datos` verde de FrioSeguro del 08-19-b: el fallback del
  texto y el fallback de la clase no acuerdan y nadie los mira juntos.

## El defecto de fondo (por qué no alcanzaba con arreglar el regex)

La tentación era agregar `otatest` a la tabla. Habría tapado el síntoma de hoy y
dejado el defecto intacto:

> **La versión del firmware es una etiqueta de compilación. El período no.**

El período real del emisor modular vive en NVS y lo cambian, en caliente, tres
cosas — y ninguna toca `FW_VERSION`:

- `CMD_SET_PERIOD_S`,
- `CMD_SET_MODE` (cada `OperationMode` tiene su período),
- **el propio self-trigger**: `updateAlertState()` pasa el nodo a `MODE_ALERTA`
  y con eso de 600 s a **10 s**.

O sea: aun con el regex arreglado, un emisor que entra en alerta —el momento en
que más importa mirarlo— tendría un presupuesto 96× más largo del que le
corresponde. El dato lo tiene el device; el dashboard lo estaba adivinando desde
el nombre del binario.

De paso: el `-palways` del RX (`3.6.7-RX-palways`) es una etiqueta **heredada**
de la familia `ota_wm_pp`. El sketch del RX **no define ni `PROFILE_SUFFIX` ni
`SLEEP_PERIOD_S`.** Que hoy sea el sufijo correcto es una coincidencia sostenida
a mano.

## Qué hice

### 1. `web/src/lib/silence.js` — la única cuenta

`reportPeriod(device, lastReading)` resuelve el período **por orden de
autoridad**, y dice de dónde lo sacó:

| `source` | de dónde |
|---|---|
| `reported` | `metadata.period_s` (modular) o `metadata.sleep_s` / `always_on` (ota_wm_pp) |
| `mode` | `metadata.mode` → espejo de `defaultPeriodForMode()` |
| `profile` | sufijo de la versión → tabla `ota_wm_pp` (último recurso) |
| `unknown` | nada de dónde agarrarse |

Una sola fórmula de buffer (`max(60, ⌊p·1,5⌋+60)`, la que ya tenía `App.jsx`), y
período 0 —"sin sleep"— **no** es presupuesto 0: usa el heartbeat de 30 s.

### 2. Tres estados, no dos

`ok` / `silent` / **`unknown`**. El tercero es el que faltaba y es el que evita
mentir en las dos direcciones a la vez: `unknown` significa *no sé cada cuánto
habla este device*, que es una cosa distinta de *este device está caído*. La
primera se arregla en el dashboard; la segunda hace que alguien maneje hasta
planta.

Y `unknown` se usa lo menos posible: aun sin conocer el período, las **cotas de
la tabla** deciden la mayoría de los casos —más fresco que **75 s** (el
presupuesto más corto posible) está vivo cualquiera sea su perfil; más viejo que
**5460 s** (el más largo) está callado cualquiera sea su perfil. Sólo la franja
del medio queda en `unknown`.

Una fecha **futura** (reloj del navegador atrasado) da edad negativa y cae en
`ok`, nunca en `silent`. Mismo criterio que FrioSeguro el 08-19-b, con el signo
al revés: allá el peligro era decir "fresco", acá es decir "muerto".

### 3. Los seis call sites, apoyados en el módulo

`App.jsx` (`TransporterHealth`, `DeviceCard`, las tabs de Mission Control y
`DeviceControlHeader`), `PlantaView.jsx` (`computeStage`, `seenClass`,
`allOnline`) y `FirmwareView.jsx` (los tres regex). Se borraron
`getMaxSilenceSec`, `getProfileSuffix`, `SILENCE_S`, `TIMEOUT_S` y el `sleepS`
de `PP_PROFILES` (que se queda: es la UI para **elegir el .bin** de OTA, eso sí
es cosa de versiones).

Dos cambios de estado que valen aparte:

- **`allOnline`** era `every(stage !== 'OFFLINE')`. Con el estado nuevo eso
  habría contado a `UNKNOWN` como en línea. Ahora es una lista explícita de los
  stages que sí cuentan. Verde por descarte, otra vez, en un `!==`.
- **`TransporterHealth`** gana una última rama: si nada disparó pero A o B están
  en `unknown`, dice `SIN PRESUPUESTO DE SILENCIO en A` en ámbar, en vez de
  `Transportador OK` en verde.

### 4. `redler.css` — el agujero

`.card[data-stage="UNKNOWN"]` y `.word.unknown` en ámbar. Y el fallback del
`stage` pasó a ser `unknown` en **los dos lados** (texto y clase), así que
`OFFLINE` dejó de poder salir verde.

### 5. Firmware — que el device diga su período

`buildMetadata()` de `esp_a_emisor` y `esp_b_emisor`:

```c
meta["period_s"] = period_s;
```

Aditivo, sin cambio de comportamiento. **+24 B de flash, 0 de RAM** (medido:
1.235.360 → 1.235.384 B, comparando contra el mismo árbol con el cambio
stasheado). Con eso la familia modular deja de depender de que alguien mantenga
a mano una tabla en JS que espeje `protocol.h`.

### 6. `docs/silence-budget.md`

Las cuatro fallas con su cita de código, las dos tablas (recalculadas por un
comando, no tipeadas), el orden de autoridad y lo que falta.

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-21-presupuesto-silencio

cd web
node --test src\lib\silence.test.js     # 30 tests, ~0,15 s
npm run build                            # vite

cd ..
C:\Tools\arduino-cli\arduino-cli compile --fqbn esp32:esp32:esp32 firmware\esp_a_emisor
C:\Tools\arduino-cli\arduino-cli compile --fqbn esp32:esp32:esp32 firmware\esp_b_emisor
```

**Lo que verifiqué yo, corriendo:**

- **30/30 tests OK.** Puros: sin DOM, sin red, sin hardware; `now` es siempre un
  parámetro, así que no dependen del reloj de la máquina que los corre.
- **`npm run build` OK** (vite 5.4.21, 395 módulos, ~5 s).
- **Compilan A y B** (esp32 core, 1.235.384 B = 94 %, RAM 61.456 B sin cambio).
- **El delta de flash medido contra la base**, no estimado: +24 B.
- **Mutación** — que los tests sean red y no decorado:

  | mutación | resultado |
  |---|---|
  | fallback fijo, sin resolver por `mode` | **4 fallan** |
  | período 0 ⇒ presupuesto 0 (el bug de `palways`) | **3 fallan** |
  | `unknown` cae en `ok` (verde por descarte) | **1 falla** |
  | `unknown` cae en `silent` (OFFLINE por descarte) | **1 falla** |
  | el sufijo de versión gana sobre lo reportado | **1 falla** |
  | frontera `>=` en vez de `>` | **1 falla** |
  | fecha ilegible no se detecta | **1 falla** |
  | buffer sin el piso de 60 s | **8 fallan** |

  Restaurado → 30/30. **Ninguna sobrevivió.**

## Lo que quedó sin verificar (necesita banco / ojos)

1. **Que un ESP32 real escriba `period_s`** en `readings.metadata`. Todo corre
   sobre objetos sintéticos y sobre el **texto** del firmware. Es de @tester con
   un emisor y la tabla `readings`: mirar una fila después del primer wake.
2. **`StaticJsonDocument<320>` con el campo nuevo.** Son 8 miembros con claves
   literales (sin copia) y la cuenta da holgado, pero **si desbordara,
   `serializeJson` trunca en silencio**. Se ve en la misma fila del punto 1.
3. **La "ventana de un reporte"** — ver abajo.
4. **Nadie lo vio en pantalla.** Hay una etiqueta nueva (`UNKNOWN`, ámbar) y
   copys nuevos: `no se sabe`, `SIN PRESUPUESTO DE SILENCIO en A`, y una fila
   `período` en el header de Control. El copy es de **@diseno**; la pantalla, de
   **@tester**: 10 minutos.
5. **Un `pmax` con la red caída duerme 6 h** (`SLEEP_FAIL_FALLBACK_S = 21600`) y
   va a aparecer `OFFLINE` bastante antes (5460 s). Es correcto —no está
   reportando— pero conviene saber que un OFFLINE de un `pmax` puede ser
   "fallback de red" y no "muerto". **No lo modelé**: sería adivinar cuál de las
   dos, que es justo lo que este branch viene a sacar.

### La ventana de un reporte (lo que decidí NO tocar, con la razón)

`period_s` se manda en el POST (paso 8 del wake) y `updateAlertState()` corre
**después** (paso 9). En una transición de modo, lo reportado es el período de
**este** wake y el próximo sleep ya es otro. Dura **un solo reporte**:

| transición | reporta | duerme | efecto |
|---|---|---|---|
| NORMAL → ALERTA | 600 s | 10 s | presupuesto generoso de más (960 s vs 75 s) |
| ALERTA → NORMAL | 10 s | 600 s | presupuesto corto de más: **un OFFLINE espurio** |

El segundo es cry-wolf y molesta. La corrección obvia es mover
`updateAlertState()` antes del POST — pero esa llamada **también** incrementa
`rtc_alert_streak`, que va en la misma metadata, y de ella depende `r.stage`. O
sea: mover una línea cambia dos campos más del reporte. **Eso es un cambio de
máquina de estados en el firmware de producción, y no se hace de noche sin
banco.** Queda anotado en el comentario de `buildMetadata()` en los dos
sketches, en el doc y acá, con dueño: **@firmware**.

## Lo que este branch NO toca

- **Ningún umbral de medición**: `TH_VPP_ALERT`, `TH_VPP_MONITOR`, `TH_V`,
  `TH_RATIO`, `TH_BATT_LOW` quedan como estaban. Esto es el eje del **tiempo**,
  no el de la señal.
- **No toca la lógica de alertas, ni los eventos, ni el self-trigger, ni el
  guard/hold del 08-19.** Cambia cuánto silencio se tolera, no qué se considera
  una rotura.
- **`PP_PROFILES` sigue vivo** para elegir el `.bin` de OTA: eso sí es cosa de
  sufijos de versión y ahí el regex es el correcto.
- **No toca Supabase, ni el schema, ni migraciones, ni el RX, ni el gateway.**
- **No toqué `hardware/`** (trabajo sin commitear de Matías, ver higiene).

## Nota para el Director

Lo que agrega esta noche al patrón: **el arreglo salió de un branch de auditoría
que estaba sin implementar hace diez días.** `galgas` tiene 12 branches nocturnos
sin mergear y la mayoría son análisis; D7 estaba escrito, con su evidencia y su
dueño, desde el 08-11. Nadie lo tocó. La auditoría no es el arreglo, y a esta
altura del año hay más hallazgos escritos que hallazgos cerrados.

Segundo, y es el mismo comentario que dejé el 08-20 con otro ejemplo: **el
hallazgo escrito era la punta.** El informe decía "un regex y dos tablas";
había cuatro copias, tres regex, una constante muerta y un OFFLINE pintado de
verde. La auditoría busca por síntoma; el arreglo va a buscar **todos los
lugares que hacen la misma cuenta** y siempre hay más.

Tercero: **este branch sale de `main` y no depende de nadie.** De los 12 de
galgas es el único del que se puede decir eso hoy, y arregla algo que se ve a
simple vista en la vista que mira Dreyfus. Si querés bajar el contador con algo
barato y verificable —`node --test` + `npm run build` en 6 segundos— es el
candidato.

**Próximo paso concreto:** mergear `08-21-presupuesto-silencio` (independiente),
y en paralelo la cadena de alertas en orden: `08-17-b-eventos-alerta` →
`08-19-guard-self-trigger`.

---

**Higiene del cuartel:**

- ⚠️ **`C:\Proyectos\galgas` tiene trabajo de día SIN COMMITEAR**: la carpeta
  `hardware/` entera, sin trackear. **No la toqué** y verifiqué que sigue igual
  después de mis cambios de branch. Matías: si eso es el diseño de la placa,
  vive sólo en este disco.
- ⚠️ **MATI-HQ sigue con los mismos 16 modificados + los sin trackear** de los
  informes anteriores (`comercial/`, `DREYFUS_ESQUEMATICO.*`, `backups/`,
  `propuestas/MAIL_SAE_PPS.md`, `agentes/diseno3d.md`…). **No los toqué ni los
  commiteé.** Este commit sólo agrega este informe.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío. El latido de DESKTOP-RK8DH7C
  sigue parado desde el **2026-08-07** (14 días).
