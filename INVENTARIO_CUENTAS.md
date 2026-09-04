# INVENTARIO DE CUENTAS Y SERVICIOS

> **Acá NO hay contraseñas ni tokens.** Esto dice *qué existe, dónde vive y con qué cuenta se
> entra*. Las claves están en la bóveda (§0), fuera de git.
> Última revisión: **2026-09-02**. Cuando algo cambie, se actualiza acá el mismo día.

## 0. Dónde están las claves

**Bóveda: `C:\Users\Pandemonium\Documents\CREDENCIALES\`** — carpeta local, **fuera de todo repo**,
con un archivo por servicio. Nunca se commitea, nunca se pega en un chat, nunca sale por mail.

Archivos de credenciales que ya existían repartidos (siguen donde están, se listan para no perderlos):

| Archivo | De qué |
|---|---|
| `C:\Proyectos\emsica-comercial\CREDENCIALES.md` | EMSICA: FTP, GitHub del cliente |
| `C:\Proyectos\tienda-cosmetica\CREDENCIALES.local.txt` | Paradise |
| `C:\Users\Pandemonium\Documents\BACKUP MATI ERP\codigo\CREDENCIALES.txt` | ERP |
| `.env` de cada proyecto | claves de servicio de esa app |

**Pendiente recomendado:** pasar todo a un gestor de contraseñas (Bitwarden es gratis y sincroniza
al celular). Una carpeta de texto en una sola PC se pierde con el disco.

---

## 1. Vercel — TODO en un solo equipo

Se entra con **`alegrematiasdev1@gmail.com`**. Equipo: **`gimap's projects`**
(`team_MbCChTPozBvjyfP3OhTrb20k`). No hay nada en otras cuentas.

| Proyecto | Qué es | Cliente | En vivo |
|---|---|---|---|
| `tienda-cosmetica` | tienda + POS + admin | **Paradise** (Eduardo, Macachín) | tienda-cosmetica-vert.vercel.app |
| `emsica-web` | sitio institucional | **EMSICA S.R.L.** | emsica-sitio.vercel.app |
| `kiosco-ofiuco` | punto de venta y stock | **Paco** | kiosco-ofiuco.vercel.app |
| `termovigia` | sitio comercial | propio | termovigia.vercel.app |
| `web-dashboard`, `panel-web` | dashboards de frío | propio | — |
| `vercel-dashboard` (datalogger) | dashboard GIMAP | propio | — |

CLI: `vercel whoami` · `vercel projects ls`. **No cambiar el login global**: si Termovigía necesita
cuenta propia, se usa un token de esa cuenta solo para ese proyecto.

## 2. Supabase — una cuenta

Se entra con **`alegrematiasdev1@gmail.com`**. Organización `frioseguro` (`eqceyxcowsolhzhfvbnl`).

| Ref | Nombre | Qué tiene | Estado |
|---|---|---|---|
| `vihxmqjjprtlzajlatvu` | proyecto principal | backend del reefer de Santa Cruz (Panamerican) | vivo, plan free |
| `egdlgprnanrlvmjfshrv` | `kiosco-ofiuco` | kiosco de Paco **+ el esquema `paradise` adentro** | vivo, plan free |

⚠️ **Tres refs están MUERTOS** (verificado 2026-08-19, no resuelven en DNS):
`cjdluhemschrynijzvap`, `nwugnhsktcihusopfldu`, `xhdeacnwdzvkivfjzard`. Los borró el pausado del
plan gratuito. **El plan de plataforma de Termovigía nombraba al primero: hay que corregirlo.**

**Por qué se mueren:** el plan free se pausa a los 7 días sin *actividad de base desde afuera*
(entrar al panel NO cuenta, `pg_cron` interno TAMPOCO) y a los 90 días de pausa se borra.
Mitigación montada: cron de Vercel a las 9 que escribe en `keepalive_ping` + `pg_cron` a las 12 que
avisa por Telegram si el latido tiene más de 48 h.

## 3. Neon — cuenta nueva de Termovigía

Se entra con **`termovigia@gmail.com`**. Organización `Termovigia` (`org-noisy-waterfall-08727863`).

| Proyecto | Id | Región | Plan |
|---|---|---|---|
| `Termovigia` | `rough-sunset-46764733` | `aws-sa-east-1` (São Paulo) | free: 0,5 GB, escala a cero, **no se pausa** |

CLI: `neon` v4.14 (el viejo `neonctl` choca, no instalarlo). `neon projects list --org-id …`.

## 4. Dominios

| Dominio | Dónde | Estado |
|---|---|---|
| `termovigia.com.ar` | — | **SIN REGISTRAR**. NIC.ar $8.500/año. Cuatro motivos para tomarlo: marca, URL de verificación impresa en los reportes, certificado del servidor propio, y la sesión del portal que se pierde en Safari/Firefox con dominios distintos |
| `emsica.com.ar` | GoDaddy, administrado por **Control Bay LLC** | del cliente; falta acceso al DNS |

## 5. Otros servicios en uso

| Servicio | Cuenta | Para qué |
|---|---|---|
| GitHub `matialegre` | — | repos `vida` (MATI-HQ) y `frioseguro` |
| Telegram (bot) | — | alertas de los equipos de frío |
| Microsoft 365 | de EMSICA | correo del dominio del cliente |
| Brevo | dueño **a confirmar con EMSICA** | campañas de mail; DKIM sin activar |
| WhatsApp Business | +54 9 2920 591019 | línea comercial de Termovigía, publicada en el sitio |
| OpenClaw (:3456) | máquina del ERP | envío de WhatsApp propio |

## 6. Reglas que evitan el próximo susto

1. **Ninguna clave entra a un repo.** El `.gitignore` de MATI-HQ ya bloquea `.env`, `*.token`,
   `*.pem`, `*.key`, `credentials.json`. Antes de commitear algo nuevo, mirar qué se está agregando.
2. **Un servicio nuevo = una fila acá el mismo día**, aunque sea de prueba.
3. **No cambiar el login global de un CLI** para usar otra cuenta: se usa un token por proyecto.
4. **Las claves que se sospechan filtradas se rotan, no se discuten.** Pendiente de rotación desde
   julio: bot de Telegram, claves de Supabase del firmware, y las que están en `config.h`.

   ⚠️ **ROTACIÓN OBLIGATORIA (detectado 2026-09-04 por @verificador, sacado del árbol pero
   sigue en el historial de git del repo `frioseguro`):**
   - Token de Management API de Supabase (`sbp_355f…2e47`) — control total de la cuenta principal.
   - JWT `service_role` del proyecto `nwugnhsktcihusopfldu` (proyecto ya muerto: verificar que no
     exista; si existe, rotar).
   - Bot de Telegram `8175168657:AA…` — estaba en `config.h`, `config_SANTA_CRUZ.h` y `DISPOSITIVOS.md`.
   Cómo: Supabase → Account → Access Tokens → revocar y generar nuevo · BotFather → `/revoke`.
   Hacerlo **el mismo día que se flashee el primer equipo con v3.1** (que ya lee las claves de
   `secrets.h`, fuera de git), para tocar cada placa una sola vez.
5. Si un proyecto free deja de recibir tráfico, **se muere solo**. Todo lo que importe necesita
   latido y vigía externo.
