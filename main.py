import argparse
import json
import os
from datetime import datetime, timezone
from config.settings import OUTPUT
from research.topics import choose_topic, save_history
from generator.script import make_script
from generator.voice import synthesize
from generator.render import render_video

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Render a video without uploading")
    args = parser.parse_args()

    category, item, history = choose_topic()
    metadata = make_script(category, item)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    audio_path = OUTPUT / f"voice_{stamp}.wav"
    video_path = OUTPUT / f"short_{stamp}.mp4"

    synthesize(metadata["script"], audio_path)
    duration = render_video(metadata["scenes"], category, audio_path, video_path)
    if duration < 25 or duration > 60:
        raise RuntimeError(f"Rendered narration duration {duration:.1f}s is outside the 25–60 second safety range")

    print(json.dumps({"category": category, "topic": item["topic"] if category == "gta6" else item["id"], "title": metadata["title"], "duration": round(duration, 1), "video": str(video_path)}, indent=2))

    if not args.dry_run:
        from youtube.upload import upload_video
        schedule_public = os.getenv("SCHEDULE_PUBLIC", "false").lower() == "true"
        result = upload_video(video_path, metadata, schedule_public=schedule_public)
        history.setdefault("published", []).append({
            "video_id": result["video_id"],
            "category": category,
            "topic_id": item["id"],
            "title": metadata["title"],
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": round(duration, 1),
            "privacy": "scheduled" if result["publish_at"] else "private",
            "publish_at": result["publish_at"]
        })
        history.setdefault("used_topics", []).append(item["id"])
        history["last_category"] = category
        save_history(history)
        print(f"Uploaded video: https://www.youtube.com/watch?v={result['video_id']}")
        if result["publish_at"]:
            print(f"Scheduled publication: {result['publish_at']}")
    else:
        print("Dry run complete. No YouTube upload was attempted.")

if __name__ == "__main__":
    main()
