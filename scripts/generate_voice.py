import json, asyncio
import edge_tts

BOY_VOICE = "hi-IN-MadhurNeural"
GIRL_VOICE = "hi-IN-SwaraNeural"

async def tts(text, voice, out_path, pitch, rate="-15%"):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(out_path)

def generate_voice():
    with open("assets/content.json", encoding="utf-8") as f:
        content = json.load(f)

    asyncio.run(tts(content["boy_line"], BOY_VOICE, "assets/boy.mp3", pitch="+25Hz",rate="+15%"))
    asyncio.run(tts(content["girl_line"], GIRL_VOICE, "assets/girl.mp3", pitch="+35Hz",rate="+20%"))
    asyncio.run(tts(content.get("laugh_text", "hihihi"), GIRL_VOICE, "assets/laugh.mp3",
                     pitch="+40Hz", rate="+30%"))

    print("Voice + laugh ready")

if __name__ == "__main__":
    generate_voice()
