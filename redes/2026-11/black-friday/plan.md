# Black Friday 27-30 nov 2026 · piezas de redes

Descuento REAL del 15 % (precio de hoy → precio con descuento), solo del viernes 27 al lunes 30 de noviembre.
Por tener fecha de cierre explícita, aquí sí van precios (pedido de Daniel, 15 nov).

| Producto | Antes | Black Friday |
|---|---|---|
| Feromonas sin olor para hombre | $39.900 | $33.900 |
| Sling arnés de posiciones (en piezas: "Arnés de posiciones") | $126.000 | $107.100 |
| Jenga Picante | $67.900 | $57.700 |
| Lubricante lychee sensación caliente (en piezas: "Hidratante íntimo lychee") | $38.900 | $33.100 |

Regalo: "regalo sorpresa" comprando en la web (aún sin definir: no se nombra).

## Entregables
- `carrusel/` 6 láminas 1080×1350: portada · 4 productos · cómo comprar en la web.
- `historias/` 5 historias 1080×1920: cuenta regresiva (zona libre para el sticker de cuenta regresiva) + 1 por producto (zona libre arriba/abajo).
- `reel/2026-11-25-black-friday.mp4` 17 s, música propia del canal, texto en pantalla, sin voz (−14 LUFS). Montaje: `reel/build_bf.py`.
- Placas: `tools/piezas/post.html?v=bf1..bf6`, `card.html?v=st_bf_*` y `bf_*`.

## Programación sugerida (no programado: espera aprobación de Daniel)
| Día | Hora | Pieza |
|---|---|---|
| Mié 25 | 19:30 | Reel (teaser) + historia de cuenta regresiva |
| Vie 27 | 12:00 | Carrusel (lanzamiento) + 4 historias de producto |
| Dom 29 | 19:30 | Historias de producto (recordatorio) |
| Lun 30 | 12:00 | Historia de cuenta regresiva "último día" + reel de nuevo en historias |

## Captions
**Reel (mié 25):** Este viernes empieza el Black Friday de XperienceLove 🖤 15 % menos en 4 favoritos, del 27 al 30 de noviembre, y si compras en la web te llega un regalo sorpresa. ¿Cuál te llevas? Link en la bio. Envío discreto · contra entrega en Bogotá.
**Carrusel (vie 27):** Arrancó el Black Friday: 15 % menos en Feromonas sin olor, Arnés de posiciones, Jenga Picante e Hidratante íntimo lychee. Solo hasta el lunes 30. Compra en la web (link en la bio) y tu pedido llega con un regalo sorpresa. Guárdalo y envíaselo a quien le toca regalarte 😉

## Voz (opcional, cuando el Chrome de Daniel esté conectado)
Guion para "Daniela - Vendedora" (~15 s): «Este viernes arranca nuestro Black Friday. Quince por ciento menos en cuatro favoritos: las feromonas sin olor, el Jenga Picante, el hidratante íntimo de lychee y el arnés de posiciones. Y si compras en la web, te llega un regalo sorpresa. Solo hasta el lunes treinta. Link en la bio.»

## Cuidado
- Arnés de posiciones: la foto del catálogo tiene ilustraciones de personas → NO se usa. En las piezas va una ilustración provisional del producto solo (`tools/piezas/recortes/sling_ilustracion.svg`). Cambiarla por foto real del producto sin figuras antes de publicar.
- Para pauta pagada en Meta, usar el carrusel sin la lámina 3 (arnés) y sin la historia del arnés: los productos de fetiche/posiciones no van en anuncios.
- "El 15 % ya viene aplicado" (lámina 6) depende de que el cambio de la web (tarea blackfriday-catalogo) esté publicado antes del 27.
