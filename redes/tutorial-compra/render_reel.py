import asyncio, subprocess, sys, time, os
from playwright.async_api import async_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FR=os.path.join(ROOT,'tuto','frames'); os.makedirs(FR,exist_ok=True)
FPS=30
async def main():
    srv=subprocess.Popen([sys.executable,'-m','http.server','8771','-d',ROOT],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
    try:
        async with async_playwright() as p:
            b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
            await pg.goto('http://localhost:8771/tuto/reel.html'); await pg.wait_for_selector('body[data-ready]')
            total=await pg.evaluate('TOTAL'); n=int(total*FPS)
            for f in range(n):
                await pg.evaluate(f'render({f/FPS})')
                await pg.evaluate('Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))')
                await pg.screenshot(path=f'{FR}/f{f:04d}.jpg',type='jpeg',quality=92)
            print('frames',n,total)
            await b.close()
    finally: srv.terminate()
asyncio.run(main())
