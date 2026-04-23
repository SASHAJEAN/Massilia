import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Massilia", layout="wide")

# --- STYLE ---
st.markdown("""
<style>
html, body {
    background-color: #f4efe6;
    font-family: 'Arial';
}

/* NAVBAR */
.navbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:10px 20px;
}
.logo {
    font-size:24px;
    font-weight:bold;
    color:#1e88e5;
}
.cta {
    background:#ff9800;
    color:white;
    padding:8px 15px;
    border-radius:10px;
}

/* HERO */
.hero {
    background: linear-gradient(135deg, #1e88e5, #42a5f5);
    padding:50px;
    border-radius:25px;
    color:white;
    margin-bottom:20px;
}

/* CARDS */
.card {
    background:white;
    padding:15px;
    border-radius:20px;
    box-shadow:0px 5px 20px rgba(0,0,0,0.08);
    margin-bottom:20px;
}

/* IMAGE CARD */
.card img {
    width:100%;
    border-radius:15px;
}

/* BADGE */
.badge {
    background:#ff9800;
    color:white;
    padding:4px 10px;
    border-radius:8px;
    font-size:12px;
}
</style>
""", unsafe_allow_html=True)

# --- NAVBAR ---
st.markdown("""
<div class="navbar">
    <div class="logo">🍋 Massilia</div>
    <div class="cta">Get Started</div>
</div>
""", unsafe_allow_html=True)

# --- DATA ---
data = [
    {
        "name": "Bar du Port",
        "lat": 43.2965,
        "lon": 5.3698,
        "price": 5,
        "specialty": "Pastis",
        "deal": "-20%",
        "img": "https://images.unsplash.com/photo-1514361892635-cebbd4f07b93"
    },
    {
        "name": "Chez Panisse",
        "lat": 43.2950,
        "lon": 5.3740,
        "price": 8,
        "specialty": "Panisse",
        "deal": "-10%",
        "img": "https://images.unsplash.com/photo-1604908176997-4319c9e6f7a1"
    },
    {
        "name": "Fougasse House",
        "lat": 43.3000,
        "lon": 5.3700,
        "price": 6,
        "specialty": "Fougasse",
        "deal": "-15%",
        "img": "https://images.unsplash.com/photo-1608198093002-ad4e005484ec"
    },
]

df = pd.DataFrame(data)

if "comments" not in st.session_state:
    st.session_state.comments = []

# --- HERO ---
st.markdown("""
<div class="hero">
    <h1>Pas fâché avec <span style="color:#ffeb3b;">le plaisir</span></h1>
    <p>Discover the best places in Marseille with community tips & deals.</p>
</div>
""", unsafe_allow_html=True)

# --- LAYOUT ---
col1, col2 = st.columns([2,1])

# MAP
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    m = folium.Map(location=[43.2965, 5.3698], zoom_start=13)
    for _, row in df.iterrows():
        folium.Marker(
            [row["lat"], row["lon"]],
            popup=row["name"]
        ).add_to(m)
    st_folium(m, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

# FILTER
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("filter"):
        specialty = st.selectbox("Specialty", ["Pastis", "Panisse", "Fougasse"])
        submit = st.form_submit_button("Search")
    st.markdown('</div>', unsafe_allow_html=True)

if submit:
    df = df[df["specialty"] == specialty]

# --- CARDS ---
st.subheader("🔥 Best Spots")
cols = st.columns(3)

for i, row in df.iterrows():
    with cols[i % 3]:
        st.markdown(f"""
        <div class="card">
            <img src="{row['img']}"/>
            <h4>{row['name']}</h4>
            <p>{row['specialty']} • €{row['price']}</p>
            <span class="badge">{row['deal']}</span>
        </div>
        """, unsafe_allow_html=True)

# --- COMMUNITY ---
st.subheader("💬 Community")

with st.form("comment"):
    user = st.text_input("Name")
    text = st.text_area("Comment")
    img = st.file_uploader("Photo")
    post = st.form_submit_button("Post")

if post and text:
    st.session_state.comments.append({"user": user, "text": text, "img": img})

cols = st.columns(3)
for i, c in enumerate(reversed(st.session_state.comments)):
    with cols[i % 3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write(f"**{c['user']}**")
        st.write(c["text"])
        if c["img"]:
            st.image(c["img"])
        st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<hr>
<p style="text-align:center; color:gray;">🌊 Massilia — Explore Marseille like a local</p>
""", unsafe_allow_html=True)
