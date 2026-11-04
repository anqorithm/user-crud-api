import pytest
from fastapi import HTTPException

from app.api.v1.routes import files


def test_upload_path_returns_file_inside_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(files, "UPLOAD_DIR", tmp_path)
    (tmp_path / "a.png").write_bytes(b"x")
    assert files.upload_path("a.png") == (tmp_path / "a.png").resolve()


@pytest.mark.parametrize("name", ["..", ".", "missing.png", "../secret.txt"])
def test_upload_path_rejects_outside_or_missing(tmp_path, monkeypatch, name):
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    (tmp_path / "secret.txt").write_text("s")
    monkeypatch.setattr(files, "UPLOAD_DIR", upload_dir)
    with pytest.raises(HTTPException) as exc:
        files.upload_path(name)
    assert exc.value.status_code == 404
