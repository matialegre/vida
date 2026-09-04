# -*- coding: utf-8 -*-
"""Arma el documento INTERNO de Cerro Moro (v7.0, 4-sep-2026).

v7.0: los dos de afuera comparten módulo (Andrés, 4-sep: "están juntos"), así que la
configuración pasa a 3 módulos, TODOS DOBLES (1 estanco de exterior + 2 de interior),
inicial 4.115 (antes 4.600), B = 9.515 (antes 10.000). El firmware doble pasa a ser
crítico para los TRES módulos (antes había colchón en los 2 simples de exterior).

Copy: PROPUESTA_PANAMERICAN_CERRO_MORO.md v7.0, PARTES 2 a 7 + anexos. Nada inventado:
lo unico propio son rotulos de seccion y de columna.

REGLA DE MATIAS (4-sep): NO hay ninguna logistica antes de que acepten el presupuesto.
Todo el cronograma esta en semanas DESDE la aceptacion y no hay una sola accion fechada
para "hoy" ni para "el dia que salga".

Salida: PRESUPUESTO_CERRO_MORO_INTERNO.html  (marcadores <!--LOGO_HORIZONTAL--> y <!--ESCUDO-->
que inlina render_v6.py)
"""
import io, os

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = "PRESUPUESTO_CERRO_MORO_INTERNO.html"
FECHA = "4 de septiembre de 2026"
REF = "PROP-CM-2026-09-04"

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
    <b>Interno · v7.0</b>
    ''' + FECHA + u'''<br>
    Ref. ''' + REF + u'''
  </div>
</div>

<div class="hero">
  <div class="kicker">Cerro Moro (Santa Cruz) · 6 reefers, 5 en servicio</div>
  <h1>Tres módulos, los tres <em>dobles</em>:<br>uno estanco de exterior y dos bajo techo</h1>
  <div class="bajada">Andrés cerró el último hueco el 4-sep: <em>«los de afuera pueden ir con un solo módulo,
  están juntos»</em>. Con eso los 2 reefers de la intemperie pasan a compartir <strong>un</strong> módulo doble
  estanco, igual que los 4 de adentro comparten 2 módulos dobles. <strong>Precio recalculado hacia abajo, sin
  acomodar nada:</strong> inicial 4.115 contra los 4.600 de la v6.1.</div>
  <div class="meta">
    Copy del cliente: <b>PARTE 1</b> de <b>PROPUESTA_PANAMERICAN_CERRO_MORO.md</b> (v7.0, @comercial).
    Decisiones de Matías del 4-sep: <b>el tendido de cable no se cotiza y tampoco el cable</b> — lo resuelve el
    cliente en el sitio, el documento del cliente no lleva spec de cable, <b>abono USD 100 por reefer/mes = 500/mes
    sin escalón</b>, y
    <b>en el documento del cliente no se dice el material del gabinete ni se menciona ningún proceso de
    fabricación</b>. Se mantiene: hitos en semanas desde la aceptación, 50/50, formas A y B, sin validez, sin
    destinatario. Lo de acá abajo <b>no se manda</b>; <b>el número final lo decide Matías</b>.
  </div>
</div>

<div class="sep-ch"></div>

<h2><span class="n">00</span>Dónde está cada cosa</h2>
<div class="grid3">
  <div class="card fuerte">
    <div class="cab"><span class="tag">Para copiar y mandar</span><h3>Hoja 2 — WhatsApp para Andrés</h3></div>
    <div class="cuerpo">
      <p>El mensaje completo, listo para copiar tal cual. Arranca con <em>«quedó como me dijiste»</em> y
      <strong>no le pide nada</strong>: trabaja por turnos de 15 días y no es él quien aprueba.</p>
    </div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">Lo que hay que poder defender</span><h3>Hoja 10 — La cuenta del caño</h3></div>
    <div class="cuerpo">
      <p>Archivo, no renglón: <strong>el tendido lo hace y lo paga el cliente</strong>. Sirve para saber el
      tamaño de lo que gastan por su lado y para que nadie regale la instalación.</p>
    </div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">Antes de mandar nada</span><h3>Última hoja — Los 17 pendientes</h3></div>
    <div class="cuerpo">
      <p>Lo que decide Matías y lo que tiene que confirmar cada dominio. <strong>Ninguno es logística:</strong>
      hasta que no haya aceptación y anticipo no se compra, no se arma y no se despacha nada.</p>
    </div>
  </div>
</div>

<div class="sep"></div>

<div class="grid3">
  <div class="cifra"><div class="big">4.115</div><div class="lb">USD inicial<br>765 + 2×750 + repuesto 400 + puesta en marcha 1.450</div></div>
  <div class="cifra"><div class="big">500</div><div class="lb">USD por mes<br>USD 100 por reefer × 5, sin escalón</div></div>
  <div class="cifra"><div class="big">3</div><div class="lb">módulos para 6 reefers<br>todos dobles: 1 estanco de exterior + 2 de interior</div></div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>Lo que no se movió:</strong> pago 50/50, formas A y B, los 5 hitos con sus plazos
relativos y criterios de aceptación, sin validez y sin destinatario. <strong>Sigue eliminada la opción C</strong>
de la v2 («sin inversión inicial», comodato con permanencia 24 meses), por decisión de Matías: <em>«el de la
inversión inicial no lo ofrecería»</em>.</p></div>
''', banda_larga=u'Este documento es de Matías. Al cliente va un solo PDF: PRESUPUESTO_CERRO_MORO, de 2 páginas.')

# =================================================================== HOJA 2
hoja(u'''
<h2><span class="n">01</span>Qué cambió en esta versión</h2>
<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Cambio 1</span><h3>El último hueco lo cerró Andrés: los de afuera están juntos</h3></div>
    <div class="cuerpo">
      <p>La v6.1 partió la diferencia: 2 afuera / 4 adentro, con módulo propio afuera por suponerlos separados. El
      4-sep Andrés lo cerró: <em>«los de afuera pueden ir con un solo módulo, están juntos»</em>. Se cae el único
      motivo del módulo simple: <strong>se comparte en los tres pares, porque en los tres los reefers están al
      lado.</strong></p>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Cambio 2</span><h3>Tres módulos, todos dobles — y el precio baja</h3></div>
    <div class="cuerpo">
      <p><strong>1 doble de exterior a USD 765</strong> + <strong>2 dobles de interior a USD 750</strong> =
      <strong>USD 2.265 en equipos</strong>, más repuesto <strong>400</strong> y puesta en marcha
      <strong>1.450</strong> = <strong>USD 4.115</strong>. Era 4.600 en la v6.1: <strong>−USD 485, un 10,5 %
      menos</strong>. No se tocó ningún unitario para sostener el 4.600: menos equipos = menos plata, dicho en voz
      alta, es lo que hace creíble el 500/mes que no se mueve.</p>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Cambio 3</span><h3>La obra de cable creció en una tirada, y esa es a la intemperie</h3></div>
    <div class="cuerpo">
      <p>Ahora son <strong>3 tiradas</strong>: dos bajo techo (como antes) y <strong>una a la intemperie</strong>,
      entre los dos reefers de afuera. Están juntos, así que debería ser la más corta de las tres, pero es la más
      expuesta. Sigue <strong>a cargo del cliente</strong>; interno: ese tramo tiene que ser cable apto exterior,
      sin empalmes.</p>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Cambios 4 y 5</span><h3>El firmware doble ya no tiene colchón, y el sexto sigue igual</h3></div>
    <div class="cuerpo">
      <p><strong>El firmware de módulo doble pasa a ser crítico para los TRES módulos.</strong> En la v6.1 los 2
      simples corrían el firmware que ya anda, y si el doble se atrasaba arrancaba igual la mitad del sistema. Ese
      colchón ya no existe: <strong>sin firmware doble no reporta nadie.</strong></p>
      <p>El sexto sigue adentro, fuera de servicio, con su módulo doble <strong>ya instalado</strong>: cuando vuelva,
      <strong>USD 260</strong> de sondas, puerta y defrost, <strong>+USD 100/mes</strong>. Sin equipo nuevo, sin
      renegociar nada.</p>
    </div>
  </div>
</div>

<div class="sep"></div>

<h2><span class="n">02</span>WhatsApp para Andrés — copiar desde acá</h2>
<div class="sub" style="margin:-1.5mm 0 4mm">Lo manda Matías. Va tal cual: arranca confirmándole que quedó como él
lo dijo. <strong>No le pide nada</strong> y <strong>no menciona el material de la caja ni cómo se fabrica</strong>.</div>

<div class="wsp-tit">MENSAJE COMPLETO — §6.1</div>
<div class="wsp">Andrés, quedó como me dijiste: los dos reefers que están a la
intemperie, juntos, van con un solo módulo doble, en caja estanca IP65
para exterior. Y los 4 de adentro van con 2 módulos, uno cada par. Tres
módulos en total, los tres iguales por dentro.

Por cada reefer: 3 sondas adentro, sensor de puerta y la señal de
defrost, así no suena la alarma cada vez que descongela.

El cable y su tendido corren por cuenta de ustedes en los tres pares,
eso lo ven ahí. En el de afuera tiene que ser cable apto para exterior,
después te digo bien cuál. Los tres módulos los pruebo acá en el banco
con 25 metros de cable puestos antes de despacharlos.

Una cosa más: el reefer fuera de servicio queda emparejado con uno que
anda, así el módulo ya va puesto y el día que vuelva se le suman las
sondas nomás, sin equipo nuevo. Y bajó el precio: al sacar un módulo el
inicial queda en 4.115 en vez de 4.600. El abono sigue en 500 por mes.

Te paso el presupuesto: dos hojas, sin nombre de empresa, para que se lo
pases a quien corresponda. El equipo que ya está puesto sigue reportando,
así que mientras lo miran se puede ver el panel en cualquier momento.
</div>
''')

# =================================================================== HOJA 3
hoja(u'''
<h2><span class="n">03</span>Por qué el mensaje está escrito así, para que no se suavice al copiarlo</h2>
<table class="compacta"><thead><tr><th style="width:6%">&nbsp;</th><th style="width:30%">Qué hace</th><th>Por qué</th></tr></thead><tbody>
<tr><td class="num">a</td><td><strong>Arranca con «quedó armado tal cual me lo describiste»</strong></td>
<td>Andrés dio la configuración y lo primero que lee es que se hizo exactamente eso. Vale más que cualquier
argumento técnico.</td></tr>
<tr><td class="num">b</td><td><strong>Devuelve la información en su propio idioma</strong></td>
<td>2 afuera juntos / 4 adentro, un módulo doble en cada par: le confirma que se entendió el sitio.</td></tr>
<tr><td class="num">c</td><td><strong>El tendido y el cable quedan dichos en una línea, sin prometer nada que no se cumple</strong></td>
<td>Son 3 tiradas y el cable lo ponen ellos en las 3 (desde el 4-sep Matías no lo manda). No se le da una spec que
no le vamos a mandar.</td></tr>
<tr><td class="num">d</td><td><strong>La prueba con 25 m de cable compra confianza técnica</strong></td>
<td>Dice, sin decirlo, «sé que hay distancia y me hago cargo».</td></tr>
<tr><td class="num">e</td><td><strong>El sexto reefer aparece como una previsión inteligente, no como un recorte</strong></td>
<td>Es la frase que muestra que estamos mirando el sitio de verdad.</td></tr>
<tr><td class="num">f</td><td><strong>No le pide nada</strong></td>
<td>Andrés trabaja por turnos de 15 días y <strong>no es él quien aprueba</strong>. Cierra en «te paso el
presupuesto»: la logística arranca con la aceptación y el anticipo, no antes.</td></tr>
<tr><td class="num">g</td><td><strong>No menciona el material de la caja ni cómo se fabrica</strong></td>
<td>Ni acá ni en el PDF.</td></tr>
</tbody></table>

<div class="sep"></div>

<h2><span class="n">04</span>Guion de 5 líneas para que la presente él</h2>
<ul class="lista">
  <li><strong>Arrancá por el problema, no por el producto:</strong> «un reefer que se corta un fin de semana es la
  comida de todo el campamento, y hoy nadie se entera hasta que abren la puerta.»</li>
  <li><strong>Mostrá lo que ya anda:</strong> abrí el panel en el celular y mostrá la temperatura de ahora del
  equipo instalado — sigue reportando mientras la propuesta se evalúa. Si podés, sacá una sonda al aire un minuto y
  que vean subir la curva. Eso convence más que el PDF.</li>
  <li><strong>Decilo en una frase:</strong> «los dos de afuera, que están juntos, van con un solo módulo estanco;
  los cuatro de adentro se cubren con dos, uno cada par. Tres sondas adentro de cada reefer, te avisa al celular si
  se sale de rango o si queda la puerta abierta, y arma el registro mensual solo.»</li>
  <li><strong>Si preguntan por el cable:</strong> «son tres tiradas, dos adentro bajo techo y una entre los dos de
  afuera. El cable y el tendido los ponen ustedes en las tres; en la de afuera tiene que ser apto para
  exterior.»</li>
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
<tr><td>Reportando cada ~5 s</td><td>Consulta a la base de Santa Cruz, 3-sep</td></tr>
<tr><td><strong>1 sola sonda y está FUERA del reefer</strong> — mide ambiente</td><td>Andrés espera confirmación de Matías para meterlas</td></tr>
<tr><td>Elección de red abierta con internet real: probada 128 ciclos</td><td><code>ESTADO_HONESTO.md</code></td></tr>
<tr><td><strong>Sin contrato y sin un peso cobrado</strong></td><td><code>PLATA.md</code></td></tr>
<tr><td>«Acá no pueden haber cables aéreos»</td><td>Andrés, WhatsApp 3-sep 17:11</td></tr>
<tr><td>«Pasale presupuesto por los 3 módulos, así cada uno controla dos reefers»</td><td>Andrés, WhatsApp 3-sep 17:13</td></tr>
<tr><td>«Son aprox 20/25 metros, el problema es que hay que pasar los cables con caño Daisa»</td><td>Andrés, WhatsApp <strong>3-sep 23:33</strong></td></tr>
<tr><td><strong>2 reefers están a la intemperie y 4 están adentro, bajo techo</strong></td><td>Andrés a Matías, <strong>4-sep</strong></td></tr>
<tr><td><strong>De los 4 de adentro, uno está fuera de servicio: hoy hay 5 reefers activos</strong></td><td>Matías, 4-sep</td></tr>
<tr><td>Ya se mandó al sitio una <strong>caja estanca IP65 apta para exterior</strong></td><td>Matías, 4-sep</td></tr>
<tr><td><strong>«Los de afuera pueden ir con un solo módulo, están juntos»</strong> — el dato que fija esta versión</td><td>Andrés a Matías, <strong>4-sep</strong></td></tr>
<tr><td><strong>Configuración final confirmada: 4 reefers adentro con 2 módulos, 1 módulo para los 2 de afuera. Los tres, dobles</strong></td><td>Matías, 4-sep</td></tr>
<tr><td><strong>Firmware de módulo doble: escrito y en auditoría, veredicto APTO CON CORRECCIONES</strong></td><td><code>frioseguro-v31/firmware_modular/VERIFICACION_V3.1_2026-09-04.md</code></td></tr>
</tbody></table>

<div class="sep"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">De Andrés</span><h3>Lo que sigue abierto — ninguna frena el envío</h3></div>
    <div class="cuerpo">
      <ul>
        <li><strong>¿La red del campamento llega bien a los 3 puntos donde van los módulos?</strong> Si alguno queda
        corto se resuelve con un repetidor barato, pero hay que saberlo <strong>antes de despachar</strong>.</li>
        <li><strong>¿Los reefers tienen una señal o contacto de defrost accesible?</strong> Si alguno no lo tiene,
        esa entrada queda libre y el resto funciona igual — ya está dicho así en el documento del cliente, sin letra
        chica.</li>
        <li><strong>¿Cuál de los 4 de adentro es el que está fuera de servicio?</strong> Define cómo se arman los
        pares: el que está fuera va emparejado con un activo, para que el canal libre quede en un módulo ya instalado
        y andando.</li>
        <li><strong>¿Para quién trabaja Andrés?</strong> (empleado de PAAS o de una contratista). No es técnica:
        decide la última hoja.</li>
      </ul>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">De la empresa, cuando tenga nombre</span><h3>Lo administrativo</h3></div>
    <div class="cuerpo">
      <p>Quién firma, cómo factura (monotributo/RI, plazo), si acepta la cláusula de moneda, <strong>cuál de las dos
      formas de pago elige (A o B)</strong>, y confirmación de que el montaje <strong>y el tendido del cable en los
      tres pares</strong> los hace personal del campamento (sin personal nuestro en sitio no corresponde ART
      ni legajo de contratista).</p>
      <p><strong>El comprador no es Pan American Silver:</strong> es «una empresa» que Andrés todavía no identifica.
      Por eso el documento del cliente va sin destinatario, sin logo ajeno y sin nombrar a la minera.</p>
    </div>
  </div>
</div>
''')

# =================================================================== HOJA 5
hoja(u'''
<h2><span class="n">06</span>Registro: por qué los tres módulos son dobles</h2>
<div class="sub">Las v4 y v5 discutieron durante dos versiones si convenía un equipo por reefer o uno cada dos. La
v6.1 partió la diferencia con el dato de Andrés (2 afuera / 4 adentro). <strong>El 4-sep Andrés cerró el último
hueco: los dos de afuera están juntos.</strong> Con eso la discusión termina sin ganador ideológico.</div>

<div class="cita"><p><strong>La regla que quedó, en una frase:</strong> <em>se comparte módulo cuando los dos reefers
están juntos — y en este sitio lo están los tres pares. Lo que cambia entre ellos no es el equipo, es la caja:
estanca afuera, común adentro.</em></p></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Qué se gana</span><h3>Un equipo menos, un repuesto que cubre todo</h3></div>
    <div class="cuerpo"><p><strong>Un equipo menos</strong> que comprar, armar, probar, despachar y dar de alta:
    <strong>−USD 485 en el precio</strong> y <strong>−USD 190 de costo directo</strong>, y un punto de red menos que
    verificar. <strong>El repuesto cubre el 100 % del parque con una sola caja</strong>: los tres módulos son
    idénticos por dentro. Y el módulo del par donde está el reefer fuera de servicio <strong>ya queda comprado con
    el canal libre</strong> — el sexto entra después por USD 260, no por un equipo entero.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Qué se pierde, y hay que tenerlo escrito</span><h3>Una tirada más, y a la intemperie</h3></div>
    <div class="cuerpo"><p>Ahora son <strong>3 tiradas</strong>: dos bajo techo y una entre los dos contenedores de
    afuera. Están juntos, así que debería ser la más corta, pero es la más expuesta. <strong>Si cae un módulo quedan
    dos reefers ciegos, ahora en los tres casos</strong> (antes los de afuera caían de a uno). Lo que compensa: el
    repuesto está en el campamento y es intercambiable con cualquiera. <strong>Y el firmware de módulo doble pasa a
    ser crítico para el sistema entero</strong> (hoja 6, riesgo 3).</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="nota"><p><strong>El riesgo del bus, asumido con conocimiento — que quede escrito.</strong>
<span class="neutro">Andrés dijo «son aprox 20/25 metros» (3-sep 23:33) y el límite prudente que fijó @muestreador
para este bus es <strong>15 m</strong>. Además, el cable ata las masas de <strong>dos contenedores metálicos con
puesta a tierra separada</strong> por el hilo de datos (<code>ALCANCE_1WIRE.md</code> §2.6: «el riesgo dominante de
esta instalación»). <strong>Matías conoce el dato y acepta el riesgo.</strong></span></p></div>

<ul class="lista">
  <li><strong>Pull-up de 2k2 con posición alternativa de 1k</strong> en la placa (@esquematico lo está poniendo). El
  1k es la carta que se juega si el bus no cierra a 25 m.</li>
  <li><strong>Los tres módulos se prueban en banco con 25 m de cable real antes de despachar</strong>, con las 6
  sondas colgadas. No sale nada que no haya cerrado a la distancia real.</li>
  <li><strong>Especificación de cable</strong> (par trenzado exterior, el par DQ/GND junto en todo el recorrido, sin
  empalmes, canalizado): <strong>queda interna</strong>, no se manda al cliente — desde el 4-sep el cable no lo
  provee Matías. <strong>Pero si Andrés pregunta qué cable comprar:</strong> par trenzado apto exterior en las tres
  tiradas, y en la de afuera no se negocia.</li>
  <li><strong>El riesgo subió respecto de la v6.1:</strong> ahora son <strong>3 tiradas y una es a la
  intemperie</strong>, no 2 y las dos bajo techo. Más metros expuestos y la única tirada sin techo.</li>
  <li>Si aun así un bus no cierra en sitio, la salida técnica existe y es barata: pasar ese par a un segundo bus con
  su propio pin, o un repetidor 1-Wire. <strong>No hay escenario en el que haya que devolver plata.</strong></li>
</ul>

<div class="box"><p><strong>Lo que NO se le dice al cliente:</strong> que esto es un riesgo. En el documento va la
nota de que el cable y el tendido no están incluidos, y nada más sobre el cable — la spec queda interna. La
mitigación real (prueba de banco con 25 m) tampoco se explica al cliente: se hace y punto.
<strong>Y el tendido no se cotiza</strong> (decisión de Matías, textual: «no contemples el tema de las tiradas»): la
cuenta del caño queda archivada en la hoja 10 <strong>como historia y como argumento</strong>, no como renglón. El
precio que mandamos es firme y no depende de nada que pase en una zanja.</p></div>
''')

# =================================================================== HOJA 6
hoja(u'''
<h2><span class="n">07</span>Qué lleva cada módulo, y qué de eso anda HOY</h2>
<div class="sub">Verificado en el código el 3-sep-2026. <strong>Los tres módulos son dobles: la misma fila vale para
los tres.</strong></div>
<table class="compacta"><thead><tr><th style="width:22%">Función</th><th class="num" style="width:12%">Por módulo<br>(los tres son dobles)</th>
<th>Qué hace el firmware hoy</th><th style="width:20%">Evidencia</th></tr></thead><tbody>
<tr><td>Sondas DS18B20</td><td class="num">6</td>
<td>Cada una identificada por ROM de 64 bits y reportada por separado; enganche en caliente; aviso si se desconecta;
<strong>offset de calibración por sonda en NVS</strong>. <strong><code>SONDAS_MAX</code> está en 4: para el doble hay
que subirlo a 8</strong> — es el tamaño de un arreglo, una línea.</td>
<td><code>sondas.h</code>: <code>sondasEscanear</code>, <code>sondasLeer</code>, <code>sondasCalibrar</code>; línea 31</td></tr>
<tr><td><strong>Verificación cruzada entre sondas</strong></td><td class="num gris">—</td>
<td><strong>NO existe.</strong> <code>sondasCalibrar()</code> iguala las sondas en un momento dado; el lazo de lectura
<strong>no compara sondas entre sí</strong> ni alerta por deriva.</td>
<td>ídem. Vendida en el <strong>hito 2</strong>, con la aclaración escrita en la página del cliente</td></tr>
<tr><td>Sensor de puerta</td><td class="num">2</td>
<td>Implementado <strong>para una sola puerta</strong>: GPIO5, alerta por puerta abierta &gt; 180 s, suprime la alerta
de temperatura mientras está abierta. Viene deshabilitado por defecto (<code>SENSOR_DOOR_ENABLED false</code>).
<strong>La segunda puerta hay que agregarla, y ahora hace falta en los tres módulos.</strong></td>
<td><code>config.h</code> 72-74, 105, 119 · <code>.ino</code> 804-890</td></tr>
<tr><td>Entrada de defrost</td><td class="num">2</td>
<td>Implementada <strong>para una sola entrada</strong>: GPIO33, NA/NC configurable, deshabilita alertas durante el
ciclo con 30 min de enfriamiento. <strong>La segunda hay que agregarla, y tiene que silenciar solo el reefer que
descongela.</strong></td>
<td><code>config.h</code> 91-96, 122 · <code>.ino</code> 54-55, 100-101, 872-878</td></tr>
<tr><td>Salidas a relé</td><td class="num">2</td>
<td><strong>1 gobernada</strong>: GPIO26, se activa sola con la alerta si <code>relayEnabled</code>. La segunda queda
cableada y disponible. <strong>El accionamiento manual desde el panel NO existe.</strong></td>
<td><code>config.h</code> 76-77, 140-150 · <code>.ino</code> 369-375, 483-488, 915-944 · <code>comandos_nube.h</code>
sin comando de relé → <strong>hito 5</strong></td></tr>
<tr><td>Gabinete</td><td colspan="2"><strong>1 IP65 estanco de exterior</strong> (Roker PRG357, $ 44.419) + <strong>2
de interior</strong> (Genrod IP65 210×310×110, $ 21.203)</td>
<td>Caja de exterior ya enviada al sitio (4-sep)</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Regla de venta</span><h3>Lo que no anda hoy va con hito, nunca como característica</h3></div>
    <div class="cuerpo"><ul>
      <li><strong>Segunda puerta, segundo defrost y <code>SONDAS_MAX</code> a 8</strong> — el software del módulo
      doble. Costeado, hito 2.</li>
      <li><strong>Verificación cruzada entre sondas</strong> — hito 2.</li>
      <li><strong>Accionamiento manual del relé desde el panel</strong> — hito 5.</li>
    </ul></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">El riesgo nuevo y el más grande</span><h3>El firmware doble ya no tiene colchón</h3></div>
    <div class="cuerpo"><p>En la v6.1 los 2 simples corrían el firmware que ya anda; si el doble se atrasaba, la
    mitad del sistema arrancaba igual. <strong>Con los tres módulos dobles ese colchón desaparece: el firmware
    doble pasa a ser crítico para el 100 % del pedido.</strong> Estado: <strong>escrito y en auditoría</strong>,
    veredicto <strong>APTO CON CORRECCIONES</strong>, correcciones en curso. No se vende como hecho: hito 2.</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="nota"><p><strong>Detalle que no se puede pasar por alto en el diseño del doble:</strong>
<span class="neutro">el defrost de un reefer <strong>no puede silenciar las alarmas del otro</strong>. Hoy el defrost
deshabilita <em>todas</em> las alertas del equipo. En el módulo doble tiene que silenciar <strong>solo las sondas del
reefer que está descongelando</strong>. Está dentro de las horas de la puesta en marcha y es lo que hay que probar sí
o sí antes del hito 2.</span></p></div>

<div class="box"><p><strong>Orden de armado:</strong> identificación por ROM sí o sí. <strong>Cuál línea se despacha —
<code>firmware_revival</code> extendido o <code>firmware_modular</code> v3.1 — lo define @firmware</strong> cuando
cierren las correcciones; es la decisión que bloquea el despacho. Pull-up 2k2 con alternativa 1k, 3 hilos, 100 nF +
10 µF al pie de la sonda más lejana. <strong>Habilitar <code>SENSOR_DOOR_ENABLED</code>, probar las dos puertas y
los dos defrost, y correr la prueba de banco con 25 m en los tres módulos antes de despachar.</strong></p></div>
''')

# =================================================================== HOJA 7
hoja(u'''
<h2><span class="n">08</span>Lo que se instala, y quién</h2>
<div class="grid3">
  <div class="card fuerte">
    <div class="cab"><span class="tag">×1 · USD 765</span><h3>Módulo doble de exterior</h3></div>
    <div class="cuerpo"><p><strong>Gabinete estanco IP65 apto para exterior</strong> (Roker PRG357 200×200×155),
    fuente de 5 V 2 A, plaqueta con borneras a tornillo, ESP32 en zócalo, módulo de 2 relés, <strong>prensacables en
    todas las entradas</strong>, 6 sondas DS18B20 estancas, 2 reed de puerta, 2 entradas de defrost — para el par de
    afuera, que ahora comparte módulo porque está junto.</p></div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">×2 · USD 750</span><h3>Módulo doble de interior</h3></div>
    <div class="cuerpo"><p>Gabinete IP65 de interior (Genrod 210×310×110 o las de stock si pasan la medición
    <code>M9</code>), misma electrónica, 6 sondas, 2 reed, 2 defrost.</p></div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">×1 · USD 400</span><h3>Kit de repuesto</h3></div>
    <div class="cuerpo"><p>Un <strong>módulo doble</strong> completo —los tres son idénticos por dentro, así que
    cubre a cualquiera de los tres— + 3 sondas + 1 reed. Va con gabinete de interior: <strong>si el que falla es el
    de afuera, la electrónica se pasa a la caja estanca que ya está en sitio</strong> (queda escrito en el
    runbook).</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>Montaje: Andrés</strong>, con kit preconfigurado y probado en banco + videollamada. Dos
pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los <strong>$ 2.500.000</strong>, y Matías
no puede viajar en octubre (Dreyfus). <strong>Eso es lo que esta propuesta no cobra.</strong></p></div>

<div class="nota"><p><strong>Intemperie:</strong> <span class="neutro">en el documento del cliente se dice
«gabinete estanco IP65 apto para exterior» <strong>y nada más</strong>. Ni material, ni fabricación. Ni en el PDF ni
en el WhatsApp.</span></p></div>

<div class="sep"></div>

<h2><span class="n">09</span>Los riesgos técnicos abiertos</h2>
<table class="compacta"><thead><tr><th style="width:5%">&nbsp;</th><th style="width:30%">Riesgo</th><th>Estado</th></tr></thead><tbody>
<tr><td class="num">1</td><td><strong>Las tres tiradas de 20-25 m</strong></td>
<td>Riesgo asumido, mitigaciones en la hoja 5. <strong>Subió respecto de la v6.1</strong>: tres tiradas en vez de
dos, y <strong>una es a la intemperie</strong> (la del par de afuera, que es la más corta pero la más expuesta).</td></tr>
<tr><td class="num">2</td><td><strong>Cobertura de red en 3 puntos</strong></td>
<td>El mejor número de todas las versiones (eran 5 en la v5.2 y 4 en la v6.1). Si alguno queda corto se resuelve con
un repetidor barato, pero hay que saberlo <strong>antes de despachar</strong>. No frena el envío.</td></tr>
<tr><td class="num">3</td><td><strong>El firmware de módulo doble ahora es crítico para los TRES</strong></td>
<td>En la v6.1 dos de los cuatro equipos corrían el firmware que ya anda; si el doble se atrasaba, la mitad
arrancaba igual. <strong>Ese colchón ya no existe: sin firmware doble no reporta nadie.</strong> Estado: APTO CON
CORRECCIONES, en curso. <strong>No prometer el hito 2 con más firmeza que la del papel.</strong></td></tr>
<tr><td class="num">4</td><td><strong>Defrost cruzado, ahora en los 3 módulos</strong> · <strong>Si cae un módulo,
2 reefers ciegos en los tres pares</strong></td>
<td>Software costeado, probar antes del hito 2. Mitigación: repuesto en el campamento, sirve para cualquiera de
los tres.</td></tr>
<tr><td class="num">5</td><td><strong>La caja de exterior a la intemperie de Santa Cruz</strong></td>
<td>Sin antecedente de campo largo, y ahora <strong>de ella dependen 2 reefers, no 1</strong>. La que se mandó el
4-sep es la prueba de campo: pedirle a Andrés una foto tras el primer temporal.</td></tr>
</tbody></table>

<div class="sep"></div>

<h2><span class="n">10</span>Opcionales, después de la primera orden</h2>
<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">USD 260 + 100/mes</span><h3>El sexto reefer cuando vuelva a servicio</h3></div>
    <div class="cuerpo"><p>Entra en el canal libre de su módulo doble, <strong>sin equipo nuevo</strong>. Ya está
    escrito con precio en el documento del cliente: no hay que venderlo de nuevo, solo ejecutarlo. <strong>Es el
    upsell más probable y el de mejor margen de esta cuenta.</strong></p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Los otros tres</span><h3>Se ofrecen cuando las sondas estén andando, no antes</h3></div>
    <div class="cuerpo"><ul>
      <li>Sirena o baliza física para la salida de relé (USD 40; el relé ya está incluido).</li>
      <li><strong>Cuarta sonda</strong> en un reefer (USD 40 + USD 5/mes).</li>
      <li>Base con batería y 4G, la única que avisa el corte de energía por sí misma (a cotizar) —
      <strong>especialmente vendible para el módulo de la intemperie, del que ahora dependen dos reefers</strong>.</li>
    </ul></div>
  </div>
</div>
''')

# =================================================================== HOJA 8
hoja(u'''
<h2><span class="n">11</span>Cómo se arman los dos precios: USD 750 el doble de interior, USD 765 el doble de exterior</h2>
<div class="sub">Base: BOM real (<code>BOM_KIT_V1.md</code> rev B de @hardware, precios de MercadoLibre AR verificados
el 2-sep-2026, a precio de reposición) y <code>BOM_CERRO_MORO.md</code> de @hardware, 4-sep (de ahí salen los
precios reales de gabinete). Cambio $ → USD al BNA vendedor 1.535 del 3-sep.</div>

<table class="compacta"><thead><tr><th>&nbsp;</th><th class="num" style="width:14%">Doble interior<br>(ARS)</th>
<th class="num" style="width:9%">USD</th><th class="num" style="width:14%">Doble exterior<br>(ARS)</th>
<th class="num" style="width:9%">USD</th></tr></thead><tbody>
<tr><td>Electrónica: ESP32 13.990 + módulo de 2 relés 5.028 + fuente 5 V 2 A 7.980 + consumibles de placa y
prensacables ~11.800</td>
<td class="num gris">~38.800</td><td class="num">25</td><td class="num gris">~38.800</td><td class="num">25</td></tr>
<tr><td><strong>Gabinete</strong> — interior Genrod IP65 210×310×110 $ 21.203 · exterior Roker PRG357 IP65
200×200×155 $ 44.419</td>
<td class="num gris">21.203</td><td class="num">14</td><td class="num gris">44.419</td><td class="num">29</td></tr>
<tr><td>Sondas DS18B20 estancas rearmadas con 3 m de cable y prensacable (6)</td>
<td class="num gris">~55.200</td><td class="num">36</td><td class="num gris">~55.200</td><td class="num">36</td></tr>
<tr><td>Sensores magnéticos de puerta cableados (2)</td>
<td class="num gris">9.492</td><td class="num">6</td><td class="num gris">9.492</td><td class="num">6</td></tr>
<tr><td>Envío a Santa Cruz, prorrateado</td>
<td class="num gris">~18.400</td><td class="num">12</td><td class="num gris">~18.400</td><td class="num">12</td></tr>
<tr><td>Armado + <strong>prueba de banco documentada con 25 m de cable</strong> + garantía de reposición
amortizada</td><td class="num gris">&nbsp;</td><td class="num">150</td><td class="num gris">&nbsp;</td><td class="num">150</td></tr>
<tr><td>Parte de plataforma del desarrollo: USD 1.000 repartidos en <strong>3</strong> módulos vendidos</td>
<td class="num gris">&nbsp;</td><td class="num">333</td><td class="num gris">&nbsp;</td><td class="num">333</td></tr>
<tr><td>Costo</td><td class="num gris">&nbsp;</td><td class="num">576</td><td class="num gris">&nbsp;</td><td class="num">591</td></tr>
<tr><td>Margen</td><td class="num gris">&nbsp;</td><td class="num">174</td><td class="num gris">&nbsp;</td><td class="num">174</td></tr>
<tr class="total"><td><strong>Precio</strong></td><td class="num gris">&nbsp;</td><td class="num">750</td>
<td class="num gris">&nbsp;</td><td class="num">765</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Los USD 15 de diferencia son la caja, exactos</span><h3>Margen absoluto idéntico: USD 174 en los dos</h3></div>
    <div class="cuerpo"><p>$ 44.419 − $ 21.203 = $ 23.216 = USD 15,1 al BNA vendedor 1.535. No se aprovechó la caja
    cara para meter margen: el que va afuera cuesta más porque su caja cuesta más, y eso es todo lo que hay para
    explicar si preguntan.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Márgenes bajaron: de 34 % a 23 %</span><h3>Tres motivos, ninguno reversible con marketing</h3></div>
    <div class="cuerpo"><p><strong>La plataforma se reparte entre 3 módulos en vez de 4</strong>: USD 250 → 333 por
    módulo (+83). <strong>La caja de interior real cuesta $ 21.203, no los ~$ 8.500 que asumió la v6.1</strong>
    (+8). <strong>A favor:</strong> se cae el renglón de los 25 m de cable de interconexión, USD 10 (−10). <strong>La
    plata de esta cuenta está en el abono (76 % de margen) y en la puesta en marcha</strong>, no en los equipos —
    exactamente el modelo de PLATA.md.</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>Por qué NO se subieron los unitarios para sostener el 4.600.</strong> Se podía: bastaba
poner el doble de exterior en 900 y el repuesto en 500 y nadie iba a auditar el número. <strong>No se hace.</strong>
El cliente que ve bajar el precio cuando baja el alcance cree el precio; el que ve el mismo total con un equipo
menos aprende que el número era blando y va a apretar en el abono, que es lo único que importa acá. <strong>Menos
equipos = menos plata, dicho en voz alta, es lo que hace creíble el 500/mes.</strong> El repuesto queda en USD 400
sin cambio, y ahora cubre el 100 % del parque con una sola caja (antes cubría 4 equipos de 2 tipos distintos): es el
renglón que más ganó con esta configuración.</p></div>
''')

# =================================================================== HOJA 9
hoja(u'''
<h2><span class="n">12</span>Puesta en marcha, USD 1.450</h2>
<table class="compacta"><thead><tr><th>Trabajo</th><th class="num" style="width:10%">h</th></tr></thead><tbody>
<tr><td>Sondas, rangos y umbrales por reefer + <strong>calibración de las 15 sondas</strong> contra referencia y
registro de offsets</td><td class="num">10</td></tr>
<tr><td><strong>Software del módulo doble: segunda puerta, segundo defrost con silenciado por reefer,
<code>SONDAS_MAX</code> a 8, validación del bus a 25 m</strong></td><td class="num">10</td></tr>
<tr><td>Registro exportable con código de verificación</td><td class="num">14</td></tr>
<tr><td>Panel multi-equipo y usuarios de lectura</td><td class="num">10</td></tr>
<tr><td>Puesta en marcha remota (alta, credencial, OTA verificada, prueba de puertas y defrost), pruebas de campo con
Andrés, runbook y capacitación — <strong>3 módulos</strong></td><td class="num">10</td></tr>
<tr><td>Salud de bus, histéresis de 3 barridos y <strong>verificación cruzada entre sondas</strong></td><td class="num">4</td></tr>
<tr class="total"><td><strong>Total a USD 25/h</strong></td><td class="num">58 h = USD 1.450</td></tr>
</tbody></table>
<p class="tabla-pie">Bajó de 1.500 (v6.1) a 1.450, y baja poco a propósito: se cae <strong>un</strong> módulo de alta
remota, credencial, OTA verificada y prueba de puertas y defrost (2 h menos, de 60 a 58 h). Todo lo demás es idéntico
con 3 módulos que con 4 — <strong>y el software del doble, que son 10 h, ahora hay que escribirlo igual pero lo usan
los tres equipos en vez de dos.</strong> <strong>Si @firmware dice que son más horas, salen del margen, no del
precio.</strong></p>

<div class="sep"></div>

<h2><span class="n">13</span>Servicio mensual: qué cuesta servir y qué se cobra</h2>
<table class="compacta"><thead><tr><th>Costo directo mensual</th><th class="num" style="width:16%">v2 (12 sondas)</th>
<th class="num" style="width:22%">v7.0 (15 sondas, 5 reed, 3 módulos)</th></tr></thead><tbody>
<tr><td>Supabase Pro</td><td class="num gris">25</td><td class="num">25</td></tr>
<tr><td>Reposición amortizada (módulos y sondas en garantía)</td><td class="num gris">10</td><td class="num">15</td></tr>
<tr><td>Soporte (2 h → 2,3 h a USD 25)</td><td class="num gris">50</td><td class="num">57</td></tr>
<tr><td>Informe mensual</td><td class="num gris">25</td><td class="num">25</td></tr>
<tr class="total"><td><strong>Total</strong></td><td class="num gris">110</td><td class="num">122</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="cita"><p><strong>Tarifa: USD 100 por reefer por mes × 5 = USD 500/mes</strong> (decisión de Matías,
4-sep, no se toca con la configuración nueva). Costo directo 122 → <strong>margen bruto USD 378 (76 %)</strong>.
Con el inicial en 4.115, <strong>el abono paga el equipamiento entero en 8,2 meses de margen</strong>: es el renglón
que sostiene la cuenta. La justificación, y es la que hay que decir si preguntan: <strong>mantenimiento del
servidor, custodia de los datos y seriedad del servicio</strong> — el registro que se entrega tiene que estar
disponible y ser defendible dentro de un año, y eso se paga todos los meses aunque no pase nada.</p></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Por reefer, no por caja</span><h3>El abono es proporcional a los reefers</h3></div>
    <div class="cuerpo"><p>5 reefers = 500, 6 = 600. Eso importa con módulos mezclados: <strong>el precio del servicio
    no depende de cuántas cajas haya</strong>, porque lo que se vigila y se registra son reefers. <strong>Cuando entre
    el sexto, los USD 100 adicionales son casi margen puro</strong> y el equipo ya está puesto.</p></div>
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
<strong>El tendido lo hace y lo paga el cliente, y no aparece en el documento que se manda.</strong> Ahora son
<strong>3 tiradas: 2 bajo techo y 1 a la intemperie</strong> (la del par de afuera, que está junto y debería ser la
más corta). Para las dos de adentro el número real es <strong>más bajo que esta cuenta</strong>, que se hizo para
caño rígido exterior; para la de afuera esta cuenta es la buena.</div>

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
  <li><strong>Saber el tamaño de lo que el cliente gasta por su lado</strong> (≈ USD 286 por tirada en el peor caso,
  bastante menos bajo techo y menos aún entre dos contenedores pegados). Si dicen «esto de la obra no lo teníamos
  previsto», la respuesta ya está: <strong>la configuración la describieron ellos</strong>, y compartir módulo es
  justamente lo que les ahorró un equipo.</li>
  <li><strong>Tener lista la variante de rescate.</strong> Si la obra los frena, <strong>no se pierde la venta</strong>:
  se ofrece un módulo por reefer, sin ninguna obra, con el mismo total. Está calculado en la v5.2 del archivo fuente
  (historial de git).</li>
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
<p>El fundamento es de caja: hay que comprar y armar <strong>4 módulos</strong> (3 + el repuesto) antes de ver un peso
del segundo tramo, y cobrar ese tramo a un contratista que todavía no tiene nombre. Con el 50 %
(<strong>USD 2.057,50 ≈ $ 3.158.000</strong>) la compra completa de materiales —<strong>≈ $ 375.000 con flete</strong>—
queda cubierta <strong>más de ocho veces</strong> antes de tocar un componente. Con el 25 % también alcanzaría para los
materiales; lo que no cubriría es el <strong>riesgo de cobranza del segundo tramo</strong>, que es lo que en realidad
se está financiando.</p>
<div class="box"><p>Los hitos siguen existiendo <strong>como compromiso de entrega con plazo</strong>, y así está
escrito en el documento del cliente: «no se facturan aparte, están incluidos en el precio». <strong>Punto para que
Matías confirme:</strong> cobrar antes de entregar los hitos es más cómodo para la caja y más exigente con la
palabra.</p></div>

<div class="sep"></div>

<h2><span class="n">16</span>Las dos formas de pagar, y por qué se cayó la tercera</h2>
<div class="grid2">
  <div class="card fuerte">
    <div class="cab"><span class="tag">A</span><h3>Equipos + servicio mensual</h3></div>
    <div class="cuerpo"><p>4.115 + 12 × 500 = <strong>USD 10.115</strong> el primer año; 6.000/año después;
    <strong>24 meses 16.115</strong>.</p></div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">B</span><h3>Anual adelantado, 10 % sobre el servicio</h3></div>
    <div class="cuerpo"><p>4.115 + (12 × 500) × 0,9 = 4.115 + 5.400 = <strong>USD 9.515</strong>; renovación
    5.400/año; <strong>24 meses 14.915</strong>. El descuento le ahorra <strong>USD 600</strong> el primer año y lo que
    compra es concreto: <strong>cero riesgo de cobranza durante 12 meses</strong> con un contratista que probablemente
    pague a 60-90 días, una factura en lugar de doce, y caja para armar los equipos. <em>Se perdió el USD 10.000
    redondo de la v6.1, y no se recupera inflando: la B ahora entra abajo de cinco cifras, que para un comprador con
    nivel de aprobación es todavía mejor argumento que un número redondo.</em></p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="nota"><p><strong>C, eliminada.</strong> <span class="neutro">Matías: «el de la inversión inicial no lo
ofrecería». Era la única que ponía USD ~4.115 nuestros en manos de un contratista a 1.500 km, sin poder retirar los
equipos y sin contrato con permanencia. <strong>No se vuelve a ofrecer sin contrato validado por contador y un cliente
con historial de pago.</strong> Con dos opciones el comprador elige; con tres se paraliza.</span></p></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Moneda y facturación</span><h3>USD, pago en pesos al BNA de la fecha de pago</h3></div>
    <div class="cuerpo"><p><strong>Sin validez en el PDF.</strong> Nota interna: revisar precios si pasan más de 6 meses
    desde el 4-sep. Antes de la cotización firme hay que saber: monotributo vs. RI, plazo de pago, si acepta la cláusula
    de moneda, quién firma. Se pregunta cuando la empresa tenga nombre. <strong>Sin cláusulas condicionales:</strong> el
    tendido es del cliente y el precio es firme.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Los dos números que cierran cualquier objeción de precio</span><h3>La pérdida y el competidor</h3></div>
    <div class="cuerpo"><p>Una pérdida de 3 t valuada al precio de novillo en pie ($ 4.181/kg, INMAG jul-2026) son
    <strong>$ 12,5 M: 16 meses de servicio</strong> al abono de USD 500 (≈ $ 767.500 por mes).</p>
    <p>testo Saveris 2-T2: USD 318 por unidad y mide <strong>un</strong> punto; para cubrir los 15 puntos de esta
    propuesta harían falta 15 unidades = <strong>USD 4.770</strong> antes de importación, sin nube, sin puerta, sin
    relé, sin defrost, sin repuesto en sitio — y se configura con una red WiFi y una clave, que es exactamente lo que
    este sitio no tiene. <strong>Y ninguna de esas unidades es apta para la intemperie sin gabinete adicional.</strong></p></div>
  </div>
</div>
''')

# =================================================================== HOJA 12
hoja(u'''
<h2><span class="n">17</span>Los 4 módulos: qué falta comprar y cuánto sale</h2>
<div class="sub"><strong>1 de exterior + 2 de interior + 1 de repuesto, los cuatro dobles.</strong> Sondas: 15
instaladas + 3 de repuesto = 18. Reed: 5 instalados + 1 de repuesto = 6. Defrost: 5 entradas (cable y bornera, sin
componente caro). Cruce contra el stock declarado (<code>BOM_KIT_V1.md</code> §1 y <code>BOM_CERRO_MORO.md</code> de
@hardware, tomando el número más bajo de cada rango, y <strong>reservando 3 ESP32 para las galgas de Dreyfus</strong>,
que es P0 de octubre).</div>

<table class="compacta"><thead><tr><th>Ítem</th><th class="num" style="width:11%">Hacen falta</th>
<th class="num" style="width:13%">Stock decl.</th><th class="num" style="width:8%">Faltan</th>
<th class="num" style="width:12%">Precio</th><th class="num" style="width:13%">A comprar</th></tr></thead><tbody>
<tr><td>ESP32 DevKit</td><td class="num gris">4 + 3 = 7</td><td class="num gris">4</td><td class="num">3</td><td class="num gris">$ 13.990</td><td class="num">$ 41.970</td></tr>
<tr><td>Sondas DS18B20</td><td class="num gris">18</td><td class="num gris">15</td><td class="num">3</td><td class="num gris">$ 4.388</td><td class="num">$ 13.164</td></tr>
<tr><td><strong>Caja IP65 de intemperie</strong> Roker PRG357 (el módulo de afuera)</td><td class="num gris">1</td>
<td class="num gris">0 de esa medida</td><td class="num">1</td><td class="num gris">$ 44.419</td><td class="num">$ 44.419</td></tr>
<tr><td>Gabinetes de interior para los 3 dobles restantes (2 + repuesto)<span class="soft det">3 de 165×165 en stock
— medida sin verificar para 6 sondas + 2 puertas + 2 defrost</span></td><td class="num gris">3</td><td class="num gris">3 de 165×165</td>
<td class="num">3 (peor caso)</td><td class="num gris">$ 21.203</td><td class="num">$ 63.609</td></tr>
<tr><td>Fuentes 5 V <strong>2 A</strong></td><td class="num gris">4</td><td class="num gris">5, amperaje sin verificar</td>
<td class="num">4 (peor caso)</td><td class="num gris">$ 7.980</td><td class="num">$ 31.920</td></tr>
<tr><td>Módulos de relé 2 canales</td><td class="num gris">4</td><td class="num gris">10</td><td class="num">0</td><td class="num gris">—</td><td class="num">$ 0</td></tr>
<tr><td>Reed / sensor de puerta</td><td class="num gris">6</td><td class="num gris">10</td><td class="num">0</td><td class="num gris">—</td><td class="num">$ 0</td></tr>
<tr><td>Consumibles del §3.1 reescalados a 4 módulos<span class="soft det">plaquetas, borneras, tiras hembra, R 2k2
y 1k, 10 k, 100 nF, electrolíticos, separadores, prensacables por las entradas del estanco</span></td>
<td class="num gris">—</td><td class="num gris">—</td><td class="num gris">—</td><td class="num gris">—</td><td class="num">$ 120.000</td></tr>
<tr><td>Cable de 3 hilos para rearmar 18 sondas a 3 m + termocontraíble</td><td class="num gris">—</td>
<td class="num gris">—</td><td class="num gris">—</td><td class="num gris">—</td><td class="num">$ 40.000</td></tr>
<tr><td><strong>Cable de interconexión entre reefers</strong></td><td class="num gris">—</td>
<td class="num gris">—</td><td class="num gris">—</td><td class="num gris"><strong>lo compra el cliente</strong></td><td class="num">$ 0</td></tr>
<tr class="total"><td colspan="5"><strong>TOTAL</strong></td><td class="num">≈ $ 355.000</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Con flete</span><h3>≈ $ 375.000 ≈ USD 244</h3></div>
    <div class="cuerpo"><p>Si las 3 cajas de stock pasan la medición <code>M9</code> de @hardware, baja $ 63.609 →
    ≈ $ 291.000 (USD 190); si además las fuentes de stock son de 2 A, baja otros $ 31.920. <strong>Contra el
    anticipo del 50 % (USD 2.057,50 ≈ $ 3.158.000), la compra completa es el 12 %.</strong> No hay problema de plata
    ni de cantidades. Contra la v6.1 (≈ $ 430.000): <strong>−$ 55.000</strong>, y eso con la caja de exterior real a
    $ 44.419 en vez de los $ 22.000 mal presupuestados — el equipo que se cae paga con creces la corrección del
    BOM.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Plazo de entrega</span><h3>La caja IP65 de intemperie se pide primero</h3></div>
    <div class="cuerpo"><p>Es el renglón de mayor plazo de entrega, y ya hay una en el sitio, que es la prueba de
    campo. Las 3 de 165×165 que hay en stock <strong>no sirven para los dobles</strong> (6 sondas + 2 puertas + 2
    defrost + fuente no entran cómodos): quedan para las demos de Bahía.</p></div>
  </div>
</div>
''')

# =================================================================== HOJA 13
hoja(u'''
<h2><span class="n">18</span>El camino a los hitos 1 y 2, en semanas desde la aceptación</h2>
<div class="cita"><p><strong>El plan arranca cuando aceptan, no antes.</strong> Semana 0 = aceptación + anticipo del
50 %. Hasta que eso pase <strong>no se compra, no se arma y no se despacha nada</strong>, y a Andrés no se le pide que
reserve ninguna ventana: trabaja por turnos de 15 días y no es él quien aprueba.</p></div>

<table class="compacta"><thead><tr><th>Paso</th><th class="num" style="width:24%">Plazo desde la aceptación</th>
<th style="width:18%">Quién</th></tr></thead><tbody>
<tr><td>Conteo del stock real + las mediciones del §8.1 del BOM y la <code>M9</code> (interior de las 3 cajas,
amperaje de las fuentes, relé con IN al aire)</td><td class="num">semana 0</td><td>Gonza</td></tr>
<tr><td>Compra del faltante —<strong>la caja de exterior primero</strong>— y rearmado de sondas a 3 m</td><td class="num">semana 0-1</td><td>Gonza / Matías</td></tr>
<tr><td>Despacho de 2 sondas para el equipo ya instalado (encomienda, 5-8 días hábiles)</td><td class="num">semana 1</td><td>—</td></tr>
<tr><td><strong>Cierre de las correcciones del firmware doble</strong> (auditoría 4-sep, APTO CON CORRECCIONES) + 2ª
puerta, 2º defrost por reefer, <code>SONDAS_MAX</code> a 8 — <strong>ahora bloquea a los 3 módulos</strong></td><td class="num">semana 1-2</td><td>Matías / @firmware</td></tr>
<tr><td>Alta, calibración remota, rangos y primera alerta real</td><td class="num">semana 2</td><td>Andrés + Matías</td></tr>
<tr class="total"><td><strong>HITO 1</strong></td><td class="num">semana 2</td><td>—</td></tr>
<tr><td>Armado de los 4 módulos + <strong>prueba de banco de los tres con 25 m de cable</strong> (~16 h)</td><td class="num">semana 1-2</td><td>Gonza / Sergio</td></tr>
<tr><td>Despacho de los 4 bultos (3 módulos + repuesto) a Cerro Moro</td><td class="num">semana 2</td><td>—</td></tr>
<tr><td><strong>Tendido del cable en los 3 pares</strong> (el de afuera, con cable apto exterior)</td><td class="num">semana 2-3</td><td><strong>cliente</strong></td></tr>
<tr><td>Montaje de los módulos por personal del campamento</td><td class="num">semana 3-4</td><td>campamento</td></tr>
<tr><td>Alta y calibración de las 12 sondas nuevas (las 3 de <code>REEFER_01_SCZ</code> ya quedaron en el hito 1)</td><td class="num">semana 4</td><td>Matías</td></tr>
<tr class="total"><td><strong>HITO 2</strong> (los 5 reefers reportando + una semana sin falsas alarmas)</td><td class="num">semana 5</td><td>—</td></tr>
</tbody></table>
<p class="tabla-pie"><span class="neutro"><strong>Nada de esta tabla se adelanta:</strong> las sondas, la compra, el
armado y el despacho arrancan con la aceptación y el anticipo. No hay una sola acción para hoy.</span></p>

<div class="sep-ch"></div>

<div class="nota"><p><strong>El riesgo que hay que decir en voz alta: el hito 2 está apretado y ahora tiene DOS
dependencias, no una.</strong> <span class="neutro">La semana sin falsas alarmas arranca cuando los 3 módulos
reportan —alrededor de la semana 4— y el hito vence en la 5: <strong>una semana, sin colchón</strong>. Y depende de
(a) <strong>una obra ajena</strong> —el tendido del cliente, ahora en tres pares— y (b) <strong>el firmware doble,
que ya no tiene plan B</strong>: en la v6.1 los 2 simples reportaban igual con lo que ya anda. <strong>Matías no
debería prometer el hito 2 por teléfono con más firmeza que la que dice el papel.</strong></span></p></div>

<div class="box"><p><strong>Por qué se puede empezar a armar antes de la orden de compra, sin exponer un peso
nuevo.</strong> Los kits <strong>ya estaban planificados como las unidades de demostración del plan comercial de
Bahía</strong>. Si Cerro Moro no compra, no quedan colgados: van a su destino original. <strong>La contracara para el
Director: si Cerro Moro compra, Bahía se queda sin demos</strong> — aunque ahora son <strong>4 módulos y no
5</strong>, así que el golpe es menor. Recomendación: la reposición de los kits de Bahía se dispara en el mismo
pedido que la orden de compra, no después.</p></div>
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
sondas del equipo instalado</strong></td></tr>
<tr><td><strong>2</strong> — Los 3 módulos y los 5 reefers reportando; nada se pierde, nada sobra</td>
<td>E1: buffer offline, alertas encoladas, alerta de sonda caída, vigía de equipo mudo, discriminador de bus +
histéresis, <strong>detección de sonda que se desvía de las otras del mismo reefer</strong>, <strong>segunda puerta y
segundo defrost con silenciado por reefer en los dobles</strong></td><td class="num gris">sem. 2</td><td class="num">sem. 5</td>
<td>Los 3 módulos montados con sus 15 sondas calibradas; desenchufar una sonda y que llegue la alarma; cortar la red
20 min sin perder lecturas; abrir una puerta 4 min y que avise; <strong>forzar el defrost de un reefer de un par y
verificar que el otro del mismo módulo sigue alarmando</strong>; <strong>una semana sin falsas alarmas</strong></td></tr>
<tr><td><strong>3</strong> — Acceso seguro</td><td>E2: RLS cerrada, credencial por módulo, secretos fuera del binario,
revocar claves quemadas</td><td class="num gris">sem. 5</td><td class="num">sem. 10</td>
<td>Con la clave vieja no se escribe; todos los módulos siguen reportando</td></tr>
<tr><td><strong>4</strong> — Actualización a distancia</td><td>E3: OTA con manifiesto inmutable</td>
<td class="num gris">sem. 10</td><td class="num">sem. 12</td>
<td>Tres actualizaciones seguidas por aire al primer intento, en todos los módulos</td></tr>
<tr><td><strong>5</strong> — Panel e informe</td><td>E4: usuarios de lectura, vista de los reefers, exportación con
código, informe mensual automático, <strong>comando de relé desde el panel</strong></td><td class="num gris">sem. 12</td>
<td class="num">sem. 15</td><td>Un usuario de la empresa entra solo, baja el informe y acciona una salida desde el
panel</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="nota"><p><strong>El hito 2 es el apretado:</strong> <span class="neutro">la semana sin falsas alarmas
arranca cuando los 3 módulos reportan, alrededor de la semana 4, y vence en la 5. <strong>Sin colchón, y con el tendido
del cliente en el camino crítico de los dos pares de adentro.</strong></span></p></div>

<div class="box"><p>Lo que hoy está roto y cada hito arregla (llave maestra en el binario, datos perdidos sin red,
umbral en 50 °C, equipo muerto que no avisa, OTA que entra 1 de 4) está en <code>AUDITORIA_HALLAZGOS.md</code>; no
cambió.</p></div>
''')

# =================================================================== HOJA 15
hoja(u'''
<h2><span class="n">20</span>La relación con Andrés — para que Matías decida</h2>
<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Lo que cambió</span><h3>De contacto en sitio a referidor de hecho</h3></div>
    <div class="cuerpo"><p>En la v1 Andrés era el contacto en sitio de un cliente y la regla era simple:
    <strong>ningún pago ni beneficio ligado a que su empleador compre</strong>. Ahora es él quien <strong>ofrece y
    presenta</strong> la propuesta a una tercera empresa que él elige.</p></div>
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
contacto en sitio, contarle el caso como logro suyo</td>
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
<p><strong>Lo bueno de esta vuelta:</strong> a Andrés le llega <strong>exactamente el sistema que él describió</strong>,
armado sobre datos que dio él (los metros, el caño, la intemperie, el reparto adentro/afuera). Ya no hay que explicarle
ningún «no». Eso lo deja bien parado adentro, que es lo único que él pidió para sí.</p></div>
''')

# =================================================================== HOJA 16
hoja(u'''
<h2><span class="n">21</span>Lo que quedó abierto, antes de mandar</h2>
<div class="sub">17 pendientes. <strong>Ninguno es logística:</strong> hasta que no haya aceptación y anticipo no se
compra, no se arma y no se despacha nada.</div>
<table class="compacta"><thead><tr><th style="width:5%">&nbsp;</th><th>Pendiente</th><th style="width:20%">Quién decide</th></tr></thead><tbody>
<tr><td class="num">1</td><td><strong>Los números:</strong> exterior 765 · interior 750 × 2 = 1.500 · repuesto 400 ·
puesta en marcha 1.450 · <strong>inicial 4.115</strong> · abono <strong>500/mes</strong> ·
B = <strong>9.515</strong>. Márgenes 23 % / 76 %. <strong>¿Van?</strong></td><td><strong>Matías</strong></td></tr>
<tr><td class="num">2</td><td>El sexto reefer entra a <strong>USD 260</strong> (canal libre de su módulo doble, sin equipo
nuevo) + USD 100/mes. Está escrito en el documento del cliente. <strong>¿Va así?</strong></td><td><strong>Matías</strong></td></tr>
<tr><td class="num">3</td><td>Riesgo de las tres tiradas de 20-25 m, una a la intemperie: <strong>asumido con
conocimiento</strong>. Confirmar que la posición del 1k queda en la placa.</td><td>@esquematico</td></tr>
<tr><td class="num">4</td><td><strong>El firmware de módulo doble bloquea a los 3 módulos</strong> (2ª puerta, 2º
defrost con silenciado por reefer, <code>SONDAS_MAX</code> a 8). Auditado, APTO CON CORRECCIONES: <strong>cerrar
las correcciones es lo que define si se despacha</strong>. Si son más horas, sale del margen, no del
precio.</td><td>@firmware</td></tr>
<tr><td class="num">5</td><td>La <strong>caja IP65 de intemperie no está en stock</strong>: renglón de mayor plazo,
ya se pidió una y está en sitio. Confirmar medida y precio de las siguientes. Las 3 de 165×165 no sirven para los
dobles.</td><td>@hardware</td></tr>
<tr><td class="num">6</td><td>Compra de materiales <strong>≈ $ 355.000 ($ 375.000 con flete)</strong>, cruzada contra
stock. Reservados 3 ESP32 para las galgas de Dreyfus (P0 de octubre).</td><td>Matías / @hardware</td></tr>
<tr><td class="num">7</td><td>Contar stock y hacer las mediciones del §8.1 del BOM y la <code>M9</code> (amperaje real
de las fuentes, relé con IN al aire, interior de las 3 cajas) <strong>antes de comprar</strong>.</td><td>@hardware</td></tr>
<tr><td class="num">8</td><td><strong>Decisión de portfolio:</strong> los kits son los mismos que iban a ser las demos de
Bahía. Si Cerro Moro compra, Bahía se queda sin demos → reposición en el mismo pedido que la OC.</td><td><strong>Director</strong></td></tr>
<tr><td class="num">9</td><td>Preguntarle a Andrés <strong>cuál de los 4 de adentro está fuera de servicio</strong>:
define el emparejamiento y que el canal libre quede en un módulo instalado y andando.</td><td>Matías</td></tr>
<tr><td class="num">10</td><td><strong>Verificación cruzada entre sondas: hoy NO existe.</strong> Vendida en el hito 2. Si
no se puede cumplir, sacar el punto 3 del bloque «por qué 3 sondas».</td><td>Matías / @firmware</td></tr>
<tr><td class="num">11</td><td><strong>Accionamiento del relé desde el panel: tampoco existe.</strong> Hito 5.</td><td>@firmware</td></tr>
<tr><td class="num">12</td><td>El sensor de puerta viene <strong>deshabilitado por defecto</strong>: que quede en la orden
de armado habilitarlo y probar <strong>las dos</strong> puertas en los dobles.</td><td>@firmware</td></tr>
<tr><td class="num">13</td><td><strong>Cobertura de red en los 3 puntos.</strong> Si alguno queda corto, repetidor
<strong>antes</strong> de despachar.</td><td>Andrés</td></tr>
<tr><td class="num">14</td><td>La caja de exterior que ya está en el sitio <strong>es la prueba de campo</strong>: pedirle
a Andrés una foto después del primer temporal. Evidencia gratis para la venta siguiente.</td><td>Matías</td></tr>
<tr><td class="num">15</td><td><strong>Andrés:</strong> opción 1, 2 o 3 de la hoja anterior, y preguntarle para quién
trabaja.</td><td><strong>Matías</strong></td></tr>
<tr><td class="num">16</td><td><strong>PDF:</strong> un solo documento de 2 páginas A4, marca Termovigía, sin logo ajeno,
sin «Para:», sin validez, <strong>sin mencionar material de gabinete</strong>.</td><td>@diseno · <strong>hecho</strong></td></tr>
<tr><td class="num">17</td><td>Monotributo vs. RI: se pregunta cuando la empresa tenga nombre.</td><td>Matías</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<h3>Fuentes consultadas</h3>
<ul class="lista">
  <li>Alcance del bus, pull-ups, tierras entre contenedores y límite prudente de 15 m:
  <code>frioseguro\\hardware\\ALCANCE_1WIRE.md</code> (@muestreador), §2.6.</li>
  <li>Costo por equipo y stock declarado: <code>BOM_KIT_V1.md</code> rev B (@hardware), precios ML verificados el
  2-sep-2026.</li>
  <li>Estado real y auditoría: <code>ESTADO_HONESTO.md</code> · <code>AUDITORIA_HALLAZGOS.md</code>.</li>
  <li>Qué hace hoy el firmware con sondas, puerta, relé y defrost (leído el 3-sep-2026):
  <code>firmware_revival/sondas.h</code> línea 31 · <code>config.h</code> 67-150 · <code>.ino</code> 369-375, 483-488,
  804-944 · <code>comandos_nube.h</code> (sin comando de relé).</li>
  <li>Contrato base: <code>MATI-HQ\\comercial\\CONTRATO_TERMOVIGIA_v4.md</code>.</li>
  <li>Precios de canalización, 1-Wire AN148, testo Saveris 2-T2, novillo INMAG, dólar BNA vendedor 1.535, Supabase Pro
  y el Código de Conducta de Proveedores: enlaces conservados en la v5.2 del archivo fuente (historial de git).</li>
</ul>
''')

# =================================================================== salida
HTML = (u'<!DOCTYPE html>\n<html lang="es-AR">\n<head>\n<meta charset="utf-8">\n'
        u'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        u'<title>INTERNO — Cerro Moro v7.0: 3 módulos, la configuración del sitio y los pendientes</title>\n'
        u'<link rel="stylesheet" href="estilo.css">\n</head>\n<body>\n<div class="doc">\n\n'
        + u'\n'.join(HOJAS) + u'\n</div>\n</body>\n</html>\n')

if __name__ == "__main__":
    io.open(os.path.join(AQUI, SALIDA), "w", encoding="utf-8").write(HTML)
    print("escrito %s (%d hojas)" % (SALIDA, len(HOJAS)))
