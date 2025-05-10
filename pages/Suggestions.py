import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests

st.set_page_config(page_title="Toddler Support", page_icon="👶", layout="centered")

# Load Lottie Animations from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load animation assets
lottie_play = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_tutvdkg0.json")
lottie_food = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_RHBBwK.json")
lottie_sleep = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_mKkKJj.json")
lottie_read = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_3vbOcw.json")

# Title
st.title("👶 Healthy Parenting: Toddler Tips & Support")

st.markdown("### 💡 Suggestions for Parents")
st.write("Your toddler's growth depends on **love**, **routine**, and **interaction**. Here's how you can help them thrive:")

# PLAY & EMOTIONAL DEVELOPMENT
with st.container():
    st.subheader("🎈 Encourage Play & Emotional Growth")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        - Let them explore freely (supervised).
        - Respond to their emotions with patience.
        - Talk and name feelings ("I see you're sad", "That made you happy").
        - Create a loving and secure environment.
        """)
    with col2:
        st_lottie(lottie_play, height=150, key="play")

# NUTRITION & MEALS
with st.container():
    st.subheader("🥗 Provide Balanced Nutrition")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(lottie_food, height=150, key="food")
    with col2:
        st.markdown("""
        - Offer fruits, vegetables, whole grains.
        - Avoid sugary drinks and processed snacks.
        - Keep mealtime relaxed and interactive.
        - Respect toddler's appetite — don’t force-feed.
        """)

# SLEEP ROUTINE
with st.container():
    st.subheader("🌙 Build a Healthy Sleep Routine")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        - Maintain a fixed bedtime and wake-up time.
        - No screens 1 hour before sleep.
        - Use bedtime stories and cuddles to calm them.
        - Toddlers need 11–14 hours of sleep/day (including naps).
        """)
    with col2:
        st_lottie(lottie_sleep, height=150, key="sleep")

# LEARNING THROUGH READING
with st.container():
    st.subheader("📚 Read & Talk Daily")
    col1, col2 = st.columns([1, 2])
    with col1:
        st_lottie(lottie_read, height=150, key="read")
    with col2:
        st.markdown("""
        - Read books with pictures and simple words.
        - Point to things and say their names aloud.
        - Let them turn pages and interact with books.
        - Talk to them even if they don’t fully respond.
        """)

# Additional Support
st.markdown("### 💖 Emotional Support for Parents")
st.info("""
You're doing great! Every toddler is unique. Stay consistent, trust your instincts, and don’t hesitate to ask for help from pediatricians or parenting groups.
""")

st.markdown("#### 🙌 Stay Strong, Stay Loving!")

# Optional: Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | [LottieFiles](https://lottiefiles.com) for animations")
