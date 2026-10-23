"""Recorre la compra en el catálogo local (vista de celular) y guarda capturas + cajas de los botones.
No sale ninguna petición a internet: CDNs se sirven desde node_modules y Wompi/Web3Forms se bloquean."""
import asyncio, json, os, re, subprocess, sys, time
from playwright.async_api import async_playwright

REPO = "/home/claude/catalogostore"
PORT = 8765
HERE = os.path.dirname(os.path.abspath(__file__))
NM = os.path.join(HERE, "node_modules")
OUT = os.path.join(HERE, "shots"); os.makedirs(OUT, exist_ok=True)
PRODUCT = sys.argv[1] if len(sys.argv) > 1 else "cosmeticos-10"

MS_CSS = open(os.path.join(NM, "material-symbols/outlined.css")).read()
MS_CSS = re.sub(r"url\([^)]*material-symbols-outlined\.woff2[^)]*\)", f"url(http://localhost:{PORT}/__f/ms.woff2)", MS_CSS)
HK_CSS = "@font-face{font-family:'Hanken Grotesk';font-style:normal;font-weight:100 900;src:url(http://localhost:8765/__f/hk.woff2) format('woff2')}"
FILES = {
    "/__f/ms.woff2": os.path.join(NM, "material-symbols/material-symbols-outlined.woff2"),
    "/__f/hk.woff2": os.path.join(NM, "@fontsource-variable/hanken-grotesk/files/hanken-grotesk-latin-wght-normal.woff2"),
}

async def route(r):
    u = r.request.url
    if u.startswith(f"http://localhost:{PORT}/__f/"):
        path = FILES[u.split(str(PORT))[1]]
        return await r.fulfill(path=path, content_type="font/woff2")
    if u.startswith(f"http://localhost:{PORT}/js/temporada.js"):
        body = open(os.path.join(REPO, "js/temporada.js")).read().replace('TEMPORADA_FORZADA = "auto"', 'TEMPORADA_FORZADA = "normal"')
        return await r.fulfill(body=body, content_type="application/javascript")
    if u.startswith(f"http://localhost:{PORT}"):
        return await r.continue_()
    if "fonts.googleapis.com" in u:
        css = MS_CSS if "Material" in u else HK_CSS
        return await r.fulfill(body=css, content_type="text/css")
    if "toastify" in u:
        p = "toastify-js/src/toastify.css" if u.endswith(".css") else "toastify-js/src/toastify.js"
        return await r.fulfill(path=os.path.join(NM, p))
    if "sweetalert2" in u:
        return await r.fulfill(path=os.path.join(NM, "sweetalert2/dist/sweetalert2.all.min.js"))
    return await r.abort()  # wompi, web3forms, workers, analytics…

async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", REPO],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    boxes = {}
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            ctx = await b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=3,
                                      is_mobile=True, has_touch=True, locale="es-CO", service_workers="block")
            await ctx.route("**/*", route)
            await ctx.add_init_script("""document.addEventListener('DOMContentLoaded',()=>{const st=document.createElement('style');
              st.textContent=`.producto-precios,#hero-producto-precio,#hero-producto-precio-anterior,.modal-precio,#carrito-drawer-productos .text-plum,
              #carrito-drawer-total,.carrito-producto-precio,#total,#datos-envio-subtotal,#datos-envio-flete,#datos-envio-total{filter:blur(7px)}`;
              document.head.appendChild(st)})""")
            pg = await ctx.new_page()
            base = f"http://localhost:{PORT}"

            async def shot(name, sel=None):
                await pg.wait_for_timeout(700)
                await pg.screenshot(path=os.path.join(OUT, f"{name}.png"))
                if sel:
                    bb = await pg.locator(sel).first.bounding_box()
                    boxes[name] = bb
                print("shot", name, boxes.get(name))

            # 1. Catálogo
            await pg.goto(base + "/index.html"); await pg.wait_for_load_state("networkidle")
            await pg.evaluate("localStorage.clear()")
            await pg.reload(); await pg.wait_for_load_state("networkidle")
            await shot("01-inicio")
            # bajar hasta el producto en la grilla
            card = pg.locator(f"#contenedor-productos [data-id='{PRODUCT}'], #contenedor-productos #{PRODUCT}").first
            if await card.count() == 0:
                card = pg.locator("#contenedor-productos .producto").filter(has_text="Feromonas sin olor para hombre").first
            await card.scroll_into_view_if_needed(); await pg.evaluate("window.scrollBy(0,-120)")
            await shot("02-producto-grilla")
            vm = card.get_by_text("Ver más información").first
            boxes["02-producto-grilla"] = await vm.bounding_box()
            # 2. Detalle del producto
            await vm.click(); await pg.wait_for_timeout(900)
            await shot("03-detalle")
            add = pg.locator("#modal-producto").get_by_text("Agregar al carrito").first
            boxes["03-detalle"] = await add.bounding_box()
            await add.click(force=True)
            await pg.wait_for_timeout(900)
            await shot("03b-agregado")
            await pg.wait_for_timeout(2200)  # deja pasar el toast
            await pg.evaluate("document.getElementById('modal-producto').close()")
            await pg.wait_for_timeout(700)
            await shot("04-drawer", "#carrito-drawer a[href='./carrito.html']")
            # 3. Carrito
            await pg.goto(base + "/carrito.html"); await pg.wait_for_load_state("networkidle")
            await shot("05-carrito", "#carrito-acciones-comprar")
            await pg.click("#carrito-acciones-comprar"); await pg.wait_for_timeout(600)
            await pg.evaluate("window.scrollTo(0,0)")
            await pg.fill("#envio-nombre", "Ana López")
            await pg.fill("#envio-contacto", "300 123 4567")
            await pg.fill("#envio-correo", "ana@correo.com")
            await pg.select_option("#envio-ciudad", "bogota")
            await pg.fill("#envio-direccion", "Calle 123 # 45-67, apto 301")
            await pg.locator("#envio-nombre").scroll_into_view_if_needed(); await pg.evaluate("window.scrollBy(0,-90)")
            await shot("06-datos", "#form-datos-envio")
            await pg.locator("#campo-metodo-pago").scroll_into_view_if_needed(); await pg.evaluate("window.scrollBy(0,-160)")
            await pg.check("input[value='contra-entrega']")
            await shot("07-metodo", "#campo-metodo-pago")
            await pg.check("input[value='online']")
            await pg.locator("#datos-envio-continuar").scroll_into_view_if_needed(); await pg.evaluate("window.scrollBy(0,220)")
            await shot("08-continuar", "#datos-envio-continuar")
            # 4. Pantalla de confirmación (se muestra sin enviar nada)
            await pg.evaluate("""()=>{for(const id of ['carrito-datos-envio','carrito-grid','carrito-vacio','carrito-error-pago'])document.getElementById(id).classList.add('disabled');
              document.getElementById('carrito-comprado').classList.remove('disabled');window.scrollTo(0,0)}""")
            await shot("09-gracias")
            json.dump(boxes, open(os.path.join(OUT, "boxes.json"), "w"), indent=1)
            await b.close()
    finally:
        srv.terminate()

asyncio.run(main())
