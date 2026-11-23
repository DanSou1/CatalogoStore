"""Marco neón para reels (fondo, borde con brillo y máscara). python3 render_marco.py -> marco_bg.png, marco_border.png, marco_mask.png, marco_bgml.png (Mercado Libre)"""
import asyncio, os
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        for v in ['bg','border','mask','bgml']:
            await pg.goto(f'file://{D}/marco.html?v={v}'); await pg.wait_for_timeout(500)
            await pg.locator('#c').screenshot(path=f'{D}/marco_{v}.png', omit_background=(v=='border'))
        await b.close()
asyncio.run(main())
