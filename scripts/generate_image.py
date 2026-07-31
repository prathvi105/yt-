"""
Step 2: Generate the cute toddler couple image using Pollinations.ai (free, no API key).
Output: assets/scene.png
"""
import json, requests, urllib.parse

def generate_image():
    with open("assets/content.json", encoding="utf-8") as f:
        content = json.load(f)

    prompt = content["scene_prompt"]
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1920&nologo=true&model=flux"

    r = requests.get(url, timeout=120)
    r.raise_for_status()

    with open("assets/scene.png", "wb") as f:
        f.write(r.content)

    print("Image saved: assets/scene.png")

if __name__ == "__main__":
    generate_image()
