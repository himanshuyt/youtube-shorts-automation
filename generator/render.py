import subprocess
from pathlib import Path
from PIL import Image
from config.settings import OUTPUT, FPS
from generator.visuals import render_scene

def render_video(scenes, category, audio_path, video_path):
    scene_dir = OUTPUT / "scenes"
    scene_dir.mkdir(parents=True, exist_ok=True)
    durations = []
    for i, scene in enumerate(scenes):
        path = scene_dir / f"scene_{i:02d}.png"
        render_scene(scene, i, len(scenes), path, category)
        durations.append(path)
    # Equal-duration visual cards, with voiceover mixed over the full sequence.
    audio_probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)],
        capture_output=True, text=True, check=True
    )
    audio_seconds = float(audio_probe.stdout.strip())
    per_scene = max(3.0, audio_seconds / len(durations))
    concat = scene_dir / "concat.txt"
    with concat.open("w", encoding="utf-8") as f:
        for path in durations:
            f.write(f"file '{path.as_posix()}'\n")
            f.write(f"duration {per_scene:.3f}\n")
        f.write(f"file '{durations[-1].as_posix()}'\n")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-i", str(audio_path), "-vf", f"fps={FPS},format=yuv420p",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
        str(video_path)
    ], check=True, capture_output=True, text=True)
    return audio_seconds
