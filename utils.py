# app/utils.py
from pathlib import Path
import uuid
from flask import current_app

def allowed_file(filename):
    allowed = current_app.config.get("ALLOWED_EXTENSIONS", set())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def save_photo(file_storage_obj, gallery):
    UPLOAD_ROOT = Path(current_app.config.get("UPLOAD_FOLDER", "uploads"))

    user_folder = UPLOAD_ROOT / str(gallery.user_id)
    gallery_folder = user_folder / str(gallery.id)
    gallery_folder.mkdir(parents=True, exist_ok=True)

    ext = Path(file_storage_obj.filename).suffix.lower()
    filename = f"{uuid.uuid4().hex}{ext}"
    file_storage_obj.save(gallery_folder / filename)

    return filename
