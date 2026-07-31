"""
Step 4: Assemble video with breathing zoom motion + boy/girl focus pan + laugh ending.
"""
import json, subprocess

def get_dur(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())

def create_video():
    with open("assets/content.json", encoding="utf-8") as f:
        content = json.load(f)

    boy_dur = get_dur("assets/boy.mp3")
    girl_dur = get_dur("assets/girl.mp3")
    laugh_dur = get_dur("assets/laugh.mp3")
    total_dur = boy_dur + girl_dur + laugh_dur + 1.5

    subprocess.run([
        "ffmpeg", "-y",
        "-i", "assets/boy.mp3", "-i", "assets/girl.mp3", "-i", "assets/laugh.mp3",
        "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1[aout]",
        "-map", "[aout]", "assets/combined_audio.mp3"
    ], check=True)

    def escape(t):
        return (t.replace("\\", "\\\\").replace("'", "\u2019")
                 .replace(":", "\\:").replace(",", "\\,"))

    boy_text = escape(content["boy_line"])
    girl_text = escape(content["girl_line"])
    fps = 25
    t1 = boy_dur
    t2 = boy_dur + girl_dur

    n1 = int(t1 * fps)
    n2 = int(t2 * fps)

    filter_complex = (
        f"[0:v]scale=1600:2844,"
        f"zoompan=z='1.15+0.03*sin(2*PI*on/25)':"
        f"x='if(lte(on,{n1}),0,if(lte(on,{n2}),iw-iw/zoom,(iw-iw/zoom)/2))':"
        f"y='(ih-ih/zoom)/2':d=1:s=1080x1920:fps={fps}[zoomed];"
        f"[zoomed]drawtext=text='{boy_text}':fontcolor=white:fontsize=58:"
        f"box=1:boxcolor=black@0.5:boxborderw=18:x=(w-text_w)/2:y=h*0.8:"
        f"enable='between(t,0,{t1+0.3})',"
        f"drawtext=text='{girl_text}':fontcolor=white:fontsize=58:"
        f"box=1:boxcolor=black@0.5:boxborderw=18:x=(w-text_w)/2:y=h*0.8:"
        f"enable='between(t,{t1+0.2},{t2+0.3})'"
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

    print("Video ready:", total_dur, "sec")

if __name__ == "__main__":
    create_video()
