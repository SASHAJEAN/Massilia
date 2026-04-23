import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

st.set_page_config(page_title="Massilia", layout="wide")

# --- STYLE ---
st.markdown("""
<style>
body { background-color:#f4efe6; }

/* NAVBAR */
.navbar {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:10px 20px;
}
.logo img { height:40px; }

/* HERO */
.hero {
    background: linear-gradient(135deg,#1e88e5,#42a5f5);
    padding:50px;
    border-radius:25px;
    color:white;
    margin-bottom:20px;
}

/* CARD */
.card {
    background:white;
    border-radius:20px;
    padding:15px;
    box-shadow:0px 5px 20px rgba(0,0,0,0.08);
    margin-bottom:20px;
}
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

/* LIKE */
.like {
    color:#e91e63;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# --- NAVBAR ---
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.markdown(f"""
    <div class="navbar">
        <div class="logo"><img src="data:image/png;base64,{st.image(logo_path)._repr_html_()}"></div>
        <div style="background:#ff9800;color:white;padding:8px 15px;border-radius:10px;">Get Started</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<h2>🍋 Massilia</h2>", unsafe_allow_html=True)

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

# --- SESSION STATE ---
if "comments" not in st.session_state:
    st.session_state.comments = []
if "likes" not in st.session_state:
    st.session_state.likes = {}
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# --- HERO ---
st.markdown("""
<div class="hero">
<h1>Pas fâché avec <span style="color:#ffeb3b;">le plaisir</span></h1>
<p>Find the best Marseille spots with deals & community tips.</p>
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
            popup=f"{row['name']} (€{row['price']})"
        ).add_to(m)
    st_folium(m, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

# FILTER PANEL
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("filter"):
        specialty = st.selectbox("Specialty", ["Pastis", "Panisse", "Fougasse"])
        budget = st.slider("Budget", 1, 15, 7)
        submitted = st.form_submit_button("Apply")
    st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    df = df[(df["specialty"] == specialty) & (df["price"] <= budget)]

# --- CARDS ---
st.subheader("🔥 Best Spots")
cols = st.columns(3)

for i, row in df.iterrows():
    key = row["name"]

    if key not in st.session_state.likes:
        st.session_state.likes[key] = 0

    with cols[i % 3]:
        st.markdown(f"""
        <div class="card">
            <img src="{row['img']}"/>
            <h4>{row['name']}</h4>
            <p>{row['specialty']} • €{row['price']}</p>
            <span class="badge">{row['deal']}</span>
        </div>
        """, unsafe_allow_html=True)

        colA, colB = st.columns(2)

        with colA:
            if st.button(f"❤️ {st.session_state.likes[key]}", key=f"like_{key}"):
                st.session_state.likes[key] += 1

        with colB:
            if st.button("⭐ Save", key=f"fav_{key}"):
                if key not in st.session_state.favorites:
                    st.session_state.favorites.append(key)

# --- FAVORITES ---
if st.session_state.favorites:
    st.subheader("⭐ Your Favorites")
    st.write(", ".join(st.session_state.favorites))

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

# --- FOOTER ---
st.markdown("""
<hr>
<p style="text-align:center;color:gray;">🌊 Massilia — Explore Marseille like a local</p>
""", unsafe_allow_html=True)
