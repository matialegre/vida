# Lista de compra banco galgas — CORREGIDA 2026-07-10 (v2, tras errores señalados por Matías)

## ⚠️ ERRATA de la v1 (lección para todos los agentes)
La v1 listó para comprar cosas que Matías YA TIENE (LoRa RA-02, galgas del GIMAP, supercap, Pro Mini) y un LDO (HT7333) que CONTRADECÍA la decisión ya tomada de ir DIRECTO sin LDO desde 3.6V. REGLA NUEVA: toda lista de compras se cruza contra el inventario (dominios/hardware.md) y contra las decisiones de diseño (DISEÑO_DREYFUS.md) ANTES de entregarse.
Nota técnica LDO: el "4.3V" del datasheet HT7333 es condición de ensayo (VOUT+1V), no VIN mínimo (real: VOUT+dropout≈3.39V). Igual NO va LDO: decisión = directo de 3.6V (SX1278 tolera 3.9V).

## LO ÚNICO A COMPRAR
| Componente | Link | Precio | Nota |
|---|---|---|---|
| ADS1220 (ADC 24-bit banco) | https://listado.mercadolibre.com.ar/ads1220 | ~$14.315 | verificado por @tester |
| Batería ER14505 LiSOCl2 3.6V | https://listado.mercadolibre.com.ar/er14505 | ~$7.990 | salvo que GIMAP tenga |
| AD7124-8 (precisión final) | DigiKey 5268092 / LCSC C578388 | USD 7-16 | IMPORTAR; QFN, necesita PCB |
| INA219 | https://listado.mercadolibre.com.ar/ina219 | ~$6.700 | SOLO si no está el módulo físico (confirmar con Matías) |

## YA EN STOCK (no comprar): LoRa RA-02, galgas (GIMAP), supercap 1F, Arduino Pro Mini, analizador lógico. SIN LDO (directo 3.6V).
