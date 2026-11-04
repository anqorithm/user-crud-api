"""
File Upload Endpoints
"""
import uuid
from pathlib import Path

import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.security import CurrentUser

router = APIRouter(prefix="/uploads", tags=["Files"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".docx", ".xlsx"}
MAX_FILE_SIZE = settings.max_upload_size_mb * 1024 * 1024
UPLOAD_DIR = Path("/tmp/uploads")


def upload_path(filename: str) -> Path:
    # Reject names like ".." that resolve outside the upload dir.
    path = (UPLOAD_DIR / filename).resolve()
    if path.parent != UPLOAD_DIR.resolve() or not path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return path


@router.post("")
async def upload_file(current_user: CurrentUser, file: UploadFile = File(...)):
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"File too large. Max: {settings.max_upload_size_mb}MB")

    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f"Allowed: {ALLOWED_EXTENSIONS}")

    file_id = str(uuid.uuid4())
    filename = f"{file_id}{ext}"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    async with aiofiles.open(UPLOAD_DIR / filename, "wb") as f:
        await f.write(content)

    return {"filename": filename, "original_filename": file.filename, "size": len(content), "url": f"/uploads/{filename}"}


@router.get("/{filename}")
async def get_file(filename: str):
    return FileResponse(path=upload_path(filename), filename=filename)


@router.delete("/{filename}")
async def delete_file(filename: str, current_user: CurrentUser):
    upload_path(filename).unlink()
    return {"message": "File deleted"}
