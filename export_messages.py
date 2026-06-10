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

from state_manager import load_last_timestamp, save_last_timestamp


PROJECT_DIR = Path(PROJECT_NAME)

OUTPUT_FILE = PROJECT_DIR / "slack" / "messages.json"

oldest_from_config = datetime.strptime(
    START_DATE,
    "%Y-%m-%d"
).timestamp()

latest = datetime.strptime(
    END_DATE,
    "%Y-%m-%d"
).timestamp()

last_saved_timestamp = float(load_last_timestamp())

oldest = max(
    oldest_from_config,
    last_saved_timestamp
)

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
            f"{len(messages)} yeni mesaj çekildi. Toplam: {len(all_messages)}"
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

    existing_messages = []

    if OUTPUT_FILE.exists():

        with open(
            OUTPUT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            existing_messages = json.load(f)

    combined_messages = existing_messages + all_messages

    unique_messages = {
        message["ts"]: message
        for message in combined_messages
    }

    final_messages = list(
        unique_messages.values()
    )

    final_messages.sort(
        key=lambda message: float(message["ts"]),
        reverse=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            final_messages,
            f,
            ensure_ascii=False,
            indent=4
        )

    if all_messages:

        latest_message_timestamp = max(
            float(message["ts"])
            for message in all_messages
        )

        save_last_timestamp(
            str(latest_message_timestamp)
        )

    print("\nTamamlandı.")
    print(
        f"Yeni çekilen mesaj sayısı: {len(all_messages)}"
    )
    print(
        f"Toplam kayıtlı mesaj sayısı: {len(final_messages)}"
    )
    print(
        f"Dosya güncellendi: {OUTPUT_FILE}"
    )

except SlackApiError as e:

    print(
        "Slack API Hatası:"
    )

    print(
        e.response.data
    )