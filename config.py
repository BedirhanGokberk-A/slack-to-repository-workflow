import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

PROJECT_NAME = config["project_name"]
CHANNEL_ID = config["channel_id"]
START_DATE = config["start_date"]
END_DATE = config["end_date"]
TOKEN = config["token"]