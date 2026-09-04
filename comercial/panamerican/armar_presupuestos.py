# -*- coding: utf-8 -*-
"""Arma los DOS presupuestos del cliente (v4, 3-sep-2026) desde UNA sola plantilla.

Por que un generador y no dos HTML a mano: los dos documentos tienen que ser GEMELOS
(mismas secciones, mismo orden, misma posicion en la hoja). Si se editan a mano se
desincronizan a la segunda correccion. Aca la estructura es una sola y lo unico que
cambia es el diccionario de contenido de cada uno.

Copy: PROPUESTA_PANAMERICAN_CERRO_MORO.md (v4, @comercial), Partes 1 y 2. Nada inventado.
Salida: PRESUPUESTO_1_UNO_POR_REEFER.html y PRESUPUESTO_2_UNO_CADA_DOS.html
"""
import io, os

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = r"C:\Proyectos\frioseguro\marca\logo_horizontal.svg"
FECHA = "3 de septiembre de 2026"

ESCUDO = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Termovigia">'
          '<path d="M50 4 L92 18 V50 C92 74.5 74 90.5 50 97 C26 90.5 8 74.5 8 50 V18 Z" fill="#0E4F66"/>'
          '<path d="M20 68 L40 68 L56 40 L62 40" fill="none" stroke="#FFFFFF" stroke-width="8.5" '
          'stroke-linecap="round" stroke-linejoin="round"/>'
          '<circle cx="75" cy="40" r="9" fill="#FFFFFF"/><circle cx="75" cy="40" r="5" fill="#C4291C"/></svg>')

# ------------------------------------------------------------------ contenido

P1 = dict(
    archivo="PRESUPUESTO_1_UNO_POR_REEFER",
    num="1",
    ref="PROP-CM-P1-2026-09-03",
    titulo="Un equipo por reefer",
    bajada="6 equipos, uno en cada reefer",
    lugar="6 reefers, campamento Cerro Moro (Santa Cruz)",

    que_es="""<p>Un equipo sobre cada reefer, seis en total, que vigila la temperatura las 24 horas y avisa
al celular cuando algo se sale de rango. Cada equipo es independiente: <strong>no hay un solo cable entre
contenedores y ningún reefer depende del de al lado</strong>. Hoy ya hay un equipo instalado y reportando
desde el campamento: se puede ver en vivo en el celular antes de decidir nada.</p>""",

    que_hace_intro="",
    que_hace=[
        "Mide la temperatura de cada reefer todo el tiempo, con hasta <strong>4 sondas por reefer</strong>, y la guarda en la nube (12 meses de historial).",
        "Avisa al celular de las personas que se definan cuando un reefer se sale del rango acordado por más tiempo del acordado.",
        "Avisa si <strong>queda la puerta abierta</strong> más de los minutos que se definan (sensor magnético incluido en cada reefer).",
        "Avisa cuando una sonda se desconecta o cuando un equipo deja de reportar.",
        "<strong>No molesta durante el descongelamiento:</strong> el equipo toma la señal de defrost del propio reefer y calla las alarmas mientras dura el ciclo, para que nadie aprenda a ignorar los avisos.",
        "Puede <strong>accionar una sirena o baliza</strong> en el pasillo: cada equipo trae 2 salidas a relé libres para eso.",
        "Genera solo el <strong>registro mensual de temperatura por reefer</strong>, para tener el papel cuando alguien lo pide.",
        "Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada más.",
    ],

    sondas=[
        "<strong>Un reefer no tiene «una» temperatura.</strong> Cerca de la puerta, cerca del evaporador, arriba y abajo puede haber varios grados de diferencia. Con una sonda se mide un punto y se supone el resto; con cuatro se mide <strong>el peor punto</strong>, que es el que decide si la carga se arruinó. En una auditoría lo que vale es el peor punto, no el promedio.",
        "<strong>Si una sonda falla, el reefer sigue vigilado.</strong> En un sistema cuyo trabajo es avisar, quedarse ciego es la peor falla posible: con una sola sonda cualquier problema deja el reefer sin vigilancia hasta que alguien viaje 1.500 km.",
        "<strong>Las sondas se controlan entre sí.</strong> Si una empieza a desviarse respecto de las otras tres, se detecta y se avisa. Con una sola sonda, una deriva de 2 o 3 °C es invisible: el registro parece perfecto y está mintiendo. <em>(Se entrega en el hito 2.)</em>",
        "<strong>Se calibran las cuatro contra la misma referencia</strong> (baño de hielo) y las diferencias quedan registradas. Eso es lo que convierte el registro en algo defendible ante un auditor.",
    ],

    instala="""<p>Seis equipos, uno por reefer, cada uno en un gabinete apto para intemperie con su fuente,
<strong>4 sondas, sensor magnético de puerta, 2 salidas a relé y entrada de defrost</strong>, más un kit de
repuesto que queda en el campamento.</p>
<p>El montaje lo hace personal del campamento con los equipos preconfigurados desde Bahía Blanca y guía por
videollamada: por eso esta propuesta no tiene línea de instalación ni viáticos.</p>""",

    cond_clase="ok",
    cond_titulo="Sin condiciones.",
    cond="""<strong>No hay cable entre reefers, ni canalización, ni obra, ni condiciones de distancia</strong>:
cada equipo se monta en su propio contenedor y todo el cableado queda adentro de ese reefer.""",
    cond_extra="",

    hitos=[
        ("1", "Las 4 sondas dentro de cada reefer, calibradas contra una misma referencia, rangos definidos, primera alerta real recibida en el celular", "2"),
        ("2", "Ningún dato ni aviso se pierde si se corta la red; aviso de equipo que deja de reportar; <strong>aviso de sonda que se desvía de las otras tres</strong>; puerta y defrost validados en campo; una semana entera sin falsas alarmas", "6"),
        ("3", "Acceso seguro: cada equipo y cada usuario con su propia credencial", "11"),
        ("4", "Actualizaciones de los equipos a distancia, sin tocarlos", "13"),
        ("5", "Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma desde el panel e informe mensual descargable", "15"),
    ],

    costos=[
        ("Equipo de monitoreo por reefer",
         "Equipo, gabinete, fuente, 4 sondas, sensor de puerta, 2 salidas a relé, entrada de defrost. Probado en banco.",
         "6 × 480", "2.880"),
        ("Cable y canalización entre reefers",
         "Cada equipo se monta en su propio reefer: no hay cable de un contenedor a otro.",
         "no lleva", "0"),
        ("Kit de repuestos en sitio",
         "1 equipo completo armado y probado + 4 sondas + 1 sensor de puerta.",
         "1", "340"),
        ("Puesta en marcha y ajuste en sitio",
         "Los 5 hitos de arriba, con fecha. No se facturan aparte: están incluidos en el precio.",
         "5 hitos", "1.700"),
    ],
    total="4.920",
    abono="250 / mes",

    pago_equipos="USD 4.920 <small>50 % con la OC, 50 % contra instalación</small>",
    pago_inicial_a="USD 4.920",
    pago_inicial_b="USD 7.130<small>equipos + 12 meses, con 10 % de descuento</small>",
    doce_a="7.545", doce_b="7.130",
    veinti_a="10.545", veinti_b="9.830",
    bna="USD 4.920 &asymp; $ 7.552.200 &middot; USD 250 &asymp; $ 383.750 &middot; USD 7.130 &asymp; $ 10.944.550",

    saber="""El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en
el equipo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. La entrada de defrost
necesita que el reefer tenga una señal o un contacto accesible; si alguno no lo tiene, esa entrada queda libre
y el resto funciona igual. Las 2 salidas a relé vienen en el equipo; la sirena o baliza que se conecte no está
incluida. Cada equipo necesita llegar a la red del campamento desde su propio reefer.""",
)

P2 = dict(
    archivo="PRESUPUESTO_2_UNO_CADA_DOS",
    num="2",
    ref="PROP-CM-P2-2026-09-03",
    titulo="Un equipo cada dos reefers",
    bajada="3 equipos, cada uno atiende dos reefers contiguos",
    lugar="6 reefers, campamento Cerro Moro (Santa Cruz)",

    que_es="""<p>Tres equipos que vigilan la temperatura de los seis reefers del campamento las 24 horas y
avisan al celular cuando algo se sale de rango. Cada equipo atiende <strong>dos reefers contiguos</strong>,
con cuatro sondas dentro de cada uno. Hoy ya hay un equipo instalado y reportando desde el campamento: se
puede ver en vivo en el celular antes de decidir nada.</p>""",

    que_hace_intro="Lo mismo que el Presupuesto 1, reefer por reefer:",
    que_hace=[
        "Mide la temperatura de cada reefer todo el tiempo, con hasta <strong>4 sondas por reefer</strong>, y la guarda en la nube (12 meses de historial).",
        "Avisa al celular de las personas que se definan cuando un reefer se sale del rango acordado por más tiempo del acordado.",
        "Avisa si <strong>queda la puerta abierta</strong> más de los minutos que se definan (sensor magnético en cada reefer).",
        "Avisa cuando una sonda se desconecta o cuando un equipo deja de reportar.",
        "<strong>No molesta durante el descongelamiento:</strong> toma la señal de defrost de cada reefer y calla las alarmas mientras dura el ciclo.",
        "Puede <strong>accionar una sirena o baliza</strong>: cada equipo trae 2 salidas a relé libres, una por reefer.",
        "Genera solo el <strong>registro mensual de temperatura por reefer</strong>.",
        "Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada más.",
    ],

    sondas=[
        "<strong>Un reefer no tiene «una» temperatura.</strong> Cerca de la puerta, cerca del evaporador, arriba y abajo puede haber varios grados de diferencia. Con una sonda se mide un punto y se supone el resto; con cuatro se mide <strong>el peor punto</strong>, que es el que decide si la carga se arruinó. En una auditoría lo que vale es el peor punto, no el promedio.",
        "<strong>Si una sonda falla, el reefer sigue vigilado.</strong> Quedarse ciego es la peor falla posible en un sistema cuyo trabajo es avisar.",
        "<strong>Las sondas se controlan entre sí.</strong> Si una empieza a desviarse respecto de las otras tres, se detecta y se avisa. Con una sola sonda, una deriva de 2 o 3 °C es invisible: el registro parece perfecto y está mintiendo. <em>(Se entrega en el hito 2.)</em>",
        "<strong>Se calibran las cuatro contra la misma referencia</strong> (baño de hielo) y las diferencias quedan registradas: eso es lo que hace defendible el registro ante un auditor.",
    ],

    instala="""<p>Tres equipos, cada uno en un gabinete apto para intemperie con su fuente, atendiendo
<strong>dos reefers contiguos</strong>: 4 sondas, sensor magnético de puerta, una salida a relé y entrada de
defrost <strong>para cada uno de los dos reefers</strong>. Más un kit de repuesto que queda en el campamento.
El cable de sondas que va del equipo al reefer vecino <strong>se canaliza por piso o bandeja, nunca aéreo</strong>,
y esa canalización está incluida en el precio.</p>
<p>El montaje lo hace personal del campamento con los equipos preconfigurados desde Bahía Blanca y guía por
videollamada: por eso esta propuesta no tiene línea de instalación ni viáticos.</p>""",

    cond_clase="aviso",
    cond_titulo="La condición de este presupuesto, sin letra chica.",
    cond="""Los dos reefers de cada par tienen que estar <strong>contiguos</strong>, con el cable
<strong>canalizado por piso o bandeja (nunca aéreo)</strong> y <strong>no más de 15 metros</strong> entre uno
y otro. El porqué en una línea: el cable que une el equipo con las sondas es un bus de sensores digitales, y
cuanto más largo y más cargado, más riesgo de lecturas intermitentes.""",
    cond_extra="""<strong>Si algún par no cumple, ese par se resuelve con dos equipos simples (uno por reefer,
sin cable entre contenedores) por USD 110 más.</strong> Está dicho acá para no renegociar nada después: el
precio de la corrección ya está puesto.""",

    hitos=[
        ("1", "Las 4 sondas dentro de cada reefer, calibradas contra una misma referencia, rangos definidos, primera alerta real recibida en el celular. <strong>La primera semana de medición sirve además de verificación del cable entre los dos reefers de cada par</strong>", "2"),
        ("2", "Ningún dato ni aviso se pierde si se corta la red; aviso de equipo que deja de reportar; <strong>aviso de sonda que se desvía de las otras tres</strong>; puertas y defrost de los dos reefers validados en campo; una semana entera sin falsas alarmas", "6"),
        ("3", "Acceso seguro: cada equipo y cada usuario con su propia credencial", "11"),
        ("4", "Actualizaciones de los equipos a distancia, sin tocarlos", "13"),
        ("5", "Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma desde el panel e informe mensual descargable", "15"),
    ],

    costos=[
        ("Equipo de monitoreo para 2 reefers",
         "Equipo, gabinete, fuente, 8 sondas (4 por reefer), 2 sensores de puerta, 2 salidas a relé, 2 entradas de defrost. Probado en banco con el cable definitivo.",
         "3 × 790", "2.370"),
        ("Cable y canalización entre los dos reefers de cada par",
         "Caño galvanizado, curvas, grampas, caja de paso y cable exterior. Por piso o bandeja, nunca aéreo.",
         "3 × 60", "180"),
        ("Kit de repuestos en sitio",
         "1 equipo completo armado y probado + 4 sondas + 1 sensor de puerta.",
         "1", "420"),
        ("Puesta en marcha y ajuste en sitio",
         "Los 5 hitos de arriba, con fecha. No se facturan aparte: están incluidos en el precio.",
         "5 hitos", "1.800"),
    ],
    total="4.770",
    abono="250 / mes",

    pago_equipos="USD 4.770 <small>50 % con la OC, 50 % contra instalación</small>",
    pago_inicial_a="USD 4.770",
    pago_inicial_b="USD 7.000<small>equipos + 12 meses, con 10 % de descuento</small>",
    doce_a="7.395", doce_b="7.000",
    veinti_a="10.395", veinti_b="9.700",
    bna="USD 4.770 &asymp; $ 7.321.950 &middot; USD 250 &asymp; $ 383.750 &middot; USD 7.000 &asymp; $ 10.745.000",

    saber="""El sistema avisa; no garantiza la mercadería ni reemplaza la revisión del reefer. Sin energía en
el equipo no mide: lo que avisa en ese caso es la nube, diciendo que dejó de reportar. <strong>Si un equipo se
apaga o falla, quedan sin vigilancia los dos reefers que atiende.</strong> La entrada de defrost necesita que el
reefer tenga una señal o un contacto accesible; si alguno no lo tiene, esa entrada queda libre y el resto
funciona igual. Las salidas a relé vienen en el equipo; la sirena o baliza que se conecte no está incluida.
Cada equipo necesita llegar a la red del campamento desde donde esté montado.""",
)

# ------------------------------------------------------------------ plantilla

def pie(d, n, total):
    return ('<div class="pie">\n'
            '  <span class="marca">%s <b>Termovig&iacute;a</b> &middot; Bah&iacute;a Blanca</span>\n'
            '  <span class="cod">Presupuesto %s &middot; %s &middot; Cerro Moro &middot; Precios en USD</span>\n'
            '  <span class="npag">%d / %d</span>\n'
            '</div>\n' % (ESCUDO, d["num"], d["titulo"].lower(), n, total))


def armar(d, logo_svg):
    h = []
    a = h.append
    a('<!DOCTYPE html>\n<html lang="es-AR">\n<head>\n<meta charset="utf-8">\n'
      '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
      '<title>Termovig&iacute;a &mdash; Presupuesto %s: %s &mdash; 6 reefers, Cerro Moro</title>\n'
      '<link rel="stylesheet" href="estilo.css">\n</head>\n<body>\n<div class="doc">\n'
      % (d["num"], d["titulo"].lower()))

    # ---------------- HOJA 1
    a('<section class="hoja compacta presu">\n')
    a('<div class="cabecera">\n  <div class="logo">%s</div>\n' % logo_svg)
    a('  <div class="sello"><b>Presupuesto %s</b>%s<br>Ref. %s</div>\n</div>\n'
      % (d["num"], FECHA, d["ref"]))

    # rotulo de tapa: lo que distingue un documento del otro de un vistazo
    a('<div class="rotulo">\n'
      '  <div class="cifra-rot">%s</div>\n'
      '  <div class="txt"><span class="k">Monitoreo de temperatura de reefers</span>'
      '<h1>%s</h1><span class="b">%s &middot; %s</span></div>\n'
      '</div>\n' % (d["num"], d["titulo"], d["bajada"], d["lugar"]))

    a('<h2><span class="n">01</span>Qu&eacute; es</h2>\n<div class="doscol">'
      + d["que_es"] + '</div>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">02</span>Qu&eacute; hace</h2>\n')
    if d["que_hace_intro"]:
        a('<p>%s</p>\n' % d["que_hace_intro"])
    a('<ul class="lista chica doscol">\n')
    for li in d["que_hace"]:
        a('  <li>%s</li>\n' % li)
    a('</ul>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">03</span>Por qu&eacute; 4 sondas por reefer y no una</h2>\n')
    a('<div class="sub">Es la diferencia entre una instalaci&oacute;n seria '
      'y un term&oacute;metro con WiFi.</div>\n')
    a('<div class="qgrid">\n')
    for i, s in enumerate(d["sondas"], 1):
        a('<div class="qitem"><div class="n">%d</div><div class="q">%s</div></div>\n' % (i, s))
    a('</div>\n')

    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">04</span>Qu&eacute; se instala</h2>\n<div class="doscol">'
      + d["instala"] + '</div>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">05</span>Condiciones de instalaci&oacute;n</h2>\n')
    a('<div class="cond %s"><p><strong class="tit">%s</strong> %s</p>%s</div>\n'
      % (d["cond_clase"], d["cond_titulo"], d["cond"],
         ('<p class="ajuste">%s</p>' % d["cond_extra"]) if d["cond_extra"] else ''))

    a('<div class="sep-ch"></div>\n')

    a('<div class="aire"></div>\n')
    a(pie(d, 1, 2))
    a('</section>\n\n')

    # ---------------- HOJA 2
    a('<section class="hoja compacta presu">\n')

    a('<h2><span class="n">06</span>Puesta en marcha y ajuste en sitio</h2>\n')
    a('<div class="sub">15 semanas, por hitos. Son compromiso de entrega con fecha: no se '
      'facturan aparte, est&aacute;n incluidos en el precio.</div>\n')
    a('<table class="compacta"><thead><tr><th style="width:8%">Hito</th><th>Qu&eacute; queda funcionando</th>'
      '<th class="num" style="width:12%">Semana</th></tr></thead><tbody>\n')
    for n, t, s in d["hitos"]:
        a('<tr><td class="num">%s</td><td>%s</td><td class="num">%s</td></tr>\n' % (n, t, s))
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
    a('<tr class="total"><td colspan="2"><strong>Servicio mensual</strong> <span class="soft">&mdash; 6 reefers: '
      'nube, alertas, soporte, reposici&oacute;n sin cargo, informe mensual</span></td>'
      '<td class="num">%s</td></tr>\n' % d["abono"])
    a('</tbody></table>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">08</span>C&oacute;mo se paga</h2>\n')
    a('<div class="sub"><strong>50 % con la orden de compra</strong> '
      '(anticipo de materiales) y <strong>50 % contra los equipos instalados y reportando</strong>. '
      'El servicio mensual arranca con el primer equipo andando.</div>\n')
    a('<table class="abc dos"><thead><tr><th></th>'
      '<th><span class="letra">A</span><span class="nom">Equipos + servicio mensual</span></th>'
      '<th><span class="letra">B</span><span class="nom">Anual adelantado</span></th></tr></thead><tbody>\n')
    a('<tr><th>Para qui&eacute;n</th><td>Compra activos y paga el servicio mes a mes</td>'
      '<td>Tiene presupuesto de inversi&oacute;n y no quiere 12 facturas</td></tr>\n')
    a('<tr><th>Equipos y puesta en marcha</th><td class="usd">%s</td><td>Incluidos</td></tr>\n'
      % d["pago_equipos"])
    a('<tr><th>Pago inicial total</th><td class="usd">%s</td><td class="usd">%s</td></tr>\n'
      % (d["pago_inicial_a"], d["pago_inicial_b"]))
    a('<tr><th>Mensual</th><td class="usd">USD 250<small>los primeros 3 meses, mientras dura la puesta en '
      'marcha, se facturan al 50 %</small></td><td class="usd">&mdash;<small>el primer a&ntilde;o; '
      'renovaci&oacute;n anual USD 2.700</small></td></tr>\n')
    a('<tr><th>Los equipos</th><td>Son del cliente</td><td>Son del cliente</td></tr>\n')
    a('<tr class="tot doce"><th>Total a 12 meses <span class="u">USD</span></th><td>%s</td><td>%s</td></tr>\n'
      % (d["doce_a"], d["doce_b"]))
    a('<tr class="tot"><th>Total a 24 meses <span class="u">USD</span></th><td>%s</td><td>%s</td></tr>\n'
      % (d["veinti_a"], d["veinti_b"]))
    a('</tbody></table>\n')
    a('<p class="tabla-pie">Facturaci&oacute;n en d&oacute;lares estadounidenses. De abonarse en pesos, se toma '
      'el tipo de cambio vendedor del Banco de la Naci&oacute;n Argentina de la fecha de pago. '
      'Referencia al 3-sep-2026 (BNA vendedor $ 1.535): %s.</p>\n' % d["bna"])
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
    for d in (P1, P2):
        p = os.path.join(AQUI, d["archivo"] + ".html")
        io.open(p, "w", encoding="utf-8").write(armar(d, logo))
        print("escrito", d["archivo"] + ".html")
