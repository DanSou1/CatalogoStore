# Reel Black Friday · voz de Daniela (versión con más intención)

Pedido de Daniel (tablero, 16 nov): "ponles la voz oficial, dale más intención a los anuncios".
Estado: guion listo; falta grabar la voz en ElevenLabs (necesita el Chrome de Daniel encendido).

## Qué cambia frente a la versión sin voz
- **Gancho que nombra a la persona y su problema** en vez de anunciar la oferta: "¿Te toca dar el detalle este diciembre?". Se dispara en 0–3 s junto con la placa "ESTE VIERNES 27 · BLACK FRIDAY".
- **Una razón por producto** (para quién o para qué), no solo el nombre.
- **Cierre de inversión** que hace circular el video: "envíaselo a quien le toca regalarte" (envíos = señal fuerte en IG).
- La fecha de cierre es real (27–30 nov), así que no es urgencia falsa.

## Texto para ElevenLabs (pegar tal cual, un solo audio)
Voz "Daniela - Vendedora", Eleven v4, estabilidad 45 %, similitud 75 %, estilo 20 %, velocidad 1,05. Sin etiquetas de pausa: los puntos bastan para que el montaje corte una frase por placa.

```
¿Te toca dar el detalle este diciembre? Este viernes arranca nuestro Black Friday: quince por ciento menos en cuatro favoritos.
Feromonas sin olor, para él.
Jenga Picante, para la noche de juego.
Hidratante íntimo de lychee, con efecto calor.
Y el arnés de posiciones.
Si compras en la web, te llega un regalo sorpresa.
Solo hasta el lunes treinta. Envíaselo a quien le toca regalarte.
```

| Placa | Frase |
|---|---|
| bf_gancho | ¿Te toca dar el detalle este diciembre? Este viernes arranca nuestro Black Friday: quince por ciento menos en cuatro favoritos. |
| bf_r1 | Feromonas sin olor, para él. |
| bf_r2 | Jenga Picante, para la noche de juego. |
| bf_r3 | Hidratante íntimo de lychee, con efecto calor. |
| bf_r4 | Y el arnés de posiciones. |
| bf_regalo | Si compras en la web, te llega un regalo sorpresa. |
| bf_end | Solo hasta el lunes treinta. Envíaselo a quien le toca regalarte. |

Duración esperada: 17–20 s.

## Montaje (cuando llegue el MP3)
1. Guardar el audio en `reel/audio/daniela.mp3`.
2. `cd tools/piezas && python3 render.py bf_gancho bf_r1 bf_r2 bf_r3 bf_r4 bf_regalo bf_end`
3. `cd redes/2026-11/black-friday/reel && VOZ=1 python3 build_bf.py`. Cada placa dura lo que dura su frase, la música baja sola bajo la voz y el volumen queda en −14 LUFS. Probado con un audio de prueba: 18,1 s, −14,0 LUFS.
4. Reemplazar el borrador del mié 25 en Metricool por el video nuevo.

## Caption con más intención (propuesta para el borrador del mié 25)
```
¿Te toca dar el detalle este diciembre? 🎁
Del viernes 27 al lunes 30: 15 % menos en Feromonas sin olor, Jenga Picante, Hidratante íntimo lychee y Arnés de posiciones.
Compra en la web y tu pedido llega con un regalo sorpresa. Envío discreto · contra entrega en Bogotá.
Envíaselo a quien le toca regalarte 😉 Link en la bio.
```

## Para pauta pagada
Usar una versión sin la placa del arnés (bf_r4) ni su frase: los productos de posiciones no van en anuncios de Meta. El botón es "Enviar mensaje" a WhatsApp.
