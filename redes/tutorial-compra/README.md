# Tutorial: cómo comprar en el catálogo web

Carrusel (9 láminas 4:5) y reel (31 s, 9:16) hechos con capturas reales del catálogo en vista de celular.
Producto de ejemplo: Feromonas sin olor para hombre (cosmeticos-10). Precios difuminados a propósito (regla: sin precios en las piezas).

Cómo regenerarlo (desde una carpeta con node_modules de material-symbols, @fontsource-variable/hanken-grotesk, toastify-js y sweetalert2, y las fuentes/logo de las placas):
1. `python3 capture.py [id-producto]` → `shots/` con capturas y `boxes.json` (no envía nada a internet: Wompi y Web3Forms bloqueados).
2. `python3 render_slides.py s1 … s9` → carrusel.
3. `python3 render_reel.py` → cuadros; luego ffmpeg con `musica-tema.mp3`.
