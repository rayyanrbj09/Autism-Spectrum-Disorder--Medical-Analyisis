import streamlit as st

st.set_page_config(page_title="Analysis", layout="centered")
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
st.title("Analysis of Autism Spectrum Disorder")

st.markdown("""
- From the Charts that was generated the insgihts found useful are
---------------
**12-18 Months**:
- Predominantly light yellow cells (scores around -4 to -15) suggest lower QCHAT-10 scores, indicating fewer or less pronounced ASD traits. This aligns with the idea that autism symptoms may be subtler or harder to detect in younger toddlers.
---------------
**18-24 Months**:
- A transition zone with more orange hues (-15 to -25), reflecting an increase in higher QCHAT-10 scores. This age range is a critical window for autism screening, as many diagnostic signs (e.g., social communication delays) become more apparent.a
---------------
**24-36 Months**:
- Darker red cells (-30 to -45) dominate, indicating a higher prevalence of elevated QCHAT-10 scores. This could suggest that ASD traits are more detectable or severe in this age group, consistent with developmental progression and increased screening sensitivity.
""")

with st.expander("**Charts**"):
    st.write('Heatmap of QCHAT-10 Scores')
    st.image(r'static/images/output.png', use_container_width=True)
    st.markdown("---")
    st.write('Asd vs Non-Asd Traits of Family Members')
    st.image(r'static/images/output2.png', use_container_width=True)
    st.markdown("---")
    st.write('Asd and Ethnicity Comparison')
    st.image(r'static/images/output4.png', use_container_width=True)

st.sidebar.info("Developed with ❤️ using Streamlit by Code-Craft")