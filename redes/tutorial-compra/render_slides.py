import asyncio, subprocess, sys, time, os
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'tuto','carrusel'); os.makedirs(OUT,exist_ok=True)
async def main(vs):
    srv=subprocess.Popen([sys.executable,'-m','http.server','8770','-d',ROOT],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1350})
            for v in vs:
                await pg.goto(f'http://localhost:8770/tuto/slides.html?v={v}')
                await pg.wait_for_selector('body[data-ready]'); await pg.wait_for_timeout(500)
                await pg.locator('#c').screenshot(path=f'{OUT}/{v}.png')
            await b.close()
    finally: srv.terminate()
asyncio.run(main(sys.argv[1:]))
