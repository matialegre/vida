# Nocturno LOCAL — 2026-07-14 (worker de la PC, Matías durmiendo)

## Tarea elegida y por qué
**FrioSeguro #10 — vista "Estabilidad del equipo" para el COMERCIO** (frontend,
software puro). Es **PLATA** (tope de la jerarquía) y, a propósito, **rompe el
monocultivo** de las últimas noches.

Recorrí los 4 `QUE_FALTA`, los nocturnos previos (07-11→07-13) y el estado real
de branches. Lo que encontré ordenó la decisión:
- **Las últimas ~5 noches fueron todas herramientas CLI de backend de FrioSeguro**
  (scan_secrets, lint_device_config, resumen-mensual + fixes). Hoy hay **4 branches
  de FrioSeguro sin mergear** + 2 de galgas + 4 de datalogger. El propio worker
  venía anotando "no apilo más deuda de merge" y "FrioSeguro es deuda de DEPLOY,
  no de código". Otro CLI de backend sería más de lo mismo.
- El item de PLATA **más subatendido y NO tocado como software** es el **#10**:
  el dashboard que el comerciante realmente ve. La info de resiliencia que el
  firmware ya emite (reinicios, watchdog, modo de conexión, señal) **solo se veía
  en el panel admin** (`DevicesAdminTable::ResilienceCell`) — el comerciante no
  la ve. Eso es exactamente "renderizar el bloque de resiliencia + vista de un
  vistazo" del #10.
- Es **PLATA**, **verificable offline** (`npm run build` + eslint), **aditivo** y
  de bajo riesgo (ver abajo por qué). galgas/datalogger son octubre (2º) y sus
  wins limpios ya están en branches. cosechador es P2.

Encaja con "UNA tarea bien hecha por noche" y no estaba en ningún branch.

## Hallazgo que hizo la tarea segura (leyendo el código real)
El query del cliente `getDevicesWithReadings` pide `readings?...&order=...&limit=1`
**sin `select=`** → PostgREST devuelve la **fila completa**. O sea: los campos de
resiliencia (`connection_mode`, `wifi_rssi`, `gsm_signal`, `reboot_count`,
`watchdog_count`, `sensor_fault_count`) **ya venían en la respuesta** — solo no se
mapeaban al objeto `reading` del cliente ni se mostraban. Por eso el cambio es:
1. **mapear campos que ya llegan** (cero cambio de query → si una columna no
   existe en el schema, queda `undefined` y la tarjeta simplemente no se muestra:
   imposible romper el dashboard), y
2. **renderizar** una tarjeta de un vistazo.
El panel admin ya mapeaba estos mismos campos (`supabaseClient.js:1007-1012`), así
que existen en la tabla `readings` del proyecto MATIAS.

## Qué hice — branch `nocturno/local-2026-07-14-vista-estabilidad-comercio`
Sale de `main`. Software **aditivo** (+84 líneas, 3 archivos). No toqué firmware,
ni schema, ni datos, ni el query. **NO expuse ningún secreto**: el admin mapea
`wifi_password` al reading — **lo dejé fuera** del mapeo del cliente a propósito.

| Archivo | Qué |
|---|---|
| `web-dashboard/src/supabaseClient.js` | En el mapeo del `reading` del cliente (`getDevicesWithReadings`), agregué `connectionMode`, `wifiRssi`, `gsmSignal`, `watchdogCount`, `rebootCount`, `sensorFaultCount` — **mismos nombres que el mapeo admin**, campos que ya llegaban en la fila. Sin cambiar el `select`/query. Sin `wifi_password`. |
| `web-dashboard/src/App.jsx` | Helpers **puros** `describeConnection(mode)` (WiFi/Datos móviles/Conectado) y `describeSignal(mode, wifiRssi, gsmSignal)` — WiFi por RSSI en dBm (≥-65 Buena / ≥-75 Regular / si no Débil), GSM por CSQ 0-31 del SIM800 (≥18/≥10, 99=Sin dato), defensivos ante `null`. Nueva sección **"🛡️ Estabilidad del equipo"** en la vista del comercio (después de "Info de conexión", antes de `SensorManager`): 3 tarjetas CONEXIÓN / SEÑAL / REINICIOS. Se renderiza **solo si hay algún dato de resiliencia**. |
| `web-dashboard/src/App.css` | `.stability-section` (+ su `h3`) reusa `.status-grid`/`.status-card` (ya responsivo: 2-col mobile) → "de un vistazo" y mobile sin CSS de layout nuevo. Grid forzado a 3 columnas para las 3 tarjetas. |

## Cómo verificarlo (comandos exactos, sin hardware ni nube)
```bash
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-07-14-vista-estabilidad-comercio
cd web-dashboard
npm ci                 # 157 paquetes, ~17 s (ya corrido esta noche)
npm run build          # -> vite build OK
npx eslint src/App.jsx src/supabaseClient.js
```
**Resultado obtenido esta noche** (Node v24.14.0, npm 11.9.0):
- `npm ci` → **OK** (157 paquetes, 17 s).
- `npm run build` → **OK**, `✓ built in 1.53s` (43 módulos, sin errores/warnings de build).
- `eslint` → **8 hallazgos, TODOS pre-existentes** (imports/`catch (e)`/`catch (error)`
  sin usar en líneas ajenas + 3 warnings de `react-hooks/exhaustive-deps` que ya
  estaban). **El código nuevo (`describeConnection`/`describeSignal`/sección
  Estabilidad/mapeo) no agregó ningún hallazgo.** No los arreglé: fuera de alcance,
  quirúrgico.

## Qué quedó SIN verificar (necesita ojos + datos vivos — @tester / @diseno / día)
- **Render real con un device reportando**: no lo vi en pantalla (el worker
  nocturno no abre navegador). Falta que **@tester** lo abra en Playwright contra
  `frioseguro-dashboard.vercel.app` (o local) con un device online y confirme que
  las 3 tarjetas se ven bien y el copy es claro para un comerciante.
- **Ajuste fino de umbrales/copy con @diseno**: los cortes de calidad de señal
  (RSSI -65/-75; CSQ 18/10) son sensatos pero conviene calibrarlos con datos
  reales de una placa instalada. "REINICIOS: Ninguno / N" puede querer un tooltip
  explicativo.
- **Semántica de `connection_mode` y `gsm_signal`**: asumí `connection_mode`
  contiene "wifi"/"gsm" (matching por substring, case-insensitive → robusto ante
  variantes) y `gsm_signal` = CSQ 0-31. Si el firmware emite otra cosa (p. ej.
  dBm en GSM), el label de señal GSM habría que reajustarlo. **A confirmar con
  @firmware** cuando haya una placa SIM800 reportando.

## Reglas respetadas
Nada borrado. No toqué firmware, ni schema, ni datos, ni migraciones, ni el query.
No mDNS (no aplica). **No se expuso ningún secreto** (`wifi_password` deliberadamente
fuera del mapeo del cliente). No stageé `node_modules/` ni `dist/` (gitignored).
`npm ci`/`build` con timeout (terminaron en segundos, sin timeouts). El branch **no
se mergea** hasta que @verificador/@tester lo revisen — pero build + eslint del
código nuevo están limpios y el cambio es aditivo y sin riesgo de query.

## Branch
`nocturno/local-2026-07-14-vista-estabilidad-comercio` (pusheado a origin, 1 commit;
sale de `main`).

## Notas para el @director / @verificador / @tester / @cronista
- **Cambio de patrón deliberado**: tras 5 noches de CLIs de backend apilando 4
  branches de FrioSeguro sin mergear, esta noche fue **frontend client-facing** —
  la cara que retiene el abono. Sigue en pie la sugerencia repetida: **agrupar un
  bloque backend/deploy FrioSeguro de ~1h** de día para bajar la pila de branches
  (secret-scan y lint YA están en main; resumen-mensual + fixes + esta vista
  esperan merge/deploy).
- **Convergencia**: esta vista "de un vistazo" para el comerciante es material
  directo para el lado SCADA/HMI (SCI) y para el pitch comercial (una demo que
  muestra estabilidad genera confianza en la venta).
- **QUE_FALTA #10 actualizado en `main`** (commit `4dc1487`) → "EN BRANCH … pendiente
  de merge".

---

## Adenda — segunda invocación del turno (2:00, misma noche)

El scheduler del nocturno disparó una **segunda vez** el turno de las 2:00. Encontré
la tarea de la noche (#10) **ya hecha y commiteada** (`948da85`), diario completo y
branch `43e15b8` pusheado a origin. Por **disciplina WIP=1 / "UNA tarea bien hecha
por noche"** — y por la advertencia repetida de no apilar más branches de FrioSeguro
sin mergear — **NO inventé una segunda tarea**.

Sí hice **higiene de backup** (cierra el hueco #1 del PORTFOLIO: trabajo sin commitear
en un solo disco; hay precedente del 13-jul "persistí trabajo diurno de @utn"):
- Commiteé `dominios/logo_acceso_remoto.md` (untracked) — nota de **UNIVERSIDAD (SCI,
  prioridad #1)**: checklist para programar los 2 LOGO! (0BA7 + 0BA8) en casa y
  acceso LAN/WiFi/internet vía el TP-LINK. **Sin secretos** (solo "admin/admin"
  genérico y la MAC del LOGO, inocua). Es material de convergencia SCI directo.
- Commiteé el append de `scripts/turno_noche_log.txt` (log del turno con el resumen
  del #10, que había quedado sin commitear).

**No** toqué código, firmware, schema, datos ni branches. Nada borrado. Noche cerrada
sin tarea nueva (paso 5 del protocolo): la tarea real de la noche ya estaba entregada.
