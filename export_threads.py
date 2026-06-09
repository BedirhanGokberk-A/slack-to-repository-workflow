import json
import time
from pathlib import Path

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import (
    TOKEN,
    CHANNEL_ID,
    PROJECT_NAME
)

PROJECT_DIR = Path(PROJECT_NAME)

INPUT_FILE = PROJECT_DIR / "slack" / "messages.json"
OUTPUT_FILE = PROJECT_DIR / "slack" / "threads.json"

client = WebClient(token=TOKEN)

if not INPUT_FILE.exists():
    print(f"Mesaj dosyası bulunamadı: {INPUT_FILE}")
    exit()

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    messages = json.load(f)

all_threads = []

for msg in messages:

    if msg.get("reply_count", 0) > 0:

        thread_ts = msg["ts"]

        try:

            response = client.conversations_replies(
                channel=CHANNEL_ID,
                ts=thread_ts
            )

            all_threads.append({
                "thread_ts": thread_ts,
                "reply_count": msg.get("reply_count"),
                "messages": response["messages"]
            })

            print(
                f"Thread çekildi: {thread_ts}"
            )

            time.sleep(1)

        except SlackApiError as e:

            print(
                f"Thread alınamadı: {thread_ts}"
            )

            print(
                e.response.data
            )

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_threads,
        f,
        ensure_ascii=False,
        indent=4
    )

print(
    f"\nToplam Thread: {len(all_threads)}"
)

print(
    f"Dosya oluşturuldu: {OUTPUT_FILE}"
)