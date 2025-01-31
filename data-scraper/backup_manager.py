import os
import shutil
from datetime import datetime
from pathlib import Path
from database import DATABASE_PATH, PROJECT_ROOT
import os

class BackupManager:
    def __init__(self):
        self.db_path = DATABASE_PATH 
        self.backup_dir = os.path.join(PROJECT_ROOT, 'backups')
        Path(self.backup_dir).mkdir(parents=True, exist_ok=True)

    def create_backup(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{timestamp}.db"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        shutil.copy2(self.db_path, backup_path)
        return backup_path

    def get_latest_backup(self) -> str:
        backups = self.get_all_backups()
        if not backups:
            return None
        return max(backups, key=os.path.getctime)

    def get_all_backups(self) -> list:
        if not os.path.exists(self.backup_dir):
            return []
            
        return [
            os.path.join(self.backup_dir, f)
            for f in os.listdir(self.backup_dir)
            if f.endswith('.db') and f.startswith('backup_')
        ]

    def restore_backup(self, backup_path: str) -> None:
        if not os.path.exists(backup_path):
            raise FileNotFoundError(f"Backup file {backup_path} not found")
            
        shutil.copy2(backup_path, self.db_path)

    def cleanup_old_backups(self, max_backups: int = 5) -> None:
        backups = self.get_all_backups()
        if len(backups) <= max_backups:
            return
            
        backups.sort(key=os.path.getctime)
        for backup in backups[:-max_backups]:
            os.remove(backup)
