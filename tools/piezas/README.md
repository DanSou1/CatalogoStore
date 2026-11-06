# Piezas gráficas (placas para reels y posts)

- `card.html?v=<nombre>`: plantillas 1080×1920 con la marca (logo pantera neón, Bodoni Moda + Cormorant Garamond Italic + Archivo, rosa #FF4FB3 → violeta → azul).
- `python3 render.py <nombre> [<nombre> ...]` genera `<nombre>.png` aquí mismo (Playwright).
- `recortes/`: productos ya recortados (rembg `isnet-general-use`), con la marca difuminada (`*_blur.png`) o retocados (`*_final.png`).
- Los scripts de montaje (`redes/**/build_*.py`) leen las placas de esta carpeta (variable `CARDS`). Renderiza las placas que piden antes de montar.
