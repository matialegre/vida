# Nocturno local — 2026-09-09-b

**Trabajador:** worker nocturno local (Matías durmiendo). **Segundo turno** de la
noche — el primero fue `nocturno-local-2026-09-09.md` (datalogger, el acelerómetro
que decía cero).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA — prioridad #1 de la
jerarquía**), zona `firmware_modular/` + `tools/` + `docs/`.
**Branch:** `nocturno/local-2026-09-09-b-el-umbral-que-vuelve-solo`
(pusheado, `b8cba7c`).
**Sale de `main` (`2ac3a7d`) limpio**, sin ningún otro branch mergeado adentro.
**No toca** `web_api.h`, `alerts.h`, `sensors.h`, `door_sensors.h`,
`power_monitor.h`, `current_sensor.h`, el panel, el servidor, SQL ni `hardware/`.

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_frio_0909b`, ya
eliminado) porque el árbol de `frioseguro` tiene el KiCad de Matías sin commitear
(TermoVigía Mini/Lite) y un `checkout` lo habría tocado. **Verificado al
terminar: el árbol quedó idéntico**, en el branch `09-04-b` donde estaba, con los
mismos 9 archivos modificados/sin trackear.

---

## TL;DR

> **El umbral que decide si el equipo alerta se puede cambiar desde dos lugares,
> y ninguno de los dos quedaba.** Lo que se editaba en el dashboard vivía **sólo
> en RAM** —`supabaseRefreshDeviceName()` nunca llamaba a `saveConfig()`—, así
> que el próximo arranque restauraba el valor viejo de NVS. Se recuperaba al
> minuto, *si había internet*: o sea que el equipo reboota después de un corte de
> luz y **vigila la cámara llena con el umbral de fábrica** mientras el router
> todavía no levantó. Y del otro lado, el panel local era un adorno:
> `web_api.h` escribía `state.lastLocalConfigChange = millis()` con el comentario
> *"para evitar que Supabase la pise"* y **ese campo no lo leía nadie**. El
> instalador ajustaba el umbral parado frente al equipo, veía el
> `{"success":true}`, y **60 segundos después** el sync lo pisaba con el valor
> viejo, sin un log.

## Por qué esta tarea

1. **Es PLATA y es la regla con la que se cobra.** El abono se paga por *"el
   servicio avisa"*. Las últimas noches cerraron el camino de la señal (la sonda
   que se cae, la temperatura congelada, el compresor, el corte de luz) y el de
   la entrega (Telegram, la cola del servidor). Faltaba lo de más arriba: **con
   qué número se compara.** Una cadena de aviso perfecta sobre el umbral
   equivocado no sirve.
2. **Está libre.** Revisé los 34 branches abiertos de frioseguro: **ninguno**
   toca `storage.h` ni `supabaseRefreshDeviceName()`. Tres tocan `web_api.h`
   (08-21-b, 08-26, 08-27) y por eso **este branch no toca `web_api.h`**: no
   hacía falta, `handleApiSetConfig()` ya escribe la marca que ahora sí se lee.
3. **Descarté lo que ya estaba tomado.** El ítem 18 del `QUE_FALTA` (defrost/
   cooldown en `alerts.h`) **ya está arreglado** en el branch `08-18`, y el
   camino de Telegram lo cerró el `09-01-b`. Los dos módulos que no compilan
   (`current_sensor.h`, `power_monitor.h`) tienen su branch del 09-08 y 09-07-b.

## Los tres agujeros

Los cuatro números que deciden si el equipo alerta —`temp_critical`,
`alert_delay_sec`, `door_open_max_sec`, `defrost_cooldown_sec`— se editan desde
el panel local (LAN del comercio) y desde el dashboard en la nube.

**(1) Lo remoto no sobrevivía un reboot.** `supabaseRefreshDeviceName()` asignaba
a `config` y listo. Ningún `saveConfig()`. `loadConfig()` restauraba NVS en el
arranque siguiente. La ventana de exposición es corta —60 s— **salvo cuando no
hay internet**, que es precisamente la situación posterior a un corte de luz, a
un watchdog o a un OTA.

**(2) Lo local se pisaba solo.** El comentario del código describe una protección
que no existe:

```c
// Marcar timestamp de config local para evitar que Supabase la pise
state.lastLocalConfigChange = millis();
```

`grep` sobre el repo entero: **una sola aparición, la escritura**. Nadie lo lee.
Y como la nube repite su valor cada 60 s para siempre, la comparación vieja
(`newTempCrit != config.tempCritical`) hacía que cada ronda pareciera una edición
del dashboard.

**(3) El valor remoto entraba sin validar.** `tools/lint_device_config.py` existe
justo para atajar un `alert_delay_sec = 0` o un orden de umbrales roto — pero
corre **antes de flashear**. Lo tipeado en el dashboard no pasaba por ahí.

## Qué hice

`firmware_modular/config_sync_model.h`: la decisión sale de la función de red a
un header **puro** (sin Arduino, sin HTTP, sin NVS) que `supabase.h`
**incluye** — no es un espejo en otro lenguaje: lo que testea el `.cpp` es lo
que se flashea. Tres reglas:

- **R1 · Sanidad.** Campo por campo, con los mismos rangos que el lint de
  flasheo. Un valor rechazado **no se anota como visto**, así que si corrigen el
  dashboard la corrección entra sola en la ronda siguiente.
- **R2 · Cambio real.** Un valor remoto se aplica sólo si difiere del último
  valor remoto **visto**, no del actual. La nube deja de ganar cada minuto y
  gana cuando alguien la editó de verdad. **Ésta es la regla que le da sentido
  al panel local**: sin ella no hay forma de que un cambio local sobreviva.
- **R3 · Ventana local.** Un cambio local de hace menos de 5 min difiere la
  ronda entera. Cubre la carrera chica: el `GET` ya en vuelo con los valores de
  antes.

El snapshot de "lo último visto" **se persiste en NVS** junto a la config (5
claves nuevas en `storage.h`), porque sin eso el primer sync después de cada
reboot volvería a parecer una edición y pisaría el panel local otra vez.
`saveConfig()` queda **condicionado** a que algo haya cambiado: esta función
corre cada 60 s de por vida, y un guardado incondicional serían ~525.000
escrituras a NVS por año para no cambiar nada.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\frioseguro
git fetch origin
git worktree add C:\Proyectos\_rev nocturno/local-2026-09-09-b-el-umbral-que-vuelve-solo
cd C:\Proyectos\_rev

g++ -std=c++17 -Wall -Wextra -O2 -o tools/test_config_sync.exe tools/test_config_sync.cpp
./tools/test_config_sync.exe

arduino-cli compile --fqbn "esp32:esp32:esp32:PartitionScheme=min_spiffs" firmware_modular
```

Resultado de anoche:

| Verificación | Resultado |
|---|---|
| `test_config_sync.exe` | 49 ok, 0 fail, sin warnings |
| `arduino-cli compile` | exit 0, 65 % flash, 16 % RAM, sin warnings |

Las dos regresiones que motivaron el branch están escritas como test: que un
cambio remoto pida persistencia, y que la nube repitiendo su valor **no** pise
un cambio local.

## Qué quedó sin verificar (necesita hardware)

Los 5 escenarios de banco están en `docs/config-sync.md`. En orden de valor:

1. **Cambiar el umbral en el dashboard y cortarle la luz al equipo.** Al volver
   tiene que arrancar con el valor nuevo, sin internet. Es el agujero (1) entero.
2. **Cambiar el umbral en el panel local y esperar 3 minutos.** No lo tiene que
   pisar nadie. Antes de este branch volvía al valor viejo al minuto.
3. **Cambiar el panel local y después editar el dashboard.** Gana el dashboard
   dentro del minuto siguiente y queda persistido.
4. **Poner `alert_delay_sec = 0` en la fila de `devices`.** El serial tiene que
   decir `1 campo(s) fuera de rango, descartado(s)`.
5. **Equipo virgen** (NVS borrada): la primera ronda adopta lo que diga la fila.

## Deuda anotada, no tocada

- **La config local nunca sube.** El panel escribe abajo y no hace `PATCH` a
  `devices`. Con R2 el equipo hace lo correcto, pero **la pantalla del dashboard
  miente** hasta la próxima edición. Cerrarlo pide `UPDATE` sobre `devices` con
  la anon key, o sea RLS: es decisión de @backend, no de una noche.
- **`config_version` se selecciona y no se usa.** Ya viaja en el `select=` y
  nadie la mira. Si el dashboard la incrementara en cada edición, R2 podría
  decidir por versión en vez de campo a campo.
- **`temp_max` no se sincroniza.** Sólo entra por el panel local o por
  `config.h`; R1 lo usa como referencia pero la nube no lo puede cambiar.
- **`saveConfig()` no chequea el resultado de `prefs.put*()`.** Una NVS llena
  falla en silencio y el problema vuelve a ser el mismo: parece guardado y no está.

## Estado del árbol

`C:\Proyectos\frioseguro` quedó exactamente como estaba: branch
`nocturno/local-2026-09-04-b-la-temperatura-que-no-se-midio`, los mismos 4
archivos modificados y 5 sin trackear del KiCad de TermoVigía. Worktree
eliminado, `git worktree prune` corrido, sin carpetas `_noche*` sueltas.

**Para mergear:** el branch sale de `main` limpio y no depende de ningún otro.
Se puede mergear en cualquier orden respecto de los 34 abiertos.
