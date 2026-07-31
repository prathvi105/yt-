"""
Step 1: Generate cute 'kuchu puchu' style dialogue using Groq API (free).
Output: content.json with character description, dialogue lines, caption text.
"""
import os, json, requests

GROQ_API_KEY = os.environ["GROQ_API_KEY"]

PROMPT = """Generate content for a viral Instagram/YouTube reel in the "kuchu puchu" trend style —
a super cute AI-animated toddler boy and girl. Create a tiny STORY ARC: boy starts a little
upset/pouting (cute baby anger, not scary), girl says something sweet, and it ends in warm
giggly laughter. Dialogue must sound like real Hindi baby talk — soft, affectionate, playful
(e.g. words like "hmpf", "sunn na", "acha baba", "hehe").

Return STRICT JSON only, no markdown, no preamble, in this exact schema:
{
  "boy_line": "cute pouty/upset baby line in Hindi (max 10 words, soft not aggressive)",
  "girl_line": "sweet loving reply that melts his anger, Hindi baby talk (max 10 words)",
  "laugh_text": "hihihi hehehe",
  "caption": "a short catchy Instagram/YouTube caption with 3-4 relevant hashtags",
  "scene_prompt": "a detailed English prompt describing the cute toddler boy and girl characters for an AI image generator - style: pixar-like 3d cute chibi toddlers, big eyes, pastel colors, soft lighting, adorable expressions, boy slightly pouting on left, girl smiling warmly on right"
}
"""

def generate_content():
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": PROMPT}],
            "temperature": 0.9,
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = json.loads(resp.json()["choices"][0]["message"]["content"])

    with open("assets/content.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Content generated:", data)
    return data

if __name__ == "__main__":
    generate_content()
