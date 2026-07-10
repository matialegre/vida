# Lista de compra — banco de galgas de precisión (Dreyfus) — VERIFICADA por @tester 2026-07-10

## Comprar en MercadoLibre (links verificados con navegador real, precios vistos en pantalla)
| Componente | Link | Precio ARS | Para qué |
|---|---|---|---|
| ADS1220 (ADC 24-bit) | https://listado.mercadolibre.com.ar/ads1220 | $14.315 | El ADC para arrancar el banco (ratiométrico) |
| LoRa RA-02 SX1278 | https://listado.mercadolibre.com.ar/lora-ra-02 | $19.990 | El enlace 433MHz |
| INA219 | https://listado.mercadolibre.com.ar/ina219 | ~$6.700-10.000 | Medir consumo real (el sleep) |
| Batería ER14505 LiSOCl2 3.6V | https://listado.mercadolibre.com.ar/er14505 | $7.990 | Batería de año |
| LDO HT7333 (usar este, NO xc6206) | https://listado.mercadolibre.com.ar/ht7333 | $7.495 | Regulador (o ir directo desde 3.6V) |
| Galga BF350 350Ω (término afinado) | https://listado.mercadolibre.com.ar/galga-bf350 | pack ~$44-65k | El sensor (viene de a 10-20) |
| HX711 (opcional, referencia) | https://listado.mercadolibre.com.ar/hx711 | $12.729 | Solo baseline de comparación |

Total banco ML ≈ $56.000 + galga. YA EN STOCK: supercap 1F, Arduino Pro Mini, analizador lógico.

## Importar en paralelo (ADC de precisión FINAL)
| AD7124-8 | https://www.digikey.com/en/products/detail/analog-devices-inc/AD7124-8BCPZ/5268092 (DigiKey) · https://www.lcsc.com/product-detail/C578388.html (LCSC) | USD 7-16 | Chip QFN, necesita PCB propia (@pcb) |

## Notas de @tester
- ML detecta bots (reCAPTCHA) — links de BÚSQUEDA (no producto puntual, que se agota).
- xc6206 se mezcla con step-ups → usar HT7333. galga genérica mezcla hubs USB → usar "galga bf350".
- Screenshots en: BACKUP MATI ERP\tests\screenshots\ml_*.png
