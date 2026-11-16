"""Renderiza placas a PNG.
  python3 render.py <nombre> [...]          -> card.html (1080×1920: placas de reel e historias)
  python3 render.py --post <nombre> [...]   -> post.html (1080×1350: láminas de carrusel)"""
import sys, asyncio, os
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))

async def main(args):
    page, h = 'card.html', 1920
    if args and args[0] == '--post':
        page, h, args = 'post.html', 1350, args[1:]
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1080, 'height': h})
        for v in args:
            await pg.goto(f'file://{D}/{page}?v={v}'); await pg.wait_for_timeout(700)
            await pg.locator('#c').screenshot(path=f'{D}/{v}.png')
        await b.close()

asyncio.run(main(sys.argv[1:]))
