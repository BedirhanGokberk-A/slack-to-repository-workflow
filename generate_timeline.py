import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

from config import PROJECT_NAME

PROJECT_DIR = Path(PROJECT_NAME)

INPUT_FILE = PROJECT_DIR / "slack" / "messages.json"
OUTPUT_FILE = PROJECT_DIR / "docs" / "timeline.md"

def ts_to_datetime(ts):
    return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")

def ts_to_date(ts):
    return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d")

def clean_text(text):
    text = text.replace("\n", " ").strip()
    return " ".join(text.split())

if not INPUT_FILE.exists():
    print(f"Girdi dosyası bulunamadı: {INPUT_FILE}")
    exit()

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    messages = json.load(f)

events_by_date = defaultdict(list)

for msg in messages:

    text = clean_text(msg.get("text", ""))

    if not text:
        continue

    if len(text) < 5:
        continue

    ts = msg.get("ts")

    date = ts_to_date(ts)
    readable_time = ts_to_datetime(ts)

    events_by_date[date].append({
        "time": readable_time,
        "timestamp": ts,
        "text": text[:400]
    })

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    f.write(f"# Project Timeline - {PROJECT_NAME}\n\n")
    f.write(
        "This timeline was generated from Slack channel messages.\n\n"
    )

    for date in sorted(events_by_date.keys()):

        f.write(f"## {date}\n\n")

        for event in events_by_date[date]:

            f.write(
                f"- **{event['time']}** "
                f"`ts:{event['timestamp']}` — "
                f"{event['text']}\n"
            )

        f.write("\n")

print(f"{OUTPUT_FILE} oluşturuldu.")
print(f"Toplam gün sayısı: {len(events_by_date)}")