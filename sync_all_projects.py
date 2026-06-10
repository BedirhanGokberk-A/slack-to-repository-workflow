import subprocess
from datetime import datetime
from pathlib import Path


PROJECTS = [
    {
        "name": "3eeos-gimbal-arcturus",
        "command": "python run_workflow.py"
    }
]


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / "sync_all_projects.log"


def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")

    print(message)


def run_project_sync(project):
    write_log(f"START: {project['name']}")

    try:
        result = subprocess.run(
            project["command"],
            shell=True,
            text=True,
            capture_output=True
        )

        if result.returncode == 0:
            write_log(f"SUCCESS: {project['name']}")
        else:
            write_log(f"FAILED: {project['name']}")
            write_log(result.stderr)

    except Exception as error:
        write_log(f"ERROR: {project['name']} - {error}")


def main():
    write_log("GLOBAL SYNC STARTED")

    for project in PROJECTS:
        run_project_sync(project)

    write_log("GLOBAL SYNC FINISHED")


if __name__ == "__main__":
    main()