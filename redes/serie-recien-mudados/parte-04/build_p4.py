"""Recién mudados · Parte 4 "La portería" — montaje (opción B, multicámara con caras).
Las tomas de Flow traen el diálogo; la música del tema va baja y se agacha cuando hablan.
Los subtítulos siguen el guion (tiempos medidos por las pausas de cada toma)."""
import subprocess, os
W = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(W)
C = os.environ.get("CARDS", "/home/claude/catalogostore/tools/piezas")
FONTS = os.path.join(C, "fonts")
T = lambda p: os.path.join(W, "tomas", p)
MUSIC = os.environ.get("MUSIC", os.path.join(R, "musica-tema.mp3"))
TIT, ANC, END = (os.path.join(C, f"{n}.png") for n in ("titulo_p4", "ancla_discreto_p4", "end_discreto"))
PINK, WHITE = r"{\c&HB34FFF&}", r"{\c&HFFFFFF&}"

# (src, src_start, src_end/dur, zoom_from, zoom_to, volumen)
SHOTS = [
    (TIT, 0, 2.0, 1.00, 1.04, 0),
    (T("b1-citofono.mp4"), 0.3, 10.0, 1.00, 1.05, 1.0),
    (T("b2-vale-suegra.mp4"), 0.3, 4.03, 1.04, 1.10, 1.0),
    (T("b3-gloria-entra.mp4"), 0.8, 8.04, 1.00, 1.05, 1.0),
    (T("b4-cocina.mp4"), 1.2, 8.04, 1.00, 1.05, 1.0),
    (T("b5-guino.mp4"), 1.6, 7.6, 1.02, 1.08, 1.0),
    (ANC, 0, 3.8, 1.00, 1.05, 0),
    (T("b6-maleta.mp4"), 0.5, 8.04, 1.00, 1.07, 1.0),
    (END, 0, 3.2, 1.00, 1.04, 0),
]
# (toma, desde, hasta) en segundos del archivo original de la toma
SUBS = [
    (1, 3.0, 3.7, "¿Quién era?"),
    (1, 4.0, 4.8, "El paquete."),
    (1, 4.8, 5.6, PINK + "¡Ay, qué bien!"),
    (1, 6.0, 8.6, "…y mi mamá."),
    (2, 0.4, 2.4, "El paquete lo estábamos\\Nesperando hace una semana…"),
    (2, 2.4, 4.03, PINK + "a tu mamá, nadie."),
    (3, 3.9, 6.0, "Mijo, el portero me dio esto."),
    (3, 6.0, 8.04, "¿Qué es? " + PINK + "Suena raro."),
    (4, 1.6, 3.3, "No dice nada:\\Nni marca, ni qué es…"),
    (4, 3.3, 5.6, PINK + "¡Son cositas de cocina!"),
    (4, 5.6, 8.04, "¿Cocina?\\N¿Ustedes cocinan?"),
    (5, 1.8, 4.5, "Treinta y cinco años de casada."),
    (5, 4.5, 7.2, "Yo sé muy bien qué son\\N" + PINK + "“cositas de cocina”."),
    (7, 1.4, 3.8, "Bueno… me quedo\\Nuna " + PINK + "semanita" + WHITE + ", mijo."),
]

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
POP = r"{\fad(60,80)\fscx86\fscy86\t(0,140,\fscx100\fscy100)}"

def make_ass(starts):
    L = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         "Style: Sub,Archivo,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,70,70,330,1",
         "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for k, a, b, txt in SUBS:
        t0, ss, end = starts[k], SHOTS[k][1], starts[k + 1]
        A, B = max(t0, t0 + a - ss), min(end, t0 + b - ss)
        if B > A + 0.2:
            L.append(f"Dialogue: 0,{ts(A)},{ts(B)},Sub,,0,0,0,,{POP}{txt}")
    p = os.path.join(W, "p4.ass"); open(p, "w").write("\n".join(L) + "\n"); return p

def build():
    tmp = os.path.join(W, "_tmp_build"); os.makedirs(tmp, exist_ok=True)
    parts, t, starts = [], 0.0, []
    for i, (src, ss, se, z0, z1, vol) in enumerate(SHOTS):
        dur = se if src.endswith(".png") else se - ss
        out = os.path.join(tmp, f"s{i}.mp4"); n = int(round(dur * 30))
        zp = f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        if src.endswith(".png"):
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                   "-frames:v", str(n), "-vf", f"scale=1080:1920,{zp.replace(':s=', ':d=' + str(n) + ':s=')},format=yuv420p",
                   "-t", f"{n/30:.3f}"]
        else:
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", src, "-frames:v", str(n), "-t", f"{n/30:.3f}",
                   "-vf", f"fps=30,scale=1080:1920:flags=lanczos,{zp.replace(':s=', ':d=1:s=')},format=yuv420p",
                   "-af", f"volume={vol},afade=t=in:d=0.05,afade=t=out:st={max(0, n/30-0.08):.3f}:d=0.08,"
                          "aresample=48000,aformat=channel_layouts=stereo,apad", "-shortest"]
        subprocess.run(cmd + ["-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "160k", out], check=True)
        parts.append(out); starts.append(t); t += n / 30
    starts.append(t); total = t
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
    joined = os.path.join(tmp, "joined.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "copy", "-c:a", "aac", joined], check=True)
    ass = make_ass(starts)
    fc = [
        "[0:a]volume=0.85,asplit=2[dlg][sc]",
        f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.32,afade=t=in:st=0:d=0.6,afade=t=out:st={total-1.8:.2f}:d=1.8[m]",
        "[m][sc]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=400[md]",
        "[dlg][md]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]",
        f"[0:v]ass={ass}:fontsdir={FONTS}[v]",
    ]
    final = os.path.join(W, "recien-mudados-parte-04.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-stream_loop", "-1", "-i", MUSIC, "-filter_complex", ";".join(fc),
                    "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final], check=True)
    print("total", round(total, 2), final)

if __name__ == "__main__":
    build()
