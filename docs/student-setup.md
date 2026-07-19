# מדריך הורדה - להתחיל לעבוד על הפרויקט

בצע את השלבים האלה **פעם אחת בלבד**, בתחילת היום, לפני שתתחיל לעבוד על המשימה שלך.

## שלב 0: ודא שיש לך Git ו-Python מותקנים

בדוק בטרמינל:
```bash
git --version
python --version
```
אם אחת הפקודות לא מוכרת - קרא למורה לפני שממשיכים.

## שלב 1: הגדרת פרטי המשתמש שלך ב-Git (פעם אחת בלבד, על כל מחשב)

Git צריך לדעת מי אתה, כדי שכל commit יסומן בשמך:
```bash
git config --global user.name "השם שלך באנגלית"
git config --global user.email "המייל שאיתו נרשמת ל-GitHub"
```

אם אתה עובד ב-Windows (MINGW/Git Bash), הרץ גם את זה - מונע בעיות עתידיות עם שבירות שורה:
```bash
git config --global core.autocrlf true
```

## שלב 2: שכפול (Clone) הפרויקט מ-GitHub

עבור לתיקייה שבה אתה רוצה שהפרויקט יישב (למשל שולחן העבודה או תיקיית Documents), ואז:
```bash
git clone https://github.com/yedidiaf-star/audio-intel-project.git
cd audio-intel-project
```

זה יוצר אצלך עותק מלא של הפרויקט **כולל** היסטוריית ה-Git - זה לא רק הורדת קבצים, זה שכפול אמיתי שמאפשר לך לעבוד עם branches ולדחוף שינויים בהמשך.

## שלב 3: יצירת סביבה וירטואלית (venv)

סביבה מבודדת לפרויקט הזה בלבד, כדי שהחבילות לא יתנגשו עם פרויקטים אחרים על המחשב שלך:
```bash
python -m venv .venv
```

**הפעלת הסביבה** - שים לב שהפקודה שונה בין Windows ל-Mac/Linux:

Windows (Git Bash / MINGW):
```bash
source .venv/Scripts/activate
```

Windows (PowerShell/CMD):
```bash
.venv\Scripts\activate
```

Mac / Linux:
```bash
source .venv/bin/activate
```

אחרי ההפעלה, אמור להופיע `(.venv)` בתחילת שורת הטרמינל - זה הסימן שהסביבה פעילה.

## שלב 4: התקנת הספריות

```bash
pip install -r requirements.txt
```

זה יתקין את כל הספריות שהפרויקט צריך (Flask ועוד) - עלול לקחת כמה דקות.

## שלב 5: בדיקה שהכל עובד

```bash
cd server
python app.py
```

אם רואים בטרמינל משהו כמו `Running on http://127.0.0.1:5000` - השרת רץ בהצלחה. אפשר לפתוח דפדפן ולגשת לכתובת `http://127.0.0.1:5000` כדי לראות `{"status": "server is running"}`.

עצור את השרת עם `Ctrl+C` בטרמינל כשסיימת לבדוק.

## שלב 6: יצירת branch למשימה שלך

**לפני שכותבים שורת קוד אחת** - לפי `docs/git-workflow.md`:
```bash
git checkout -b task/<מספר-משימה>-<תיאור-קצר>
```
לדוגמה, אם קיבלת משימה 03:
```bash
git checkout -b task/03-cleaning
```

---

## אם משהו נכשל

**שגיאת SSL certificate בזמן push/clone** (נפוץ ברשתות בית ספר):
```bash
git config http.sslBackend schannel
```
ואם זה לא פותר - כפתרון זמני נוסף (רק בתוך תיקיית הפרויקט, לא גלובלית):
```bash
git config http.sslVerify false
```

**`pip install` נכשל / לוקח נצח** - ודא שהסביבה הוירטואלית פעילה (`(.venv)` מופיע בטרמינל) לפני ההתקנה.

**כל שגיאה אחרת** - קרא למורה עם הצילום מסך/הודעת השגיאה המלאה לפני שמנסים "לתקן" באקראי.

---

## סיכום מהיר - כל הפקודות ברצף

```bash
git config --global user.name "השם שלך"
git config --global user.email "המייל שלך"
git clone https://github.com/yedidiaf-star/audio-intel-project.git
cd audio-intel-project
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
git checkout -b task/<מספר-המשימה-שלך>
```
