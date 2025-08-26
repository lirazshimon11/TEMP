# streamlit_app.py
# ⚠️ מידע כללי בלבד – לא ייעוץ רפואי.

import streamlit as st
from datetime import datetime
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components

# -----------------------------
# הגדרות בסיס ו-SEO
# -----------------------------
st.set_page_config(
    page_title="המרפאה של יפת – רפואה טבעית לגיל השלישי",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="collapsed",   # NEW: במובייל ייפתח סגור
)

# --------- CSS מאוחד ורספונסיבי ---------
st.markdown("""
<style>
/* ========== בסיס ========== */
:root { --lift: 64px; }
* { box-sizing: border-box; }
html, body { margin:0; padding:0; }
body { overflow-x: hidden; } /* NEW: בלי גלילה אופקית */

/* הסתרת תפריט עליון (נשאיר כפתור סיידבר במובייל) */
#MainMenu { visibility: hidden; }
[data-testid="stToolbar"] { display: none !important; }

/* סיידבר – דסקטופ (ימין ב-RTL) */
[data-testid="stSidebar"]{
  min-width: 350px;
  max-width: 350px;
  right: 0 !important; left: auto !important;
  z-index: 100; /* מעל התוכן כשפתוח */
}

/* הסתרת כפתור סיידבר בדסקטופ – במובייל כן נציג */
@media (min-width: 769px){
  [data-testid="stSidebarCollapseButton"],
  button[title="Toggle sidebar"],
  button[title="Show sidebar"],
  button[title="Hide sidebar"] { display: none !important; }
}

/* "הרמת" העמוד – דסקטופ בלבד */
.stApp header, .stApp header[data-testid="stHeader"] {
  display: none !important; height: 0 !important; min-height: 0 !important;
}
.stApp [data-testid="stAppViewContainer"] {
  padding-top: 0 !important; margin-top: calc(-1 * var(--lift)) !important;
}
.stApp .main .block-container, .stApp [data-testid="block-container"] {
  padding-top: 0 !important; margin-top: calc(-1 * var(--lift)) !important; padding-bottom: 1rem !important;
}
.main .block-container { margin-top: -48px !important; }

/* תמונות רספונסיביות */
img { max-width: 100%; height: auto; }

/* טאבים – גלילה אופקית עדינה במובייל אם אין מקום */
.stTabs [role="tablist"]{ overflow-x:auto; white-space:nowrap; }

/* ======== מובייל/טאבלט (עד 768px) ======== */
@media (max-width: 768px){
  :root { --lift: 0px; } /* מבטלים הרמה */
  .stApp header, .stApp header[data-testid="stHeader"] {
    display: block !important; height: auto !important; min-height: auto !important;
  }
  .stApp [data-testid="stAppViewContainer"],
  .stApp .main .block-container, .stApp [data-testid="block-container"], .main .block-container {
    margin-top: 0 !important; padding-top: 0.5rem !important;
  }

  /* מציגים את כפתור פתיחת/סגירת הסיידבר במובייל */
  [data-testid="stSidebarCollapseButton"],
  button[title="Toggle sidebar"],
  button[title="Show sidebar"],
  button[title="Hide sidebar"] { display: inline-flex !important; }

  /* סיידבר צר יותר במובייל; יושב מעל התוכן כשפתוח */
  [data-testid="stSidebar"]{
    min-width: 260px; max-width: 80vw;
    position: sticky;
    top: 0;
  }

  /* מגבלה על בסיס הפונט במובייל כדי שה-H1 לא יתנפח בגלל הסליידר */
  html, body, [class*="css"] {
    font-size: min(var(--fs, 18px), 18px) !important;  /* NEW: תקרה 18px בנייד */
  }

  /* כיוונון כותרות – זה הפתרון ל-H1 הענק בצילום */
  .stApp h1, [data-testid="stMarkdownContainer"] h1 {
    font-size: clamp(22px, 6.2vw + 6px, 32px) !important; line-height: 1.25 !important;
    margin-top: .25rem !important; margin-bottom: .5rem !important;
    word-break: break-word;
  }
  .stApp h2, [data-testid="stMarkdownContainer"] h2 {
    font-size: clamp(18px, 4.6vw + 6px, 26px) !important; line-height: 1.3 !important;
  }
  .stApp h3, [data-testid="stMarkdownContainer"] h3 {
    font-size: clamp(16px, 3.8vw + 6px, 22px) !important;
  }

  /* כפתורים/קופסאות – פחות ריווח כדי למנוע גלילה רוחבית */
  .stButton>button { padding: 0.5rem 0.9rem; }
  .box { padding: 14px; border-radius: 14px; }
}

/* קישורי קשר – תיקון כיווניות למספרים */
.contact a { unicode-bidi: plaintext; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# שליטת גודל טקסט (סליידר) + הגדרת משתנה גלובלי
# -----------------------------
font_size = st.sidebar.slider("גודל טקסט", 14, 30, 18)
st.markdown(f"<style>:root{{--fs:{font_size}px;}}</style>", unsafe_allow_html=True)

# עיצוב RTL בסיסי
st.markdown(
    """
    <style>
    html, body, [class*="css"]{
        direction: rtl;
        text-align: right;
        font-family: "Heebo","Rubik",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen,Ubuntu,Cantarell,"Fira Sans","Droid Sans","Helvetica Neue",Arial,sans-serif;
        font-size: var(--fs, 18px);
    }
    .stButton>button { border-radius: 16px; padding: 0.6rem 1rem; }
    .box { background:#fff; border-radius:18px; padding:18px; box-shadow:0 8px 24px rgba(0,0,0,0.06); }
    .muted { color:#666; font-size:0.9rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# נתונים – דמו + קריאה/כתיבה ל-CSV (מקומי)
# -----------------------------
DATA_DIR = Path("data")
REVIEWS_CSV = DATA_DIR / "reviews.csv"
DATA_DIR.mkdir(exist_ok=True)
APP_DIR = Path(__file__).resolve().parent
IMG_PATH = APP_DIR / "images" / "saba.jpg"

if REVIEWS_CSV.exists():
    try:
        reviews_df = pd.read_csv(REVIEWS_CSV)
    except Exception:
        reviews_df = pd.DataFrame(columns=["שם", "כותרת", "תיאור", "דירוג", "תאריך"])
else:
    reviews_df = pd.DataFrame([
        {"שם": "רונית מ.", "כותרת": "לחץ דם מאוזן",
         "תיאור": "יפת הכין לאמי חליטות מצמחי מרפא שגידל והמדדים השתפרו לצד הטיפול הרפואי.", "דירוג": 5,
         "תאריך": "2025-08-01"},
        {"שם": "יואב ש.", "כותרת": "הקלה בפצעי לחץ",
         "תיאור": "השמנים של יפת נתנו מענה לפצעי הלחץ של אבי והחלמה הייתה מהירה יותר.", "דירוג": 4,
         "תאריך": "2025-07-21"},
    ])
    try:
        reviews_df.to_csv(REVIEWS_CSV, index=False)
    except Exception:
        pass

def stars(n: int):
    n = int(n)
    return "⭐" * n + "☆" * (5 - n)

# -----------------------------
# סרגל צד
# -----------------------------
with st.sidebar:
    if IMG_PATH.exists():
        st.image(str(IMG_PATH))
    else:
        st.warning("לא נמצאה התמונה images/saba.jpg בקונטיינר. מציג תמונת ברירת מחדל.")
        st.image("https://static.streamlit.io/examples/dice.jpg")

    st.markdown("""
    ### על יפת
    יפת מגדל צמחי מרפא ומציע רפואה אלטרנטיבית למבוגרים עם לחץ דם, כולסטרול או פצעי לחץ.

    **חשוב**: אין כאן ייעוץ רפואי. יש לפנות לרופא מוסמך בכל בעיה.
    """)

    st.divider()
    st.markdown("### פרטי התקשרות")
    st.markdown(
        """
- 📞 [0522222222](tel:+972522222222)
- ✉️ [example@example.com](mailto:example@example.com)
- 💬 WhatsApp: [שליחת הודעה](https://wa.me/972522222222)
        """
    )

# -----------------------------
# כותרת עליונה
# -----------------------------
st.title("יפת 💚 – רפואה טבעית לגיל השלישי")
st.write("מידע כללי על צמחי מרפא ושיטות משלימות המבוססות על ניסיונו של יפת. התוכן אינו תחליף לרופא.")

with st.container(border=True):
    st.markdown(
        """
**דיסקליימר רפואי**: התוכן באתר נועד למידע כללי וחוויות אישיות בלבד ואינו מהווה ייעוץ רפואי, אבחון או תחליף לטיפול רפואי מקצועי. בכל בעיה רפואית יש לפנות לרופא.
        """
    )

st.divider()

# -----------------------------
# טאבּים
# -----------------------------
tab_home, tab_articles, tab_reviews, tab_contact = st.tabs([
    "ראשי", "מאמרים וטיפים", "ביקורות הקהילה", "יצירת קשר"
])

with tab_home:
    st.subheader("ברוכים הבאים!")
    st.write(
        """
יפת משלב ידע מסורתי עם צמחים שהוא מגדל כדי לסייע למבוגרים הסובלים מלחץ דם, כולסטרול ופצעי לחץ.
באתר תמצאו מידע כללי וסיפורי הצלחה מהקהילה.
        """
    )
    with st.container():
        st.markdown("### סיפור הצלחה: פתרון לפצעי לחץ")
        st.markdown("אחד המטופלים קיבל משחות וחליטות מצמחיו של יפת לצד טיפול רפואי, והמשפחה דיווחה על שיפור.")
        st.info("טיפ בטיחות: פצעי לחץ דורשים מעקב רפואי. אם יש סימני זיהום/כאב/חום – לפנות לרופא מיד.")

with tab_articles:
    st.subheader("מאמרים וטיפים")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("#### צמחים לאיזון לחץ דם")
        st.write("חליטות על בסיס זית, רוזמרין ועוד – בהכוונת רופא בלבד.")
        st.caption("מידע כללי – לא במקום טיפול תרופתי.")
    with cols[1]:
        st.markdown("#### תמיכה באיזון כולסטרול")
        st.write("תזונה מאוזנת וצמחי מרפא כמו גדילן מצוי או שום.")
    with cols[2]:
        st.markdown("#### טיפוח העור ומניעת פצעי לחץ")
        st.write("שמנים/משחות לצד החלפת תנוחה והיגיינה.")

    st.markdown("---")
    st.markdown("### שאלות נפוצות (FAQ)")
    with st.expander("האם זה ייעוץ רפואי?"):
        st.write("לא. זהו מידע כללי בלבד. לכל שאלה רפואית יש לפנות לרופא.")
    with st.expander("האם אפשר להשתמש בשיטות משלימות?"):
        st.write("אפשר לשקול, אך רק בנוסף ולא במקום טיפול רפואי.")

with tab_reviews:
    st.subheader("ביקורות הקהילה")

    if not reviews_df.empty and "תאריך" in reviews_df.columns:
        try:
            df_show = reviews_df.copy()
            df_show["__ts__"] = pd.to_datetime(df_show["תאריך"], errors="coerce")
            df_show = df_show.sort_values("__ts__", ascending=False).drop(columns=["__ts__"])
        except Exception:
            df_show = reviews_df
    else:
        df_show = reviews_df

    for _, row in df_show.iterrows():
        with st.container():
            st.markdown(f"**{row.get('כותרת','')}** · {stars(int(row.get('דירוג',0) or 0))}")
            st.caption(f"מאת {row.get('שם','')} בתאריך {row.get('תאריך','')}")
            st.write(row.get('תיאור',''))
            st.markdown("---")

    st.markdown("#### הוספת ביקורת (דמו)")
    with st.form("add_review"):
        name = st.text_input("שם פרטי או שם מקוצר (יוצג באתר)")
        title = st.text_input("כותרת קצרה")
        desc = st.text_area("תיאור החוויה בקצרה")
        rating = st.slider("דירוג", 1, 5, 5)
        agree = st.checkbox("אני מאשר/ת לפרסם את הביקורת באתר בהתאם לתנאי השימוש ולמדיניות הפרטיות")
        submitted = st.form_submit_button("שמור ביקורת")

        if submitted:
            if not agree:
                st.error("יש לאשר פרסום בהתאם למדיניות.")
            elif not (name and title and desc):
                st.error("נא למלא את כל השדות.")
            else:
                new_row = {
                    "שם": name, "כותרת": title, "תיאור": desc,
                    "דירוג": rating, "תאריך": datetime.now().date().isoformat(),
                }
                try:
                    df2 = pd.concat([reviews_df, pd.DataFrame([new_row])], ignore_index=True)
                    df2.to_csv(REVIEWS_CSV, index=False)
                    st.success("תודה! הביקורת נוספה (בדמו). להפקה – חברו ל-Google Sheets/Airtable.")
                except Exception:
                    st.warning("לא ניתן לשמור כעת (סביבת ענן?). שמרו לשירות מאובטח חיצוני.")

with tab_contact:
    st.subheader("יצירת קשר")
    st.markdown(
        """
אפשר ליצור קשר:
- 📞 **0522222222**
- ✉️ **example@example.com**
- 💬 **wa.me/972522222222**
- 📍 אזור פעילות: מרכז הארץ

**טופס מקוון** (מומלץ): Google Form/Typeform והטמעה עם iframe.
        """
    )
    st.divider()
    st.caption("© 2025 יפת – רפואה טבעית. אין לראות בתוכן ייעוץ רפואי.")
