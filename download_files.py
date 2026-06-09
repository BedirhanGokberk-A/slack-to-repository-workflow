import json
import re
import requests
from pathlib import Path

from config import PROJECT_NAME, TOKEN

PROJECT_DIR = Path(PROJECT_NAME)

INPUT_FILE = PROJECT_DIR / "slack" / "messages.json"
FILES_DIR = PROJECT_DIR / "files"

def safe_filename(name):
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    return name.strip()

def get_category_folder(filename):
    name = filename.lower()

    if name.endswith((".step", ".stp", ".iges", ".igs", ".f3d")):
        return FILES_DIR / "cad"

    if name.endswith(".pdf"):
        if "drawing" in name or "çizim" in name:
            return FILES_DIR / "drawings"
        return FILES_DIR / "documents"

    if name.endswith((".jpg", ".jpeg", ".png")):
        return FILES_DIR / "images"

    if name.endswith((".zip", ".rar", ".7z")):
        return FILES_DIR / "archives"

    if name.endswith((".mp4", ".mov", ".avi")):
        return FILES_DIR / "videos"

    return FILES_DIR / "other"

def main():
    if not INPUT_FILE.exists():
        print(f"Mesaj dosyası bulunamadı: {INPUT_FILE}")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)

    downloaded = 0
    skipped = 0
    failed = 0

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    for msg in messages:
        for file in msg.get("files", []):
            filename = file.get("name") or file.get("title") or "unknown_file"
            filename = safe_filename(filename)

            url = file.get("url_private_download") or file.get("url_private")

            if not url:
                skipped += 1
                continue

            target_dir = get_category_folder(filename)
            target_dir.mkdir(parents=True, exist_ok=True)

            target_path = target_dir / filename

            if target_path.exists():
                print(f"Atlandı, zaten var: {target_path}")
                skipped += 1
                continue

            try:
                response = requests.get(
                    url,
                    headers=headers,
                    timeout=60
                )

                if response.status_code == 200:
                    with open(target_path, "wb") as out:
                        out.write(response.content)

                    print(f"İndirildi: {target_path}")
                    downloaded += 1
                else:
                    print(f"İndirilemedi: {filename} | Status: {response.status_code}")
                    failed += 1

            except Exception as e:
                print(f"Hata: {filename}")
                print(e)
                failed += 1

    print("\nİndirme tamamlandı.")
    print(f"İndirilen: {downloaded}")
    print(f"Atlanan: {skipped}")
    print(f"Başarısız: {failed}")

if __name__ == "__main__":
    main()