import uuid
from pathlib import Path
from typing import Protocol, runtime_checkable

from fastapi import UploadFile, HTTPException, status

from app.config import settings

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
EXTENSION_MAP = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}
MAX_FILE_SIZE = settings.MAX_FILE_SIZE_MB * 1024 * 1024


@runtime_checkable
class FileServiceProtocol(Protocol):
    async def save_file(self, store_id: int, file: UploadFile) -> str: ...
    async def delete_file(self, file_path: str) -> bool: ...


def validate_image(file: UploadFile) -> None:
    """이미지 파일 유효성 검증."""
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="허용되지 않는 파일 형식입니다 (JPEG, PNG, WebP만 가능)",
        )


class LocalFileService:
    """로컬 파일시스템 기반 파일 저장 서비스."""

    def __init__(self, upload_dir: str = settings.UPLOAD_DIR):
        self.upload_dir = upload_dir

    async def save_file(self, store_id: int, file: UploadFile) -> str:
        validate_image(file)

        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"파일 크기가 {settings.MAX_FILE_SIZE_MB}MB를 초과합니다",
            )

        ext = EXTENSION_MAP.get(file.content_type, ".jpg")
        filename = f"{uuid.uuid4()}{ext}"
        store_dir = Path(self.upload_dir) / str(store_id)
        store_dir.mkdir(parents=True, exist_ok=True)

        file_path = store_dir / filename
        with open(file_path, "wb") as f:
            f.write(content)

        return f"/{self.upload_dir}/{store_id}/{filename}"

    async def delete_file(self, file_path: str) -> bool:
        full_path = Path(file_path.lstrip("/"))
        if full_path.exists():
            full_path.unlink()
            return True
        return False
