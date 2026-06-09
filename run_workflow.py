import subprocess
import sys
from pathlib import Path

from config import PROJECT_NAME

PROJECT_DIR = Path(PROJECT_NAME)

STEPS = [
    ("Repo yapısı oluşturuluyor", "create_repo_structure.py"),
    ("Slack mesajları export ediliyor", "export_messages.py"),
    ("Threadler export ediliyor", "export_threads.py"),
    ("Dosyalar indiriliyor", "download_files.py"),
    ("Dosya indeksleri oluşturuluyor", "generate_file_index.py"),
    ("Timeline oluşturuluyor", "generate_timeline.py"),
    ("Project summary oluşturuluyor", "generate_project_summary.py"),
    ("Technical decisions oluşturuluyor", "generate_technical_decisions.py"),
    ("README oluşturuluyor", "generate_readme.py"),
]

def run_step(description, script_name):
    print("\n" + "=" * 60)
    print(f"START: {description}")
    print("=" * 60)

    if not Path(script_name).exists():
        print(f"HATA: {script_name} bulunamadı.")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    if result.returncode != 0:
        print(f"HATA: {script_name} başarısız oldu.")
        sys.exit(result.returncode)

    print(f"TAMAMLANDI: {description}")

def main():
    print("\nSLACK TO REPO WORKFLOW BAŞLATILDI")
    print(f"Proje klasörü: {PROJECT_DIR}")

    for description, script_name in STEPS:
        run_step(description, script_name)

    print("\n" + "=" * 60)
    print("WORKFLOW BAŞARIYLA TAMAMLANDI")
    print("=" * 60)
    print(f"Oluşturulan repo: {PROJECT_DIR}")

if __name__ == "__main__":
    main()