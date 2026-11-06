import sys, asyncio, os
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__))
async def main(vs):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        for v in vs:
            await pg.goto(f'file://{D}/card.html?v={v}'); await pg.wait_for_timeout(700)
            await pg.locator('#c').screenshot(path=f'{D}/{v}.png')
        await b.close()
asyncio.run(main(sys.argv[1:]))
