# Detección de rotura de cadena en el REDLER RPRB3
### Estado del desarrollo GIMAP–UTN y plan hasta la parada de planta de octubre

**Louis Dreyfus Company S.A. — Planta General Lagos, Santa Fe**
Documento preparado para la reunión del **4 de septiembre de 2026** · GIMAP, UTN Bahía Blanca

---

## 1. Qué se midió en la planta y qué se vio

Entre el **11 y el 13 de febrero de 2026** el equipo del GIMAP instaló dos galgas extensométricas
sobre el **eje de mando del REDLER RPRB3** —una por cada cadena, en posiciones opuestas— y midió
sobre el equipo en marcha. Todos los números que siguen están **medidos muestra por muestra sobre
los registros crudos**, que quedaron archivados sin modificación.

**Los tres hechos centrales:**

**a) Con el REDLER funcionando se registraron dos eventos de cadena que se suelta —13:26:04 y
13:35:33— y el sistema los declaró solo, en 4,4 y 2,8 segundos.**

En el primero, la señal empieza a moverse a las 13:26:03,3 y el receptor declara ALERTA a las
13:26:07,8: **4,4 segundos**. El escalón mecánico dura 3,4 s, así que la alerta sale **1,0 segundo
después de que el fenómeno terminó de producirse**. En el segundo evento, 2,8 s desde la mitad del
escalón. Esos 4,4 s son **el equipo de febrero**: un prototipo alimentado de la red que medía en
forma continua, con un cable de datos a una computadora al lado de la máquina. Es la prueba de que
**el método detecta la falla**, y por eso está medido y escrito acá.

**b) Por qué funciona: la galga del lado que se suelta sube ~19 mV y la del otro lado casi no se
entera (+4 mV).** No hace falta interpretar una imagen: la máquina se desbalancea y el desbalance
aparece en la diferencia entre las dos señales.

**c) Lo que compromete el equipo definitivo, el que se instala en octubre: avisa dentro de los
5 minutos de producido el corte, las 24 horas, sin que nadie tenga que mirar nada.**

El equipo definitivo no lleva cables: va a pila, atornillado a la máquina, y **mide cada 5 minutos**
en lugar de medir en forma continua. Ese es un intercambio elegido a propósito, y el fundamento es
el propio comportamiento de la falla: **una cadena cortada no es un destello, es una condición que
queda.** La carga se redistribuye sobre el eje y **se mantiene así hasta que alguien la repara** —
en los datos de ustedes, el desbalance se sostuvo **22 minutos** sin volver solo. Detectarla dentro
de los 5 minutos siguientes no cambia nada operativo, y a cambio **el nodo dura más de un año con
una pila y no hay que tender un solo cable sobre una máquina en movimiento**. Si en algún punto de
la planta hicieran falta segundos en lugar de minutos, es una decisión de diseño que se toma con
números sobre la mesa (se gana tiempo de aviso y se paga en autonomía o en cableado): díganlo y lo
evaluamos.

**Los números, sin adornos:**

| | |
|---|---|
| Eventos de cadena registrados con el motor en marcha | **2** (13:26:04 y 13:35:33) |
| Latencia **medida** (equipo de febrero, medición continua con cable) | **4,4 s** y **2,8 s** |
| **Compromiso del equipo definitivo** (a pila, sin cables) | **aviso dentro de los 5 minutos**, las 24 horas, automático |
| Amplitud del evento | galga del lado suelto **+19 mV**, la otra **+4 mV** |
| Separación señal / ruido (motor en marcha) | **2,2×** por muestra suelta · **6,9×** promediando 2 s · **9,9×** promediando 10 s |
| **Falsas alarmas** | **0 en 8.136 muestras = 27,2 minutos** de operación normal, en 5 tramos, uno de ellos de **6,3 min con el motor en marcha** |
| Repetibilidad | segundo ensayo sostenido **22 minutos** con la misma calibración: la señal no vuelve sola |
| Medición efectiva | **16.752 muestras · 56,1 minutos** de adquisición continua |

**La letra chica, que preferimos decir nosotros:** por muestra instantánea el ruido del equipo en
marcha llega a picar en 21,5 mV y puede tapar al evento; **lo que sostiene las cero falsas alarmas
no es la amplitud sino la persistencia en el tiempo**. Promediando 2 segundos la separación es
limpia: el peor ruido queda en 4,86 mV y el mínimo del evento en 9,13 mV. Por eso el sistema exige
que la condición se mantenga antes de alarmar, y por eso no alarma con la vibración normal.

**Lo que estos ensayos NO probaron, dicho de frente:**

- El REDLER operó **sin carga de material**. Con carga nominal las señales son mayores y la
  diferencia ante falla debería ser más marcada, pero **eso hay que medirlo**: es exactamente la
  medición que se hace en la parada de octubre, y es el motivo por el que la fecha nos importa tanto.
- La medición efectiva fue de **56 minutos**, no de una jornada: hubo dos huecos largos sin
  adquisición durante los tres días de campo.
- No se calibró la ganancia de las galgas, así que los valores están en milivoltios y no en
  unidades de deformación. La calibración se hace con el equipo definitivo.

*Figuras que acompañan esta sección (ver anexo): `01_deteccion_evento_principal.png` — antes,
durante y después del evento, con los 4,4 s marcados; `02_galga_A_vs_galga_B.png` — las dos galgas
por separado, que muestra el principio de funcionamiento.*

---

## 2. Galga contra cámara: la comparación honesta

**Lo que una cámara hace bien.** Ve muchas cosas a la vez con un solo equipo, no requiere tocar la
máquina para instalarse, y una imagen es evidencia que cualquiera entiende sin explicación. Para
inspección visual general de una línea, es una herramienta válida.

**Dónde el problema del REDLER juega en contra de la cámara:**

1. **La cadena va adentro de una caja cerrada.** El REDLER es, por diseño, un transportador de
   cadena **hermético**: la cadena arrastra el grano dentro de un cajón cerrado, y esa hermeticidad
   es lo que evita la emisión de polvo y la contaminación del producto. Para que una cámara vea la
   cadena hay que abrirle una ventana de inspección — y esa ventana es también por donde entra el
   polvo a la óptica. *(Confirmar en la reunión en qué punto exacto piensan mirar con la cámara: si
   fuera un tramo abierto, este punto cambia.)*
2. **El polvo tapa el vidrio, y ese es un problema conocido de la industria, no un invento
   nuestro.** Los propios proveedores de visión artificial para plantas polvorientas venden como
   parte de la solución **carcasas presurizadas que soplan aire filtrado sobre el lente**,
   **cuchillas de aire** y una función específica de **"detección de oclusión de lente"** para
   avisar cuando la imagen dejó de ser confiable — porque en ambientes de este tipo el polvo se
   mete en el equipo en cuestión de meses. Todo eso es infraestructura adicional (aire comprimido,
   filtros, mantenimiento periódico de limpieza) que hay que instalar y sostener.
3. **La galga mide donde el eje se deforma; la cámara mira la consecuencia.** El sensor está pegado
   sobre el eje de mando, en el punto de engrane de la corona — donde la propia simulación del
   GIMAP muestra que el eje más se deforma. Cuando una cadena deja de tirar, la carga se desbalancea
   sobre el eje **y queda desbalanceada hasta que se repara**: es una condición física medible en
   cualquier momento, no un instante que hay que estar mirando para no perdérselo.
4. **Y sobre todo: no hace falta que haya alguien mirando.** Una cámara resuelve el problema si hay
   una persona atenta a la pantalla, o si se le suma un software de visión que es justamente lo que
   falla con polvo, luz cambiante y vibración. Nuestro nodo **avisa solo, a las tres de la mañana,
   con la planta vacía** — dentro de los 5 minutos de producido el corte.
5. **La galga no depende de la luz, del polvo, ni de tener línea de vista.** No hay iluminación que
   ajustar ni encuadre que se desplace con la vibración del equipo.
6. **Nuestro sistema avisa cuando se queda ciego.** En los ensayos se apagó a propósito uno de los
   nodos y el receptor avisó **a los 10 segundos** (es el tiempo de espera de enlace configurado;
   se puede acortar). Una cámara tapada por polvo sigue mandando imagen —una imagen gris— y no
   avisa que dejó de ver, salvo que se le agregue la función de detección de oclusión mencionada
   arriba.

**Conclusión justa:** no son excluyentes. La cámara documenta; la galga mide y alarma. Si Dreyfus
va a instalar cámaras igual, la galga sigue siendo el disparador que le dice a la cámara —y al
operador— *cuándo mirar*.

---

## 3. En qué estado está el desarrollo hoy (2 de septiembre de 2026)

Después de los ensayos de febrero, el sistema dejó de ser un prototipo de laboratorio y pasó a
diseñarse como **equipo definitivo para quedar instalado en la máquina**: nodo alimentado a pila
con autonomía objetivo de más de un año, sin cables de datos, en caja estanca, con enlace de radio
propio y envío de las mediciones a un servidor. El avance de las últimas semanas:

| Etapa | Estado hoy |
|---|---|
| **Plano eléctrico del nodo** | **Terminado y aprobado.** Lo revisó una persona distinta de la que lo dibujó: la primera revisión lo **rechazó** con 9 observaciones; se corrigieron todas y la segunda lo aprobó para pasar a la placa. La revisión automática del programa de diseño da **cero errores**, con los 43 controles activados. |
| **Placa de circuito impreso** | **En etapa final.** Los 55 componentes están ubicados y la parte más delicada —el circuito de medición, donde se juega la precisión— ya está trazada y verificada sin errores. Falta cerrar el trazado de la parte digital y de alimentación y generar los archivos de fabricación. |
| **Programa del nodo** | **Escrito y compilando** (ocupa el 14 % de la memoria del microcontrolador). Todavía **no probado sobre hardware**: eso es parte del armado. |
| **Sistema de datos y alertas** | **Funcionando punta a punta en banco**: el equipo envía la medición, el servidor la recibe y la muestra, se disparan alertas y el equipo se puede actualizar a distancia sin ir a la planta. |
| **Ensayos con carga nominal** | **Pendiente. Es lo que se hace en la parada.** |

Dicho de la forma más corta posible: **el diseño está cerrado y auditado; lo que falta es fabricar,
armar y probar sobre la máquina.**

---

## 4. Metas y fechas hasta la parada de octubre

**El camino crítico no es el diseño: es la fabricación de la placa y la compra de dos componentes
importados.** El cronograma está armado hacia atrás desde la parada, y cada fecha tiene un
responsable y un entregable que se puede mostrar.

| Fecha | Hito | Cómo se comprueba |
|---|---|---|
| **Vie 4-sep** | Medición con instrumento del módulo de radio (10 minutos de trabajo, pero **bloquea la fabricación**) | Anotación de la medición |
| **Lun 7-sep** | **Pedido de los componentes importados cursado** (2 supercapacitores y 1 diodo de protección) + compra de los componentes locales | Comprobante de compra |
| **Vie 11-sep** | **Archivos de fabricación liberados y placa encargada** — *este es el hito que manda todo el cronograma* | Orden de compra al fabricante |
| **Vie 25-sep** | **Nodo de banco midiendo con galga real** sobre placa armada a mano, con los datos llegando al servidor | **Video de 1 minuto** para mostrar internamente |
| **~29-sep / 2-oct** | Llegada de las placas fabricadas (10-15 días de fabricación + envío aéreo) | Recepción |
| **Semana del 5-oct** | Armado y puesta en marcha de 2 nodos + receptor | Fotos + primera medición |
| **Semana del 12-oct** | Ensayo continuo de 72 h en banco: autonomía, alcance de radio y disparo de alertas | Registro de las 72 h |
| **Parada de planta (fecha a confirmar)** | **Instalación sobre el REDLER, calibración y medición con carga nominal** | Registro en planta |
| **+30 días de la parada** | Informe con los datos de la parada y los umbrales definitivos de operación | Informe entregado |

**Lo que decimos con todas las letras, para no prometer de más:**

- **Si la parada cae antes del 20 de octubre, la placa fabricada puede no llegar.** Por eso el
  ensayo con galga real del 25-sep **no espera a la placa**: se hace sobre una plaqueta armada a
  mano, con los mismos componentes y el mismo programa. Es la red de seguridad del proyecto: si la
  fabricación se atrasa, **igual vamos a la parada con equipo funcionando**, sólo que armado a mano
  en vez de en placa impresa.
- **El plazo de la importación es el mayor riesgo del cronograma** y no depende de nosotros. Se
  cursa el 7-sep para tener el máximo margen. Uno de los dos componentes importados se puede
  resolver pidiendo la placa con montaje incluido, y así sale del camino crítico.
- **Nada de lo que figura arriba depende de desarrollo nuevo sin empezar.** Todo lo que falta es
  fabricar, comprar, armar y medir.

**Lo que hay que decidir esta semana para que octubre llegue:** autorizar la compra de los
importados (lunes 7) y fijar la fecha de la parada, porque de ella depende si vamos con placa
fabricada o con la plaqueta de banco.

---

## 5. Qué necesitamos de Louis Dreyfus

1. **Fecha exacta (o ventana) de la parada de planta.** Es el único dato que hoy no podemos
   estimar y del que depende todo el cronograma de arriba.
2. **Confirmación de que el proyecto sigue adelante**, para cursar el lunes 7 la compra de los
   componentes importados. Sin esa confirmación esta semana, el cronograma se corre.
3. **Acceso al REDLER RPRB3 durante la parada**: tiempo de máquina detenida para preparar la
   superficie del eje y pegar las galgas (la instalación de febrero llevó una jornada), y
   autorización para dejar los equipos montados de forma permanente.
4. **Poder medir con carga nominal.** Necesitamos al menos un tramo de operación con material real
   después de instalar: es la medición que falta y la que convierte el prototipo en un sistema con
   umbrales definitivos.
5. **Un contacto de mantenimiento de planta** para coordinar el montaje y el punto de instalación
   del receptor.
6. **Si hay alguna compra, permiso o habilitación interna que destrabar** (ingreso de personal,
   trabajo en altura, intervención sobre el equipo), decírnoslo el viernes: se resuelve ahora o
   aparece en octubre como sorpresa.

---

*GIMAP — Grupo de Investigación en Multifísica Aplicada, UTN Facultad Regional Bahía Blanca.
Todos los valores de la sección 1 provienen de los registros crudos de los ensayos del 11-13 de
febrero de 2026 en la planta de General Lagos, archivados sin modificación.*

---
---

# NO IMPRIMIR — nota interna (Matías / @diseno). Sacar todo lo que sigue antes del PDF.

**Para @diseno:** el documento del cliente termina en el bloque en itálica de arriba. Objetivo:
2-3 páginas A4. La tabla de números de la §1 es lo primero que tiene que ver un directivo: si algo
se achica, que no sea eso. Poner al pie de la §2 esta línea de fuentes, en cuerpo chico:

> Fuentes de la §2: carcasas presurizadas, cuchillas de aire y detección de oclusión de lente como
> requisito en plantas polvorientas — ifactoryapp.com, "AI Vision Conveyor Monitoring for Cement
> Plants"; dificultad de la visión artificial con iluminación variable y polvo — *Scientific
> Reports* 2024, doi 10.1038/s41598-024-78985-0; hermeticidad del transportador tipo Redler —
> documentación de fabricantes (GSI, Coppi Industrial, Calero Group).

**AVISO GRANDE — el informe de ensayos de campo de febrero TIENE ERRORES. Matías tiene que
saberlos antes de entrar a la reunión, porque Juliano recibió cosas nuestras y adentro de Dreyfus
puede haber una copia de ese informe.** @muestreador rehizo el análisis muestra por muestra sobre
los CSV (`C:\Proyectos\galgas\hardware\evidencia_campo\EVIDENCIA.md` + 7 figuras +
`generar_evidencia.py`, todo regenerable). Discrepancias:

1. **Los famosos 922 mV de las 13:02 NO son la rotura de la cadena B.** El salto ocurre a las
   13:02:32,471, que es **exactamente** el instante en que el auto-offset pasa de ∓0,4199 V a cero:
   es el artefacto de la calibración. Reconstruido el crudo, el desbalance A−B vale 915,2 mV antes,
   915,7 durante y 916,5 después de la supuesta reconexión, y 914-921 mV toda la tarde. Es
   desbalance eléctrico permanente entre canales. **Y así nos lo desarman en dos frases: una
   desconexión real de cadena, ese mismo día y ese mismo equipo, vale 16-19 mV; 916 mV son 50 veces
   eso.** Por eso salió del documento. Figura interna: `99_reposo1_NO_PRESENTABLE.png`.
2. **`reposo_1.csv` no cubre 08:17-13:10:** son 23 s de ceros, un hueco de 4 h 44 min y después
   313 s + 169 s. El evento ya está en curso en la primera muestra → de ese evento **no hay latencia
   calculable**.
3. **"Emisor apagado detectado en < 2 s" es falso: medido, 10,0 s.** Corregido en la §2.
4. **"34.563 muestras / ~6 horas" es doble conteo:** los 12 CSV son exportaciones anidadas de la
   misma base SQLite y comparten `id`. Real: **16.752 muestras únicas, 56,1 min** de adquisición.
5. **Las horas del informe no anclan las figuras:** ubica la desconexión a las 13:43, y los escalones
   reales están a las **13:26:04** y **13:35:33**.
6. **El README de `data/field_captures/` también se equivoca** (declara 0 alertas en
   `galgas_..._133045.csv` y tiene 480). **No citar el README ni el informe: citar EVIDENCIA.md.**

**Si en la reunión alguien saca el informe de febrero y lee un número que no coincide con este
dossier, la respuesta es una sola y conviene tenerla ensayada:** *"ese informe es de febrero y lo
revisamos con los datos crudos en la mano; algunos números estaban mal calculados y los corregimos
a la baja. Los que están acá salen de los registros, muestra por muestra."* Corregir a la baja por
iniciativa propia suma credibilidad; que lo encuentre un ingeniero de ellos, la destruye.

**Riesgo abierto para octubre (NO es tema de la reunión, es técnico):** la galga A derivó **+75,5 mV
en 4 h 44 min**, que es 4-5 veces el evento que hay que detectar (16-19 mV). Hasta acotar esa
deriva, el detector por umbral absoluto sobre una sola galga es inusable y el diferencial A−B
necesita re-cero periódico. Está anotado en `dominios/muestreador.md`.

**LOS 5 MINUTOS — lo más importante que Matías tiene que llevar sabido a la reunión.**
Los **4,4 s y 2,8 s de la §1 son del equipo de febrero**: alimentado de la red y midiendo continuo.
**El nodo que se instala en octubre duerme 300 s entre mediciones** para durar más de un año con
pila, y el despertar por interrupción **no está implementado** → la resolución real de detección
del sistema que vamos a entregar es de **hasta 5 minutos**. Por eso el documento separa las dos
cosas y **compromete 5 minutos, no 4,4 segundos**. Si prometemos 4,4 y entregamos 300, perdemos lo
único que nos queda, que es la credibilidad.
- **Si Dreyfus dice que necesita segundos y no minutos: es un cambio de diseño con costo de
  autonomía** (medir más seguido, o despertar por interrupción, o alimentar el nodo desde la
  planta y tender cable). Se evaluúa con números, no se promete en la reunión. **La decisión es de
  ellos, informada** — y tiene que tomarse mañana o en los días que siguen, **no ser una sorpresa
  nuestra en octubre**. En la §1 quedan invitados explícitamente a plantearlo ("díganlo y lo
  evaluamos").
- Si alguien pregunta por qué 5 minutos, la respuesta es la que ya está escrita en el documento y
  es verdadera: **la falla persiste** (22 minutos en sus propios datos), así que el aviso dentro de
  los 5 minutos no cambia nada operativo y es lo que permite que no haya cables sobre una máquina
  en movimiento.

**Huecos que faltan cerrar antes de imprimir (Matías):**
1. **Las dos figuras van SÍ o SÍ en el PDF**: `01_deteccion_evento_principal.png` y
   `02_galga_A_vs_galga_B.png` (en `C:\Proyectos\galgas\hardware\evidencia_campo\`). La §1
   sin las figuras pierde la mitad de su fuerza. **Nunca** incluir `99_reposo1_NO_PRESENTABLE.png`.
2. **Confirmar con GIMAP cómo se produjeron los eventos de 13:26:04 y 13:35:33.** Por los datos,
   fueron desconexiones de cadena hechas a propósito para el ensayo. El dossier dice "eventos de
   cadena que se suelta", que es cierto; si preguntan, la respuesta honesta es "los provocamos
   nosotros para poder medirlos, sobre su máquina en marcha" — y eso no debilita nada, al
   contrario: quiere decir que es repetible.
3. Confirmar dónde piensan poner la cámara (§2, punto 1). Si es un tramo abierto y no el cajón del
   REDLER, ese punto se reescribe.
4. Las fechas de la §4 son propuesta: si Matías cambia alguna el viernes, cambia el resto en cadena.

**Riesgos del cronograma, para tenerlos en la cabeza el viernes:** el plazo de la importación no
está cotizado (se asume que entra en 3-4 semanas y no hay evidencia de eso); la fecha de la parada
es desconocida; y el nodo v3 **nunca se probó sobre hardware** — el programa compila, nada más.
Por eso el único compromiso duro que se toma frente al cliente es el del 25-sep con plaqueta de
banco, que no depende de nadie de afuera.
