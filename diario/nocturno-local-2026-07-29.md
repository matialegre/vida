# Nocturno local — 2026-07-29 (worker de la PC, Matías durmiendo)

## TL;DR para Matías (si leés una sola cosa)
Revalidé los umbrales de `v_pp` del sistema de galgas **contra la señal REAL de campo**
(las capturas Dreyfus del 13-feb) — algo que hasta hoy se había calibrado contra un
comentario del simulador, no contra el terreno. Escribí un tool (`tools/analyze_vpp_field.py`,
read-only sobre las capturas sagradas) + 9 tests + informe. **Dos hallazgos:** (1) el ALERT de
40 mV tiene margen ENORME (el v_pp real es ≤14 mV en toda condición normal) → el fix del SCADA
de anoche (MONITOR=35 mV) queda validado y hasta conservador; (2) **hay un cry-wolf latente en
el firmware v3**: su self-trigger dispara con un solo burst y sin hold, así que un dropout de
0.0 V (los hay: 1.2 % de las muestras con el motor prendido) se vuelve **ALERTA espuria** — 3 %
de los segundos con motor ON. El legacy tenía `HOLD_SEC=1.5s`; v3 lo perdió. **No lo arreglé de
noche** (es firmware, se confirma en banco); lo dejé documentado con evidencia y fix candidato
para @firmware. **Branch `nocturno/local-2026-07-29-vpp-field-characterization`** (galgas).

## Tarea elegida y por qué
**Caracterizar el `v_pp` real de las capturas de campo contra los umbrales del firmware/SCADA**
— bloqueante **#2 de galgas** ("Revalidar umbral v_pp>40mV con señal real", P0-octubre) y cierra
literal el pendiente de campo que dejó el fix del SCADA del 2026-07-28-b.
- **Categoría 2 (octubre) y toca "la cara que Dreyfus ve"**: la fiabilidad de la alerta es el
  corazón del sistema en la parada. Además converge con **Medidas Electrónicas 2**
  (caracterización/incertidumbre — el mapeo del PORTFOLIO).
- **Es genuinamente nuevo y NO estaba en ningún branch:** los 13 branches nocturnos de galgas son
  rx/vpp-audit/energy/alert-replay/ota/readme/firmware-check/scada — **ninguno** mide el v_pp
  real de las capturas en la ventana del firmware. La auditoría de vpp del 07-11 fue sobre el
  código, no sobre los datos.
- **Offline y read-only sobre datos sagrados:** el análisis solo LEE `data/field_captures/`
  (nunca escribe ni reprocesa in-place — regla del README de las capturas). Cero hardware, cero
  red, cero riesgo de timeout (stdlib pura, corre en <5 s).
- **Ataca el hueco de fondo con honestidad (generator≠evaluator):** encontré un defecto de
  firmware pero NO lo apliqué a ciegas — lo dejo con test/evidencia para que @firmware lo
  confirme en banco.

## Por qué NO otra tarea (descarte honesto)
- **Otro branch de producción (modelo/test):** el sistema lleva ~10 noches gritando que el cuello
  es **merge humano** (32 branches). Pero esta tarea es distinta: no es "otro modelo especulativo",
  es **medir la realidad** contra la que ya se venían calibrando umbrales a ciegas — y el propio
  informe de anoche pidió explícitamente "validar el borde exacto contra `field_captures`". Era el
  siguiente paso natural, no trabajo manufacturado.
- **PLATA (FrioSeguro):** anoche se cerró el último deliverable de software puro (plantillas
  WhatsApp). Lo que queda es hardware/humano (marca, flasheo, caja, visita).
- **Aplicar el fix de firmware que encontré:** es exactamente lo que NO se hace de noche sin
  hardware (mismo criterio que el alert-model de FrioSeguro #18).

## El hallazgo (con evidencia)
La ventana que faltaba: el firmware calcula `v_pp = v_max - v_min` sobre `BURST_SAMPLES_NORMAL=500`
muestras @ 500 Hz = **1.0 s** (`adc_sampler.cpp:169`, `shared/protocol.h:51`, `config.h:115/123`).
El tool reconstruye esa ventana exacta desde los `bufA` crudos de cada paquete.

Resultado sobre las 12 capturas (mV, ventana 1 s):
- **Reposo/motor/ensayo:** v_pp mediana **6–14 mV**, p95 ≤19, max ≤24 → **muy por debajo** del
  ALERT (40) y del MONITOR (20 main / 35 branch). El "reposo ~30 mV" del `config.h:108` era una
  estimación del **simulador**, pesimista frente al campo real (~6 mV). → el fix MONITOR=35 mV de
  anoche es **seguro y hasta conservador**.
- **Dropouts:** el campo tiene muestras `== 0.0 V` (1.2 % con motor ON, 5.6 % en la captura de la
  rotura). Como `v_pp = max-min`, **una sola muestra en 0.0 V** vuelve v_pp ≈ 1.5 V ≫ 40 mV. En
  `132330` (motor ON, operación NORMAL) eso hace que **3.0 % de los segundos crucen el ALERT** solo
  por dropouts; con un guard de rango bajan a **0.0 %**.
- El self-trigger v3 dispara con **1 burst y sin persistencia** (`esp_a_emisor.ino:259`). El legacy
  tenía `HOLD_SEC=1.5s`; el informe de ensayos §9.2 recomienda 2–3 s. → **cry-wolf en el ALERT**.
- **El guard no enmascara roturas reales:** en `reposo_1.csv` la CADENA B ROTA real sigue > ALERT
  con guard (2.9 %, max 463 mV). Limpia el dropout, no el evento físico. (Buena validación cruzada.)

## Qué hice
Branch `nocturno/local-2026-07-29-vpp-field-characterization` en `C:\Proyectos\galgas`:
1. `tools/analyze_vpp_field.py` — oráculo de caracterización (stdlib; parseo robusto de `bufA` por
   regex porque el `raw_json` sin comillas rompe un split CSV posicional; ventaneo alineado al burst
   del firmware con guard de dropout dentro de cada ventana). Read-only sobre las capturas.
2. `tools/test_analyze_vpp_field.py` — **9 tests OK** (sintéticos: parser anti-coma, pp de ventana
   conocida, guard que limpia dropout, veredicto). No tocan las capturas reales.
3. `docs/vpp-field-characterization.md` — método + tabla + los 2 hallazgos + fix candidato +
   qué queda para hardware.
4. `QUE_FALTA.md` (en el branch): item #2 anotado con los hallazgos.

En `main` de galgas (commit `b717127`, pusheado): puntero `🔀 EN BRANCH` en el item #2.

## Cómo verificarlo (comandos exactos, sin hardware)
```bash
cd C:/Proyectos/galgas
git checkout nocturno/local-2026-07-29-vpp-field-characterization
python tools/test_analyze_vpp_field.py     # 9 tests OK
python tools/analyze_vpp_field.py          # tabla de 12 capturas + veredicto
# la ventana del firmware que se está reproduciendo:
grep -n "BURST_SAMPLES_NORMAL" firmware/shared/protocol.h        # 500
grep -n "self_alert\|v_pp = v_max" firmware/esp_a_emisor/*.ino firmware/esp_a_emisor/*.cpp
# capturas intactas (read-only respetado):
git status --short data/field_captures/    # vacío
```

## Verificado offline
- `python tools/test_analyze_vpp_field.py` → **9/9 OK** (<0.1 s).
- `python tools/analyze_vpp_field.py` → corre sobre las 12 capturas en <5 s, tabla + veredicto
  coherentes; sin escritura sobre `data/field_captures/` (`git status` limpio ahí).

## Sin verificar (hardware / banco — para @muestreador + @firmware)
- Que el ADC v3 real produzca el mismo tipo de **dropout (0.0 V)** que el pipeline legacy de estas
  capturas (v3 lee por ISR a 500 Hz; hay que ver su patrón en banco).
- El **valor exacto del guard** (`[0.3, 3.2] V`) contra el acondicionamiento real (INA333/offset).
- **Aplicar el fix** (guard de outliers y/o restaurar hold de 2–3 s): decisión de @firmware con
  verificación en hardware — el tool lo deja documentado, no lo aplica.

## Branch
`nocturno/local-2026-07-29-vpp-field-characterization` (galgas) — commit `877390b` (deliverable) +
push. Puntero en `main` de galgas: commit `b717127`.

## Reglas respetadas
Solo software (tool + tests + docs) + lectura. `data/field_captures/` **solo leído, nunca
escrito** (respetada la regla INMUTABLE del README); sin `rm -rf`/`reset --hard`/`push --force`;
sin migraciones; sin mDNS; sin tocar firmware/backend de producción (el hallazgo queda documentado,
no aplicado); sin decisiones de plata/hardware; stdlib pura → cero riesgo de timeout.
