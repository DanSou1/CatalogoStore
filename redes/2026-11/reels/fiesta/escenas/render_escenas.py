"""Escenas animadas de cartas/fichas reales (texto tal cual el producto). python3 render_escenas.py stop pregunta solteros"""
import asyncio, os, sys, subprocess, shutil
from playwright.async_api import async_playwright
D=os.path.dirname(os.path.abspath(__file__)); FPS=30; DUR=3.6
async def main(vs):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':860,'height':1140})
        for v in vs:
            fr=os.path.join(D,'_f_'+v); shutil.rmtree(fr,ignore_errors=True); os.makedirs(fr)
            await pg.goto(f'file://{D}/escena.html?v={v}'); await pg.wait_for_timeout(600)
            for i in range(int(DUR*FPS)):
                await pg.evaluate(f"document.getAnimations().forEach(a=>{{a.pause();a.currentTime={i*1000/FPS}}})")
                await pg.locator('#c').screenshot(path=f'{fr}/{i:04d}.png')
            subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(FPS),'-i',f'{fr}/%04d.png','-f','lavfi','-i','anullsrc=r=48000:cl=stereo',
                            '-shortest','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','aac',os.path.join(D,f'{v}.mp4')],check=True)
            shutil.rmtree(fr)
        await b.close()
asyncio.run(main(sys.argv[1:]))
