# Dominio: COMUNICACIONES (agente @comms)

Doc de dominio + bitácora. El agente lo lee al arrancar y lo actualiza al cerrar.

## Estado del dominio (nacimiento, 2026-07-07)
- galgas-supabase: HTTPS a Supabase OK (cert GTS Root R4 + HTTPClient simple — lección cerrada). Falta: gateway HTTP local del RX (PLAN v5) y prueba de robustez WiFi en planta.
- RuView: LoRa 433 RV1 mesh+ACK OK en banco. Falta: alcance real, salto repetidor, RSSI↔distancia, SSID GIMAP case-sensitive. Regla dura: jamás mDNS; beacon UDP 50505.
- FrioSeguro: SIM800 código completo, JAMÁS probado con SIM real. APN/credenciales producción pendientes.
- Cosechador: NRF24 spec cerrada (payload 8B, auto-ACK), sin armar.

## ⚖️ DOCTRINA: ¿LoRa o WiFi? (pedida por Matías 2026-07-07 — regla de oro del dominio)

**El árbol de decisión (en orden):**
1. **¿El dato entra en decenas de bytes por mensaje?** (agregados, eventos, telemetría) → LoRa es POSIBLE. Si necesitás forma de onda cruda, FFT completa u OTA → **LoRa NO alcanza**: el crudo va a SD local y por el aire viaja solo el resumen (patrón datalogger), o directamente WiFi.
2. **¿Hay AP/router confiable a <30-50m indoor (o <100m con línea vista)?** → **WiFi nomás.** No agregues LoRa donde el WiFi ya llega: es hardware, firmware y una capa de fallas extra. Ej: FrioSeguro en comercios (router del local), ESP-RX de galgas (220V + WiFi de planta).
3. **¿Distancia larga (100m–km), campo abierto, sin infraestructura, o zonas que el WiFi no cubre?** → **LoRa**, con gateway que puentea a WiFi/internet (patrón RuView: nodos LoRa → ESP32-S3 gateway → cloud). Con obstáculos/estructura metálica: mesh con repetidores (frame RV1 ya lo soporta).
4. **¿No hay NADA (ni WiFi ni posibilidad de gateway cerca)?** → GSM/SIM800 (patrón FrioSeguro minero) o registrar offline en SD y descargar después.

**El mito de energía (importante):** "LoRa siempre gasta menos" es FALSO en nuestros sistemas. Un ESP32 que despierta, manda una ráfaga corta por WiFi y vuelve a deep sleep (patrón galgas-supabase validado) compite con LoRa e incluso gana si el AP está cerca — el costo real de WiFi es la CONEXIÓN (DHCP/TLS), no el TX; se amortiza espaciando reportes. LoRa gana sin discusión cuando: la distancia obligaría a repetidores WiFi, el nodo reporta muy seguido (conexión WiFi cara por ciclo), o el receptor debe escuchar continuo (RX LoRa duty-cycled << WiFi asociado).

**Resumen por sistema (estado actual):**
| Sistema | Enlace correcto | Por qué |
|---|---|---|
| Galgas Dreyfus (emisores) | WiFi en ráfaga + deep sleep → RX local/Supabase | planta con infra, payload chico, ya validado |
| Galgas RX/gateway | WiFi (220V) | enchufado, es el puente |
| Datalogger RuView (nodos) | **LoRa** → gateway ESP32-S3 | distancia/zonas sin WiFi, telemetría de agregados; crudo queda en SD |
| FrioSeguro comercios | WiFi del local (fallback GSM si el local no tiene) | AP a metros |
| FrioSeguro minero | WiFi campamento + fallback SIM800 | infra irregular |
| Cosechador | NRF24 punto a punto | 2-10m, 8 bytes, ya especificado |

**Regla final:** ante la duda, prototipá con WiFi (ya lo dominás, debug fácil) y migrá a LoRa SOLO si una prueba de alcance real lo exige. La prueba de alcance manda, no la intuición.

## Métricas de enlaces (tabla viva)
| Enlace | Escenario | RSSI | Loss | Fecha |
|---|---|---|---|---|
| (vacío — completar con pruebas reales) | | | | |

## Bitácora
- 2026-07-07 — Agente creado por Claude Fable. Próximo paso sugerido: plan de prueba de robustez WiFi de galgas-supabase (cortes inducidos + reconexión) y prueba de alcance LoRa de RuView.
