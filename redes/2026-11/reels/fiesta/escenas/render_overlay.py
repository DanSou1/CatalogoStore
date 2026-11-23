"""Carta legible encima de la mano (PNG con transparencia por cuadro). python3 render_overlay.py stopover"""
import asyncio, os, sys, shutil
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__)); FPS=30; DUR=2.8
async def main(v):
    fr=os.path.join(D,'ov_'+v); shutil.rmtree(fr,ignore_errors=True); os.makedirs(fr)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':860,'height':1140})
        await pg.goto(f'file://{D}/escena.html?v={v}'); await pg.wait_for_timeout(600)
        for i in range(int(DUR*FPS)):
            await pg.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={i*1000/FPS}}})")
            await pg.locator('#c').screenshot(path=f'{fr}/{i:04d}.png', omit_background=True)
        await b.close()
asyncio.run(main(sys.argv[1]))
