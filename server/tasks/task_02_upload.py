import os
import uuid
from pydub import AudioSegment

UPLOAD_DIR = os.path.join("data", "uploads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def handle_upload(file):
    if not file or file.filename == '':
        return {"success": False, "error": "לא נבחר קובץ."}

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    if file_size == 0:
        return {"success": False, "error": "הקובץ ריק (0 בייטים)."}
    if file_size > MAX_FILE_SIZE:
        return {"success": False, "error": "הקובץ חורג מהגודל המקסימלי המותר (50MB)."}

    try:
        AudioSegment.from_file(file)
    except Exception:
        return {"success": False, "error": "פורמט הקובץ אינו נתמך או שהקובץ פגום."}

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    safe_filename = f"{file_id}.wav"
    save_path = os.path.join(UPLOAD_DIR, safe_filename)
    file.seek(0)
    file.save(save_path)

    return {
        "success": True,
        "file_id": file_id,
        "original_filename": file.filename
    }