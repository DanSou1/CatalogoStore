"""Reel Black Friday (27-30 nov 2026), ~17-20 s: placas de marca + música del canal.
  python3 build_bf.py          -> versión sin voz (duraciones fijas de SHOTS)
  VOZ=1 python3 build_bf.py    -> con la voz de Daniela (guion en ../guion-reel.md) en audio/daniela.mp3:
                                  cada placa dura lo que su frase (corte en las 6 pausas más largas de la voz),
                                  música al ~30 % con sidechain bajo la voz.
Las placas se renderizan antes: cd tools/piezas && python3 render.py bf_gancho bf_r1 bf_r2 bf_r3 bf_r4 bf_regalo bf_end"""
import os, re, subprocess
W = os.path.dirname(os.path.abspath(__file__))
C = os.environ.get("CARDS", "/home/claude/catalogostore/tools/piezas")
MUSIC = "/home/claude/catalogostore/redes/serie-recien-mudados/musica-tema.mp3"
P = lambda n: os.path.join(C, n + ".png")
# (placa, duración, zoom_desde, zoom_hasta)
SHOTS = [("bf_gancho", 2.6, 1.12, 1.00), ("bf_r1", 2.2, 1.00, 1.06), ("bf_r2", 2.2, 1.06, 1.00),
         ("bf_r3", 2.2, 1.00, 1.06), ("bf_r4", 2.2, 1.06, 1.00), ("bf_regalo", 2.6, 1.00, 1.07), ("bf_end", 3.2, 1.00, 1.04)]
ENC = ["-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p"]

VOZ = os.path.join(W, "audio", "daniela.mp3")
LEAD = 0.15  # la voz entra 0,15 s después del primer fotograma

def dur_audio(f):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                         capture_output=True, text=True, check=True).stdout
    return float(out)

def tiempos_por_voz():
    """Duraciones de las 7 placas según las pausas de la voz (una frase por placa)."""
    log = subprocess.run(["ffmpeg", "-i", VOZ, "-af", "silencedetect=noise=-35dB:d=0.2", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    fin = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    total = dur_audio(VOZ)
    pausas = [(b - a, (a + b) / 2) for a, b in zip(ini, fin) if a > 0.3 and b < total - 0.3]
    n = len(SHOTS) - 1
    if len(pausas) < n:
        raise SystemExit(f"La voz tiene {len(pausas)} pausas y hacen falta {n}: graba una frase por placa.")
    cortes = sorted(m for _, m in sorted(pausas, reverse=True)[:n])
    bordes = [0] + [c + LEAD for c in cortes] + [total + LEAD + 1.3]  # 1,3 s de cierre después de la voz
    return [round(b - a, 2) for a, b in zip(bordes, bordes[1:])]

def build():
    con_voz = os.environ.get("VOZ") == "1"
    shots = SHOTS
    if con_voz:
        durs = tiempos_por_voz(); print("duraciones por voz", durs)
        shots = [(n, t, z0, z1) for (n, _, z0, z1), t in zip(SHOTS, durs)]
    d = os.path.join(W, "_tmp_segs"); os.makedirs(d, exist_ok=True); files = []; total = 0
    for i, (n, dur, z0, z1) in enumerate(shots):
        f = int(round(dur * 30)); out = os.path.join(d, f"s{i}.mp4")
        zp = f"zoompan=z='{z0}+({z1}-{z0})*on/{f}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={f}:s=1080x1920:fps=30"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", P(n), "-frames:v", str(f),
                        "-vf", f"scale=2160:3840,{zp},format=yuv420p", *ENC, out], check=True)
        files.append(out); total += f / 30
    lst = os.path.join(d, "list.txt"); open(lst, "w").write("".join(f"file '{x}'\n" for x in files))
    joined = os.path.join(d, "joined.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined], check=True)
    final = os.path.join(W, "2026-11-25-black-friday.mp4")
    if not con_voz:
        af = f"volume=1.33,afade=t=in:st=0:d=0.4,afade=t=out:st={total-1.4:.2f}:d=1.4,alimiter=limit=0.95"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-ss", "8", "-i", MUSIC, "-map", "0:v", "-map", "1:a",
                        "-af", af, "-t", f"{total:.2f}", *ENC, "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                        "-movflags", "+faststart", final], check=True)
    else:
        ms = int(LEAD * 1000)
        fc = (f"[2:a]aresample=48000,atempo=1.0,adelay={ms}|{ms},apad,asplit=2[v1][v2];"
              f"[1:a]aresample=48000,volume=0.30,afade=t=in:st=0:d=0.4,afade=t=out:st={total-1.4:.2f}:d=1.4[m];"
              f"[m][v2]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300[md];"
              f"[md][v1]amix=inputs=2:duration=first:normalize=0,volume=VOL,alimiter=limit=0.95[a]")
        def mezcla(vol, out):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", joined, "-ss", "8", "-i", MUSIC, "-i", VOZ,
                            "-filter_complex", fc.replace("VOL", f"{vol:.2f}dB"), "-map", "0:v", "-map", "[a]",
                            "-t", f"{total:.2f}", *ENC, "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                            "-movflags", "+faststart", out], check=True)
        mezcla(0, final)
        log = subprocess.run(["ffmpeg", "-i", final, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])
        if abs(lufs + 14) > 1:  # objetivo -14 LUFS
            mezcla(-14 - lufs, final); print("ajuste de volumen", round(-14 - lufs, 1), "dB")
    print("total", round(total, 2), final)

if __name__ == "__main__":
    build()
