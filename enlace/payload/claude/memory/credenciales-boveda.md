---
name: credenciales-boveda
description: Dónde viven las claves de Matías y el índice de qué cuenta tiene qué proyecto — la bóveda local y el inventario en git
metadata: 
  node_type: memory
  type: project
  originSessionId: 72c41d2f-de68-4f4d-8ae8-1fc3ec89613e
  modified: 2026-09-02T20:28:43.642Z
---

Matías no recuerda en qué cuenta está cada cosa (lo dijo textual el 2026-09-02: *"ya me había olvidado"*), y tiene sitios de **tres clientes** en producción. La solución montada ese día son **dos lugares separados**:

1. **Bóveda: `C:\Users\Pandemonium\Documents\CREDENCIALES\`** — fuera de todo repo, un `.md` por servicio (`vercel`, `supabase`, `neon`, `github`, `telegram-bot`, `whatsapp`, `dominios`, `google-cuentas`) con la clave real, la fecha de creación y cuándo rotarla. Nunca se commitea ni se pega en un chat.
2. **Índice sin claves: `MATI-HQ\INVENTARIO_CUENTAS.md`** (en git) — qué existe, dónde vive y **con qué cuenta se entra**. Regla escrita ahí: servicio nuevo = fila nueva el mismo día.

**Lo que hay que saber sin abrir nada:** todos los proyectos de Vercel en producción (Paradise, EMSICA, kiosco Ofiuco, termovigia, los dashboards) están en **un solo equipo**, `gimap's projects`, cuenta `alegrematiasdev1@gmail.com`. No hay nada perdido en cuentas olvidadas.

**Desde el 2026-09-02 hay cuentas nuevas de Termovigía** (`termovigia@gmail.com`): Vercel `termovigia-2686` (vacía), Supabase org `iazxogjshyftwwkftdot` con el proyecto `ccyrncqyvabzcjobggfm`, y Neon `Termovigia` (`rough-sunset-46764733`, São Paulo). Detalle en [[supabase-cuentas-proyectos]].

**Regla que evita el próximo susto:** no cambiar el login global de un CLI para usar otra cuenta — se usa un token por proyecto (`vercel --token`, `$env:SUPABASE_ACCESS_TOKEN`). Cambiar el login deja sin acceso a los sitios de los clientes.

**Pendiente:** pasar la bóveda a Bitwarden. Una carpeta de texto en una sola PC se pierde con el disco, y con ella el acceso a las páginas de tres clientes.
