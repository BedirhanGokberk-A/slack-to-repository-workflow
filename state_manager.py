import json
from pathlib import Path


STATE_FILE = Path("state.json")


def load_last_timestamp():
    if not STATE_FILE.exists():
        return "0"

    with open(
        STATE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data.get(
        "last_fetch_timestamp",
        "0"
    )


def save_last_timestamp(timestamp):
    data = {
        "last_fetch_timestamp": timestamp
    }

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )