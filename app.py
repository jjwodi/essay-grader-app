import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Essay Grader",
    page_icon="📝",
    layout="wide"
)

# --- HEADER ---
st.title("📝 Automated Essay Assessment System")
st.markdown("""
**Prototype v1.0** | Built for [Your Module Name]  
*Adjust the weights below to manage the assessment logic.*
""")

# --- SIDEBAR (The "Control Panel") ---
with st.sidebar:
    st.header("⚙️ Configuration")
    model_choice = st.selectbox("Select AI Model", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])
    st.divider()
    
    st.subheader("Rubric Weights")
    w_content = st.slider("Content Weight", 0.0, 1.0, 0.4)
    w_org = st.slider("Organization Weight", 0.0, 1.0, 0.3)
    w_conv = st.slider("Conventions Weight", 0.0, 1.0, 0.3)
    
    # Validation Check
    total = w_content + w_org + w_conv
    if total != 1.0:
        st.error(f"⚠️ Weights sum to {total:.1f}. They must equal 1.0!")
    else:
        st.success("✅ Weights Balanced")

# --- MAIN AREA ---
st.info("👈 Upload a CSV file in the sidebar or adjust settings to start.")