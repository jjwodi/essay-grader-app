import streamlit as st
import pandas as pd
import re
import time
from groq import Groq

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Essay Assessment System",
    page_icon="📝",
    layout="wide"
)

# --- 1. THE BACKEND ENGINE (From Colab) ---
class ProfessionalGrader:
    def __init__(self, api_key, model):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.weights = {"content": 0.2, "org": 0.4, "conv": 0.4}
        self.penalty = -1
        self.enable_cap = True

    def set_config(self, weights, enable_cap):
        self.weights = weights
        self.enable_cap = enable_cap

    def grade(self, essay_text):
        try:
            prompt = (
                "Grade essay 1-6 in: CONTENT, ORGANIZATION, CONVENTIONS.\n"
                "Format exactly:\n"
                "CONTENT: [Score] | [Reasoning]\n"
                "ORGANIZATION: [Score] | [Reasoning]\n"
                "CONVENTIONS: [Score] | [Reasoning]"
            )
            
            start_time = time.time()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": essay_text}
                ],
                temperature=0
            )
            duration = time.time() - start_time
            usage = response.usage
            
            res = response.choices[0].message.content
            
            # Regex to capture Score AND Reasoning
            patterns = {
                'c': r'CONTENT:\s*(\d+)\s*\|\s*(.*)',
                'o': r'ORGANIZATION:\s*(\d+)\s*\|\s*(.*)',
                'g': r'CONVENTIONS:\s*(\d+)\s*\|\s*(.*)'
            }
            
            data = {}
            for key, pat in patterns.items():
                match = re.search(pat, res)
                if match:
                    data[f'{key}_score'] = int(match.group(1))
                    data[f'{key}_feedback'] = match.group(2).strip()
                else:
                    data[f'{key}_score'] = 3
                    data[f'{key}_feedback'] = "Could not parse feedback."

            # Math Logic
            score = (data['c_score'] * self.weights['content']) + \
                    (data['o_score'] * self.weights['org']) + \
                    (data['g_score'] * self.weights['conv'])
            
            final = int(round(score)) + self.penalty
            
            if self.enable_cap and (data['g_score'] <= 2 or data['o_score'] <= 2):
                final = min(final, 3)

            return {
                "status": "success",
                "final_grade": max(1, min(6, final)),
                "scores": {k: v for k, v in data.items() if 'score' in k},
                "feedback": {k: v for k, v in data.items() if 'feedback' in k},
                "metrics": {"latency": round(duration * 1000), "tokens": usage.total_tokens if usage else 0}
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

# --- 2. THE FRONTEND UI ---
st.title("📝 Automated Essay Assessment System")
st.markdown("### Configurable AI Grading for Application Development")

# SIDEBAR: Configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Key Input (Secure way for demo)
    api_key = st.text_input("Groq API Key", type="password", placeholder="gsk_...")
    
    # Model Selection
    model = st.selectbox("AI Model", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])
    
    st.divider()
    st.subheader("⚖️ Rubric Weights")
    
    # Sliders for Weights (The Lecturer's Request)
    w_c = st.slider("Content", 0.0, 1.0, 0.2, 0.1)
    w_o = st.slider("Organization", 0.0, 1.0, 0.4, 0.1)
    w_g = st.slider("Conventions", 0.0, 1.0, 0.4, 0.1)
    
    if round(w_c + w_o + w_g, 1) != 1.0:
        st.error(f"⚠️ Sum is {w_c+w_o+w_g:.1f}. Must be 1.0!")
    
    enable_cap = st.checkbox("Enable 'Fail Guardrail'", value=True, help="Prevents high scores if grammar is poor.")

# MAIN AREA
if api_key:
    # Initialize the Engine
    grader = ProfessionalGrader(api_key, model)
    grader.set_config({"content": w_c, "org": w_o, "conv": w_g}, enable_cap)
    
    # File Uploader
    uploaded_file = st.file_uploader("Upload Student Essays (CSV)", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} essays.")
        
        if st.button("🚀 Start Assessment"):
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for index, row in df.iterrows():
                status_text.text(f"Grading Essay ID: {row['essay_id']}...")
                
                # Call the Engine
                res = grader.grade(row['full_text'])
                
                if res['status'] == 'success':
                    results.append({
                        "Essay ID": row['essay_id'],
                        "Final Grade": res['final_grade'],
                        "Content": res['scores']['c_score'],
                        "Organization": res['scores']['o_score'],
                        "Conventions": res['scores']['g_score'],
                        "Feedback": res['feedback']['c_feedback'], # Just showing content feedback for brevity
                        "Latency (ms)": res['metrics']['latency']
                    })
                
                progress_bar.progress((index + 1) / len(df))
            
            st.success("✅ Assessment Complete!")
            
            # Show Results Table
            result_df = pd.DataFrame(results)
            st.dataframe(result_df)
            
            # Download Button
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Report Card", csv, "report_card.csv", "text/csv")

else:
    st.warning("👈 Please enter your Groq API Key in the sidebar to begin.")
