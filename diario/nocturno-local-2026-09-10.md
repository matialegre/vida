# Nocturno local — 2026-09-10

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (**PLATA — prioridad #1 de la
jerarquía**), zona `web-dashboard/` + `tools/` + `docs/`. **Es la primera noche
que se toca el panel**: las 12 anteriores de este repo vivieron en
`firmware_modular/`, `servidor/` y `supabase/`.
**Branch:** `nocturno/local-2026-09-10-el-panel-que-se-queda-verde`
(pusheado, `13f1af6`).
**⚠ Sale de `nocturno/local-2026-08-19-b-fuente-frescura`**, que sale de `main`
(`ddf5134`). **Al mergear éste entra también aquél** — usa su `lib/freshness.js`
y no reimplementa la resta contra el reloj (regla: una sola fuente de verdad).
**No toca** firmware, ni SQL, ni el notificador, ni `data/`. No hay mDNS de por
medio.

**Trabajé en un `git worktree` aparte** (`C:\Proyectos\_noche_frio_0910`, ya
eliminado) porque el árbol de `frioseguro` tiene el KiCad de Matías sin
commitear. **Verificado al terminar: el árbol quedó idéntico** (mismo hash de
`git status`), en el branch `09-04-b` donde estaba.

---

## TL;DR

> **El panel podía quedarse verde sobre un equipo muerto, y el camino que lo
> permitía es el camino sano.** `is_online` se calculaba **una sola vez**,
> adentro de la carga de datos. No es un dato del equipo: es una resta contra el
> reloj, y una resta contra el reloj envejece sola. Con Realtime conectado —el
> caso normal— lo único que vuelve a correr la carga es **un evento de
> `readings`/`alerts`**, que es exactamente lo que un equipo muerto deja de
> generar. Corte de luz, router colgado, ESP32 trabado: la tarjeta seguía
> mostrando 🟢 **Online** y la última temperatura buena, quieta, **para
> siempre**, sin que nada la envejeciera. Y del otro lado, el canal: el
> heartbeat Phoenix se manda cada 25 s y **su respuesta se tiraba** junto con
> los demás mensajes de control. Un WebSocket **medio abierto no dispara
> `onclose`** — y todo el fallback a polling cuelga de `onclose`. El header
> decía **⚡ Realtime**, no llegaba un evento más, el rescate no se activaba
> nunca, y no había ni un log.

## Por qué esta tarea

1. **Es PLATA y es la última milla de lo que se cobra.** Doce noches cerraron la
   cadena adentro del equipo (la sonda que se cae, la temperatura congelada, el
   compresor, el corte de luz, el umbral, Telegram). Lo que faltaba es **la
   pantalla**: el comerciante no ve el firmware, ve la tarjeta. Una cadena de
   aviso perfecta detrás de un panel que muestra verde no se distingue de un
   sistema apagado.
2. **Es la misma enfermedad de siempre, una capa más arriba.** La sonda
   congelada (09-04-b) y el acelerómetro que decía cero (09-09, datalogger):
   *el sistema no falla, contesta bien y dice otra cosa*. Acá el sistema ni
   siquiera contesta — la pantalla contesta por él.
3. **Estaba libre.** Ninguno de los 12 branches abiertos de frioseguro toca el
   dashboard (el único que lo roza, `08-23`, agrega **una** línea en
   `AdminPanel.jsx`). El del 08-19-b lo tocó y **dejó este agujero explícitamente
   abierto**: arregló *cómo se muestra* una fecha, no *cuándo se vuelve a mirar*.
4. **Se hace entera sin hardware.** El único hardware que hace falta para verlo
   es un navegador, y eso queda anotado como pendiente.
5. **Le tocaba a PLATA por jerarquía**: las últimas dos noches fueron
   datalogger (09-09) y frioseguro-firmware (09-09-b).

## Los dos agujeros

### 1. La presencia se estampaba en la carga

```js
return { ...device, is_online: computeIsOnline(device), ... }
```

Parece un campo del equipo. Es una resta contra el reloj. Sólo se refrescaba
cuando volvía a correr `loadData()`, y con Realtime conectado `loadData()` corre
**sólo cuando llega un evento**. El equipo que se muere deja de generar eventos.

Había un **segundo camino al mismo verde**: los devices llegan con `select=*`, y
la tabla `devices` **tiene** una columna `is_online` que se pone en `TRUE` con
cada lectura (`schema_v2.sql`) y que **nada vuelve a poner en `FALSE`**. Entraba
sola por el spread.

### 2. El heartbeat se mandaba y nadie miraba si volvía

```js
if (event === 'phx_reply' || event === 'heartbeat') return
```

Ese `return` descartaba **la única prueba de que el socket está vivo**. Un
WebSocket medio abierto (NAT caducado, WiFi que se fue sin cerrar el socket,
proxy que traga) sigue en `OPEN` para el navegador y no dispara `onclose`. Y el
polling de rescate cuelga de `onclose`.

Aparte, aun con el socket sano, **Realtime puede perder eventos** (RLS, la tabla
fuera de la publicación, un reconnect corto) y nadie los reclamaba después.

## Qué hice

Tres módulos chicos, y el criterio de siempre: **la decisión sale a un archivo
puro que el código de producción IMPORTA** — no es un espejo, lo que se testea
es lo que corre.

- **`lib/presencia.js`** — `conPresencia(devices, ahora)` deriva `is_online` en
  cada render, sobre `freshness.isOnline` (la misma y única resta del
  dashboard). `supabaseClient.js` deja de estamparla y además **saca** la
  columna de Postgres. Si una vista futura se olvida de decorar, queda
  `undefined` ⇒ **offline**: la omisión alarma, no tranquiliza.
- **`lib/useAhora.js`** — el reloj que late (5 s). Sin él, React sólo
  re-renderiza cuando cambia el estado, y el estado sólo cambia cuando llega un
  dato. **El tick no es el umbral**: los 2 minutos de online no se movieron; el
  tick sólo fija cuánto tarda la pantalla en enterarse.
- **`lib/enlace.js`** — la decisión del watchdog, pura (sin WebSocket, sin
  timers, sin red). Socket mudo más de 60 s (dos heartbeats): resincroniza,
  **cierra el socket** para que la máquina de `onclose` levante el polling, y el
  header pasa a **⚠️ Servidor mudo**. Y un **piso duro**: lo que se ve en
  pantalla no puede tener más de 60 s, pase lo que pase con el socket.

Dos detalles de una línea cada uno que evitan un bug nuevo: al cerrar el socket
mudo se **desconectan sus handlers antes** del `close` (si el `close` real llega
más tarde, `_onClose` correría dos veces: dos backoffs, dos reconexiones); y un
**salto de reloj hacia atrás** (cambio de hora, sincro NTP) se lee como
*recién*, no como vencido — reconectar por un salto de reloj sería tirar un
socket sano.

## Cómo verificarlo (comandos exactos, ~2 minutos, sin hardware)

```bash
cd C:\Proyectos\frioseguro
git fetch origin
git worktree add C:\Proyectos\_rev nocturno/local-2026-09-10-el-panel-que-se-queda-verde
cd C:\Proyectos\_rev\web-dashboard
# node_modules no está en git: se puede enlazar el del árbol principal
#   New-Item -ItemType Junction -Path node_modules -Target C:\Proyectos\frioseguro\web-dashboard\node_modules

node --test src/lib/presencia.test.js src/lib/enlace.test.js src/lib/freshness.test.js
npm run build
npx eslint src/

cd C:\Proyectos\_rev
python tools/check_panel_vivo.py --mutantes
```

Resultado de anoche:

| Verificación | Resultado |
|---|---|
| `node --test` (3 suites) | 35 tests, 0 fallos |
| `check_panel_vivo.py --mutantes` | OK · **11/11 mutantes muertos** |
| el mismo checker contra el código anterior al branch | lo **reprueba: 23 fallas** |
| `npm run build` (vite) | OK, 2,67 s |
| `npx eslint src/` | 31 errores / 7 warnings — **exactamente los preexistentes**, cero nuevos |

Los 4 tests marcados **REGRESIÓN** fallan contra la lógica vieja: que el mismo
equipo, con los mismos datos y sólo el reloj corriendo, se vuelva offline solo;
que un `is_online` heredado del servidor no mande; que un socket abierto y mudo
se declare mudo; y que un socket sano con datos viejos se resincronice igual.

El checker de cableado existe por la lección del 09-09-b: **la lógica correcta
que nadie llama** (`state.lastLocalConfigChange`). Los tests prueban la
decisión; el checker prueba que esté enchufada.

## Qué quedó SIN verificar (pide un navegador, no hardware)

1. **Desenchufar un equipo con el panel abierto.** La tarjeta tiene que pasar
   sola a 🔴 Offline en menos de ~2 min, **sin tocar F5**. Es el agujero entero.
2. **Cortarle la red a la PC del panel** (no al equipo) y ver el header ir de
   ⚡ Realtime a ⚠️ Servidor mudo y de ahí a 🔄 Polling.
3. **El socket medio abierto**, que es el caso real y el más difícil de
   provocar: con las DevTools en *offline* el `close` **sí** llega. Se reproduce
   tirando el WiFi desde el sistema operativo.
4. **Que el tick de 5 s no moleste**: panel abierto una hora, mirar CPU y que el
   gráfico no parpadee.

Los 4 son para **@tester** (tiene Playwright) y no necesitan un equipo real:
alcanza con una fila de `devices` con `last_seen_at` viejo.

## Deuda anotada, no tocada

- **La columna `devices.is_online` sigue sin apagarse nunca en la base.** Este
  branch la ignora en el panel, pero cualquier otro consumidor (la app Android,
  un reporte, una Edge Function) la sigue leyendo como si valiera. Apagarla es
  del lado del servidor: hay un `cron-device-silence` propuesto en el branch
  `nocturno/local-2026-08-23-el-que-se-apaga-no-avisa`. [@backend]
- **Que el panel deje de mentir no es avisar.** El equipo que se apaga sigue sin
  generar un aviso por Telegram. Eso es justo lo que cierra el branch del 08-23:
  **son complementarios y conviene mergearlos juntos.**
- **`ClientManager.jsx`** muestra devices de un RPC que devuelve esa columna.
  Hoy no la renderiza (no miente); si algún día la muestra, tiene que pasar por
  `conPresencia()`.
- **El copy es de @diseno**: "⚠️ Servidor mudo" lo puse yo y describe bien lo que
  pasa, pero se lo lee un comerciante, no un dev.

## Lo que NO hice, a propósito

- **No toqué el ítem 10 del `QUE_FALTA` de frente** (bloque "resiliencia" y
  vista mobile). El render de resiliencia ya está en el branch `07-14` sin
  mergear; agregar otra vista arriba de un panel que podía mentir sobre la
  presencia era decorar antes de arreglar.
- **No metí `is_online` derivado en `ClientManager.jsx`.** No lo muestra: sería
  código especulativo.
- **No cambié los 2 minutos del umbral de online.** Es un número de producto
  (los equipos WiFi reportan cada 10 s y laten cada 60 s), no un bug — y
  cambiarlo habría enmascarado si el arreglo del tick funciona.

## Estado al cerrar

- Branch pusheado: `nocturno/local-2026-09-10-el-panel-que-se-queda-verde`
  (`13f1af6`), sobre `nocturno/local-2026-08-19-b-fuente-frescura`.
- `QUE_FALTA.md` de frioseguro actualizado (ítem 10).
- Worktree `C:\Proyectos\_noche_frio_0910` eliminado, `worktree prune` corrido,
  sin carpetas `_noche*` sueltas. `frioseguro` quedó **idéntico** (mismo hash de
  `git status`, mismo branch `09-04-b`).
- En MATI-HQ quedan **sin commitear, tal como los encontré**,
  `comercial/panamerican/PRESUPUESTO_CERRO_MORO_INTERNO.html`, las bitácoras de
  `dominios/` y `scripts/turno_noche_log.txt`: son de otro trabajo y no me
  corresponde firmarlos.
- Nada corriendo, nada abierto.
