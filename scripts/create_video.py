"""
Step 4: Combine image + voice + captions into final reel using ffmpeg.
Output: assets/final_video.mp4
"""
import json, subprocess

def get_audio_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True
    )
    return float(out.stdout.strip())

def create_video():
    with open("assets/content.json", encoding="utf-8") as f:
        content = json.load(f)

    boy_dur = get_audio_duration("assets/boy.mp3")
    girl_dur = get_audio_duration("assets/girl.mp3")
    total_dur = boy_dur + girl_dur + 1.0  # 1s gap

    # Concat audio with a small silence gap
    subprocess.run([
        "ffmpeg", "-y",
        "-i", "assets/boy.mp3", "-i", "assets/girl.mp3",
        "-filter_complex",
        "[0:a]apad=pad_dur=0.5[a0];[a0][1:a]concat=n=2:v=0:a=1[aout]",
        "-map", "[aout]", "assets/combined_audio.mp3"
    ], check=True, capture_output=True)

    boy_text = content["boy_line"].replace("'", "\u2019").replace(":", "\\:")
    girl_text = content["girl_line"].replace("'", "\u2019").replace(":", "\\:")

    # Ken Burns zoom + timed captions (drawtext) burned onto 1080x1920 vertical video
    filter_complex = (
        f"[0:v]scale=1200:2134,zoompan=z='min(zoom+0.0008,1.15)':d={int(total_dur*25)}:"
        f"s=1080x1920:fps=25[zoomed];"
        f"[zoomed]drawtext=text='{boy_text}':fontcolor=white:fontsize=64:"
        f"box=1:boxcolor=black@0.45:boxborderw=20:x=(w-text_w)/2:y=h*0.78:"
        f"enable='between(t,0,{boy_dur+0.3})',"
        f"drawtext=text='{girl_text}':fontcolor=white:fontsize=64:"
        f"box=1:boxcolor=black@0.45:boxborderw=20:x=(w-text_w)/2:y=h*0.78:"
        f"enable='gte(t,{boy_dur+0.5})'"
    )

    subprocess.run([
        "ffmpeg", "-y",
        "-loop", "1", "-i", "assets/scene.png",
        "-i", "assets/combined_audio.mp3",
        "-filter_complex", filter_complex,
        "-map", "1:a",
        "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p",
        "-t", str(total_dur),
        "assets/final_video.mp4"
    ], check=True, capture_output=True)

    print("Final video ready: assets/final_video.mp4")

if __name__ == "__main__":
    create_video()
