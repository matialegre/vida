# -*- coding: utf-8 -*-
"""Arma el documento INTERNO de Cerro Moro (v9.0, 8-sep-2026).

v9.0: la configuracion la cambio Andres el 8-sep por WhatsApp: "con tres modulos
solucionamos lo de Cerro Moro, un modulo para dos reefer; al estar juntos de a dos es
facil hacer la conexion; pongo la caja sobre la union de los dos y saco las sondas".
Matias acepto, mantiene 3 sondas por reefer ("3 es mucho mejor para calibracion";
Andres midio casi 3 grados entre la puerta y el fondo de un reefer) y le dijo: "rehago
el presupuesto, queda mas o menos lo mismo, porque le tengo que meter un poco mas de
electronica adentro de la caja y programacion".

3 MODULOS DOBLES (1 exterior estanco + 2 interior), 6 sondas / 2 puertas / 2 defrost /
2 reles cada uno, UN cable de 3 hilos por reefer; repuesto = 1 doble completo.

PRECIOS v9.0 (cuenta completa en el docstring de armar_cliente_v7.py, unica fuente):
  doble interior 900 x 2 = 1.800 (costo 612, 32,0 %) - doble exterior 950 (costo 629,
  33,8 %) - repuesto 400 (costo 279, 30,2 %) - puesta en marcha 1.650 (66 h)
  -> inicial 4.800 (v8.0: 5.000; -4 %). Abono 500/mes. B = 10.200. Anticipo 2.400.
  Sexto reefer: sin costo de equipo, solo +100/mes.

Copy: PROPUESTA_PANAMERICAN_CERRO_MORO.md v9.0, PARTES 2 a 7 + anexos. Nada inventado:
lo unico propio son rotulos de seccion y de columna.

REGLA DE MATIAS (4-sep, sigue): NO hay ninguna logistica antes de que acepten el
presupuesto. Todo el cronograma esta en semanas DESDE la aceptacion.

Salida: PRESUPUESTO_CERRO_MORO_INTERNO.html  (marcadores <!--LOGO_HORIZONTAL--> y
<!--ESCUDO--> que inlina render_v7.py)
"""
import io, os
import armar_cliente_v7 as CLI

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = "PRESUPUESTO_CERRO_MORO_INTERNO.html"
FECHA = CLI.FECHA
REF = CLI.D["ref"]
P = CLI.PRECIOS
C = CLI.C
m = CLI.miles

PIE = ('<div class="aire"></div>\n'
       '<div class="pie">\n'
       '  <span class="marca"><!--ESCUDO--> <b>Termovig&iacute;a</b> &middot; Bah&iacute;a Blanca</span>\n'
       '  <span class="cod">INTERNO &middot; ' + REF + ' &middot; no enviar</span>\n'
       '  <span class="npag">&middot;</span>\n'
       '</div>\n</section>\n')

BANDA = ('<div class="agua">INTERNO — NO ENVIAR</div>\n'
         '<div class="banda">Interno — no enviar</div>\n')

HOJAS = []


def hoja(html, banda_larga=None):
    b = BANDA
    if banda_larga:
        b = ('<div class="agua">INTERNO — NO ENVIAR</div>\n'
             '<div class="banda">Interno — no enviar\n  <span class="men">%s</span>\n</div>\n' % banda_larga)
    HOJAS.append('<section class="hoja">\n' + b + html + PIE)


# =================================================================== HOJA 1
hoja(u'''
<div class="cabecera">
  <div class="logo"><!--LOGO_HORIZONTAL--></div>
  <div class="sello">
    <b>Interno · v9.0</b>
    ''' + FECHA + u'''<br>
    Ref. ''' + REF + u'''
  </div>
</div>

<div class="hero">
  <div class="kicker">Cerro Moro (Santa Cruz) · 6 reefers, 5 en servicio</div>
  <h1>Tres módulos dobles: uno por cada par<br>de reefers, con la caja sobre la unión</h1>
  <div class="bajada">Andrés cambió la configuración el 8-sep por WhatsApp: <em>«con tres módulos solucionamos lo de
  Cerro Moro, un módulo para dos reefer; al estar juntos de a dos es fácil hacer la conexión; pongo la caja sobre la
  unión de los dos y saco las sondas»</em>. Matías aceptó, <strong>mantiene 3 sondas por reefer</strong> (<em>«3 es
  mucho mejor para calibración»</em> — y Andrés midió <strong>casi 3 °C entre la puerta y el fondo</strong> de un
  reefer) y le dijo: <em>«rehago el presupuesto, queda más o menos lo mismo, porque le tengo que meter un poco más de
  electrónica adentro de la caja y programación»</em>. <strong>Queda en USD ''' + m(C["total"]) + u'''</strong>
  (la v8.0 decía 5.000).</div>
  <div class="meta">
    Copy del cliente: <b>PARTE 1</b> de <b>PROPUESTA_PANAMERICAN_CERRO_MORO.md</b> (v9.0, @comercial).
    Siguen las decisiones de Matías: <b>ni cable ni tendido se cotizan</b>, sin spec de cable en el PDF, <b>abono
    500/mes sin escalón</b>, sin material del gabinete. Lo de acá abajo <b>no se manda</b>; <b>el número final lo
    decide Matías</b>.
  </div>
</div>

<div class="sep-ch"></div>

<h2><span class="n">00</span>Dónde está cada cosa</h2>
<div class="grid3">
  <div class="card fuerte">
    <div class="cab"><span class="tag">Para copiar y mandar</span><h3>Hoja 2 — WhatsApp para Andrés</h3></div>
    <div class="cuerpo">
      <p>Acompaña al PDF nuevo. Arranca con <em>«rehecho como lo armaste vos»</em>, dice el número una sola vez con
      el motivo pegado (menos cajas, más electrónica y programación por caja), usa los 3 °C que midió él para
      sostener las 3 sondas, y cierra con <em>«este reemplaza al anterior»</em> <strong>sin citar la cifra
      vieja</strong>. <strong>No se manda sin el PDF al lado.</strong></p>
    </div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">Lo que hay que poder defender</span><h3>Hoja 9 — Los tres precios</h3></div>
    <div class="cuerpo">
      <p>Costo → margen → precio de cada ítem, con el mismo ~32 % de la v8.0. <strong>Por qué un doble vale 900 y
      no 1.200</strong>, y por qué el total <strong>baja 200 y no 1.000</strong> aunque haya dos cajas menos.</p>
    </div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">Antes de mandar nada</span><h3>Última hoja — Lo que quedó abierto</h3></div>
    <div class="cuerpo">
      <p>Lo que decide Matías y lo que tiene que confirmar cada dominio. <strong>Ninguno es logística:</strong>
      hasta que no haya aceptación y anticipo no se compra, no se arma y no se despacha nada.</p>
    </div>
  </div>
</div>

<div class="sep"></div>

<div class="grid3">
  <div class="cifra"><div class="big">''' + m(C["total"]) + u'''</div><div class="lb">USD inicial<br>''' + m(P["doble_ext"]) + u''' + 2×''' + m(P["doble_int"]) + u''' + repuesto ''' + m(P["repuesto"]) + u''' + puesta en marcha ''' + m(P["puesta"]) + u'''</div></div>
  <div class="cifra"><div class="big">''' + m(C["abono"]) + u'''</div><div class="lb">USD por mes<br>USD 100 por reefer × 5, sin escalón</div></div>
  <div class="cifra"><div class="big">3</div><div class="lb">módulos dobles para 6 reefers<br>1 estanco de exterior + 2 de interior, uno por par</div></div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>Lo que no se movió:</strong> pago 50/50, formas A y B, los 5 hitos con sus plazos
relativos, sin validez y sin destinatario, <strong>abono 500/mes sin escalón</strong>, <strong>3 sondas + puerta +
defrost por reefer</strong>. <strong>Sigue eliminada la opción C</strong> («sin inversión inicial»): <em>«el de la
inversión inicial no lo ofrecería»</em>.</p></div>
''', banda_larga=u'Este documento es de Matías. Al cliente va un solo PDF: PRESUPUESTO_CERRO_MORO, de 2 páginas.')

# =================================================================== HOJA 2
hoja(u'''
<h2><span class="n">01</span>Qué cambió en esta versión</h2>
<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Cambio 1</span><h3>Tres módulos dobles, uno por par. Lo armó Andrés</h3></div>
    <div class="cuerpo">
      <p>Los 6 reefers están <strong>de a dos</strong>: 2 afuera y 4 adentro en dos pares. Andrés pone <strong>la
      caja sobre la unión de cada par</strong> y saca las sondas desde ahí. <strong>1 doble de exterior estanco + 2
      dobles de interior</strong>, cada uno con 6 sondas, 2 puertas, 2 defrost y 2 relés. A cada reefer le llega
      <strong>un solo cable de 3 hilos</strong> y las 3 sondas se reparten adentro (puerta, medio, fondo): no hay
      que pasar 9 hilos.</p>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Cambio 2</span><h3>El sexto reefer entra sin costo de equipo</h3></div>
    <div class="cuerpo">
      <p>El reefer fuera de servicio comparte módulo con su vecino, y <strong>el doble ya trae sus 3 sondas, su reed
      y su entrada de defrost</strong>. Antes entraba por USD 260; ahora <strong>no hay nada que comprar</strong>:
      se conecta y el abono pasa de 500 a 600/mes. Se dice como ventaja en el PDF: es el upsell más probable y
      ahora cuesta cero venderlo.</p>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Cambio 3</span><h3>USD ''' + m(C["total"]) + u''', con el mismo margen parejo (~32 %)</h3></div>
    <div class="cuerpo">
      <p>Matías le dijo a Andrés «queda más o menos lo mismo», y la cuenta lo sostiene sola: dos cajas menos, pero
      cada doble lleva <strong>más electrónica</strong> (segundo bus 1-Wire con su protección, segunda entrada de
      defrost, borneras y prensacables ×2), <strong>la plataforma se reparte entre 3 módulos y no 5</strong> (333
      c/u en vez de 200) y la puesta en marcha suma <strong>8 h de software</strong> para repartir por reefer.
      Resultado: interior <strong>900</strong>, exterior <strong>950</strong>, repuesto <strong>400</strong>, puesta en
      marcha <strong>1.650</strong> → <strong>''' + m(C["total"]) + u'''</strong>. <strong>−200 sobre la v8.0 (−4 %)</strong>: eso es
      «más o menos lo mismo», y se dice así.</p>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Cambio 4</span><h3>⚠ El riesgo volvió: el firmware doble es crítico en los tres</h3></div>
    <div class="cuerpo">
      <p>En la v8.0 los 4 simples corrían lo que ya anda. <strong>Ahora los tres módulos son dobles</strong>, así que
      sin el firmware doble (2.ª puerta, 2.º defrost con silenciado por reefer, <code>SONDAS_MAX</code> a 8, reparto
      de sondas por reefer) <strong>no reporta ningún módulo nuevo</strong>. Estado: APTO CON CORRECCIONES
      (auditoría 4-sep). Y <strong>un módulo caído deja dos reefers ciegos</strong>, siempre: para eso el repuesto.
      A cambio: <strong>3 puntos de red</strong> en vez de 5, y <strong>ningún cable entre contenedores</strong>
      — sólo 6 tiradas cortas de la unión a cada reefer.</p>
    </div>
  </div>
</div>

<div class="sep"></div>

<h2><span class="n">02</span>WhatsApp para Andrés — copiar desde acá</h2>
<div class="sub" style="margin:-1.5mm 0 4mm">Lo manda Matías, <strong>junto con el PDF nuevo</strong>. Andrés ya tiene
en el celular un presupuesto anterior (el de 4.600 del 4-sep seguro; el de 5.000 si se mandó): el mensaje lo
reemplaza <strong>sin citar la cifra vieja</strong>, así cubre los dos casos.</div>

<div class="wsp-tit">MENSAJE COMPLETO — §6.1</div>
<div class="wsp">Andrés, ahí va el presupuesto rehecho como lo armaste vos: tres
módulos, uno por cada par de reefers, con la caja sobre la unión de los
dos y un solo cable de 3 hilos a cada reefer. Queda en USD ''' + m(C["total"]) + u''': son
menos cajas, pero cada una lleva más electrónica adentro y más
programación para repartir por reefer, así que queda más o menos lo
mismo, como te dije. El abono es el mismo, USD 100 por reefer por mes
= 500 por los cinco que andan.

Mantengo las 3 sondas por reefer: con los casi 3 grados que mediste
entre la puerta y el fondo, con una sola sonda no sabés qué temperatura
tiene la carga. Van puerta, medio y fondo por el mismo cable, y se
calibran las tres juntas.

El de afuera va en caja estanca para intemperie. Los módulos los pruebo
acá en el banco con 25 metros de cable antes de despacharlos.

El reefer que está parado ya queda cubierto por el módulo de su
vecino, con sus sondas incluidas: el día que vuelva se conectan y
listo, sin comprar nada.

Mismas dos hojas, sin nombre de empresa. Este reemplaza al anterior.
</div>
''')

# =================================================================== HOJA 3
hoja(u'''
<h2><span class="n">03</span>Por qué el mensaje está escrito así, para que no se suavice al copiarlo</h2>
<table class="compacta"><thead><tr><th style="width:6%">&nbsp;</th><th style="width:30%">Qué hace</th><th>Por qué</th></tr></thead><tbody>
<tr><td class="num">a</td><td><strong>Arranca con «rehecho como lo armaste vos»</strong></td>
<td>La configuración es de él. Lo primero que lee es que se hizo exactamente eso, con la caja sobre la unión y un
cable por reefer, sus dos frases.</td></tr>
<tr><td class="num">b</td><td><strong>El número va una sola vez, con el motivo pegado en la misma oración</strong></td>
<td>«Menos cajas, pero cada una lleva más electrónica y más programación» es lo que Matías ya le dijo por chat.
El mensaje lo repite tal cual, y cierra con «como te dije»: coherencia entre lo hablado y lo escrito.</td></tr>
<tr><td class="num">c</td><td><strong>No cita la cifra vieja</strong></td>
<td>No sabemos con certeza si Andrés tiene el PDF de 4.600 o el de 5.000. «Este reemplaza al anterior» sirve para
los dos, y no pone un número más chico o más grande a competir con el nuevo.</td></tr>
<tr><td class="num">d</td><td><strong>Que el abono NO cambia se dice en la misma frase que el total</strong></td>
<td>Ahí se corta «¿y el mensual?» antes de que exista. Y con menos cajas y el mismo abono, la regla «se cobra por
reefer vigilado, no por caja» queda demostrada por segunda vez.</td></tr>
<tr><td class="num">e</td><td><strong>Las 3 sondas se defienden con SU dato</strong> (casi 3 °C puerta-fondo)</td>
<td>Es el mejor argumento que tenemos y lo midió él. No se discute con teoría: se le devuelve su medición y se le
dice qué haría una sola sonda con ese gradiente (mentir).</td></tr>
<tr><td class="num">f</td><td><strong>«Por el mismo cable»</strong></td>
<td>Se anticipa la objeción de los 9 hilos: un cable de 3 hilos por reefer, las tres sondas se reparten adentro.</td></tr>
<tr><td class="num">g</td><td><strong>La prueba con 25 m compra confianza técnica</strong></td>
<td>Dice, sin decirlo: sé que hay distancia y me hago cargo. Y 25 m es más que cualquier tirada de esta
configuración.</td></tr>
<tr><td class="num">h</td><td><strong>El sexto reefer aparece como previsión, y ahora gratis</strong></td>
<td>«Ya queda cubierto por el módulo de su vecino, con sus sondas incluidas». Es lo que él gana adentro para
defender la compra: el día que vuelva no hay que pedir nada.</td></tr>
<tr><td class="num">i</td><td><strong>No le pide nada. No menciona material de caja ni riesgo.</strong></td>
<td>Andrés trabaja por turnos de 15 días y no es él quien aprueba. Lo del material y el riesgo del bus es decisión
de Matías: ni acá ni en el PDF.</td></tr>
<tr><td class="num">j</td><td><strong>No se manda hasta que el PDF esté al lado</strong></td>
<td>Los dos juntos, o el mensaje pierde la mitad.</td></tr>
</tbody></table>

<div class="sep"></div>

<h2><span class="n">04</span>Guion de 5 líneas para que la presente él</h2>
<ul class="lista">
  <li><strong>Arrancá por el problema, no por el producto:</strong> «un reefer que se corta un fin de semana es la
  comida de todo el campamento, y hoy nadie se entera hasta que abren la puerta.»</li>
  <li><strong>Mostrá lo que ya anda:</strong> abrí el panel en el celular y mostrá la temperatura de ahora del
  equipo instalado — sigue reportando mientras la propuesta se evalúa. Si podés, sacá una sonda al aire un minuto y
  que vean subir la curva. Eso convence más que el PDF.</li>
  <li><strong>Decilo en una frase:</strong> «tres equipos, uno por cada par de reefers, con la caja sobre la unión.
  Tres sondas adentro de cada reefer —medí casi 3 grados entre la puerta y el fondo—, te avisa al celular si se
  sale de rango o si queda la puerta abierta, y arma el registro mensual solo.»</li>
  <li><strong>Si preguntan por el cable:</strong> «un solo cable de tres hilos de la caja a cada reefer, corto,
  porque la caja va entre los dos. No hay que cruzar nada de un contenedor a otro.»</li>
  <li><strong>Lo que NO prometés:</strong> que garantiza la mercadería (avisa, no garantiza) · que avisa el corte de
  luz (avisa que el equipo dejó de reportar) · que la sirena está incluida (van las salidas, la sirena se conecta) ·
  que está terminado (hay una puesta en marcha por hitos, y está en el precio) · fechas o precios distintos a los
  del PDF. Cualquier pregunta técnica o de números: «eso lo contesta Matías, lo llamamos ahora.»</li>
</ul>
''')

# =================================================================== HOJA 4
hoja(u'''
<h2><span class="n">05</span>Qué hay hoy, verificado</h2>
<table class="compacta"><thead><tr><th>Hecho</th><th style="width:38%">Evidencia</th></tr></thead><tbody>
<tr><td>1 equipo instalado en el campamento, <code>REEFER_01_SCZ</code>, firmware <code>firmware_revival</code> 2.6.21</td><td>Puesto el 21-ago; reconectado por Andrés el 3-sep</td></tr>
<tr><td>Reportando cada ~5 s, <strong>con 1 sola sonda y FUERA del reefer</strong> — mide ambiente</td><td>Base de Santa Cruz, 3-sep; Andrés espera confirmación para meterlas</td></tr>
<tr><td><strong>Sin contrato y sin un peso cobrado</strong></td><td><code>PLATA.md</code></td></tr>
<tr><td>«Acá no pueden haber cables aéreos»</td><td>Andrés, WhatsApp 3-sep 17:11</td></tr>
<tr><td><strong>2 reefers a la intemperie y JUNTOS; 4 adentro, bajo techo, también de a dos</strong></td><td>Andrés, 4-sep y <strong>8-sep</strong></td></tr>
<tr><td><strong>De los 4 de adentro, uno está fuera de servicio: hoy hay 5 reefers activos</strong></td><td>Matías, 4-sep</td></tr>
<tr><td>Ya se mandó al sitio una <strong>caja estanca IP65 apta para exterior</strong></td><td>Matías, 4-sep</td></tr>
<tr><td><strong>CONFIGURACIÓN v9 — Andrés: «con tres módulos solucionamos lo de Cerro Moro, un módulo para dos reefer; al estar juntos de a dos es fácil hacer la conexión; pongo la caja sobre la unión de los dos y saco las sondas»</strong></td><td>WhatsApp, <strong>8-sep</strong>. Es el dato que fija esta versión</td></tr>
<tr><td><strong>Andrés midió casi 3 °C de diferencia entre la puerta y el fondo de un reefer</strong></td><td>WhatsApp, 8-sep. <strong>Argumento de las 3 sondas, con dato del sitio</strong></td></tr>
<tr><td><strong>Matías: 3 sondas por reefer se mantienen («3 es mucho mejor para calibración»); «rehago el presupuesto, queda más o menos lo mismo»</strong></td><td>WhatsApp, 8-sep. Fija el precio objetivo de esta versión</td></tr>
<tr><td><strong>La placa Mini tiene UN bus 1-Wire (GPIO4, hasta 6 sondas) y deja GPIO 18/23 reservados para un 2.º bus</strong></td><td><code>PINOUT_MINI.md</code> filas 4 y «libres». Es la «más electrónica» de esta versión</td></tr>
<tr><td><strong>Firmware de módulo doble: escrito y en auditoría, veredicto APTO CON CORRECCIONES</strong></td><td><code>frioseguro-v31/firmware_modular/VERIFICACION_V3.1_2026-09-04.md</code> — correcciones en curso</td></tr>
</tbody></table>

<div class="sep"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">De Andrés</span><h3>Lo que sigue abierto — ninguna frena el envío</h3></div>
    <div class="cuerpo">
      <ul>
        <li><strong>¿Cuál de los 4 de adentro es el que está fuera de servicio?</strong> Ahora <strong>sí</strong>
        cambia algo: define qué par tiene un solo reefer activo hoy, y por lo tanto qué módulo arranca con 3
        sondas conectadas y 3 en espera.</li>
        <li><strong>¿Cuántos metros hay de la unión de cada par a la sonda más lejana de cada reefer?</strong> Con
        la caja sobre la unión deberían ser pocos; conviene el número antes de cortar cable de prueba.</li>
        <li><strong>¿La red del campamento llega bien a los 3 puntos donde van las cajas?</strong> Son 3, no 5:
        mejoró. Si alguno queda corto, repetidor <strong>antes</strong> de despachar.</li>
        <li><strong>¿Los reefers tienen una señal o contacto de defrost accesible?</strong> Si alguno no lo tiene,
        esa entrada queda libre y el resto funciona igual — ya está dicho así en el documento del cliente.
        @hardware pide además saber si es <strong>12-24 V o contacto seco</strong> (dos puentes de soldadura en la
        placa, se define <strong>antes de rutear</strong>).</li>
        <li><strong>¿Cómo midió los 3 °C?</strong> Pedirle el dato o la foto: sirve para fijar rangos por reefer y
        es evidencia del argumento de las 3 sondas.</li>
        <li><strong>¿Para quién trabaja Andrés?</strong> (empleado de PAAS o de una contratista). No es técnica:
        decide la hoja 16.</li>
      </ul>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">De la empresa, cuando tenga nombre</span><h3>Lo administrativo</h3></div>
    <div class="cuerpo">
      <p>Quién firma, cómo factura (monotributo/RI, plazo), si acepta la cláusula de moneda, <strong>cuál de las dos
      formas de pago elige (A o B)</strong>, y confirmación de que el montaje <strong>y el tendido de los 6 cables
      cortos de cada reefer a su caja</strong> los hace personal del campamento (sin personal nuestro en sitio no
      corresponde ART ni legajo de contratista).</p>
      <p><strong>El comprador no es Pan American Silver:</strong> es «una empresa» que Andrés todavía no identifica.
      Por eso el documento del cliente va sin destinatario, sin logo ajeno y sin nombrar a la minera.</p>
    </div>
  </div>
</div>
''')

# =================================================================== HOJA 5
hoja(u'''
<h2><span class="n">06</span>Qué módulo va en cada reefer — la configuración que armó el sitio</h2>
<div class="sub">Las v4 y v5 discutieron si convenía un equipo por reefer o uno cada dos; la v7.0 se fue al «uno cada
dos»; la v8.0 volvió a «uno por reefer adentro». <strong>El 8-sep Andrés la cerró desde el sitio, con la caja en la
mano: los seis están de a dos, y la caja va sobre la unión de cada par.</strong></div>

<table class="compacta"><thead><tr><th>Ubicación</th><th class="num" style="width:9%">Reefers</th><th style="width:16%">Módulos</th>
<th style="width:30%">Gabinete</th><th>Por módulo</th></tr></thead><tbody>
<tr><td><strong>Intemperie</strong> (los 2 están juntos)</td><td class="num">2</td><td><strong>1 doble</strong></td>
<td><strong>IP65 estanco de exterior</strong> (Roker PRG357, $ 44.419) — ya hay una en el sitio</td>
<td>6 sondas, 2 puertas, 2 defrost, 2 relés · un cable de 3 hilos a cada reefer</td></tr>
<tr><td><strong>Bajo techo, de a dos</strong> (uno de los 4 fuera de servicio)</td><td class="num">4</td><td><strong>2 dobles</strong>, uno por par</td>
<td>interior (Genrod IP65 210×310×110, $ 21.203)</td>
<td>ídem · el par con el reefer parado arranca con 3 sondas conectadas y 3 en espera</td></tr>
<tr><td>Repuesto en el campamento</td><td class="num">—</td><td><strong>1 doble</strong></td><td>interior</td>
<td>completo, con 6 sondas y 2 reed: reemplaza a cualquiera de los 3</td></tr>
<tr class="total"><td><strong>Total</strong></td><td class="num"><strong>6</strong></td><td><strong>3 instalados + 1 repuesto</strong></td><td colspan="2">4 placas Mini idénticas, las 4 con el 2.º bus poblado</td></tr>
</tbody></table>

<div class="cita"><p><strong>La regla que quedó, en una frase:</strong> <em>un módulo por cada par de reefers pegados,
montado sobre la unión, con un cable de 3 hilos a cada reefer.</em> Es la que dijo el sitio, con la caja en la mano,
no la que dedujimos nosotros. Y es la que <strong>menos cable</strong> tiene de todas las versiones: cero entre
contenedores, seis tiradas cortas de la unión a cada reefer.</p></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Qué se gana</span><h3>Tres cajas, tres puntos de red, nada entre contenedores</h3></div>
    <div class="cuerpo"><p><strong>3 puntos de red</strong> en vez de 5. <strong>Ningún cable entre
    contenedores</strong>: la caja está sobre la unión y cada reefer recibe el suyo, corto. <strong>Dos cajas
    menos</strong> que comprar, armar, probar y despachar (4 bultos). <strong>Un solo diseño</strong> para los cuatro:
    un firmware, un stock, un runbook. <strong>El sexto reefer entra gratis.</strong> Y las 3 sondas ahora tienen
    <strong>dato del sitio</strong>: casi 3 °C entre puerta y fondo.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Qué se pierde, y hay que tenerlo escrito</span><h3>El firmware doble vuelve a ser crítico, y una caja caída ciega dos</h3></div>
    <div class="cuerpo"><p><strong>Acá no hay simples:</strong> sin el firmware doble no reporta ningún módulo
    nuevo (hoja 6). <strong>Un módulo sin energía deja dos reefers sin vigilancia, siempre</strong> — mitigación
    cotizada: el repuesto en el campamento y el aviso de equipo mudo. La plataforma se reparte entre 3 (USD 333
    c/u en vez de 200): es la mitad de por qué un doble cuesta 900 y no 700. Y hay una <strong>decisión de placa
    antes de pedir la PCB</strong>: poblar el 2.º bus (hoja 6).</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="nota"><p><strong>El riesgo del bus, ahora repartido en seis tiradas cortas.</strong>
<span class="neutro">El límite prudente que fijó @muestreador para este bus es <strong>15 m</strong>
(<code>ALCANCE_1WIRE.md</code>); con la caja sobre la unión, cada tirada es <strong>del gabinete a la sonda más
lejana de un reefer</strong>: unos metros. Lo que sí queda, y hay que decirlo: <strong>cada módulo ata por el hilo
de masa dos contenedores metálicos con puesta a tierra separada</strong> (§2.6 de ALCANCE: «el riesgo dominante de
esta instalación»). Con <strong>un bus por reefer</strong> (2.º bus en GPIO 18, pines ya reservados en la Mini) los dos
reefers no comparten hilo de datos, el defrost de uno no puede callar al otro por diseño y una sonda en corto en un
reefer no tumba las del vecino. <strong>Matías conoce el dato y acepta el riesgo.</strong></span></p></div>

<ul class="lista">
  <li><strong>Un bus 1-Wire por reefer</strong>: poblar el 2.º bus de la Mini (R pull-up 2k2 con alternativa 1k, 100 Ω
  serie, clamps; <strong>sin el TVS D2 que @hardware demostró que rompe el bus a 25 m</strong>). A definir con
  @esquematico <strong>antes de mandar la PCB a JLCPCB</strong>: es la «más electrónica» que Matías le dijo a Andrés.</li>
  <li><strong>Las 8 salidas a reefer (4 módulos × 2) se prueban en banco con 25 m de cable real antes de
  despachar</strong>, con sus 3 sondas colgadas cada una. No sale nada que no haya cerrado a más distancia que la
  del sitio.</li>
  <li><strong>Especificación de cable</strong> (3 hilos, el par DQ/GND junto, sin empalmes, apto exterior para el par
  de afuera): <strong>queda interna</strong>, no se manda al cliente — el cable no lo provee Matías. <strong>Pero si
  Andrés pregunta qué comprar, se le dice, y ahí no se negocia.</strong></li>
</ul>

<div class="box"><p><strong>Lo que NO se le dice al cliente:</strong> que esto es un riesgo. En el documento va «no
incluye cable ni tendido» y «el tendido del cable de cada reefer al módulo lo hace el cliente», y nada más. La
mitigación real (banco con 25 m, un bus por reefer) tampoco se explica: se hace y punto. <strong>Y el tendido no se
cotiza</strong> («no contemples el tema de las tiradas»): la cuenta del caño queda en la hoja 11 como argumento.</p></div>
''')

# =================================================================== HOJA 6
hoja(u'''
<h2><span class="n">07</span>Qué lleva cada módulo, y qué de eso anda HOY</h2>
<div class="sub">Verificado en el código el 3-sep-2026. <strong>Los cuatro módulos (3 + repuesto) son la misma placa
Mini, poblada entera y con el 2.º bus.</strong> Ya no hay «simple»: lo que corre hoy en <code>REEFER_01_SCZ</code>
sirve para el hito 1 y como plan B parcial, no para el pedido.</div>
<table class="compacta"><thead><tr><th style="width:22%">Función</th><th class="num" style="width:11%">Doble<br>(×3 + rep.)</th>
<th>Qué hace el firmware hoy</th><th style="width:19%">Evidencia</th></tr></thead><tbody>
<tr><td>Sondas DS18B20</td><td class="num">6 (3 + 3)</td>
<td>Cada una identificada por ROM de 64 bits y reportada por separado; enganche en caliente; aviso si se desconecta;
<strong>offset de calibración por sonda en NVS</strong>. <code>SONDAS_MAX</code> está en 4: <strong>hay que subirlo a
8 y asignar cada ROM a su reefer</strong> — con un bus por reefer la asignación es por pin, no por tabla.</td>
<td><code>sondas.h</code>: <code>sondasEscanear</code>, <code>sondasLeer</code>, <code>sondasCalibrar</code>; línea 31 ·
<code>PINOUT_MINI.md</code> GPIO 4 / 18</td></tr>
<tr><td><strong>Verificación cruzada entre sondas</strong></td><td class="num gris">—</td>
<td><strong>NO existe.</strong> <code>sondasCalibrar()</code> iguala las sondas en un momento dado; el lazo de lectura
<strong>no compara sondas entre sí</strong> ni alerta por deriva. Con 3 °C reales entre puerta y fondo, la comparación
tiene que ser <strong>contra la propia historia de cada sonda</strong>, no contra el promedio del reefer.</td>
<td>ídem. Vendida en el <strong>hito 2</strong>, con la aclaración escrita en la página del cliente</td></tr>
<tr><td>Sensor de puerta</td><td class="num">2</td>
<td>Implementado <strong>para una sola puerta</strong>: GPIO5, alerta por puerta abierta &gt; 180 s, suprime la alerta
de temperatura mientras está abierta. Viene deshabilitado por defecto (<code>SENSOR_DOOR_ENABLED false</code>).
<strong>La segunda puerta hace falta en los tres.</strong></td>
<td><code>config.h</code> 72-74, 105, 119 · <code>.ino</code> 804-890</td></tr>
<tr><td>Entrada de defrost</td><td class="num">2</td>
<td>Implementada <strong>para una sola entrada</strong>: GPIO33, NA/NC configurable, deshabilita alertas durante el
ciclo con 30 min de enfriamiento. <strong>La segunda hace falta en los tres, y tiene que silenciar sólo el reefer que
descongela</strong> — es la prueba de aceptación del hito 2.</td>
<td><code>config.h</code> 91-96, 122 · <code>.ino</code> 54-55, 100-101, 872-878</td></tr>
<tr><td>Salidas a relé</td><td class="num">2</td>
<td><strong>1 gobernada</strong>: GPIO26, se activa sola con la alerta si <code>relayEnabled</code>. La segunda queda
cableada y disponible. <strong>El accionamiento manual desde el panel NO existe.</strong></td>
<td><code>config.h</code> 76-77, 140-150 · <code>.ino</code> 369-375, 483-488, 915-944 · <code>comandos_nube.h</code>
sin comando de relé → <strong>hito 5</strong></td></tr>
<tr><td>Gabinete</td><td class="num">1</td>
<td>Interior: Genrod IP65 210×310×110, $ 21.203 (×2 + repuesto). Exterior: Roker PRG357 IP65 200×200×155, $ 44.419
(×1, ya en el sitio).</td><td><code>BOM_CERRO_MORO.md</code> §3</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Regla de venta</span><h3>Lo que no anda hoy va con hito, nunca como característica</h3></div>
    <div class="cuerpo"><ul>
      <li><strong>Segunda puerta, segundo defrost por reefer, <code>SONDAS_MAX</code> a 8, reparto de sondas por
      reefer (un bus por reefer) y panel que muestra dos reefers por módulo</strong> — el software del módulo
      doble. Costeado (18 h, hoja 10), hito 2. <strong>Lo necesitan los tres módulos y el repuesto.</strong></li>
      <li><strong>Verificación cruzada entre sondas</strong> — hito 2.</li>
      <li><strong>Accionamiento manual del relé desde el panel</strong> — hito 5.</li>
    </ul></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">⚠ El riesgo que VOLVIÓ</span><h3>Sin firmware doble no reporta ningún módulo nuevo</h3></div>
    <div class="cuerpo"><p>Como en la v7.0. Estado real: <strong>APTO CON CORRECCIONES</strong> (auditoría 4-sep),
    correcciones en curso, <strong>sin fecha de cierre confirmada por @firmware</strong>. Lo que lo hace tolerable:
    el hito 1 no depende de él (es <code>REEFER_01_SCZ</code> con lo que ya anda + 2 sondas), y si se atrasa hay un
    plan B parcial: <strong>cada doble arranca vigilando un solo reefer con el firmware actual</strong> (3 de 5) mientras
    se cierra. <strong>No se vende como cosa hecha: se vende en el hito 2, como siempre. Y esto hay que decírselo al
    Director: volvió al camino crítico de la venta.</strong></p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>Orden de armado:</strong> identificación por ROM sí o sí (si se lee por índice, cuando
cae una sonda la otra se reporta con el nombre equivocado). <strong>Un bus por reefer</strong> (GPIO 4 y 18), cada uno
con pull-up 2k2 y alternativa 1k, 3 hilos, 100 nF + 10 µF al pie de la sonda más lejana, <strong>sin D2</strong>.
<strong>Cuál de las dos líneas se despacha — <code>firmware_revival</code> extendido o <code>firmware_modular</code>
v3.1 — lo define @firmware</strong> cuando cierren las correcciones; <strong>esta vez la decisión bloquea a los
tres.</strong> Habilitar <code>SENSOR_DOOR_ENABLED</code>, probar puerta y defrost de <strong>los dos canales de los 4
módulos</strong>, y correr la prueba de banco con 25 m en las 8 salidas antes de despachar.</p></div>
''')

# =================================================================== HOJA 7
hoja(u'''
<h2><span class="n">08</span>Lo que se instala, y quién</h2>
<div class="grid3">
  <div class="card fuerte">
    <div class="cab"><span class="tag">×1 · USD ''' + m(P["doble_ext"]) + u'''</span><h3>Módulo doble de exterior</h3></div>
    <div class="cuerpo"><p><strong>Gabinete estanco IP65 apto para exterior</strong> (Roker PRG357 200×200×155),
    fuente de 5 V 2 A, placa Mini con borneras a tornillo y <strong>2 buses 1-Wire</strong>, ESP32 en zócalo, módulo de
    2 relés, <strong>prensacables en todas las entradas</strong>, 6 sondas DS18B20 estancas, 2 reed de puerta, 2
    entradas de defrost — para el par de afuera, montado sobre la unión.</p></div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">×2 · USD ''' + m(P["doble_int"]) + u'''</span><h3>Módulo doble de interior</h3></div>
    <div class="cuerpo"><p>Uno por cada par bajo techo. Gabinete IP65 de interior (Genrod 210×310×110 o las de
    stock si pasan la medición <code>M9</code>), <strong>la misma placa</strong>, 6 sondas, 2 reed, 2 defrost. El par
    con el reefer parado arranca con 3 sondas puestas y 3 en espera, ya calibradas.</p></div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">×1 · USD ''' + m(P["repuesto"]) + u'''</span><h3>Kit de repuesto</h3></div>
    <div class="cuerpo"><p>Un <strong>módulo doble completo</strong> — la placa es la misma en los cuatro, así que
    <strong>cubre a cualquiera</strong> — con 6 sondas y 2 reed. Va con gabinete de interior: <strong>si el que falla
    es el de afuera, la electrónica se pasa a la caja estanca que ya está en sitio</strong> (queda escrito en el
    runbook).</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>Montaje: Andrés</strong> (o quien la empresa designe), con kit preconfigurado y probado
en banco + videollamada. Dos pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los
<strong>$ 2.500.000</strong>, y Matías no puede viajar en octubre (Dreyfus). <strong>Eso es lo que esta propuesta no
cobra.</strong> <strong>El cable no lo mandamos</strong> (decisión del 4-sep): son seis tiradas cortas de la unión a
cada reefer, y las hace el cliente. <strong>Qué pasa con <code>REEFER_01_SCZ</code>:</strong> cumple el hito 1 con
sus 3 sondas; en el hito 2 su reefer pasa al doble de su par, <strong>sus 3 sondas ya calibradas se reaprovechan</strong>
y el kit viejo queda en el campamento como segundo respaldo o vuelve a Bahía (decide Matías, pendiente 7).</p></div>

<div class="nota"><p><strong>Intemperie:</strong> <span class="neutro">en el documento del cliente se dice
«gabinete estanco IP65 apto para exterior» <strong>y nada más</strong>. Ni material, ni fabricación. Ni en el PDF ni
en el WhatsApp.</span></p></div>

<div class="sep"></div>

<h2><span class="n">09</span>Opcionales, después de la primera orden</h2>
<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Sin costo de equipo · +100/mes</span><h3>El sexto reefer cuando vuelva a servicio</h3></div>
    <div class="cuerpo"><p><strong>El doble de su par ya trae sus 3 sondas, su reed y su defrost.</strong> Es conectar y
    subir el abono de 500 a 600. Está escrito con ese precio (cero) en el documento del cliente: no hay que venderlo
    de nuevo, solo ejecutarlo. <strong>Es el upsell más probable y de mejor margen de esta cuenta</strong> — y ahora
    no tiene fricción de compra.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Los otros tres</span><h3>Se ofrecen cuando las sondas estén andando, no antes</h3></div>
    <div class="cuerpo"><ul>
      <li><strong>Sirena o baliza: a USD 40 NO deja margen.</strong> @hardware midió que la BR300 de exterior sale
      $ 39.530 (USD 26) <strong>más su propia fuente de 12 V</strong>, porque el relé entrega contacto seco.
      <strong>Propuesta: USD 70 instalada</strong>, o baliza LED de 12 V, más barata. Decide Matías.</li>
      <li><strong>Cuarta sonda</strong> en un reefer (USD 40 + USD 5/mes) — con 3 °C entre puerta y fondo, puede
      pedirse sola.</li>
      <li>Base con batería y 4G, la única que avisa el corte de energía por sí misma (a cotizar) —
      <strong>especialmente vendible para la caja de la intemperie, de la que dependen dos reefers</strong>.</li>
    </ul></div>
  </div>
</div>
''')

# =================================================================== HOJA 7b
hoja(u'''
<h2><span class="n">10</span>Los riesgos técnicos abiertos</h2>
<table class="compacta"><thead><tr><th style="width:5%">&nbsp;</th><th style="width:30%">Riesgo</th><th>Estado</th></tr></thead><tbody>
<tr><td class="num">1</td><td><strong>⚠ EL QUE VOLVIÓ: el firmware doble es crítico para los tres módulos</strong></td>
<td>Como en la v7.0. APTO CON CORRECCIONES, en curso, sin fecha. Plan B parcial: cada doble arranca con un solo
reefer (3 de 5). <strong>@firmware tiene que dar fecha antes de que Matías prometa el hito 2 por teléfono.</strong></td></tr>
<tr><td class="num">2</td><td><strong>Una caja sin energía = dos reefers ciegos, siempre</strong></td>
<td>Mitigación cotizada: repuesto en el campamento + aviso de equipo mudo desde la nube. Está escrito en «Lo que hay
que saber» del PDF, sin dramatizar.</td></tr>
<tr><td class="num">3</td><td><strong>Decisión de placa: poblar el 2.º bus antes de pedir la PCB</strong></td>
<td>La Mini deja GPIO 18/23 reservados. Con un bus por reefer el reparto es por pin y el defrost cruzado es trivial;
con un solo bus de 6 sondas hay que repartir por tabla de ROM y probar el bus a 6 sondas con dos ramas. <strong>Lo
define @esquematico con Matías esta semana; después de JLCPCB ya no.</strong></td></tr>
<tr><td class="num">4</td><td><strong>✅ Cobertura de red: 3 puntos</strong></td>
<td>Mejor que los 5 de la v8.0 y que los 4 de la v6.1. Sigue siendo pregunta para Andrés antes de despachar.</td></tr>
<tr><td class="num">5</td><td><strong>✅ Cable: seis tiradas cortas, ninguna entre contenedores</strong></td>
<td>La caja sobre la unión las acorta todas. Queda el cruce de masas entre los dos contenedores de cada par por el
hilo de GND: un bus por reefer lo aísla en datos, no en masa. Riesgo asumido (hoja 5).</td></tr>
<tr><td class="num">6</td><td><strong>El defrost cruzado, ahora en los tres</strong></td>
<td>Que el descongelamiento de un reefer no ciegue al otro. Es la prueba de aceptación del hito 2 («forzar el defrost
de un reefer y que el que comparte módulo siga alarmando») y aplica a los 3 pares.</td></tr>
<tr><td class="num">7</td><td><strong>La caja de exterior a la intemperie de Santa Cruz</strong></td>
<td>Única parte del equipo sin antecedente de campo largo, y de ella dependen 2 reefers. La que se mandó el 4-sep es
la prueba de campo: pedirle a Andrés una foto tras el primer temporal.</td></tr>
<tr><td class="num">8</td><td><strong>⚠ Plazo de fabricación — sigue siendo el cuello</strong></td>
<td>@hardware: con la PCB Mini el despacho realista es <strong>semana 4-5, no 2</strong>, y el hito 2 caería en la
<strong>7-8</strong>. Son 4 placas en vez de 6, pero el plazo lo pone JLCPCB + DHL, no la cantidad. En el documento del
cliente los hitos quedan como están; <strong>Matías resuelve con @hardware antes de firmar</strong> (pedir la PCB ya,
USD 43, sirve igual para las demos de Bahía).</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="cita"><p><strong>Resumen para el Director, en una línea:</strong> contra la v8.0 <strong>bajaron</strong> la
red (5 → 3 puntos), el cable (1 tirada larga → 6 cortas), las cajas (5 → 3) y el precio (−200); <strong>subieron</strong>
el firmware doble (vuelve a bloquear a todos) y el alcance de una caída (siempre 2 reefers). El cuello de fabricación
es el mismo. <strong>Saldo: mejor negocio, mismo riesgo de plazo, un riesgo técnico más concentrado.</strong></p></div>
''')

# =================================================================== HOJA 8
hoja(u'''
<h2><span class="n">11</span>Los tres precios, con el MISMO margen: interior ''' + m(P["doble_int"]) + u''' · exterior ''' + m(P["doble_ext"]) + u''' · repuesto ''' + m(P["repuesto"]) + u'''</h2>
<div class="sub">Base: <code>BOM_CERRO_MORO.md</code> rev A (@hardware, 4-sep), precios verificados en vivo; cambio $ → USD
al BNA vendedor <strong>1.530 (8-sep)</strong>. <strong>Mismo criterio que la v8.0: ~32 % sobre precio de venta, parejo.</strong></div>

<table class="compacta"><thead><tr><th>&nbsp;</th><th class="num" style="width:14%">Doble interior<br>(ARS)</th>
<th class="num" style="width:9%">USD</th><th class="num" style="width:14%">Doble exterior<br>(ARS)</th>
<th class="num" style="width:9%">USD</th></tr></thead><tbody>
<tr><td>Electrónica: ESP32 + módulo de 2 relés + fuente 5 V 2 A + PCB Mini prorrateada + consumibles y prensacables
<strong>+ 2.º bus 1-Wire con su protección, 2.ª entrada de defrost, borneras y prensacables ×2</strong> (30 de la v8 + ~8)</td>
<td class="num gris">~58.000</td><td class="num">38</td><td class="num gris">~58.000</td><td class="num">38</td></tr>
<tr><td><strong>Gabinete</strong> — interior Genrod IP65 210×310×110 $ 21.203 · exterior Roker PRG357 IP65
200×200×155 $ 44.419</td>
<td class="num gris">21.203</td><td class="num">14</td><td class="num gris">44.419</td><td class="num">29</td></tr>
<tr><td>Sondas DS18B20 estancas moldeadas de 3 m ($ 10.587 c/u): 6 por módulo</td>
<td class="num gris">63.522</td><td class="num">41</td><td class="num gris">63.522</td><td class="num">41</td></tr>
<tr><td>Sensores magnéticos de puerta cableados: 2 por módulo</td>
<td class="num gris">16.274</td><td class="num">11</td><td class="num gris">16.274</td><td class="num">11</td></tr>
<tr><td>Envío a Santa Cruz, prorrateado en <strong>4</strong> bultos (eran 6)</td>
<td class="num gris">&nbsp;</td><td class="num">15</td><td class="num gris">&nbsp;</td><td class="num">17</td></tr>
<tr><td>Armado + <strong>prueba de banco documentada de los DOS buses con 25 m de cable</strong> + garantía de
reposición amortizada (era 150 en el doble de la v8)</td><td class="num gris">&nbsp;</td><td class="num">160</td><td class="num gris">&nbsp;</td><td class="num">160</td></tr>
<tr><td>Parte de plataforma del desarrollo: USD 1.000 repartidos en <strong>3</strong> módulos vendidos (eran 5 → 200)</td>
<td class="num gris">&nbsp;</td><td class="num">333</td><td class="num gris">&nbsp;</td><td class="num">333</td></tr>
<tr><td>Costo</td><td class="num gris">&nbsp;</td><td class="num">612</td><td class="num gris">&nbsp;</td><td class="num">629</td></tr>
<tr class="total"><td><strong>Precio</strong> (costo / 0,68, redondeado: 900 · 925 → 950)</td><td class="num gris">&nbsp;</td><td class="num">''' + m(P["doble_int"]) + u'''</td>
<td class="num gris">&nbsp;</td><td class="num">''' + m(P["doble_ext"]) + u'''</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<table class="compacta"><thead><tr><th>Ítem</th><th class="num" style="width:12%">Costo</th>
<th class="num" style="width:12%">Margen</th><th class="num" style="width:12%">Precio</th>
<th class="num" style="width:10%">%</th></tr></thead><tbody>
<tr><td><strong>Doble de interior</strong> (×2)</td><td class="num">612</td><td class="num">288</td><td class="num"><strong>''' + m(P["doble_int"]) + u'''</strong></td><td class="num">32,0 %</td></tr>
<tr><td><strong>Doble de exterior</strong> (×1) — redondeado a 950: caja de intemperie, de la que dependen 2 reefers, y mayor plazo</td><td class="num">629</td><td class="num">321</td><td class="num"><strong>''' + m(P["doble_ext"]) + u'''</strong></td><td class="num">33,8 %</td></tr>
<tr><td><strong>Repuesto doble</strong> (×1, completo, sin cargo de plataforma) — redondeado a 400 hacia abajo: queda en estante</td><td class="num">279</td><td class="num">121</td><td class="num"><strong>''' + m(P["repuesto"]) + u'''</strong></td><td class="num">30,2 %</td></tr>
<tr class="total"><td><strong>Total equipos + repuesto</strong></td><td class="num">2.132</td><td class="num">1.018</td><td class="num"><strong>''' + m(C["equipos"]) + u'''</strong></td><td class="num">32,3 %</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Por qué un doble sale 900 y no 1.200 (ni 700)</span><h3>La cuenta, renglón por renglón</h3></div>
    <div class="cuerpo"><p>Contra dos simples de la v8 (2 × 600): ESP32 + fuente + relés + PCB + gabinete + envío +
    alta + punto de red <strong>NO se duplican</strong>; sondas y reed <strong>sí</strong>. Contra el doble de la v8
    (700): <strong>+8 de electrónica</strong> (2.º bus, 2.º defrost, borneras), <strong>+10 de armado</strong> (dos buses a
    probar), <strong>+5 de envío</strong> (menos bultos) y <strong>+133 de plataforma</strong> (USD 1.000 entre 3 y no
    entre 5). Costo 473 → 612 (+139); precio 700 → 900 (+200). <strong>Se le dice al cliente sin abrir la cuenta: menos
    cajas, más electrónica y más programación por caja.</strong> Y si la abren, los tres ítems tienen el mismo margen.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Por qué el total baja 200 y no 1.000</span><h3>Dos cajas menos no son dos precios menos</h3></div>
    <div class="cuerpo"><p>v8: 4×600 + 700 + 350 = 3.450 en equipos. v9: 2×900 + 950 + 400 = ''' + m(C["equipos"]) + u'''. <strong>−300 en equipos
    (−8,7 %)</strong>, con la misma plataforma (1.000), las mismas 15 sondas en servicio y 4 placas en vez de 6.
    Puesta en marcha 1.550 → 1.650 (<strong>+100</strong>: +8 h de software, −4 h de altas). <strong>Neto −200.</strong>
    El margen absoluto de equipos baja de 1.105 a 1.018 (−87): es lo que cuesta que Andrés tenga razón — y la tiene:
    menos cable, menos red, menos cajas.</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>Cómo llegó a ''' + m(C["total"]) + u''', y por qué no se forzó a 5.000.</strong> Se costeó cada ítem desde el BOM
rev A con los tres cambios reales (2.º bus, plataforma entre 3, dos buses a probar), se aplicó el 32 % de la v8.0 y se
redondeó cada unitario (900 / 950 / 400); la puesta en marcha se recontó hora por hora (66). <strong>La suma dio
''' + m(C["total"]) + u''' sola.</strong> «Más o menos lo mismo» es −4 %, y es honesto con el cliente que propuso la configuración más
barata de instalar. <strong>Alternativa para sostener 5.000</strong>: exterior 1.000 · interior 950 × 2 · repuesto 400 ·
puesta 1.700 = 5.000, margen 36 % — desparejo con el 32 % de la v8.0. <strong>Recomiendo ''' + m(C["total"]) + u'''. Decide Matías.</strong>
B anual = ''' + m(C["b1"]) + u'''; anticipo 50 % = ''' + m(C["anticipo"]) + u'''.</p></div>
''')

# =================================================================== HOJA 9
hoja(u'''
<h2><span class="n">12</span>Puesta en marcha, USD ''' + m(P["puesta"]) + u'''</h2>
<table class="compacta"><thead><tr><th>Trabajo</th><th class="num" style="width:10%">h</th></tr></thead><tbody>
<tr><td>Sondas, rangos y umbrales por reefer + <strong>calibración de las 15 sondas</strong> contra referencia y
registro de offsets (con los 3 °C puerta-fondo de Andrés como primer dato de rango)</td><td class="num">10</td></tr>
<tr><td><strong>Software del módulo doble, ahora en los tres: segunda puerta, segundo defrost con silenciado por
reefer, <code>SONDAS_MAX</code> a 8, un bus por reefer con asignación de sondas por bus, panel que muestra dos reefers
por módulo, validación de los dos buses a 25 m</strong> (10 h en la v8 + 8 del reparto por reefer y el panel)</td><td class="num">18</td></tr>
<tr><td>Registro exportable con código de verificación</td><td class="num">14</td></tr>
<tr><td>Panel multi-equipo y usuarios de lectura</td><td class="num">10</td></tr>
<tr><td>Puesta en marcha remota (alta, credencial, OTA verificada, prueba de puerta y defrost de los dos canales),
pruebas de campo con Andrés, runbook y capacitación — <strong>3 módulos</strong> (eran 5 → 14 h)</td><td class="num">10</td></tr>
<tr><td>Salud de bus, histéresis de 3 barridos y <strong>verificación cruzada entre sondas</strong></td><td class="num">4</td></tr>
<tr class="total"><td><strong>Total a USD 25/h</strong></td><td class="num">66 h = USD ''' + m(P["puesta"]) + u'''</td></tr>
</tbody></table>
<p class="tabla-pie">De 62 a 66 h: <strong>+8 h en el software del doble</strong> (es la «programación» que Matías le dijo a Andrés:
repartir por reefer lo que entra por dos buses, silenciar por reefer y mostrar dos reefers por caja) y <strong>−4 h</strong>
en altas remotas (3 en vez de 5). Si @firmware dice que son más horas, <strong>salen del margen, no del precio</strong>.</p>

<div class="sep"></div>

<h2><span class="n">13</span>Servicio mensual: qué cuesta servir y qué se cobra</h2>
<table class="compacta"><thead><tr><th>Costo directo mensual</th><th class="num" style="width:16%">v8.0 (5 módulos)</th>
<th class="num" style="width:22%">v9.0 (15 sondas, 5 reed, 3 módulos)</th></tr></thead><tbody>
<tr><td>Supabase Pro</td><td class="num gris">25</td><td class="num">25</td></tr>
<tr><td>Reposición amortizada (módulos y sondas en garantía)</td><td class="num gris">18</td><td class="num">15</td></tr>
<tr><td>Soporte (2,5 h → 2,3 h a USD 25)</td><td class="num gris">62</td><td class="num">57</td></tr>
<tr><td>Informe mensual</td><td class="num gris">25</td><td class="num">25</td></tr>
<tr class="total"><td><strong>Total</strong></td><td class="num gris">130</td><td class="num">122</td></tr>
</tbody></table>
<p class="tabla-pie">Reposición y soporte vuelven a los valores de la v7.0 (3 módulos en campo).</p>

<div class="sep-ch"></div>

<div class="cita"><p><strong>Tarifa: USD 100 por reefer por mes × 5 = USD ''' + m(C["abono"]) + u'''/mes</strong> (decisión de Matías,
no se toca con la configuración nueva). Costo directo 122 → <strong>margen bruto USD 378 (76 %)</strong>.
Con el inicial en ''' + m(C["total"]) + u''', <strong>el abono paga el equipamiento entero en 12,7 meses de margen</strong>: sigue siendo
el renglón que sostiene la cuenta. La justificación, si preguntan: <strong>mantenimiento del servidor, custodia de
los datos y seriedad del servicio</strong> — el registro que se entrega tiene que estar disponible y ser defendible
dentro de un año, y eso se paga todos los meses aunque no pase nada.</p></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Por reefer, no por caja</span><h3>El abono es estrictamente proporcional a los reefers</h3></div>
    <div class="cuerpo"><p>5 reefers = 500, 6 = 600. Pasamos de 5 cajas a 3 y se vigila lo mismo — 5 reefers.
    <strong>Y esta vez la regla juega al revés y también sirve:</strong> si preguntan «¿con menos equipos no baja el
    mensual?», la respuesta está escrita desde la v2: el servicio se cobra por reefer vigilado, no por caja
    instalada. Cuando entre el sexto, los USD 100 adicionales son margen puro: el equipo ya está puesto y las sondas
    también.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Eliminado</span><h3>El escalón de los primeros 3 meses al 50 %</h3></div>
    <div class="cuerpo"><p>Decisión de Matías, 4-sep: <strong>abono completo desde el primer mes</strong> en las dos
    formas. Lo justifica que el servicio ya está corriendo —servidor, custodia y guardia de alertas— desde el primer
    equipo que reporta.</p></div>
  </div>
</div>
''')

# =================================================================== HOJA 10
hoja(u'''
<h2><span class="n">14</span>LA CUENTA DEL CAÑO — archivo, y por qué ya no entra en el precio</h2>
<div class="sub">Se conserva de la v5 <strong>como historia y como argumento</strong>, no como parte del presupuesto.
<strong>El tendido lo hace y lo paga el cliente, y no aparece en el documento que se manda.</strong> Con la v9 <strong>no
queda ninguna tirada entre contenedores</strong>: la caja va sobre la unión de cada par y de ahí sale un cable corto a cada
reefer. Esta cuenta era la de UNA tirada de 25 m con caño Daisa; hoy sirve para saber cuánto se ahorró el sitio con la
configuración que propuso Andrés.</div>

<table class="compacta"><thead><tr><th>Ítem (por par, 25 m de recorrido)</th><th class="num" style="width:24%">Subtotal</th></tr></thead><tbody>
<tr><td>Caño galvanizado Daisa 3/4 liviano, 9 tiras de 3 m a $ 11.637</td><td class="num">$ 104.733</td></tr>
<tr><td>Cuplas (8), curvas (6), cajas de paso estancas (4), conectores caño-caja (10)</td><td class="num">$ 96.000</td></tr>
<tr><td>Grampas omega 3/4 una cada 1,5 m (18) + tarugos y tornillos</td><td class="num">$ 35.000</td></tr>
<tr><td>Cable exterior, 30 m a $ 400/m</td><td class="num">$ 12.000</td></tr>
<tr class="total"><td><strong>Materiales por par</strong></td><td class="num">≈ $ 247.700 ≈ USD 161</td></tr>
<tr><td>Mano de obra: 2 jornadas de oficial electricista al piso de tarifa ($ 12.000/h × 16 h)</td>
<td class="num">$ 192.000 ≈ USD 125</td></tr>
<tr class="total"><td><strong>Total por par</strong></td><td class="num">$ 439.700 ≈ USD 286</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<h3>Para qué sirve esta cuenta ahora que no la cotizamos. Tres cosas concretas.</h3>
<ul class="lista">
  <li><strong>Saber cuánto vale lo que Andrés resolvió con la caja en la mano:</strong> tres pares que hubieran
  costado hasta USD 286 cada uno de canalización se convirtieron en seis cables cortos. Si igual dicen «esto de la
  obra no lo teníamos previsto», la respuesta ya está: <strong>la configuración la describieron ellos, y es la de
  menos obra posible</strong>.</li>
  <li><strong>El argumento del precio del doble.</strong> Si alguien compara 900 contra «dos simples de 600», acá
  está lo que NO se paga: ni canalización entre contenedores ni un segundo punto de red por par.</li>
  <li><strong>Que nadie regale la instalación.</strong> Si aparece la tentación de «se lo hacemos nosotros para
  cerrar», el número a tener en la cabeza es <strong>USD 286 por tirada</strong>, más pasajes y estadía.</li>
</ul>

<div class="sep-ch"></div>

<div class="nota"><p><strong>Honestidad sobre esta cuenta.</strong> <span class="neutro">Los renglones de cuplas,
curvas, cajas de paso, grampas y cable son <strong>estimados</strong> a precio de plaza; el caño y la mano de obra
salen de precios y de piso de tarifa relevados. Es una cuenta para decidir y para argumentar, no una cotización de
obra: <strong>nosotros no la cotizamos y no la ejecutamos.</strong></span></p></div>
''')

# =================================================================== HOJA 11
hoja(u'''
<h2><span class="n">15</span>Condiciones de pago — 50 / 50, y por qué no 25</h2>
<div class="sub"><strong>50 % con la orden de compra</strong> (anticipo de materiales) y <strong>50 % contra los
equipos instalados y reportando</strong>. El abono arranca con el primer equipo andando.</div>
<p>El fundamento es de caja: hay que comprar y armar <strong>4 módulos dobles</strong> (3 + el repuesto) antes de ver un
peso del segundo tramo, y cobrar ese tramo a un contratista que todavía no tiene nombre. Con el 50 % (<strong>USD
''' + m(C["anticipo"]) + u''' ≈ $ ''' + m(C["anticipo"] * P["bna"]) + u'''</strong>) la compra completa de materiales —<strong>≈ $ 749.000, hoja 13</strong>— queda
cubierta <strong>casi cinco veces</strong> antes de tocar un componente. Con el 25 % (USD ''' + m(C["anticipo"] / 2) + u''' ≈ $ ''' + m(C["anticipo"] / 2 * P["bna"]) + u''')
también alcanzaría para los materiales; lo que no cubriría es el <strong>riesgo de cobranza del segundo tramo</strong>,
que es lo que en realidad se está financiando.</p>
<div class="box"><p>Los hitos siguen existiendo <strong>como compromiso de entrega con plazo</strong>, y así está
escrito en el documento del cliente: «no se facturan aparte, están incluidos en el precio». <strong>Punto para que
Matías confirme:</strong> cobrar antes de entregar los hitos es más cómodo para la caja y más exigente con la
palabra.</p></div>

<div class="sep"></div>

<h2><span class="n">16</span>Las dos formas de pagar, y por qué se cayó la tercera</h2>
<div class="grid2">
  <div class="card fuerte">
    <div class="cab"><span class="tag">A</span><h3>Equipos + servicio mensual</h3></div>
    <div class="cuerpo"><p>''' + m(C["total"]) + u''' + 12 × ''' + m(C["abono"]) + u''' = <strong>USD ''' + m(C["a12"]) + u'''</strong> el primer año; 6.000/año después;
    <strong>24 meses ''' + m(C["a24"]) + u'''</strong>.</p></div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">B</span><h3>Anual adelantado, 10 % sobre el servicio</h3></div>
    <div class="cuerpo"><p>''' + m(C["total"]) + u''' + (12 × ''' + m(C["abono"]) + u''') × 0,9 = ''' + m(C["total"]) + u''' + ''' + m(C["anual_b"]) + u''' = <strong>USD ''' + m(C["b1"]) + u'''</strong>; renovación
    ''' + m(C["anual_b"]) + u'''/año; <strong>24 meses ''' + m(C["b24"]) + u'''</strong>. El descuento le ahorra <strong>USD 600</strong> el primer año y lo que
    compra es concreto: <strong>cero riesgo de cobranza durante 12 meses</strong> con un contratista que probablemente
    pague a 60-90 días, una factura en lugar de doce, y caja para armar los equipos.</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="nota"><p><strong>C, eliminada.</strong> <span class="neutro">Matías: «el de la inversión inicial no lo
ofrecería». Era la única que ponía USD ~5.000 nuestros en manos de un contratista a 1.500 km, sin poder retirar los
equipos y sin contrato con permanencia. <strong>No se vuelve a ofrecer sin contrato validado por contador y un cliente
con historial de pago.</strong> Con dos opciones el comprador elige; con tres se paraliza.</span></p></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Moneda y facturación</span><h3>USD, pago en pesos al BNA de la fecha de pago</h3></div>
    <div class="cuerpo"><p><strong>Sin validez en el PDF.</strong> Referencia impresa: BNA vendedor billete
    <strong>$ 1.530 del 8-sep-2026</strong> (bna.com.ar, 09:50). Nota interna: revisar precios si pasan más de 6 meses
    desde el 8-sep. Antes de la cotización firme hay que saber: monotributo vs. RI, plazo de pago, si acepta la cláusula
    de moneda, quién firma. Se pregunta cuando la empresa tenga nombre. <strong>Sin cláusulas condicionales:</strong> el
    tendido es del cliente y el precio es firme.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Los dos números que cierran cualquier objeción de precio</span><h3>La pérdida y el competidor</h3></div>
    <div class="cuerpo"><p>Una pérdida de 3 t valuada al precio de novillo en pie ($ 4.181/kg, INMAG jul-2026) son
    <strong>$ 12,5 M: 16 meses de servicio</strong> al abono de USD 500 (≈ $ ''' + m(C["bna_abono"]) + u''' por mes).</p>
    <p>testo Saveris 2-T2: USD 318 por unidad y mide <strong>un</strong> punto; para cubrir los 15 puntos de esta
    propuesta harían falta 15 unidades = <strong>USD 4.770</strong> antes de importación — <strong>prácticamente el total
    de esta propuesta</strong> — sin nube, sin puerta, sin relé, sin defrost, sin repuesto en sitio — y se configura con
    una red WiFi y una clave, que es exactamente lo que este sitio no tiene. <strong>Y ninguna de esas unidades es
    apta para la intemperie sin gabinete adicional.</strong></p></div>
  </div>
</div>
''')

# =================================================================== HOJA 12
hoja(u'''
<h2><span class="n">17</span>Los 4 módulos: qué falta comprar y cuánto sale (estimación, pide rev B a @hardware)</h2>
<div class="sub"><strong>1 doble de exterior + 2 dobles de interior + 1 doble de repuesto = 4 placas Mini, las 4 con
el 2.º bus.</strong> Gabinetes: 1 de intemperie (ya en sitio) + 3 de interior. Sondas: 18 en los dobles (las 3 de
<code>REEFER_01_SCZ</code>, ya calibradas, se reaprovechan) + 6 del repuesto = <strong>21 a comprar</strong>. Reed: 6 + 2
− 1 existente = <strong>7</strong>. Defrost: 6 entradas (opto, cable y bornera). <strong>Reservados 3 ESP32 para las galgas de
Dreyfus</strong>, que es P0 de octubre.</div>

<p>La cuenta arranca del BOM real de @hardware y del total de la v8 (6 placas, ≈ $ 821.000). De ahí a la v9:</p>

<table class="compacta"><thead><tr><th>Ajuste a la v9</th><th class="num" style="width:16%">$</th></tr></thead><tbody>
<tr><td><strong>−2 placas</strong> (4 en vez de 6): 2 ESP32 ($ 14.999), 2 fuentes ($ 10.579), 2 gabinetes de interior
($ 21.203) y sus consumibles, borneras, optos y prensacables</td><td class="num">−$ 160.000</td></tr>
<tr><td><strong>+2.º bus 1-Wire en las 4 placas</strong>: pull-up + alternativa, resistencia serie, clamps, bornera,
prensacable y opto de la 2.ª entrada de defrost (≈ $ 12.000 por placa, estimado; los pines ya están)</td><td class="num">+$ 48.000</td></tr>
<tr><td><strong>+3 sondas</strong> (21 en vez de 18: los dobles van completos y el repuesto también)</td><td class="num">+$ 31.761</td></tr>
<tr><td><strong>+1 reed</strong> (7 en vez de 6)</td><td class="num">+$ 8.137</td></tr>
<tr><td>Rollo de UTP para la prueba de banco, módulos de relé, caja Roker (ya comprada): sin cambio</td><td class="num">0</td></tr>
<tr class="total"><td><strong>TOTAL v9 (estimado)</strong></td><td class="num">≈ $ 749.000 ≈ USD 490</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Bajan si...</span><h3>USD 76 en 10 minutos con un calibre</h3></div>
    <div class="cuerpo"><p>Si las 3 cajas IP65 de stock pasan la medición <code>M9</code> (−$ 63.609: ahora alcanzan
    justo para los 3 gabinetes de interior) y las fuentes de stock resultan de 2 A (−$ 52.895). Las dos mediciones
    juntas valen USD 76 y son 10 minutos con un calibre (<code>BOM_CERRO_MORO.md</code> §7.1).</p>
    <p><strong>Contra el anticipo del 50 % (USD ''' + m(C["anticipo"]) + u''' ≈ $ ''' + m(C["anticipo"] * P["bna"]) + u'''), la compra completa es el 20 %.</strong> No hay
    problema de plata ni de cantidades.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">⚠ Lo que hay que pedirle a @hardware</span><h3>Rev B del BOM: 4 placas dobles con 2 buses</h3></div>
    <div class="cuerpo"><p>El +$ 48.000 del 2.º bus y el −$ 160.000 de las dos placas son estimaciones sobre el rev A.
    <strong>@hardware recuesta las 4 placas con el 2.º bus poblado y sin D2</strong>, y confirma si el stock de 20 sondas
    y 10 reed de <code>PLATA.md</code> sirve (escenario A, rearmar) o se compran moldeadas (escenario B, recomendado).
    <strong>El margen del 32 % aguanta ± USD 40 por placa sin tocar precios.</strong></p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>La PCB es el renglón de mayor plazo de entrega: se pide primero, y con el 2.º bus ya
decidido</strong> (la caja Roker ya está en el sitio). Orden de pago el día de la OC (<code>BOM_CERRO_MORO.md</code> §8):
1. PCB a JLCPCB (10 placas: las 4 de Cerro Moro + demos de Bahía) · 2. los ESP32, todos al mismo vendedor y en la
misma orden · 3. sondas y cable, que bloquean la prueba de banco · 4. gabinetes de interior si <code>M9</code> no pasa ·
5. el resto. <strong>Nada antes del conteo de stock de 30 minutos.</strong></p></div>
''')

# =================================================================== HOJA 13
hoja(u'''
<h2><span class="n">18</span>El camino a los hitos 1 y 2, en semanas desde la aceptación</h2>
<div class="cita"><p><strong>El plan arranca cuando aceptan, no antes.</strong> Semana 0 = aceptación + anticipo del
50 %. Hasta que eso pase <strong>no se compra, no se arma y no se despacha nada</strong>, y a Andrés no se le pide que
reserve ninguna ventana: trabaja por turnos de 15 días y no es él quien aprueba. <strong>Única excepción, y es de
diseño, no de compra:</strong> decidir el 2.º bus con @esquematico esta semana, porque condiciona la PCB.</p></div>

<table class="compacta"><thead><tr><th>Paso</th><th class="num" style="width:24%">Plazo desde la aceptación</th>
<th style="width:18%">Quién</th></tr></thead><tbody>
<tr><td><strong>Decisión del 2.º bus en la Mini</strong> (GPIO 18, sin D2) — antes de pedir la PCB</td><td class="num">esta semana</td><td>Matías / @esquematico</td></tr>
<tr><td>Conteo del stock real + las mediciones <code>M1</code>-<code>M5</code> (huellas), <code>M7</code>, la
<code>M9</code> (interior de las 3 cajas) y la etiqueta V/A de las fuentes</td><td class="num">semana 0</td><td>Gonza</td></tr>
<tr><td>Compra del faltante — <strong>la PCB primero</strong></td><td class="num">semana 0-1</td><td>Gonza / Matías</td></tr>
<tr><td>Despacho de 2 sondas para el equipo ya instalado (encomienda, 5-8 días hábiles)</td><td class="num">semana 1</td><td>—</td></tr>
<tr><td><strong>Cierre del firmware doble</strong> (correcciones de la auditoría 4-sep + 2.ª puerta, 2.º defrost por
reefer, <code>SONDAS_MAX</code> a 8, un bus por reefer) — <strong>bloquea a los tres módulos</strong></td><td class="num">semana 1-3</td><td>Matías / @firmware</td></tr>
<tr><td>Alta, calibración remota, rangos y primera alerta real en <code>REEFER_01_SCZ</code></td><td class="num">semana 2</td><td>Andrés + Matías</td></tr>
<tr class="total"><td><strong>HITO 1</strong></td><td class="num">semana 2</td><td>—</td></tr>
<tr><td>Armado de los 4 módulos + <strong>prueba de banco de las 8 salidas con 25 m de cable</strong></td><td class="num">semana 1-3</td><td>Gonza / Sergio</td></tr>
<tr><td>Despacho de los 4 bultos (3 módulos + repuesto) a Cerro Moro</td><td class="num">semana 2-3</td><td>—</td></tr>
<tr><td><strong>Tendido de los 6 cables cortos</strong>, de la unión de cada par a cada reefer (apto exterior en el par de afuera)</td><td class="num">semana 3</td><td><strong>cliente</strong></td></tr>
<tr><td>Montaje de las 3 cajas sobre la unión de cada par; el reefer de <code>REEFER_01_SCZ</code> pasa a su doble con sus 3 sondas</td><td class="num">semana 3-4</td><td>campamento</td></tr>
<tr><td>Alta y calibración de las 12 sondas nuevas (las 3 de <code>REEFER_01_SCZ</code> ya quedaron en el hito 1)</td><td class="num">semana 4</td><td>Matías</td></tr>
<tr class="total"><td><strong>HITO 2</strong> (los 3 módulos y los 5 reefers reportando + una semana sin falsas alarmas)</td><td class="num">semana 5</td><td>—</td></tr>
</tbody></table>
<p class="tabla-pie"><span class="neutro"><strong>Nada de esta tabla se adelanta:</strong> las sondas, la compra, el
armado y el despacho arrancan con la aceptación y el anticipo. No hay una sola acción de compra para hoy.</span></p>

<div class="sep-ch"></div>

<div class="nota"><p><strong>El riesgo que hay que decir en voz alta: el hito 2 tiene dos dueños otra vez.</strong>
<span class="neutro"><strong>La fabricación</strong> (@hardware: despacho realista semana 4-5, hito 2 en la 7-8) <strong>y
el firmware doble</strong>, que en la v8.0 había salido del camino crítico y <strong>acá vuelve para los tres módulos</strong>.
Lo que ya no aprieta: la obra del cliente (seis cables cortos) y la red (3 puntos). Matías no debería prometer el
hito 2 por teléfono con más firmeza que la que dice el papel, y esto hay que resolverlo con @hardware y @firmware
antes de firmar.</span></p></div>

<div class="box"><p><strong>Por qué se puede empezar a armar antes de la orden de compra, sin exponer un peso
nuevo.</strong> Los kits <strong>ya estaban planificados como las unidades de demostración del plan comercial de
Bahía</strong>. Si Cerro Moro no compra, no quedan colgados: van a su destino original. <strong>La contracara para el
Director: si Cerro Moro compra, Bahía se queda sin demos — ahora son 4 módulos, no 6.</strong> Recomendación: la
reposición de los kits de Bahía se dispara en el mismo pedido que la orden de compra, no después. <em>(Las 10 placas
de JLCPCB por USD 43,10 ya contemplan las de sobra para eso.)</em></p></div>
''')

# =================================================================== HOJA 14
hoja(u'''
<h2><span class="n">19</span>Qué es cada hito por dentro</h2>
<div class="sub">Las duraciones se cuentan <strong>en semanas desde la aceptación</strong>, no contra el calendario.
Los hitos pesados caen después de la semana 5 para no chocar con la parada de Dreyfus.</div>
<table class="compacta"><thead><tr><th style="width:17%">Hito (cliente)</th><th style="width:30%">Etapa interna</th>
<th class="num" style="width:8%">Desde</th><th class="num" style="width:8%">Hasta</th><th>Cómo se acepta</th></tr></thead><tbody>
<tr><td><strong>1</strong> — El equipo ya instalado con sus 3 sondas adentro y calibradas, rangos, primera alerta real</td>
<td>E0</td><td class="num gris">sem. 0</td><td class="num">sem. 2</td>
<td>Captura de la alerta en el celular + registro en nube + <strong>planilla de calibración con el offset de las 3
sondas de <code>REEFER_01_SCZ</code></strong></td></tr>
<tr><td><strong>2</strong> — Los 3 módulos y los 5 reefers reportando; nada se pierde, nada sobra</td>
<td>E1: buffer offline, alertas encoladas, alerta de sonda caída, vigía de equipo mudo, discriminador de bus +
histéresis, <strong>detección de sonda que se desvía de las otras del mismo reefer</strong>, <strong>segunda puerta y
segundo defrost con silenciado por reefer, un bus por reefer — en los tres módulos y en el repuesto</strong></td><td class="num gris">sem. 2</td><td class="num">sem. 5</td>
<td>Los 3 módulos montados con sus 15 sondas calibradas; desenchufar una sonda y que llegue la alarma; cortar la red
20 min sin perder lecturas; abrir una puerta 4 min y que avise; <strong>forzar el defrost de un reefer y verificar que
el que comparte módulo sigue alarmando</strong>; <strong>una semana sin falsas alarmas</strong></td></tr>
<tr><td><strong>3</strong> — Acceso seguro</td><td>E2: RLS cerrada, credencial por módulo, secretos fuera del binario,
revocar claves quemadas</td><td class="num gris">sem. 5</td><td class="num">sem. 10</td>
<td>Con la clave vieja no se escribe; los 3 módulos siguen reportando</td></tr>
<tr><td><strong>4</strong> — Actualización a distancia</td><td>E3: OTA con manifiesto inmutable</td>
<td class="num gris">sem. 10</td><td class="num">sem. 12</td>
<td>Tres actualizaciones seguidas por aire al primer intento, en todos los módulos</td></tr>
<tr><td><strong>5</strong> — Panel e informe</td><td>E4: usuarios de lectura, vista de los reefers (dos por módulo),
exportación con código, informe mensual automático, <strong>comando de relé desde el panel</strong></td><td class="num gris">sem. 12</td>
<td class="num">sem. 15</td><td>Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el
panel</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="nota"><p><strong>El hito 2 es el apretado</strong> <span class="neutro">(la semana sin falsas alarmas
arranca cuando los 3 módulos reportan, alrededor de la semana 4, y vence en la 5). Sin colchón — y con dos cuellos:
la fabricación de la PCB y el firmware doble, que ahora necesitan los tres.</span></p></div>

<div class="box"><p>Lo que hoy está roto y cada hito arregla (llave maestra en el binario, datos perdidos sin red,
umbral en 50 °C, equipo muerto que no avisa, OTA que entra 1 de 4) está en <code>AUDITORIA_HALLAZGOS.md</code>; no
cambió.</p></div>
''')

# =================================================================== HOJA 15
hoja(u'''
<h2><span class="n">20</span>La relación con Andrés — para que Matías decida</h2>
<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Lo que cambió</span><h3>De contacto en sitio a referidor de hecho — y ahora, co-diseñador</h3></div>
    <div class="cuerpo"><p>En la v1 Andrés era el contacto en sitio de un cliente y la regla era simple:
    <strong>ningún pago ni beneficio ligado a que su empleador compre</strong>. Ahora es él quien <strong>ofrece y
    presenta</strong> la propuesta a una tercera empresa que él elige, <strong>y quien armó la configuración final</strong>
    con la caja en la mano.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Lo que sigue vigente, sin discusión</span><h3>Si el comprador está bajo el Código de Conducta, no hay comisión</h3></div>
    <div class="cuerpo"><p>Si el comprador termina siendo la minera, o una contratista que opera bajo su Código de
    Conducta de Proveedores (que alcanza a proveedores <strong>y a sus subcontratistas</strong>), <strong>no hay
    comisión ni reconocimiento material</strong>. Y hay que ser honesto con la probabilidad: <strong>cualquier empresa
    que opere dentro del campamento está, casi seguro, bajo ese código.</strong></p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="nota"><p><strong>El conflicto de interés, escrito.</strong> <span class="neutro">Andrés trabaja adentro
(no sabemos todavía si es empleado de la minera o de una contratista — <strong>hay que preguntarlo</strong>), elige a
quién ofrecerle el sistema y lo presenta con la credibilidad de su puesto. Si cobra por eso, pasa de «el que trajo un
proveedor bueno» a «el que le vendió algo a la empresa de al lado y se llevó una parte». <strong>El costo de un
reconocimiento mal puesto sigue siendo mayor que el negocio.</strong></span></p></div>

<table class="compacta"><thead><tr><th style="width:20%">Opción</th><th style="width:26%">Qué es</th>
<th style="width:27%">A favor</th><th>En contra</th></tr></thead><tbody>
<tr><td><strong>1. Nada material, todo el reconocimiento no monetario</strong> <span class="soft det">status quo</span></td>
<td>Agradecer por escrito, darle el acceso y la hoja de una carilla para que quede bien adentro, nombrarlo como
contacto en sitio, contarle el caso como logro suyo — <strong>y la configuración como idea suya, porque lo es</strong></td>
<td>Cero riesgo. Es lo que él pidió («la gente de acá no lo vio»): quedar bien, no cobrar</td>
<td>Si el negocio crece por él y no recibe nada, el empuje puede enfriarse</td></tr>
<tr><td><strong>2. Referidor formal solo para leads AJENOS al campamento</strong> <span class="soft det">Bahía, Venado
Tuerto, futuros</span></td>
<td>Reconocimiento único equivalente a 1 mes de abono del cliente referido, pagado después del 3er abono cobrado;
<strong>excluye</strong> a la minera, sus contratistas y cualquier empresa del campamento; condicionado a que su
empleador lo permita</td>
<td>Es honesto, separa los mundos, y <strong>ya tiene un caso real: Venado Tuerto lo trajo él</strong></td>
<td>Hay que escribirlo y preguntarle si su empleador tiene política de actividades externas</td></tr>
<tr><td><strong>3. Reconocimiento en especie, fuera del negocio</strong></td>
<td>Un equipo Termovigía para uso propio, o capacitación, sin vínculo con ninguna compra</td>
<td>Barato, tangible</td>
<td>Si se da mientras Cerro Moro está en discusión, se lee igual que una comisión</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="cita"><p><strong>Recomendación honesta de @comercial:</strong> 1 ahora, 2 por escrito cuando Venado Tuerto
avance, y <strong>preguntarle a Andrés para quién trabaja y si su empresa tiene política de actividades
externas</strong> antes de ofrecerle cualquier cosa. La 3, nunca durante la negociación de Cerro Moro. <strong>No
decide él: decide Matías.</strong></p>
<p><strong>Lo bueno de esta vuelta:</strong> a Andrés le llega <strong>exactamente el sistema que él armó</strong>, con
sus tres frases adentro (un módulo para dos, la caja sobre la unión, un cable por reefer) y su medición de los 3 °C
como argumento. <strong>Lo que hay que cuidar:</strong> es el tercer presupuesto en cuatro días. Se compensa con que
esta vez el número <strong>baja</strong> y con que la razón es suya. Cuarta vuelta no hay: <strong>la próxima
conversación es de aceptación, no de configuración.</strong></p></div>
''')

# =================================================================== HOJA 16
hoja(u'''
<h2><span class="n">21</span>Lo que quedó abierto, antes de mandar</h2>
<div class="sub">20 pendientes. <strong>Ninguno es logística:</strong> hasta que no haya aceptación y anticipo no se
compra, no se arma y no se despacha nada.</div>
<table class="compacta"><thead><tr><th style="width:5%">&nbsp;</th><th>Pendiente</th><th style="width:20%">Quién decide</th></tr></thead><tbody>
<tr><td class="num">1</td><td><strong>Los números, con el mismo margen parejo (~32 %) de la v8.0:</strong> doble de
interior <strong>''' + m(P["doble_int"]) + u'''</strong> × 2 · doble de exterior <strong>''' + m(P["doble_ext"]) + u'''</strong> · repuesto <strong>''' + m(P["repuesto"]) + u'''</strong> · puesta en
marcha <strong>''' + m(P["puesta"]) + u'''</strong> (66 h) · <strong>inicial USD ''' + m(C["total"]) + u'''</strong> (v8.0: 5.000; −4 %) · abono <strong>''' + m(C["abono"]) + u'''/mes, sin
tocar</strong> · B = <strong>''' + m(C["b1"]) + u'''</strong> · anticipo 50 % = <strong>''' + m(C["anticipo"]) + u'''</strong>. Alternativa para sostener 5.000 en la hoja 9
(margen 36 %, desparejo). <strong>¿Van?</strong></td><td><strong>Matías</strong></td></tr>
<tr><td class="num">2</td><td><strong>Mandar el WhatsApp de la hoja 2 junto con el PDF.</strong> Dice «reemplaza al
anterior» sin cifra vieja: sirve tanto si Andrés tiene el de 4.600 como el de 5.000.</td><td><strong>Matías</strong></td></tr>
<tr><td class="num">3</td><td><strong>⚠ Decisión de placa, esta semana: poblar el 2.º bus 1-Wire de la Mini</strong>
(GPIO 18, pines reservados) para tener un bus por reefer, sin D2. Es la «más electrónica» que se le dijo a Andrés y
condiciona la PCB. <strong>Después de JLCPCB ya no se cambia.</strong></td><td>Matías / @esquematico</td></tr>
<tr><td class="num">4</td><td><strong>⚠ El firmware doble VOLVIÓ al camino crítico: lo necesitan los tres módulos.</strong>
@firmware da fecha de cierre y confirma que las 18 h de la hoja 10 alcanzan; si son más, salen del margen, no del
precio. Plan B parcial: cada doble arranca con un reefer. <strong>Avisar al Director.</strong></td><td>@firmware</td></tr>
<tr><td class="num">5</td><td><strong>Preguntarle a Andrés:</strong> cuál de los 4 de adentro está fuera de servicio
(define el par con un reefer activo), metros de la unión a la sonda más lejana de cada reefer, si el defrost es
12-24 V o contacto seco, si la red llega a los 3 puntos, y cómo midió los 3 °C.</td><td>Matías</td></tr>
<tr><td class="num">6</td><td><strong>⚠ El cuello de fabricación sigue:</strong> PCB Mini, despacho semana 4-5, hito 2
en la 7-8. O se corren los hitos en el PDF, o se pide la PCB ya (USD 43, con el 2.º bus decidido). <strong>Decisión
tuya, antes de firmar.</strong></td><td><strong>Matías</strong></td></tr>
<tr><td class="num">7</td><td><strong>Qué pasa con <code>REEFER_01_SCZ</code> en el hito 2:</strong> su reefer pasa al
doble de su par, sus 3 sondas calibradas se reaprovechan; el kit viejo queda como segundo respaldo en el campamento o
vuelve a Bahía como demo.</td><td>Matías</td></tr>
<tr><td class="num">8</td><td>El sexto reefer entra <strong>sin costo de equipo</strong> (el doble de su par ya trae
sus sondas) y sube el abono a 600. Está escrito así en el documento del cliente. <strong>¿Va así?</strong></td><td><strong>Matías</strong></td></tr>
<tr><td class="num">9</td><td>Compra de materiales: <strong>≈ $ 749.000 ≈ USD 490, estimado</strong> sobre el BOM rev A.
<strong>@hardware recuesta las 4 placas dobles con 2 buses (rev B)</strong> y confirma si el stock de 20 sondas y 10 reed
sirve. Reservados 3 ESP32 para las galgas de Dreyfus.</td><td>@hardware</td></tr>
<tr><td class="num">10</td><td><code>M9</code> vale $ 63.609 (ahora las 3 cajas de stock cubren justo los 3 gabinetes de
interior) y la etiqueta V/A de las fuentes $ 52.895: 10 minutos con un calibre, antes del pedido.</td><td>@hardware</td></tr>
<tr><td class="num">11</td><td><strong>Decisión de portfolio, no comercial:</strong> si Cerro Moro compra, Bahía se
queda sin demos — ahora son 4 módulos. Recomendación: reposición en el mismo pedido que la OC.</td><td><strong>Director</strong></td></tr>
<tr><td class="num">12</td><td><strong>Verificación cruzada entre sondas: hoy NO existe.</strong> Vendida en el hito 2. Con
3 °C reales entre puerta y fondo, tiene que comparar cada sonda contra su propia historia, no contra el promedio. Si no
se puede cumplir, sacar el punto 3 del bloque «por qué 3 sondas».</td><td>Matías / @firmware</td></tr>
<tr><td class="num">13</td><td><strong>Accionamiento del relé desde el panel: tampoco existe.</strong> Hito 5.</td><td>@firmware</td></tr>
<tr><td class="num">14</td><td>El sensor de puerta viene <strong>deshabilitado por defecto</strong>: que quede en la
orden de armado habilitarlo y probar puerta y defrost de <strong>los dos canales de los 4 módulos</strong>.</td><td>@firmware</td></tr>
<tr><td class="num">15</td><td>La sirena a USD 40 no deja margen: la BR300 sale USD 26 más su propia fuente de 12 V
porque el relé es contacto seco. <strong>Propongo USD 70 instalada, o baliza LED de 12 V.</strong></td><td>Matías</td></tr>
<tr><td class="num">16</td><td>La caja de exterior que ya está en el sitio es la prueba de campo, y de ella dependen
2 reefers: pedirle a Andrés una foto después del primer temporal.</td><td>Matías</td></tr>
<tr><td class="num">17</td><td><strong>Andrés:</strong> opción 1, 2 o 3 de la hoja anterior, y preguntarle para quién
trabaja. Y reconocerle la configuración como suya: lo es.</td><td><strong>Matías</strong></td></tr>
<tr><td class="num">18</td><td><strong>PDF:</strong> un solo documento de 2 páginas A4, marca Termovigía, sin logo
ajeno, sin «Para:», sin validez, sin material de gabinete, <strong>sin «cinco», sin «5 módulos», sin USD 260 ni ninguna
cuenta vieja</strong> — verificado por la guarda de <code>render_v7.py</code> sobre el texto del PDF.</td><td>@comercial · <strong>hecho</strong></td></tr>
<tr><td class="num">19</td><td>Monotributo vs. RI: se pregunta cuando la empresa tenga nombre.</td><td>Matías</td></tr>
<tr><td class="num">20</td><td><strong>Cuarta vuelta no hay.</strong> Tres presupuestos en cuatro días es el límite: si
aparece otro cambio de configuración, se contesta por teléfono y se ajusta después de la aceptación, no antes.</td><td><strong>Matías</strong></td></tr>
</tbody></table>
''')

# =================================================================== HOJA 17
hoja(u'''
<h2><span class="n">22</span>Fuentes consultadas</h2>
<ul class="lista">
  <li><strong>Configuración v9:</strong> WhatsApp de Andrés, 8-sep («con tres módulos solucionamos lo de Cerro Moro, un
  módulo para dos reefer; al estar juntos de a dos es fácil hacer la conexión; pongo la caja sobre la unión de los dos y
  saco las sondas»; «casi 3 °C entre la puerta y el fondo») y respuesta de Matías («3 es mucho mejor para calibración»;
  «rehago el presupuesto, queda más o menos lo mismo, porque le tengo que meter un poco más de electrónica adentro de
  la caja y programación»).</li>
  <li><strong>Un solo bus en la Mini y pines reservados para el 2.º:</strong> <code>frioseguro\\hardware\\mini\\PINOUT_MINI.md</code>
  (GPIO 4 bus DS18B20 hasta 6 sondas; 18 y 23 «quedan para un 2.º bus 1-Wire si hace falta»).</li>
  <li>Alcance del bus, pull-ups, tierras entre contenedores y límite prudente de 15 m:
  <code>frioseguro\\hardware\\ALCANCE_1WIRE.md</code> (@muestreador), §2.6.</li>
  <li><strong>Costos reales, gabinetes, PCB, plazos y margen:</strong> <code>frioseguro\\hardware\\mini\\BOM_CERRO_MORO.md</code>
  rev A (@hardware, 4-sep-2026) — §5.1 D2 rompe el bus a 25 m.</li>
  <li><strong>BOM de la placa:</strong> <code>frioseguro\\hardware\\mini\\BOM_MINI.md</code> rev A (@esquematico, 4-sep-2026).</li>
  <li><strong>Firmware de módulo doble:</strong> <code>frioseguro-v31\\firmware_modular\\VERIFICACION_V3.1_2026-09-04.md</code>,
  veredicto APTO CON CORRECCIONES, correcciones en curso.</li>
  <li>Estado real y auditoría: <code>ESTADO_HONESTO.md</code> · <code>AUDITORIA_HALLAZGOS.md</code>.</li>
  <li>Qué hace hoy el firmware con sondas, puerta, relé y defrost (leído el 3-sep-2026):
  <code>firmware_revival/sondas.h</code> línea 31 · <code>config.h</code> 67-150 · <code>.ino</code> 369-375, 483-488,
  804-944 · <code>comandos_nube.h</code> (sin comando de relé).</li>
  <li>Contrato base: <code>MATI-HQ\\comercial\\CONTRATO_TERMOVIGIA_v4.md</code>.</li>
  <li><strong>Dólar BNA vendedor billete $ 1.530, 8-sep-2026 09:50</strong> (bna.com.ar/Personas). Precios de canalización,
  1-Wire AN148, testo Saveris 2-T2, novillo INMAG, Supabase Pro y el Código de Conducta de Proveedores: enlaces
  conservados en la v5.2 del archivo fuente (historial de git).</li>
</ul>
''')

# =================================================================== salida
HTML = (u'<!DOCTYPE html>\n<html lang="es-AR">\n<head>\n<meta charset="utf-8">\n'
        u'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        u'<title>INTERNO — Cerro Moro v9.0: 3 módulos dobles, la configuración de Andrés y los pendientes</title>\n'
        u'<link rel="stylesheet" href="estilo.css">\n</head>\n<body>\n<div class="doc">\n\n'
        + u'\n'.join(HOJAS) + u'\n</div>\n</body>\n</html>\n')

if __name__ == "__main__":
    io.open(os.path.join(AQUI, SALIDA), "w", encoding="utf-8").write(HTML)
    print("escrito %s (%d hojas)" % (SALIDA, len(HOJAS)))
