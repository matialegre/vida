# -*- coding: utf-8 -*-
"""Arma el UNICO presupuesto del cliente (v6.1, 4-sep-2026).

Copy: PROPUESTA_PANAMERICAN_CERRO_MORO.md v6.1 (@comercial), PARTE 1 + la columna
"como se acepta" de la PARTE 4 reescrita sin nombres internos. Nada inventado.

Cambia respecto de la v5.2 (mismo generador, otro contenido):
  - 4 modulos: 2 simples de exterior (IP65) + 2 dobles de interior. Antes: 5 iguales.
  - Seccion 02 NUEVA: "Que modulo va en cada reefer" -> la configuracion del sitio de un vistazo.
  - 3 sondas por reefer (antes 4). Inicial 4.600 (antes 4.540). Sexto reefer 260 (antes 520).
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
    titulo="Cuatro m&oacute;dulos, armados seg&uacute;n c&oacute;mo est&aacute; el sitio",
    bajada="2 m&oacute;dulos de exterior + 2 m&oacute;dulos dobles bajo techo",
    lugar="Campamento Cerro Moro (Santa Cruz) &mdash; 5 reefers en servicio",

    que_es="""<p>Un sistema que mide la temperatura de cada reefer las 24 horas y avisa al celular cuando algo se
sale de rango. Por cada reefer, siempre lo mismo: <strong>3 sondas, 1 sensor de puerta y 1 se&ntilde;al de
defrost</strong>.</p>
<p>Hoy ya hay un equipo instalado y reportando desde el campamento. <strong>Mientras se eval&uacute;a esta
propuesta ese equipo sigue midiendo y reportando</strong>, y el panel se puede abrir en el celular en cualquier
momento: los resultados se ven durante el proceso, no despu&eacute;s.</p>""",

    # --- 02: la configuracion del sitio, de un vistazo (bloque nuevo de la v6.1)
    config=[
        ("2", "a la intemperie",
         "<strong>Un m&oacute;dulo cada uno</strong>, en gabinete <strong>estanco IP65 apto para "
         "exterior</strong>.",
         "3 sondas &middot; 1 sensor de puerta &middot; 1 se&ntilde;al de defrost",
         "Ni un metro de cable entre contenedores.",
         "2 m&oacute;dulos<span>simples, de exterior</span>"),
        ("4", "bajo techo",
         "<strong>Un m&oacute;dulo doble cada par</strong>, en gabinete com&uacute;n de interior.",
         "3 sondas &middot; 1 sensor de puerta &middot; 1 se&ntilde;al de defrost",
         "Una tirada de cable por par, bajo techo. Uno de los 4 est&aacute; hoy fuera de servicio: su canal ya queda libre.",
         "2 m&oacute;dulos<span>dobles, de interior</span>"),
    ],
    config_pie="""<strong>Total: 4 m&oacute;dulos para los 6 reefers</strong> &mdash; <strong>5 en servicio
hoy</strong> y el sexto con su canal ya puesto.""",

    que_hace=[
        "Mide la temperatura de cada reefer todo el tiempo, con <strong>3 sondas por reefer</strong>, y la guarda en la nube (12 meses de historial).",
        "Avisa al celular de quien se defina cuando un reefer se sale del rango acordado, por m&aacute;s tiempo del acordado.",
        "Avisa si <strong>queda la puerta abierta</strong> m&aacute;s de los minutos que se definan (sensor magn&eacute;tico en cada reefer).",
        "Avisa cuando una sonda se desconecta o cuando un m&oacute;dulo deja de reportar.",
        "<strong>No molesta durante el descongelamiento:</strong> toma la se&ntilde;al de defrost de cada reefer y calla las alarmas <strong>de ese reefer</strong> mientras dura el ciclo &mdash; para que nadie aprenda a ignorar los avisos.",
        "Puede <strong>accionar una sirena o baliza</strong>: cada m&oacute;dulo trae 2 salidas a rel&eacute; libres para eso.",
        "Genera solo el <strong>registro mensual de temperatura por reefer</strong>, para tener el papel cuando alguien lo pide.",
        "Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada m&aacute;s.",
    ],

    sondas=[
        "<strong>Un reefer no tiene &laquo;una&raquo; temperatura.</strong> Cerca de la puerta, cerca del evaporador, arriba y abajo puede haber varios grados de diferencia. Con una sonda se mide un punto y se supone el resto; con tres se mide <strong>el peor punto</strong>, que es el que decide si la carga se arruin&oacute; y el que vale en una auditor&iacute;a, no el promedio.",
        "<strong>Si una sonda falla, el reefer sigue vigilado.</strong> En un sistema cuyo trabajo es avisar, quedarse ciego es la peor falla posible: con una sola sonda, cualquier problema deja el reefer sin vigilancia hasta que alguien viaje 1.500 km. Con tres, se pierde una y quedan dos.",
        "<strong>Las sondas se controlan entre s&iacute;.</strong> Tres es el m&iacute;nimo que permite saber <strong>cu&aacute;l</strong> se desvi&oacute;: si una se aparta de las otras dos, se detecta y se avisa. Con una sola sonda, una deriva de 2 o 3 &deg;C es invisible: el registro parece perfecto y est&aacute; mintiendo. <em>(Se entrega en el hito 2.)</em>",
        "<strong>Se calibran las tres contra la misma referencia</strong> (ba&ntilde;o de hielo) y las diferencias quedan registradas: eso es lo que hace defendible el registro ante un auditor.",
    ],

    instala="""<p>Cada m&oacute;dulo trae su fuente y <strong>2 salidas a rel&eacute;</strong>, y se suma un
<strong>kit de repuesto que queda en el campamento</strong> (un m&oacute;dulo doble completo, que reemplaza a
cualquiera de los cuatro). El montaje lo hace personal del campamento con los equipos preconfigurados y gu&iacute;a
por videollamada: <strong>por eso esta propuesta no tiene l&iacute;nea de instalaci&oacute;n ni
vi&aacute;ticos</strong>.</p>""",

    banco="""<strong>Cada m&oacute;dulo se prueba con el cable real antes de viajar.</strong> Los equipos
<strong>se arman y se verifican uno por uno en banco de prueba</strong> &mdash;todas las sondas leyendo, las puertas,
las se&ntilde;ales de defrost y las salidas de alarma&mdash;, y <strong>cada m&oacute;dulo doble se prueba con 25
metros de cable antes de despacharlo</strong>, la distancia real del sitio. Para un equipo que va a quedar a 1.500 km,
esa verificaci&oacute;n es la diferencia entre uno que llega andando y uno que hay que diagnosticar por
tel&eacute;fono.""",

    sexto_titulo="El sexto reefer, con el precio ya puesto.",
    sexto="""El reefer que hoy est&aacute; fuera de servicio <strong>ya tiene su m&oacute;dulo instalado, con el
canal libre</strong>. Cuando vuelva <strong>no hay que comprar ning&uacute;n equipo</strong>: se le suman sus 3 sondas,
su puerta y su defrost por <strong>USD 260</strong>, y el servicio mensual pasa de USD 500 a USD 600. Queda dicho
ac&aacute; para no renegociar nada el d&iacute;a que pase.""",

    hitos=[
        ("1",
         "El equipo ya instalado, con sus 3 sondas dentro del reefer, calibradas contra una misma referencia, rangos definidos y primera alerta real en el celular",
         "Captura de la alerta en el celular, el registro en la nube y la planilla de calibraci&oacute;n de las 3 sondas.",
         "a las 2 semanas de iniciado"),
        ("2",
         "Los 4 m&oacute;dulos montados y los 5 reefers reportando; nada se pierde si se corta la red; aviso de m&oacute;dulo mudo y <strong>de sonda que se desv&iacute;a de las otras del mismo reefer</strong>; puertas y defrost validados; una semana sin falsas alarmas",
         "Desenchufar una sonda y que llegue la alarma; cortar la red 20 minutos sin perder lecturas; abrir una puerta 4 minutos y que avise; forzar el defrost de un reefer y que el otro del mismo m&oacute;dulo siga alarmando.",
         "a las 5 semanas"),
        ("3",
         "Acceso seguro: cada m&oacute;dulo y cada usuario con su propia credencial",
         "Con una credencial dada de baja ya no se puede escribir, y todos los m&oacute;dulos siguen reportando.",
         "a las 10 semanas"),
        ("4",
         "Actualizaciones de los equipos a distancia, sin tocarlos",
         "Tres actualizaciones seguidas por aire, al primer intento, en todos los m&oacute;dulos.",
         "a las 12 semanas"),
        ("5",
         "Panel para la empresa (usuarios de solo lectura), accionamiento de las salidas de alarma e informe mensual descargable",
         "Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el panel.",
         "a las 15 semanas"),
    ],

    costos=[
        ("M&oacute;dulo de exterior, para un reefer a la intemperie",
         "Gabinete estanco IP65, fuente, 2 rel&eacute;s, 3 sondas, puerta y defrost.",
         "2 &times; 600", "1.200"),
        ("M&oacute;dulo doble, para dos reefers bajo techo",
         "Gabinete, fuente, 2 rel&eacute;s, y por reefer 3 sondas + puerta + defrost. Probado en banco con 25 m.",
         "2 &times; 750", "1.500"),
        ("Kit de repuestos en sitio",
         "1 m&oacute;dulo doble completo, que reemplaza a cualquiera de los cuatro, + 3 sondas + 1 puerta.",
         "1", "400"),
        ("Puesta en marcha y ajuste en sitio",
         "Los 5 hitos de arriba, con su plazo. Incluidos en el precio, no se facturan aparte. El montaje lo hace "
         "personal del campamento con los equipos preconfigurados y gu&iacute;a por videollamada: no hay l&iacute;nea "
         "de instalaci&oacute;n ni vi&aacute;ticos.",
         "5 hitos", "1.500"),
    ],
    total="4.600",
    abono="500 / mes",
    pie_precio="No incluye cable ni tendido entre reefers.",

    pago_equipos="USD 4.600 <small>50 % con la OC, 50 % contra instalaci&oacute;n</small>",
    pago_inicial_a="USD 4.600",
    pago_inicial_b="USD 10.000<small>equipos + 12 meses de servicio, con 10 % de descuento sobre el servicio</small>",
    mensual_a="USD 500<small>USD 100 por reefer, completo desde el primer mes</small>",
    mensual_b="&mdash;<small>el primer a&ntilde;o; renovaci&oacute;n anual USD 5.400</small>",
    doce_a="10.600", doce_b="10.000",
    veinti_a="16.600", veinti_b="15.400",
    bna="USD 4.600 &asymp; $ 7.061.000 &middot; USD 500 &asymp; $ 767.500 &middot; USD 10.000 &asymp; $ 15.350.000",

    saber="""El sistema avisa; no garantiza la mercader&iacute;a ni reemplaza la revisi&oacute;n del reefer. Sin
energ&iacute;a en el m&oacute;dulo no mide: lo que avisa en ese caso es la nube, diciendo que dej&oacute; de
reportar. La entrada de defrost necesita una se&ntilde;al o un contacto accesible; si alg&uacute;n reefer no lo
tiene, esa entrada queda libre y el resto funciona igual. Las 2 salidas a rel&eacute; vienen en el
m&oacute;dulo; la sirena o baliza que se conecte no est&aacute; incluida. Cada m&oacute;dulo necesita llegar a la red del campamento. El tendido del cable de los dos pares de adentro lo hace el cliente, y ah&iacute; si un
m&oacute;dulo se queda sin energ&iacute;a quedan <strong>dos</strong> reefers sin vigilancia hasta que vuelva; en los
de la intemperie, uno. Los plazos de los hitos 1 y 2 suponen que el montaje en sitio se hace dentro de la ventana prevista, que depende de personal del campamento.""",
)

# ------------------------------------------------------------------ plantilla


def pie(n, total):
    return ('<div class="pie">\n'
            '  <span class="marca">%s <b>Termovig&iacute;a</b> &middot; Bah&iacute;a Blanca</span>\n'
            '  <span class="cod">Presupuesto &middot; 4 m&oacute;dulos &middot; Cerro Moro &middot; Precios en USD</span>\n'
            '  <span class="npag">%d / %d</span>\n'
            '</div>\n' % (ESCUDO, n, total))


def armar(d, logo_svg):
    h = []
    a = h.append
    a('<!DOCTYPE html>\n<html lang="es-AR">\n<head>\n<meta charset="utf-8">\n'
      '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
      '<title>Termovig&iacute;a &mdash; Presupuesto: monitoreo de temperatura de reefers, Cerro Moro</title>\n'
      '<link rel="stylesheet" href="estilo.css">\n</head>\n<body>\n<div class="doc">\n')

    # ---------------- HOJA 1
    a('<section class="hoja compacta presu">\n')
    a('<div class="cabecera">\n  <div class="logo">%s</div>\n' % logo_svg)
    a('  <div class="sello"><b>Presupuesto</b>%s<br>Ref. %s</div>\n</div>\n' % (FECHA, d["ref"]))

    a('<div class="rotulo">\n'
      '  <div class="cifra-rot">4</div>\n'
      '  <div class="txt"><span class="k">Monitoreo de temperatura de reefers</span>'
      '<h1>%s</h1><span class="b">%s &middot; %s</span></div>\n'
      '</div>\n' % (d["titulo"], d["bajada"], d["lugar"]))

    a('<h2><span class="n">01</span>Qu&eacute; es</h2>\n<div class="doscol">' + d["que_es"] + '</div>\n')
    a('<div class="sep-ch"></div>\n')

    # --- la configuracion del sitio, de un vistazo
    a('<h2><span class="n">02</span>Qu&eacute; m&oacute;dulo va en cada reefer</h2>\n')
    a('<table class="compacta config"><thead><tr>'
      '<th style="width:17%">D&oacute;nde est&aacute; el reefer</th>'
      '<th>Qu&eacute; le va</th>'
      '<th style="width:21%">Qu&eacute; lleva cada reefer</th>'
      '<th class="num" style="width:19%">Equipos</th></tr></thead><tbody>\n')
    for cant, donde, que, lleva, nota, equipos in d["config"]:
        a('<tr><td><strong class="cant">%s</strong> <span class="donde">reefers<br>%s</span></td>'
          '<td>%s<span class="soft det">%s</span></td>'
          '<td class="lleva">%s</td>'
          '<td class="num equipos">%s</td></tr>\n' % (cant, donde, que, nota, lleva, equipos))
    a('</tbody></table>\n')
    a('<p class="tabla-pie">%s</p>\n' % d["config_pie"])
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">03</span>Qu&eacute; hace</h2>\n')
    a('<ul class="lista chica doscol">\n')
    for li in d["que_hace"]:
        a('  <li>%s</li>\n' % li)
    a('</ul>\n')
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">04</span>Por qu&eacute; 3 sondas por reefer y no una</h2>\n')
    a('<div class="sub">Es la diferencia entre una instalaci&oacute;n seria y un term&oacute;metro con WiFi.</div>\n')
    a('<div class="qgrid">\n')
    for i, s in enumerate(d["sondas"], 1):
        a('<div class="qitem"><div class="n">%d</div><div class="q">%s</div></div>\n' % (i, s))
    a('</div>\n')

    a('<div class="sep-ch"></div>\n')

    a('<div class="box"><p>%s</p></div>\n' % d["banco"])

    a('<h2><span class="n">05</span>Ampliaci&oacute;n</h2>\n')
    a('<div class="cond ok"><p><strong class="tit">%s</strong> %s</p></div>\n'
      % (d["sexto_titulo"], d["sexto"]))
    a('<div class="aire"></div>\n')
    a(pie(1, 2))
    a('</section>\n\n')

    # ---------------- HOJA 2
    a('<section class="hoja compacta presu">\n')
    a('<div class="sep-ch"></div>\n')




    a('<h2><span class="n">06</span>Puesta en marcha y ajuste en sitio</h2>\n')
    a('<div class="sub">15 semanas, por hitos, incluidos en el precio. <strong>Los plazos se cuentan desde el inicio, y el inicio es la aceptaci&oacute;n de esta propuesta con su anticipo.</strong></div>\n')
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
    a('<tr class="total"><td colspan="2"><strong>Servicio mensual</strong> <span class="soft">&mdash; USD 100 por '
      'reefer por mes, 5 reefers en servicio: nube, alertas, soporte, reposici&oacute;n sin cargo, informe '
      'mensual</span></td><td class="num">%s</td></tr>\n' % d["abono"])
    a('</tbody></table>\n')
    a('<p class="tabla-pie">%s</p>\n' % d["pie_precio"])
    a('<div class="sep-ch"></div>\n')

    a('<h2><span class="n">08</span>C&oacute;mo se paga</h2>\n')
    a('<table class="abc dos"><thead><tr><th></th>'
      '<th><span class="letra">A</span><span class="nom">Equipos + servicio mensual</span></th>'
      '<th><span class="letra">B</span><span class="nom">Anual adelantado</span></th></tr></thead><tbody>\n')
    a('<tr><th>Pago inicial</th><td class="usd">%s</td><td class="usd">%s</td></tr>\n'
      % (d["pago_equipos"], d["pago_inicial_b"]))
    a('<tr><th>Mensual</th><td class="usd">%s</td><td class="usd">%s</td></tr>\n'
      % (d["mensual_a"], d["mensual_b"]))
    a('<tr><th>Los equipos</th><td colspan="2">Son del cliente en las dos formas</td></tr>\n')
    a('<tr class="tot doce"><th>Total a 12 meses <span class="u">USD</span></th><td>%s</td><td>%s</td></tr>\n'
      % (d["doce_a"], d["doce_b"]))
    a('<tr class="tot"><th>Total a 24 meses <span class="u">USD</span></th><td>%s</td><td>%s</td></tr>\n'
      % (d["veinti_a"], d["veinti_b"]))
    a('</tbody></table>\n')
    a('<p class="tabla-pie">Facturaci&oacute;n en d&oacute;lares estadounidenses. De abonarse en pesos, se toma '
      'el tipo de cambio vendedor del Banco de la Naci&oacute;n Argentina de la fecha de pago. '
      'Ref. al 4-sep-2026 (BNA vendedor $ 1.535): %s.</p>\n' % d["bna"])
    a('<div class="sep-ch"></div>\n')

    a('<div class="grid2 cierre">\n'
      '  <div class="box"><p><strong>Incluido en el servicio mensual</strong><br>Nube con 12 meses de historial '
      '&middot; alertas por temperatura, puerta abierta, sonda ca&iacute;da y equipo mudo &middot; '
      'reposici&oacute;n sin cargo de cualquier m&oacute;dulo o sonda fallada, env&iacute;o incluido &middot; '
      'actualizaciones &middot; soporte por WhatsApp y tel&eacute;fono el mismo d&iacute;a h&aacute;bil '
      '&middot; informe mensual por reefer.</p></div>\n'
      '  <div class="nota azul"><p><strong>Lo que hay que saber</strong><br><span class="neutro">%s</span></p></div>\n'
      '</div>\n' % d["saber"])

    a('<div class="aire grande"></div>\n')
    a('<div class="contacto">\n'
      '  <div class="cta">Se puede ver en vivo antes de decidir.<span>Contacto en sitio: '
      'Andr&eacute;s Leiva Chavez</span></div>\n'
      '  <div class="line">Mat&iacute;as Alegre &mdash; Ingenier&iacute;a Electr&oacute;nica, UTN Facultad Regional Bah&iacute;a Blanca &middot; Grupo de investigaci&oacute;n GIMAP<br>'
      'Termovig&iacute;a, Bah&iacute;a Blanca &middot; 2920 59-1019 &middot; alegrematias08@gmail.com &middot; <b>termovigia.vercel.app</b></div>\n</div>\n')
    a(pie(2, 2))
    a('</section>\n\n</div>\n</body>\n</html>\n')
    return "".join(h)


if __name__ == "__main__":
    logo = io.open(LOGO, encoding="utf-8").read()
    p = os.path.join(AQUI, D["archivo"] + ".html")
    io.open(p, "w", encoding="utf-8").write(armar(D, logo))
    print("escrito", D["archivo"] + ".html")
