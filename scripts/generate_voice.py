"""
Step 3: Generate clear baby-style voice using edge-tts native pitch (no distortion).
"""
import json, asyncio
import edge_tts

BOY_VOICE = "hi-IN-MadhurNeural"
GIRL_VOICE = "hi-IN-SwaraNeural"

async def tts(text, voice, out_path, pitch):
    communicate = edge_tts.Communicate(
        text, voice,
        rate="-20%",      # slightly slower = clearer
        pitch=pitch,       # native pitch shift, no artifacts
    )
    await communicate.save(out_path)

def generate_voice():
    with open("assets/content.json", encoding="utf-8") as f:
        content = json.load(f)

    asyncio.run(tts(content["boy_line"], BOY_VOICE, "assets/boy.mp3", pitch="+55Hz"))
    asyncio.run(tts(content["girl_line"], GIRL_VOICE, "assets/girl.mp3", pitch="+45Hz"))

    print("Voice files ready (clear, native pitch)")

if __name__ == "__main__":
    generate_voice()
