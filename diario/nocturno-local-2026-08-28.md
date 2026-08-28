# Nocturno local — 2026-08-28

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\galgas` (**P0** — parada Dreyfus, octubre).
**Branch:** `nocturno/local-2026-08-28-la-calibracion-que-nadie-lee` (pusheado, `c048b93`).
**Sale de:** `main` (`e9cd4bc`). **No depende de ningún otro branch nocturno** y no
toca ninguno de los archivos de la cadena de entrega (`08-22-b` → `08-25` → `08-26-c`):
ésos viven en `supabase_client`, el gateway y el dashboard; éste, en el sampler y el
handler de comandos. Se mergea en cualquier orden.

## TL;DR

> **La calibración se escribía en NVS y no la leía nadie.**

```c
// firmware/esp_a_emisor/adc_sampler.cpp (main, hoy)
const float k        = DEFAULT_K;                            // 1.00f, de config.h
const float off      = DEFAULT_OFFSET * (float)OFFSET_SIGN;  // 0.00f, de config.h
```

Del otro lado de la cadena estaba **todo** construido: el comando en la cola, la
validación de rangos, `nvsSaveCalibration()`, y hasta `nvsLoadCalK()` /
`nvsLoadCalOffsetV()` — que existían desde el primer día y **no las llamaba nadie**.

Mandabas `set_calibration` desde la nube, el equipo contestaba **`ack=OK`**, la fila
quedaba `executed` en `commands`, y la próxima medición salía **idéntica**.

`force_calibration` estaba peor: seteaba `sx->calibration_pending = true` en una
struct de RAM que no consumía nadie y que el deep sleep de las líneas siguientes
borraba. Las **tres** etapas contestaban `ack=OK` sin medir nada.

## Por qué esta tarea y no otra

1. **Es el canal que octubre necesita.** El plan de la parada es calibrar cada
   emisor **contra la galga física en sitio** (QUE_FALTA #2, bloqueante). El único
   mecanismo remoto para hacerlo era éste. Sin él, calibrar = recompilar y
   reflashear por cable, **con la caja ya montada en el REDLER**.
2. **Es la familia de octubre.** `esp_a_emisor` / `esp_b_emisor`, la modular. El
   monolítico `ota_wm_pp` sí tiene la calibración completa desde 3.6.0 — o sea que
   esto es **drift entre familias**, el mismo patrón que se viene pagando en
   frioseguro toda la semana.
3. **Ningún branch nocturno lo tocaba.** Revisé los 30 branches de galgas: la
   cadena de medición (`08-09-b`), la caracterización de v_pp (`07-29`) y la cadena
   de entrega (`08-11` → `08-26-c`) pasan por al lado y ninguno entra al sampler.
4. **Es 100 % software y se verifica sin encender nada** — salvo la prueba final,
   que queda escrita.

## Qué hice

### 1. Un agravante que encontré por el camino: las dos familias no usaban la misma fórmula

```
modular (viejo):       v = v_raw * k + offset * OFFSET_SIGN   <- offset DESPUÉS de la ganancia
monolítico ota_wm_pp:  v = (v_raw - offset) * k               <- offset ANTES de la ganancia
```

No es cosmético. El par `(k, offset)` que produce el procedimiento remoto que **ya
existe** (`autoffset` para tarar, después `cal_with_load` con peso conocido) está
definido para la fórmula del monolítico. Con `v_raw = 1.70 V, k = 2.0, offset = 0.20 V`:
monolítico **3.00 V**, modular vieja **3.60 V**.

O sea: aun cableando la calibración tal como estaba, un par calculado con el
procedimiento existente habría dado una medición **mal escalada**. Por eso el
arreglo no es "llamar a `nvsLoadCalK()`" sino unificar la fórmula primero.

### 2. `firmware/shared/cal_model.h` (nuevo)

Una sola definición, en funciones puras (sin Arduino, sin NVS) para poder probarla
en la PC. Se adopta la del monolítico: es la que está en producción y la que el
procedimiento asume.

- `calIsValid()` — rangos **y finitud**.
- `calSanitize()` — un par inválido cae a la **identidad** (medir crudo) en vez de medir mal.
- `calTareOffset()`, `calSeedOffsetFromConfig()`, `calStageImplemented()`.

**Por qué se valida antes de aplicar, y no después:** una `k = NaN` propaga NaN a
`v_pp`, y `NaN > 0.040` es `false`. Un par corrupto en NVS no haría medir mal:
**apagaría el self-trigger de alerta, en silencio**. Es el modo de falla más caro
del sistema y hay un check explícito de eso en el test.

### 3. El cableado (lo que faltaba)

- **`adc_sampler.cpp`** aplica `calApply()` con el par que dejó
  `samplerSetCalibration()`, en **las dos ramas** — la real y la de
  `DEV_SIMULATE_ADC`. La simulada también **a propósito**: si no, en banco la
  cadena de calibración no se ejerce nunca y el problema aparece recién en planta.
- **El `.ino` carga NVS y se la pasa al sampler ANTES de `samplerStartBurst()`.**
  El orden es el punto: dársela después del burst se lee perfecto y no calibra
  nada. (Hay un mutante que hace exactamente eso y el checker lo caza.) Se lee
  **una vez por wake**: abrir `Preferences` cuesta ms y mAh en un nodo a batería.
- **Primer boot:** se siembra el par en NVS. Ése es el **único** lugar donde entra
  `OFFSET_SIGN`; desde ahí NVS es la única fuente de verdad del offset. Si el mismo
  número vive en dos lados se desincroniza, que es como empezó todo esto.
- **La tara (`force_calibration` stage 1)** se persiste en NVS y la ejecuta el
  **wake siguiente** (el comando llega después del burst; entre medio hay un deep
  sleep que borra la RAM). Las **etapas 2 y 3 ahora fallan con error**: no están
  implementadas en esta familia, y un error es mejor que un `ack=OK` que no midió.
- **El reading publica `cal_k` / `cal_offset_v`** en su `metadata` (y `cal_tared`
  en el wake de la tara). Sin eso, desde la nube no hay forma de distinguir un
  equipo calibrado de uno en identidad.
- **`set_calibration`** valida con los límites de `cal_model.h`, no con `0.1f`/`10.0f`
  sueltos — que es como se desincronizaron las dos familias la primera vez.

### 4. Compatibilidad (por qué es seguro mergear)

Con los defaults (`k = 1.0`, `offset = 0.0`) **la fórmula nueva es la identidad**:
un equipo que nunca se calibró mide exactamente lo mismo que antes. El cambio de
fórmula sólo se nota en un equipo efectivamente calibrado, y hoy no hay ninguno —
justamente porque el comando no hacía nada.

### 5. La verificación

| Herramienta | Qué prueba | Resultado |
|---|---|---|
| `tools/test_cal_model.cpp` | la fórmula, sobre **el header real** que se compila en el ESP32 | **35 checks OK** |
| `tools/check_calibration_wiring.py` | que el firmware la **use** (no que exista) | **62/62 OK** |
| `tools/test_check_calibration_wiring.py` | 16 mutantes + **el código real de `main`** | **18 tests OK** |
| `arduino-cli compile` A y B | que compile de verdad | **OK** |

El test que más vale es `test_codigo_de_main_es_rojo`: saca los archivos de `main`
con `git show` y **exige que el checker repruebe el bug histórico**. Un checker que
no caza el bug que motivó su existencia no sirve para nada.

> Un mutante encontró un defecto real del checker mientras lo escribía: comentar
> `// nvsClearCalPending();` dejaba el nombre en el archivo y la búsqueda por
> subcadena la daba por hecha. El checker ahora saca los comentarios antes de
> buscar llamadas. Ése es el trabajo que hacen los mutantes.

## Cómo verificarlo (comandos exactos)

```powershell
cd C:\Proyectos\galgas
git checkout nocturno/local-2026-08-28-la-calibracion-que-nadie-lee

# 1) la formula, sobre el header real
g++ -std=c++11 -Wall -Wextra -o tools/test_cal_model.exe tools/test_cal_model.cpp
.\tools\test_cal_model.exe                                   # 35 checks OK, exit 0

# 2) que el firmware la use
python tools/check_calibration_wiring.py                     # 62/62, exit 0

# 3) que (2) sirva de algo
python -m unittest tools.test_check_calibration_wiring -v    # 18 OK

# 4) que compile (~2 min por sketch, todo instalado en esta maquina)
C:\Tools\arduino-cli\arduino-cli compile --fqbn esp32:esp32:esp32 firmware\esp_a_emisor
C:\Tools\arduino-cli\arduino-cli compile --fqbn esp32:esp32:esp32 firmware\esp_b_emisor
```

**Compilación real, hecha esta noche (A y B, las dos):**
`1237624 bytes (94%)` de programa, `61464 bytes (18%)` de RAM.
Contra `main` compilado en un worktree limpio: `1235360 bytes` / `61456`.
**Delta: +2264 bytes de flash, +8 de RAM.** El worktree del baseline se creó y se
**removió** (`git worktree prune` corrido, `git worktree list` limpio).

## Lo que quedó sin verificar (necesita banco, no hay forma de cerrarlo de noche)

- **La tara punta a punta.** Nadie mandó todavía un `force_calibration` a un equipo
  prendido. Prueba mínima de banco, 15 minutos: bajar el período con `set_period`,
  mandar `{"stage": 1}` con la galga en reposo, y verificar en `readings` que el
  wake siguiente trae `"cal_tared": true` y que el posterior tiene `v_mean ≈ 0` con
  `cal_offset_v` distinto de 0 en el metadata.
- **El `k` real de cada emisor.** Sigue sin medirse: hace falta el peso conocido
  (QUE_FALTA #2). **Este branch da el canal, no el número.**
- **Cuánto tarda la tara en campo:** un período de sueño. En `MODE_NORMAL` son
  10 minutos entre el comando y la tara. Con la planta parada y el reloj corriendo,
  eso importa — por eso el procedimiento del doc arranca bajando el período.

## ⚠️ Cosas que vi y NO toqué (son decisiones tuyas)

1. **El sketch está al 94 % de la partición de programa** (`1237624 / 1310720`).
   No lo causé yo (+2264 bytes), pero es **el mismo problema que `firmware_modular`
   de FrioSeguro tiene al 98 %** (informe del `08-27`): un firmware que no entra en
   la partición **no se puede actualizar por OTA**, y con la caja montada en el
   REDLER eso es un viaje a planta. La solución es un esquema `min_spiffs` o
   `huge_app` (`--build-property`, no es cambio de código). Afecta el espacio de
   datos → es decisión tuya, no de una noche.
2. **`ota_wm_pp` (la familia monolítica) no se tocó.** Tiene la calibración bien y
   anda; unificar las dos familias es un trabajo con banco, no a ciegas de noche.
   Lo que sí quedó es que ahora **usan la misma fórmula**, que era la mitad
   peligrosa del drift.
3. **Los emisores ya flasheados** (A en 0.1.3) tienen NVS sin la semilla porque su
   `first_boot` ya pasó. No es problema: los defaults de `nvsLoadCal*()` son la
   identidad, o sea lo que están midiendo hoy. Queda anotado en el doc por si
   alguien cambia `DEFAULT_OFFSET` (hoy `0.00` en A y en B).

## Estado del repo

- `QUE_FALTA.md` de galgas: puntero nuevo bajo el **ítem #2**, marcado
  `EN BRANCH … pendiente de merge`.
- Commiteados **solo mis 17 archivos**. `hardware/` sigue **sin trackear** (trabajo
  de día tuyo) y **no lo toqué** — el `git add` fue archivo por archivo.
- `tools/test_cal_model.exe` queda sin trackear a propósito (igual que
  `test_forward_queue.exe` y `test_gateway_route.exe`): se regenera con el `g++`.
- La cola de merge de galgas son **30 branches**.

## Próximo paso sugerido

1. **@verificador** audita el branch (doctrina: antes de merge). Ojo con el punto
   que más me interesa que mire alguien: la fórmula nueva es la identidad con los
   defaults, así que **el riesgo de merge es cero hoy** — pero conviene confirmarlo
   contra `data/field_captures/` antes de calibrar el primer equipo de verdad.
2. **Mergear.** No colisiona con la cadena de entrega (`08-22-b` → `08-25` → `08-26-c`).
3. **En el banco, la prueba de 15 minutos de arriba.** Cierra el único hueco que
   este branch no puede cerrar solo.
4. **Sumar `python tools/check_calibration_wiring.py` al gate previo a cada
   flasheo**, junto a los checkers de las noches anteriores. Todos contestan la
   misma pregunta desde distinto ángulo: *¿esta placa, tal como está, sirve?*

**Documento largo con todo el detalle:** `docs/calibration-chain.md` (en el branch),
incluido el procedimiento de tara paso a paso para campo.
