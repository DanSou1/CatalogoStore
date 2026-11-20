"""Reels de la semana 17-23 nov 2026, hechos con tomas ya generadas de la serie (sin caras) + texto en pantalla.
Voz de Daniela - Vendedora (ElevenLabs), tomas cortadas en las pausas de la voz. Música propia de la serie (musica-tema.mp3). Para audio en tendencia, ver el plan semanal.
Uso: python3 build_semana.py [etapas|viernes]"""
import subprocess, os, sys
W = os.path.dirname(os.path.abspath(__file__))
SERIE = "/home/claude/catalogostore/redes/serie-recien-mudados"
C = "/home/claude/catalogostore/tools/piezas"; FONTS = os.path.join(C, "fonts")
P = lambda n, f: os.path.join(SERIE, f"parte-0{n}", "tomas", f)
CARD = lambda n: os.path.join(C, n + ".png")
MUSIC = os.path.join(SERIE, "musica-tema.mp3")
PK, WH = r"{\c&HB34FFF&}", r"{\c&HFFFFFF&}"

TRIO = lambda f: os.path.join("/home/claude/catalogostore/redes/reels/trio/tomas", f)
VOZ = lambda n: os.path.join(W, "audio", n)
# Duraciones medidas sobre la voz de Daniela (corte de cada toma = pausa de la voz)
REELS = {
 "etapas": dict(out="2026-11-17-cinco-etapas.mp4", voz=VOZ("daniela-etapas.mp3"), shots=[
    (P(1,"t1-puerta.mp4"), 0.2, 3.26, 1.00, 1.06, "Las 5 etapas de\\N" + PK + "mudarte con tu pareja", "Big"),
    (P(1,"t1-puerta.mp4"), 4.0, 3.94, 1.04, 1.10, "Etapa 1: " + PK + "la emoción\\N" + WH + "“¡Nuestro primer hogar!”", "Sub"),
    (P(1,"t2-pizza-piso.mp4"), 2.5, 4.81, 1.00, 1.08, "Etapa 2: " + PK + "el romance\\N" + WH + "pizza en el piso (no hay mesa)", "Sub"),
    (P(2,"n1-solo-sofa.mp4"), 2.5, 4.75, 1.06, 1.12, "Etapa 3: " + PK + "la realidad\\N" + WH + "tres semanas sin una cita", "Sub"),
    (P(2,"n2-reloj.mp4"), 1.0, 4.51, 1.00, 1.08, "Etapa 4: " + PK + "el pánico\\N" + WH + "¿en qué momento nos volvimos roomies?", "Sub"),
    (P(1,"t3-celulares.mp4"), 3.0, 4.36, 1.00, 1.08, "Etapa 5: " + PK + "la solución\\N" + WH + "viernes de juego… sin celular", "Sub"),
    (CARD("prod_vor_5etapas"), 0, 4.08, 1.00, 1.06, None, None),
    (CARD("end_atreve_juego"), 0, 3.0, 1.00, 1.04, None, None)]),
 "viernes": dict(out="2026-11-20-plan-de-viernes.mp4", voz=VOZ("daniela-viernes.mp3"), shots=[
    (P(2,"n4-ventana.mp4"), 0.5, 3.09, 1.00, 1.06, "Afuera llueve.\\N" + PK + "Adentro, plan.", "Big"),
    (P(2,"n5-manos-sofa.mp4"), 0.3, 3.03, 1.06, 1.12, "Plan de viernes en casa,\\Nen " + PK + "3 pasos:", "Sub"),
    (P(1,"t3-celulares.mp4"), 5.4, 2.55, 1.00, 1.06, "1. Celulares " + PK + "boca abajo", "Sub"),
    (P(1,"t5-manos.mp4"), 3.0, 2.81, 1.00, 1.08, "2. Una vela\\Ny " + PK + "su playlist", "Sub"),
    (P(3,"m3-caricia.mp4"), 3.4, 4.6, 1.00, 1.06, "3. Masaje de 10 minutos:\\N" + PK + "manos calientes, sin afán", "Sub"),
    (TRIO("f2-manos-locion.mp4"), 0.0, 3.75, 1.00, 1.08, "El truco: " + PK + "loción Trío", "Sub"),
    (CARD("prod_trio_viernes"), 0, 2.76, 1.00, 1.07, None, None),
    (CARD("end3"), 0, 3.3, 1.00, 1.04, None, None)]),
 # Versión Facebook (100 % neutra): sin producto, sin voz (solo música + texto), cierre sin "Comenta" ni envío discreto
 "viernes_fb": dict(out="2026-11-20-plan-de-viernes-facebook.mp4", voz=None, shots=[
    (P(2,"n4-ventana.mp4"), 0.5, 3.09, 1.00, 1.06, "Afuera llueve.\\N" + PK + "Adentro, plan.", "Big"),
    (P(2,"n5-manos-sofa.mp4"), 0.3, 3.03, 1.06, 1.12, "Plan de viernes en casa,\\Nen " + PK + "3 pasos:", "Sub"),
    (P(1,"t3-celulares.mp4"), 5.4, 2.55, 1.00, 1.06, "1. Celulares " + PK + "boca abajo", "Sub"),
    (P(1,"t5-manos.mp4"), 3.0, 2.81, 1.00, 1.08, "2. Una vela\\Ny " + PK + "su playlist", "Sub"),
    (P(3,"m3-caricia.mp4"), 3.4, 4.6, 1.00, 1.06, "3. Diez minutos de abrazo,\\N" + PK + "sin afán", "Sub"),
    (CARD("end_fb_viernes"), 0, 3.3, 1.00, 1.04, None, None)]),
}

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
POP = r"{\fad(60,80)\fscx86\fscy86\t(0,140,\fscx100\fscy100)}"

def build(key):
    R = REELS[key]; tmp = os.path.join(W, "_tmp_" + key); os.makedirs(tmp, exist_ok=True)
    parts, t, subs = [], 0.0, []
    for i, (src, ss, dur, z0, z1, txt, sty) in enumerate(R["shots"]):
        out = os.path.join(tmp, f"s{i}.mp4"); n = int(round(dur * 30))
        zp = f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        if src.endswith(".png"):
            cmd = ["ffmpeg","-v","error","-y","-loop","1","-i",src,"-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-frames:v",str(n),
                   "-vf",f"scale=1080:1920,{zp.replace(':s=', ':d='+str(n)+':s=')},format=yuv420p","-t",f"{n/30:.3f}"]
        else:
            cmd = ["ffmpeg","-v","error","-y","-ss",str(ss),"-i",src,"-frames:v",str(n),"-t",f"{n/30:.3f}",
                   "-vf",f"fps=30,scale=1080:1920:flags=lanczos,{zp.replace(':s=', ':d=1:s=')},format=yuv420p",
                   "-af","volume=0.25,aresample=48000,aformat=channel_layouts=stereo,apad","-shortest"]
        subprocess.run(cmd+["-r","30","-c:v","libx264","-preset","fast","-crf","18","-c:a","aac","-b:a","160k",out], check=True)
        if txt: subs.append((t + 0.1, t + n/30 - 0.05, txt, sty))
        parts.append(out); t += n/30
    total = t
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(tmp, "joined.mp4")
    subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-c:v","copy","-c:a","aac",joined], check=True)
    L = ["[Script Info]","ScriptType: v4.00+","PlayResX: 1080","PlayResY: 1920","","[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         "Style: Sub,Archivo,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,70,70,520,1",
         "Style: Big,Archivo,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,4,5,70,70,0,1",
         "","[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    L += [f"Dialogue: 0,{ts(a)},{ts(b)},{s},,0,0,0,,{POP}{x}" for a, b, x, s in subs]
    ass = os.path.join(tmp, "subs.ass"); open(ass, "w").write("\n".join(L) + "\n")
    if R["voz"] is None:  # sin voz: música + ambiente
        fc = [f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.55,afade=t=in:st=0:d=0.6,afade=t=out:st={total-1.6}:d=1.6[m]",
              "[0:a]volume=1.0[amb]", "[m][amb]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]",
              f"[0:v]ass={ass}:fontsdir={FONTS}[v]"]
        final = os.path.join(W, R["out"])
        subprocess.run(["ffmpeg","-v","error","-y","-i",joined,"-i",MUSIC,"-filter_complex",";".join(fc),"-map","[v]","-map","[a]",
                        "-t",f"{total:.2f}","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
                        "-c:a","aac","-b:a","192k","-movflags","+faststart",final], check=True)
        print(key, round(total, 2), final); return
    fc = ["[2:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.6,apad,asplit=2[vo][sc]",
          f"[1:a]aresample=48000,volume=0.30,afade=t=in:st=0:d=0.6,afade=t=out:st={total-1.6}:d=1.6[m0]",
          "[m0][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[m]",
          "[0:a]volume=0.4[amb]",
          "[vo][m][amb]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]",
          f"[0:v]ass={ass}:fontsdir={FONTS}[v]"]
    final = os.path.join(W, R["out"])
    subprocess.run(["ffmpeg","-v","error","-y","-i",joined,"-i",MUSIC,"-i",R["voz"],"-filter_complex",";".join(fc),"-map","[v]","-map","[a]",
                    "-t",f"{total:.2f}","-c:v","libx264","-preset","medium","-crf","20","-pix_fmt","yuv420p",
                    "-c:a","aac","-b:a","192k","-movflags","+faststart",final], check=True)
    print(key, round(total, 2), final)

if __name__ == "__main__":
    for k in (sys.argv[1:] or REELS): build(k)
