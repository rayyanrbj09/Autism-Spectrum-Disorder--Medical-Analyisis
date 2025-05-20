import streamlit as st
from config import image1, image2


st.set_page_config(page_title="About", layout="centered")
st.markdown(
    """
    <style>
    .stApp {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 18px;
    }
    h1 {
        font-family: 'Trebuchet MS', Arial, sans-serif;
        color: white;
        font-size: 2.5em;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("About the Autism Spectrum Disorder (ASD)")

st.video(r'https://www.youtube.com/watch?v=TJuwhCIQQTs', start_time=0)
st.write("""
Autism spectrum disorder is a neurological and developmental disorder that affects how people interact with others, communicate, learn, and behave. Although autism can be diagnosed at any age, it is described as a “developmental disorder” because symptoms generally appear in the first two years of life.
""")

with st.expander("**What is Autism Spectrum Disorder?**"):
    st.write("""
    Autism spectrum disorder (ASD) is a complex neurodevelopmental disorder characterized by a range of symptoms and challenges in social interaction, communication, and behavior. The term "spectrum" reflects the wide variation in challenges and strengths possessed by each person with autism. Some individuals may have significant challenges, while others may be highly skilled in certain areas.
    """)
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, use_container_width=True, width=400, caption="Autism Spectrum Disorder - Inforgraphics : Common Signs. \n Visual Summary ")
    with col2:
        st.image(image2, use_container_width=True, width=400)
    st.markdown("---")

with st.expander("**Signs and Symptoms**"):
    st.write("""
    The signs and symptoms of autism can vary widely, but they generally fall into two main categories:
    Autism spectrum disorder (ASD) can present with a wide range of signs and symptoms, including difficulties with social interaction, communication, and repetitive behaviors. Individuals with ASD may experience sensory sensitivities, intense focus on specific interests, and emotional regulation challenges.
    """)


st.markdown("**Social Communication Challenges**")
st.write("- Difficulty in understanding social cues, such as body language and tone of voice.")

with st.expander("**Cures and Treatments**"):
    st.write("""
    There is no known cure for autism, but early intervention and tailored therapies can significantly improve outcomes. Treatments may include behavioral therapy, speech therapy, occupational therapy, and educational support. Medications may also be prescribed to manage specific symptoms or co-occurring conditions.
    """)

st.sidebar.info("Developed with ❤️ using Streamlit by Code-Craft")