# run_app.py — LAUNCHER (recomendado)
import os, sys, subprocess, shutil
from pathlib import Path

def resource_path(relative: str) -> str:
    base = getattr(sys, "_MEIPASS", None)  # quando "frozen"
    if base:
        return str(Path(base) / relative)
    return str(Path(__file__).resolve().parent / relative)

def main():
    app_py = resource_path("app.py")

    # Pasta de dados gravável (DB e uploads) fora do exe
    app_home = Path.home() / ".concurso_planner"
    (app_home / "uploads").mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("DB_PATH", str(app_home / "studyplanner.db"))
    os.environ.setdefault("UPLOADS_DIR", str(app_home / "uploads"))

    # Evita alto consumo de CPU/loop do watcher
    os.environ.setdefault("STREAMLIT_SERVER_HEADLESS", "true")
    os.environ.setdefault("STREAMLIT_SERVER_ADDRESS", "127.0.0.1")
    os.environ.setdefault("STREAMLIT_SERVER_PORT", "8501")
    os.environ.setdefault("STREAMLIT_SERVER_FILE_WATCHER_TYPE", "none")
    os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")

    if getattr(sys, "frozen", False):
        # Preferir o launcher do Windows; fallback para python
        py = shutil.which("py") or shutil.which("python") or "python"
        cmd = [py, "-m", "streamlit", "run", app_py,
               "--server.headless=true", "--server.port=8501", "--server.fileWatcherType=none"]
    else:
        cmd = [sys.executable, "-m", "streamlit", "run", app_py,
               "--server.headless=true", "--server.port=8501", "--server.fileWatcherType=none"]

    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()