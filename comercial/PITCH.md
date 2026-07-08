# PITCH FrioSeguro — mostrador, 30 segundos

> @comercial · 2026-07-07 · Se dice mirando a los ojos, sin folleto en la mano. El folleto queda DESPUÉS.
> Precios del escenario recomendado (PRECIOS_FRIOSEGURO.md): instalación $70.000 + abono $45.000/mes. Si Matías cambia el escenario, actualizar acá.

---

## Pitch principal (5 renglones)

1. Le pongo un sensor en la cámara que la vigila las 24 horas, también el fin de semana cuando acá no hay nadie.
2. Si se corta la luz, se rompe el motor o queda la puerta abierta, le llega la alerta al celular al minuto — no el lunes cuando ya perdió todo.
3. Además le arma solo la planilla de temperatura que pide bromatología: la imprime y listo, no la llena más a mano.
4. No compra nada: el equipo lo pongo yo, usted paga la instalación una vez y un abono de $45.000 por mes — menos de $1.500 por día por cuidar millones en mercadería.
5. Se lo muestro ahora andando en mi celular, y si algo falla lo arreglo yo, que estoy acá en Bahía.

---

## Variantes por segmento (renglón 1-2 se adaptan, el resto igual)

### 🥩 Carnicería
"¿Cuánta plata tenés adentro de la cámara ahora? ¿Tres palos, cinco? Si el compresor se te muere un sábado a la noche, ¿cuándo te enterás? Yo te pongo un sensor que te avisa al celular al minuto, de día, de noche y en Reyes. Y de paso te llena solo la planilla de temperatura para cuando cae bromatología."

### 💊 Farmacia
"Ustedes por norma tienen que registrar la temperatura de la heladera de vacunas todos los días y archivar la planilla — COFA y el manual del Ministerio lo piden así. Esto lo registra cada minuto, guarda el historial y te imprime el reporte para la inspección. Y si la heladera se queda un feriado, te avisa antes de que tengas que descartar un lote de vacunas o insulina que vale más que el abono de todo el año."

### 🐾 Veterinaria
"Las vacunas y los biológicos que tenés en la heladera, si pierden la cadena de frío, no sirven más — y aplicar una vacuna muerta es peor que tirarla. Esto te vigila la heladera las 24 hs, te avisa al celular si se sale de rango y te deja el registro de que la cadena de frío nunca se cortó. Ante cualquier reclamo, tenés el historial para mostrarlo."

### 🍽️ Restaurante
"Vos cerrás a la 1 de la mañana y volvés a las 10. Si la cámara se cortó a las 2, la mercadería estuvo 8 horas muerta y no lo sabés — la usás igual, y ahí sí tenés un problema en serio. Esto te avisa al celular al toque, y además te deja el registro de temperatura que te pide bromatología para la habilitación."

---

## Manejo de objeciones (las 5 que van a caer sí o sí)

### 1. "¿Y esto dónde anda? ¿Quién lo tiene?"
(Las 3 capas de PLATA, todas verdaderas, en este orden:)
- "Mirá, esta es mi heladera, ahora." → sacar el celular y mostrar el dashboard EN VIVO. Es la respuesta más fuerte: no es un folleto, está andando.
- "El sistema lo desarrollé para un campamento minero de Panamerican en Santa Cruz." (*desarrollado para* — no decir "instalado" hasta que sea cierto.)
- "Yo instalo sistemas industriales: equipos míos corren en Louis Dreyfus con la UTN."
- (Desde el cliente 2:) "Lo tiene [nombre] acá a N cuadras, preguntale."

### 2. "¿Y si se corta internet? / ¿y si se corta la luz?"
"Buena pregunta — justamente el sistema avisa cuando eso pasa: si el equipo deja de reportar, te llega la alerta de que quedó sin conexión o sin luz, que casi siempre es el mismo momento en que la cámara dejó de enfriar. O sea: el corte no lo deja ciego, el corte ES una alarma. Y cuando vuelve, el equipo se reconecta solo y seguís teniendo el historial."
(Técnico, si pregunta más: el ESP32 rearranca solo, la nube detecta silencio del equipo y dispara alerta de desconexión.)

### 3. "¿Cuánto sale?"
"La instalación, $70.000 por única vez — menos que un datalogger USB de esos que no avisan nada. Y $45.000 por mes por heladera o cámara: $1.500 por día. Vos decime cuánta mercadería tenés en la cámara y sacá la cuenta de qué te cuesta UN corte sin aviso. La alternativa 'profesional' es un equipo alemán que sale más de $700.000 por cámara, más licencia anual, y no te lo instala ni te lo mira nadie."

### 4. "¿Y si se rompe, quién lo arregla?"
"Yo. Estoy en Bahía, no es un 0800. El equipo es mío — vos no compraste nada — así que si falla, lo repongo sin cargo, está incluido en el abono. Vivo de que esto ande: si no anda, no cobro."

### 5. "Ya tengo termómetro / ya anoto la temperatura en una planilla"
"Perfecto, el termómetro sirve — cuando hay alguien parado adelante mirándolo. ¿Quién lo mira el sábado a la noche? Esto es el mismo termómetro pero que te llama a vos cuando algo anda mal, y que llena la planilla solo, todos los días, sin que nadie se olvide. Bromatología no pide un termómetro: pide el REGISTRO (Código Alimentario, art. 178 — lo traigo impreso). La planilla a mano con letra del empleado, el inspector la conoce de memoria."

---

## Reglas de la visita (recordatorio de doctrina, PLATA.md)
- El objetivo NO es el primer cliente: es el ABONO. Sin contrato y débito/transferencia mensual, no hay venta.
- Piloto gratis: UNO solo (máx 2), 30 días, precio pactado ANTES: "gratis 30 días, después son $45.000/mes o lo retiro."
- Cliente 2 en adelante: paga desde el día 1, garantía "si en 60 días no te sirvió, te devuelvo todo".
- Cerrar SIEMPRE con fecha: "¿te lo instalo el sábado a la mañana o el lunes al mediodía?"
- Upsell en la misma visita: sirena / alerta puerta abierta (+$10–15k/mes) — mismo firmware, misma visita.
- Cada cliente FrioSeguro es lead de Modulia (y viceversa): misma visita, dos productos.

## Bitácora
- 2026-07-07 — Creado por @comercial junto con PRECIOS_FRIOSEGURO.md y CONTRATO_BORRADOR.md.
