"""Renderiza el fondo del hero de Black Friday a WebP: python3 render_banner.py <carpeta-destino>"""
import sys, asyncio, os
from PIL import Image
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__)); out=sys.argv[1]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1600,'height':1100})
        for v,n in [('desk','hero-blackfriday'),('movil','hero-blackfriday-movil')]:
            await pg.goto(f'file://{D}/banner.html?v={v}'); await pg.wait_for_timeout(600)
            await pg.locator('#c').screenshot(path=f'{D}/{n}.png')
            Image.open(f'{D}/{n}.png').convert('RGB').save(f'{out}/{n}.webp',quality=88); print(n)
        await b.close()
asyncio.run(main())
