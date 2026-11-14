from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
STORAGE = ROOT / "storage"
OUTPUT = ROOT / "output"
HISTORY_FILE = STORAGE / "history.json"
FACTS_FILE = DATA / "gta6_facts.json"
STORIES_FILE = DATA / "story_seeds.json"

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 30
VIDEO_SECONDS_MIN = 30
VIDEO_SECONDS_MAX = 58
TARGET_TIMEZONE = "Asia/Kolkata"
PUBLISH_PUBLIC = os.getenv("PUBLISH_PUBLIC", "false").lower() == "true"

for directory in (DATA, STORAGE, OUTPUT):
    directory.mkdir(parents=True, exist_ok=True)
