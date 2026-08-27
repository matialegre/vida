# Nocturno local — 2026-08-27

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA** — prioridad #1 de la jerarquía).
**Branch:** `nocturno/local-2026-08-27-el-testigo-que-certificaba` (pusheado, `b679b11`).
**Sale de:** `main` (`ddf5134`). **No depende de ningún otro branch nocturno.**
Roza `web_api.h` y `html_ui.h`, que también tocan `08-26-el-hueco-y-el-reloj` y
`08-21-b-cuanto-hace-que-esta-prendido`, pero en líneas distintas: son adiciones,
no reescrituras. Se puede mergear en cualquier orden.

## TL;DR

> **El único detector capaz de ver el portal cautivo era el que lo certificaba
> como bueno.**

`firmware_modular/wifi_utils.h`, una línea:

```c
state.internetAvailable = (httpCode == 204 || httpCode == 200);
```

`http://www.google.com/generate_204` existe **exactamente** para separar dos cosas:

| Qué hay del otro lado | Qué contesta |
|---|---|
| Internet de verdad | **204**, sin cuerpo |
| Portal cautivo (WiFi abierto ajeno) | **200** con el HTML del login, o **302** hacia él |
| Router prendido sin uplink / ISP suspendido | **200** con la página del ISP |

El `|| httpCode == 200` **anulaba la única prueba que sabía distinguirlos**.

Y no es un flag cosmético: `state.internetAvailable` es **la compuerta de todo
lo que se cobra**. Veinte `return` tempranos en `supabase.h`, más las ramas de
Telegram en `alerts.h`, `door_sensors.h`, `current_sensor.h` y `power_monitor.h`.
Con el equipo declarándose ONLINE, esas llamadas salían y **fallaban contra el
portal sin que nadie mirara el resultado**: el comercio se ve verde en el panel
y **la alerta no sale**. Es el modo de falla exacto contra el que se vende el
abono ("el servicio avisa").

## Por qué esta tarea y no otra

1. **Es PLATA, la punta de la jerarquía.** Toca `firmware_modular`, que es la
   familia que se flashea para los abonos (P1–P5, la que se auto-actualizó a
   3.0.1 por OTA la semana pasada). No es investigación: es el core del servicio.
2. **Ya estaba diagnosticado y nadie lo había arreglado.** Es el **H4** de la
   auditoría del `2026-08-07` (`diario/nocturno-local-2026-08-07.md`, "**Fix: un
   carácter**"). Revisé los 25 branches nocturnos de frioseguro: **ninguno toca
   `wifi_utils.h`**. El hallazgo llevaba 20 días escrito y sin tocar.
3. **Es drift entre dos firmwares.** `firmware_revival` 2.6.0 —el de Santa Cruz—
   **ya tiene la versión correcta** (204 + cuerpo vacío + dos testigos). El que
   va a los abonos, no. Una misma empresa con dos firmwares que deciden distinto
   la misma pregunta es una bomba de tiempo: portar el arreglo cierra el drift.
4. **Pega en lo que está pasando esta semana.** `SESION_1_FRIOSEGURO_SANTACRUZ.md`
   (sin commitear) pide explícitamente verificar que el testigo "esté
   distinguiendo *asociado* de *con internet de verdad*". Para los comercios de
   Bahía el caso no es el portal sino **el router prendido con el ISP caído**, y
   se ve exactamente igual desde el firmware.

## Qué hice

### 1. `firmware_modular/net_witness.h` (nuevo, 128 líneas)

La política, en un solo lugar, portada de `firmware_revival` 2.6.0:

- **Solo `204` con cuerpo vacío.** `c == 204 && h.getSize() <= 0`. El `200` nunca
  es internet. (`getSize()` es el `Content-Length`; `-1` cuando no vino.)
- **Redirects deshabilitados.** Siguiendo el `302` se llega al login, que
  contesta `200`, y el bug vuelve por la ventana.
- **Dos testigos independientes** (Google y Cloudflare); alcanza con que **uno**
  conteste limpio. Con uno solo, un bloqueo de ese dominio daría "sin internet"
  en una red que anda, y el equipo se pasaría la vida saltando de red en red.
- **El resultado deja de ser un bool.** Cuatro diagnósticos:

| `internet_diag` | Qué pasó | Qué se hace |
|---|---|---|
| `ok` | 204 limpio | nada |
| `portal` | algo contestó HTTP y no es internet (viene con el código) | aceptar el portal o cambiar de red |
| `sin_red` | asociado y **nadie contesta** | router prendido sin uplink → llamar al ISP |
| `wifi_off` | ni asociado | reponer WiFi / revisar clave |

Esto es lo que **no** estaba en el `firmware_revival` y me parece la mitad que
importa: *"Offline"* a secas no distingue el router apagado del portal cautivo,
y **son dos llamadas de soporte distintas**. Si el equipo está a 1500 km, la
diferencia entre las dos es una noche de laburo.

### 2. `wifi_utils.h` — el cableado (3 cambios)

- `checkInternet()` delega en `netWitnessProbe()` y **no vuelve a decidir**.
- `connectWiFi()` **ya no asume** `internetAvailable = true` al asociarse. Antes
  había una ventana de hasta 30 s en la que el equipo recién conectado posteaba
  a Supabase y Telegram creyendo que iba a la nube. Ahora queda `false` y se
  vence `lastInternetCheck` para que la prueba corra en el próximo `loop()`
  (milisegundos). *Ojo con el detalle:* `lastInternetCheck = 0` **no** sirve —
  con `millis()` chico, `millis() - 0 < 30000` es verdadero y la prueba no
  corría en los primeros 30 s de vida. Va `millis() - INTERVAL_INTERNET_CHECK_MS`,
  que con aritmética unsigned envuelve bien.
- La cadencia sale de `INTERVAL_INTERNET_CHECK_MS` y no del `30000` pelado que
  tenía al lado. La constante de `config.h` era **decoración**: nadie la usaba.

### 3. Que se vea desde afuera

- `GET /api/status` → `system.internet_diag` + `system.internet_http_code`.
- Panel embebido: la fila **Internet** muestra el diagnóstico, en verde (`ok`),
  ámbar (`portal`, con el HTTP entre corchetes) o rojo. Cae con elegancia al
  bool viejo si el firmware es anterior.

### 4. Cuatro maneras de verificarlo sin tocar hardware

| Herramienta | Qué prueba | Resultado |
|---|---|---|
| `tools/test_net_witness_model.py` | la política, en Python (oráculo espejo 1:1) | **17 tests OK** |
| `tools/test_net_witness.cpp` | **el C++ real**, compilado con stubs de `HTTPClient` | **15 checks OK** |
| `tools/check_net_witness_wiring.py` | que el firmware la **use** (no que exista) | **16/16 OK** |
| `tools/test_check_net_witness_wiring.py` | que el chequeo anterior sirva: **11 mutantes** que reabren cada agujero de a uno | **15 tests OK** |

El de mutantes es el que más me importa: un checador que siempre dice OK es peor
que no tenerlo. Cada mutante copia el firmware a un tempdir, reintroduce **un**
agujero (volver a aceptar el 200, dejar de mirar el cuerpo, seguir redirects,
un solo testigo, `checkInternet()` decidiendo solo, `connectWiFi()` asumiendo
internet, el include al revés, el panel sin diagnóstico…) y exige que el check
correspondiente se ponga en rojo.

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-27-el-testigo-que-certificaba

# 1) la política, en Python
python -m unittest tools.test_net_witness_model -v          # 17 OK

# 2) la política, en el C++ real
g++ -std=c++11 -Wall -Wextra -o tools/test_net_witness.exe tools/test_net_witness.cpp
.\tools\test_net_witness.exe                                # 15 OK, exit 0

# 3) que el firmware la use
python tools/check_net_witness_wiring.py                    # 16/16, exit 0

# 4) que (3) sirva de algo
python -m unittest tools.test_check_net_witness_wiring -v   # 15 OK

# 5) que compile de verdad (~3 min, todo instalado en esta máquina)
C:\Tools\arduino-cli\arduino-cli compile --fqbn esp32:esp32:esp32 firmware_modular
```

**Compilación real, hecha esta noche:** OK.
`1289764 bytes (98%)` de programa, `53784 bytes (16%)` de RAM.
Contra `main` compilado en un worktree limpio: `1288696 bytes`.
**Delta: +1068 bytes de flash, RAM idéntica.**

## Lo que quedó sin verificar (necesita campo, no hardware de banco)

- **Que un portal cautivo real dispare `portal`.** Hace falta pararse en una red
  abierta con login —o desenchufar el WAN del router y mirar la página del ISP—
  y pedir `GET /api/status`. Los stubs prueban la **decisión**, no el transporte.
- **`getSize()` con respuesta `chunked`.** Sin `Content-Length` devuelve `-1`, así
  que un 204 chunked (raro pero posible) pasaría como bueno. Es la dirección
  segura del error, pero está sin confirmar en el ESP32 real.
- **Que Cloudflare no esté bloqueado** en la red del comercio.

## ⚠️ Hallazgo aparte que NO toqué (y que Matías tiene que ver)

**El sketch está al 98 % de la partición de programa, y ya lo estaba en `main`.**
`1288696 / 1310720 bytes` → quedan **~21 kB**. No lo causé yo (mi cambio son
1068 bytes). **Ya estaba anotado** en `dominios/firmware.md` (entrada 2026-07-13,
"98% flash — SIN margen, próxima feature no entra") y sigue sin resolverse; lo
repito acá porque ahora hay 1 kB menos y porque significa que:

- **la próxima feature no entra**, y el error de compilación va a aparecerle a
  quien esté haciendo otra cosa;
- **el OTA cloud está en riesgo**: el esquema por defecto reserva dos particiones
  de app del mismo tamaño, y un firmware que no entra no se puede actualizar por
  aire — con las placas ya encajonadas, eso es una visita al comercio.

**Recomendación:** antes de agregar nada más, pasar a un esquema de particiones
`min_spiffs` (~1,9 MB de app) o `huge_app`. Es un cambio de `--build-property` en
el flasheo, no de código. Lo dejo escrito porque es una decisión de Matías (afecta
al espacio de datos), no del worker nocturno.

## Observación de drift menor (no arreglado, ya conocida)

`firmware_modular/serial_api.h` **no está incluido** en `firmware_modular.ino`:
no se compila. Lo mismo `power_monitor.h` y `current_sensor.h`. @firmware ya los
tenía anotados como "headers huérfanos" el 2026-07-13. Lo agrego acá porque
ahora tiene una consecuencia concreta: el `serial_api.h` imprime
`Internet: OK / Sin conexión`, que es **literalmente** el diagnóstico que la
auditoría del 08-07 mandaba a mirar por serial para confirmar H4 — y ese comando
**no existe en esta familia de firmware**. Por eso no fui por ahí a exponer el
diagnóstico, y sí por `/api/status` y el panel. Decidir si se conectan o se
borran sigue siendo de @firmware, no de una noche.

## Estado del repo

- `QUE_FALTA.md` de frioseguro: ítem **19** nuevo, marcado `EN BRANCH … pendiente de merge`.
- Committeados **solo mis 13 archivos**. El working tree de frioseguro tiene
  cambios previos sin commitear que **no toqué** (apps Android, `firmware_revival/`,
  `kit_santacruz/`, `entrega_scz/`, `panel-web/`, los dos ZIP del kit). Siguen ahí
  intactos — pero son de Matías y llevan días sueltos: convendría decidir qué se
  commitea de eso.
- Worktree temporal del baseline: creado y **removido** (`git worktree prune` corrido).
- `tools/test_net_witness.exe` queda sin trackear a propósito (igual que
  `test_offline_buffer.exe`): se regenera con el `g++` de arriba.

## Próximo paso sugerido

1. **@verificador** audita el branch (es lo que la doctrina pide antes de merge).
2. Mergear. No colisiona con los otros branches abiertos de frioseguro.
3. **En el próximo flasheo** (que ya está pendiente por la rotación de claves del
   `07-10-b` y el `OTA_PASSWORD` del `07-12`): entra este arreglo, y de paso se
   resuelve la partición del 98 %.
4. **Con el equipo andando:** desenchufar el WAN del router y mirar
   `/api/status` — tiene que aparecer `sin_red`, o `portal` si el ISP sirve una
   página de cortesía. Es una prueba de 2 minutos y cierra el hallazgo.
