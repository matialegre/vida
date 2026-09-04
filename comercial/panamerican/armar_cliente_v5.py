# -*- coding: utf-8 -*-
"""Arma el UNICO presupuesto del cliente (v5, 4-sep-2026).

v4 tenia dos presupuestos gemelos y por eso habia una plantilla con dos diccionarios.
En la v5 el Presupuesto 2 se cayo (la cuenta del cano lo dio vuelta): queda UN documento.
Se conserva el generador igual, con UN diccionario, porque el copy vive separado del
armado y asi una correccion de @comercial se aplica sin tocar el HTML.

Copy: PROPUESTA_PANAMERICAN_CERRO_MORO.md (v5, @comercial), PARTE 1 (y la columna de
aceptacion de la PARTE 4, reescrita sin nombres internos). Nada inventado.
Salida: PRESUPUESTO_CERRO_MORO.html
"""
import io, os

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = r"C:\Proyectos\frioseguro\marca\logo_horizontal.svg"
FECHA = "4 de septiembre de 2026"

ESCUDO = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Termovigia">'
          '<path d="M50 4 L92 18 V50 C92 74.5 74 90.5 50 97 C26 90.5 8 74.5 8 50 V18 Z" fill="#0E4F66"/>'
          '<path d="M20 68 L40 68 L56 40 L62 40" fill="none" stroke="#FFFFFF" stroke-width="8.5" '
          'stroke-linecap="round" stroke-linejoin="round"/>'
          '<circle cx="75" cy="40" r="9" fill="#FFFFFF"/><circle cx="75" cy="40" r="5" fill="#C4291C"/></svg>')

# ------------------------------------------------------------------ contenido

D = dict(
    archivo="PRESUPUESTO_CERRO_MORO",
    ref="PROP-CM-2026-09-04",
    titulo="Un equipo por reefer",
    bajada="5 equipos, uno en cada reefer",
    lugar="Campamento Cerro Moro (Santa Cruz) &mdash; 5 reefers en servicio",

    que_es="""<p>Un equipo sobre cada reefer, cinco en total, que vigila la temperatura las 24 horas y avisa
al celular cuando algo se sale de rango. Cada equipo es independiente: <strong>no hay un solo cable entre
contenedores y ning&uacute;n reefer depende del de al lado</strong>.</p>
<p>Hoy ya hay un equipo instalado y reportando desde el campamento: se puede ver en vivo en el celular antes de decidir nada.
<strong>Mientras se eval&uacute;a esta propuesta ese equipo sigue midiendo y reportando</strong>, y el panel se
puede abrir en cualquier momento: los resultados se muestran durante el proceso, no despu&eacute;s.</p>""",

    que_hace=[
        "Mide la temperatura de cada reefer todo el tiempo, con hasta <strong>4 sondas por reefer</strong>, y la guarda en la nube (12 meses de historial).",
        "Avisa al celular de las personas que se definan cuando un reefer se sale del rango acordado por m&aacute;s tiempo del acordado.",
        "Avisa si <strong>queda la puerta abierta</strong> m&aacute;s de los minutos que se definan (sensor magn&eacute;tico incluido en cada reefer).",
        "Avisa cuando una sonda se desconecta o cuando un equipo deja de reportar.",
        "<strong>No molesta durante el descongelamiento:</strong> el equipo toma la se&ntilde;al de defrost del propio reefer y calla las alarmas mientras dura el ciclo, para que nadie aprenda a ignorar los avisos.",
        "Puede <strong>accionar una sirena o baliza</strong> en el pasillo: cada equipo trae 2 salidas a rel&eacute; libres para eso.",
        "Genera solo el <strong>registro mensual de temperatura por reefer</strong>, para tener el papel cuando alguien lo pide.",
        "Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada m&aacute;s.",
    ],

    sondas=[
        "<strong>Un reefer no tiene &laquo;una&raquo; temperatura.</strong> Cerca de la puerta, cerca del evaporador, arriba y abajo puede haber varios grados de diferencia. Con una sonda se mide un punto y se supone el resto; con cuatro se mide <strong>el peor punto</strong>, que es el que decide si la carga se arruin&oacute;. En una auditor&iacute;a lo que vale es el peor punto, no el promedio.",
        "<strong>Si una sonda falla, el reefer sigue vigilado.</strong> En un sistema cuyo trabajo es avisar, quedarse ciego es la peor falla posible: con una sola sonda cualquier problema deja el reefer sin vigilancia hasta que alguien viaje 1.500 km.",
        "<strong>Las sondas se controlan entre s&iacute;.</strong> Si una empieza a desviarse respecto de las otras tres, se detecta y se avisa. Con una sola sonda, una deriva de 2 o 3 &deg;C es invisible: el registro parece perfecto y est&aacute; mintiendo. <em>(Se entrega en el hito 2.)</em>",
        "<strong>Se calibran las cuatro contra la misma referencia</strong> (ba&ntilde;o de hielo) y las diferencias quedan registradas. Eso es lo que convierte el registro en algo defendible ante un auditor.",
    ],

    instala="""<p>Cinco equipos, uno por reefer, cada uno en un gabinete apto para intemperie con su fuente,
<strong>4 sondas, sensor magn&eacute;tico de puerta, 2 salidas a rel&eacute; y entrada de defrost</strong>,
m&aacute;s un kit de repuesto que queda en el campamento.</p>
<p>El montaje lo hace personal del campamento con los equipos preconfigurados desde Bah&iacute;a Blanca y
gu&iacute;a por videollamada: por eso esta propuesta no tiene l&iacute;nea de instalaci&oacute;n ni
vi&aacute;ticos.</p>""",

    banco="""<strong>Cada equipo se prueba individualmente antes de viajar.</strong> Los equipos no salen de una
l&iacute;nea de montaje: <strong>se arman y se verifican uno por uno en banco de prueba</strong> &mdash;las 4
sondas leyendo, la puerta, la se&ntilde;al de defrost y las dos salidas de alarma&mdash; y reci&eacute;n
ah&iacute; se despachan. Para un lote que va a quedar a 1.500 km del proveedor, esa verificaci&oacute;n
unitaria es la diferencia entre un equipo que llega andando y uno que hay que diagnosticar por
tel&eacute;fono.""",

    cond_titulo="Condiciones de instalaci&oacute;n: ninguna.",
    cond="""Cada equipo se monta sobre su propio reefer y todo el cableado queda adentro de ese contenedor:
<strong>no hay cable entre reefers, ni canalizaci&oacute;n, ni obra, ni condici&oacute;n de
distancia.</strong>""",
    cond_extra="""<em>Se evalu&oacute; tambi&eacute;n un equipo cada dos reefers: con los 20-25 metros que hay
entre uno y otro habr&iacute;a que montar ca&ntilde;o r&iacute;gido en todo el recorrido, y esa obra cuesta
m&aacute;s que los equipos que se ahorrar&iacute;an &mdash; por eso la propuesta va con un equipo por
reefer.</em>""",

    sexto_titulo="El sexto reefer, con el precio ya puesto.",
    sexto="""Esta propuesta cubre los <strong>5 reefers hoy en servicio</strong>. Cuando el sexto vuelva a
funcionar se le suma su equipo <strong>al mismo precio unitario de esta propuesta (USD 520)</strong>, con las
mismas 4 sondas, puerta, salidas y defrost, y el servicio mensual pasa de USD 500 a USD 600: <strong>+USD 520 el equipo y +USD 100/mes</strong>. Queda dicho
ac&aacute; para no tener que renegociar nada el d&iacute;a que pase.""",

    hitos=[
        ("1",
         "El equipo que ya est&aacute; instalado, con sus 4 sondas dentro del reefer, calibradas contra una misma referencia, rangos definidos y primera alerta real recibida en el celular",
         "Captura de la alerta en el celular, el registro en la nube y la planilla de calibraci&oacute;n con el desv&iacute;o de las 4 sondas.",
         "a las 2 semanas de iniciado"),
        ("2",
         "Los 5 equipos montados y reportando; ning&uacute;n dato ni aviso se pierde si se corta la red; aviso de equipo que deja de reportar; <strong>aviso de sonda que se desv&iacute;a de las otras tres</strong>; puerta y defrost validados en campo; una semana entera sin falsas alarmas",
         "Desenchufar una sonda y que llegue la alarma; cortar la red 20 minutos sin perder lecturas; abrir una puerta 4 minutos y que avise; forzar un descongelamiento y que <strong>no</strong> avise.",
         "a las 5 semanas"),
        ("3",
         "Acceso seguro: cada equipo y cada usuario con su propia credencial",
         "Con una credencial dada de baja ya no se puede escribir, y todos los equipos siguen reportando.",
         "a las 10 semanas"),
        ("4",
         "Actualizaciones de los equipos a distancia, sin tocarlos",
         "Tres actualizaciones seguidas por aire, al primer intento, en todos los equipos.",
         "a las 12 semanas"),
        ("5",
         "Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma desde el panel e informe mensual descargable",
         "Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el panel.",
         "a las 15 semanas"),
    ],

    costos=[
        ("Equipo de monitoreo por reefer",
         "Equipo, gabinete, fuente, 4 sondas, sensor de puerta, 2 salidas a rel&eacute;, entrada de defrost. "
         "Probado individualmente en banco.",
         "5 &times; 520", "2.600"),
        ("Kit de repuestos en sitio",
         "1 equipo completo armado y probado + 4 sondas + 1 sensor de puerta.",
         "1", "340"),
        ("Puesta en marcha y ajuste en sitio",
         "Los 5 hitos de arriba, con su plazo. No se facturan aparte: est&aacute;n incluidos en el precio.",
         "5 hitos", "1.600"),
    ],
    total="4.540",
    abono="500 / mes",

    pago_equipos="USD 4.540 <small>50 % con la OC, 50 % contra instalaci&oacute;n</small>",
    pago_inicial_a="USD 4.540",
    pago_inicial_b="USD 9.940<small>equipos + 12 meses de servicio, con 10 % de descuento sobre el servicio</small>",
    mensual_a="USD 500<small>USD 100 por reefer, completo desde el primer mes</small>",
    mensual_b="&mdash;<small>el primer a&ntilde;o; renovaci&oacute;n anual USD 5.400</small>",
    doce_a="10.540", doce_b="9.940",
    veinti_a="16.540", veinti_b="15.340",
    bna="USD 4.540 &asymp; $ 6.968.900 &middot; USD 500 &asymp; $ 767.500 &middot; USD 9.940 &asymp; $ 15.257.900",

    saber="""El sistema avisa; no garantiza la mercader&iacute;a ni reemplaza la revisi&oacute;n del reefer. Sin
energ&iacute;a en el equipo no mide: lo que avisa en ese caso es la nube, diciendo que dej&oacute; de reportar.
La entrada de defrost necesita que el reefer tenga una se&ntilde;al o un contacto accesible; si alguno no lo
tiene, esa entrada queda libre y el resto funciona igual. Las 2 salidas a rel&eacute; vienen en el equipo; la
sirena o baliza que se conecte no est&aacute; incluida. Cada equipo necesita llegar a la red del campamento
desde su propio reefer. Los plazos de los hitos 1 y 2 suponen que el montaje en sitio se hace dentro de la
ventana prevista, que depende de personal del campamento.""",
)

# ------------------------------------------------------------------ plantilla


def pie(d, n, total):
    return ('<div class="pie">\n'
            '  <span class="marca">%s <b>Termovig&iacute;a</b> &middot; Bah&iacute;a Blanca</span>\n'
            '  <span class="cod">Presupuesto &middot; un equipo por reefer &middot; Cerro Moro &middot; Precios en USD</span>\n'
            '  <span class="npag">%d / %d</span>\n'
            '</div>\n' % (ESCUDO, n, total))


def armar(d, logo_svg):
    h = []
    a = h.append
    a('<!DOCTYPE html>\n<html lang="es-AR">\n<head>\n<meta charset="utf-8">\n'
      '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
      '<title>Termovig&iacute;a &mdash; Presupuesto: un equipo por reefer &mdash; 5 reefers, Cerro Moro</title>\n'
      '<link rel="stylesheet" href="estilo.css">\n</head>\n<body>\n<div class="doc">\n')

    # ---------------- HOJA 1
    a('<section class="hoja compacta presu">\n')
    a('<div class="cabecera">\n  <div class="logo">%s</div>\n' % logo_svg)
    a('  <div class="sello"><b>Presupuesto</b>%s<br>Ref. %s</div>\n</div>\n' % (FECHA, d["ref"]))

    a('<div class="rotulo">\n'
      '  <div class="cifra-rot">5</div>\n'
      '  <div class="txt"><span class="k">Monitoreo de temperatura de reefers</span>'
      '<h1>%s</h1><span class="b">%s &middot; %s</span></div>\n'
      '</div>\n' % (d["titulo"], d["bajada"], d["lugar"]))

    a('<h2><span class="n">01</span>Qu&eacute; es</h2>\n<div class="doscol">' + d["que_es"] + '</div>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">02</span>Qu&eacute; hace</h2>\n')
    a('<ul class="lista chica doscol">\n')
    for li in d["que_hace"]:
        a('  <li>%s</li>\n' % li)
    a('</ul>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">03</span>Por qu&eacute; 4 sondas por reefer y no una</h2>\n')
    a('<div class="sub">Es la diferencia entre una instalaci&oacute;n seria y un term&oacute;metro con WiFi.</div>\n')
    a('<div class="qgrid">\n')
    for i, s in enumerate(d["sondas"], 1):
        a('<div class="qitem"><div class="n">%d</div><div class="q">%s</div></div>\n' % (i, s))
    a('</div>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">04</span>Qu&eacute; se instala</h2>\n<div class="doscol">' + d["instala"] + '</div>\n')
    a('<div class="sep-ch"></div>\n')
    a('<div class="box"><p>%s</p></div>\n' % d["banco"])
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">05</span>Condiciones de instalaci&oacute;n y ampliaci&oacute;n</h2>\n')
    a('<div class="cond ok"><p><strong class="tit">%s</strong> %s</p><p class="ajuste">%s</p></div>\n'
      % (d["cond_titulo"], d["cond"], d["cond_extra"]))
    a('<div class="cond sexto"><p><strong class="tit">%s</strong> %s</p></div>\n'
      % (d["sexto_titulo"], d["sexto"]))

    a('<div class="aire"></div>\n')
    a(pie(d, 1, 2))
    a('</section>\n\n')

    # ---------------- HOJA 2
    a('<section class="hoja compacta presu">\n')

    a('<h2><span class="n">06</span>Puesta en marcha y ajuste en sitio</h2>\n')
    a('<div class="sub">15 semanas, por hitos. Son compromiso de entrega: no se '
      'facturan aparte, est&aacute;n incluidos en el precio. <strong>Los plazos se cuentan desde el inicio, y el inicio es la aceptaci&oacute;n de esta propuesta con su anticipo.</strong></div>\n')
    a('<table class="compacta"><thead><tr><th style="width:7%">Hito</th>'
      '<th>Qu&eacute; queda funcionando &middot; c&oacute;mo se comprueba</th>'
      '<th class="num" style="width:18%">Plazo</th></tr></thead><tbody>\n')
    for n, t, acep, f in d["hitos"]:
        a('<tr><td class="num">%s</td><td>%s<span class="soft det"><strong>Se acepta con:</strong> %s</span></td>'
          '<td class="num">%s</td></tr>\n' % (n, t, acep, f))
    a('</tbody></table>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">07</span>Qu&eacute; cuesta</h2>\n')
    a('<table class="compacta precios"><thead><tr><th>Concepto</th>'
      '<th class="num" style="width:13%">Unid.</th><th class="num" style="width:15%">USD</th></tr></thead><tbody>\n')
    for tit, det, uni, usd in d["costos"]:
        a('<tr><td><strong>%s</strong><span class="soft det">%s</span></td>'
          '<td class="num gris">%s</td><td class="num">%s</td></tr>\n' % (tit, det, uni, usd))
    a('<tr class="total"><td colspan="2"><strong>Total equipos y puesta en marcha</strong></td>'
      '<td class="num">%s</td></tr>\n' % d["total"])
    a('<tr class="total"><td colspan="2"><strong>Servicio mensual</strong> <span class="soft">&mdash; USD 100 por reefer '
      'por mes, 5 reefers: nube, alertas, soporte, reposici&oacute;n sin cargo, informe mensual</span></td>'
      '<td class="num">%s</td></tr>\n' % d["abono"])
    a('</tbody></table>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">08</span>C&oacute;mo se paga</h2>\n')
    a('<div class="sub"><strong>50 % con la orden de compra</strong> (anticipo de materiales) y '
      '<strong>50 % contra los equipos instalados y reportando</strong>. El servicio mensual arranca con el '
      'primer equipo andando.</div>\n')
    a('<table class="abc dos"><thead><tr><th></th>'
      '<th><span class="letra">A</span><span class="nom">Equipos + servicio mensual</span></th>'
      '<th><span class="letra">B</span><span class="nom">Anual adelantado</span></th></tr></thead><tbody>\n')
    a('<tr><th>Para qui&eacute;n</th><td>Compra activos y paga el servicio mes a mes</td>'
      '<td>Tiene presupuesto de inversi&oacute;n y no quiere 12 facturas</td></tr>\n')
    a('<tr><th>Equipos y puesta en marcha</th><td class="usd">%s</td><td>Incluidos</td></tr>\n' % d["pago_equipos"])
    a('<tr><th>Pago inicial total</th><td class="usd">%s</td><td class="usd">%s</td></tr>\n'
      % (d["pago_inicial_a"], d["pago_inicial_b"]))
    a('<tr><th>Mensual</th><td class="usd">%s</td><td class="usd">%s</td></tr>\n'
      % (d["mensual_a"], d["mensual_b"]))
    a('<tr><th>Los equipos</th><td>Son del cliente</td><td>Son del cliente</td></tr>\n')
    a('<tr class="tot doce"><th>Total a 12 meses <span class="u">USD</span></th><td>%s</td><td>%s</td></tr>\n'
      % (d["doce_a"], d["doce_b"]))
    a('<tr class="tot"><th>Total a 24 meses <span class="u">USD</span></th><td>%s</td><td>%s</td></tr>\n'
      % (d["veinti_a"], d["veinti_b"]))
    a('</tbody></table>\n')
    a('<p class="tabla-pie">Facturaci&oacute;n en d&oacute;lares estadounidenses. De abonarse en pesos, se toma '
      'el tipo de cambio vendedor del Banco de la Naci&oacute;n Argentina de la fecha de pago. '
      'Referencia al 4-sep-2026 (BNA vendedor $ 1.535): %s.</p>\n' % d["bna"])
    a('<div class="sep-ch"></div>\n')

    a('<div class="grid2 cierre">\n'
      '  <div class="box"><p><strong>Incluido en el servicio mensual</strong><br>Nube con 12 meses de historial '
      '&middot; alertas por temperatura, puerta abierta, sonda ca&iacute;da y equipo mudo &middot; '
      'reposici&oacute;n sin cargo de cualquier equipo o sonda fallada, env&iacute;o incluido &middot; '
      'actualizaciones &middot; soporte por WhatsApp y tel&eacute;fono el mismo d&iacute;a h&aacute;bil '
      '&middot; informe mensual por reefer.</p></div>\n'
      '  <div class="nota azul"><p><strong>Lo que hay que saber</strong><br><span class="neutro">%s</span></p></div>\n'
      '</div>\n' % d["saber"])

    a('<div class="aire grande"></div>\n')
    a('<div class="contacto">\n'
      '  <div class="cta">Se puede ver en vivo antes de decidir.<span>Contacto en sitio: '
      'Andr&eacute;s Leiva Chavez</span></div>\n'
      '  <div class="line">Mat&iacute;as Alegre &middot; Termovig&iacute;a &middot; Bah&iacute;a Blanca<br>'
      '2920 59-1019 &middot; alegrematias08@gmail.com</div>\n</div>\n')
    a(pie(d, 2, 2))
    a('</section>\n\n</div>\n</body>\n</html>\n')
    return "".join(h)


if __name__ == "__main__":
    logo = io.open(LOGO, encoding="utf-8").read()
    p = os.path.join(AQUI, D["archivo"] + ".html")
    io.open(p, "w", encoding="utf-8").write(armar(D, logo))
    print("escrito", D["archivo"] + ".html")
