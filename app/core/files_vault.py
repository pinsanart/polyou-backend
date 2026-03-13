from pathlib import Path
from uuid import UUID
import shutil

class FilesVault:
    def __init__(self, base_path: Path):
        self.base_path = base_path
    
    def _get_unique_path(self, file_path: Path) -> Path:
        counter = 1
        new_path = file_path

        while new_path.exists():
            new_path = file_path.with_stem(f"{file_path.stem}_{counter}")
            counter += 1

        return new_path

    def get_user_dir(self, user_public_id: UUID) -> Path:
        user_public_id_str = str(user_public_id)
        return self.base_path / user_public_id_str[:2] / user_public_id_str

    def save(self, user_public_id: UUID, filename: str, file_stream) -> str:
        user_dir = self.get_user_dir(user_public_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        file_path = user_dir / filename
        file_path = self._get_unique_path(file_path)

        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file_stream, buffer)

        new_filename = file_path.name
        
        return new_filename
    
    def delete(self, user_public_id: UUID, filename:str) -> bool:
        user_dir = self.get_user_dir(user_public_id)
        file_path = user_dir / filename

        if file_path.exists():
            file_path.unlink()

            if not any(user_dir.iterdir()):
                user_dir.rmdir()

            return True
        
        return False