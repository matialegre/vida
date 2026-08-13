# Nocturno local — 2026-08-12

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (P1 — **LA PALANCA DE PLATA**, meta
3 abonos antes del **18-ago**: quedan 6 días).
**Branch:** `nocturno/local-2026-08-12-cadena-instalacion` (pusheado, `a289d7b`).

## TL;DR

El `QUE_FALTA` define vendible como *"un kit instalable en un comercio en <2
horas"*. El repo tiene un solo runbook de instalación, y **describe otro
despliegue**: los 5 reefers de Santa Cruz. Para el producto que se vende antes
del 18-ago —un equipo, un comercio de Bahía— **no hay procedimiento escrito.**

De los 8 pasos del runbook que sí existe, **6 están bloqueados, 1 tiene fricción
y 1 es ejecutable**, y el primer freno está en el PASO 1. El más filoso: **las 6
queries de verificación no pueden devolver una fila nunca**, y el troubleshooting
lee eso como "el equipo no conectó, volvé al PASO 3" — **manda a repetir para
siempre un paso que ya salió bien**.

## Tarea elegida y por qué

Por rotación tocaba datalogger o frioseguro (los dos turnos previos fueron
galgas y cosechador). La jerarquía manda **PLATA**, y el 18-ago está a 6 días:
frioseguro.

Repasando qué está cubierto en el repo:

| noche | qué audita | dónde empieza |
|---|---|---|
| 07-18 `alert_model` | la decisión de alertar | equipo instalado |
| 08-02 `telegram_gate_model` | la entrega del aviso | equipo instalado |
| 08-03-b `check_schema_drift` | la forma de los datos | equipo instalado |
| 08-09 `check_tenant_isolation` | el aislamiento entre clientes | equipo instalado |
| 08-10-b `check_temperature_chain` | de qué sonda sale el número | equipo instalado |

**Los cinco empiezan cuando el equipo ya está andando en el local.** El tramo de
antes —sacar el kit de la caja y dejarlo reportando— nunca se auditó. Y es
justo el que separa "tengo 5 PCBs fabricadas" de "tengo 3 abonos".

Además es un tramo que **se puede auditar sin hardware**: "instalable en <2
horas" es una afirmación sobre un procedimiento, y el procedimiento está escrito.
La pregunta que elegí:

> el kit sale de la caja y hay que dejarlo reportando en el comercio del
> cliente. **El procedimiento escrito, ¿se puede ejecutar?**

## Qué hice

**`tools/check_install_chain.py`** (stdlib, solo lectura, sin red ni hardware,
no compila nada). Cruza `GUIA_INSTALACION.md` contra `firmware_modular/config.h`,
`supabase.h`, el SQL, `vite.config.js` y los otros documentos de instalación del
repo. Exit 0/1/2/3, `--json`, `--detail`, `--fail-on`, `--root`.

**Dos oráculos** que demuestran los hallazgos en vez de afirmarlos:

- `--demo-coldstart` recorre los **8 pasos** como quien lee el runbook por
  primera vez, y marca cada uno *ejecutable / fricción / BLOQUEADO* con el
  hallazgo que lo frena. Resultado: **1 / 1 / 6**, primer freno en el PASO 1.
- `--demo-identity` cruza los momentos de la instalación contra qué señal hay
  disponible en cada uno para saber **qué caja es cada fila del dashboard**.
  La única que distingue de verdad aparece *después* de montar la caja, y por USB.

**`tools/test_check_install_chain.py` — 90 tests en 7 capas:** utilidades de
texto, semántica del `LIKE` de SQL, extractores sobre runbooks sintéticos, los
dos oráculos con números fijados, un test por código de hallazgo sobre un **repo
sano al que se le inyecta un solo defecto** (control negativo + delta),
regresión sobre el repo real y el CLI.

**`docs/install-chain.md`** — el análisis completo y el orden de arreglo.

### Lo que hubo que resolver

- **El `_` de SQL `LIKE` es un comodín de un carácter, no un guión bajo.** En
  este repo tratarlo como literal da la respuesta correcta *por casualidad*
  (una MAC no empieza con `REEFER` de ninguna manera). Está implementado bien y
  con test, porque el día que alguien cambie el patrón la casualidad se termina.
- **La rama muerta, tercera vez.** `config.h` tiene cinco bloques
  `#if PLACA_NUM == n`. Leyendo el archivo plano, el nombre por defecto del
  dispositivo sale `"Placa 1 — FrioSeguro"` — la rama que **no** compila (hoy
  está committeado `PLACA_NUM=2`). Como ya pasó con `#ifdef DEV_SIMULATE_ADC`
  en galgas y con el `#if 1 / #else` del gateway, lo resolví en una utilidad
  (`resolve_placa_branches`) y no caso por caso.
- **El origen del `device_id` no se ve en una línea.** Pasa por una variable
  local, un lazo de reintento de MAC y un fallback por chip ID antes de llegar a
  `g_device_id`. Un detector que mire la línea del `#define` concluye que sale de
  config, y con eso **I3 desaparece entero**. Hay test con 40 líneas de ruido en
  el medio.
- **Mi primer filtro de la tabla de APs descartaba los SSID con espacios.**
  Andaba bien contra el runbook (`FrioSeguro-ESP01`) y hacía que el checker **no
  pudiera dar OK nunca**, porque el SSID real *tiene* espacios
  (`FRIOSEGURO BAHIA BLANCA`). Lo cambié por una regla honesta: cuentan las
  celdas que el markdown escribe entre backticks. Lo agarró el control negativo,
  no yo.
- **Separar "molesta" de "frena".** La primera versión del oráculo marcaba el
  PASO 5 como BLOQUEADO por el puerto del dashboard, que es un `info`. Inflar el
  conteo justo donde el oráculo tiene que ser creíble es la peor economía
  posible. Ahora hay tres estados y el `info` es "fricción".

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **6 error · 4 warn · 2 info.**

| código | sev | qué |
|---|---|---|
| **I12** | error | **el único runbook del repo instala OTRO despliegue.** `GUIA_INSTALACION.md` es el kit de 5 reefers de Santa Cruz (`REEFER_xx_SCZ`, `firmware_ESPxx`, SIM800/Personal). Para el producto que se vende antes del 18-ago —un equipo, un comercio de Bahía, el WiFi del cliente, su Telegram— **no hay procedimiento escrito**. Los otros 11 hallazgos no son erratas: son la distancia entre el documento que hay y el que hace falta. |
| **I1** | error | el **primer comando** hace `cd "X:\Supervisor Bahia Blanca\…\firmware_ESP01"` (y 02..05): ninguna existe, y son rutas absolutas de otra máquina. El firmware que se flashea vive en `firmware_modular/` y se compila distinto. **Nadie que siga el runbook llega al PASO 2.** |
| **I2** | error | el PASO 4 verifica contra el proyecto Supabase **abandonado** (`nwugnhsktcihusopfldu`, link al SQL Editor + `.env` del dashboard). El firmware apunta a `cjdluhemschrynijzvap`, y el propio `config.h` deja escrito que el viejo quedó abandonado. Se consulta una base donde el equipo no reporta y se concluye que el equipo está roto. |
| **I3** | error | **las 6 queries de verificación devuelven 0 filas SIEMPRE.** Todas filtran por `device_id LIKE 'REEFER_%_SCZ'`; el firmware usa **la MAC** como `device_id`. Lo grave no es la query vacía: la tabla de troubleshooting lee "menos de 5 filas" como *"ese ESP32 no conectó WiFi → volver al PASO 3"*. **El procedimiento manda a repetir para siempre un paso que ya salió bien**, y el que se come el lazo es una persona parada en el local del cliente. |
| **I4** | error | el AP del portal cautivo no se llama como dice el runbook: real `FRIOSEGURO BAHIA BLANCA` y **abierto**; runbook `FrioSeguro-ESPxx` + `frioseguro1234`; `config_SANTA_CRUZ.h` `Reefer-Setup`/`reefer1234`. **Ninguna de las tres coincide.** Es el paso que se hace parado adentro de la cámara con el celular en la mano. |
| **I5** | error | los **pasos 6 y 7** transcriben salida `[DISCOVERY]` que el firmware **nunca imprime** y esperan que las sondas aparezcan solas en `sensor_probes`, tabla que el firmware **no escribe nunca** (cero URLs `/rest/v1/sensor_probes`). Dos pasos de ocho, y los dos que le dan **nombre y umbral a cada sonda**. Confirma **T2** del 08-10-b desde el lado del procedimiento. |
| **I6** | warn | **nada distingue una placa de otra al instalarla.** Las 5 publican el **mismo SSID**, se registran con el **mismo nombre** (`DEVICE_NAME=""` ⇒ todas `Placa 2 — FrioSeguro`), y su única identidad —la MAC— **sólo se lee por Serial, o sea por USB**, cuando la caja ya está cerrada y montada. El checklist pide "MACs anotadas en DISPOSITIVOS.md" y **ningún paso las obtiene**. |
| **I7** | warn | el runbook usa **dos veces como criterio de éxito** que "las temperaturas se actualizan cada 5 segundos". `INTERVAL_SUPABASE_SYNC_MS = 10000`. Un criterio de éxito es lo que no puede dar falsos negativos: el instalador que cronometra declara falla en un sistema sano. |
| **I8** | warn | el runbook lleva credenciales adentro (clave publicable + mail de la cuenta admin) y es un documento pensado para dárselo a quien instala. La clave es publicable, no `service_role` — el problema es que apunta al proyecto viejo (I2) y viaja junto al mail de admin. |
| **I9** | warn | hay **dos documentos más** de instalación/uso (`docs/INSTALACION.md`, `MANUAL.md`) y son de **otro sistema** (Parametican Silver, ESP8266 emisor/receptor, `reefer.local` por mDNS, una APK). Quien busque "cómo se instala" encuentra tres documentos que se contradicen y ninguno del producto de Bahía. |
| **I10** | info | el runbook manda a `localhost:5174`; `vite.config.js` no define `server.port` ⇒ `npm run dev` levanta en **5173**. Trivial, pero es la fricción que hace perder confianza en el resto del documento. |
| **I11** | info | **2 ítems del checklist final no pueden pasar nunca** (`last_temp_c` no NULL, umbrales por sonda): dependen de I5. Un checklist con ítems imposibles se firma igual — y ahí entrena a tildar sin mirar. |

**Orden sugerido** (por costo de no arreglarlo antes del 18-ago):

1. **Escribir el runbook del comercio** (I12) — sale gratis del **piloto casero**
   que ya está en el `QUE_FALTA` (ítem #2): instalar uno y anotar lo que se hace.
2. **I4 + I6 juntos** — el sufijo de MAC en el SSID (`…BAHIA BLANCA 3DE4`)
   arregla el paso más incómodo y la identificación de la placa de un saque. Es
   una línea de firmware, y se aprovecha el **reflasheo que ya está pendiente**
   por la rotación de claves (#4) y por T2/T5.
3. **I2 + I3** — el runbook nuevo verifica contra el proyecto correcto y filtra
   por lo que el equipo realmente manda.
4. **I5** — firmware de verdad, con dueño y ya priorizado por T2. Mientras no
   exista, **sacar los pasos 6 y 7** del runbook: un paso que no se puede hacer
   es peor que ausente.
5. **I9** — archivar los dos documentos del despliegue minero bajo un prefijo
   que lo diga. Cinco minutos.
6. **I7, I8, I10** — se corrigen solos al escribir el documento nuevo.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-12-cadena-instalacion

python tools/check_install_chain.py                  # informe; exit 3
python tools/check_install_chain.py --detail         # analisis + evidencia
python tools/check_install_chain.py --demo-coldstart # los 8 pasos, uno por uno
python tools/check_install_chain.py --demo-identity  # que caja es cada card
python tools/check_install_chain.py --json

python -m unittest tools.test_check_install_chain    # -> Ran 90 tests, OK
```

Tres de los hallazgos se comprueban **sin la herramienta**, mirando tres lugares:

- `grep -n "firmware_ESP" GUIA_INSTALACION.md` contra `ls firmware_modular/` (I1)
- `grep -n "supabase.co" GUIA_INSTALACION.md firmware_modular/config.h` (I2)
- `grep -rn "sensor_probes" firmware_modular/` → **un solo hit, y es un
  comentario** (I5)

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **90 tests en verde** (1,1 s). Sin descargas ni toolchains: cero riesgo de timeout.
- **Control negativo real:** un repo sintético sano no enciende **nada**, y cada
  defecto inyectado por separado enciende **uno y sólo un** código. Ocho de los
  hallazgos tienen además su test "no salta cuando no corresponde" (p. ej. I3 no
  salta si el `device_id` viene de config: el hallazgo es del **cruce**, no del
  patrón solo).
- **Verificado por mutación** — las **7** hacen fallar la suite: el `_` de LIKE
  como literal, no resolver `PLACA_NUM`, achicar la ventana de búsqueda del
  `device_id`, `writes_table` por nombre pelado en vez de la URL REST, descartar
  los SSID con espacios, fundir "fricción" con "bloqueado" en el oráculo, y
  `min` en vez de `max` en el exit code.
  *(El andamio de mutación fue descartable: no se commiteó. Borré el
  `__pycache__` antes de cada corrida — la trampa del 08-11-b.)*
- **No se tocó una sola línea de firmware, de `web-dashboard/` ni de SQL.** El
  branch agrega 3 archivos y edita `QUE_FALTA.md`. No hay build de dashboard que
  correr.

## Qué quedó sin verificar

- **Todo sale de leer el repo, no de mirar una instalación.** El oráculo
  demuestra el efecto de lo que dice el código; no que el hardware lo haga.
- **No mide las <2 horas.** Eso se cronometra el día del piloto.
- **No juzga el contenido técnico del procedimiento** (dónde va la sonda, cómo
  se fija la caja): juzga si los pasos escritos se corresponden con el sistema
  que existe.
- **I6 asume que WiFiManager no muestra la MAC en el portal por defecto.** Es
  cierto para la config actual (`autoConnect(AP_NAME)` pelado), pero se confirma
  en 30 segundos abriendo `192.168.4.1` con una placa prendida.
- **Ningún fix aplicado** — y el primero de la lista (escribir el runbook)
  sale de una instalación real, no de una noche de análisis.

## Estado

- Branch `nocturno/local-2026-08-12-cadena-instalacion` pusheado (`a289d7b`),
  sale de `main`. frioseguro volvió a `main` limpio.
- `QUE_FALTA.md` de frioseguro: ítem **#22** nuevo, dentro del branch.
  ⚠️ **Numeración:** empecé en 22 a propósito porque el branch
  `nocturno/local-2026-08-10-b-cadena-temperatura` agrega #19–#21. Si se mergean
  en cualquier orden no hay conflicto de números; sí va a haber un conflicto
  trivial de contexto en `QUE_FALTA.md` (los dos tocan la misma zona).
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Undécima noche que lo reporto:** es firmware que va a un equipo a 2000 km y
  vive **sólo en este disco**. **No lo toqué.** Detalle incómodo de hoy: parte de
  lo que I12 pide —el contexto de Santa Cruz— probablemente esté ahí adentro.
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día sin commitear**
  (`firmwares/nodo-gimap/`, `tools/rx_gimap.py`, los dos tests, el
  `docs/ARMADO_NODO_GIMAP.html`, `.gitignore` modificado). **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  dieciséis noches anteriores, más `agentes/diseno3d.md`, `dominios/diseno3d.md`,
  `dominios/LOGO_RED_GUIA.html` y `propuestas/MAIL_SAE_PPS.md`). **No los toqué.**
  Matías: commitealos, o la rutina cloud choca en el próximo `git pull`.
- ℹ️ `C:\Proyectos\cosechador` quedó checkouteado en el branch del 08-11-b.
  **No lo cambié.**
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío (sólo el `.gitkeep`). El único
  `enlace\maquinas\*.estado.json` (DESKTOP-RK8DH7C) sigue con `ultima_vez_viva`
  del **2026-07-07**. **No lo toqué.**
- La cola de merge suma **54 branches** en origin (galgas 19, datalogger 16,
  frioseguro **17**, cosechador 2).

## Para @firmware / @comercial / @cronista / @verificador

- **@firmware:** **I4+I6 son tuyos y son el mismo commit.** Sufijo de MAC en
  `AP_NAME` + la MAC impresa en el portal cautivo resuelve la identificación en
  los tres momentos de la instalación. Entra en el reflasheo que ya está
  pendiente por la rotación de claves. **I5** ya lo tenías por T2.
- **@comercial / MATÍAS:** el ítem #22 es el que **más cerca está de la plata** y
  el único de la lista que **no se puede escribir de noche**: sale de instalar
  uno y anotar. Media hora del piloto casero produce el documento entero.
- **@cronista:** **I9** es drift puro de docs (`docs/INSTALACION.md` y
  `MANUAL.md` son del despliegue minero viejo). Renombrarlos con prefijo es
  trabajo tuyo y son cinco minutos.
- **@verificador:** el DoD es *"cada paso del runbook tiene un hecho del repo que
  lo confirma o lo desmiente"*. Los 90 tests son el oráculo, y `TestRepoReal`
  fija los 12 hallazgos. **Puntos a atacar, en orden:** (1) **I12 es un juicio de
  alcance, no un hecho** — se apoya en que el producto de Bahía y el kit de Santa
  Cruz son despliegues distintos; si Matías considera que el runbook de Santa
  Cruz *es* la base a adaptar, I12 baja de severidad pero **I1–I5 quedan igual de
  vivos**. (2) **I6 asume el portal de WiFiManager por defecto** — verificable en
  30 s con una placa prendida. (3) **I8 es el más discutible**: la clave es
  publicable por diseño, así que el hallazgo es de higiene, no de seguridad;
  está declarado como `warn` por eso.
