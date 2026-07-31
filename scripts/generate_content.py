"""
Step 1: Generate cute 'kuchu puchu' style dialogue using Groq API (free).
Output: content.json with character description, dialogue lines, caption text.
"""
import os, json, requests

GROQ_API_KEY = os.environ["GROQ_API_KEY"]

PROMPT = """Generate content for a viral Instagram/YouTube reel in the "kuchu puchu" trend style —
a super cute AI-animated toddler boy and girl couple saying sweet, over-the-top affectionate
lines to each other in baby voice style (Hindi-English mix, Gen-Z cute tone).

Return STRICT JSON only, no markdown, no preamble, in this exact schema:
{
  "boy_line": "one short cute baby-style line the boy says (max 12 words)",
  "girl_line": "one short cute baby-style reply the girl says (max 12 words)",
  "caption": "a short catchy Instagram/YouTube caption with 3-4 relevant hashtags",
  "scene_prompt": "a detailed English prompt describing the cute toddler boy and girl characters for an AI image generator - style: pixar-like 3d cute chibi toddlers, big eyes, pastel colors, soft lighting, adorable expressions"
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
