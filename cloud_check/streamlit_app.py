# streamlit_app.py
# תבנית אתר מידע/ביקורות/יצירת קשר בסגנון פורטל מידע (לא מכירות)
# ⚠️ חשוב: זו אינה עצה רפואית. יש להוסיף דיסקליימר מתאים ולהפנות לייעוץ רפואי מוסמך.

import streamlit as st
from datetime import datetime
import pandas as pd
from pathlib import Path

# -----------------------------
# הגדרות בסיס ו-SEO
# -----------------------------
st.set_page_config(
    page_title="בריאות המשפחה – ידע, סיפורים וביקורות",
    page_icon="💚",
    layout="wide",
)

# עיצוב RTL בסיסי
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        direction: rtl;
        text-align: right;
        font-family: "Heebo", "Rubik", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Fira Sans", "Droid Sans", "Helvetica Neue", Arial, sans-serif;
    }
    /* כפתורים וכרטיסים רכים */
    .stButton>button {border-radius: 16px; padding: 0.6rem 1rem;}
    .box {background: #ffffff; border-radius: 18px; padding: 18px; box-shadow: 0 8px 24px rgba(0,0,0,0.06);}    
    .muted {color: #666; font-size: 0.9rem}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# נתונים – דמו + קריאה מ-CSV (מקומי)
# בענן של Streamlit, קבצי כתיבה לא תמיד נשמרים. להפקה – מומלץ Google Sheets/Airtable.
# -----------------------------
DATA_DIR = Path("data")
REVIEWS_CSV = DATA_DIR / "reviews.csv"
DATA_DIR.mkdir(exist_ok=True)

if REVIEWS_CSV.exists():
    reviews_df = pd.read_csv(REVIEWS_CSV)
else:
    reviews_df = pd.DataFrame([
        {"שם": "רונית מ.", "כותרת": "תודה גדולה",
         "תיאור": "קיבלתי עצות שעזרו לי להקל על כאבי גב כרוניים. ברור שזה לא במקום רופא, אבל זה תרם.", "דירוג": 5,
         "תאריך": "2025-08-01"},
        {"שם": "יואב ש.", "כותרת": "מידע שימושי ומעודן",
         "תיאור": "קראתי על מניעת פצעי לחץ והצלחתי לשפר את המצב של אבי.", "דירוג": 4, "תאריך": "2025-07-21"},
    ])
    reviews_df.to_csv(REVIEWS_CSV, index=False)


# פונקציה להצגת כוכבים
def stars(n: int):
    n = int(n)
    return "⭐" * n + "☆" * (5 - n)


# -----------------------------
# סרגל צד
# -----------------------------
with st.sidebar:
    st.image("https://static.streamlit.io/examples/dice.jpg", caption="תמונת דמו להחלפה")
    st.markdown("""
    ### על סבא
    סבא אוהב לעזור לאנשים לשפר איכות חיים בעזרת ידע, ניסיון וטיפים מעשיים.

    **חשוב**: אין כאן ייעוץ רפואי. תמיד לפנות לגורם רפואי מוסמך.
    """)
    st.divider()
    st.markdown("""
    **פרטי התקשרות**  
    📞 050-000-0000  
    ✉️ example@example.com  
    💬 WhatsApp: wa.me/972500000000
    """)

# -----------------------------
# כותרת עליונה
# -----------------------------
st.title("בריאות המשפחה 💚 – ידע, סיפורים וביקורות")
st.write(
    "אתר מידע ידידותי: מאמרים, טיפים, סיפורי השראה וביקורות מהקהילה. לא במקום רופא."
)

# אזור דיסקליימר ברור
with st.container(border=True):
    st.markdown(
        """
        **דיסקליימר רפואי**: התוכן באתר נועד למידע כללי וחוויות אישיות בלבד ואינו מהווה ייעוץ רפואי, אבחון או תחליף לטיפול רפואי מקצועי. בכל בעיה רפואית יש לפנות לרופא.
        """
    )

st.divider()

# -----------------------------
# ניווט טאבּים
# -----------------------------
tab_home, tab_articles, tab_reviews, tab_contact = st.tabs([
    "ראשי", "מאמרים וטיפים", "ביקורות הקהילה", "יצירת קשר"
])

# -----------------------------
# טאב ראשי – סיפור אישי ודגשים
# -----------------------------
with tab_home:
    st.subheader("ברוכים הבאים!")
    st.write(
        """
        כאן תמצאו מידע קריא ומסודר על נושאי בריאות פופולריים, **סיפורי השראה מהשטח**, וקישורים למקורות אמינים. 
        **הערה**: סיפורים אישיים הם חוויות – לא הוכחות מדעיות. 
        """
    )

    with st.container():
        st.markdown("### סיפור השראה: התמודדות עם פצעי לחץ")
        st.markdown(
            """
            סיפור משפחתי: לאחר שבני המשפחה התמודדו עם פצעי לחץ, למדנו על **מניעה** (החלפת תנוחה, כריות מתאימות, תזונה והיגיינה) ועל חשיבות **מעקב רפואי**.
            התנסינו גם בשיטות משלימות שנוח לאנשים לנסות – אך תמיד לצד מעקב רופא. 
            """
        )
        st.info("טיפ בטיחות: פצעי לחץ דורשים מעקב רפואי. אם יש סימני זיהום/כאב/חום – לפנות לרופא מיד.")

# -----------------------------
# טאב מאמרים
# -----------------------------
with tab_articles:
    st.subheader("מאמרים וטיפים")

    cols = st.columns(3)
    with cols[0]:
        st.markdown("#### מניעת פצעי לחץ")
        st.write("החלפת תנוחה תכופה, מזרנים/כריות מתאימים, תזונה מספקת, והיגיינה.")
        st.caption("מידע כללי – לא במקום הנחיית צוות רפואי.")
    with cols[1]:
        st.markdown("#### עקרונות תזונה התומכת בחוסן")
        st.write("שתייה מספקת, חלבון איכותי, ויטמינים ומינרלים בהתאם להנחיות רופא/דיאטנית.")
    with cols[2]:
        st.markdown("#### תנועה עדינה")
        st.write("תרגילי טווח תנועה עדינים (בהנחיית פיזיותרפיסט), תמיכה בהקלה מכאבים והגמשת מפרקים.")

    st.markdown("---")
    st.markdown("### שאלות נפוצות (FAQ)")
    with st.expander("האם זה ייעוץ רפואי?"):
        st.write("לא. זהו מידע כללי בלבד. לכל שאלה רפואית יש לפנות לרופא.")
    with st.expander("האם אפשר להשתמש בשיטות משלימות?"):
        st.write("אפשר לשקול, אך רק בנוסף ולא במקום טיפול רפואי. אם מתפתח כאב, חום או החמרה – ליצור קשר עם רופא.")

# -----------------------------
# טאב ביקורות
# -----------------------------
with tab_reviews:
    st.subheader("ביקורות הקהילה")

    # תצוגה
    for _, row in reviews_df.sort_values("תאריך", ascending=False).iterrows():
        with st.container():
            st.markdown(f"**{row['כותרת']}** · {stars(int(row['דירוג']))}")
            st.caption(f"מאת {row['שם']} בתאריך {row['תאריך']}")
            st.write(row['תיאור'])
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
                    "שם": name,
                    "כותרת": title,
                    "תיאור": desc,
                    "דירוג": rating,
                    "תאריך": datetime.now().date().isoformat(),
                }
                # כתיבה ל-CSV (במקומי). בענן ייתכן שלא יישמר לאורך זמן.
                try:
                    df2 = pd.concat([reviews_df, pd.DataFrame([new_row])], ignore_index=True)
                    df2.to_csv(REVIEWS_CSV, index=False)
                    st.success("תודה! הביקורת נוספה (בדמו). להפקה – חברו ל-Google Sheets/Airtable.")
                except Exception as e:
                    st.warning(f"לא ניתן לשמור כעת (סביבת ענן?). שמרו לשירות מאובטח חיצוני. פרטים בלשונית יצירת קשר.")

# -----------------------------
# טאב יצירת קשר
# -----------------------------
with tab_contact:
    st.subheader("יצירת קשר")

    st.markdown(
        """
        אפשר ליצור קשר בכל אחת מהדרכים הבאות:

        - 📞 טלפון: **050-000-0000**  
        - ✉️ אימייל: **example@example.com**  
        - 💬 WhatsApp: **wa.me/972500000000**  
        - 📍 אזור פעילות: מרכז הארץ  

        **טופס מקוון** (מומלץ): אפשר לחבר Google Form/Typeform ולקבל הודעות למייל ולגיליון. 
        """
    )

    with st.expander("איך לחבר Google Form לאתר?"):
        st.markdown(
            """
            1. צרו Google Form חדש לשם *יצירת קשר* או *שליחת ביקורת*.
            2. קבלו קישור Embed (Iframe) של הטופס.
            3. הוסיפו כאן `st.components.v1.iframe(url, height=600)` כדי להטמיע את הטופס בתוך העמוד.
            4. התגובות ייאספו אוטומטית ל-Google Sheets שתוכלו להציג בלשונית הביקורות/פניות.
            """
        )

    st.divider()
    st.caption("© 2025 משפחת סבא – אתר מידע לקהילה. אין לראות בתוכן ייעוץ רפואי.")
