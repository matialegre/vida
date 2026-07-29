# Nocturno local — 2026-07-28-b (2º turno de la noche)

**Trabajador nocturno local** (Matías durmiendo). Una tarea, bien hecha.

## Tarea elegida
**Corregir un cry-wolf del SCADA de galgas** (la vista "Planta" que ve Dreyfus): el umbral
visual `TH_VPP_MONITOR` estaba mal calibrado y dejaba las cards en ámbar "MONITOREO" de
forma permanente durante operación normal. De paso, cerré el **drift del item #9** de
`galgas/QUE_FALTA.md` (decía "integrar SCADA — pendiente" cuando ya está integrado).

## Por qué esa y no otra
- **Jerarquía:** es P0-octubre (categoría 2) y toca "la cara que Dreyfus ve" en la parada;
  además converge con el final de **SCI** (SCADA/alertas), categoría 1. Los bloqueantes de
  PLATA/UNI que eran software o ya están en branch (32 branches esperando merge — el cuello
  real hace ~2 semanas) o necesitan hardware/humano.
- **No estaba en ningún branch** (los 12 branches nocturnos de galgas son rx/vpp/energy/
  alert-replay/ota/readme-drift/firmware-check — ninguno toca el SCADA).
- **Es un defecto de correctitud, no una decisión de diseño ni de plata ni de hardware** →
  entra de lleno en el mandato del turno nocturno (solo software, verificable offline).
- Descarté: (a) escribir otro modelo/test offline — el cuello es merge humano, no producción;
  (b) el fix del alert-model de FrioSeguro (item #18) — necesita confirmación en hardware
  (generator≠evaluator); (c) integrar el SCADA "de cero" — ya estaba hecho.

## El hallazgo (con evidencia)
- Firmware, fuente de verdad del disparo de ALERTA: `SELF_TRIGGER_VPP_V = 0.040f` (40 mV
  pico-pico) — `firmware/esp_a_emisor/config.h:123` y `esp_b_emisor/config.h:89`.
- Firmware, vpp de **reposo** documentado: `config.h:108` → *"Periodo 25s -> vpp pequeno
  (0.03V) -> NO triggea ALERTA en operacion normal"* → **~30 mV en operación normal**, con
  ruido 5 mV RMS (`DEV_SIM_NOISE_RMS_V`).
- El SCADA real (`web/src/views/PlantaView.jsx:23`) clasificaba con `TH_VPP_MONITOR = 0.020`
  (20 mV). Como el reposo (~30 mV) es **mayor** que 20 mV → `computeStage` devolvía
  `MONITOR` siempre → **card ámbar permanente en operación normal** = cry-wolf, desensibiliza
  al operario justo antes de la parada.
- La banda MONITOR es **solo visual** (no existe en el firmware); es una zona de vigilancia
  entre reposo y el ALERT de 40 mV.

## Qué hice
Branch `nocturno/local-2026-07-28-b-scada-monitor-threshold` en `C:\Proyectos\galgas`:
1. `web/src/views/PlantaView.jsx`: `TH_VPP_MONITOR` **0.020 → 0.035** (30 mV reposo + 1σ de
   ruido 5 mV, quedando 5 mV por debajo del ALERT de 40 mV), con comentario que cita la
   evidencia. **La lógica de ALERTA (40 mV) NO se toca** → imposible que el fix cause una
   alerta perdida; el peor caso es una banda ámbar más angosta.
2. `redler/README.md`: la tabla de estados NORMAL/MONITOR/ALERT mentía (decía MONITOR
   25-40 mV, también por debajo del reposo) → alineada a los valores reales y aclarada como
   banda SOLO visual del dashboard.
3. `QUE_FALTA.md` (en el branch): item #9 marcado HECHO con evidencia (vive en PlantaView) +
   nota de afinado del borde contra `field_captures`.

En `main` de galgas (commit `bbe095f`, pusheado): puntero `🔀 EN BRANCH` en el item #9 con
la nota de drift, siguiendo la convención del repo (para que quien lea main sepa que hay un
fix esperando merge).

## Cómo verificarlo (comandos exactos)
```bash
cd C:/Proyectos/galgas
git checkout nocturno/local-2026-07-28-b-scada-monitor-threshold
# el fix + su comentario con evidencia:
grep -n "TH_VPP_MONITOR" web/src/views/PlantaView.jsx      # -> 0.035
# la fuente de verdad del reposo y del alert:
grep -n "vpp pequeno\|SELF_TRIGGER_VPP_V" firmware/esp_a_emisor/config.h
# build offline (lo corrí, pasa):
cd web && npm run build                                     # vite OK, 394 módulos, ~4.7s
```

## Verificado offline
- `web/ npm run build` → **OK** (vite 5.4.21, 394 módulos, 4.72 s, sin errores; el warning de
  chunk >500 kB es preexistente, no relacionado).
- Consistencia de umbrales: firmware ALERT 40 mV == `TH_VPP_ALERT` 0.040 ✔; nuevo MONITOR
  35 mV queda estrictamente entre reposo (30) y alert (40) ✔.

## Sin verificar (hardware / campo — para Matías o @muestreador de día)
- El **borde exacto** del MONITOR (35 mV es una estimación derivada de los specs
  documentados). Validarlo contra `data/field_captures/` con señal real de galga
  (READ-ONLY, no lo toqué). Puede que la banda quiera ser 33 o 36 mV según el ruido real.
- Que el operario efectivamente vea NORMAL (verde) en reposo con un device reportando en
  vivo — eso lo mira @tester/@diseno en pantalla cuando haya datos reales.

## Branch
`nocturno/local-2026-07-28-b-scada-monitor-threshold` (galgas) — commit del fix + push.
Puntero en `main` de galgas: commit `bbe095f`.

## Nota
Encontré 3 archivos de bitácora sin commitear de sesiones previas (drift de otro worker):
`dominios/firmware.md` (drive-torno-esp32s3), `dominios/frontend.md` (Monopoly del auto) y el
log del wrapper. No son míos; los dejé y los commiteé aparte para que no generen conflicto en
el próximo `git pull`.
