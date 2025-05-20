import streamlit as st

st.set_page_config(page_title="Autism Toddler Treatment Guide", layout="wide")

st.title("Treatments for Autistic Toddlers")

# Sidebar for Navigation
section = st.sidebar.selectbox("Jump to a Section", [
    "1. Behavioral and Developmental Therapies",
    "2. Speech and Language Therapy",
    "3. Occupational Therapy (OT)",
    "4. Physical Therapy (PT)",
    "5. Sensory Integration Therapy",
    "6. Parent-Mediated Interventions",
    "7. Medication (in Some Cases)",
    "8. Alternative and Complementary Therapies",
    "9. Educational Interventions"
])

# Main Content
if section == "1. Behavioral and Developmental Therapies":
    st.header("1. Behavioral and Developmental Therapies")

    st.subheader("Applied Behavior Analysis (ABA)")
    st.markdown("""
    - Most evidence-based therapy for autism.  
    - Uses positive reinforcement to teach desired behaviors and skills.  
    - Includes programs like **Early Start Denver Model (ESDM)** for toddlers.
    """)

    st.subheader("Developmental, Individual Difference, Relationship-Based (DIR/Floortime)")
    st.markdown("""
    - Focuses on emotional and relational development.  
    - Encourages learning through play and relationship-building.
    """)

    st.subheader("Early Intervention Programs (IDEA Part C in the U.S.)")
    st.markdown("""
    - Government-supported programs offering therapies at home or centers.  
    - Involve **speech**, **occupational**, and **behavioral therapy**.
    """)

elif section == "2. Speech and Language Therapy":
    st.header("2. Speech and Language Therapy")
    st.markdown("""
    - Helps children improve verbal and non-verbal communication.  
    - Focuses on:  
      • Understanding spoken language  
      • Using words or signs to express needs  
      • Developing social communication
    """)

elif section == "3. Occupational Therapy (OT)":
    st.header("3. Occupational Therapy (OT)")
    st.markdown("""
    - Aims to improve:  
      • Fine motor skills  
      • Daily living activities (e.g., feeding, dressing)  
      • Sensory processing issues
    """)

elif section == "4. Physical Therapy (PT)":
    st.header("4. Physical Therapy (PT)")
    st.markdown("""
    - Helps with:  
      • Gross motor skills (walking, balance)  
      • Coordination and posture
    """)

elif section == "5. Sensory Integration Therapy":
    st.header("5. Sensory Integration Therapy")
    st.markdown("""
    - For children who are hypersensitive or hyposensitive to sensory input.  
    - Uses structured activities to help them respond more appropriately.
    """)

elif section == "6. Parent-Mediated Interventions":
    st.header("6. Parent-Mediated Interventions")
    st.markdown("""
    - Parents are trained to use strategies at home.  
    - Examples: **Pivotal Response Training (PRT)**, **Hanen Program**
    """)

elif section == "7. Medication (in Some Cases)":
    st.header("7. Medication (in Some Cases)")
    st.markdown("""
    - Not for autism itself, but for associated symptoms like:  
      • Hyperactivity  
      • Aggression  
      • Anxiety  
      • Sleep problems  
    - Should be used under **pediatrician or child psychiatrist** supervision.
    """)

elif section == "8. Alternative and Complementary Therapies":
    st.header("8. Alternative and Complementary Therapies")
    st.markdown("""
    - Must be used with caution.  
    - Examples:  
      • Dietary changes (gluten-free/casein-free)  
      • Music therapy  
      • Animal therapy  
    - **Evidence varies**, always consult healthcare professionals.
    """)

elif section == "9. Educational Interventions":
    st.header("9. Educational Interventions")
    st.markdown("""
    - Structured preschool programs with:  
      • Low student-to-teacher ratio  
      • Visual supports  
      • Individualized instruction
    """)
    st.image(r'static/images/strategies-for-asd-support-w1300.png', caption="Strategies for ASD Support")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Developed with ❤️ using Streamlit by Code-Craft")