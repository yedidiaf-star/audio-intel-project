# חוזה API קבוע ("קובץ האמת")

מסמך זה הוא "האמת" שכל 12 המשימות בנויות עליה. הוא מגדיר, לכל שלב: **מה** ה-endpoint מקבל ומחזיר, **באיזה קובץ** כותבים את הקוד, ו**באילו כלים** משתמשים. אם קלט/פלט של המשימה שלך שונה ממה שכתוב כאן — תתאם/י עם מי שתלוי בך *לפני* שמשנים.

## מבנה קבצים בשרת

כל משימה כותבת את הלוגיקה שלה בקובץ נפרד תחת `server/tasks/`, ו-`server/app.py` רק "מחבר" בין הנתיב (route) לפונקציה שכתבתם. **אל תכתבו את כל הלוגיקה ישירות בתוך `app.py`** - זה גורם לכל התלמידים לערוך את אותו קובץ במקביל ויוצר קונפליקטים מיותרים ב-Git.

```
server/
├── app.py                          # רק routes - קורא לפונקציות מ-tasks/
├── templates/
│   ├── upload.html                 # משימה 02
│   └── report.html                 # משימה 07
└── tasks/
    ├── task_01_login.py
    ├── task_02_upload.py
    ├── task_03_cleaning.py
    ├── task_04_enrollment.py
    ├── task_05_identification.py
    ├── task_06_segmentation.py
    ├── task_07_report.py
    ├── task_08_noise_reduction.py   # בונוס
    ├── task_09_transcription.py     # בונוס
    ├── task_10_timeline.py          # בונוס
    ├── task_11_llm_summary.py       # בונוס
    └── task_12_confidence_flag.py   # בונוס
```

כל קובץ `task_XX_*.py` מכיל **פונקציה אחת מרכזית** ש-`app.py` קורא לה. שם הפונקציה מוגדר בטבלה של כל שלב למטה - אל תשנו את השם בלי לתאם, כי מי שתלוי בכם קורא לפונקציה בשם הזה.

---

## שלב 1: התחברות (משימה 01)
**קובץ:** `server/tasks/task_01_login.py` · **פונקציה:** `login_agent(username, password)`
**כלים:** `bcrypt` (hash), קובץ JSON למאגר הסוכנים (`data/agents.json`)

`POST /login`
קלט: `{"username": "...", "password": "..."}`
פלט: `{"success": true, "token": "..."}` או `{"success": false, "error": "..."}`
סיסמאות נשמרות בקובץ הסוכנים כ-**hash** (bcrypt), לעולם לא כטקסט גלוי או הצפנה הפיכה.

**מה `app.py` עושה:** קורא ל-`login_agent()` עם השדות מ-`request.json`, ומחזיר את מה שהיא מחזירה כ-`jsonify`.

---

## שלב 2: העלאת קובץ (משימה 02)
**קובץ:** `server/tasks/task_02_upload.py` · **פונקציה:** `handle_upload(file)`
**כלים:** `pydub` (בדיקת תקינות קובץ), `uuid` (ליצירת `file_id`)
**+ קובץ נוסף:** `server/templates/upload.html` (טופס ההעלאה - HTML+JS)

`GET /upload` — מציג את `upload.html`
`POST /upload` — multipart/form-data, שדה `audio_file`
פלט הצלחה: `{"success": true, "file_id": "...", "original_filename": "..."}`
פלט כישלון: `{"success": false, "error": "..."}`

**מה `app.py` עושה:** ב-GET, קורא ל-`render_template("upload.html")`. ב-POST, קורא ל-`handle_upload(request.files.get("audio_file"))`.
**איפה הקובץ עצמו נשמר בפועל:** `data/uploads/<file_id>.wav` — תיקייה זו לא נכנסת ל-Git (ראו `.gitignore`).

---

## שלב 3: ניקוי (משימה 03, + משימה 08 בונוס)
**קובץ:** `server/tasks/task_03_cleaning.py` · **פונקציה:** `clean_audio(file_id)`
**כלים:** `pydub`, `numpy` · **בונוס (08):** `noisereduce` — נקרא **מתוך** אותה פונקציה, לא endpoint נפרד

`POST /clean` — קלט: `{"file_id": "..."}`
פלט:
```json
{
  "duration_sec": 42.3,
  "sample_rate": 16000,
  "silence_trimmed_sec": 8.1,
  "file_url": "/files/cleaned_001.wav"
}
```
קובץ הפלט הוא תמיד **WAV, 16kHz, mono**, נשמר תחת `data/uploads/cleaned/`.

**מה `app.py` עושה:** קורא ל-`clean_audio(file_id)` עם ה-`file_id` שהתקבל ממשימה 02.
**חשוב:** מי שעושה משימה 08 (בונוס) **עורך את אותו קובץ** (`task_03_cleaning.py`) ומוסיף את שלב הפחתת הרעש בתוך `clean_audio()` — לא יוצר endpoint נפרד. יש לתאם ישירות עם מי שכתב את הגרסה הבסיסית לפני עריכה.

---

## שלב 4: רישום קולות (משימה 04)
**קובץ:** `server/tasks/task_04_enrollment.py` · **פונקציה:** `enroll_speaker(speaker_name, file_path)`
**כלים:** `librosa` או `resemblyzer` (חילוץ features), מאגר נשמר ב-`data/speaker_profiles.json` או `.pkl`

`POST /enroll` — קלט: `{"speaker_name": "...", "audio_file": <קובץ WAV נקי>}`
פלט: `{"success": true, "speaker_name": "...", "samples_count": N}`

**מה `app.py` עושה:** קורא ל-`enroll_speaker()` עם השם והקובץ שהתקבלו.
**תלות ישירה:** משימה 05 קוראת לפונקציית עזר מקובץ זה (למשל `load_speaker_profiles()`) — לתאם שם הפונקציה מראש עם מי שעושה משימה 05.

---

## שלב 5: זיהוי דובר בודד (משימה 05)
**קובץ:** `server/tasks/task_05_identification.py` · **פונקציה:** `identify_single_segment(file_path)`
**כלים:** `librosa`/`resemblyzer`, `numpy`, `scipy.spatial.distance` (cosine similarity)
**זו לא פונקציה עם endpoint משלה** — היא נקראת מתוך משימה 06 (segmentation), לא ישירות מ-`app.py`.

קלט (פנימי, לא HTTP): קטע שמע (WAV) בודד
פלט (פנימי): `{"speaker": "...", "confidence": 0.0-1.0}`

**תלות ישירה:** משימה 06 מייבאת (`import`) את `identify_single_segment` מהקובץ הזה ומריצה אותה על כל חלון זמן. לתאם את שם הפונקציה ואת הפרמטרים בדיוק עם מי שעושה משימה 06.

---

## שלב 6: חלוקה לקטעים (משימה 06)
**קובץ:** `server/tasks/task_06_segmentation.py` · **פונקציה:** `segment_and_identify(file_url)`
**כלים:** `pydub`/`librosa` (חיתוך לחלונות) + קריאה ל-`identify_single_segment` ממשימה 05
**+ משימה 09 בונוס:** עורכת פונקציה זו (או קוראת לה) כדי להוסיף שדה `text` לכל segment

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
עם תמלול (בונוס 09), כל segment מקבל גם `"text": "..."`.

**מה `app.py` עושה:** קורא ל-`segment_and_identify(file_url)`, שבתוכה קוראת בלולאה ל-`identify_single_segment` על כל חלון.

---

## שלב 7: דוח (משימה 07, + משימות 10/11/12 בונוס)
**קובץ:** `server/tasks/task_07_report.py` · **פונקציה:** `build_report(segments)`
**כלים:** `Flask` + `Jinja2` (תבנית ב-`server/templates/report.html`), אופציונלי `fpdf2`
**בונוסים שנכנסים לתוך אותו קובץ/תבנית:**
- משימה 10 (timeline) - מוסיפה קריאה ל-`build_timeline()` בתוך `build_report()`
- משימה 11 (LLM summary) - מוסיפה קריאה ל-`generate_summary()` בתוך `build_report()`
- משימה 12 (confidence flag) - מוסיפה עיבוד ל-segments *לפני* שהם מגיעים ל-`build_report()`

`POST /report` — קלט: JSON של שלב 6
פלט: דוח HTML (מוצג ב-`server/templates/report.html`) + JSON סיכום:
```json
{
  "total_speakers": 2,
  "total_duration_sec": 42.3,
  "speaker_breakdown": {"speaker_A": 12.4, "unknown": 17.7}
}
```

**מה `app.py` עושה:** קורא ל-`build_report(segments)`, שמרנדרת HTML עם `render_template("report.html", ...)`.

---

## פירוט משימות הבונוס - קובץ ופונקציה

| משימה | קובץ | פונקציה | איך מתחברת לפייפליין |
|---|---|---|---|
| 08 - הפחתת רעש | `task_08_noise_reduction.py` | `reduce_noise(audio_segment)` | נקראת **מתוך** `task_03_cleaning.py` |
| 09 - תמלול | `task_09_transcription.py` | `transcribe_segment(file_path, start, end)` | נקראת **מתוך** `task_06_segmentation.py` |
| 10 - ציר זמן | `task_10_timeline.py` | `build_timeline(segments)` | נקראת **מתוך** `task_07_report.py` |
| 11 - סיכום LLM | `task_11_llm_summary.py` | `generate_summary(segments)` | נקראת **מתוך** `task_07_report.py` |
| 12 - דגל אדום | `task_12_confidence_flag.py` | `flag_low_confidence(segments, threshold=0.5)` | נקראת **לפני** `task_07_report.py` (על ה-segments) |

**חשוב לכל משימות הבונוס:** אתם עורכים קובץ חדש משלכם, אבל **גם** קובץ קיים של מישהו אחר (כדי לחבר את הקריאה). זה אומר שחייבים לתאם ולעבוד לפי `docs/git-workflow.md` - branch נפרד, ו-PR שמישהו אחר (בעל הקובץ המקורי) מאשר, לא רק push.

---

## כלל ברזל
כל שינוי בטבלאות למעלה - שם קובץ, שם פונקציה, פרמטרים, או מבנה ה-JSON - חייב תיאום עם כל מי שתלוי בו *לפני* השינוי, לא אחריו.
