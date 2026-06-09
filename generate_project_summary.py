import json
from pathlib import Path
from collections import Counter

from config import PROJECT_NAME

PROJECT_DIR = Path(PROJECT_NAME)

MESSAGES_FILE = PROJECT_DIR / "slack" / "messages.json"
THREADS_FILE = PROJECT_DIR / "slack" / "threads.json"
FILE_INDEX = PROJECT_DIR / "ai_context" / "file_index.md"
OUTPUT_FILE = PROJECT_DIR / "docs" / "project_summary.md"

KEYWORDS = [
    "stepmotor", "step motor", "encoder", "enkoder", "homing",
    "worm", "gearbox", "slipring", "rs232", "rs485", "imu",
    "gps", "gnss", "cad", "drawing", "motor", "assembly",
    "montaj", "test", "demo", "gimbal"
]


def load_json(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def clean_text(text):
    return " ".join(text.replace("\n", " ").split()).strip()


def extract_keyword_counts(messages):
    counter = Counter()

    for msg in messages:
        text = clean_text(msg.get("text", "")).lower()

        for keyword in KEYWORDS:
            if keyword in text:
                counter[keyword] += 1

    return counter


def count_files(messages):
    total = 0
    types = Counter()

    for msg in messages:
        for file in msg.get("files", []):
            total += 1
            filetype = file.get("filetype", "unknown")
            name = (file.get("name") or "").lower()

            if name.endswith((".step", ".stp", ".iges", ".igs", ".f3d")):
                types["CAD / 3D Model"] += 1
            elif name.endswith(".pdf"):
                if "drawing" in name:
                    types["Technical Drawing"] += 1
                else:
                    types["PDF Document"] += 1
            elif name.endswith((".jpg", ".jpeg", ".png")):
                types["Image / Visual Reference"] += 1
            elif name.endswith((".zip", ".rar", ".7z")):
                types["Archive / Project Package"] += 1
            elif name.endswith((".mp4", ".mov", ".avi")):
                types["Video / Demo"] += 1
            else:
                types["Other"] += 1

    return total, types


def main():
    messages = load_json(MESSAGES_FILE)
    threads = load_json(THREADS_FILE)

    keyword_counts = extract_keyword_counts(messages)
    total_files, file_types = count_files(messages)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Project Summary - {PROJECT_NAME}\n\n")

        f.write("## Overview\n\n")
        f.write(
            f"This repository was generated from the Slack project channel "
            f"`{PROJECT_NAME}`. It contains exported project messages, "
            "thread data, file metadata, timestamped file indexes, and generated "
            "documentation outputs for AI-assisted project knowledge management.\n\n"
        )

        f.write("## Extracted Data\n\n")
        f.write(f"- Total messages: {len(messages)}\n")
        f.write(f"- Total threads: {len(threads)}\n")
        f.write(f"- Total files: {total_files}\n")
        f.write(f"- File index: `{FILE_INDEX.as_posix()}`\n\n")

        f.write("## Detected Technical Topics\n\n")
        if keyword_counts:
            for keyword, count in keyword_counts.most_common():
                f.write(f"- {keyword}: {count}\n")
        else:
            f.write("- No predefined technical keywords detected.\n")

        f.write("\n## File Distribution\n\n")
        if file_types:
            for category, count in file_types.most_common():
                f.write(f"- {category}: {count}\n")
        else:
            f.write("- No files detected.\n")

        f.write("\n## Inferred Project Context\n\n")
        f.write(
            "Based on the extracted messages and file metadata, this project appears "
            "to include mechanical design, motor/encoder selection, homing sensor "
            "discussion, slipring signal routing, CAD/STEP files, technical drawings, "
            "assembly-related files, and demo/test materials.\n\n"
        )

        f.write("## Generated Artifacts\n\n")
        f.write(
            f"- `slack/messages_{PROJECT_NAME}.json`: Raw Slack message export\n")
        f.write(
            f"- `slack/threads_{PROJECT_NAME}.json`: Slack thread export\n")
        f.write(
            f"- `ai_context/file_index_{PROJECT_NAME}.md`: Timestamped file index\n")
        f.write(
            f"- `docs/timeline_{PROJECT_NAME}.md`: Timestamped project timeline\n")
        f.write(
            f"- `docs/project_summary_{PROJECT_NAME}.md`: Generated project summary\n\n")

        f.write("## Workflow Purpose\n\n")
        f.write(
            "The purpose of this workflow is to transform unstructured Slack project "
            "communication into a structured, version-controlled, and AI-readable "
            "knowledge repository that can be reused across future engineering projects.\n"
        )

    print(f"{OUTPUT_FILE} oluşturuldu.")


if __name__ == "__main__":
    main()
