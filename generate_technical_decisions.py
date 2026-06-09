import json
from pathlib import Path

from config import PROJECT_NAME

PROJECT_DIR = Path(PROJECT_NAME)

INPUT_FILE = PROJECT_DIR / "slack" / "messages.json"
OUTPUT_FILE = PROJECT_DIR / "docs" / "technical_decisions.md"

DECISION_KEYWORDS = [
    "yerine",
    "kullanalım",
    "değerlendirebiliriz",
    "uygun",
    "karar",
    "seçelim",
    "tercih",
    "olmalı",
    "gerekiyor",
    "gerekir"
]

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    messages = json.load(f)

decisions = []

for msg in messages:

    text = msg.get("text", "").strip()

    if not text:
        continue

    text_lower = text.lower()

    if any(k in text_lower for k in DECISION_KEYWORDS):

        decisions.append({
            "ts": msg.get("ts"),
            "text": text
        })

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        f"# Technical Decisions - {PROJECT_NAME}\n\n"
    )

    f.write(
        f"Detected discussions potentially related to design and engineering decisions.\n\n"
    )

    for i, d in enumerate(decisions, start=1):

        f.write(
            f"## Decision Candidate {i}\n\n"
        )

        f.write(
            f"- Timestamp: {d['ts']}\n"
        )

        f.write(
            f"- Message: {d['text']}\n\n"
        )

print(
    f"{OUTPUT_FILE} oluşturuldu."
)

print(
    f"Tespit edilen karar adayı: {len(decisions)}"
)