import time
from io import BytesIO

import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance
import streamlit as st

# ---------- Page config ----------
st.set_page_config(
    page_title="Starter App • Streamlit",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Minimal custom styling ----------
st.markdown(
    """
    <style>
      .app-hero {
        padding: 1.25rem 1.5rem;
        border-radius: 1rem;
        background: linear-gradient(135deg,#1f6feb22,#00c2ff22);
        border: 1px solid rgb(230 230 230 / 40%);
      }
      .metric-card {
        border: 1px solid rgb(230 230 230 / 60%);
        border-radius: 1rem;
        padding: 1rem 1.25rem;
        background: white;
      }
      [data-theme="dark"] .metric-card, .metric-card:has(.st-emotion-cache-1wqrzur) {
        background: rgb(255 255 255 / 05%);
        border-color: rgb(255 255 255 / 12%);
      }
      .subtle {
        color: var(--text-color-secondary, #6b7280);
        font-size: 0.9rem;
      }
      .pill {
        display:inline-block;padding:.25rem .6rem;border-radius:999px;
        border:1px solid rgb(230 230 230 / 70%); font-size:.8rem; margin-left:.5rem;
      }
      /* make images look nice */
      .img-wrap img { border-radius: .75rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.title("⚙️ Settings")
    st.caption("בחרי את ההדגמות שתרצי לראות")
    demo = st.radio("Demo section", ["Overview", "Data Playground", "Uploads", "Mini App"], horizontal=False)

    st.divider()
    with st.expander("Theme tweak (client-side only)"):
        accent = st.color_picker("Accent hint (buttons/links)", "#4F46E5", help="רמז צבעוני עדין בעזרת CSS")
        st.markdown(
            f"""
            <style>
              :root {{
                --accent: {accent};
              }}
              .stButton>button, .stDownloadButton>button {{
                border-radius: 10px !important;
                border: 1px solid rgb(230 230 230 / 60%);
              }}
              .st-emotion-cache-1vt4y43 a {{ color: var(--accent) !important; }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.caption("🧪 This is a starter UI built with Streamlit.")

# ---------- Hero ----------
st.markdown(
    """
    <div class="app-hero">
      <h2 style="margin:0;">✨ Streamlit Starter</h2>
      <p class="subtle" style="margin:.25rem 0 0;">
        בסיס נקי לבדיקה: כרטיסי סטטוס, גרפים, העלאת קבצים וטפסים — מוכן להתרחבות.
        <span class="pill">Fast</span><span class="pill">Clean</span><span class="pill">Test-Ready</span>
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# ---------- Session state ----------
if "todos" not in st.session_state:
    st.session_state.todos = [" polish UI", " add API call", " connect DB"]

# ---------- Overview ----------
if demo == "Overview":
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])
    with c1:
        st.markdown("###### Status")
        with st.container(border=True):
            st.write("✅ Everything looks good............................")
            st.progress(80, text="Bootstrapped")
            st.caption("Tip: שחקי עם הקוד בתוך app.py ותראי תוצאה מיידית.")

    for i, (title, value, foot) in enumerate(
        [
            ("Visitors", "1,284", "+12% WoW"),
            ("Conversion", "4.7%", "demo mock"),
            ("Latency", "92 ms", "local run"),
        ]
    ):
        with (c2, c3, c4)[i]:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(title, value, foot)
            st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    lc, rc = st.columns([2, 1])

    with lc:
        st.subheader("Traffic (demo data)")
        n = 50
        x = pd.date_range(end=pd.Timestamp.now().normalize(), periods=n, freq="H")
        y = np.cumsum(np.random.randn(n)) + 50
        df = pd.DataFrame({"timestamp": x, "visitors": y})
        df = df.set_index("timestamp")
        st.line_chart(df)

    with rc:
        st.subheader("Quick Notes")
        new_todo = st.text_input("Add todo", placeholder="e.g. connect to Firestore")
        cols = st.columns([1, 1])
        if cols[0].button("➕ Add", use_container_width=True):
            if new_todo.strip():
                st.session_state.todos.append(new_todo.strip())
                st.toast("Added ✓")
        if cols[1].button("🗑️ Clear all", use_container_width=True):
            st.session_state.todos.clear()
            st.toast("Cleared ✓")
        st.write("—", *st.session_state.todos)

# ---------- Data Playground ----------
elif demo == "Data Playground":
    st.subheader("Upload a CSV and explore")
    up = st.file_uploader("Upload CSV", type=["csv"])
    if up:
        df = pd.read_csv(up)
        st.success(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")
        st.dataframe(df, use_container_width=True)
        st.caption("Quick describe:")
        st.write(df.describe(include="all").T)

        num_cols = df.select_dtypes(include="number").columns.tolist()
        if num_cols:
            st.divider()
            st.markdown("#### Visualize a numeric column")
            sel = st.selectbox("Pick a column", num_cols)
            st.line_chart(df[sel])
    else:
        st.info("העלי קובץ CSV כדי לראות טבלה וסטטיסטיקות.")

# ---------- Uploads (image enhancer) ----------
elif demo == "Uploads":
    st.subheader("Image Enhancer (demo)")
    img_file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg", "webp"])
    if img_file:
        img = Image.open(img_file).convert("RGB")
        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Original**")
            st.image(img, use_column_width=True)
        with colB:
            st.markdown("**Enhanced**")
            bright = st.slider("Brightness", 0.2, 2.0, 1.1, 0.05)
            contrast = st.slider("Contrast", 0.2, 2.0, 1.05, 0.05)
            sharp = st.slider("Sharpness", 0.2, 2.0, 1.0, 0.05)

            out = ImageEnhance.Brightness(img).enhance(bright)
            out = ImageEnhance.Contrast(out).enhance(contrast)
            out = ImageEnhance.Sharpness(out).enhance(sharp)
            st.image(out, use_column_width=True)

            b = BytesIO()
            out.save(b, format="PNG")
            st.download_button("⬇️ Download enhanced PNG", data=b.getvalue(), file_name="enhanced.png")
    else:
        st.info("העלי תמונה כדי לשפר בהירות/קונטרסט/חדות.")

# ---------- Mini App (form) ----------
elif demo == "Mini App":
    st.subheader("Mini contact form")
    with st.form("contact"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        msg = st.text_area("Message", height=120, placeholder="Tell me what you'd like to build…")
        sent = st.form_submit_button("Send")
        if sent:
            if not name or not email or not msg:
                st.error("Please fill all fields.")
            else:
                with st.spinner("Sending... (demo)"):
                    time.sleep(0.8)
                st.success("Sent! (demo only)")

# ---------- Footer ----------
st.write("")
st.caption("Built with ❤️ + Streamlit • Ready to extend.")
