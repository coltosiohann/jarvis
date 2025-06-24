# memory_manager.py
import os
from datetime import datetime

MEMORY_DIR = "memories"
os.makedirs(MEMORY_DIR, exist_ok=True)

ACTIVE_PROJECT = "default"

def set_active_project(name: str):
    global ACTIVE_PROJECT
    ACTIVE_PROJECT = name.strip().replace(" ", "_") or "default"

def get_project_log_path():
    return os.path.join(MEMORY_DIR, f"{ACTIVE_PROJECT}.log")

def log_memory(entry: str):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(get_project_log_path(), "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {entry.strip()}\n")

def read_memory():
    try:
        with open(get_project_log_path(), "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
