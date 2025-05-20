import streamlit as st
# App configuration
st.set_page_config(page_title="Toddler Parenting Support", layout="centered")
st.markdown(
    """
    <style>
    /* Change font for the whole app */
    .stApp {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 18px;
    }
    /* Change font and color for h1 (title) */
    h1 {
        font-family: 'Trebuchet MS', Arial, sans-serif;
        color: white;
        font-size: 2.5em;
        font-weight: bold;
        text-shadow:
            0 0 10px rgba(255,255,255,0.8),
            0 0 20px rgba(255,215,0,0.7),
            0 0 30px rgba(0,255,255,0.6),
            0 0 40px rgba(255,255,255,0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("👶 Toddler Parenting Support")
st.markdown("### 💖 Gentle, Practical Tips for Your Toddler’s Growth")

st.markdown("Parenting a toddler can be challenging — but you're not alone! Here's a friendly, informative guide to help you build healthy habits and nurture your child’s development.")

st.image(r'static/images/support.jpg')
# 1. Emotional Growth & Play
st.header("🎈 Emotional Development & Play")
with st.expander("Why Play Matters"):
    st.markdown("""
    - Encourages imagination and problem-solving.
    - Helps build trust and emotional security.
    - Develops social skills like sharing and empathy.
    """)

st.markdown("""
**Tips for Parents:**
- Create a safe space to explore and play.
- Allow free play time daily — even 30 mins is great!
- Join their play and follow their lead.
""")

# 2. Nutrition & Eating Habits
st.header("🥦 Healthy Eating Habits")
with st.expander("Balanced Diet for Toddlers"):
    st.markdown("""
    - Include fruits, vegetables, grains, and proteins.
    - Avoid junk food, sugary drinks, and excess salt.
    - Respect hunger cues — don’t force meals.
    """)

st.markdown("""
**Tips for Parents:**
- Eat together as a family.
- Make food colorful and fun (e.g., fruit smiley faces).
- Keep meal and snack times regular.
""")

# 3. Sleep Routine
st.header("🌙 Sleep Schedule")
with st.expander("Why Sleep Is Crucial"):
    st.markdown("""
    - Supports brain growth and emotional balance.
    - Reduces tantrums and improves focus.
    - Toddlers need **11–14 hours** of sleep (including naps).
    """)

st.markdown("""
**Tips for Parents:**
- Maintain a calm and consistent bedtime routine.
- Avoid screen time at least 1 hour before sleep.
- Use dim lighting and read bedtime stories.
""")

# 4. Language & Learning
st.header("📚 Early Learning & Talking")
with st.expander("Language Boosters"):
    st.markdown("""
    - Talk to them about everyday things.
    - Ask questions and wait for their answers.
    - Read daily, even if it’s the same story again!
    """)

st.markdown("""
**Tips for Parents:**
- Name objects around them (“This is a ball!”).
- Repeat words and encourage speech attempts.
- Let them explore books, textures, and sounds.
""")

# 5. For You, Dear Parent
st.header("🫶 Support for You")
with st.expander("You're Not Alone ❤️"):
    st.markdown("""
    - It’s okay to feel tired or overwhelmed.
    - Talk to your partner, family, or other parents.
    - Celebrate small wins. You are doing amazing!
    """)

# Footer
st.markdown("---")
st.markdown("✨ Made with love in Streamlit")

st.sidebar.info("Developed with ❤️ using Streamlit by Code-Craft")
