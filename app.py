import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Massilia", layout="wide")

# --- GLOBAL STYLE ---
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f4efe6;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #1e88e5, #42a5f5);
    padding: 40px;
    border-radius: 25px;
    color: white;
    margin-bottom: 20px;
}

/* CARDS */
.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* ORANGE CARD */
.card-orange {
    background: #ff9800;
    color: white;
    padding: 20px;
    border-radius: 20px;
}

/* BUTTON */
.stButton>button {
    background-color: #ff9800;
    color: white;
    border-radius: 10px;
    border: none;
}

/* TAG */
.tag {
    background: #e3f2fd;
    padding: 5px 10px;
    border-radius: 10px;
    font-size: 12px;
}

/* DISCOUNT BADGE */
.badge {
    background: #ff9800;
    color: white;
    padding: 4px 10px;
    border-radius: 8px;
    font-size: 12px;
}

/* TITLE */
h1, h2, h3 {
    color: #1e88e5;
}
</style>
""", unsafe_allow_html=True)

# --- DATA ---
data = [
    {"name": "Bar du Port", "lat": 43.2965, "lon": 5.3698, "price": 5, "specialty": "Pastis", "deal": "-20%"},
    {"name": "Chez Panisse", "lat": 43.2950, "lon": 5.3740, "price": 8, "specialty": "Panisse", "deal": "-10%"},
    {"name": "Fougasse House", "lat": 43.3000, "lon": 5.3700, "price": 6, "specialty": "Fougasse", "deal": "-15%"},
    {"name": "Le Vieux Marseille", "lat": 43.2970, "lon": 5.3725, "price": 7, "specialty": "Pastis", "deal": "-5%"},
]

df = pd.DataFrame(data)

if "comments" not in st.session_state:
    st.session_state.comments = []

# --- HERO ---
st.markdown("""
<div class="hero">
    <h1>🍋 Pas fâché avec <span style="color:#ffeb3b;">le plaisir</span></h1>
    <p>Discover the best spots in Marseille with deals & community tips.</p>
</div>
""", unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2 = st.columns([2,1])

# --- MAP ---
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📍 Explore Marseille")

    m = folium.Map(location=[43.2965, 5.3698], zoom_start=13, tiles="CartoDB positron")

    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"{row['name']} - €{row['price']}",
            icon=folium.Icon(color="blue"),
        ).add_to(m)

    st_folium(m, height=450)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SIDEBAR FILTER ---
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Your Preferences")

    with st.form("preferences"):
        specialty = st.radio("Specialty", ["Pastis", "Panisse", "Fougasse"])
        budget = st.select_slider("Budget", ["€", "€€", "€€€"])
        mood = st.selectbox("Mood", ["Chill", "Party", "Authentic"])
        submitted = st.form_submit_button("Apply")

    st.markdown('</div>', unsafe_allow_html=True)

# --- FILTER ---
if submitted:
    filtered = df[df["specialty"] == specialty]
else:
    filtered = df

# --- RESULTS CARDS ---
st.subheader("🔥 Best Spots")

cols = st.columns(3)
for i, row in filtered.iterrows():
    with cols[i % 3]:
        st.markdown(f"""
        <div class="card">
            <h4>{row['name']}</h4>
            <span class="tag">{row['specialty']}</span>
            <p>💰 €{row['price']}</p>
            <span class="badge">{row['deal']}</span>
        </div>
        """, unsafe_allow_html=True)

# --- COMMUNITY ---
st.subheader("💬 Community")

with st.form("comment_form"):
    username = st.text_input("Your name")
    comment = st.text_area("Share your experience")
    photo = st.file_uploader("Upload a photo", type=["jpg", "png"])
    post = st.form_submit_button("Post")

if post and comment:
    st.session_state.comments.append(
        {"user": username, "comment": comment, "photo": photo}
    )

# Display styled comments
cols = st.columns(3)
for i, c in enumerate(reversed(st.session_state.comments)):
    with cols[i % 3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"**{c['user']}**")
        st.write(c["comment"])
        if c["photo"]:
            st.image(c["photo"])
        st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<hr>
<p style="text-align:center; color:gray;">🌊 Made in Marseille • Deals • Community • Food</p>
""", unsafe_allow_html=True)
