"""Videos promocionales de juegos para tomar (Fondo Blanco y Torre de retos y shots), estructura del comercial
de Verdad o se atreve: gancho -> cómo se juega -> ideal para -> producto -> cierre WhatsApp.
Aptos para Facebook: sin palabras sexuales, sin precio, leyenda de moderación (+18). Tomas de Flow (Veo 3.1 Lite) con su
propio audio de fiesta; música de la serie solo bajo las placas finales.
Uso: python3 build_fiesta.py [fondo|jenga]"""
import subprocess, os, sys
W = os.path.dirname(os.path.abspath(__file__))
C = "/home/claude/catalogostore/tools/piezas"; FONTS = os.path.join(C, "fonts")
T = lambda f: os.path.join(W, "tomas", f)
CARD = lambda n: os.path.join(C, n + ".png")
MUSIC = "/home/claude/catalogostore/redes/serie-recien-mudados/musica-tema.mp3"
PK, WH = r"{\c&HB34FFF&}", r"{\c&HFFFFFF&}"

# Daniela (Flow, Veo 3.1 Lite): recortes medidos sobre su voz
DI_F, DUR_DI_F, DC_F, DUR_DC_F = 0.0, 4.4, 0.0, 6.6
DI_J, DUR_DI_J, DC_J, DUR_DC_J = 0.0, 4.0, 0.0, 5.6
# (fuente, inicio, duración, zoom0, zoom1, texto, estilo)
REELS = {
 "fondo": dict(out="fondo-blanco-promo.mp4", shots=[
    (T("d-fondo-intro.mp4"), DI_F, DUR_DI_F, 1.00, 1.05, [(0.0,2.85,"¿Llegó el parche y\\Nno saben " + PK + "qué jugar?"),(2.9,4.3,"Miren esto…")], "Sub"),
    (T("f2-carta.mp4"), 0.2, 2.8, 1.00, 1.08, "Sacas una carta…", "Sub"),
    ("SLOWZOOM", 3.05, 3.3, 1, 1, PK + "¡FONDO BLANCO!", "Big"),
    (T("f1-cenital.mp4"), 0.0, 3.0, 1.04, 1.10, "Retos, preguntas\\N" + PK + "y tragos", "Sub"),
    (T("f3-brindis.mp4"), 0.2, 3.0, 1.00, 1.08, "Ideal para " + PK + "previas\\N" + WH + "y planes con el parche", "Sub"),
    (T("d-fondo-cta.mp4"), DC_F, DUR_DC_F, 1.00, 1.04, [(0.0,4.1,PK + "Fondo Blanco:" + WH + "\\N58 cartas de retos y tragos"),(4.2,6.5,"Escríbannos al " + PK + "WhatsApp\\N" + WH + "y se lo llevamos")], "Sub"),
    (CARD("fb_fondo_end"), 0, 3.2, 1.00, 1.04, None, None)]),
 "jenga": dict(out="torre-retos-shots-promo.mp4", shots=[
    (T("d-jenga-intro.mp4"), DI_J, DUR_DI_J, 1.00, 1.05, [(0.0,2.2,"¿Ustedes tienen pulso\\Nde " + PK + "cirujano?"),(2.3,3.9,"Ya vamos a ver…")], "Sub"),
    (T("j1-ficha.mp4"), 0.4, 3.4, 1.00, 1.08, "Saca una ficha…\\N" + PK + "sin tumbar la torre", "Big"),
    (T("j3-brindis-ficha.mp4"), 0.0, 3.3, 1.00, 1.06, "Cada ficha trae\\N" + PK + "un reto o un shot", "Sub"),
    (T("j2-caida.mp4"), 0.0, 2.8, 1.00, 1.06, "Y si la tumbas…", "Sub"),
    (T("j2-caida.mp4"), 4.4, 2.6, 1.04, 1.10, PK + "¡te toca a ti!", "Big"),
    (T("d-jenga-cta.mp4"), DC_J, DUR_DC_J, 1.00, 1.04, [(0.0,2.0,"La torre de\\N" + PK + "retos y shots"),(2.05,5.5,"Escríbannos al " + PK + "WhatsApp\\N" + WH + "y armen la fiesta")], "Sub"),
    (CARD("fb_jenga_end"), 0, 3.2, 1.00, 1.04, None, None)]),
}

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
POP = r"{\fad(60,80)\fscx86\fscy86\t(0,140,\fscx100\fscy100)}"

def build(key):
    R = REELS[key]; tmp = os.path.join(W, "_tmp_" + key); os.makedirs(tmp, exist_ok=True)
    parts, t, subs, cards_at = [], 0.0, [], None
    for i, (src, ss, dur, z0, z1, txt, sty) in enumerate(R["shots"]):
        out = os.path.join(tmp, f"s{i}.mp4"); n = int(round(dur * 30))
        zp = f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        if src == "SLOWZOOM":  # grito en cámara lenta con zoom al chico de la derecha (f2-carta)
            cmd = ["ffmpeg","-v","error","-y","-ss",str(ss),"-t","1.1","-i",T("f2-carta.mp4"),"-filter_complex",
                   "[0:v]setpts=3*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1,scale=1080:1920:flags=lanczos,"
                   "zoompan=z='if(lt(on,12),1+1.3*on/12,2.3+0.25*(on-12)/90)':x='(iw*0.79)-(iw/zoom/2)':y='(ih*0.32)-(ih/zoom/2)':d=1:s=1080x1920:fps=30,format=yuv420p[v];"
                   f"[0:a]asetrate=48000*0.6,aresample=48000,atempo=0.556,volume=1.5,aformat=channel_layouts=stereo,apad[a]",
                   "-map","[v]","-map","[a]","-frames:v",str(n),"-t",f"{n/30:.3f}"]
        elif src.endswith(".png"):
            if cards_at is None: cards_at = t
            cmd = ["ffmpeg","-v","error","-y","-loop","1","-i",src,"-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-frames:v",str(n),
                   "-vf",f"scale=1080:1920,{zp.replace(':s=', ':d='+str(n)+':s=')},format=yuv420p","-t",f"{n/30:.3f}"]
        else:
            cmd = ["ffmpeg","-v","error","-y","-ss",str(ss),"-i",src,"-frames:v",str(n),"-t",f"{n/30:.3f}",
                   "-vf",f"fps=30,scale=1080:1920:flags=lanczos,{zp.replace(':s=', ':d=1:s=')},eq=saturation=1.06,format=yuv420p",
                   "-af",f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.06,afade=t=out:st={n/30-0.08:.3f}:d=0.08,apad","-shortest"]
        subprocess.run(cmd+["-r","30","-c:v","libx264","-preset","fast","-crf","18","-c:a","aac","-b:a","192k",out], check=True)
        if isinstance(txt, list): subs += [(t + a, t + min(b, n/30 - 0.05), x, sty) for a, b, x in txt]
        elif txt: subs.append((t + 0.1, t + n/30 - 0.05, txt, sty))
        parts.append(out); t += n/30
    total = t
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(tmp, "joined.mp4")
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-c:v","copy","-c:a","aac",joined], check=True)
    L = ["[Script Info]","ScriptType: v4.00+","PlayResX: 1080","PlayResY: 1920","","[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         "Style: Sub,Archivo,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,70,70,520,1",
         "Style: Big,Archivo,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,4,8,70,70,330,1",
         "","[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    L += [f"Dialogue: 0,{ts(a)},{ts(b)},{s},,0,0,0,,{POP}{x}" for a, b, x, s in subs]
    ass = os.path.join(tmp, "subs.ass"); open(ass, "w").write("\n".join(L) + "\n")
    st = max(cards_at - 1.2, 0)
    fc = [f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total-st+1:.2f},volume=0.9,afade=t=in:st=0:d=1.2,afade=t=out:st={total-st-1.4:.2f}:d=1.4,adelay={int(st*1000)}|{int(st*1000)}[m]",
          f"[0:a]volume=1.0,afade=t=out:st={cards_at-0.6:.2f}:d=0.9[amb]",
          "[amb][m]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
          f"[0:v]ass={ass}:fontsdir={FONTS}[v]"]
    final = os.path.join(W, R["out"])
    subprocess.run(["ffmpeg","-v","error","-y","-i",joined,"-i",MUSIC,"-filter_complex",";".join(fc),"-map","[v]","-map","[a]",
                    "-t",f"{total:.2f}","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
                    "-c:a","aac","-b:a","192k","-movflags","+faststart",final], check=True)
    print(key, round(total, 2), final)

if __name__ == "__main__":
    for k in (sys.argv[1:] or REELS): build(k)
