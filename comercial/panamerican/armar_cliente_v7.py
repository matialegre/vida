# -*- coding: utf-8 -*-
"""Arma el UNICO presupuesto del cliente (v9.0, 8-sep-2026).

Copy: PROPUESTA_PANAMERICAN_CERRO_MORO.md v9.0 (@comercial), PARTE 1 + la columna
"como se acepta" de la PARTE 4 reescrita sin nombres internos. Nada inventado.

v9.0: 3 MODULOS DOBLES, uno por cada par de reefers pegados. Andres (8-sep, WhatsApp):
"con tres modulos solucionamos lo de Cerro Moro, un modulo para dos reefer; al estar
juntos de a dos es facil hacer la conexion; pongo la caja sobre la union de los dos y
saco las sondas". Matias acepto, mantiene 3 sondas por reefer ("3 es mucho mejor para
calibracion" -- y Andres midio casi 3 grados entre la puerta y el fondo de un reefer) y
le dijo: "rehago el presupuesto, queda mas o menos lo mismo, porque le tengo que meter
un poco mas de electronica adentro de la caja y programacion".
  - 1 doble de EXTERIOR (caja estanca IP65) para los 2 de la intemperie
  - 2 dobles de INTERIOR para los 4 bajo techo, de a dos (uno de los 4 esta fuera de
    servicio y YA queda cubierto por su modulo, con sus sondas incluidas)
  - por modulo: 6 sondas, 2 puertas, 2 defrost, 2 reles; a cada reefer le llega UN solo
    cable de 3 hilos y las 3 sondas se reparten adentro
  - repuesto: 1 modulo doble completo, reemplaza a cualquiera de los 3

PRECIOS (unica fuente de verdad, cambiar solo ACA). La cuenta, con margen parejo ~32 %
sobre precio de venta (mismo criterio que la v8.0; costos en USD al BNA 1.530):
  costo doble interior = electronica 38 (30 de la v8 + ~8 del segundo bus 1-Wire con su
    proteccion, 2.a entrada de defrost, borneras y prensacables x2) + gabinete 14 +
    6 sondas 41 + 2 reed 11 + envio 15 (4 bultos) + armado/prueba de banco de los DOS
    buses a 25 m/garantia 160 + plataforma 333 (USD 1.000 / 3 modulos) = 612
    -> 612/0,68 = 900  (margen 288, 32,0 %)
  costo doble exterior = idem con gabinete 29 y envio 17 = 629 -> 925 -> 950 (33,8 %)
  costo repuesto (doble completo, 6 sondas + 2 reed, sin plataforma) = 279 -> 410 -> 400
    (30,2 %; redondeado a la centena hacia abajo: no lleva plataforma y queda en estante)
  equipos 2x900 + 950 + 400 = 3.150 - costo 2.132 - margen 1.018 = 32,3 %
  puesta en marcha 66 h x USD 25 = 1.650 (62 h de la v8 + 8 h de software del doble que
    ahora corre en los TRES modulos: reparto de sondas por reefer, un bus por reefer,
    silenciado de defrost por reefer, panel con dos reefers por modulo; - 4 h por hacer
    3 altas remotas en vez de 5)
  TOTAL INICIAL 4.800 (v8.0: 5.000; -200, -4 %: "mas o menos lo mismo", y se dice asi:
    menos cajas, pero cada caja lleva mas electronica y mas programacion).
  Abono 500/mes sin escalon (100 x 5 reefers). B anual = 4.800 + 5.400 = 10.200.
  Sexto reefer: SIN costo de equipo (su modulo y sus sondas ya estan) -- solo el abono
    pasa de 500 a 600.

Salida: PRESUPUESTO_CERRO_MORO.html
"""
import io, os

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = r"C:\Proyectos\frioseguro\marca\logo_horizontal.svg"
FECHA = "8 de septiembre de 2026"
BNA_FECHA = "8-sep-2026"

ESCUDO = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Termovigia">'
          '<path d="M50 4 L92 18 V50 C92 74.5 74 90.5 50 97 C26 90.5 8 74.5 8 50 V18 Z" fill="#0E4F66"/>'
          '<path d="M20 68 L40 68 L56 40 L62 40" fill="none" stroke="#FFFFFF" stroke-width="8.5" '
          'stroke-linecap="round" stroke-linejoin="round"/>'
          '<circle cx="75" cy="40" r="9" fill="#FFFFFF"/><circle cx="75" cy="40" r="5" fill="#C4291C"/></svg>')

# ------------------------------------------------------------------ PRECIOS: unica fuente de verdad

PRECIOS = dict(
    doble_int=900,       # modulo doble de interior (2 reefers pegados bajo techo), c/u
    n_int=2,             # cantidad de modulos dobles de interior
    doble_ext=950,       # modulo doble de exterior (los 2 de la intemperie), estanco IP65
    repuesto=400,        # kit de repuesto: 1 modulo doble completo
    puesta=1650,         # puesta en marcha y ajuste en sitio (66 h a USD 25/h)
    abono_unit=100,      # USD por reefer por mes
    n_reefers=5,         # reefers en servicio hoy
    sexto=0,             # alta del sexto reefer: sin costo de equipo (modulo y sondas ya incluidos)
    sexto_abono=100,     # USD/mes adicionales que suma el sexto reefer
    desc_b=0.10,         # descuento de la forma B sobre el servicio anual
    bna=1530,            # BNA vendedor billete, 8-sep-2026 09:50 (bna.com.ar)
)


def miles(n):
    """Formatea un entero con separador de miles estilo AR (punto)."""
    return "{:,.0f}".format(n).replace(",", ".")


def calcular(p):
    c = dict(p)
    c["n_modulos"] = p["n_int"] + 1
    c["equipos"] = p["doble_ext"] + p["doble_int"] * p["n_int"] + p["repuesto"]
    c["total"] = c["equipos"] + p["puesta"]
    c["abono"] = p["abono_unit"] * p["n_reefers"]
    c["anual_b"] = round(c["abono"] * 12 * (1 - p["desc_b"]))
    c["a12"] = c["total"] + c["abono"] * 12
    c["a24"] = c["total"] + c["abono"] * 24
    c["b1"] = c["total"] + c["anual_b"]
    c["b24"] = c["b1"] + c["anual_b"]
    c["anticipo"] = c["total"] / 2
    c["bna_total"] = c["total"] * p["bna"]
    c["bna_abono"] = c["abono"] * p["bna"]
    c["bna_b1"] = c["b1"] * p["bna"]
    return c


C = calcular(PRECIOS)

# ------------------------------------------------------------------ contenido

D = dict(
    archivo="PRESUPUESTO_CERRO_MORO",
    ref="PROP-CM-2026-09-08",
    titulo="Tres m&oacute;dulos, uno por cada par de reefers",
    bajada="1 m&oacute;dulo estanco de exterior + 2 m&oacute;dulos de interior, cada uno para dos reefers que est&aacute;n juntos",
    lugar="Campamento Cerro Moro (Santa Cruz) &mdash; 5 reefers en servicio",

    que_es="""<p>Un sistema que mide la temperatura de cada reefer las 24 horas y avisa al celular cuando algo se
sale de rango. Por cada reefer, siempre lo mismo: <strong>3 sondas, 1 sensor de puerta y 1 se&ntilde;al de
defrost</strong>, y <strong>un solo cable de 3 hilos</strong> desde el m&oacute;dulo hasta el reefer.</p>
<p>Hoy ya hay un equipo instalado y reportando desde el campamento. <strong>Mientras se eval&uacute;a esta
propuesta ese equipo sigue midiendo y reportando</strong>, y el panel se puede abrir en el celular en cualquier
momento: los resultados se ven durante el proceso, no despu&eacute;s.</p>""",

    # --- 02: la configuracion del sitio, de un vistazo
    config=[
        ("2", "a la intemperie, juntos",
         "<strong>Un m&oacute;dulo para los dos</strong>, en gabinete <strong>estanco IP65 apto para "
         "exterior</strong>, montado sobre la uni&oacute;n de los dos contenedores.",
         "3 sondas &middot; 1 sensor de puerta &middot; 1 se&ntilde;al de defrost &middot; 1 cable de 3 hilos",
         "Comparten m&oacute;dulo porque est&aacute;n pegados: a cada reefer le llega un solo cable, corto, desde la caja.",
         "1 m&oacute;dulo<span>de exterior, para 2 reefers</span>"),
        ("4", "bajo techo, de a dos",
         "<strong>Un m&oacute;dulo por cada par</strong>, en gabinete de interior, montado sobre la uni&oacute;n "
         "de los dos.",
         "3 sondas &middot; 1 sensor de puerta &middot; 1 se&ntilde;al de defrost &middot; 1 cable de 3 hilos",
         "Est&aacute;n de a dos, as&iacute; que cada par comparte un m&oacute;dulo. Uno de los 4 est&aacute; hoy fuera de servicio: <strong>su m&oacute;dulo y sus sondas ya quedan incluidos</strong>.",
         "2 m&oacute;dulos<span>de interior, para 2 reefers cada uno</span>"),
    ],
    config_pie="""<strong>Total: 3 m&oacute;dulos para los 6 reefers</strong> &mdash; <strong>5 en servicio
hoy</strong> y el sexto ya cubierto por el m&oacute;dulo que comparte con su vecino.""",

    que_hace=[
        "Mide la temperatura de cada reefer todo el tiempo, con <strong>3 sondas por reefer</strong>, y la guarda en la nube (12 meses de historial).",
        "Avisa al celular de quien se defina cuando un reefer se sale del rango acordado, por m&aacute;s tiempo del acordado.",
        "Avisa si <strong>queda la puerta abierta</strong> m&aacute;s de los minutos que se definan (sensor magn&eacute;tico en cada reefer).",
        "Avisa cuando una sonda se desconecta o cuando un m&oacute;dulo deja de reportar.",
        "<strong>No molesta durante el descongelamiento:</strong> toma la se&ntilde;al de defrost de cada reefer y calla las alarmas <strong>de ese reefer solamente</strong> &mdash;el que comparte m&oacute;dulo sigue vigilado&mdash; para que nadie aprenda a ignorar los avisos.",
        "Puede <strong>accionar una sirena o baliza</strong>: cada m&oacute;dulo trae 2 salidas a rel&eacute; libres para eso.",
        "Genera solo el <strong>registro mensual de temperatura por reefer</strong>, para tener el papel cuando alguien lo pide.",
        "Funciona con la red de internet que ya hay en el campamento: no hay que contratar nada m&aacute;s.",
    ],

    sondas=[
        "<strong>Un reefer no tiene &laquo;una&raquo; temperatura.</strong> En uno de los reefers del campamento ya se midi&oacute; <strong>casi 3 &deg;C de diferencia entre la puerta y el fondo</strong>. Con una sonda se mide un punto y se supone el resto; con tres &mdash;puerta, medio y fondo&mdash; se mide <strong>el peor punto</strong>, que es el que decide si la carga se arruin&oacute; y el que vale en una auditor&iacute;a, no el promedio.",
        "<strong>Si una sonda falla, el reefer sigue vigilado.</strong> En un sistema cuyo trabajo es avisar, quedarse ciego es la peor falla posible: con una sola sonda, cualquier problema deja el reefer sin vigilancia hasta que alguien viaje 1.500 km. Con tres, se pierde una y quedan dos.",
        "<strong>Las sondas se controlan entre s&iacute;.</strong> Tres es el m&iacute;nimo que permite saber <strong>cu&aacute;l</strong> se desvi&oacute;: si una se aparta de las otras dos, se detecta y se avisa. Con una sola sonda, una deriva de 2 o 3 &deg;C es invisible: el registro parece perfecto y est&aacute; mintiendo. <em>(Se entrega en el hito 2.)</em>",
        "<strong>Se calibran las tres contra la misma referencia</strong> (ba&ntilde;o de hielo) y las diferencias quedan registradas: eso es lo que hace defendible el registro ante un auditor. Y las tres van por <strong>un solo cable de 3 hilos</strong>: se reparten adentro del reefer, no hay que pasar nueve.",
    ],

    instala="""<p>Cada m&oacute;dulo atiende a <strong>dos reefers que est&aacute;n juntos</strong> y se monta sobre
la uni&oacute;n de los dos: desde ah&iacute; sale <strong>un solo cable de 3 hilos a cada reefer</strong>, y las 3
sondas se reparten adentro. Cada m&oacute;dulo trae su fuente y <strong>2 salidas a rel&eacute;</strong>, y se suma
un <strong>kit de repuesto que queda en el campamento</strong> (un m&oacute;dulo completo, con sus sondas, que
reemplaza a cualquiera de los tres). El montaje lo hace personal del campamento con los equipos preconfigurados
y gu&iacute;a por videollamada: <strong>por eso esta propuesta no tiene l&iacute;nea de instalaci&oacute;n ni
vi&aacute;ticos</strong>.</p>""",

    banco="""<strong>Cada m&oacute;dulo se prueba con el cable real antes de viajar.</strong> Los equipos
<strong>se arman y se verifican uno por uno en banco de prueba</strong> &mdash;las 6 sondas leyendo, las dos puertas,
las dos se&ntilde;ales de defrost y las salidas de alarma&mdash;, y <strong>cada salida a reefer se prueba con 25
metros de cable antes de despachar</strong>, m&aacute;s de lo que va a haber en el sitio. Para un lote que va a
quedar a 1.500 km, esa verificaci&oacute;n es la diferencia entre uno que llega andando y uno que hay que
diagnosticar por tel&eacute;fono.""",

    sexto_titulo="El sexto reefer, sin costo de equipo.",
    sexto="""El reefer que hoy est&aacute; fuera de servicio comparte m&oacute;dulo con su vecino, y ese
m&oacute;dulo <strong>ya trae sus 3 sondas, su sensor de puerta y su entrada de defrost</strong>. Cuando vuelva
<strong>no hay que comprar ning&uacute;n equipo ni tocar nada de lo instalado</strong>: se le conectan y el servicio
mensual pasa de USD %s a USD %s. Queda dicho ac&aacute; para no renegociar nada el d&iacute;a que pase.""" % (
        miles(C["abono"]), miles(C["abono"] + PRECIOS["sexto_abono"])),

    hitos=[
        ("1",
         "El equipo ya instalado, con sus 3 sondas dentro del reefer, calibradas contra una misma referencia, rangos definidos y primera alerta real en el celular",
         "Captura de la alerta en el celular, el registro en la nube y la planilla de calibraci&oacute;n de las 3 sondas.",
         "a las 2 semanas de iniciado"),
        ("2",
         "Los 3 m&oacute;dulos montados y los 5 reefers reportando; nada se pierde si se corta la red; aviso de m&oacute;dulo mudo y <strong>de sonda que se desv&iacute;a de las otras del mismo reefer</strong>; puertas y defrost validados; una semana sin falsas alarmas",
         "Desenchufar una sonda y que llegue la alarma; cortar la red 20 minutos sin perder lecturas; abrir una puerta 4 minutos y que avise; forzar el defrost de un reefer y que el que comparte m&oacute;dulo siga alarmando.",
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
        ("M&oacute;dulo de exterior para los dos reefers que est&aacute;n juntos a la intemperie",
         "Gabinete estanco IP65 apto para exterior, fuente, 2 rel&eacute;s, y por cada reefer 3 sondas + "
         "puerta + defrost por un solo cable. Probado en banco con 25 m.",
         "1", miles(PRECIOS["doble_ext"])),
        ("M&oacute;dulo de interior para dos reefers que est&aacute;n juntos bajo techo",
         "Gabinete, fuente, 2 rel&eacute;s, y por cada reefer 3 sondas + puerta + defrost por un solo cable. "
         "Probado en banco con 25 m. &mdash; %d &times; %s"
         % (PRECIOS["n_int"], miles(PRECIOS["doble_int"])),
         str(PRECIOS["n_int"]), miles(PRECIOS["doble_int"] * PRECIOS["n_int"])),
        ("Kit de repuestos en sitio",
         "1 m&oacute;dulo completo, con sus 6 sondas y 2 sensores de puerta, que reemplaza a cualquiera de los tres.",
         "1", miles(PRECIOS["repuesto"])),
        ("Puesta en marcha y ajuste en sitio",
         "Los 5 hitos de arriba, con su plazo. Incluidos en el precio, no se facturan aparte. El montaje lo hace "
         "personal del campamento con los equipos preconfigurados y gu&iacute;a por videollamada: no hay l&iacute;nea "
         "de instalaci&oacute;n ni vi&aacute;ticos.",
         "5 hitos", miles(PRECIOS["puesta"])),
    ],
    total=miles(C["total"]),
    abono="%s / mes" % miles(C["abono"]),
    pie_precio="No incluye cable ni tendido.",

    pago_equipos="USD %s <small>50 %% con la OC, 50 %% contra instalaci&oacute;n</small>" % miles(C["total"]),
    pago_inicial_a="USD %s" % miles(C["total"]),
    pago_inicial_b="USD %s<small>equipos + 12 meses de servicio, con 10 %% de descuento sobre el servicio</small>" % miles(C["b1"]),
    mensual_a="USD %s<small>USD 100 por reefer, completo desde el primer mes</small>" % miles(C["abono"]),
    mensual_b="&mdash;<small>el primer a&ntilde;o; renovaci&oacute;n anual USD %s</small>" % miles(C["anual_b"]),
    doce_a=miles(C["a12"]), doce_b=miles(C["b1"]),
    veinti_a=miles(C["a24"]), veinti_b=miles(C["b24"]),
    bna="USD %s &asymp; $ %s &middot; USD %s &asymp; $ %s &middot; USD %s &asymp; $ %s" % (
        miles(C["total"]), miles(C["bna_total"]), miles(C["abono"]), miles(C["bna_abono"]),
        miles(C["b1"]), miles(C["bna_b1"])),
    bna_ref="Ref. al %s (BNA vendedor $ %s)" % (BNA_FECHA, miles(PRECIOS["bna"])),

    saber="""El sistema avisa; no garantiza la mercader&iacute;a ni reemplaza la revisi&oacute;n del reefer. Sin
energ&iacute;a en el m&oacute;dulo no mide: lo que avisa en ese caso es la nube, diciendo que dej&oacute; de
reportar. La entrada de defrost necesita una se&ntilde;al o un contacto accesible; si alg&uacute;n reefer no lo
tiene, esa entrada queda libre y el resto funciona igual. Las 2 salidas a rel&eacute; vienen en el
m&oacute;dulo; la sirena o baliza que se conecte no est&aacute; incluida. Cada m&oacute;dulo necesita llegar a la
red del campamento. El tendido del cable de cada reefer al m&oacute;dulo lo hace el cliente. Si un m&oacute;dulo se
queda sin energ&iacute;a quedan <strong>sus dos</strong> reefers sin vigilancia: para eso est&aacute; el
m&oacute;dulo de repuesto en el campamento. Los plazos de los hitos 1 y 2 suponen que el montaje en sitio se hace
dentro de la ventana prevista, que depende de personal del campamento.""",
)

# ------------------------------------------------------------------ plantilla


def pie(n, total):
    return ('<div class="pie">\n'
            '  <span class="marca">%s <b>Termovig&iacute;a</b> &middot; Bah&iacute;a Blanca</span>\n'
            '  <span class="cod">Presupuesto &middot; 3 m&oacute;dulos &middot; Cerro Moro &middot; Precios en USD</span>\n'
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
      '  <div class="cifra-rot">%d</div>\n'
      '  <div class="txt"><span class="k">Monitoreo de temperatura de reefers</span>'
      '<h1>%s</h1><span class="b">%s &middot; %s</span></div>\n'
      '</div>\n' % (C["n_modulos"], d["titulo"], d["bajada"], d["lugar"]))

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
      '%s: %s.</p>\n' % (d["bna_ref"], d["bna"]))
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
      'Encargado de proyectos de sistemas &mdash; Montagne &middot; Mundo Outdoor<br>'
      'Termovig&iacute;a, Bah&iacute;a Blanca &middot; 2920 59-1019 &middot; alegrematias08@gmail.com &middot; <b>termovigia.vercel.app</b></div>\n</div>\n')
    a(pie(2, 2))
    a('</section>\n\n</div>\n</body>\n</html>\n')
    return "".join(h)


if __name__ == "__main__":
    logo = io.open(LOGO, encoding="utf-8").read()
    p = os.path.join(AQUI, D["archivo"] + ".html")
    io.open(p, "w", encoding="utf-8").write(armar(D, logo))
    print("escrito", D["archivo"] + ".html")
