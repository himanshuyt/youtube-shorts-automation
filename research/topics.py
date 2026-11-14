import json
from config.settings import FACTS_FILE, STORIES_FILE, HISTORY_FILE

def load_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    return {"published": [], "used_topics": [], "last_category": None}

def save_history(history):
    HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")

def choose_topic():
    history = load_history()
    # Alternate categories so the combined channel has a predictable mix.
    category = "story" if history.get("last_category") == "gta6" else "gta6"
    source = STORIES_FILE if category == "story" else FACTS_FILE
    items = json.loads(source.read_text(encoding="utf-8"))
    used = set(history.get("used_topics", []))
    candidates = [item for item in items if item["id"] not in used]
    if not candidates:
        # Once every seed has been used, allow rotation again; retain recent history.
        candidates = items
    index = len(history.get("published", [])) % len(candidates)
    item = candidates[index]
    return category, item, history
