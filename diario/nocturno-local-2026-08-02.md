# Nocturno local — 2026-08-02

**Trabajador:** worker nocturno local (Matías durmiendo).
**Repo tocado:** `C:\Proyectos\frioseguro` (P1 — PLATA, la palanca de abonos).
**Branch:** `nocturno/local-2026-08-02-telegram-gate-model` (pusheado a origin, commit `3eec6e8`).

## Tarea elegida y por qué

Jerarquía: PLATA y UNIVERSIDAD primero. Las últimas 6 noches fueron todas a galgas/cuartel
(octubre = 2º), así que revisé primero FrioSeguro. Los ítems del `QUE_FALTA.md` que quedan
sin branch son casi todos de hardware/cloud (flashear, SIM800, NTP, migración SQL, caja
IP65) o decisiones de Matías (precio, contrato). El único hueco de **software puro,
verificable offline y no brancheado** que encontré es además el más caro de todos:

**el camino de AVISO.** FrioSeguro se cobra por una promesa: *"el servicio avisa"*. La
**decisión** de alertar ya tiene oráculo offline (`tools/alert_model.py`, branch 07-18) —
pero la **entrega** del aviso, el último metro hasta el celular del comerciante, no tenía
ninguna verificación. Y ahí no hay 4 caminos: hay **uno solo**. Las cuatro fuentes de
alerta del firmware

| Fuente | Archivo | Dispara a |
|---|---|---|
| Temperatura crítica | `alerts.h:28-66` | 300 s sostenidos (`alertDelaySec`) |
| Puerta abierta | `door_sensors.h:154-166` | 120 s |
| Corte / retorno de luz | `power_monitor.h:111-143` | ~3 s (debounce) |
| Sobrecorriente | `current_sensor.h:160-176` | > 20 A |

desembocan todas en `telegram.h::sendTelegramMessage`, que tiene **un único gate global de
300 s** (`state.lastTelegramAlert`, `telegram.h:24`) que nadie había ejercitado nunca.

## Qué hice

1. **`tools/telegram_gate_model.py`** — oráculo (espejo 1:1, no versión limpia) del gate y
   de los 4 call-sites, stdlib pura, sin red ni hardware (el código HTTP se inyecta por
   parámetro). Distingue dos cosas que el firmware confunde:
   - **entregado**: el POST devolvió 2xx → el cliente se entera.
   - **marcado**: la máquina de estados anotó "ya avisé" (`door->alertSent`,
     `powerState.alertSent`, `overcurrentAlert`, `state.alertActive`).
   `marcado && !entregado` = el nodo se cree que avisó, no reintenta, el comerciante nunca
   se entera. Es la propiedad que miden los tests (`Notification.silently_lost`).
2. **`tools/test_telegram_gate_model.py`** — 18 tests agrupados por hallazgo. Los `test_h*`
   fijan el comportamiento **actual** (cuando @firmware aplique un fix, el test falla — ese
   fallo ES la evidencia del fix); los `test_ok_*` fijan lo que hoy funciona bien y no se
   debe romper (el gate frenando spam de una misma fuente, avisos espaciados entregándose).
3. **`docs/telegram-gate-model.md`** — hallazgos + fixes candidatos + alcance.
4. `QUE_FALTA.md`: ítem nuevo **#19** anotado `EN BRANCH ... (pendiente de merge)`.

## Hallazgos (con test que los demuestra — NO corregidos, generator≠evaluator)

- **H1 — ventana muda de 5 minutos después de CADA arranque.** `SystemState state;` es una
  global (`firmware_modular.ino:62`) → `lastTelegramAlert = 0` al bootear, y `millis()` también
  arranca en 0 ⇒ `millis() - 0 < 300000` es verdadero los primeros 300 s de vida del nodo.
  No es un caso raro: es exactamente la ventana posterior a **un corte de luz, un reset por
  watchdog o un reflasheo OTA**. El aviso de corte de luz (nace a los ~3 s) y el de puerta
  abierta (120 s) se descartan **y quedan marcados como enviados**. La alerta de temperatura
  zafa **por el borde** (300 s de delay vs 300 s de ventana), por casualidad, no por diseño.
- **H2 — un gate para 4 fuentes, y el descarte no se difiere: se pierde.** Una puerta abierta
  silencia 5 minutos a la temperatura crítica que venga atrás. En la tormenta realista (se
  corta la luz → alguien abre la puerta para mirar → sube la temperatura), de 4 eventos en 5
  minutos al cliente le llega **1** y los otros 3 quedan marcados como avisados. Un corte de
  luz de menos de 5 min avisa el corte pero **no** el "luz restaurada".
- **H3 — un envío fallido cuenta como enviado.** `state.lastTelegramAlert = millis()`
  (`telegram.h:46`) corre después del POST **sin mirar el código de respuesta** (solo se
  imprime por Serial) ⇒ un 429 (rate limit de la propia API de Telegram), un 500 o un `-1`
  por TLS caído consumen la ventana igual: el aviso se pierde **y** bloquea al siguiente.
- **H4 — las salidas tempranas por config también marcan "ya avisé".** Los 3 call-sites
  no-temperatura hacen `if (internet && telegramEnabled) sendTelegramAlert(msg);` y marcan
  su flag **fuera del `if`** ⇒ sin internet, con Telegram deshabilitado o con token vacío
  (placa sin provisionar, ítem #4) el evento se da por avisado y no se reintenta al volver
  la conexión.

Fixes candidatos escritos en el doc (flag `telegramEverSent` para H1; gate por fuente para
H2; `sendTelegramMessage` devolviendo `bool` y call-sites marcando según el retorno para
H3/H4). **Ninguno aplicado**: son cambios de firmware que se confirman en banco.

## Cómo verificarlo (comandos exactos)

```
cd C:\Proyectos\frioseguro
git checkout nocturno/local-2026-08-02-telegram-gate-model
python -m unittest tools.test_telegram_gate_model -v     # -> Ran 18 tests, OK
```

## Qué quedó sin verificar (necesita banco/hardware)

- Que H1 y H3 se den tal cual en la placa real: hay que **rebootear una placa con la puerta
  abierta** (o cortarle la luz) y ver que el mensaje no llega, y forzar un POST fallido
  (cortar DNS/TLS) y ver que el siguiente aviso se bloquea igual. El modelo predice el
  resultado; la placa lo confirma.
- Los fixes candidatos no se compilaron (no toqué firmware). Compilar el firmware modular
  requiere el core ESP32 en el IDE — trabajo de día.
- La ruta **SMS/SIM800** (`sim800SendPowerAlert`) **no** pasa por este gate y no está
  modelada: en las placas con SIM el corte de luz sigue avisando por SMS aunque Telegram
  quede mudo. Vale como mitigación parcial de H1 solo en esas placas.

## Estado

- Branch `nocturno/local-2026-08-02-telegram-gate-model` pusheado (1 commit).
- `QUE_FALTA.md` de frioseguro: ítem **#19** nuevo, marcado EN BRANCH.
- 4 repos intactos salvo el branch de trabajo. `data/field_captures` de galgas no tocado.
- ⚠️ **MATI-HQ tenía trabajo de día SIN COMMITEAR** cuando arranqué (modificados
  `agentes/esquematico.md`, `agentes/pcb.md`, `dominios/{diseno,esquematico,firmware,hardware,pcb,utn}.md`,
  `scripts/turno_noche_log.txt`; sin trackear `agentes/diseno3d.md` y `dominios/diseno3d.md`).
  **No los toqué ni los commiteé** — no es trabajo mío. Matías: commitealos antes del próximo
  `git pull`, o la rutina cloud va a chocar.
- Recordatorio del cuello de botella: la cola de merge sigue creciendo (frioseguro ya suma
  ~11 branches). El tooling de drenaje (`tools/merge_queue_status.py` +
  `tools/resolve_doc_conflicts.py` en MATI-HQ) está listo; falta la sesión humana.
