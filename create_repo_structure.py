from pathlib import Path
from config import PROJECT_NAME

folders = [
    f"{PROJECT_NAME}/slack",
    f"{PROJECT_NAME}/files/cad",
    f"{PROJECT_NAME}/files/drawings",
    f"{PROJECT_NAME}/files/images",
    f"{PROJECT_NAME}/files/archives",
    f"{PROJECT_NAME}/files/videos",
    f"{PROJECT_NAME}/docs",
    f"{PROJECT_NAME}/ai_context",
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

print(f"{PROJECT_NAME} repo yapısı oluşturuldu.")