"""Recién mudados · Parte 2 — montaje (Andrés en primera persona).
Misma receta que build_p1.py: voz colocada por tiempos, ambiente de las tomas bajo,
música con ducking, subtítulos quemados, placa del producto y cierre."""
import subprocess, os
W = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(W)
C = os.environ.get("CARDS", "/tmp/claude-0/-home-claude/d3141047-47b3-5415-be12-edec1a18ebf1/scratchpad/vid/cards")
FONTS = os.path.join(C, "fonts")
T = lambda p: os.path.join(W, "tomas", p)
P1 = lambda p: os.path.join(R, "parte-01", "tomas", p)
DOOR, SHOULDER = P1("t1-puerta.mp4"), P1("t6-carta.mp4")
N1, N2, N3, N4, N5 = T("n1-solo-sofa.mp4"), T("n2-reloj.mp4"), T("n3-mano-vale.mp4"), T("n4-ventana.mp4"), T("n5-manos-sofa.mp4")
ANDRES, VALE = os.path.join(W, "audio", "andres.mp3"), os.path.join(W, "audio", "vale.mp3")
MUSIC = os.path.join(R, "musica-tema.mp3")
PROD, END = os.path.join(C, "prod_spray_p2.png"), os.path.join(C, "end_calma.png")
PINK, WHITE = r"{\c&HB34FFF&}", r"{\c&HFFFFFF&}"
TEMPO = 1.10  # la voz de Andrés salió de 34 s; se acelera un 10 %

# (src, src_start, dur, zoom_from, zoom_to)
SHOTS = [
    (DOOR, 0.2, 2.2, 1.00, 1.06),
    (SHOULDER, 2.0, 3.9, 1.00, 1.08),
    (N1, 3.0, 3.0, 1.00, 1.06),
    (N1, 6.0, 2.0, 1.10, 1.16),
    (N2, 1.5, 2.6, 1.00, 1.06),
    (N2, 4.5, 2.4, 1.12, 1.18),
    (N3, 2.2, 3.4, 1.08, 1.14),
    (N4, 1.0, 3.0, 1.00, 1.06),
    (N4, 4.6, 2.4, 1.14, 1.20),
    (PROD, 0, 5.0, 1.00, 1.07),
    (N5, 1.0, 1.6, 1.00, 1.05),
    (N5, 5.2, 1.1, 1.06, 1.10),
    (END, 0, 3.6, 1.00, 1.04),
]
# voz: (archivo, recorte_inicio, recorte_fin, colocar_en, tempo)
VOICE = [(ANDRES, 0.0, 30.66, 1.9, TEMPO), (VALE, 0.25, 2.30, 30.05, 1.0), (ANDRES, 31.5, 34.19, 32.75, TEMPO)]
SUBS = [
    (0.0, 1.9, "Recién mudados\\N" + PINK + "Parte 2", "Big"),
    (2.2, 4.67, "Cuando Vale me preguntó\\Nqué nunca le había contado…"),
    (5.08, 6.0, "me quedé callado."),
    (6.43, 8.49, "La verdad, me daba pena:"),
    (9.03, 10.83, "esos momentos me duraban\\N" + PINK + "muy poquito."),
    (11.3, 13.15, "Y por eso,\\Nmejor ni la buscaba."),
    (13.83, 15.84, "Cuando por fin se lo conté,\\N" + PINK + "no se rió."),
    (16.29, 17.7, "Me dijo que le pasa\\Na muchos…"),
    (17.9, 19.4, "y que casi nadie lo habla."),
    (19.71, 20.9, "La presión lo empeora;"),
    (21.08, 22.6, PINK + "respirar lento ayuda."),
    (22.84, 24.8, "Y si persiste,\\Ntoca ir al médico."),
    (30.05, 32.2, "“Yo también tengo algo\\N" + PINK + "que confesarte.”"),
]

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
POP = r"{\fad(60,80)\fscx86\fscy86\t(0,140,\fscx100\fscy100)}"

def make_ass(card_ranges):
    L = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         "Style: Sub,Archivo,68,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,70,70,520,1",
         "Style: Big,Archivo,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,6,4,5,70,70,0,1",
         "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for s in SUBS:
        a, b, t = s[0], s[1], s[2]
        st = s[3] if len(s) > 3 else "Sub"
        if any(x <= a < y for x, y in card_ranges): continue
        b = min([b] + [x for x, y in card_ranges if a < x < b])
        L.append(f"Dialogue: 0,{ts(a)},{ts(b)},{st},,0,0,0,,{POP}{t}")
    p = os.path.join(W, "p2.ass"); open(p, "w").write("\n".join(L) + "\n"); return p

def build():
    tmp = os.path.join(W, "_tmp"); os.makedirs(tmp, exist_ok=True)
    parts, t, card_ranges = [], 0.0, []
    for i, (src, ss, dur, z0, z1) in enumerate(SHOTS):
        out = os.path.join(tmp, f"s{i}.mp4"); n = int(round(dur * 30))
        zp = f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        if src.endswith(".png"):
            card_ranges.append((t, t + n / 30))
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                   "-frames:v", str(n), "-vf", f"scale=1080:1920,{zp.replace(':s=', ':d=' + str(n) + ':s=')},format=yuv420p",
                   "-t", f"{n/30:.3f}"]
        else:
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", src, "-frames:v", str(n), "-t", f"{n/30:.3f}",
                   "-vf", f"fps=30,scale=1080:1920:flags=lanczos,{zp.replace(':s=', ':d=1:s=')},format=yuv420p",
                   "-af", "aresample=48000,aformat=channel_layouts=stereo,apad", "-shortest"]
        subprocess.run(cmd + ["-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "160k", out], check=True)
        parts.append(out); t += n / 30
    total = t
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(tmp, "joined.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "copy", "-c:a", "aac", joined], check=True)
    ass = make_ass(card_ranges)
    ins, fc = ["-i", joined], []
    for k, (f, a, b, at, tempo) in enumerate(VOICE):
        ins += ["-i", f]
        fc.append(f"[{k+1}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,atempo={tempo},aresample=48000,aformat=channel_layouts=stereo,"
                  f"adelay={int(at*1000)}|{int(at*1000)}[v{k}]")
    mi = len(VOICE) + 1; ins += ["-i", MUSIC]
    fc.append("".join(f"[v{k}]" for k in range(len(VOICE))) + f"amix=inputs={len(VOICE)}:normalize=0,volume=1.2,apad,asplit=2[vo][sc]")
    fc.append(f"[{mi}:a]aresample=48000,volume=0.30,afade=t=in:st=0:d=0.8,afade=t=out:st={total-1.8}:d=1.8[m]")
    fc.append("[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md]")
    fc.append("[0:a]volume=0.35[amb]")
    fc.append("[vo][md][amb]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]")
    fc.append(f"[0:v]ass={ass}:fontsdir={FONTS}[v]")
    final = os.path.join(W, "recien-mudados-parte-02.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
                    "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final], check=True)
    print("total", round(total, 2), final)

if __name__ == "__main__":
    build()
