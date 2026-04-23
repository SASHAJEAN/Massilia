import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Massilia", layout="wide")

# Sample dataset
data = [
    {"name": "Bar du Port", "lat": 43.2965, "lon": 5.3698, "price": 5, "specialty": "Pastis"},
    {"name": "Chez Panisse", "lat": 43.2950, "lon": 5.3740, "price": 8, "specialty": "Panisse"},
    {"name": "Fougasse House", "lat": 43.3000, "lon": 5.3700, "price": 6, "specialty": "Fougasse"},
    {"name": "Le Vieux Marseille", "lat": 43.2970, "lon": 5.3725, "price": 7, "specialty": "Pastis"},
]

df = pd.DataFrame(data)

# Session state for community
if "comments" not in st.session_state:
    st.session_state.comments = []

st.title("🍋 Massilia")

# --- FORM ---
st.header("Find your perfect spot")
with st.form("preferences"):
    budget = st.slider("Budget (€)", 1, 15, 7)
    specialty = st.selectbox("Specialty", ["Pastis", "Panisse", "Fougasse"])
    mood = st.selectbox("Mood", ["Chill", "Party", "Authentic"])
    submitted = st.form_submit_button("Search")

# Filter results
if submitted:
    filtered = df[(df["price"] <= budget) & (df["specialty"] == specialty)]
else:
    filtered = df

# --- MAP ---
st.header("📍 Map of Marseille")
m = folium.Map(location=[43.2965, 5.3698], zoom_start=13)

for _, row in filtered.iterrows():
    color = "green" if row["price"] <= budget else "red"
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"{row['name']} - €{row['price']} ({row['specialty']})",
        icon=folium.Icon(color=color),
    ).add_to(m)

st_folium(m, width=700, height=500)

# --- RESULTS TABLE ---
st.subheader("Best Matches")
st.dataframe(filtered)

# --- COMMUNITY ---
st.header("💬 Community")

with st.form("comment_form"):
    username = st.text_input("Your name")
    comment = st.text_area("Your comment")
    photo = st.file_uploader("Upload a photo", type=["jpg", "png"])
    post = st.form_submit_button("Post")

if post and comment:
    st.session_state.comments.append(
        {"user": username, "comment": comment, "photo": photo}
    )

# Display comments
for c in reversed(st.session_state.comments):
    st.write(f"**{c['user']}**: {c['comment']}")
    if c["photo"]:
        st.image(c["photo"], width=200)
