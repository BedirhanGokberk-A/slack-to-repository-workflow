from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
from pathlib import Path
import json
import time

from config import (
    TOKEN,
    CHANNEL_ID,
    START_DATE,
    END_DATE,
    PROJECT_NAME
)

PROJECT_DIR = Path(PROJECT_NAME)

OUTPUT_FILE = PROJECT_DIR / "slack" / "messages.json"

oldest = datetime.strptime(
    START_DATE,
    "%Y-%m-%d"
).timestamp()

latest = datetime.strptime(
    END_DATE,
    "%Y-%m-%d"
).timestamp()

client = WebClient(token=TOKEN)

all_messages = []
cursor = None

try:

    while True:

        response = client.conversations_history(
            channel=CHANNEL_ID,
            oldest=str(oldest),
            latest=str(latest),
            limit=200,
            cursor=cursor
        )

        messages = response.get(
            "messages",
            []
        )

        all_messages.extend(messages)

        print(
            f"{len(messages)} mesaj çekildi. Toplam: {len(all_messages)}"
        )

        cursor = response.get(
            "response_metadata",
            {}
        ).get(
            "next_cursor"
        )

        if not cursor:
            break

        time.sleep(1)

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
            all_messages,
            f,
            ensure_ascii=False,
            indent=4
        )

    print("\nTamamlandı.")
    print(
        f"Toplam mesaj sayısı: {len(all_messages)}"
    )

    print(
        f"Dosya oluşturuldu: {OUTPUT_FILE}"
    )

except SlackApiError as e:

    print(
        "Slack API Hatası:"
    )

    print(
        e.response.data
    )