import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Massilia", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
body {
    background-color: #f4efe6;
}
.main {
    background-color: #f4efe6;
}
h1, h2, h3 {
    color: #1e88e5;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.hero {
    background: linear-gradient(135deg, #1e88e5, #42a5f5);
    padding: 40px;
    border-radius: 25px;
    color: white;
}
.button-primary {
    background-color: #ff9800;
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    border: none;
}
.highlight {
    color: #ff9800;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Sample dataset
data = [
    {"name": "Bar du Port", "lat": 43.2965, "lon": 5.3698, "price": 5, "specialty": "Pastis"},
    {"name": "Chez Panisse", "lat": 43.2950, "lon": 5.3740, "price": 8, "specialty": "Panisse"},
    {"name": "Fougasse House", "lat": 43.3000, "lon": 5.3700, "price": 6, "specialty": "Fougasse"},
    {"name": "Le Vieux Marseille", "lat": 43.2970, "lon": 5.3725, "price": 7, "specialty": "Pastis"},
]

df = pd.DataFrame(data)

# Session state
if "comments" not in st.session_state:
    st.session_state.comments = []

# --- HERO ---
st.markdown("""
<div class="hero">
    <h1>🍋 Pas fâché avec <span class="highlight">le plaisir</span> !</h1>
    <p>Find the best spots in Marseille for Pastis, Panisse & more.</p>
</div>
""", unsafe_allow_html=True)

# --- FORM ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🎯 Find your perfect spot")

with st.form("preferences"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        budget = st.slider("Budget (€)", 1, 15, 7)
    with col2:
        specialty = st.selectbox("Specialty", ["Pastis", "Panisse", "Fougasse"])
    with col3:
        mood = st.selectbox("Mood", ["Chill", "Party", "Authentic"])

    submitted = st.form_submit_button("Search")

st.markdown('</div>', unsafe_allow_html=True)

# Filter
if submitted:
    filtered = df[(df["price"] <= budget) & (df["specialty"] == specialty)]
else:
    filtered = df

# --- MAP + RESULTS ---
col1, col2 = st.columns([2,1])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📍 Map of Marseille")

    m = folium.Map(location=[43.2965, 5.3698], zoom_start=13)

    for _, row in filtered.iterrows():
        color = "green" if row["price"] <= budget else "red"
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"{row['name']} - €{row['price']} ({row['specialty']})",
            icon=folium.Icon(color=color),
        ).add_to(m)

    st_folium(m, width=700, height=450)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💰 Best Deals")
    st.dataframe(filtered)
    st.markdown('</div>', unsafe_allow_html=True)

# --- COMMUNITY ---
st.markdown("## 💬 Join the Community")

st.markdown('<div class="card">', unsafe_allow_html=True)
with st.form("comment_form"):
    username = st.text_input("Your name")
    comment = st.text_area("Share your experience")
    photo = st.file_uploader("Upload a photo", type=["jpg", "png"])
    post = st.form_submit_button("Post")

if post and comment:
    st.session_state.comments.append(
        {"user": username, "comment": comment, "photo": photo}
    )
st.markdown('</div>', unsafe_allow_html=True)

# Display comments
for c in reversed(st.session_state.comments):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"**{c['user']}**")
    st.write(c["comment"])
    if c["photo"]:
        st.image(c["photo"])
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<hr>
<p style="text-align:center; color:gray;">Made with ☀️ in Marseille</p>
""", unsafe_allow_html=True)
