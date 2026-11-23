"""Promos Fondo Blanco y Torre de retos y shots, versión 3 (pedido de Daniel 23 nov):
- Marco neón como el reel de Verdad o se atreve (fondo morado, @x_experiencelove · +18, títulos grandes arriba, video en
  marco redondeado con brillo rosa-violeta).
- Voz real de Daniela (ElevenLabs, "Daniela - Vendedora", Eleven v4) en lugar de la voz de Flow.
- Música de fondo continua (ElevenLabs Music, reguetón suave/afro-house 100 BPM) con ducking bajo la voz.
- Efectos: punch-in en cada corte, destello blanco + whoosh, títulos con rebote, sacudida y golpe cuando cae la torre,
  grito en cámara lenta con zoom.
Uso: python3 build_fiesta_v3.py [fondo|jenga]"""
import subprocess, os, sys
W = os.path.dirname(os.path.abspath(__file__))
P = "/home/claude/catalogostore/tools/piezas"; FONTS = os.path.join(P, "fonts")
T = lambda f: os.path.join(W, "tomas", f)
A = lambda f: os.path.join(W, "audio", f)
BG, BORDER, MASK = (os.path.join(P, f"marco_{k}.png") for k in ("bg", "border", "mask"))
FX, FY, FW, FH = 110, 560, 860, 1140
PK, YL, WH = r"{\c&HB34FFF&}", r"{\c&H3FD2FF&}", r"{\c&HFFFFFF&}"
POP = r"{\fscx55\fscy55\t(0,110,\fscx108\fscy108)\t(110,190,\fscx100\fscy100)}"
SHAKE = r"{\t(0,70,\frz5)\t(70,140,\frz-5)\t(140,210,\frz4)\t(210,280,\frz-3)\t(280,350,\frz0)}"

# Voz de Daniela (ElevenLabs): se recorta el silencio inicial (0.33 s) que dejó la grabación
VO_LEAD = 0.33
# Tomas: (tipo, fuente, inicio, duración, opciones)  tipo: clip | slow | card
# opciones: amb (volumen del audio de la toma), shake=(t0,t1), vo=archivo de voz, titles=[(t0,t1,texto,estilo)], boom=t
REELS = {
 "fondo": dict(out="fondo-blanco-promo.mp4", shots=[
   ("clip", T("d-fondo-intro.mp4"), 0.0, 3.95, dict(amb=0.0, vo="vo1-fondo-intro.mp3", titles=[
       (0.0, 2.45, "¿LLEGÓ EL " + PK + "PARCHE" + WH + "\\NY NO SABEN QUÉ JUGAR?", "T"),
       (2.5, 3.95, "MIREN " + YL + "ESTO…", "T")])),
   ("clip", T("f2-carta.mp4"), 0.2, 2.8, dict(amb=0.35, titles=[(0, 2.8, "SACAS UNA\\N" + PK + "CARTA…", "T")])),
   ("slow", T("f2-carta.mp4"), 3.05, 3.3, dict(amb=1.0, titles=[(0.15, 3.3, SHAKE + YL + "¡FONDO\\NBLANCO!", "Huge")])),
   ("clip", T("f1-cenital.mp4"), 0.0, 3.0, dict(amb=0.3, titles=[(0, 3.0, "RETOS, " + PK + "PREGUNTAS\\N" + YL + "Y TRAGOS", "T")])),
   ("clip", T("f3-brindis.mp4"), 0.2, 3.0, dict(amb=0.35, titles=[(0, 3.0, "IDEAL PARA", "T"),
       (0.25, 3.0, "{\\pos(540,562)}  PREVIAS  ", "Pill"), (0.45, 3.0, "{\\pos(540,1698)}  PLANES CON EL PARCHE  ", "PillY")])),
   ("clip", T("d-fondo-cta.mp4"), 0.0, 6.95, dict(amb=0.0, vo="vo2-fondo-cta.mp3", titles=[
       (0.0, 3.85, PK + "FONDO BLANCO", "T"), (0.9, 3.85, "{\\pos(540,562)}  58 CARTAS DE RETOS Y TRAGOS  ", "Pill"),
       (3.9, 6.95, "ESCRÍBANNOS AL\\N" + YL + "WHATSAPP", "T"), (4.3, 6.95, "{\\pos(540,1698)}  300 467 5206  ", "PillG")])),
   ("card", os.path.join(P, "fb_fondo_end.png"), 0, 3.0, dict())]),
 "jenga": dict(out="torre-retos-shots-promo.mp4", shots=[
   ("clip", T("d-jenga-intro.mp4"), 0.0, 4.85, dict(amb=0.0, vo="vo3-jenga-intro.mp3", titles=[
       (0.0, 2.45, "¿TIENEN PULSO\\NDE " + PK + "CIRUJANO?", "T"),
       (2.5, 4.85, "YA VAMOS " + YL + "A VER…", "T")])),
   ("clip", T("j1-ficha.mp4"), 0.4, 3.4, dict(amb=0.35, titles=[(0, 3.4, "SACA UNA FICHA…\\N" + PK + "SIN TUMBAR LA TORRE", "T")])),
   ("clip", T("j3-brindis-ficha.mp4"), 0.0, 3.3, dict(amb=0.35, titles=[(0, 3.3, "CADA FICHA TRAE\\N" + YL + "UN RETO O UN SHOT", "T"),
       (0.3, 3.3, "{\\pos(540,1698)}  54 FICHAS DE MADERA  ", "Pill")])),
   ("clip", T("j2-caida.mp4"), 0.0, 2.8, dict(amb=0.5, shake=(0.0, 1.0), boom=0.05, titles=[(0, 2.8, "Y SI LA " + PK + "TUMBAS…", "T")])),
   ("clip", T("j2-caida.mp4"), 4.4, 2.6, dict(amb=0.5, titles=[(0.05, 2.6, SHAKE + YL + "¡TE TOCA\\NA TI!", "Huge")])),
   ("clip", T("d-jenga-cta.mp4"), 0.0, 5.3, dict(amb=0.0, vo="vo4-jenga-cta.mp3", titles=[
       (0.0, 2.2, "LA TORRE DE\\N" + PK + "RETOS Y SHOTS", "T"),
       (2.25, 5.3, "ESCRÍBANNOS AL\\N" + YL + "WHATSAPP", "T"), (2.6, 5.3, "{\\pos(540,1698)}  300 467 5206  ", "PillG")])),
   ("card", os.path.join(P, "fb_jenga_end.png"), 0, 3.0, dict())]),
}

def run(cmd): subprocess.run(cmd, check=True)

def sfx(tmp):
    out = {}
    specs = {
     "whoosh": ["-f","lavfi","-i","anoisesrc=d=0.42:c=pink:a=0.7","-af","highpass=f=500,lowpass=f=5500,afade=t=in:d=0.26:curve=exp,afade=t=out:st=0.26:d=0.16,volume=0.9"],
     "boom": ["-f","lavfi","-i","aevalsrc='0.95*sin(2*PI*(48+70*exp(-9*t))*t)*exp(-3.5*t)':d=1.1:s=48000"],
     "pop": ["-f","lavfi","-i","aevalsrc='0.5*sin(2*PI*(1200-5000*t)*t)*exp(-30*t)':d=0.14:s=48000"],
    }
    for k, a in specs.items():
        out[k] = os.path.join(tmp, k + ".wav"); run(["ffmpeg","-v","error","-y",*a,"-ac","2","-ar","48000",out[k]])
    return out

def shot_video(i, kind, src, ss, dur, o, tmp):
    n = int(round(dur * 30)); out = os.path.join(tmp, f"s{i}.mp4")
    if kind == "card":
        run(["ffmpeg","-v","error","-y","-loop","1","-i",src,"-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-frames:v",str(n),
             "-vf",f"scale=1080:1920,zoompan=z='1.04-0.04*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30,fade=in:d=0.18:color=white,format=yuv420p",
             "-t",f"{n/30:.3f}","-r","30","-c:v","libx264","-preset","fast","-crf","18","-c:a","aac",out]); return out
    if kind == "slow":
        # 1,1 s reales a ~1/3 de velocidad, zoom al chico de la derecha (x≈0,79 y≈0,32 del cuadro original)
        v = (f"[0:v]setpts=3*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1,crop=720:955:0:0,scale=1720:2280:flags=lanczos,"
             f"zoompan=z='if(lt(on,10),1+0.75*on/10,1.75+0.2*(on-10)/{n})':x='(iw*0.84)-(iw/zoom/2)':y='(ih*0.40)-(ih/zoom/2)':d=1:s={FW}x{FH}:fps=30,eq=saturation=1.15")
        a = "[0:a]asetrate=48000*0.6,aresample=48000,atempo=0.556,volume=1.6,aformat=channel_layouts=stereo,apad[a]"
        inp = ["-ss",str(ss),"-t","1.1","-i",src]
    else:
        sh = o.get("shake"); jx = jy = "0"
        if sh:
            f0, f1 = int(sh[0]*30), int(sh[1]*30)
            jx = f"if(between(on,{f0},{f1}),28*sin(on*2.7),0)"; jy = f"if(between(on,{f0},{f1}),22*cos(on*3.3),0)"
        z = f"if(lt(on,7),1.16-0.08*on/7,1.08+0.05*(on-7)/{n})"
        v = (f"[0:v]fps=30,scale={FW}:-2:flags=lanczos,crop={FW}:{FH}:0:(ih-{FH})/2,scale={FW*2}:{FH*2},"
             f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)+{jx}':y='ih/2-(ih/zoom/2)+{jy}':d=1:s={FW}x{FH}:fps=30,eq=saturation=1.08:contrast=1.04")
        a = f"[0:a]volume={o.get('amb',0.35)},aresample=48000,aformat=channel_layouts=stereo,apad[a]"
        inp = ["-ss",str(ss),"-i",src]
    fc = (f"{v},fade=in:d=0.12:color=white,format=yuva420p[c];[2:v]crop={FW}:{FH}:{FX}:{FY},format=gray[m];[c][m]alphamerge[cm];"
          f"[1:v][cm]overlay={FX}:{FY}[b1];[b1][3:v]overlay=0:0,format=yuv420p[v];{a}")
    run(["ffmpeg","-v","error","-y",*inp,"-loop","1","-i",BG,"-loop","1","-i",MASK,"-loop","1","-i",BORDER,
         "-filter_complex",fc,"-map","[v]","-map","[a]","-frames:v",str(n),"-t",f"{n/30:.3f}","-r","30",
         "-c:v","libx264","-preset","fast","-crf","18","-c:a","aac","-b:a","192k",out]); return out

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"

def build(key):
    R = REELS[key]; tmp = os.path.join(W, "_tmp3_" + key); os.makedirs(tmp, exist_ok=True)
    fx = sfx(tmp); parts, t, events, aud = [], 0.0, [], []
    for i, (kind, src, ss, dur, o) in enumerate(R["shots"]):
        parts.append(shot_video(i, kind, src, ss, dur, o, tmp)); n = int(round(dur*30)); d = n/30
        if i > 0: aud.append((fx["whoosh"], max(t - 0.2, 0), 0.55))
        if o.get("vo"): aud.append((A(o["vo"]), t, 1.0, VO_LEAD))
        if "boom" in o: aud.append((fx["boom"], t + o["boom"], 0.9))
        for a, b, txt, sty in o.get("titles", []):
            pre = POP if sty in ("T", "Huge") else r"{\fad(80,0)\fscx70\fscy70\t(0,120,\fscx100\fscy100)}"
            events.append((t + a, t + min(b, d), pre + txt, sty))
            if sty.startswith("Pill"): aud.append((fx["pop"], t + a, 0.5))
        t += d
    total = t
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(tmp, "joined.mp4")
    run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",lst,"-c:v","copy","-c:a","aac",joined])
    L = ["[Script Info]","ScriptType: v4.00+","PlayResX: 1080","PlayResY: 1920","WrapStyle: 2","","[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         "Style: T,Archivo Black,82,&H00FFFFFF,&H00FFFFFF,&H00301040,&H80000000,0,0,0,0,100,100,1,0,1,3,5,8,60,60,292,1",
         "Style: Huge,Archivo Black,112,&H00FFFFFF,&H00FFFFFF,&H00301040,&H80000000,0,0,0,0,100,100,2,0,1,5,7,8,40,40,280,1",
         "Style: Pill,Archivo Black,40,&H00180A1A,&H00FFFFFF,&H00B34FFF,&H00B34FFF,0,0,0,0,100,100,1,0,3,14,0,5,0,0,0,1",
         "Style: PillY,Archivo Black,40,&H00180A1A,&H00FFFFFF,&H003FD2FF,&H003FD2FF,0,0,0,0,100,100,1,0,3,14,0,5,0,0,0,1",
         "Style: PillG,Archivo Black,46,&H00102010,&H00FFFFFF,&H0066D325,&H0066D325,0,0,0,0,100,100,1,0,3,16,0,5,0,0,0,1",
         "","[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    L += [f"Dialogue: 1,{ts(a)},{ts(b)},{s},,0,0,0,,{x}" for a, b, x, s in events]
    ass = os.path.join(tmp, "subs.ass"); open(ass, "w").write("\n".join(L) + "\n")
    # Audio: ambiente de tomas + música continua (ducking bajo voz) + voces + efectos
    ins = ["-i", joined, "-i", A("musica-fiesta.mp3")]; fc = []; vo_labels = []; fx_labels = []
    for k, item in enumerate(aud):
        path, start, vol = item[0], item[1], item[2]; lead = item[3] if len(item) > 3 else 0
        ins += ["-i", path]; idx = k + 2; lab = f"x{k}"
        fc.append(f"[{idx}:a]atrim=start={lead},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume={vol},adelay={int(start*1000)}|{int(start*1000)},apad[{lab}]")
        (vo_labels if path.endswith(".mp3") else fx_labels).append(lab)
    vo_mix = "".join(f"[{l}]" for l in vo_labels)
    fc.append(f"{vo_mix}amix=inputs={len(vo_labels)}:normalize=0,volume=1.9,asplit=2[vo][sc]")
    fc.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{total:.2f},volume=0.55,afade=t=in:d=0.4,afade=t=out:st={total-1.5:.2f}:d=1.5[m0]")
    fc.append("[m0][sc]sidechaincompress=threshold=0.04:ratio=5:attack=15:release=300[m]")
    fx_mix = "".join(f"[{l}]" for l in fx_labels)
    fc.append(f"[0:a][m][vo]{fx_mix}amix=inputs={3+len(fx_labels)}:duration=first:normalize=0,alimiter=limit=0.95[a]")
    fc.append(f"[0:v]ass={ass}:fontsdir={FONTS}[v]")
    final = os.path.join(W, R["out"])
    run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",";".join(fc),"-map","[v]","-map","[a]","-t",f"{total:.2f}",
         "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",final])
    print(key, round(total, 2), final)

if __name__ == "__main__":
    for k in (sys.argv[1:] or REELS): build(k)
