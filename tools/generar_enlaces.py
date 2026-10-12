"""Genera una página para compartir por cada producto de js/productos.json.

Cada página (p/<id>.html) muestra la foto, el nombre y el precio cuando se pega
el enlace en WhatsApp, Facebook o Instagram, y lleva al cliente directo a la
ventana de detalle del producto en la tienda (?p=<id>).

Uso (desde la carpeta CatalogoStore):  python tools/generar_enlaces.py
Requiere Pillow (pip install pillow). Vuelve a ejecutarlo cada vez que agregues
o cambies productos.
"""
import csv, html, json, pathlib
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SITIO = "https://dansou1.github.io/CatalogoStore"
SALIDA = RAIZ / "p"
(SALIDA / "img").mkdir(parents=True, exist_ok=True)


def slug(pid):
    return pid.replace(".", "-")


def precio(v):
    return "$" + f"{v:,}".replace(",", ".")


PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} | XperienceLove</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="product">
<meta property="og:site_name" content="XperienceLove">
<meta property="og:title" content="{titulo} · {precio}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{imagen}">
<meta property="og:image:width" content="600">
<meta property="og:image:height" content="750">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary_large_image">
<style>body{{margin:0;font-family:system-ui,sans-serif;background:#1B1A1A;color:#fff;display:grid;place-items:center;min-height:100vh;text-align:center}}a{{color:#ff9a4d}}</style>
</head>
<body>
<p>Abriendo <a href="{destino}">{titulo}</a>…</p>
<script>location.replace({destino_js});</script>
</body>
</html>
"""


def main():
    productos = json.loads((RAIZ / "js" / "productos.json").read_text(encoding="utf-8"))
    filas = []
    for p in productos:
        s = slug(p["id"])
        origen = RAIZ / p["imagen"].lstrip("./")
        og = SALIDA / "img" / f"{s}.jpg"
        if origen.exists():
            im = Image.open(origen).convert("RGB")
            im.thumbnail((600, 750))
            fondo = Image.new("RGB", (600, 750), (255, 255, 255))
            fondo.paste(im, ((600 - im.width) // 2, (750 - im.height) // 2))
            fondo.save(og, "JPEG", quality=85, optimize=True)
        txt_precio = precio(p["precio"])
        if p.get("precioAnterior") and p["precioAnterior"] > p["precio"]:
            txt_precio += f" (antes {precio(p['precioAnterior'])})"
        desc = (p.get("descripcion") or p["categoria"]["nombre"]).strip()
        if len(desc) > 160:
            desc = desc[:157].rsplit(" ", 1)[0] + "…"
        destino = f"{SITIO}/?p={p['id']}"
        url = f"{SITIO}/p/{s}.html"
        (SALIDA / f"{s}.html").write_text(PLANTILLA.format(
            titulo=html.escape(p["titulo"]), precio=html.escape(txt_precio), desc=html.escape(desc),
            imagen=f"{SITIO}/p/img/{s}.jpg", url=url, destino=html.escape(destino),
            destino_js=json.dumps(destino)), encoding="utf-8")
        filas.append([p["titulo"], p["categoria"]["nombre"], txt_precio, url])
    with open(SALIDA / "enlaces.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Producto", "Categoría", "Precio", "Enlace para compartir"])
        w.writerows(filas)
    print(f"{len(filas)} páginas generadas en p/  (lista en p/enlaces.csv)")


if __name__ == "__main__":
    main()
