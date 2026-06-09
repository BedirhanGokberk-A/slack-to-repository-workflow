import json
from datetime import datetime
from pathlib import Path

from config import PROJECT_NAME

PROJECT_DIR = Path(PROJECT_NAME)

INPUT_FILE = PROJECT_DIR / "slack" / "messages.json"
OUTPUT_FILE = PROJECT_DIR / "ai_context" / "file_index.md"

def get_category(filename, filetype):
    name = filename.lower()

    if name.endswith((".step", ".stp", ".iges", ".igs", ".f3d")):
        return "CAD / 3D Model"

    if name.endswith(".pdf"):
        if "drawing" in name or "çizim" in name:
            return "Technical Drawing"
        if "motor" in name or "datasheet" in name:
            return "Datasheet"
        return "PDF Document"

    if name.endswith((".jpg", ".jpeg", ".png")):
        return "Image / Visual Reference"

    if name.endswith((".zip", ".rar", ".7z")):
        return "Archive / Project Package"

    if name.endswith((".mp4", ".mov", ".avi")):
        return "Video / Demo"

    return f"Other ({filetype})"

def ts_to_date(ts):
    if not ts:
        return "Unknown"

    return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M:%S")

def main():
    if not INPUT_FILE.exists():
        print(f"Girdi dosyası bulunamadı: {INPUT_FILE}")
        return

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)

    files = []

    for msg in messages:
        message_ts = msg.get("ts")
        message_datetime = ts_to_date(message_ts)
        msg_text = msg.get("text", "")

        for file in msg.get("files", []):
            filename = file.get("name") or file.get("title") or "unknown"
            filetype = file.get("filetype", "unknown")

            file_created_ts = file.get("created")
            file_created_datetime = ts_to_date(file_created_ts)

            files.append({
                "name": filename,
                "filetype": filetype,
                "category": get_category(filename, filetype),

                "file_created_ts": file_created_ts,
                "file_created_datetime": file_created_datetime,

                "message_ts": message_ts,
                "message_datetime": message_datetime,

                "url": file.get("url_private") or file.get("url_private_download") or "",
                "message_text": msg_text.strip()
            })

    files.sort(key=lambda x: x["file_created_ts"] or 0)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# File Index - {PROJECT_NAME}\n\n")
        f.write(f"Total files: {len(files)}\n\n")

        current_category = None

        for item in files:
            if item["category"] != current_category:
                current_category = item["category"]
                f.write(f"\n## {current_category}\n\n")

            f.write(f"### {item['name']}\n")
            f.write(f"- Category: {item['category']}\n")
            f.write(f"- Type: {item['filetype']}\n")
            f.write(f"- File Created TS: {item['file_created_ts']}\n")
            f.write(f"- File Created Date: {item['file_created_datetime']}\n")
            f.write(f"- Message TS: {item['message_ts']}\n")
            f.write(f"- Message Date: {item['message_datetime']}\n")
            f.write(f"- Slack URL: {item['url']}\n")

            if item["message_text"]:
                clean_text = item["message_text"].replace("\n", " ")
                f.write(f"- Related Message: {clean_text[:300]}\n")

            f.write("\n")

    print(f"{OUTPUT_FILE} oluşturuldu.")
    print(f"Toplam dosya: {len(files)}")

if __name__ == "__main__":
    main()
