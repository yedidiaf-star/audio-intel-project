# חוזה API קבוע

מסמך זה הוא "האמת" שכל המשימות בנויות עליה. אם קלט/פלט של המשימה שלך שונה ממה שכתוב כאן — תתאם/י עם הצוות/תלמיד שתלוי בך *לפני* שמשנים.

## שלב 1: התחברות
`POST /login`
קלט: `{"username": "...", "password": "..."}`
פלט: `{"success": true, "token": "..."}` או `{"success": false, "error": "..."}`
סיסמאות נשמרות בקובץ הסוכנים כ-**hash** (למשל bcrypt), לעולם לא כטקסט גלוי או הצפנה הפיכה.

## שלב 2: העלאה + ניקוי
`POST /clean` — multipart/form-data, שדה `audio_file`
פלט:
```json
{
  "duration_sec": 42.3,
  "sample_rate": 16000,
  "silence_trimmed_sec": 8.1,
  "file_url": "/files/cleaned_001.wav"
}
```
קובץ הפלט הוא תמיד **WAV, 16kHz, mono**.

## שלב 3: זיהוי דובר
`POST /identify` — קלט: `{"file_url": "..."}`
פלט:
```json
{
  "segments": [
    {"start": 0.0, "end": 12.4, "speaker": "speaker_A", "confidence": 0.87},
    {"start": 12.4, "end": 30.1, "speaker": "unknown", "confidence": 0.31}
  ]
}
```
- `speaker`: שם מזוהה מתוך מאגר הקולות הרשומים, או `"unknown"` אם אין התאמה מספיק טובה.
- `confidence`: מספר בין 0 ל-1.

## שלב 4: דוח
`POST /report` — קלט: JSON של שלב 3 (ואופציונלי metadata של שלב 2)
פלט: דוח (HTML/PDF) + JSON סיכום.

## פורמט תמלול (אם נעשה - משימת בונוס)
```json
{
  "segments": [
    {"start": 0.0, "end": 12.4, "speaker": "speaker_A", "text": "..."}
  ]
}
```
שדה `text` מתווסף לאותו מבנה סגמנטים — לא מבנה חדש.
