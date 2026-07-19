import os
import uuid
from pydub import AudioSegment

# הגדרות קבועות
UPLOAD_DIR = os.path.join("data", "uploads")
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB בבייטים


def handle_upload(file):
    # 1. בדיקה שהקובץ הועבר ושמו לא ריק
    if not file or file.filename == '':
        return {"success": False, "error": "לא נבחר קובץ."}

    # 2. בדיקת גודל הקובץ
    # אנחנו מעבירים את ה"סמן" לסוף הקובץ כדי לקרוא את הגודל שלו
    file.seek(0, os.SEEK_END)
    file_size = file.tell()

    # חובה להחזיר את הסמן להתחלה כדי שנוכל לקרוא ולשמור את הקובץ בהמשך
    file.seek(0)

    if file_size == 0:
        return {"success": False, "error": "הקובץ ריק (0 בייטים)."}

    if file_size > MAX_FILE_SIZE:
        return {"success": False, "error": "הקובץ חורג מהגודל המקסימלי המותר (50MB)."}

    # 3. בדיקת תקינות הקובץ בפועל (Validation)
    # כאן אנחנו בודקים שזה באמת קובץ שמע, ולא קובץ טקסט ששינו לו את הסיומת
    try:
        audio = AudioSegment.from_file(file)
    except Exception as e:
        return {"success": False, "error": "פורמט הקובץ אינו נתמך או שהקובץ פגום."}

    # 4. שמירת הקובץ
    # וידאו שהתיקייה קיימת (אם לא - היא תיווצר)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # יצירת מזהה ייחודי למניעת דריסה של קבצים בעלי אותו שם
    file_id = str(uuid.uuid4())

    # לפי חוזה ה-API, חובה לשמור את הקובץ עם סיומת .wav, לא משנה מה הועלה
    safe_filename = f"{file_id}.wav"
    save_path = os.path.join(UPLOAD_DIR, safe_filename)

    # אנחנו מחזירים שוב את הסמן להתחלה, כי pydub קרא את הקובץ בבדיקה למעלה
    file.seek(0)
    file.save(save_path)

    # 5. החזרת הפלט בדיוק לפי חוזה ה-API[cite: 6]
    return {
        "success": True,
        "file_id": file_id,
        "original_filename": file.filename
    }