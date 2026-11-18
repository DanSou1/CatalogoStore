"""Recién mudados · Parte 4 "La portería" — montaje v2 (opción B, multicámara con caras).

Cambios frente a la v1 (pedidos por Daniel):
- Todas las tomas en la misma sala (set fijo en Flow) y con el color igualado entre tomas.
- Cortes suavizados: fundido corto entre tomas (XF) y las risas del público cruzan el corte,
  como en una sitcom real.
- Risas grabadas (ElevenLabs) después de cada remate y voz de Vale en el ancla.
- Un fondo continuo de sala muy bajo para que el sonido no salte entre tomas.
"""
import subprocess, os, json
W = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(W)
C = os.environ.get("CARDS", "/home/claude/catalogostore/tools/piezas")
FONTS = os.path.join(C, "fonts")
T = lambda p: os.path.join(W, "tomas", p)
A = lambda p: os.path.join(W, "audio", p)
MUSIC = os.path.join(R, "musica-tema.mp3")
TIT, ANC, END = (os.path.join(C, f"{n}.png") for n in ("titulo_p4", "ancla_discreto_p4", "end_discreto"))
PINK, WHITE = r"{\c&HB34FFF&}", r"{\c&HFFFFFF&}"
XF = 0.14          # fundido entre tomas (s)
TARGET = (95, 68, 46)  # color medio de referencia (toma del citófono)

def first(*opts):
    for o in opts:
        if os.path.exists(o): return o
    raise FileNotFoundError(opts)

# (src, inicio, fin|duración, zoom_de, zoom_a)
SHOTS = [
    (TIT, 0, 2.0, 1.00, 1.04),
    (T("b1-citofono.mp4"), 0.3, 9.4, 1.00, 1.05),
    (T("c2-vale-suegra.mp4"), 0.9, 6.9, 1.03, 1.08),
    (first(T("c3-gloria-entra.mp4"), T("b3-gloria-entra.mp4")), 0.6, 8.04, 1.00, 1.05),
    (T("c3-andres-contador.mp4"), 1.1, 7.5, 1.02, 1.07),
    (first(T("c4-cocina.mp4"), T("b4-cocina.mp4")), 0.8, 8.04, 1.00, 1.05),
    (T("c5-guino.mp4"), 1.1, 8.04, 1.02, 1.08),
    (ANC, 0, 4.6, 1.00, 1.05),
    (T("b6-maleta.mp4"), 0.5, 8.04, 1.00, 1.07),
    (END, 0, 3.4, 1.00, 1.04),
]
# Subtítulos: (toma, desde, hasta, texto) en segundos del archivo de la toma (se leen de subs.json si existe)
SUBS = [
    (1, 3.0, 3.7, "¿Quién era?"), (1, 4.0, 4.8, "El paquete."), (1, 4.8, 5.6, PINK + "¡Ay, qué bien!"),
    (1, 6.0, 8.6, "…y mi mamá."),
    (2, 1.2, 3.8, "El paquete lo estábamos\\Nesperando hace una semana…"), (2, 4.1, 6.0, PINK + "a tu mamá, nadie."),
    (3, 3.9, 6.0, "Mijo, el portero me dio esto."), (3, 6.0, 8.04, "¿Qué es? " + PINK + "Suena raro."),
    (4, 1.4, 2.6, "Yo soy contador."), (4, 2.7, 4.3, "Con los números no sudo."),
    (4, 4.6, 7.4, "Con mi mamá y una caja…\\N" + PINK + "sí."),
    (5, 1.6, 3.3, "No dice nada:\\Nni marca, ni qué es…"), (5, 3.3, 5.6, PINK + "¡Son cositas de cocina!"),
    (5, 5.6, 8.04, "¿Cocina?\\N¿Ustedes cocinan?"),
    (6, 1.4, 4.4, "Mija, treinta y cinco\\Naños de casada."), (6, 4.4, 7.6, "Yo sé muy bien qué son\\N" + PINK + "“cositas de cocina”."),
    (8, 1.4, 3.8, "Bueno… me quedo\\Nuna " + PINK + "semanita" + WHITE + ", mijo."),
]
# Risas: (toma, segundo de la toma, archivo, volumen). Arrancan sobre el remate y cruzan el corte.
LAUGHS = [
    (1, 7.6, "risa-media.mp3", 0.55), (2, 5.9, "risa-media.mp3", 0.6), (3, 7.6, "risa-corta.mp3", 0.5),
    (4, 6.9, "risa-media.mp3", 0.6), (5, 7.5, "risa-grande.mp3", 0.7), (6, 7.3, "risa-grande.mp3", 0.75),
    (7, 3.6, "risa-corta.mp3", 0.5), (8, 5.2, "risa-grande.mp3", 0.75),
]
VO = [(7, 0.35, "vale-ancla.mp3", 1.0)]  # voz de Vale sobre la placa del ancla
SUBS_VO = [(7, 0.35, 4.3, "Lo bueno: la caja llega sin marca.\\N" + PINK + "Lo malo… llegó con mi suegra.")]

def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
POP = r"{\fad(60,80)\fscx86\fscy86\t(0,140,\fscx100\fscy100)}"

def mean_rgb(src):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", "fps=1,scale=1:1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True).stdout
    px = [out[i:i + 3] for i in range(0, len(out) - 2, 3)]
    return [sum(p[c] for p in px) / len(px) for c in range(3)]

def grade(src):
    m = mean_rgb(src)
    g = [max(0.85, min(1.15, TARGET[c] / max(m[c], 1))) for c in range(3)]
    return f"colorchannelmixer=rr={g[0]:.3f}:gg={g[1]:.3f}:bb={g[2]:.3f},eq=contrast=1.04:saturation=1.03"

def build():
    tmp = os.path.join(W, "_tmp_build"); os.makedirs(tmp, exist_ok=True)
    parts, durs = [], []
    for i, (src, ss, se, z0, z1) in enumerate(SHOTS):
        img = src.endswith(".png")
        dur = se if img else se - ss
        n = int(round(dur * 30)); out = os.path.join(tmp, f"s{i}.mp4")
        zp = f"zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30"
        if img:
            cmd = ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", src, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                   "-frames:v", str(n), "-vf", f"scale=1080:1920,{zp.replace(':s=', ':d=' + str(n) + ':s=')},format=yuv420p",
                   "-t", f"{n/30:.3f}"]
        else:
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", src, "-frames:v", str(n), "-t", f"{n/30:.3f}",
                   "-vf", f"fps=30,scale=1080:1920:flags=lanczos,{grade(src)},{zp.replace(':s=', ':d=1:s=')},format=yuv420p",
                   "-af", "aresample=48000,aformat=channel_layouts=stereo,apad", "-shortest"]
        subprocess.run(cmd + ["-r", "30", "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-c:a", "pcm_s16le",
                              out.replace(".mp4", ".mov")], check=True)
        parts.append(out.replace(".mp4", ".mov")); durs.append(n / 30)
    starts, t = [], 0.0
    for i, d in enumerate(durs):
        starts.append(t); t += d - (XF if i < len(durs) - 1 else 0)
    total = t
    at = lambda k, s: starts[k] + (s - (0 if SHOTS[k][0].endswith(".png") else SHOTS[k][1]))
    # --- subtítulos
    L = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         "Style: Sub,Archivo,66,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,70,70,330,1",
         "Style: VO,Archivo,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,70,70,230,1",
         "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    have_vo = all(os.path.exists(A(f)) for _, _, f, _ in VO)
    for st, rows in (("Sub", SUBS), ("VO", SUBS_VO if have_vo else [])):
        for k, a, b, txt in rows:
            end = starts[k] + durs[k] - XF
            A0, B0 = max(starts[k], at(k, a)), min(end, at(k, b))
            if B0 > A0 + 0.2:
                L.append(f"Dialogue: 0,{ts(A0)},{ts(B0)},{st},,0,0,0,,{POP}{txt}")
    ass = os.path.join(W, "p4.ass"); open(ass, "w").write("\n".join(L) + "\n")
    # --- video + diálogo con fundidos cortos
    ins, fc = [], []
    for p in parts: ins += ["-i", p]
    v, a = "[0:v]", "[0:a]"
    for i in range(1, len(parts)):
        off = starts[i]
        fc.append(f"{v}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[v{i}]")
        fc.append(f"{a}[{i}:a]acrossfade=d={XF}:c1=tri:c2=tri[a{i}]")
        v, a = f"[v{i}]", f"[a{i}]"
    fc.append(f"{v}ass={ass}:fontsdir={FONTS}[vout]")
    fc.append(f"{a}volume=0.9,asplit=2[dlg][sc]")
    n_in = len(parts)
    # música
    ins += ["-stream_loop", "-1", "-i", MUSIC]; mi = n_in; n_in += 1
    fc.append(f"[{mi}:a]aresample=48000,aformat=channel_layouts=stereo,volume=0.28,afade=t=in:st=0:d=0.6,"
              f"afade=t=out:st={total-1.8:.2f}:d=1.8[m]")
    fc.append("[m][sc]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=400[md]")
    # fondo de sala continuo (muy bajo) para tapar los saltos de ambiente entre tomas
    fc.append(f"anoisesrc=color=brown:amplitude=0.012:r=48000:d={total:.2f},lowpass=f=500,highpass=f=60,"
              f"aformat=channel_layouts=stereo,afade=t=in:d=0.5,afade=t=out:st={total-1:.2f}:d=1[room]")
    mix = ["[dlg]", "[md]", "[room]"]
    extra = [(k, s, f, g, "fx") for k, s, f, g in LAUGHS] + [(k, s, f, g, "vo") for k, s, f, g in VO]
    for j, (k, s, f, g, kind) in enumerate(extra):
        p = A(f)
        if not os.path.exists(p): continue
        ins += ["-i", p]; idx = n_in; n_in += 1
        d = int(at(k, s) * 1000)
        fc.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,volume={g},"
                  f"afade=t=out:st=2.6:d=1.0,adelay={d}|{d}[x{j}]")
        mix.append(f"[x{j}]")
    fc.append("".join(mix) + f"amix=inputs={len(mix)}:duration=first:normalize=0,alimiter=limit=0.93[aout]")
    final = os.path.join(W, "recien-mudados-parte-04.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[vout]", "-map", "[aout]",
                    "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final], check=True)
    missing = [f for _, _, f, _ in LAUGHS + VO if not os.path.exists(A(f))]
    print("total", round(total, 2), final, "| faltan audios:", sorted(set(missing)) or "ninguno")

if __name__ == "__main__":
    build()
