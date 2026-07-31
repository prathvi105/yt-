"""
Step 3: Generate baby-style voice lines using edge-tts (free), then pitch-shift with ffmpeg
to sound cuter/higher (kuchu-puchu style).
Output: assets/boy.mp3, assets/girl.mp3
"""
import json, asyncio, subprocess
import edge_tts

BOY_VOICE = "hi-IN-MadhurNeural"
GIRL_VOICE = "hi-IN-SwaraNeural"

async def tts(text, voice, out_path):
    communicate = edge_tts.Communicate(text, voice, rate="+5%")
    await communicate.save(out_path)

def pitch_shift(in_path, out_path, semitones=4):
    factor = 2 ** (semitones / 12)
    subprocess.run([
        "ffmpeg", "-y", "-i", in_path,
        "-af", f"asetrate=44100*{factor},aresample=44100,atempo={1/factor:.4f}",
        out_path
    ], check=True, capture_output=True)

def generate_voice():
    with open("assets/content.json", encoding="utf-8") as f:
        content = json.load(f)

    asyncio.run(tts(content["boy_line"], BOY_VOICE, "assets/boy_raw.mp3"))
    asyncio.run(tts(content["girl_line"], GIRL_VOICE, "assets/girl_raw.mp3"))

    pitch_shift("assets/boy_raw.mp3", "assets/boy.mp3", semitones=3)
    pitch_shift("assets/girl_raw.mp3", "assets/girl.mp3", semitones=5)

    print("Voice files ready: assets/boy.mp3, assets/girl.mp3")

if __name__ == "__main__":
    generate_voice()
