"""Comercial "¡Sí señor!" — 7 tomas de Flow (con su audio) + cierre, subtítulos quemados."""
import os, subprocess
W = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(os.path.dirname(W), "vid", "cards")
FONTS = os.path.join(C, "fonts")
PINK = r"{\c&HB34FFF&}"
# (clip, inicio, fin)
SEGS = [("t1", 0.5, 7.0), ("t2", 1.0, 8.0), ("t3", 1.0, 8.0), ("t4", 1.5, 7.5),
        ("t5", 3.0, 8.0), ("t6", 1.0, 7.6), ("t7", 2.5, 8.0)]
END = (os.path.join(C, "end_sisenor.png"), 2.6)
SUBS = [
    (3.0, 4.4, "“¿Lunes otra vez?”"),
    (5.0, 6.4, PINK + "Sí señor…"),
    (9.0, 11.1, "“¿Sin energía\\Nni para el tinto?”"),
    (11.5, 13.4, PINK + "Sí señor…"),
    (18.0, 20.5, "“Entonces usted necesita…\\N" + PINK + "¡energía de verdad!”"),
    (27.7, 31.4, "“Energía de verdad,\\Npara el que sí se le mide.”"),
    (31.7, 33.6, "“Carlos, ¿listo\\Npara la reunión?”"),
    (35.1, 36.6, PINK + "¡Sí señor!"),
    (40.3, 43.2, "“¿Listo para todo?\\N" + PINK + "¡Sí señor!”"),
]
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
POP = r"{\fad(60,80)\fscx86\fscy86\t(0,140,\fscx100\fscy100)}"
ENC = ["-r", "30", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]

def run(cmd, out):
    tmp = out[:-4] + ".part.mp4"
    subprocess.run(cmd + [tmp], check=True); os.replace(tmp, out)

def main():
    seg_dir = os.path.join(W, "segs"); os.makedirs(seg_dir, exist_ok=True)
    files, t = [], 0.0
    for i, (clip, a, b) in enumerate(SEGS):
        out = os.path.join(seg_dir, f"s{i}.mp4"); d = b - a
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(a), "-t", f"{d:.3f}", "-i", os.path.join(W, "clips", clip + ".mp4"),
             "-vf", "scale=1080:1920:flags=lanczos,setsar=1,fps=30",
             "-af", f"loudnorm=I=-15:TP=-1.5:LRA=11,afade=t=in:d=0.04,afade=t=out:st={d-0.06:.3f}:d=0.06",
             *ENC], out)
        files.append(out); t += d
    png, d = END
    out = os.path.join(seg_dir, "end.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", png, "-f", "lavfi", "-t", f"{d}", "-i", "anullsrc=r=48000:cl=stereo",
         "-vf", f"format=yuv420p,loop=-1:1,trim=duration={d},fade=t=in:d=0.4", "-t", f"{d}", *ENC], out)
    files.append(out); total = t + d
    lst = os.path.join(seg_dir, "list.txt"); open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    joined = os.path.join(seg_dir, "joined.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy"], joined)
    L = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
         "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
         "Style: Sub,Archivo,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,5,3,2,70,70,470,1",
         "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    L += [f"Dialogue: 0,{ts(a)},{ts(b)},Sub,,0,0,0,,{POP}{x}" for a, b, x in SUBS]
    ass = os.path.join(W, "subs.ass"); open(ass, "w").write("\n".join(L) + "\n")
    final = os.path.join(W, "si-senor-comercial.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-vf", f"ass={ass}:fontsdir={FONTS}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart"], final)
    print("total", round(total, 2), final)

main()
