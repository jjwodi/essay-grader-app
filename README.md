# 📝 AI Essay Assessment System

**Student Name:** [Your Name]  
**Project:** Automated Essay Scoring with Multi-Trait Feedback  
**Live Demo:** [Paste your Streamlit App Link Here]

## 📌 Project Overview
This tool automates essay grading using the Llama 3 and Groq API. It goes beyond simple scoring by providing:
1.  **Multi-Trait Analysis:** Grades separately on Content, Organization, and Conventions.
2.  **Qualitative Feedback:** Generates specific text feedback for each criteria.
3.  **Configurable Logic:** Allows teachers to adjust rubric weights via the UI.

## 📂 File Structure
* `app.py`: The main application code containing the `ProfessionalGrader` class and Streamlit UI logic.
* `requirements.txt`: Python dependencies required to run the app.
* `sample_100.csv`: A dataset of 100 anonymized student essays for testing the batch processing feature.

## 🚀 How to Run Locally
1.  Clone the repository.
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the app: `streamlit run app.py`