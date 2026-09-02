# Bitácora @diseno3d — diseño mecánico 3D

## 2026-09-01 (b) — GABINETE TERMOVIGÍA v2: PCB pasa a 120 × 100 (relés a bordo)

**Decisión del Director**: la PCB de la Base v2 pasa de 100 × 80 a **120 × 100 ×
1,6** con los 2 módulos de relé a bordo (@esquematico mostró en `DISENO.md` §8
que con 3 LM2596 + borneras no entraba en 100 × 80). Agujeros M3 a 4 mm de las
esquinas: (4,4) (116,4) (4,96) (116,96). Alto máx. de componentes sigue 25.

**Hecho** (`C:\Proyectos\frioseguro\hardware\v2\gabinete\`):
- `pcb = [120, 100, 1.6]` en `termovigia_gabinete.scad`. Gabinete cerrado
  **154,5 × 134,5 × 46** (178 de ancho con orejas); interior 144 × 124;
  standoffs a 112 × 92 entre centros; tornillos de tapa a 128 × 108.
- **Lo que NO recalculaba y se arregló** (el parametrizado de la mañana
  tenía números fijos): posiciones de los prensacables (eran X/Y a mano),
  `oreja_y = 42`, `logo_pos`/`texto_pos`/`logo_alto`, `sma_pos` y
  `prensas_der`. Ahora: `pg_distribuir(lista, luz, centro)` en la lib reparte
  los PG a lo largo de la pared con 4 mm entre tuercas y centra el grupo
  (abajo X = −36/−10/+14,5/+37,5; izq. Y = −27/−4; der. Y = −31 + SMA en
  +20,7); orejas a `ext_y/2 − 22`; logo `round(0,38·ext_y)` = 49 mm, bloque
  escudo+texto centrado en la franja libre a la izquierda de los rótulos de
  LED. Cuatro `assert` nuevos: tuerca de PG vs columna de tapa (3 paredes),
  tubo de LED vs nervio de la tapa, tubo de LED vs columna.
- **LEDs: SUPUESTO** `led_pcb = [[110,90],[110,78]]`. `DISENO.md` §8 solo
  fija (90,70)/(90,58) para la PCB de 100 × 80; los corrí 20 mm en X e Y
  (misma esquina). @esquematico/@pcb tienen que confirmar.
- Bug de OpenSCAD 2021 cazado: una variable de nivel superior que referencia
  otra definida MÁS ABAJO da `undef` (sin error, solo warning) → el logo se
  iba a `translate([undef, …])`. Se reordenó. Lección: en OpenSCAD los
  derivados van siempre después de lo que usan.
- Re-exportados `base_estandar.stl`, `base_premium.stl`, `tapa.stl`: los 3
  `Simple: yes / Volumes: 2`, sin warnings. Medidos sobre la malla: bases
  178 × 130 × 43, 127 cm³ (~100 g PETG al 25 %); tapa 154,5 × 134,5 × 24,8,
  75 cm³ (~60 g). Entra en cama de 220 × 220.
- Re-renderizados y mirados los 6 PNG del gabinete (`renders/`): 4 gotas con
  el pico arriba y centradas en la pared de abajo, PG9 + SMA solo en la
  premium, tapa con logo/rótulos/anillos en su lugar, ensamble con la PCB
  fantasma de 120 × 100 (2 relés + DevKit + 2 LM2596 de ejemplo).
- `IMPRESION.md` al día (cotas, gramos, checklist con 144 × 124 / 112 × 92 /
  posiciones de PG, tabla de faltantes con el supuesto de LEDs).
- `cuna_bateria`, `soporte_sonda`, `soporte_puerta`: sin cambios (no
  dependen de la PCB).

**Evaluación pedida: ¿sirven las 3 cajas IP65 de ferretería para la demo del
viernes mientras se imprime la v2?** Respuesta corta: **para la demo sí,
casi seguro; para el equipo definitivo no.** La demo lleva una de las PCB v1
WiFi (`TERMOVIGIA_PLAN_COMERCIAL.md` ya dice "base en caja IP65"): no
necesita la Base v2 de 120 × 100 ni sus relés a bordo, así que la
restricción es mucho más laxa. Lo que bloquea es que **nadie anotó las
medidas de las cajas** (`hardware.md` las tiene como "3 cajas, medida
interior: confirmar contando"). Qué medir con calibre/cinta, una sola caja
basta si son iguales:
  1. **Interior útil** largo × ancho × profundidad (a la altura del piso y a
     la altura de la boca — muchas tienen las paredes con desmolde y son
     2-3 mm más chicas abajo).
  2. **Profundidad libre** entre piso y cara interior de la tapa (la tapa
     suele tener burlete y nervio que comen 3-5 mm).
  3. Si el piso trae **torretas de montaje**: cuántas, a qué distancia entre
     centros, diámetro del agujero (¿M3, M4, autorroscante?) y cuánto
     sobresalen. Si no trae, va PCB sobre separadores pegados o una placa
     de PLA (15 min de impresión) atornillada a 2 puntos.
  4. **Espesor de pared** donde van los prensacables y si es lisa o con
     nervaduras (para taladrar Ø12,8 / Ø15,5 hace falta ≥ 20 mm de pared
     lisa por agujero, y con copa o escalonada, no mecha común).
  5. Tipo de cierre (tornillos plásticos cautivos vs. metálicos) y si la
     tapa es opaca o translúcida (para los LEDs de la demo: opaca = hay que
     agujerear).
  Regla para decidir: si el interior ≥ **140 × 110 × 55** entra hasta la
  Base v2 con relés (PCB 120 × 100 + 10 mm por lado para tuercas de PG +
  altura 6 + 1,6 + 25); si ≥ **110 × 90 × 45** entra la PCB v1 de la demo.
  Nada de esto lo hago hasta tener los números.

**Próximo paso**: (1) que Matías o Gonza midan las 3 cajas (lista de arriba)
y lo anoten en `hardware.md`; (2) @pcb/@esquematico confirmen `led_pcb` y si
el USB del DevKit queda a ≤ 3 mm del borde; (3) imprimir `soporte_sonda`
como pieza de calibración y después `base_estandar`. Sin commitear (orden
del Director).

## 2026-09-01 — GABINETE TERMOVIGÍA v2 (custom 3D, reemplaza la caja IP65 de ferretería)

**Pedido del Director**: gabinete propio para las 5 unidades de Termovigía
(Estándar / Premium), montaje en pared afuera de la cámara, IP54 razonable en
PLA/PETG, logo de marca, más soportes de sonda y de puerta.

**Hecho** (`C:\Proyectos\frioseguro\hardware\v2\gabinete\`): 5 `.scad` +
6 STL + 10 PNG + `IMPRESION.md`.
- `lib_termovigia.scad` — módulos genéricos con FICHA para @bibliotecario:
  tabla PG (PG7/PG9/PG11/PG13/M12/M16), `agujero_pared()` en **gota
  truncada** (agujero horizontal que imprime sin soporte, pico de 1 mm que
  tapa el hexágono del prensacable), `standoff()`, `columna_tapa()`,
  `oreja_pared()`, `guia_luz()`, `oblongo()`, `ranura_precinto()` y el
  **isotipo Termovigía modelado nativo** (`isotipo()`).
- `termovigia_gabinete.scad` — base + tapa, `variante = "estandar"|"premium"`.
  Cerrado **134,5 × 114,5 × 46** (158 con orejas). PCB 100 × 80 a 12 mm de
  las paredes (lugar para la tuerca del prensacable), standoffs M3 directos,
  4 columnas con **inserto térmico M3** que asoman 2 mm sobre la pared y son
  el tope duro de la tapa. Tapa con falda exterior + nervio interior = canal
  de 3,5 × 6 para **cordón de silicona Ø3**. Prensacables: abajo 2×PG9 + 2×PG7,
  izquierda 2×PG7, derecha (Premium) PG9 batería + SMA. Dos ventanas de LED
  selladas (placa a 0,8 mm + tubo guía hasta la PCB) con rótulo OK/ALERTA.
  Logo en bajorrelieve de 0,8 en dos niveles. USB apagado (ver hallazgo 3).
- `cuna_bateria.scad`, `soporte_sonda.scad`, `soporte_puerta.scad`.

**DECISIÓN — batería FUERA del gabinete, en cuna aparte.** Con la SLA adentro
la caja se va a ~200 × 150 × 130, cuelga 3 kg de orejas de plástico, hay que
abrir el equipo para cambiar la batería y una SLA ventea gas al cargar (no
va en caja sellada). Con la cuna, **la base es la misma para las dos
variantes salvo 2 agujeros**: para 5 unidades importa. Bolsillo de 40 mm,
4 tornillos de 5 con tarugo 8, ranuras de velcro opcionales.

**Cuatro hallazgos que salieron de mirar los renders (no del código)**:
1. **La gota estaba al revés.** `rotate([-90,0,0])` mandaba el +Y del 2D a
   −Z: el pico de la gota quedaba ABAJO, o sea el voladizo seguía arriba y
   encima había un pico inútil. Se vio en la vista ortogonal de la pared de
   abajo. Fix: `rotate([90,0,0])` + extrude centrado. Lección: todo agujero
   con forma orientada se verifica con una vista ortogonal de esa pared.
2. **El clip de sonda no retenía nada.** Los dedos subían 4,5 mm sobre el eje
   y el chaflán de entrada de 1,8 mm se los comía casi enteros. Rehecho:
   dedos rectos hasta 3 mm sobre el eje, boca 5,2 para sonda de 6 (0,4 de
   interferencia por dedo), chaflán de 1,2. Verificado con corte ortogonal
   (`renders/soporte_sonda_seccion.png`).
3. **La ventana USB "para flashear sin abrir" no sirve con esta PCB.** Con la
   PCB a 12 mm de la pared (que hace falta para la tuerca del PG9) un
   micro-USB no llega al DevKit. Queda apagada (`usb_ventana=false`); el
   flasheo es por OTA (firmware v2.6 ya la tiene) o abriendo 4 tornillos.
   **Pedido a @esquematico**: si el conector del DevKit queda a ≤ 3 mm del
   borde de la PCB, se activa la ventana y se imprime el `tapon_usb`.
4. **La PCB de 100 × 80 está justa.** 2 relés de 50 × 39 + DevKit 25 × 48 +
   A7670SA 50 × 35 = ~6.900 de 8.000 mm² sin borneras ni fuente. Si
   @esquematico la agranda, `pcb = [x, y, 1.6]` es la única variable a tocar.

**Sobre el logo**: OpenSCAD 2021 ignora los STROKES del SVG y la curva del
escudo es un stroke de 8,5 → `import()` habría dado el escudo sin curva. Se
reconstruyó nativo con las mismas coordenadas del `isotipo.svg` (Bézier
evaluada en 16 puntos, curva = hull de círculos). `renders/tapa_frente.png`
(CGAL, ortogonal) muestra el isotipo exacto. La tapa se imprime cara abajo,
por eso bajorrelieve y no alto: en esa orientación un relieve positivo es
imposible; a cambio, cambiando filamento a los 0,8 mm sale bicolor.

**Evidencia**: los 6 STL con `Simple: yes / Volumes: 2` en CGAL (un cuerpo
cerrado cada uno), sin warnings; bbox y volumen medidos sobre la malla con
parser propio (base 102,7 cm³, tapa 56,9, cuna 112,6, sonda 6,6, puerta
6,1). **Cero soportes en las 6 piezas.** Renders CGAL de cada pieza mirados.

**Lo que falta (calibre / otros agentes)** — tabla completa al final de
`IMPRESION.md`: `led_pcb`/`led_alto` y posición del USB (@esquematico),
`sma_d`, `sonda_d` (6,0 vs 6,3), dimensiones del MC-38, `riser` por cámara
(lo mide el electricista), altura real de la SLA (94 vs 100), rango de cable
de los PG de Matías. **Sin impresora todavía: nada de esto se probó en
plástico.**

**Próximo paso**: imprimir **solo `soporte_sonda`** (30 min, 8 g) como pieza
de calibración de tolerancias y `base_estandar` cuando @esquematico confirme
la PCB. Antes de la base, medir los prensacables reales con calibre y poner
`tabla_pg` al día. @bibliotecario: cosechar `lib_termovigia.scad` (ya tiene
ficha).


## 2026-08-31 — BANCO DE ENSAYO del drive CC del torno (Sistemas de Control)

**Contexto**: el profesor objetó que "tocar el motor para cargarlo modifica la
planta". Respuesta mecánica: un **disco de aluminio agarrado en el mandril** —
una pieza de trabajo, no una modificación del motor — que hace tres cosas a la
vez: inercia conocida, blanco de dos frenos (perturbación) y rueda fónica.

**Hecho** (repo `C:\Proyectos\drive-torno-esp32s3\SISTEMAS_CONTROL\3d\`):
6 `.scad` paramétricos + 10 STL + 4 PNG + DXF del plano acotado del disco +
`NOTAS_MECANICA.md` con toda la memoria de cálculo.
- `disco.scad` — Ø150 × 8 Al, cubo Ø40, 36 ranuras. **NO se imprime: es el
  plano de mecanizado.** Exporta también DXF y PNG acotados (`-D VISTA="plano"`).
- `brazo_imanes.scad` — freno de Foucault: base con servo MG996R, brazo
  pivotante, porta con 4 N52 de 20×10×5 y rebaje de culata. 3 piezas.
- `zapata_prony.scad` — freno de fricción: soporte, palanca (partida) y zapata.
- `soporte_optico.scad` — bracket del TCRT5000 a 2-4 mm del canto, con escala.
- `guarda.scad` — guarda de contacto en 2 segmentos de 90°.
- `montaje.scad` — ensamble completo con sistema de coordenadas documentado.

**LOS NÚMEROS** (los calcula el propio `.scad` con `echo()`, no un papel aparte
que se desincroniza): masa **407,5 g**, **J = 1,001 × 10⁻³ kg·m²**,
τ_m = J·Ra/(Kt·Ke) = **3,36 ms** (solo el disco), velocidad periférica
**11,78 m/s** a 1500 rpm, óptico a **900 Hz**.
*Verificación cruzada*: el volumen medido sobre la malla del STL da 407,3 g
contra 407,5 g de la fórmula — **0,04 %**. El cálculo y el dibujo son la misma
pieza.

**Tres hallazgos que valen más que las piezas**:
1. **El disco NO domina la inercia y hay que decirlo.** Un motor CC de 1 HP a
   1400 rpm tiene J_rotor de 0,005 a 0,03 kg·m²: este disco mueve τ_m entre un
   3 % y un 20 %. Pero eso se da vuelta a favor: el disco aporta un **ΔJ
   conocido**, así que dos ensayos de desaceleración libre (con y sin disco) a
   la misma velocidad dan `J_rotor = J_disco/(a_sin/a_con − 1)` — la misma
   fricción se cancela. **El disco no ensucia la planta: es el patrón con el que
   se la mide.** Ese es el argumento para la defensa.
2. **Los dos frenos no son redundantes, son de especies distintas.** Foucault
   da τ ∝ ω ⇒ cambia el coeficiente viscoso ⇒ **mueve el polo**: es una
   perturbación PARAMÉTRICA (ensayo de robustez). Prony da τ ≈ cte·signo(ω) ⇒
   **escalón aditivo puro**: es el que muestra el error de régimen del P y cómo
   lo mata el I. Hacen falta los dos.
3. **El freno de Foucault no puede frenar despacio.** Con 4 imanes N52 a 3 mm
   y culata, el par estimado es **0,26–0,44 N·m a 300 rpm** y **0,9–2,0 N·m a
   1000–1400 rpm** (fórmula de Wiederick, Am. J. Phys. 55, 500 (1987), con la
   corrección ×0,3–0,5 por el retorno de las corrientes; **incertidumbre factor
   3**). El objetivo de 1,2 N·m se alcanza arriba de ~1000 rpm y NO a 300 rpm, y
   eso es física (τ ∝ ω), no un defecto. Para baja velocidad, Prony.
   Si falta par: **culata en C (imanes en las dos caras) ⇒ ×3-4**, es la que
   cierra el número; después entrehierro 3→1,5 mm (×1,7).
   Y la calibración real de los dos frenos es **τ = Kt·(I_con − I_sin)**: el
   propio drive es el dinamómetro. La fórmula dimensiona, no informa.

**Cuatro bugs cazados por el conteo de volúmenes de CGAL** (el test unitario
del CSG, otra vez):
- `prony_palanca` daba **Volumes 3** = un cuerpo con una **cavidad cerrada**: el
  agujero del eje de la zapata medía exactamente 2·pal_t y no llegaba a salir
  por ninguna cara. Un agujero que no perfora es una burbuja.
- `prony_zapata` salía con **15 facetas** (una caja): el asiento cilíndrico
  Ø157 se comía la lengüeta entera. Se rediseñó la unión zapata-palanca como
  **brida lateral atornillada** en vez de horquilla con pasador — más simple,
  imprime sin soportes y encima es lo correcto (la palanca va AL COSTADO del
  disco, no arriba).
- `guarda_segmento` daba **Simple: no**: las orejas de unión entre segmentos
  tocaban el cuerpo en **tangente** (unión de espesor cero). Se eliminaron: cada
  segmento se amarra por sus propias patas. Menos piezas, y sano.
- `soporte_optico` daba **Volumes 3**: las pestañas del canal de cable caían
  justo sobre la ventana del sensor y quedaban **flotando en el aire**.

**Un bug de FÍSICA que no lo caza ningún render, solo dibujar el conjunto**: la
palanca del Prony tenía la zapata y la pesa **del mismo lado del pivote**, así
que el peso **descargaba** la zapata en vez de cargarla. Pasó a palanca de
primer género (pivote en el medio). Con b/a = 5 y µ = 0,3: **1 kg ⇒ 1,10 N·m =
18,7 % del par nominal**, y 5 agujeros de gancho dan relaciones 2,8 a 5,0 con la
misma pesa.

**Un problema de cama**: la palanca entera medía **333 mm** y no entra en una
cama de 220. Se partió con **empalme a media madera de 50 mm y 3 M5** en dos
mitades de 217 y 166 mm. `palanca_b` se imprime **dada vuelta** para que su
lengüeta quede contra la cama.

**Total impreso**: ~490 g de PETG, ~22 h, **cero soportes en las 9 piezas**.

**MEDIDAS QUE FALTAN (calibre, bloquean todo)** — tabla completa en §7 de
`NOTAS_MECANICA.md`:
1. **capacidad de las mordazas de 3** (`cubo_d`, puesto 40 mm) — si no agarra,
   no hay disco. Es la primera.
2. **altura del carro respecto del eje** (los 3 brackets: 50/55/55 mm). Los
   oblongos dan ±11 mm; si el error es mayor, hay que reimprimir.
3. **separación de agujeros del porta-herramientas** (50/50/24 mm).
Menores: Ra en frío, **La (no hay dato, falta para τ_e)**, dimensiones reales
del módulo TCRT5000, offset eje-cuerpo del servo, espesor del fieltro, alabeo
axial del disco montado (decide si se puede bajar el entrehierro a 1,5 mm).

**Próximo paso**: medir esas 3 cotas, poner los valores en los `.scad` y
recompilar. **Y hacer el ensayo de desaceleración libre con y sin disco antes de
imprimir nada**: da `J_rotor` y el τ_m real, que ya es un resultado del informe
y no necesita ni una pieza de plástico.

## 2026-08-19 (c) — STITCH: rediseño de la cara porque DABA MIEDO

**El disparador**: Matías vio el render armado y dijo *"es terrorífico, da miedo
posta, parece un diablito"*. Para un juguete de una nena de 7 años eso es un
fallo de primer orden — más grave que cualquier cota. Se frenó todo y se
rehízo la forma.

**Referencia**: se bajó el SVG oficial de Stitch de Wikipedia
(`Stitch_(Lilo_&_Stitch).svg`, 960 px) y se comparó lado a lado con el render.
No se tocó una línea antes de tener la referencia al lado.

**Diagnóstico — por qué leía como un diablito** (5 causas, en orden de peso):
1. **Orejas = cuernos.** Medían 91 mm, nacían de la CORONILLA, iban rectas
   hacia arriba y afuera y terminaban en una bola de r=4, o sea EN PUNTA.
   Llegaban a ±132 mm. Dos apéndices largos, finos y puntiagudos saliendo
   para arriba de la cabeza: cuernos de manual.
2. **Cabeza con forma de corazón invertido.** `cabeza_bolas` tenía las bolas
   grandes (r=52) a z=248 y los "pómulos" a z=250, todo ARRIBA: de frente daba
   un trapecio ancho arriba y afinado abajo = silueta de cara de diablo.
   Stitch es exactamente al revés: ancho abajo (mejillas), redondo arriba.
3. **Ojos rojos rectangulares.** En el visor las placas Heltec estaban
   pintadas naranja rojizo (#c94f2f) y se veían POR DENTRO de los ojos: dos
   rectángulos rojos encendidos en dos cuencas negras.
4. **Nariz en punta y del mismo azul.** Un triangulito que no se leía como
   nariz sino como hocico afilado.
5. **Cinturón táctico.** La visera de sensores pintada de negro con los
   módulos IR en verde cruzaba el pecho como una bandolera.
Secundarios: brazos finos y largos (patas de araña), escalón de "collar" en el
hombro (el torso era MÁS ANCHO que la falda de la cabeza) y sonrisa de 3 mm.

**Qué se cambió** (todo en `parametros.scad` salvo lo indicado):
- `cabeza_bolas` reescrita: ancho máximo 140 mm a z=236 (tercio medio-bajo) y
  coronilla en domo. Perfil documentado en el archivo. Además la falda de la
  cabeza pasó a 96 mm y el hombro del torso se achicó de 120 a 90: **la cabeza
  ahora vuela sobre el torso y tapa la junta — desapareció el cuello.**
- `mejilla_bolas` (nuevas): dos bollos que SOBRESALEN del panel plano. La
  jerarquía de profundidad nariz(65) > hocico(61) > ojos(57) > mejillas(54) >
  panel(46) es lo que devuelve la silueta redonda con un panel plano detrás.
- Orejas: 35 % más cortas, punta r=4 → r=8.5 (redonda), la cadena se curva,
  y la raíz bajó de la coronilla al COSTADO de la cabeza (x=67, z=250).
  **La condición que importa no es el ancho: es que la oreja no asome por
  encima de la coronilla y no termine en punta.** Punta a z=268 contra 298 de
  la coronilla. Ancho total 238 mm (antes 264) — sigue siendo la cota más
  grande y está bien: las orejas de Stitch son enormes.
- Ojos: `ojo_bola_r` 30 → 36 y saliente 10 → 11 ⇒ el ojo se ve de 47 mm (antes
  40) y, de yapa, el espesor en los postes sube de 4,4 a 6,5 mm (**más grande
  Y más fuerte**). Separados 50: quedan a 3 mm uno de otro. La apertura pasó
  de rectángulo redondeado a ÓVALO (el radio de esquina = la mitad del alto):
  un rectángulo iluminado lee como pantalla, un óvalo lee como ojo.
- **`nariz.scad` (pieza nueva, filamento NEGRO)**: en FDM no hay dos colores en
  una pieza. Son 10 g de plástico y es lo que más parecido compra por gramo.
  Encaja con un truco lindo: el MISMO sólido es la pieza (d=0) y el hueco que
  se le resta a la cabeza (d=tol), así no queda ni una luz; y como es un
  prisma con la silueta de la nariz que arranca en un plano, rebana el hocico
  y la nariz apoya en una plataforma PLANA (imprimible y medible).
- Boca: r 26 → 30 y grosor 3 → 5,5.
- Brazos más cortos y gordos; `pata_rr` 12 → 16.
- Visor: hardware **apagado por defecto** (lo primero que se ve es el muñeco,
  no las placas), Heltec gris oscuro en vez de rojo, visera azul, y un grupo
  nuevo **"pantallas encendidas"** para ver cómo queda con los ojos prendidos.

**Tres bugs de ingeniería que salieron de este rediseño** (los tres los cazó el
conteo de volúmenes de CGAL, que es el test unitario del CSG):
1. **La boca pasó a ser un donut.** Con el hocico nuevo (76 mm, 15 de saliente)
   el anillo ENTERO del toro quedaba dentro de la piel y tallaba un círculo
   completo alrededor del morro en vez de una sonrisa. Antes funcionaba "de
   casualidad" porque el hocico era chico y el resto del anillo pasaba por el
   aire. Ahora el toro se recorta explícitamente por debajo de su centro.
   **Lección: no depender de que la geometría se desvanezca sola.**
2. **El poste de la nariz quedó flotando.** `cabeza_frente` salía en 2 cuerpos:
   la cabeza y un cilindro suelto. El hocico es una cáscara de 2,4 mm; el
   alojamiento de la nariz la atravesaba entera y el poste nacía en el aire,
   adentro del hueco del morro. Se agregó `nariz_taco()`, que se le resta a la
   CAVIDAD para dejar carne maciza detrás de la nariz.
3. **Cada oreja salía en 2 pedazos** (4 volúmenes en vez de 2). `espiga_macho`
   se construye desde el origen local hacia adentro; al reubicar la oreja el
   origen quedó un pelo DENTRO de la piel, así que la espiga vivía entera
   adentro de la cabeza y no tocaba el cuerpo de la oreja. Se agregó
   `oreja_espiga_off = 5`: la espiga cruza la piel (5 mm soldados a la oreja,
   8 mm metidos en la mortaja). Como macho y hembra usan el MISMO transform,
   `cabeza_atras` se acomodó sola.

**Herramienta nueva: `3d\preview_forma.scad`.** Dibuja solo las envolventes
exteriores (sin cavidades ni tornillos) y contesta en 30 s la única pregunta
que importa al principio: ¿parece Stitch o parece un diablito? Un render de
verificación completo tarda 3 minutos y la forma se decide en 10 iteraciones.
**OJO — trampa que costó una iteración entera:** el preview de OpenSCAD
(OpenCSG) miente con CSG anidado profundo: mostraba una mancha negra enorme
tapando media cara que NO existía en la geometría. Hay que usar `--render`
(CGAL) para juzgar forma. El PNG sale en gris, pero es la verdad.

**Verificación** (Playwright + Chromium headless, SwiftShader): sin errores de
página, consola limpia, **24 mallas / 47.682 triángulos**, 47.730 triángulos
dibujados en 26 draw calls con todo prendido, 46.166 en 21 con solo carcasa,
48 con "nada" (solo el disco de sombra), 510 frames animados y 36-39 % de
píxeles no-fondo en las 4 vistas. Los 17 STL se re-exportaron con CALIDAD=1 y
**todos dan 1 cuerpo sólido** (2 para los pares). Cotas nuevas: alto **298 mm**,
ancho **238 mm**, fondo **230 mm**.

**El filtro que importa**: se miró la cara ampliada y la respuesta honesta es
que sí, una nena de 7 la abraza. Ojos grandes y redondos, nariz de botón
negra, sonrisa ancha, mejillas, orejas romas hacia atrás. Cero cuernos, cero
colmillos, cero cejas enojadas, cero rectángulos rojos.

**Lo que queda pendiente de estética** (no da miedo, pero es lo menos peluche):
la **visera de sensores** sigue siendo una banda de 124 mm que cruza el pecho
y de perfil sobresale como una bandeja. Es funcional (los IR necesitan ver).
Próxima iteración: hundirla en el torso o partirla en dos parches chicos.
También quedó sin hacer el **interior de oreja rosa** (pieza fina que se
pegaría en un rebaje de la cara frontal de la oreja): es lo que falta para el
golpe de color de la referencia.

## 2026-08-19 (b) — STITCH: visor 3D del muñeco ARMADO

**Problema**: los STL de `3d\stl\` están en ORIENTACIÓN DE IMPRESIÓN (acostados,
rotados). Sirven para el slicer, no para mostrarle a Matías cómo queda el bicho.

**Hecho**:
- `3d\armado_pieza.scad` (nuevo, NO se imprime): exportador que renderiza UNA
  pieza —o un grupo de hardware— **en su posición del conjunto**, elegida con
  `-D "PIEZA=\"torso_frente\""`. Mismas coordenadas que `stitch_completo.scad`
  (z=0 = piso, +Y = adelante), sin la rotación de impresión. 15 nombres válidos.
- `3d\stl_armado\` (nuevo): 15 STL, uno por pieza/grupo, ya posicionados.
  ~22 min de CGAL con `CALIDAD=1`; se renderizaron de a 3 en paralelo.
- `C:\Proyectos\stitch-ainho\VISTA3D_IMPRESO.html` (2,9 MB, autocontenido):
  Three.js 0.147 por CDN + parser propio de STL binario; los 21 objetos van
  embebidos en base64 (abre de doble click por `file://`, sin servidor).
  Órbita con el mouse, zoom con la rueda, pan con botón derecho, 4 vistas
  (Frente/Perfil/3-4/Arriba), prender-apagar pieza por pieza, "solo carcasa" /
  "solo hardware", **explosión gradual con slider** y aristas opcionales.
  Cada fila del panel muestra la cota real de la pieza (bbox en mm), su rango
  de z en el muñeco y su cantidad de triángulos; abajo, alto/ancho/fondo total.
- Las piezas simétricas que vienen de a dos en un mismo STL (orejas, brazos,
  patas, marcos de ojo, cunas, Heltec) se **parten en el generador por el signo
  de X del centroide** de cada triángulo: así se prenden y explotan por
  separado sin tener que renderizar el doble de STL.

**Cotas reales medidas sobre el STL armado** (esto es lo que hay que creerle,
no los comentarios): alto **296 mm** (objetivo 300; los 4 mm son la faceta de
las esferas), ancho **264 mm**, fondo **230 mm**.

**HALLAZGO — el ancho documentado está mal.** `parametros.scad` dice que con
orejas el ancho da 177 mm y `pata_carcasa.scad` afirma que la cota más grande
del robot son los 214 mm de las patas. Medido sobre el STL: las **orejas
llegan a x = ±132 → 264 mm**, contra 220 de las patas y 202 de las ruedas.
**La cota más grande del bicho son las orejas, no las patas.** Hay que
corregir los dos comentarios y, si 264 molesta para pasar por algún lado,
bajar `oreja_rot` (hoy `[0,-18,-49]`).

**Verificación (Playwright + Chromium headless con SwiftShader)**: sin errores
de página, consola limpia, `DIAG.mallas = 21`, `DIAG.tris = 43.334`. Con todo
visible el render reporta **43.382 triángulos en 23 draw calls**; con "solo
carcasa" baja a 41.818 en 18; con "nada", 48 (solo el disco de sombra) — o sea
que el toggle mueve geometría de verdad. Análisis de píxeles del canvas: 36-39 %
de píxeles distintos del fondo en las 4 vistas (nada de pantalla negra), y 755
frames animados. Capturas: vista de frente, 3/4, explotada y solo-carcasa.
Se corrigieron dos cosas encontradas en esa verificación: la vista "Frente"
mostraba la nuca (el +Y de OpenSCAD cae en −Z del mundo Three.js) y el sol
iluminaba a contraluz.

**Próximo paso**: sigue siendo el de abajo (medir `chasis_z`, `heltec`,
`heltec_off` con calibre e imprimir `marco_ojo` + `soporte_heltec` de prueba).
Si se cambia una cota, hay que re-exportar `stl_armado\` para que el visor deje
de mentir: `openscad -o stl_armado\<p>.stl -D "PIEZA=\"<p>\"" armado_pieza.scad`.

## 2026-08-19 — Carcasa STITCH para Ainho (entrega completa)

**Hecho** (repo `C:\Proyectos\stitch-ainho\3d\`): 12 piezas imprimibles +
`parametros.scad` (única fuente de cotas) + `comun.scad` (módulos) +
`stitch_completo.scad` (conjunto de verificación) + `README.md`.
Robot de 300 mm sobre el chasis Smart Car 2WD, cabeza de 135 × 122 × 108.

**Técnica que se usó y conviene reusar**: los cuerpos orgánicos son
`hull()` de esferas. Como `hull(esferas r en c) = conv(c) ⊕ B(r)`, restarle
el mismo espesor a TODAS las esferas da el offset interior EXACTO → pared de
espesor constante sin `minkowski()` (que tardaría horas). Ídem cajas
redondeadas (dims −2t, radio −t). Toda la cáscara sale de ahí.

**Tres hallazgos de ingeniería (no cosmética)**:
1. **Las Heltec no entran detrás de una cara redonda.** Se mapeó numéricamente
   el hueco disponible en toda la huella de la placa (26 × 51) y en la esquina
   abajo-afuera faltaban 9,6 mm. Se demostró que ninguna inclinación lo
   arregla (una recta no puede ser tangente en la pantalla y quedar detrás de
   la superficie en los dos extremos). Solución: **la cara es un panel PLANO**
   recortado con caja redondeada (r=25 para fundirlo en la cabeza). Bonus: así
   los dos marcos de ojo y las dos cunas salen piezas idénticas, y Stitch tiene
   la cara chata igual.
2. **El labio de junta estaba flotando.** Por definición va `tol` más adentro
   que la pared, o sea que no toca su propia mitad: se caía en la impresora.
   Se le agregó un ARRANQUE del lado y>0 que entra 0,5 mm en la pared.
   Evidencia: `Simple: no` → `Simple: yes` en el render de `torso_frente`.
3. **La pata no puede cerrar por abajo.** Centro de rueda a 32,5 del piso,
   pata a 5 → 27,5 mm de radio, pero necesita 35,5 para no rozar la goma.
   27,5 < 35,5 ⇒ imposible. Es un capuchón abierto cortado plano en z=5.

**Tres más que salieron del render de verificación** (por eso se hace):
4. `marco_ojo` daba **7 volúmenes** = cada marco en 3 pedazos sueltos. Los
   postes arrancaban en `ojo_y0+12`, o sea en el aire: como al marco se le
   resta la cabeza, lo único que le queda es el casquete que sobresale. El
   poste tiene que nacer en `ojo_y0 + sqrt(r²−(sep/2)²)`. Ahora da 3 (= 2
   cuerpos). **El conteo de volúmenes de CGAL es el test unitario del CSG.**
5. La **raíz redonda de la oreja** (⌀30) se clavaba 23 mm dentro de la cabeza:
   la oreja no podía asentar. Se le talla la raíz con `cabeza_ext(tol)` en su
   marco local (misma técnica que el marco de ojo). Y la dirección de la oreja
   se derivó pidiendo punta < 300 mm de alto y ancho total < el de las ruedas.
6. La **pata terminaba en el chasis (55)** y dejaba la corona de la goma al
   aire pegada al borde fijo de la tapa: punto de pellizco con la rueda
   girando. Sube a 71 y encapsula la rueda.

**Regla de orientación que ordenó todo el diseño**: cada mitad se imprime con
el plano de corte contra la cama, y por eso ninguna pieza puede tener
salientes que crucen ese plano — salvo el labio, que al ser anillo continuo se
imprime primero y sostiene el resto. De ahí salieron los tornillos de unión
RADIALES (avellanados, al ras) en vez de torres axiales. **Cero soportes en
las 12 piezas.**

**Medidas que faltan (calibre, bloquean la versión definitiva)**: `chasis_z`
(altura de la madera sobre el piso — es la que más mueve todo), `heltec` y
`heltec_off` (borde→centro de pantalla), `heltec_pantalla`, `chasis_x/y`,
`rueda_sep_ext`, patrón de agujeros del chasis, `parlante_d`,
`hcsr04_ojo_sep`, `porta_pilas`, `pico`, `pulsera_muneca_d`. Lista completa al
final del README.

**Próximo paso**: medir `chasis_z`, `heltec` y `heltec_off`, poner los valores
reales y tirar SOLO `marco_ojo` + `soporte_heltec` (~4 h) para probar el ojo
contra una Heltec real. Si el ojo cierra, cierra el resto: recién ahí las
60 h de las cáscaras.

## 2026-07-30 — Monturas LASER-PCB (primera entrega completa)

**Hecho** (repo `C:\Proyectos\laser-pcb\mecanica\`):
- `laser_mount.scad` — montura del módulo láser en 3 partes: placa al carro
  con ranuras de foco ±10 mm y escala grabada, cuna en U que abraza el bloque
  de aluminio (33/40 mm paramétrico, no depende del patrón de agujeros de la
  marca), tapa frontal. Haz vertical por construcción, fan libre.
- `torno_mount.scad` — cuerpo trasero macizo + tapa; variantes motor 775
  (Ø42, abrazadera doble sep. 26 mm) y cuello Dremel (Ø19, collar único).
- `porta_placa.scad` — base con esquina (0,0) grabada, topes en L y 2 levas
  excéntricas M3; variantes 100×70 y 160×100.
- `interlock_pantalla.scad` — escuadra ranurada para acrílico 3 mm + variante
  con torre para microswitch V-15 (interlock físico).
- **OpenSCAD 2021.01 instalado vía winget** (no estaba). 12 STL renderizados
  en `mecanica\stl\`, todos verificados sólido único (CGAL Volumes=2) y con
  bounding box reportado en `PIEZAS.md`.
- Bug encontrado y corregido en render: orejas de la tapa del torno tocaban
  el semi-anillo solo en tangente → 5 cuerpos sueltos; se solaparon con el
  anillo (evidencia: Volumes 6→2).
- Documentación completa en `mecanica\PIEZAS.md` (qué es cada pieza, cómo se
  imprime, ferretería M3, advertencia acrílico ≠ filtro de 450 nm).

**Medidas que faltan (calibre, bloquean versión definitiva)**: agujeros del
carro (sep + M3/M4), lado del módulo láser (33/40), Ø motor 775, Ø cuello
Dremel, espesor placa de cobre, agujeros de la cama, espesor acrílico.
Lista completa al final de `PIEZAS.md`.

**Próximo paso**: cuando se defina la impresora → medir carro, poner valores
reales en los 4 .scad, re-renderizar (`openscad -D ...`, comandos en cada
archivo) e imprimir primero la placa del carro como pieza de prueba de agujeros.
