"""Recién mudados · Parte 1 — montaje.
Voz (Daniela + Vale) colocada por tiempos, ambiente de las tomas de Flow bajo, música con ducking,
subtítulos quemados (Archivo, palabra clave en rosa), placa de producto y cierre."""
import subprocess, os
U = "/root/.claude/uploads/d3141047-47b3-5415-be12-edec1a18ebf1"
W = os.path.dirname(os.path.abspath(__file__))
C = "/tmp/claude-0/-home-claude/d3141047-47b3-5415-be12-edec1a18ebf1/scratchpad/vid/cards"
FONTS = os.path.join(C, "fonts")
def u(prefix): return next(os.path.join(U, f) for f in os.listdir(U) if f.startswith(prefix))
DOOR, COUPLE, PHONES, HANDS, SHOULDER = u("baaa82c5"), u("840606f9"), u("8d1ffa03"), u("c8d5f929"), u("1ed46a6c")
B1, B2, B3, VALE = u("135c1769"), u("e83de6f9"), u("208e9765"), u("059bcfe9")
MUSIC = u("9a1a86f1")
PROD, END = os.path.join(C, "prod_vor.png"), os.path.join(C, "end_atreve.png")
PINK, WHITE = r"{\c&HB34FFF&}", r"{\c&HFFFFFF&}"

# (src, src_start, dur, zoom_from, zoom_to)
SHOTS = [
    (DOOR, 0.2, 2.8, 1.00, 1.06),
    (DOOR, 5.6, 2.0, 1.04, 1.10),
    (COUPLE, 2.0, 2.6, 1.00, 1.06),
    (COUPLE, 5.0, 2.0, 1.14, 1.20),
    (PHONES, 1.5, 3.3, 1.00, 1.06),
    (PHONES, 3.6, 2.9, 1.10, 1.16),
    (HANDS, 2.8, 4.1, 1.00, 1.08),
    (COUPLE, 4.6, 2.4, 1.18, 1.24),
    (PHONES, 5.7, 2.3, 1.12, 1.18),
    (PROD, 0, 3.4, 1.00, 1.06),
    (SHOULDER, 2.0, 3.0, 1.00, 1.06),
    (SHOULDER, 5.0, 2.8, 1.14, 1.22),
    (END, 0, 3.8, 1.00, 1.04),
]
# voz: (archivo, recorte_inicio, recorte_fin, colocar_en)
VOICE = [(B1, 0, 12.7, 0.0), (VALE, 0, 2.8, 12.9), (B2, 0, 11.9, 15.8), (VALE, 4.8, 7.55, 28.1), (B3, 0, 6.2, 30.8)]
SUBS = [
    (0.0, 2.75, "Recién mudados\\N" + PINK + "Parte 1", "Big"),
    (3.5, 6.05, "Vale y Andrés se fueron\\Na vivir juntos"),
    (6.32, 9.05, "y en tres semanas,\\N" + PINK + "ni una sola cita."),
    (9.44, 12.7, "Hasta la primera noche,\\Ncada uno en su " + PINK + "celular."),
    (13.05, 15.6, "“¿Te acuerdas de la última vez\\Nque jugamos a algo?”"),
    (15.8, 20.1, "La rutina " + PINK + "apaga las ganas," + WHITE + "\\Ny lo nuevo las vuelve a prender."),
    (20.5, 22.0, "Por eso hicieron un pacto:"),
    (22.3, 24.5, PINK + "viernes de juego,\\N" + WHITE + "sin celular."),
    (28.2, 30.7, "“¿Qué es lo que nunca\\Nle has contado a tu pareja?”"),
    (30.8, 33.6, "Y Andrés…\\N" + PINK + "se quedó callado."),
]

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
POP = r"{\fad(60,80)\fscx86\fscy86\t(0,140,\fscx100\fscy100)}"

def make_ass(total, card_ranges):
    L = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         "Style: Sub,Archivo,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,70,70,520,1",
         "Style: Big,Archivo,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,4,5,70,70,0,1",
         "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for s in SUBS:
        a, b, t = s[0], s[1], s[2]
        st = s[3] if len(s) > 3 else "Sub"
        if any(x <= a < y for x, y in card_ranges): continue
        L.append(f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{POP}{t}")
    p = os.path.join(W, "p1.ass"); open(p, "w").write("\n".join(L) + "\n"); return p

def build():
    parts, t, card_ranges = [], 0.0, []
    for i, (src, ss, dur, z0, z1) in enumerate(SHOTS):
        out = os.path.join(W, f"s{i}.mp4"); n = int(round(dur * 30))
        zp = f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        if src.endswith(".png"):
            card_ranges.append((t, t + dur))
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                   "-frames:v", str(n), "-vf", f"scale=1080:1920,{zp.replace(':s=', ':d=' + str(n) + ':s=')},format=yuv420p",
                   "-t", f"{n/30:.3f}"]
        else:
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", src, "-frames:v", str(n), "-t", f"{n/30:.3f}",
                   "-vf", f"fps=30,scale=1080:1920:flags=lanczos,{zp.replace(':s=', ':d=1:s=')},format=yuv420p",
                   "-af", "aresample=48000,aformat=channel_layouts=stereo"]
        subprocess.run(cmd + ["-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "160k", out], check=True)
        parts.append(out); t += n / 30
    total = t
    lst = os.path.join(W, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(W, "joined.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "copy", "-c:a", "aac", joined], check=True)
    ass = make_ass(total, card_ranges)
    # voz: cada pieza recortada y retrasada a su lugar
    ins, fc = ["-i", joined], []
    for k, (f, a, b, at) in enumerate(VOICE):
        ins += ["-i", f]
        fc.append(f"[{k+1}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,adelay={int(at*1000)}|{int(at*1000)}[v{k}]")
    mi = len(VOICE) + 1; ins += ["-i", MUSIC]
    fc.append("".join(f"[v{k}]" for k in range(len(VOICE))) + f"amix=inputs={len(VOICE)}:normalize=0,volume=1.2,apad,asplit=2[vo][sc]")
    fc.append(f"[{mi}:a]aresample=48000,volume=0.30,afade=t=in:st=0:d=0.8,afade=t=out:st={total-1.8}:d=1.8[m]")
    fc.append("[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md]")
    fc.append("[0:a]volume=0.35[amb]")
    fc.append("[vo][md][amb]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]")
    fc.append(f"[0:v]ass={ass}:fontsdir={FONTS}[v]")
    final = os.path.join(W, "recien-mudados-parte-01.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                    "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final], check=True)
    print("total", round(total, 2), final)

if __name__ == "__main__":
    build()
