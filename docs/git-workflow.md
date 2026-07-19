# פרוטוקול עבודה ב-Git

מסמך זה מגדיר איך עובדים על הפרויקט הזה - **בדיוק כמו בתעשייה**. אין push ישיר ל-`main`, אף פעם. כל שינוי עובר branch → commit → push → Pull Request → review → merge.

## למה זה חשוב
`main` הוא הענף שתמיד אמור לעבוד. אם כולם דוחפים ישירות אליו, מספיק תלמיד אחד עם קוד שבור כדי לשבור לכולם את הפרויקט. Branch נפרד = כל אחד עובד בבועה משלו עד שהקוד באמת מוכן.

---

## שלב 1: לפני שמתחילים - לוודא שה-main מעודכן

```bash
git checkout main
git pull origin main
```

## שלב 2: יצירת branch חדש למשימה שלך

שם ה-branch חייב להיות ברור - כולל מספר המשימה ותיאור קצר. פורמט:
```
task/<מספר-משימה>-<תיאור-קצר>
```

```bash
git checkout -b task/03-cleaning
```

**דוגמאות נוספות לשמות תקינים:**
```bash
git checkout -b task/05-speaker-identification
git checkout -b task/09-transcription-bonus
```

## שלב 3: עבודה + commit

עובדים על הקוד כרגיל. מ-commit ראשון עדיף לא לחכות עד "הכל מוכן" - commit-ים קטנים ותכופים עדיפים על commit ענק אחד בסוף היום.

```bash
git add server/tasks/cleaning.py
git commit -m "task 03: add silence trimming"
```

**כללי הודעת commit:**
- מתחילים במספר המשימה
- פועל בהווה ("add", "fix" - לא "added", "fixed")
- קצר וממוקד - מה השתנה, לא איך

```bash
git commit -m "task 03: normalize audio volume"
git commit -m "task 03: convert output to 16kHz mono"
git commit -m "task 03: handle empty file edge case"
```

## שלב 4: דחיפה ל-GitHub

בפעם הראשונה שדוחפים branch חדש:
```bash
git push -u origin task/03-cleaning
```
בפעמים הבאות על אותו branch, מספיק:
```bash
git push
```

## שלב 5: פתיחת Pull Request

ב-GitHub, לוחצים "Compare & pull request" (מופיע אוטומטית אחרי push של branch חדש).

**כותרת ה-PR:** אותו פורמט כמו שם ה-branch
```
Task 03: Audio cleaning (silence trim + normalize)
```

**תיאור ה-PR - תבנית מומלצת:**
```markdown
## מה נעשה
חיתוך שקטים אוטומטי + נרמול עוצמה + המרה ל-16kHz mono

## איך בדקתי
הרצתי על 3 קבצי דוגמה מ-data/samples, כולל קובץ עם שקט ארוך בהתחלה

## תואם לחוזה ה-API?
כן - פלט תואם למבנה ב-docs/api-contract.md
```

## שלב 6: Code Review

**לפני שמבקשים review מחבר אחר:**
- לוודא שהקוד רץ בפועל (לא רק "נראה טוב")
- לבדוק שהפלט תואם לחוזה ה-API בדיוק (שמות שדות, טיפוסים)

**מי שעושה review:**
- בודק שהקוד עונה לקריטריון הסיום (Definition of Done) בכרטיס המשימה
- מוסיף הערות ישירות על שורות קוד ב-GitHub (לא רק "נראה טוב" גורף)
- מאשר (Approve) רק אחרי שבאמת בדק, לא אוטומטית

## שלב 7: מיזוג (Merge)

**רק אחרי אישור (Approve) של code review אחד לפחות:**

```bash
git checkout main
git pull origin main
git checkout task/03-cleaning
git merge main
```
אם יש קונפליקטים - פותרים אותם עכשיו, ב-branch שלכם, לא אחרי המיזוג ל-main.

לאחר מכן, ב-GitHub: לוחצים "Merge pull request" (לא בטרמינל - כדי שההיסטוריה בגיטהב תישאר ברורה).

## שלב 8: ניקוי

אחרי שה-PR מוזג:
```bash
git checkout main
git pull origin main
git branch -d task/03-cleaning
```

---

## חוקי ברזל
1. **אף פעם לא `git push origin main` ישירות** - רק דרך PR.
2. **branch אחד = משימה אחת.** לא מערבבים כמה משימות באותו branch.
3. **לא דוחסים (`git commit --amend`) commit-ים שכבר נדחפו** ושמישהו אחר כבר ראה.
4. **אם שינית שדה בחוזה ה-API** (ב-`docs/api-contract.md`) - זה חייב review של מי שהמשימה שלו תלויה בשינוי, לפני merge.
5. **קונפליקט merge = לפתור בעצמך ב-branch שלך**, לא לבקש מהמורה "לתקן את זה".

## פקודות שימושיות למצבי חירום

בדיקה על איזה branch אני נמצא:
```bash
git branch
```

ביטול שינויים לא-committed בקובץ:
```bash
git checkout -- <filename>
```

הצגת היסטוריית commit-ים:
```bash
git log --oneline
```
