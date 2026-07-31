"""
Step 4: Assemble video - zoom on boy while he talks, zoom on girl while she talks,
then zoom out to full duo shot. Adds motion + focus-based "who's talking" feel.
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
    hold_dur = 2.0
    total_dur = boy_dur + girl_dur + hold_dur

    subprocess.run([
        "ffmpeg", "-y",
        "-i", "assets/boy.mp3", "-i", "assets/girl.mp3",
        "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[aout]",
        "-map", "[aout]", "assets/combined_audio.mp3"
    ], check=True, capture_output=True)

    boy_text = content["boy_line"].replace("'", "\u2019").replace(":", "\\:")
    girl_text = content["girl_line"].replace("'", "\u2019").replace(":", "\\:")
    fps = 25
    total_frames = int(total_dur * fps)

    # zoompan: zoom into left half (boy) during boy_dur, right half (girl) during girl_dur,
    # then zoom out to full frame for the hold at the end
    filter_complex = (
        f"[0:v]scale=1600:2844,"
        f"zoompan=z='if(lte(on,{int(boy_dur*fps)}),1.4,"
        f"if(lte(on,{int((boy_dur+girl_dur)*fps)}),1.4,1.0))':"
        f"x='if(lte(on,{int(boy_dur*fps)}),0,"
        f"if(lte(on,{int((boy_dur+girl_dur)*fps)}),iw-iw/zoom,(iw-iw/zoom)/2))':"
        f"y='(ih-ih/zoom)/2':d=1:s=1080x1920:fps={fps}[zoomed];"
        f"[zoomed]drawtext=text='{boy_text}':fontcolor=white:fontsize=60:"
        f"box=1:boxcolor=black@0.5:boxborderw=18:x=(w-text_w)/2:y=h*0.8:"
        f"enable='between(t,0,{boy_dur+0.3})',"
        f"drawtext=text='{girl_text}':fontcolor=white:fontsize=60:"
        f"box=1:boxcolor=black@0.5:boxborderw=18:x=(w-text_w)/2:y=h*0.8:"
        f"enable='gte(t,{boy_dur+0.2})'"
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

    print("Final video ready:", total_dur, "seconds")

if __name__ == "__main__":
    create_video()
