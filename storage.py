"""
storage.py

Handles all permanent storage of application data using JSON files, plus
timestamped backup/restore of the entire data directory. Kept separate
from Academy so that business logic never has to know the storage format
directly (single-responsibility principle).
"""

import json
import os
import shutil
from datetime import datetime

from exceptions import StorageError


class Storage:
    FILES = {
        "students": "students.json",
        "teachers": "teachers.json",
        "courses": "courses.json",
        "attendance": "attendance.json",
        "fees": "fees.json",
    }

    def __init__(self, data_dir="data", backup_dir="backup"):
        self.data_dir = data_dir
        self.backup_dir = backup_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def fileExists(self, key):
        return os.path.exists(os.path.join(self.data_dir, self.FILES[key]))

    def save(self, key, data_dict):
        if key not in self.FILES:
            raise StorageError(f"Unknown storage key '{key}'.")
        path = os.path.join(self.data_dir, self.FILES[key])
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data_dict, f, indent=4)
        except OSError as exc:
            raise StorageError(f"Failed to save '{key}': {exc}") from exc

    def load(self, key):
        if key not in self.FILES:
            raise StorageError(f"Unknown storage key '{key}'.")
        path = os.path.join(self.data_dir, self.FILES[key])
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (OSError, json.JSONDecodeError) as exc:
            raise StorageError(f"Failed to load '{key}': {exc}") from exc

    def backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target = os.path.join(self.backup_dir, f"backup_{timestamp}")
        try:
            os.makedirs(target, exist_ok=True)
            for filename in self.FILES.values():
                src = os.path.join(self.data_dir, filename)
                if os.path.exists(src):
                    shutil.copy2(src, os.path.join(target, filename))
        except OSError as exc:
            raise StorageError(f"Backup failed: {exc}") from exc
        return target

    def listBackups(self):
        if not os.path.exists(self.backup_dir):
            return []
        return sorted(
            d for d in os.listdir(self.backup_dir)
            if os.path.isdir(os.path.join(self.backup_dir, d))
        )

    def restore(self, backup_name=None):
        backups = self.listBackups()
        if not backups:
            raise StorageError("No backups are available to restore.")
        if backup_name is None:
            backup_name = backups[-1]  # most recent (names are timestamp-sortable)
        elif backup_name not in backups:
            raise StorageError(f"Backup '{backup_name}' was not found.")

        source = os.path.join(self.backup_dir, backup_name)

        # Validate the backup before touching any live data: every JSON
        # file present must actually parse, and there must be at least one
        # recognizable data file inside the folder.
        found_any = False
        for filename in self.FILES.values():
            src = os.path.join(source, filename)
            if os.path.exists(src):
                found_any = True
                try:
                    with open(src, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                        if content:
                            json.loads(content)
                except (OSError, json.JSONDecodeError) as exc:
                    raise StorageError(
                        f"Backup '{backup_name}' is invalid ({filename}): {exc}"
                    ) from exc
        if not found_any:
            raise StorageError(
                f"Backup '{backup_name}' does not contain any recognizable data files."
            )

        for filename in self.FILES.values():
            src = os.path.join(source, filename)
            if os.path.exists(src):
                shutil.copy2(src, os.path.join(self.data_dir, filename))
        return backup_name