# Nocturno local — 2026-08-16-b (2do turno)

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**P1 — LA PALANCA DE PLATA**).
**Branch:** `nocturno/local-2026-08-16-b-cadena-tiempo` (pusheado, `ec92bdf`).

## TL;DR

FrioSeguro se cobra con una promesa de una línea: **"el servicio avisa"**. Todo
aviso lleva una fecha. Nadie había preguntado nunca de qué reloj sale.

**FrioSeguro no tiene ni un solo timestamp de origen.**

- **El firmware que se vende no tiene reloj.** Cero `configTime()`, cero NTP en
  todo `firmware_modular/`. El equipo que se instala en el comercio **no sabe qué
  hora es**: sólo puede medir intervalos con `millis()`, que cuenta desde el
  último boot.
- **Los 7 campos que parecen fechados por el equipo los fecha el servidor.** El
  firmware manda la **cadena** `"now()"` a `last_seen_at`, `applied_at`,
  `downloaded_at`, `executed_at` y `updated_at`. Lo resuelve el reloj de
  Postgres. Dicen **cuándo llegó el POST**, no cuándo pasó la cosa.
- Mientras hay internet los dos relojes coinciden y no se nota. **Se separan
  justo cuando hay corte** — que es el único escenario contra el que se vende
  el abono.

Y hay un hallazgo que explica por qué esto sobrevivió siete auditorías:
**`ESTADO_ACTUAL.md:28` afirma que `last_seen_at` lleva "timestamp NTP real"**, y
nombra `supabaseUpdateDeviceStatus()`, **que no existe** en el firmware que se
compila. Las dos mitades de la frase son falsas. Mientras el doc diga eso, nadie
va a ir a buscar el problema.

**Corolario para el plan:** `QUE_FALTA` #9 —*"validar NTP, offset sin confirmar
en hardware"*— **no se puede hacer tal como está escrito.** No se valida en
hardware algo que no está en el código. El ítem apunta a otro firmware.

## Tarea elegida y por qué

Por rotación tocaba frioseguro (los cinco turnos previos: cosechador 08-14,
frioseguro 08-14-b, datalogger 08-15, galgas 08-15-b, cosechador 08-16 — el más
viejo era éste). La jerarquía manda **PLATA**, así que coincide.

Dentro del repo, los 🔴 que quedan son hardware, plata o nube; todo lo
software-puro sin branch ya estaba tomado. Los 🟡 sin branch eran #7 (SIM800,
hardware), #8 (OTA en hardware), #9 (NTP en hardware), #12 y #13.

**#9 era el único con una mitad de software real** — y resultó tener más adentro
de lo que decía el título.

Repasando qué estaba cubierto:

| noche | qué audita | dónde empieza |
|---|---|---|
| 07-18 `alert_model` | la **decisión** de alertar | equipo andando |
| 08-02 `telegram_gate_model` | la **entrega** del aviso | equipo andando |
| 08-03-b `check_schema_drift` | la **forma** de los datos | equipo andando |
| 08-09 `check_tenant_isolation` | el **aislamiento** entre clientes | equipo andando |
| 08-10-b `check_temperature_chain` | de qué **sonda** sale el número | equipo andando |
| 08-12 cadena de instalación | cómo **llega** el equipo al comercio | antes del equipo |
| 08-14-b cadena de continuidad | qué pasa cuando **se corta la luz** | equipo caído |

Las siete entran **después de que el número existe**. Ninguna pregunta lo único
que las atraviesa a todas:

> Cada fecha que el producto muestra o razona, **¿de qué reloj salió, y sigue
> siendo cierta?**

## Qué hice

**`tools/check_time_chain.py`** (stdlib, sólo lectura, sin nube ni hardware, no
compila nada). **No inventa números: los LEE** de `firmware_modular/`,
`supabase/*.sql`, `web-dashboard/src/` y los `.md`, y cita `archivo:línea` de
cada afirmación. Exit 0/1/2/3, `--json`, `--detail`, `--fail-on`, `--root`.

**Cuatro oráculos** que demuestran los hallazgos en vez de afirmarlos:

- `--demo-now` — qué hace Postgres con el literal que manda el firmware,
  contra la lista cerrada de valores especiales que documenta el manual.
- `--demo-relojes` — el inventario completo: cada dato, qué reloj lo estampa y
  si es cierto. Cuenta los relojes disponibles en el equipo: **cero**.
- `--demo-rollover` — `millis()`: las **restas** son correctas incluso cruzando
  el rollover (y eso está bien); los **absolutos publicados** mienten. A los 60
  días encendido, el equipo informa 10.
- `--demo-futuro` — espejo 1:1 de `fmtRelative()`: cualquier fecha futura, por
  poco o por mucho, se muestra **"ahora"**.

**`tools/test_check_time_chain.py` — 64 tests en 6 capas:** oráculos puros,
extractores sobre fuentes sintéticas, parsers del dashboard, **control negativo**
(un repo sintético sano no enciende **nada**) con un defecto inyectado por vez
que enciende **exactamente** su código, la capa «no salta cuando no corresponde»,
y regresión sobre el repo real + CLI.

**`docs/time-chain.md`** — el análisis, el orden de arreglo y las premisas
externas declaradas una por una.

### El error que cometí, y cómo se corrigió

Vale contarlo porque casi se va al informe como el titular de la noche.

Mi primera versión afirmaba que **Postgres RECHAZA el literal `"now()"`** y que
por lo tanto el POST de registro y el PATCH de heartbeat **fallaban enteros con
400** — o sea que `last_seen_at` no se escribía nunca. Un hallazgo grande.

**Era falso, y lo desmintió el propio repo.** El commit `8bdc579` dejó filas de
`ota_updates` en estado `'applied'`, y **ese mismo PATCH manda
`applied_at = "now()"`**. Si el literal se rechazara, la fila entera habría
vuelto 400 y el estado nunca habría llegado a `'applied'`.

La explicación: el tokenizador de fechas de Postgres, ante un carácter de
puntuación que no reconoce, **lo saltea y lo usa como delimitador** en vez de
abortar. `now()` queda como el único campo alfabético `now`, que sí es un valor
especial válido. **Funciona.**

Lo que quedó es más chico pero sobrevive y es la tesis de la noche: el reloj que
resuelve ese literal es **el del servidor**. Hay un test dedicado
(`test_now_con_parentesis_NO_es_rechazado`) para que la corrección no se pierda,
y el oráculo `--demo-now` la explica en pantalla.

*(La lección es la misma del 08-16: un hallazgo **exagerado** es tan inservible
como uno perdido. Acá el freno no fue un test propio — fue ir a buscar evidencia
en el historial antes de escribir.)*

### Lo otro que hubo que resolver

- **T3 salía con 18 funciones y sólo una venía al caso.** Mi extractor barría
  cualquier `` `funcion()` `` en líneas que mencionaran «NTP», y se tragaba el
  inventario entero de `firmware_v2` de `ESTADO_ACTUAL:278`. Acotado a las
  líneas que **afirman** algo sobre `last_seen_at`, queda **una**:
  `supabaseUpdateDeviceStatus()`. Mismo criterio que arriba.
- **El análisis leía un solo `.sql` y perdía media columna.** `applied_at` y
  `downloaded_at` viven en `migration_ota_updates.sql`, no en
  `SETUP_COMPLETO.sql`: el hallazgo salía con 5 sitios y su prosa nombraba
  columnas que **su propia evidencia no listaba**. Ahora une todos los `.sql`.
- **La herramienta se apagaba a sí misma.** T7 dice *«que la hora la pone el
  servidor no está escrito en ningún lado»*. Al escribir `docs/time-chain.md`
  —que lo explica— el hallazgo **desapareció solo**. Es un informe *sobre* el
  hueco, no la decisión registrada por su dueño: el propio informe queda
  excluido, con test.
- **Dos guardas que sobraban, y una hacía daño.** La mutación reveló que el
  filtro «si la línea tiene una resta de `millis()`, saltearla» **nunca evitaba
  un falso positivo** (el patrón ya distingue solo la resta del absoluto) y en
  cambio **causaba un falso negativo**: una línea con una resta *y* un absoluto
  publicado se descartaba entera. Se fue, con test que lo fija.

## Hallazgos — NO corregidos (generator ≠ evaluator)

Corrida real: **3 error · 3 warn · 1 info.**

| código | sev | dueño | qué |
|---|---|---|---|
| **T1** | error | @firmware + @backend | **Los 7 campos que parecen fechados por el equipo los fecha el SERVIDOR.** El firmware manda la cadena `"now()"` a `last_seen_at`, `applied_at`, `downloaded_at`, `executed_at`, `updated_at`. Dicen *cuándo llegó el POST*, no *cuándo pasó*. |
| **T2** | error | @firmware | **El firmware que se vende no tiene reloj.** Cero `configTime()`/NTP en `firmware_modular/`. Sí lo hay en `receptor/` y `firmware_revival/`: el código sabe hacerlo, no está donde se vende. **`QUE_FALTA` #9 pide validar en hardware algo que no está en el código.** |
| **T3** | error | @cronista + @firmware | **El doc de estado promete un reloj que el código no tiene.** `ESTADO_ACTUAL:28` dice *"timestamp NTP real"* y nombra `supabaseUpdateDeviceStatus()`, que **no existe**. Es el hallazgo que tapa a los otros dos. |
| **T4** | warn | @frontend | **La frescura se renderiza sólo en la rama que no ocurre.** `OnlineBadge` muestra `lastSeenAt` únicamente cuando `is_online` es false — y nadie escribe false (08-14-b). El operador ve `● Online` sin fecha, para siempre. |
| **T5** | warn | @frontend | **`fmtRelative` muestra cualquier fecha futura como "ahora".** Con `diff` negativo, `d`/`h`/`m` quedan ≤ 0 y cae al `return 'ahora'`. El error va siempre en la dirección peligrosa: falso *"está fresco"*. |
| **T6** | warn | @firmware | **`uptime_sec` y el historial se dan vuelta a los 49,7 días.** Las **restas** están bien (fijado por test); los **absolutos** publicados no. A los 60 días el panel informa 10: **el equipo más estable del parque es el que peor se ve**. |
| **T7** | info | @backend + @cronista | **Todo lo que se cobra depende del reloj del servidor, y no está escrito.** `readings`/`alerts` usan `DEFAULT NOW()`. Está **bien** —es lo que hace que funcione a pesar de T1/T2— pero es tácito. |

**Orden sugerido:**

1. **T3 primero, porque tapa a los otros dos.** Es una corrección de texto.
2. **T2 — decidir si el equipo necesita reloj.** No es obvio que sí: hoy el
   servidor alcanza. Pero es **prerrequisito del buffer que pidió el 08-14-b**:
   sin reloj no se pueden reinsertar las lecturas de un corte con su hora real.
   **Decidirlo antes de escribir el buffer, no después.**
3. **T5 y T4** — dos líneas de dashboard, y es lo único que el cliente ve.
4. **T6** — publicar el rollover (o un contador de boots) en vez de esconderlo.
5. **T1** — de fondo es T2. Aparte, `"now()"` → `"now"` en los 7 sitios los
   apoya en la ortografía documentada. Barato, sin cambio de comportamiento.
6. **T7** — una línea en `docs/ARQUITECTURA.md`. Lo más barato del informe.

## Lo que está BIEN (fijado por test, para no ir a revisarlo)

- **`readings` y `alerts` no mandan ningún timestamp.** La historia de
  temperatura —el dato que se cobra— la fecha Postgres. Es lo correcto, y hay un
  test que **falla si alguien le agrega un `created_at` al firmware**.
- **Todas las restas de `millis()` son rollover-safe.** Fijado por test para que
  nadie las "arregle".
- **La retención borra por antigüedad absoluta**, sin depender de husos.
- **`fmtRelative` maneja bien el null** (`'Sin datos'`). El agujero es sólo el
  signo negativo.

## Cómo verificarlo (comandos exactos)

```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-16-b-cadena-tiempo

python tools/check_time_chain.py                    # informe; exit 3
python tools/check_time_chain.py --detail           # + evidencia archivo:linea
python tools/check_time_chain.py --demo-now         # el literal contra Postgres
python tools/check_time_chain.py --demo-relojes     # inventario de relojes
python tools/check_time_chain.py --demo-rollover    # restas vs absolutos
python tools/check_time_chain.py --demo-futuro      # fmtRelative desfasado
python tools/check_time_chain.py --json

cd tools && python -m unittest test_check_time_chain   # -> Ran 64 tests, OK
```

Tres hallazgos se comprueban **sin la herramienta**, con `grep`:

```bash
# T2: cero hits -> el firmware que se vende no tiene reloj
grep -rn "configTime\|pool.ntp.org" firmware_modular/
grep -rln "configTime" receptor/ firmware_revival/      # ...pero ahi si hay

# T1: los sitios que mandan la cadena
grep -rn '"now()"' firmware_modular/

# T3: la afirmacion, y la funcion que no existe
grep -n "NTP real" ESTADO_ACTUAL.md
grep -rn "supabaseUpdateDeviceStatus" firmware_modular/   # cero hits
```

**Verificado en esta máquina:**

- `py_compile` de los dos archivos.
- **64 tests en verde** (3,4 s). Sin descargas ni toolchains: cero riesgo de
  timeout.
- **Control negativo real:** un repo sintético sano no enciende **nada**, y cada
  defecto inyectado por separado enciende **exactamente** el código esperado.
  Los siete tienen además su test «no salta cuando no corresponde».
- **Verificado por mutación — 14 mutaciones, las 14 hacen fallar la suite.** La
  primera ronda dejó **3 vivas**, y las 3 eran defectos reales: dos guardas
  redundantes (una causaba un falso negativo) y un test que no mordía. El
  andamio de mutación fue descartable, en `/tmp`: **no se commiteó**. Borré el
  `__pycache__` antes de cada corrida y restauré el archivo al final;
  `git status` quedó limpio.
- **No se tocó firmware, ni schema, ni el dashboard.** El branch agrega 3
  archivos y edita `QUE_FALTA.md`. **No hay build que correr**: no toqué el
  dashboard, así que no hay `npm run build` que aporte información.

## Qué quedó sin verificar

- **Todo sale de leer el repo, no de correr el sistema.** No hay equipo
  instalado ni acceso a la nube desde acá.
- **La premisa externa de T1 es una sola y se cierra en 10 segundos de día:**
  correr en el SQL editor de Supabase
  `SELECT 'now()'::timestamptz, 'now'::timestamptz, now();`.
  **No hay `psql` ni Docker en esta máquina**, así que no pude ejecutarlo. La
  evidencia empírica del repo (commit `8bdc579`) ya respalda que funciona; la
  consulta lo vuelve incontestable.
- **T6 supone `millis()` de 32 bits**, que es lo del core ESP32. Si alguna vez
  pasa a 64, T6 desaparece solo.
- **T4 se apoya en el hallazgo del 08-14-b** (nadie escribe `is_online=false`).
  Si eso se arregla, T4 **baja de severidad pero no desaparece**: el badge sigue
  escondiendo la frescura mientras el equipo está sano.
- **T5 y T4 son de UI: hay que verlos en pantalla.** Son para @tester con un
  device reportando, no para un análisis estático.
- **Ningún fix aplicado** — generator ≠ evaluator. Ni siquiera T3, que es una
  línea de texto: el que corrige el doc tiene que ser el que sabe qué firmware
  se va a flashear.

## Estado

- Branch `nocturno/local-2026-08-16-b-cadena-tiempo` pusheado (`ec92bdf`), sale
  de `main` (`ddf5134`). **frioseguro volvió a `main` limpio.**
- `QUE_FALTA.md` del repo actualizado **dentro del branch** (ítem #9).
  ⚠️ **Conflicto anunciado, chico:** varios branches previos agregan viñetas
  bajo ítems distintos del mismo `QUE_FALTA.md`. El mío entra bajo el **#9**,
  que **ningún otro branch toca** — debería mergear sin conflicto real.
- 4 repos intactos salvo el branch de trabajo.
- ⚠️ **`C:\Proyectos\frioseguro` sigue con el trabajo de día SIN COMMITEAR**
  (`REVIVAL_2026-08.md`, `kit_santacruz/`, `firmware_revival/`, el `.zip`).
  **Decimonovena noche que lo reporto**: es firmware que va a un equipo a 2000 km
  y vive **sólo en este disco**. **No lo toqué.**
  *(Dato nuevo de esta noche: `firmware_revival/` **sí tiene NTP** —
  `configTime(-3*3600, 0, "pool.ntp.org")`. O sea que la versión sin commitear
  resuelve parte de T2, y está fuera de git.)*
- ⚠️ **`C:\Proyectos\datalogger` sigue con trabajo de día SIN COMMITEAR**
  (6 archivos: `firmwares/nodo-gimap/`, `tools/rx_gimap.py`, los dos tests del
  nodo GIMAP, `docs/ARMADO_NODO_GIMAP.html`, `.gitignore`). **No lo toqué.**
- ⚠️ **MATI-HQ sigue con trabajo de día SIN COMMITEAR** (los mismos de las
  veinticuatro noches anteriores: `agentes/`, `dominios/`, `enlace/`, más
  `agentes/diseno3d.md`, `dominios/diseno3d.md`, `dominios/LOGO_RED_GUIA.html` y
  `propuestas/MAIL_SAE_PPS.md`). **No los toqué.** Matías: commitealos, o la
  rutina cloud choca en el próximo `git pull`.
- ⚠️ Sigue el branch local vacío `nocturno/local-2026-08-05-b-identidad-ota` en
  galgas (0 commits). `git branch -d` cuando quieras.
- ℹ️ **ENLACE:** `enlace\buzon\pendiente\` vacío. El único
  `enlace\maquinas\*.estado.json` (DESKTOP-RK8DH7C) sigue con `ultima_vez_viva`
  del **2026-08-07**: el latido está parado hace **9 días**. **No lo toqué** (los
  scripts de ENLACE son trabajo de día sin commitear).
- La cola de merge suma **62 branches** en origin (galgas **21**, frioseguro
  **19**, datalogger 18, cosechador 4).

## Para @firmware / @frontend / @backend / @cronista / @verificador

- **@firmware: T2 es tuyo y es una DECISIÓN, no un bug.** La pregunta no es
  "¿por qué falta el NTP?" sino **"¿el equipo necesita saber la hora?"**. Hoy no:
  el servidor alcanza y el producto funciona. **Pero es prerrequisito del buffer
  que pidió el 08-14-b** — sin reloj, las lecturas de un corte no se pueden
  reinsertar con su hora real. Decidilo **antes** de escribir el buffer. Y ojo:
  `firmware_revival/` (sin commitear) **ya tiene el NTP puesto**.
- **@cronista: T3 es tuyo y es el más urgente de los tres errores.**
  `ESTADO_ACTUAL.md:28` promete un reloj que no existe y nombra una función de
  otro árbol. Mientras eso esté escrito, **el problema es invisible**. Y de paso:
  ese archivo describe `firmware_v2/`, no `firmware_modular/` — vale revisar
  cuánto más del doc está hablando del árbol equivocado. **T7 también te toca**
  (una línea en `docs/ARQUITECTURA.md`).
- **@frontend: T4 y T5 son dos líneas y son lo único que el cliente ve.** T5 es
  `if (diff < 0)` en `fmtRelative`; T4 es mover `lastSeenAt` afuera del ternario.
  **T4 se cruza con el 08-14-b**: arreglar uno solo de los dos no cambia lo que
  el operador ve en pantalla — coordinalo con quien tome ese hallazgo.
- **@backend: T1 de fondo es T2.** Lo tuyo es barato: cambiar `"now()"` por
  `"now"` en los 7 sitios los apoya en la ortografía documentada en vez de en
  una tolerancia del tokenizador. **No cambia el comportamiento** — es
  robustez, no un fix.
- **@verificador:** el DoD es *«cada fecha que el producto muestra tiene un
  reloj identificado y declarado»*. Los 64 tests son el oráculo y `TestRepoReal`
  fija los 7 hallazgos. **Puntos a atacar, en orden:**
  1. **T1 es donde ya me equivoqué una vez.** Mi primera versión decía que
     Postgres rechaza `"now()"`; es falso. Si vas a atacar algo, atacá eso —
     pero notá que el hallazgo **ya se reescribió** y su forma actual («la hora
     la pone el servidor») no depende del veredicto del parser.
  2. **T2 y T3 son los más sólidos**: los dos son `grep` que dan cero.
  3. **T6 es el más fácil de discutir como "no importa"** — 49,7 días es mucho.
     Mi argumento es que un abono se cobra por continuidad y el uptime es
     justamente el número que la demuestra. Es opinable.
  4. **T4 y T5 no los verifiques leyendo: son de UI.** Pasáselos a @tester con
     un device reportando.
  5. **Revisá que T4 no se pise con el hallazgo de `is_online` del 08-14-b.**
     Están cerca a propósito y son distintos: aquel dice que el estado nunca se
     apaga; T4 dice que la UI esconde la frescura en la rama que sí ocurre. Si
     te parece que son el mismo, el que sobra es T4.
