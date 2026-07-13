# Dominio: frontend (agente @frontend)

Doc de dominio + bitacora. El agente lo lee al arrancar y lo actualiza al cerrar. Backlog inicial: ver seccion "Tu backlog inicial" en ~/.claude/agents/frontend.md (copia en ../agentes/frontend.md).

## Bitacora
- 2026-07-07 - Agente creado por Claude Fable con backlog real de los repos migrados (C:/Proyectos).

- 2026-07-13 - **FrioSeguro dashboard migrado a Vercel + Supabase nuevo** (@frontend):
  - **URL prod: https://frioseguro-dashboard.vercel.app** (proyecto Vercel `frioseguro-dashboard`, scope `alegrematiasdev2-dels-projects`). HTTP 200 verificado con curl; bundle en prod apunta SOLO a `cjdluhemschrynijzvap.supabase.co` (cero rastro del proyecto viejo `nwugnhsktcihusopfldu`).
  - Env vars: el codigo YA usaba `import.meta.env` (nada hardcodeado). Configuradas en Vercel (Production): `VITE_SUPABASE_URL`, `VITE_SUPABASE_KEY`. `.env` local actualizado al proyecto nuevo (gitignoreado, no commiteado). `.env.example` ya estaba correcto con placeholders. Pendiente opcional: `VITE_VAPID_PUBLIC_KEY` para web push (hoy sin configurar → push degradado a Notification API local).
  - Smoke Supabase nuevo: auth health 200; REST `devices` con anon key → 200 `[]` (RLS filtra anon, correcto).
  - **Features encontradas** (la app es admin + cliente en una, ruteo por rol en App.jsx):
    - Vista CLIENTE (rol no-admin → `Dashboard`): login Supabase, sus devices con ultima lectura (RLS), grafico historial temperatura (1h/24h/7d), alertas activas + reconocer/resolver/silenciar, config de umbrales (temp critica, delay, defrost, puerta), SensorManager (sondas), push notifications, estado realtime + "Actualizado: HH:MM". CSS mobile-first (media min-width).
    - Vista ADMIN (`AdminPanel` + `DevicesAdminTable` + `ClientManager` + `SIM800Panel`): tabla global de devices con RSSI/GSM/sondas/**bloque resiliencia** (ResilienceCell: connection_mode, free_heap — backlog #2 YA renderizado en admin), renombrar device, config hardware, WiFi remoto (scan/cambio), **OTA** (upload .bin a bucket firmware-ota + ota_updates), rele, suspender/reactivar, asignar device a cliente; ABM de clientes con pagos/abonos (registrar pago, historial, extender suscripcion); alertas globales; panel SIM800 (AT commands — OBSOLETO: decision 2026-07-11 SIM800 descartado, candidato a poda).
  - **Evaluacion interfaz usuario final**: NO falta construirla de cero — ya existe (`Dashboard`). Lo que falta: (1) crear usuarios cliente en el Supabase NUEVO y asignarles devices (ClientManager lo hace desde admin); (2) verificar que las RLS del schema nuevo (SETUP_COMPLETO.sql) filtren por owner como el viejo; (3) pulido "3 segundos": semaforo grande OK/ALERTA por heladera, "ultima lectura hace X min" relativo (hoy muestra hora absoluta), marcar dato viejo como viejo; (4) podar SIM800Panel. Smoke visual pendiente por @tester.

- 2026-07-08 [BRIEFING GIMAP] — leer ../BRIEFING_EQUIPO_GIMAP.md y los 4 docs (PARTE_GIMAP, PRESUPUESTO_ENERGIA, PROTOCOLO_CALIBRACION, INGENIERIA_NODO_1ANO). Para vos: LAB streamea 1kHz a la PC (no nube); receptor sirve dashboard local en su AP (192.168.4.1) + cloud; mostrar edad del dato, batería, RSSI, A vs B.

## 🔵 TypeScript 7.0 salió (nota 2026-07-09, para el próximo agente)
Microsoft lanzó TS 7 = rewrite nativo en Go ("tsgo"): **8-12x más rápido** (VSCode 125s→10.6s; abrir archivo con errores en editor 17.5s→1.3s), 18-26% menos memoria. Anuncio: https://devblogs.microsoft.com/typescript/announcing-typescript-7-0/
- **El ERP NO se toca** (es JSX/JavaScript puro por regla dura — TS7 no aplica).
- **SÍ sirve** para los dashboards TypeScript/Vite: `datalogger/vercel-dashboard`, `galgas/web`, `frioseguro/web-dashboard` → builds más rápidos.
- ⚠️ **Breaking changes fuertes** (`strict:true` default, adiós CommonJS, `types:[]` default) → NO instalar en proyecto que ande sin plan. Migrar gradual con el paquete `@typescript/typescript6` (side-by-side). Probar primero en proyecto nuevo/de juguete, no en producción.
- Instalación: `npm install -D typescript`. Evaluar cuando haya tiempo, no urgente.
