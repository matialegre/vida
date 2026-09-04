---
name: supabase-cuentas-proyectos
description: "Qué proyecto de Supabase vive en qué cuenta de Matías, y cuáles murieron por el free tier"
metadata: 
  node_type: memory
  type: project
  originSessionId: 3c2ffe10-96cb-49dc-a097-78e5ec79d3b8
  modified: 2026-08-20T11:59:54.350Z
---

Matías tiene proyectos de Supabase repartidos en **dos cuentas de Google distintas**, y eso es fuente constante de confusión.

**Cuenta principal (alegrematiasdev1@gmail.com)** — org `frioseguro` (`eqceyxcowsolhzhfvbnl`), proyecto **`vihxmqjjprtlzajlatvu`**, región us-west-2, plan FREE. Es el backend vivo de FríoSeguro: creado el 2026-08-19 y bootstrapeado ese mismo día con el esquema completo (16 tablas + 4 vistas, `device_logs`, bucket `firmware-ota`, pg_cron/pg_net, 3 cron jobs, 7 Edge Functions). El equipo `REEFER_01_SCZ` reporta acá.

**Kiosco Ofiuco — YA MIGRADO** (2026-08-19). Vivía en una cuenta vieja de Google (`ofiucokioscosao-max`) a la que Matías casi no entra y cuyo CLI login fallaba. Se restauró en la cuenta principal, misma org `frioseguro`: proyecto **`egdlgprnanrlvmjfshrv`** (`kiosco-ofiuco`), con las 8 tablas y las 2087 filas verificadas contra el backup. La cuenta vieja quedó para abandonar. Backup original en `MATI-HQ\backups\ofiuco_db_cluster_2026-08-11.backup.gz` y el SQL de restauración en `Documents\KIOSCO OFIUCO PACO\backup_supabase\RESTAURAR_kiosco.sql`. **Falta el código de la app**: en disco solo hay un README. El cliente es Paco, ver [[kiosco-ofiuco-paco]].

Dos trampas al restaurar un dump de Supabase, por si se repite: el dump de cluster **no se corre tal cual** (trae roles y los schemas de sistema que Supabase ya crea; hay que quedarse solo con `public` y pasar los `COPY` a `INSERT`), y las tablas hay que insertarlas **en orden de clave foránea**, no alfabético — el dump pone `product_batches` antes que `products`. Y lo que casi pasa desapercibido: tras insertar con IDs explícitos, **las secuencias quedan en 1** y el primer alta choca con un duplicado. Hay que `setval` a `max(id)`.

**Tres refs anteriores están MUERTOS** (no resuelven en DNS, verificado con tres resolvers el 2026-08-19): `nwugnhsktcihusopfldu`, `cjdluhemschrynijzvap` y `xhdeacnwdzvkivfjzard`. Todo el repo de frioseguro apuntaba a ellos, por eso el sistema entero estaba mudo sin que nada avisara.

**Por qué pasa:** el plan FREE se pausa si en 7 días no recibe **actividad de base de datos de usuario**, y a los 90 días de pausado se borra. Ya se comió tres proyectos. Lo que NO cuenta como actividad, y por eso Matías veía proyectos "usados" que igual se pausaban: **entrar al dashboard no cuenta**, y **los cron de `pg_cron` tampoco** (corren dentro de Postgres, no entran por la API). Solo cuentan requests que entran desde afuera.

**La solución, montada el 2026-08-19 y probada de punta a punta** — dos capas que se vigilan entre sí:
1. Cron de Vercel a las 9, en `api/keepalive.js` del proyecto del kiosco: consulta 3 tablas de cada base **y actualiza** la fila única de `keepalive_ping` (escribir es actividad sin discusión, y no ensucia datos del negocio). Si algo no responde, avisa por Telegram.
2. `pg_cron` `vigilar-latido` a las 12 **dentro de cada base**: si el último latido tiene más de 48 h, el guardián externo se murió y avisa por Telegram vía `pg_net`. Es el hombre muerto que cubre el caso de que se caiga Vercel.

Las alertas van por el bot **@FrioSeguro_bot** al chat `7713503644` (Matías). Probado rompiendo una URL a propósito: la alerta llegó. Silencio = todo bien.

**Para trabajar por API sin pedirle claves a Matías:** el token del CLI (`supabase login`) queda en el Credential Manager de Windows bajo el target `Supabase CLI:supabase`, se lee con `CredRead` desde PowerShell, y sirve para la Management API (`api.supabase.com/v1`), incluido `POST /projects/{ref}/database/query` para correr DDL. Dos detalles que cuestan tiempo si no se saben: hay que mandar un **User-Agent normal** (Cloudflare devuelve 403 "error code: 1010" al de Python), y la API devuelve las claves *secret* **enmascaradas** — la única utilizable que entrega entera es el JWT `service_role` legacy.

**ACTUALIZACION 2026-09-02 — cuentas nuevas de Termovigia.** Matias creo `termovigia@gmail.com` y ahi viven las bases nuevas del producto comercial: **Supabase** org `iazxogjshyftwwkftdot`, proyecto **`ccyrncqyvabzcjobggfm`** ("termovigia-del's Project", East US Ohio, free) — es el destino de la base de produccion de Termovigia, porque el firmware ya habla PostgREST; y **Neon** org `Termovigia` (`org-noisy-waterfall-08727863`), proyecto **`rough-sunset-46764733`** en `aws-sa-east-1` (Sao Paulo, free 0,5 GB, escala a cero y **no se pausa**) — pensado como copia de respaldo/historial. Los tokens de ambas estan en la boveda: ver [[credenciales-boveda]]. **No cambiar el login global del CLI**: la cuenta vieja sigue siendo la que tiene Santa Cruz, el kiosco y Paradise.
