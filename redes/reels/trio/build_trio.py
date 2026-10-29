"""Reel loción Trío — estructura de 8 piezas. Voz de Daniela a velocidad real; subtítulos tipo karaoke arriba."""
import os, re, subprocess
W = os.path.dirname(os.path.abspath(__file__))
C = os.environ.get("CARDS", "/tmp/claude-0/-home-claude/d3141047-47b3-5415-be12-edec1a18ebf1/scratchpad/vid/cards")
FONTS = os.path.join(C, "fonts")
T = lambda p: os.path.join(W, "tomas", p)
F1, F2, F3, F4, F5 = T("f1-lampara.mp4"), T("f2-manos-locion.mp4"), T("f3-gota.mp4"), T("f4-pareja-cama.mp4"), T("f5-masaje.mp4")
G, B3, END = (os.path.join(C, n + ".png") for n in ("gancho_trio", "bucle_trio", "end_trio"))
VOZ = os.path.join(W, "audio", "daniela.mp3")
MUSIC = "/home/claude/catalogostore/redes/serie-recien-mudados/musica-tema.mp3"

# (src, inicio, dur, zoom_desde, zoom_hasta, volumen)
SHOTS = [
    (G, 0, 3.6, 1.18, 1.00, 0),      # 1 gancho: zoom hacia atrás
    (F1, 1.5, 5.0, 1.00, 1.08, 0.2),  # 2 intro
    (F2, 0.0, 2.7, 1.00, 1.06, 0.2),  # 3 cuerpo 1
    (F2, 3.0, 3.6, 1.08, 1.14, 0.2),
    (F5, 3.2, 2.5, 1.00, 1.06, 0.2),
    (G, 0, 1.9, 1.00, 1.25, 0),       # 4 bucle
    (F3, 0.5, 5.8, 1.00, 1.10, 0.2),  # 5 cuerpo 2
    (B3, 0, 3.2, 1.00, 1.08, 0),      # 6 bucle
    (F4, 0.0, 2.0, 1.00, 1.05, 0.2),  # 7 cuerpo 3
    (F1, 6.3, 1.5, 1.08, 1.14, 0.2),
    (F5, 5.7, 1.7, 1.10, 1.16, 0.2),
    (G, 0, 3.2, 1.05, 1.15, 0),       # 8 cierre
    (END, 0, 6.2, 1.00, 1.04, 0),
]
# frases (inicio, fin) medidas en la voz
LINES = [
    (0.0, 3.49, "Este frasquito reemplaza tres cosas de tu mesa de noche."),
    (3.87, 8.27, "Quédate hasta el final, porque el tercer uso es el que casi nadie conoce."),
    (8.86, 11.10, "Uno: es loción de masajes."),
    (11.44, 14.74, "Un poquito en las manos, las frotas para calentarla…"),
    (15.03, 17.13, "y despacio por la espalda."),
    (17.46, 18.95, "Pero eso es lo más básico."),
    (19.41, 24.87, "Dos: es hidratante íntimo, a base de agua: suave y fácil de limpiar."),
    (25.24, 28.13, "Y el tercero… es el que más nos preguntan."),
    (28.40, 30.23, "Tiene un sabor delicioso."),
    (30.51, 33.26, "Así que los besos no tienen por qué detenerse."),
    (33.63, 36.56, "Si llegaste hasta aquí, eres de los que sí se atreven."),
    (36.84, 39.44, "Comenta TRÍO y te contamos cómo pedirlo."),
    (39.71, 42.60, "Y guárdalo para tu próxima noche de masajes."),
]
PINK_WORDS = {"TRÍO", "tres", "Uno:", "Dos:", "tercero…", "tercer"}
ENC = ["-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"

def wrap(words, n=4):
    """parte la frase en renglones de ~n palabras para que quepan 2-3 líneas arriba"""
    out, line = [], []
    for w in words:
        line.append(w)
        if len(line) >= n: out.append(line); line = []
    if line: out.append(line)
    return out

def make_ass():
    L = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         # karaoke: primary = palabra ya dicha (blanco), secondary = por decir (gris)
         "Style: Top,Archivo,74,&H00FFFFFF,&H00A8A0A8,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,8,90,90,300,1",
         "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for a, b, text in LINES:
        if a >= 36.7: continue  # en el cierre el logo ocupa la parte de arriba
        words = text.split()
        # duración de cada palabra proporcional a su largo
        tot = sum(len(w) + 2 for w in words); dur = (b - a) * 0.92
        rows, parts = wrap(words), []
        for r, row in enumerate(rows):
            seg = []
            for w in row:
                k = max(1, round(100 * dur * (len(w) + 2) / tot))
                col = r"{\1c&HB34FFF&}" if w in PINK_WORDS else ""
                seg.append(rf"{{\kf{k}}}{col}{w}" + (r"{\1c&HFFFFFF&}" if col else ""))
            parts.append(" ".join(seg))
        L.append(f"Dialogue: 0,{ts(a)},{ts(b + 0.25)},Top,,0,0,0,,{{\\fad(80,80)}}" + r"\N".join(parts))
    p = os.path.join(W, "trio.ass"); open(p, "w").write("\n".join(L) + "\n"); return p

def run(cmd, out):
    tmp = out[:-4] + ".part.mp4"; subprocess.run(cmd + [tmp], check=True); os.replace(tmp, out)

def build():
    d = os.path.join(W, "_segs"); os.makedirs(d, exist_ok=True)
    files, t = [], 0.0
    for i, (src, ss, dur, z0, z1, vol) in enumerate(SHOTS):
        n = int(round(dur * 30)); out = os.path.join(d, f"s{i:02d}.mp4")
        zp = f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        if src.endswith(".png"):
            run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                 "-frames:v", str(n), "-vf", f"scale=1080:1920,{zp.replace(':s=', ':d=' + str(n) + ':s=')},format=yuv420p",
                 "-t", f"{n/30:.3f}", *ENC], out)
        else:
            run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", src, "-frames:v", str(n), "-t", f"{n/30:.3f}",
                 "-vf", f"fps=30,scale=1080:1920:flags=lanczos,{zp.replace(':s=', ':d=1:s=')},format=yuv420p",
                 "-af", f"volume={vol},aresample=48000,aformat=channel_layouts=stereo,apad", "-shortest", *ENC], out)
        files.append(out); t += n / 30
    total = t
    lst = os.path.join(d, "list.txt"); open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    joined = os.path.join(d, "joined.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy"], joined)
    ass = make_ass()
    fc = ["[1:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.15,apad,asplit=2[vo][sc]",
          f"[2:a]aresample=48000,volume=0.28,afade=t=in:st=0:d=0.6,afade=t=out:st={total-1.6}:d=1.6[m]",
          "[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[md]",
          "[vo][md][0:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.95[a]",
          f"[0:v]ass={ass}:fontsdir={FONTS}[v]"]
    final = os.path.join(W, "trio-3-usos.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-i", VOZ, "-i", MUSIC, "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"], final)
    print("total", round(total, 2), final)

if __name__ == "__main__":
    build()
