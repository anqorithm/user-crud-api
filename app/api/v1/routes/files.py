"""
File Upload Endpoints
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
import aiofiles
import uuid
from pathlib import Path

from app.core.config import settings
from app.core.security import CurrentUser

router = APIRouter(prefix="/uploads", tags=["Files"])

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".pdf", ".docx", ".xlsx"}
MAX_FILE_SIZE = settings.max_upload_size_mb * 1024 * 1024


@router.post("")
async def upload_file(file: UploadFile = File(...), current_user: CurrentUser = None):
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=f"File too large. Max: {settings.max_upload_size_mb}MB")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f"Allowed: {ALLOWED_EXTENSIONS}")

    file_id = str(uuid.uuid4())
    filename = f"{file_id}{ext}"
    upload_dir = Path("/tmp/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    async with aiofiles.open(upload_dir / filename, "wb") as f:
        await f.write(content)

    return {"filename": filename, "original_filename": file.filename, "size": len(content), "url": f"/uploads/{filename}"}


@router.get("/{filename}")
async def get_file(filename: str):
    file_path = Path("/tmp/uploads") / filename
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return FileResponse(path=file_path, filename=filename)


@router.delete("/{filename}")
async def delete_file(filename: str, current_user: CurrentUser = None):
    file_path = Path("/tmp/uploads") / filename
    if file_path.exists():
        file_path.unlink()
        return {"message": "File deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")