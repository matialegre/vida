# -*- coding: utf-8 -*-
"""Arma el documento INTERNO de Cerro Moro (v6.1, 4-sep-2026).

Reemplaza a interno_v5.fuente.html (escrito a mano para la v5.2): la v6.1 cambio la
configuracion entera (4 modulos: 2 simples de exterior + 2 dobles de interior, 3 sondas
por reefer, 4.600 / 500 / sexto a 260), asi que el interno se genera y no se parchea.

Copy: PROPUESTA_PANAMERICAN_CERRO_MORO.md v6.1, PARTES 2 a 7 + anexos. Nada inventado:
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
    <b>Interno · v6.1</b>
    ''' + FECHA + u'''<br>
    Ref. ''' + REF + u'''
  </div>
</div>

<div class="hero">
  <div class="kicker">Cerro Moro (Santa Cruz) · 6 reefers, 5 en servicio</div>
  <h1>Cuatro módulos:<br>dos <em>a la intemperie</em> y dos <em>dobles</em> bajo techo</h1>
  <div class="bajada">La configuración la describió Andrés el 4-sep y es la que manda: 2 reefers afuera con un
  módulo cada uno en caja estanca IP65, y los 4 de adentro cubiertos con 2 módulos dobles.</div>
  <div class="meta">
    Copy del cliente: <b>PARTE 1</b> de <b>PROPUESTA_PANAMERICAN_CERRO_MORO.md</b> (v6.1, @comercial).
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
      <p>El mensaje completo, listo para copiar tal cual. Arranca con <em>«quedó armado tal cual me lo
      describiste»</em> y <strong>no le pide nada</strong>: trabaja por turnos de 15 días y no es él quien
      aprueba.</p>
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
  <div class="cifra"><div class="big">4.600</div><div class="lb">USD inicial<br>2×600 + 2×750 + repuesto 400 + puesta en marcha 1.500</div></div>
  <div class="cifra"><div class="big">500</div><div class="lb">USD por mes<br>USD 100 por reefer × 5, sin escalón</div></div>
  <div class="cifra"><div class="big">4</div><div class="lb">módulos para 6 reefers<br>2 simples de exterior + 2 dobles de interior</div></div>
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
    <div class="cab"><span class="tag">Cambio 1</span><h3>La configuración la fija el sitio, no la planilla</h3></div>
    <div class="cuerpo">
      <p>Andrés informó que <strong>2 reefers están afuera y 4 adentro</strong>. Eso resuelve de una la discusión
      de las v4 y v5 sobre compartir o no compartir equipos: <strong>se comparte donde se puede compartir
      bien</strong> (los de adentro, bajo techo, con la tirada corta y protegida) y <strong>no se comparte donde no
      conviene</strong> (los de afuera, cada uno con su módulo estanco). No es una concesión ni un descarte: es la
      solución que cae sola cuando aparece el dato real.</p>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Cambio 2</span><h3>Cuatro módulos, dos precios</h3></div>
    <div class="cuerpo">
      <p><strong>2 simples de exterior a USD 600</strong> + <strong>2 dobles de interior a USD 750</strong> =
      <strong>USD 2.700 en equipos</strong>, más repuestos <strong>400</strong> y puesta en marcha
      <strong>1.500</strong> = <strong>USD 4.600</strong>. Era 4.540 en la v5.2: <strong>+USD 60, un 1,3 %</strong>,
      y el motivo es uno solo y se puede decir en voz alta — la caja estanca de exterior cuesta casi tres veces la
      común, y el kit de repuesto ahora es un módulo doble.</p>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Cambio 3</span><h3>La obra de cable se achicó sola</h3></div>
    <div class="cuerpo">
      <p>Solo hay <strong>dos tiradas</strong>, las de los pares de adentro, <strong>bajo techo</strong>. Los dos
      módulos de afuera no tienen ni un metro de cable entre contenedores. Sigue <strong>a cargo del
      cliente</strong>, y ahora es visiblemente menos trabajo del que Andrés tenía en la cabeza cuando habló del
      caño Daisa.</p>
    </div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Cambios 4 y 5</span><h3>Tres sondas, y el sexto reefer es un canal libre</h3></div>
    <div class="cuerpo">
      <p><strong>Tres sondas por reefer, no cuatro</strong> (decisión de Matías): 15 sondas en servicio, y el
      argumento de por qué más de una sigue valiendo entero (peor punto, redundancia, verificación cruzada — tres es
      el mínimo que permite saber <strong>cuál</strong> se desvió).</p>
      <p>El sexto está adentro, fuera de servicio, y su módulo doble <strong>ya va instalado</strong>: cuando vuelva,
      <strong>USD 260</strong> de sondas, puerta y defrost, <strong>+USD 100/mes</strong>. Sin equipo nuevo, sin
      renegociar nada.</p>
    </div>
  </div>
</div>

<div class="sep"></div>

<h2><span class="n">02</span>WhatsApp para Andrés — copiar desde acá</h2>
<div class="sub" style="margin:-1.5mm 0 4mm">Lo manda Matías. Va tal cual: arranca devolviéndole la configuración
que él mismo describió. <strong>No le pide nada</strong> y <strong>no menciona el material de la caja ni cómo se
fabrica</strong>.</div>

<div class="wsp-tit">MENSAJE COMPLETO</div>
<div class="wsp">Andrés, quedó armado tal cual me lo describiste: los 2 reefers que están
a la intemperie llevan un módulo cada uno, en caja estanca IP65 para
exterior, y los 4 de adentro van con 2 módulos, uno cada par. Cuatro
módulos en total.

Por cada reefer: 3 sondas adentro, sensor de puerta y la señal de
defrost, así no suena la alarma cada vez que descongela.

El cable entre los dos reefers de cada par de adentro y su tendido
corren por cuenta de ustedes, eso lo ven ahí. Los de afuera no llevan ni
un metro de cable entre contenedores. Los módulos dobles los pruebo acá
en el banco con 25 metros de cable puestos antes de despacharlos.

Una cosa más: el reefer que está fuera de servicio queda emparejado con
uno que anda, así el módulo ya va puesto y el día que vuelva se le suman
las sondas nomás, sin equipo nuevo.

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
<td>2 afuera / 4 adentro, dos tiradas bajo techo: le confirma que se entendió el sitio.</td></tr>
<tr><td class="num">c</td><td><strong>El tendido queda dicho en una línea, con algo a cambio y con el alivio adelante</strong></td>
<td>Son dos tiradas, bajo techo, y nosotros mandamos el cable. No es una carga, es un reparto.</td></tr>
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
  <li><strong>Decilo en una frase:</strong> «los dos de afuera llevan cada uno su módulo estanco; los cuatro de
  adentro se cubren con dos. Tres sondas adentro de cada reefer, te avisa al celular si se sale de rango o si queda
  la puerta abierta, y arma el registro mensual solo.»</li>
  <li><strong>Si preguntan por el cable:</strong> «solo hay dos tiradas y las dos son adentro, bajo techo. El cable
  lo mandan ellos y dicen cómo va; el caño lo pasamos nosotros. Los de la intemperie no llevan cable entre
  contenedores.»</li>
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
<tr><td><strong>2 reefers están a la intemperie y 4 están adentro, bajo techo</strong></td><td>Andrés a Matías, <strong>4-sep</strong>. Es el dato que define toda esta versión</td></tr>
<tr><td><strong>De los 4 de adentro, uno está fuera de servicio: hoy hay 5 reefers activos</strong></td><td>Matías, 4-sep</td></tr>
<tr><td>Ya se mandó al sitio una <strong>caja estanca IP65 apta para exterior</strong></td><td>Matías, 4-sep</td></tr>
</tbody></table>

<div class="sep"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">De Andrés</span><h3>Lo que sigue abierto — ninguna frena el envío</h3></div>
    <div class="cuerpo">
      <ul>
        <li><strong>¿La red del campamento llega bien a los 4 puntos donde van los módulos?</strong> Si alguno queda
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
      dos pares de adentro</strong> los hace personal del campamento (sin personal nuestro en sitio no corresponde ART
      ni legajo de contratista).</p>
      <p><strong>El comprador no es Pan American Silver:</strong> es «una empresa» que Andrés todavía no identifica.
      Por eso el documento del cliente va sin destinatario, sin logo ajeno y sin nombrar a la minera.</p>
    </div>
  </div>
</div>
''')

# =================================================================== HOJA 5
hoja(u'''
<h2><span class="n">06</span>Registro: cómo quedó resuelta la discusión de compartir o no compartir</h2>
<div class="sub">Las v4 y v5 discutieron durante dos versiones si convenía un equipo por reefer o uno cada dos. El
dato de Andrés del 4-sep —2 afuera, 4 adentro— <strong>cerró la discusión sin que hubiera que elegir bando</strong>.
Queda escrito por qué, para poder defenderlo si alguien pregunta.</div>

<div class="cita"><p><strong>La regla que quedó, y es defendible con una frase:</strong> <em>se comparte módulo donde
compartir es barato y seguro (adentro, bajo techo, tirada corta y protegida), y no se comparte donde no lo es (a la
intemperie, donde el cable tendría que salir a cielo abierto entre dos contenedores)</em>.</p></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Los 2 de afuera</span><h3>Con módulo propio</h3></div>
    <div class="cuerpo"><p>Cero cable entre contenedores en la zona más hostil, <strong>cero obra</strong>, y si un
    módulo cae queda <strong>un</strong> reefer ciego, no dos. Se paga con una caja más cara, y vale la pena.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Los 4 de adentro</span><h3>De a pares</h3></div>
    <div class="cuerpo"><p>Dos módulos en vez de cuatro, la tirada es corta y bajo techo, y <strong>el módulo del par
    donde está el reefer fuera de servicio ya queda comprado con el canal libre</strong> — el sexto reefer entra
    después por USD 260 en vez de por un equipo entero.</p></div>
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
  <li><strong>Los dos módulos dobles se prueban en banco con 25 m de cable real antes de despachar</strong>, con las
  6 sondas colgadas. No sale nada que no haya cerrado a la distancia real.</li>
  <li><strong>Especificación de cable</strong> (par trenzado exterior, el par DQ/GND junto en todo el recorrido, sin
  empalmes, canalizado): <strong>queda interna</strong>, no se manda al cliente — desde el 4-sep el cable no lo
  provee Matías, así que no corresponde especificarle un tipo que no le vamos a mandar.</li>
  <li><strong>El riesgo se redujo a la mitad respecto de la v6.0:</strong> ahora son <strong>2 tiradas y las dos bajo
  techo</strong>, no tres a la intemperie. Menos metros expuestos, menos humedad en las uniones, menos diferencia de
  potencial entre masas.</li>
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
<div class="sub">Verificado en el código el 3-sep-2026.</div>
<table class="compacta"><thead><tr><th style="width:15%">Función</th><th class="num" style="width:8%">Simple<br>(ext.)</th>
<th class="num" style="width:8%">Doble<br>(int.)</th><th>Qué hace el firmware hoy</th><th style="width:20%">Evidencia</th></tr></thead><tbody>
<tr><td>Sondas DS18B20</td><td class="num">3</td><td class="num">6</td>
<td>Cada una identificada por ROM de 64 bits y reportada por separado; enganche en caliente; aviso si se desconecta;
<strong>offset de calibración por sonda en NVS</strong>. <strong><code>SONDAS_MAX</code> está en 4: para el doble hay
que subirlo a 8</strong> — es el tamaño de un arreglo, una línea.</td>
<td><code>sondas.h</code>: <code>sondasEscanear</code>, <code>sondasLeer</code>, <code>sondasCalibrar</code>; línea 31</td></tr>
<tr><td><strong>Verificación cruzada entre sondas</strong></td><td class="num gris">—</td><td class="num gris">—</td>
<td><strong>NO existe.</strong> <code>sondasCalibrar()</code> iguala las sondas en un momento dado; el lazo de lectura
<strong>no compara sondas entre sí</strong> ni alerta por deriva.</td>
<td>ídem. Vendida en el <strong>hito 2</strong>, con la aclaración escrita en la página del cliente</td></tr>
<tr><td>Sensor de puerta</td><td class="num">1</td><td class="num">2</td>
<td>Implementado <strong>para una sola puerta</strong>: GPIO5, alerta por puerta abierta &gt; 180 s, suprime la alerta
de temperatura mientras está abierta. Viene deshabilitado por defecto (<code>SENSOR_DOOR_ENABLED false</code>).
<strong>La segunda puerta hay que agregarla, solo en el doble.</strong></td>
<td><code>config.h</code> 72-74, 105, 119 · <code>.ino</code> 804-890</td></tr>
<tr><td>Entrada de defrost</td><td class="num">1</td><td class="num">2</td>
<td>Implementada <strong>para una sola entrada</strong>: GPIO33, NA/NC configurable, deshabilita alertas durante el
ciclo con 30 min de enfriamiento. <strong>La segunda hay que agregarla, y tiene que silenciar solo el reefer que
descongela.</strong></td>
<td><code>config.h</code> 91-96, 122 · <code>.ino</code> 54-55, 100-101, 872-878</td></tr>
<tr><td>Salidas a relé</td><td class="num">2</td><td class="num">2</td>
<td><strong>1 gobernada</strong>: GPIO26, se activa sola con la alerta si <code>relayEnabled</code>. La segunda queda
cableada y disponible. <strong>El accionamiento manual desde el panel NO existe.</strong></td>
<td><code>config.h</code> 76-77, 140-150 · <code>.ino</code> 369-375, 483-488, 915-944 · <code>comandos_nube.h</code>
sin comando de relé → <strong>hito 5</strong></td></tr>
<tr><td>Gabinete</td><td><strong>IP65 estanco de exterior</strong></td><td>Gabinete común de interior</td><td>—</td>
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
    <div class="cab"><span class="tag">Ventaja no obvia</span><h3>La mitad del sistema no necesita una línea nueva</h3></div>
    <div class="cuerpo"><p><strong>Los 2 módulos de exterior corren el firmware que ya anda hoy.</strong> Solo los dos
    dobles necesitan el software de doble reefer: <strong>si ese software se atrasa, la mitad del sistema igual
    arranca</strong>.</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="nota"><p><strong>Detalle que no se puede pasar por alto en el diseño del doble:</strong>
<span class="neutro">el defrost de un reefer <strong>no puede silenciar las alarmas del otro</strong>. Hoy el defrost
deshabilita <em>todas</em> las alertas del equipo. En el módulo doble tiene que silenciar <strong>solo las sondas del
reefer que está descongelando</strong>. Está dentro de las horas de la puesta en marcha y es lo que hay que probar sí
o sí antes del hito 2.</span></p></div>

<div class="box"><p><strong>Orden de armado:</strong> línea <code>entrega_scz</code>/<code>firmware_revival</code>
(identificación por ROM), <strong>no</strong> <code>firmware_modular</code> (lee por índice: si cae una sonda, la otra
se reporta con el nombre equivocado). Pull-up 2k2 con posición alternativa de 1k, 3 hilos (nada de parasite power),
100 nF + 10 µF al pie de la sonda más lejana de cada rama. <strong>Habilitar <code>SENSOR_DOOR_ENABLED</code>, probar
puertas y defrost, y correr la prueba de banco con 25 m de cable en los dos dobles antes de despachar.</strong></p></div>
''')

# =================================================================== HOJA 7
hoja(u'''
<h2><span class="n">08</span>Lo que se instala, y quién</h2>
<div class="grid3">
  <div class="card fuerte">
    <div class="cab"><span class="tag">×2 · USD 600</span><h3>Módulo simple de exterior</h3></div>
    <div class="cuerpo"><p><strong>Gabinete estanco IP65 apto para exterior</strong> 200×200×80, fuente de 5 V 2 A,
    plaqueta con borneras a tornillo, ESP32 en zócalo, módulo de 2 relés, <strong>prensacables en todas las
    entradas</strong>, 3 sondas DS18B20 estancas, 1 reed de puerta.</p></div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">×2 · USD 750</span><h3>Módulo doble de interior</h3></div>
    <div class="cuerpo"><p>Gabinete común 200×200×80, misma electrónica, 6 sondas, 2 reed, y <strong>25 m de par
    trenzado exterior</strong> para llegar al reefer vecino.</p></div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">×1 · USD 400</span><h3>Kit de repuesto</h3></div>
    <div class="cuerpo"><p>Un <strong>módulo doble</strong> completo —cubre a cualquiera de los cuatro— + 3 sondas +
    1 reed. Queda en el campamento.</p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>Montaje: Andrés (o quien la empresa designe)</strong>, con kit preconfigurado y probado
en banco + videollamada. Dos pasajes a Santa Cruz, alojamiento, inducción y 5 días de ingeniero rondan los
<strong>$ 2.500.000</strong>, y Matías no puede viajar en octubre (parada de Dreyfus). <strong>Eso es lo que esta
propuesta no cobra.</strong></p></div>

<div class="nota"><p><strong>Intemperie:</strong> <span class="neutro">en el documento del cliente se dice
«gabinete estanco IP65 apto para exterior» <strong>y nada más</strong>. Ni material, ni proceso de fabricación. Ni en
el PDF ni en el WhatsApp.</span></p></div>

<div class="sep"></div>

<h2><span class="n">09</span>Los riesgos técnicos abiertos</h2>
<table class="compacta"><thead><tr><th style="width:5%">&nbsp;</th><th style="width:30%">Riesgo</th><th>Estado</th></tr></thead><tbody>
<tr><td class="num">1</td><td><strong>Los dos buses de 20-25 m de los pares de adentro</strong></td>
<td>Riesgo asumido, mitigaciones en la hoja 5. <strong>Bajó respecto de la v6.0</strong>: dos tiradas en vez de tres, y
las dos bajo techo.</td></tr>
<tr><td class="num">2</td><td><strong>Cobertura de red en 4 puntos</strong></td>
<td>Mejor que los 5 de la v5.2, peor que los 3 de la v6.0. Si alguno queda corto se resuelve con un repetidor barato,
pero hay que saberlo <strong>antes de despachar</strong>. No frena el envío.</td></tr>
<tr><td class="num">3</td><td><strong>El defrost cruzado en los módulos dobles</strong></td>
<td>Que el descongelamiento de un reefer no ciegue al otro. Trabajo de software, costeado, y es lo que hay que probar
antes del hito 2.</td></tr>
<tr><td class="num">4</td><td><strong>La caja de exterior a la intemperie de Santa Cruz</strong></td>
<td>Es la única parte del equipo que no tiene antecedente de campo largo. La que se mandó al sitio el 4-sep es, de
hecho, <strong>la prueba de campo</strong>: conviene pedirle a Andrés una foto después del primer temporal.</td></tr>
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
      <strong>especialmente vendible para los dos de la intemperie</strong>.</li>
    </ul></div>
  </div>
</div>
''')

# =================================================================== HOJA 8
hoja(u'''
<h2><span class="n">11</span>Cómo se arman los dos precios: USD 600 el simple, USD 750 el doble</h2>
<div class="sub">Base: BOM real (<code>BOM_KIT_V1.md</code> rev B de @hardware, precios de MercadoLibre AR verificados
el 2-sep-2026, a precio de reposición). Cambio $ → USD al BNA vendedor 1.535 del 3-sep.</div>

<table class="compacta"><thead><tr><th>&nbsp;</th><th class="num" style="width:14%">Simple ext.<br>(ARS)</th>
<th class="num" style="width:9%">USD</th><th class="num" style="width:14%">Doble int.<br>(ARS)</th>
<th class="num" style="width:9%">USD</th></tr></thead><tbody>
<tr><td>Electrónica y gabinete: ESP32 13.990 + módulo de 2 relés 5.028 + fuente 5 V 2 A 7.980 + consumibles de placa +
prensacables. <strong>Caja: IP65 de exterior ~22.000 en el simple, gabinete común ~8.500 en el doble</strong></td>
<td class="num gris">~59.000</td><td class="num">38</td><td class="num gris">~47.500</td><td class="num">31</td></tr>
<tr><td>Sondas DS18B20 estancas rearmadas con 3 m de cable y prensacable (3 y 6)</td>
<td class="num gris">~27.600</td><td class="num">18</td><td class="num gris">~55.200</td><td class="num">36</td></tr>
<tr><td>Sensores magnéticos de puerta cableados (1 y 2)</td>
<td class="num gris">4.746</td><td class="num">3</td><td class="num gris">9.492</td><td class="num">6</td></tr>
<tr><td>Cable de interconexión al reefer vecino (25 m de par trenzado exterior) — <strong>solo el doble</strong></td>
<td class="num gris">—</td><td class="num">0</td><td class="num gris">~15.000</td><td class="num">10</td></tr>
<tr><td>Envío a Santa Cruz, prorrateado</td>
<td class="num gris">~12.300</td><td class="num">8</td><td class="num gris">~18.400</td><td class="num">12</td></tr>
<tr><td>Armado + <strong>prueba de banco documentada</strong> (el doble, con 25 m de cable) + garantía de reposición
amortizada</td><td class="num gris">&nbsp;</td><td class="num">100</td><td class="num gris">&nbsp;</td><td class="num">150</td></tr>
<tr><td>Parte de plataforma del desarrollo: USD 1.000 repartidos en <strong>4</strong> módulos</td>
<td class="num gris">&nbsp;</td><td class="num">250</td><td class="num gris">&nbsp;</td><td class="num">250</td></tr>
<tr><td>Margen</td><td class="num gris">&nbsp;</td><td class="num">183</td><td class="num gris">&nbsp;</td><td class="num">255</td></tr>
<tr class="total"><td><strong>Precio</strong></td><td class="num gris">&nbsp;</td><td class="num">600</td>
<td class="num gris">&nbsp;</td><td class="num">750</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Márgenes</span><h3>30,5 % el simple · 34 % el doble</h3></div>
    <div class="cuerpo"><p>El doble gana más porque <strong>carga el riesgo del bus de 25 m</strong> (si no cierra hay
    que resolverlo remoto o mandar material) y porque su garantía pesa el doble: un doble caído deja dos reefers
    ciegos.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Por qué 600 y 750</span><h3>Y no otros números</h3></div>
    <div class="cuerpo"><p>Los dos son redondos, se dicen en una frase, y la cuenta cierra sin forzar nada:
    <strong>2 × 600 + 2 × 750 = 2.700 en equipos</strong>, exactamente el mismo renglón de equipos que la v5.2 y la
    v6.0. <strong>La configuración cambió tres veces y el cliente vería siempre el mismo número de equipos: eso es
    señal de que el precio está bien puesto, no de que se acomodó.</strong></p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="box"><p><strong>De dónde salen los USD 60 de diferencia con la v5.2 (4.540 → 4.600), y es un solo renglón
y medio.</strong> El <strong>kit de repuestos pasa de 340 a 400</strong> porque ahora el repuesto es un módulo doble
(que puede reemplazar a cualquiera de los cuatro, incluido un simple) y no un simple. Los equipos y la puesta en
marcha no se movieron. Es un <strong>1,3 %</strong> de diferencia y compra una garantía que cubre el sistema entero con
una sola caja de repuesto. Si Matías prefiere el número redondo de 4.540, se llega bajando el repuesto a 340 y
aceptando que el repuesto sea un simple: <strong>no lo recomiendo</strong> — el día que falle un doble, un repuesto
simple deja un reefer sin vigilancia y obliga a un envío urgente a 1.500 km.</p></div>
''')

# =================================================================== HOJA 9
hoja(u'''
<h2><span class="n">12</span>Puesta en marcha, USD 1.500</h2>
<table class="compacta"><thead><tr><th>Trabajo</th><th class="num" style="width:10%">h</th></tr></thead><tbody>
<tr><td>Sondas, rangos y umbrales por reefer + <strong>calibración de las 15 sondas</strong> contra referencia y
registro de offsets</td><td class="num">10</td></tr>
<tr><td><strong>Software del módulo doble: segunda puerta, segundo defrost con silenciado por reefer,
<code>SONDAS_MAX</code> a 8, validación del bus a 25 m</strong></td><td class="num">10</td></tr>
<tr><td>Registro exportable con código de verificación</td><td class="num">14</td></tr>
<tr><td>Panel multi-equipo y usuarios de lectura</td><td class="num">10</td></tr>
<tr><td>Puesta en marcha remota (alta, credencial, OTA verificada, prueba de puertas y defrost), pruebas de campo con
Andrés, runbook y capacitación — 4 módulos</td><td class="num">12</td></tr>
<tr><td>Salud de bus, histéresis de 3 barridos y <strong>verificación cruzada entre sondas</strong></td><td class="num">4</td></tr>
<tr class="total"><td><strong>Total a USD 25/h</strong></td><td class="num">60 h = USD 1.500</td></tr>
</tbody></table>
<p class="tabla-pie">Bajó de 1.600 (v5.2) a 1.500: se ahorran horas en calibración (15 sondas en vez de 20) y en alta
remota (4 módulos en vez de 5), y se gastan 10 h nuevas en el software del doble. <strong>Las 10 h del software del
doble son la línea a vigilar</strong>: si @firmware dice que son más, salen del margen, no del precio.</p>

<div class="sep"></div>

<h2><span class="n">13</span>Servicio mensual: qué cuesta servir y qué se cobra</h2>
<table class="compacta"><thead><tr><th>Costo directo mensual</th><th class="num" style="width:16%">v2 (12 sondas)</th>
<th class="num" style="width:22%">v6.1 (15 sondas, 5 reed, 4 módulos)</th></tr></thead><tbody>
<tr><td>Supabase Pro</td><td class="num gris">25</td><td class="num">25</td></tr>
<tr><td>Reposición amortizada (módulos y sondas en garantía)</td><td class="num gris">10</td><td class="num">17</td></tr>
<tr><td>Soporte (2 h → 2,3 h a USD 25)</td><td class="num gris">50</td><td class="num">57</td></tr>
<tr><td>Informe mensual</td><td class="num gris">25</td><td class="num">25</td></tr>
<tr class="total"><td><strong>Total</strong></td><td class="num gris">110</td><td class="num">124</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="cita"><p><strong>Tarifa: USD 100 por reefer por mes × 5 = USD 500/mes</strong> (decisión de Matías,
4-sep). Costo directo 124 → <strong>margen bruto USD 376 (76 %)</strong>. La justificación, y es la que hay que decir
si preguntan: <strong>mantenimiento del servidor, custodia de los datos y seriedad del servicio</strong> — el registro
que se entrega tiene que estar disponible y ser defendible dentro de un año, y eso se paga todos los meses aunque no
pase nada.</p></div>

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
<strong>El tendido lo hace y lo paga el cliente, y no aparece en el documento que se manda.</strong> Y ahora son
<strong>2 tiradas bajo techo</strong>, no 2 a la intemperie: el número real que van a gastar es <strong>más bajo que
esta cuenta</strong>, que se hizo para caño rígido exterior.</div>

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
  <li><strong>Saber el tamaño de lo que el cliente gasta por su lado</strong> (≈ USD 572 por las 2 tiradas en el peor
  caso, bastante menos bajo techo). Si dicen «esto de la obra no lo teníamos previsto», la respuesta ya está:
  <strong>la configuración la describieron ellos</strong>, y las tiradas bajaron de 3 a 2 y de la intemperie al
  interior.</li>
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
<p>El fundamento es de caja: hay que comprar y armar <strong>5 módulos</strong> (4 + el repuesto) antes de ver un peso
del segundo tramo, y cobrar ese tramo a un contratista que todavía no tiene nombre. Con el 50 %
(<strong>USD 2.300 ≈ $ 3.530.500</strong>) la compra completa de materiales —<strong>≈ $ 430.000 con flete</strong>—
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
    <div class="cuerpo"><p>4.600 + 12 × 500 = <strong>USD 10.600</strong> el primer año; 6.000/año después;
    <strong>24 meses 16.600</strong>.</p></div>
  </div>
  <div class="card fuerte">
    <div class="cab"><span class="tag">B</span><h3>Anual adelantado, 10 % sobre el servicio</h3></div>
    <div class="cuerpo"><p>4.600 + (12 × 500) × 0,9 = 4.600 + 5.400 = <strong>USD 10.000 redondos</strong>; renovación
    5.400/año; <strong>24 meses 15.400</strong>. El descuento le ahorra <strong>USD 600</strong> el primer año y lo que
    compra es concreto: <strong>cero riesgo de cobranza durante 12 meses</strong> con un contratista que probablemente
    pague a 60-90 días, una factura en lugar de doce, y caja para armar los equipos. <em>Que la B dé USD 10.000
    exactos es una casualidad útil: es el número más fácil de aprobar de toda la propuesta.</em></p></div>
  </div>
</div>

<div class="sep-ch"></div>

<div class="nota"><p><strong>C, eliminada.</strong> <span class="neutro">Matías: «el de la inversión inicial no lo
ofrecería». Era la única que ponía USD ~4.600 nuestros en manos de un contratista a 1.500 km, sin poder retirar los
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
<h2><span class="n">17</span>Los 5 módulos: qué falta comprar y cuánto sale</h2>
<div class="sub"><strong>2 simples de exterior + 2 dobles de interior + 1 doble de repuesto.</strong> Sondas: 15
instaladas + 3 de repuesto = 18. Reed: 5 instalados + 1 de repuesto = 6. Defrost: 5 entradas (cable y bornera, sin
componente caro). Cruce contra el stock declarado (<code>BOM_KIT_V1.md</code> §1, tomando el número más bajo de cada
rango, y <strong>reservando 3 ESP32 para las galgas de Dreyfus</strong>, que es P0 de octubre).</div>

<table class="compacta"><thead><tr><th>Ítem</th><th class="num" style="width:11%">Hacen falta</th>
<th class="num" style="width:13%">Stock decl.</th><th class="num" style="width:8%">Faltan</th>
<th class="num" style="width:12%">Precio</th><th class="num" style="width:13%">A comprar</th></tr></thead><tbody>
<tr><td>ESP32 DevKit</td><td class="num gris">5 + 3 = 8</td><td class="num gris">4</td><td class="num">4</td><td class="num gris">$ 13.990</td><td class="num">$ 55.960</td></tr>
<tr><td>Sondas DS18B20</td><td class="num gris">18</td><td class="num gris">15</td><td class="num">3</td><td class="num gris">$ 4.388</td><td class="num">$ 13.164</td></tr>
<tr><td><strong>Cajas IP65 de exterior</strong> (los 2 módulos de la intemperie)</td><td class="num gris">2</td>
<td class="num gris">0 de esa medida</td><td class="num">2</td><td class="num gris">~$ 22.000</td><td class="num">$ 44.000</td></tr>
<tr><td>Gabinetes para los 3 dobles (2 + repuesto)<span class="soft det">las 3 de 165×165 del stock son chicas para
6 sondas + 2 puertas + 2 defrost</span></td><td class="num gris">3</td><td class="num gris">3 chicas</td>
<td class="num">3</td><td class="num gris">~$ 14.000</td><td class="num">$ 42.000</td></tr>
<tr><td>Fuentes 5 V <strong>2 A</strong></td><td class="num gris">5</td><td class="num gris">5, amperaje sin verificar</td>
<td class="num">5 (peor caso)</td><td class="num gris">$ 7.980</td><td class="num">$ 39.900</td></tr>
<tr><td>Módulos de relé 2 canales</td><td class="num gris">5</td><td class="num gris">10</td><td class="num">0</td><td class="num gris">—</td><td class="num">$ 0</td></tr>
<tr><td>Reed / sensor de puerta</td><td class="num gris">6</td><td class="num gris">10</td><td class="num">0</td><td class="num gris">—</td><td class="num">$ 0</td></tr>
<tr><td>Consumibles reescalados a 5 módulos<span class="soft det">plaquetas ×5, borneras, tiras hembra, R 2k2 y 1k,
10 k, 100 nF, electrolíticos, separadores, prensacables 6 packs por las entradas extra de los estancos</span></td>
<td class="num gris">—</td><td class="num gris">—</td><td class="num gris">—</td><td class="num gris">—</td><td class="num">$ 150.000</td></tr>
<tr><td>Cable de 3 hilos para rearmar 18 sondas a 3 m + termocontraíble</td><td class="num gris">—</td>
<td class="num gris">—</td><td class="num gris">—</td><td class="num gris">—</td><td class="num">$ 40.000</td></tr>
<tr><td><strong>Cable par trenzado exterior para las 2 tiradas</strong> (60 m con sobrante)</td><td class="num gris">—</td>
<td class="num gris">—</td><td class="num gris">—</td><td class="num gris">—</td><td class="num">$ 24.000</td></tr>
<tr class="total"><td colspan="5"><strong>TOTAL</strong></td><td class="num">≈ $ 409.000</td></tr>
</tbody></table>

<div class="sep-ch"></div>

<div class="grid2">
  <div class="card">
    <div class="cab"><span class="tag">Con flete</span><h3>≈ $ 430.000 ≈ USD 280</h3></div>
    <div class="cuerpo"><p>Si las fuentes de stock resultan ser de 2 A, baja a ≈ $ 390.000 (USD 254). <strong>Contra el
    anticipo del 50 % (USD 2.300 ≈ $ 3.530.500), la compra completa es el 12 %.</strong> No hay problema de plata ni de
    cantidades.</p></div>
  </div>
  <div class="card">
    <div class="cab"><span class="tag">Plazo de entrega</span><h3>Las 2 cajas IP65 de exterior se piden primero</h3></div>
    <div class="cuerpo"><p>Es el renglón de mayor plazo. Las 3 cajas de 165×165 que hay en stock <strong>no sirven para
    los dobles</strong> (6 sondas + 2 puertas + 2 defrost + fuente no entran cómodos): quedan para las demos de
    Bahía.</p></div>
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
<tr><td>Conteo del stock real + las 2 mediciones del BOM (amperaje de las fuentes, relé con IN al aire)</td><td class="num">semana 0</td><td>Gonza</td></tr>
<tr><td>Compra del faltante —<strong>las 2 cajas de exterior primero</strong>— y rearmado de sondas a 3 m</td><td class="num">semana 0-1</td><td>Gonza / Matías</td></tr>
<tr><td>Despacho de 2 sondas para el equipo ya instalado (encomienda, 5-8 días hábiles)</td><td class="num">semana 1</td><td>—</td></tr>
<tr><td>Software del módulo doble (2ª puerta, 2º defrost por reefer, <code>SONDAS_MAX</code> a 8)</td><td class="num">semana 1-2</td><td>Matías / @firmware</td></tr>
<tr><td>Alta, calibración remota, rangos y primera alerta real</td><td class="num">semana 2</td><td>Andrés + Matías</td></tr>
<tr class="total"><td><strong>HITO 1</strong></td><td class="num">semana 2</td><td>—</td></tr>
<tr><td>Armado de los 5 módulos + <strong>prueba de banco, los dobles con 25 m de cable</strong> (~20 h)</td><td class="num">semana 1-2</td><td>Gonza / Sergio</td></tr>
<tr><td>Despacho de los 5 bultos (4 módulos + repuesto) a Cerro Moro</td><td class="num">semana 2</td><td>—</td></tr>
<tr><td><strong>Tendido del cable en los 2 pares de adentro</strong></td><td class="num">semana 2-3</td><td><strong>cliente</strong></td></tr>
<tr><td>Montaje de los módulos por personal del campamento</td><td class="num">semana 3-4</td><td>campamento</td></tr>
<tr><td>Alta y calibración de las 13 sondas nuevas</td><td class="num">semana 4</td><td>Matías</td></tr>
<tr class="total"><td><strong>HITO 2</strong> (los 5 reefers reportando + una semana sin falsas alarmas)</td><td class="num">semana 5</td><td>—</td></tr>
</tbody></table>
<p class="tabla-pie"><span class="neutro"><strong>Nada de esta tabla se adelanta:</strong> las sondas, la compra, el
armado y el despacho arrancan con la aceptación y el anticipo. No hay una sola acción para hoy.</span></p>

<div class="sep-ch"></div>

<div class="nota"><p><strong>El riesgo que hay que decir en voz alta: el hito 2 está apretado y depende de una obra
ajena.</strong> <span class="neutro">La semana sin falsas alarmas arranca cuando los 4 módulos reportan —alrededor de
la semana 4— y el hito vence en la 5: <strong>una semana, sin colchón</strong>. Está cubierto en el documento del
cliente por la línea de que los plazos de los hitos 1 y 2 dependen de la ventana de montaje del campamento;
<strong>Matías no debería prometer el hito 2 por teléfono con más firmeza que la que dice el papel.</strong>
<strong>Lo que sí mejoró:</strong> los 2 módulos de exterior no dependen de ningún tendido y pueden estar reportando
apenas se montan.</span></p></div>

<div class="box"><p><strong>Por qué se puede armar sin exponer un peso nuevo, y la contracara para el Director.</strong>
Los kits <strong>ya estaban planificados como las unidades de demostración del plan comercial de Bahía</strong>. Si
Cerro Moro no compra, no quedan colgados: van a su destino original. <strong>Si Cerro Moro compra, Bahía se queda sin
demos.</strong> Recomendación: la reposición de los kits de Bahía se dispara en el mismo pedido que la orden de compra,
no después. <strong>Decide el Director.</strong></p></div>
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
<tr><td><strong>2</strong> — Los 4 módulos y los 5 reefers reportando; nada se pierde, nada sobra</td>
<td>E1: buffer offline, alertas encoladas, alerta de sonda caída, vigía de equipo mudo, discriminador de bus +
histéresis, <strong>detección de sonda que se desvía de las otras del mismo reefer</strong>, <strong>segunda puerta y
segundo defrost con silenciado por reefer en los dobles</strong></td><td class="num gris">sem. 2</td><td class="num">sem. 5</td>
<td>Los 4 módulos montados con sus 15 sondas calibradas; desenchufar una sonda y que llegue la alarma; cortar la red
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
arranca cuando los 4 módulos reportan, alrededor de la semana 4, y vence en la 5. <strong>Sin colchón, y con el tendido
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
<tr><td class="num">1</td><td><strong>Los números:</strong> simple de exterior 600 × 2 = 1.200 · doble de interior
750 × 2 = 1.500 · repuestos 400 · puesta en marcha 1.500 · <strong>inicial 4.600</strong> · abono <strong>500/mes</strong> ·
B = <strong>10.000</strong>. Márgenes 30,5 % / 34 % / 76 %. <strong>¿Van?</strong></td><td><strong>Matías</strong></td></tr>
<tr><td class="num">2</td><td>El sexto reefer entra a <strong>USD 260</strong> (canal libre de su módulo doble, sin equipo
nuevo) + USD 100/mes. Está escrito en el documento del cliente. <strong>¿Va así?</strong></td><td><strong>Matías</strong></td></tr>
<tr><td class="num">3</td><td>Riesgo de los dos buses de 20-25 m: <strong>asumido con conocimiento</strong>. Confirmar
que la posición del 1k queda en la placa.</td><td>@esquematico</td></tr>
<tr><td class="num">4</td><td><strong>10 h de software del módulo doble</strong> (2ª puerta, 2º defrost con silenciado por
reefer, <code>SONDAS_MAX</code> a 8) vendidas en el hito 2. Si son más, sale del margen, no del precio.</td><td>@firmware</td></tr>
<tr><td class="num">5</td><td>Las <strong>2 cajas IP65 de exterior no están en stock</strong>: renglón de mayor plazo,
pedir primero. Confirmar medida y precio. Las 3 cajas de 165×165 no sirven para los dobles.</td><td>@hardware</td></tr>
<tr><td class="num">6</td><td>Compra de materiales <strong>≈ $ 409.000 ($ 430.000 con flete)</strong>, cruzada contra
stock. Reservados 3 ESP32 para las galgas de Dreyfus (P0 de octubre).</td><td>Matías / @hardware</td></tr>
<tr><td class="num">7</td><td>Contar stock y hacer las 2 mediciones del BOM (amperaje real de las fuentes, relé con IN
al aire) <strong>antes de comprar</strong>.</td><td>@hardware</td></tr>
<tr><td class="num">8</td><td><strong>Decisión de portfolio:</strong> los kits son los mismos que iban a ser las demos de
Bahía. Si Cerro Moro compra, Bahía se queda sin demos → reposición en el mismo pedido que la OC.</td><td><strong>Director</strong></td></tr>
<tr><td class="num">9</td><td>Preguntarle a Andrés <strong>cuál de los 4 de adentro está fuera de servicio</strong>:
define el emparejamiento y que el canal libre quede en un módulo instalado y andando.</td><td>Matías</td></tr>
<tr><td class="num">10</td><td><strong>Verificación cruzada entre sondas: hoy NO existe.</strong> Vendida en el hito 2. Si
no se puede cumplir, sacar el punto 3 del bloque «por qué 3 sondas».</td><td>Matías / @firmware</td></tr>
<tr><td class="num">11</td><td><strong>Accionamiento del relé desde el panel: tampoco existe.</strong> Hito 5.</td><td>@firmware</td></tr>
<tr><td class="num">12</td><td>El sensor de puerta viene <strong>deshabilitado por defecto</strong>: que quede en la orden
de armado habilitarlo y probar <strong>las dos</strong> puertas en los dobles.</td><td>@firmware</td></tr>
<tr><td class="num">13</td><td><strong>Cobertura de red en los 4 puntos.</strong> Si alguno queda corto, repetidor
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
        u'<title>INTERNO — Cerro Moro v6.1: 4 módulos, la configuración del sitio y los pendientes</title>\n'
        u'<link rel="stylesheet" href="estilo.css">\n</head>\n<body>\n<div class="doc">\n\n'
        + u'\n'.join(HOJAS) + u'\n</div>\n</body>\n</html>\n')

if __name__ == "__main__":
    io.open(os.path.join(AQUI, SALIDA), "w", encoding="utf-8").write(HTML)
    print("escrito %s (%d hojas)" % (SALIDA, len(HOJAS)))
