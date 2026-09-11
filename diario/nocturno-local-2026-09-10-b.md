# Nocturno local — 2026-09-10-b

**Trabajador:** worker nocturno local (Matías durmiendo). **Segundo turno** de la
noche — el primero fue `nocturno-local-2026-09-10.md` (frioseguro, el panel que
se queda verde).
**Repo tocado:** `C:\Proyectos\galgas` (**P0 octubre**, con el frente comercial
abierto: hay cámaras compitiendo adentro de Dreyfus).
**Branch:** `nocturno/local-2026-09-10-b-el-bin-que-arranca-y-no-vuelve`
(pusheado, `cb47bad`).
**Sale de `origin/main` (`35a8200`) limpio**, sin ningún otro branch mergeado
adentro.
**No toca** SQL, ni el bucket de Storage, ni `data/field_captures/`, ni el nodo
v3 (ATmega), ni `hardware/`, ni el panel web, ni `supabase_client.cpp`. **No
colisiona con ningún branch abierto.**

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_galgas_0910b`, ya
eliminado). **Verificado al terminar: el árbol de `galgas` quedó idéntico**
(mismo hash de `git status`), en el branch
`nocturno/local-2026-09-05-la-potencia-que-nadie-cambio` donde estaba.

---

## TL;DR

> **El rescate post-OTA se desarmaba solo, y justo sobre la única falla que el
> OTA no puede arreglar.** Confirmaba el bin nuevo con "3 arranques sin crash".
> Un bin que arranca perfecto y **no llega nunca a Supabase** —credenciales mal,
> una regresión en `wifiBoot()`, un certificado vencido, `supabaseInit() FAIL`—
> junta esos tres arranques sin despeinarse: levanta, falla el WiFi, `goSleep()`,
> vuelve. A los 3 wakes (**30 minutos** en MONITOR) el módulo corría
> `otaRescueClear()` + `esp_ota_mark_app_valid_cancel_rollback()` y **desarmaba
> su propia red**. A partir de ahí no hay vuelta atrás remota: para mandarle el
> OTA que lo arregla hay que poder alcanzarlo. Es un ladrillo con el LED
> prendido. Y del otro lado, el agujero que estaba **declarado** y frenado desde
> el 09-01: un bin que se **cuelga** no resetea, no genera `reset_reason`, y el
> rollback entero cuelga del `reset_reason`.

## Por qué esta tarea

1. **Cierra el único ítem de `QUE_FALTA` que el propio repo declaraba a medias.**
   El header de `ota_rescue.h` y los README de A y B decían textual *"TODO Task
   09 (otra mitad): watchdog post-OTA"*. Ningún branch de los 30 abiertos lo
   tocaba.
2. **Las dos razones por las que se había frenado no eran de banco.** El 09-01
   lo dejó anotado: *"la API de `esp_task_wdt` cambió entre arduino-esp32 2.x y
   3.x y no hay banco esta noche para confirmar cuál compila"*. Eso no es una
   duda de hardware, es una duda de **toolchain**, y el toolchain está
   instalado: `arduino-cli core list` dice `esp32:esp32 3.3.8`. La segunda duda
   —qué timeout— sale de leer el wake más largo del propio firmware.
3. **El agujero A no lo había visto nadie**, y es peor que el que estaba
   declarado: el declarado deja al nodo colgado; éste lo deja **corriendo, sano
   en el dashboard, inalcanzable y sin red de rescate**.
4. **Se hace entera sin hardware** y el cableado se puede probar.
5. **Frioseguro ya tuvo el primer turno de la noche** (es PLATA, prioridad #1).
   El segundo le toca a octubre, y galgas es el que tiene competencia adentro
   del cliente.

## Los dos agujeros

### A · Contar arranques no es verificar nada

La confirmación miraba un solo número. Mirando el `setup()` del emisor se ve por
qué eso no alcanza:

```c
WifiBootResult wr = wifiBoot(DEVICE_ID);
if (wr == WIFI_FAIL_RETRY || wr == WIFI_FAIL_PORTAL) {
  Serial.println("[WIFI] sin conexion -- skip POST y a sleep");
  goSleep(period_s);            // <-- arranque "bueno"
  return;
}
```

Ese camino —y el de `supabaseInit() FAIL`, y el de `BATT_CRITICAL`— sale de
`setup()` sin haber tocado la nube, y contaba igual.

El doc viejo defendía el criterio así, y vale la pena citarlo porque el
argumento es **casi** correcto:

> *Tres boots sin crash dicen que arranca, no que mide bien ni que llega a
> Supabase. Es lo correcto: el criterio anti-ladrillo es* arranca. *Un bin que
> arranca y mide mal se arregla con otro OTA; uno que no arranca, no.*

Sirve para **medir mal** y no sirve para **no llegar a la nube**, y el texto mete
las dos cosas en la misma bolsa. "Se arregla con otro OTA" supone que se le puede
hablar al nodo.

### B · Un bin que se cuelga no resetea

Toda la decisión del rollback miraba el `reset_reason`. Un `while` infinito, un
handshake TLS sin timeout, un `samplerWaitDone()` que no vuelve: nada de eso
produce un reset. El equipo queda colgado, con la verificación pendiente, hasta
que se termina la pila.

## Qué hice

La decisión sale a `otaRescueDecidir()`, **pura** (sin NVS, sin flash, sin red,
sin reloj propio) y **adentro del mismo header que se flashea** — no es un
espejo: lo que se testea es lo que corre.

- **Prueba de alcance.** `otaRescueMarkCycleOk()` se llama después de cualquier
  respuesta 2xx de Supabase. La confirmación pide 3 arranques **y** un viaje de
  ida y vuelta. Dos anclas por familia, para que ningún modo normal se quede sin
  evidencia: en los emisores el `POST readings` y el `GET commands` (un nodo en
  `PAUSED` no hace POST); en el RX el `PATCH devices` —su latido— y el
  `GET commands` **antes** del early return por cola vacía, que es el caso normal.
- **Paciencia.** No confirmar nunca es el mismo ladrillo, más lento. Agotado el
  presupuesto sin una sola prueba de alcance, **rollback**. Dos ejes, porque los
  dos equipos gastan distinto: 9 arranques para el emisor que duerme, 900 s
  encendido para el RX, **que no duerme y cuyo contador de arranques no avanza
  nunca**.
- **Watchdog.** Armado a 180 s con `trigger_panic`, **mientras dura la
  verificación y sólo entonces**: el equipo en operación normal no cambia en
  nada. El cuelgue se vuelve un `ESP_RST_TASK_WDT`, que el rollback ya sabía
  atender. Los 180 s salen del wake legítimo más largo (un OTA con 3 reintentos,
  ~110 s) contra un wake normal de 5,5 s, y además **el bucle de descarga del OTA
  le da de comer**: un OTA sano tomado por cuelgue sería el falso positivo más
  caro posible.

Dos detalles chicos que evitan un bug nuevo: `otaRescueMarkCycleOk()` **no toca
la NVS fuera de una verificación** (corre en todos los wakes de la vida del nodo;
un `putUChar` por wake serían ~52.000 escrituras al año para no cambiar nada) y
**anota una sola vez por arranque**; y el tick del RX **relee la NVS una vez por
segundo**, no una vez por vuelta del `loop()`.

**La asimetría que ordena toda la decisión, escrita en el código:** un rollback
de más cuesta un ciclo de OTA; una confirmación de más cuesta una subida al
REDLER con un cable. Ante la duda, rollback.

Sobre la API del watchdog: se escribe **una sola rama**, la de 3.x, con un
`#error` para core 2.x. Si algún día se compila con uno viejo tiene que romper
fuerte y a la vista, no comportarse distinto en silencio.

## Cómo verificarlo (comandos exactos, sin hardware)

```bash
cd C:\Proyectos\galgas
git fetch origin
git worktree add C:\Proyectos\_rev nocturno/local-2026-09-10-b-el-bin-que-arranca-y-no-vuelve
cd C:\Proyectos\_rev

g++ -std=c++17 -Wall -Wextra -I tools/fakes -o tools/test_ota_rescue.exe tools/test_ota_rescue.cpp
./tools/test_ota_rescue.exe

python tools/check_ota_rescue_wiring.py --mutants

# la prueba de que el checker sirve: contra main tiene que REPROBAR
mkdir /tmp/mainsnap && git archive origin/main firmware/ | tar -x -C /tmp/mainsnap
python tools/check_ota_rescue_wiring.py --root /tmp/mainsnap

# las tres familias (secrets.h no esta en git: se copia del arbol principal)
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_a_emisor
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_b_emisor
arduino-cli compile --fqbn esp32:esp32:esp32:PartitionScheme=min_spiffs firmware/esp_rx_receptor
```

Resultado de anoche:

| Verificación | Resultado |
|---|---|
| `test_ota_rescue.exe` | **127 checks, 0 fallos**, sin warnings (eran 62) |
| `check_ota_rescue_wiring.py --mutants` | **OK · 73 checks · 19/19 mutantes muertos** (eran 50 y 9) |
| el mismo checker con `--root` contra `main` | lo **reprueba: 22 fallas** |
| `arduino-cli compile` × 3 familias | exit 0, sin warnings, 63 % flash / 18 % RAM |

Costo medido contra `main` con el mismo core y el mismo esquema de particiones:
**+1 964 B** de flash en A/B, **+2 232 B** en el RX, **+8 B** de RAM en las tres.

**Cinco tests marcados REGRESIÓN** fallan contra la lógica vieja: que tres
arranques sin llegar a la nube ya no confirmen; que la paciencia agotada haga
rollback; que un bin que sí llegó una vez **no** se tire aunque después se caiga
el enlace; que el RX vuelva por tiempo encendido; y que el watchdog se arme con
panic durante la verificación.

Entre los mutantes nuevos está **"vuelve el defecto"** (`OTA_RESCUE_VERIFY_CYCLES`
en 0, o sea confirmar contando arranques), y los cuatro del watchdog: que no se
arme, que se arme sin panic, que se arme y nadie le dé de comer, y que la
paciencia no venza nunca.

## Qué quedó SIN verificar (necesita hardware)

Los 4 escenarios están en `docs/ota-rescue.md`, en orden de valor:

1. **El cuelgue.** Subir un bin con un `while (true) {}` después del
   `otaRescueCheckOnBoot()`: panic del task WDT a los 180 s y rollback en el
   arranque siguiente. **Es el agujero B entero y lo único que prueba que el WDT
   realmente vigila esta tarea.**
2. **El bin incomunicado.** Subir un bin con la contraseña de WiFi cambiada a
   propósito y verlo volver solo a los 9 wakes. Es el agujero A. Son ~90 min en
   MONITOR: se acorta bajando `period_s` por comando antes de empujar el OTA.
3. **Que un OTA sano no se coma el watchdog.** Un OTA normal *durante* una
   verificación en curso. Es el falso positivo más caro y sólo se mide con la
   descarga real.
4. **El RX por tiempo.** El mismo bin incomunicado en el receptor: a los 15 min
   encendido tiene que volver.

## Deuda anotada, no tocada

- **Nada ata el `.bin` descargado a un `device_id`.** Lo dejó anotado el 09-08-b
  y sigue igual: el `sha256` de la fila se verifica, pero un binario de B subido
  con la versión de A entra en A. La barrera que faltaría es que el propio
  binario declare su `DEVICE_ID`. **Segunda noche que se anota.** [@firmware]
- **El bucket sigue público** (ítem 6 del `QUE_FALTA`). Es de `@backend` y toca
  políticas de Storage. **Tercera noche que se anota.**
- **`BATT_CRITICAL` termina en rollback.** Un equipo con la batería agotada no
  enciende la radio, no junta pruebas de alcance y a las 9 horas vuelve al bin
  anterior. Es un rollback innecesario hacia un binario que ya era bueno, y está
  aceptado a propósito por la asimetría de arriba. Si alguna vez molesta, la
  salida limpia es que el sketch diga "este arranque no intentó la red" en vez de
  inventar un tercer contador. [@firmware]
- **La telemetría `metadata.ota_rescue` no distingue por qué se está
  verificando.** Hoy dice `verifying`; no dice cuántos arranques ni cuántos
  viajes lleva. Con la prueba de alcance adentro, eso ya es información útil para
  el dashboard. [@frontend]
- **`main` tiene cinco `.exe` de test commiteados** en `tools/`. El de esta noche
  **no** viaja en el commit (se regenera con g++). **Tercera noche que se anota
  lo mismo.** [@bibliotecario]
- **El ítem 3 del `QUE_FALTA` de galgas sigue duplicado como 3 y como 4b.** No lo
  toqué: arreglarlo garantiza un conflicto con el branch `09-03`. Se resuelve al
  mergear ése. [@cronista]

## Lo que NO hice, a propósito

- **No toqué `supabase_client.cpp`.** El armado del rescate ya está ahí y anda;
  meter las anclas de la prueba de alcance adentro del downloader compartido
  habría tocado el archivo que pelean los branches del gateway (08-11, 08-25,
  08-26) para no ganar nada.
- **No agregué un tercer contador** para separar "no intentó la red" de "intentó
  y no llegó". Sería especulativo: hoy no hay quien lo lea y la decisión ya está
  bien del lado seguro.
- **No cambié los 3 arranques de la cuota.** Es un número de producto que ya
  estaba calibrado; cambiarlo habría enmascarado si la prueba de alcance
  funciona.
- **No moví `ota_rescue.h` a la biblioteca.** Sigue sin probarse en hardware: se
  cosecha cuando pase el punto 1 de "sin verificar". [@bibliotecario]

## Drift corregido de paso

`docs/ota-rescue.md` decía que el sketch estaba al **94 %** de flash y usaba ese
número para justificar que el costo en bytes importaba. Ese 94 % es del esquema
de particiones **por defecto**; con el `min_spiffs` que usan las tres familias
está al **63 %**. El presupuesto de flash no es el cuello de botella que ese
número sugería.

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-10-b-el-bin-que-arranca-y-no-vuelve`
  (`cb47bad`), sobre `origin/main` (`35a8200`).
- `QUE_FALTA.md` de galgas actualizado (ítem 1 cerrado como "ya está en main" +
  ítem **1b** nuevo con el pendiente de merge).
- Worktree `C:\Proyectos\_noche_galgas_0910b` eliminado, `worktree prune`
  corrido, sin carpetas `_noche*` sueltas. El árbol de `galgas` quedó
  **idéntico**, en `nocturno/local-2026-09-05-la-potencia-que-nadie-cambio`.
- En MATI-HQ quedan **sin commitear, tal como los encontré**,
  `comercial/panamerican/PRESUPUESTO_CERRO_MORO_INTERNO.html`, las bitácoras de
  `dominios/` y `scripts/turno_noche_log.txt`: son de otro trabajo y no me
  corresponde firmarlos.
- Nada corriendo, nada abierto.
