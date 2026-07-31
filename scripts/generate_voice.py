"""
Step 3: Generate baby-style voice using edge-tts + light pitch shift + silence padding.
"""
import json, asyncio, subprocess
import edge_tts

BOY_VOICE = "hi-IN-MadhurNeural"
GIRL_VOICE = "hi-IN-SwaraNeural"

async def tts(text, voice, out_path):
    communicate = edge_tts.Communicate(text, voice)  # normal speed, no +5%
    await communicate.save(out_path)

def pitch_shift(in_path, out_path, semitones=2):
    factor = 2 ** (semitones / 12)
    subprocess.run([
        "ffmpeg", "-y", "-i", in_path,
        "-af", f"asetrate=44100*{factor},aresample=44100,atempo={1/factor:.4f},"
               f"apad=pad_dur=1.2",  # add 1.2s silence after each line
        out_path
    ], check=True, capture_output=True)

def generate_voice():
    with open("assets/content.json", encoding="utf-8") as f:
        content = json.load(f)

    asyncio.run(tts(content["boy_line"], BOY_VOICE, "assets/boy_raw.mp3"))
    asyncio.run(tts(content["girl_line"], GIRL_VOICE, "assets/girl_raw.mp3"))

    pitch_shift("assets/boy_raw.mp3", "assets/boy.mp3", semitones=2)
    pitch_shift("assets/girl_raw.mp3", "assets/girl.mp3", semitones=3)

    print("Voice files ready")

if __name__ == "__main__":
    generate_voice()
