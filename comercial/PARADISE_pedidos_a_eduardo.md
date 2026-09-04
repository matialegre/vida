# Paradise — mensaje a Eduardo: agradecer las fotos y pedir las 3 que faltan

**Redactado 2026-09-03.** Para mandar por WhatsApp. Va en tres mensajes cortos a
propósito: un texto largo en WhatsApp se lee en diagonal, y acá se necesita que
haga tres cosas concretas.

**Contexto**: Eduardo mandó las 6 fotos del local el 2026-09-02, ya están
publicadas en https://tienda-cosmetica-vert.vercel.app. Seña del 50 % ($200.000)
cobrada el 2026-08-29. Quedan tres bloqueantes del cliente, y el alias es el que
más urge: hoy hay un placeholder `PARADISE.MP` en `src/datos.js`, así que un
cliente que quiera pagar por transferencia transfiere a la nada.

---

## Mensaje 1 — agradecimiento y novedad

> Eduardo, buenísimas las fotos, gracias! Ya están en la web 🙌
>
> Quedaron en la portada y armé una sección "Nuestro local" al final, así el que
> entra de afuera ve dónde está comprando. La del arco con las letras doradas
> quedó de portada — es la mejor de las seis.
>
> https://tienda-cosmetica-vert.vercel.app
>
> Miralo del celular que es de donde te van a entrar casi todos.

## Mensaje 2 — los tres pedidos

> Para poder terminar me faltan 3 cosas tuyas. La 1 es la urgente:
>
> **1) El alias de transferencia.** Hoy está puesto uno de prueba, así que si
> alguien quiere pagar por transferencia le aparece un alias que no existe.
> Pasame el alias o CBU real y lo cambio en el momento.
>
> **2) Los productos.** Mandámelos como los tengas — Excel, la lista del
> proveedor, lo que sea. No hace falta que armes nada especial, yo lo acomodo.
> Con las fotos que tengas de cada uno. Eso es lo que hace que la tienda pase de
> demo a real.
>
> **3) Una contraseña de aplicación de Gmail**, para que salgan solos los mails
> de confirmación cuando alguien te hace un pedido. Sin eso el pedido te entra
> igual, pero el cliente no recibe el mail. Te paso los pasos abajo, son 2
> minutos.

## Mensaje 3 — el cómo de la contraseña (donde la gente se traba)

> Para la contraseña de aplicación, entrando con la cuenta
> **paradisee.lp@gmail.com**:
>
> 1. myaccount.google.com → Seguridad
> 2. Activá "Verificación en 2 pasos" si no la tenés (te pide el celular)
> 3. Buscá "Contraseñas de aplicaciones"
> 4. Creá una que diga "Tienda" y copiame los 16 caracteres que te da
>
> Esa clave sirve **solo** para que el sistema mande los mails, no da acceso a tu
> casilla ni a nada más. Igual, si en algún momento querés cortarla, la borrás
> desde ahí mismo y listo.

---

## Por qué está redactado así (leer antes de editarlo)

- **Los productos se piden "como los tengas", a propósito.** Existe
  `scripts/plantilla_productos.csv` y el importador
  (`scripts/importar_productos.mjs`), pero mandarle la plantilla es la forma más
  rápida de que el pedido se duerma dos semanas: un comerciante no llena una
  planilla de 300 filas. Que mande el Excel del proveedor y se acomoda de este
  lado — media hora de Matías contra un mes de espera.
- **La contraseña de aplicación de Gmail asusta**, por eso va la aclaración de
  que no da acceso a la casilla. Es el pedido que más se cae por desconfianza.
- **El cambio del dorado quedó afuera a propósito.** Es una mejora de contraste
  que Eduardo no pidió y no va a notar; mencionarla abre una conversación sobre
  su identidad de marca justo cuando lo que se necesita es el alias. Si pregunta,
  se le pasa `C:\Proyectos\tienda-cosmetica\paradise_dorado_decision.png`, que
  muestra las cuatro opciones lado a lado y se entiende en dos segundos.

## Al recibir cada cosa

| Llega | Qué se hace |
|---|---|
| Alias / CBU | Reemplazar el placeholder `PARADISE.MP` en `src\datos.js` y redeploy. |
| Lista de productos + fotos | `scripts\importar_productos.mjs` (comprime las fotos a WebP). Los 16 productos actuales son seed de demo con fotos de Unsplash: se borran. |
| App password | Cargar `GMAIL_USER` / `GMAIL_PASS` en Vercel y redeploy. Va a `CREDENCIALES.local.txt` (gitignoreado), nunca al repo. |

**Y una que no depende de él**: la pantalla de "pedido confirmado" no la vio
nadie todavía — solo aparece después de un pedido real contra la base. Mirarla en
el primer pedido de verdad que entre.
