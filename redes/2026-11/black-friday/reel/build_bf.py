"""Reel Black Friday (27-30 nov 2026), ~17 s. Versión sin voz: placas de marca + música del canal.
Cuando haya voz de Daniela (guion en ../guion-reel.md), ponerla en audio/daniela.mp3 y correr con VOZ=1."""
import os, subprocess
W = os.path.dirname(os.path.abspath(__file__))
C = os.environ.get("CARDS", "/home/claude/catalogostore/tools/piezas")
MUSIC = "/home/claude/catalogostore/redes/serie-recien-mudados/musica-tema.mp3"
P = lambda n: os.path.join(C, n + ".png")
# (placa, duración, zoom_desde, zoom_hasta)
SHOTS = [("bf_gancho", 2.6, 1.12, 1.00), ("bf_r1", 2.2, 1.00, 1.06), ("bf_r2", 2.2, 1.06, 1.00),
         ("bf_r3", 2.2, 1.00, 1.06), ("bf_r4", 2.2, 1.06, 1.00), ("bf_regalo", 2.6, 1.00, 1.07), ("bf_end", 3.2, 1.00, 1.04)]
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p"]

def build():
    d = os.path.join(W, "_tmp_segs"); os.makedirs(d, exist_ok=True); files = []; total = 0
    for i, (n, dur, z0, z1) in enumerate(SHOTS):
        f = int(round(dur * 30)); out = os.path.join(d, f"s{i}.mp4")
        zp = f"zoompan=z='{z0}+({z1}-{z0})*on/{f}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={f}:s=1080x1920:fps=30"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", P(n), "-frames:v", str(f),
                        "-vf", f"scale=2160:3840,{zp},format=yuv420p", *ENC, out], check=True)
        files.append(out); total += f / 30
    lst = os.path.join(d, "list.txt"); open(lst, "w").write("".join(f"file '{x}'\n" for x in files))
    joined = os.path.join(d, "joined.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined], check=True)
    final = os.path.join(W, "2026-11-25-black-friday.mp4")
    af = f"volume=1.33,afade=t=in:st=0:d=0.4,afade=t=out:st={total-1.4:.2f}:d=1.4,alimiter=limit=0.95"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-ss", "8", "-i", MUSIC, "-map", "0:v", "-map", "1:a",
                    "-af", af, "-t", f"{total:.2f}", *ENC, "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", final], check=True)
    print("total", round(total, 2), final)

if __name__ == "__main__":
    build()
