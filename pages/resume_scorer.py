import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="Resume Scorer",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 Resume Scorer")
st.markdown("Get a detailed score breakdown of your resume out of 100.")
st.divider()


st.info("AI scores are indicative, not absolute.Use the breakdown and feedback, not just the number.")

resume_text = st.text_area(
    label="Paste your resume here:",
    placeholder="Copy and paste your entire resume text here...",
    height=300
)

job_role = st.text_input(
    label="What job role are you targeting?",
    placeholder="e.g. Data Scientist, Software Engineer, Product Manager"
)

def score_resume(resume, role):
    prompt = f"""
    You are an expert resume evaluator and hiring manager with 15 years of experience.
    
    Score the following resume for a {role} position out of 100.
    
    Resume:
    {resume}
    
    Respond in EXACTLY this format, no extra text:

    OVERALL: [score]/100
    
    BREAKDOWN:
    - Format & Presentation: [score]/20
    - Relevant Skills Match: [score]/25
    - Work Experience & Projects: [score]/25
    - Keywords & ATS Optimization: [score]/20
    - Achievements & Impact: [score]/10
    
    VERDICT:
    2-3 sentences summarizing the resume strength for this role
    
    TOP 3 ACTIONS:
    1. [most important improvement]
    2. [second improvement]
    3. [third improvement]
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


if st.button("Score My Resume", type="primary", use_container_width=True):

    if not resume_text:
        st.error("Please paste your resume text!")
    elif not job_role:
        st.error("Please enter the job role you are targeting!")
    else:
        with st.spinner("AI is scoring your resume..."):
            result = score_resume(resume_text, job_role)

        st.divider()

       ### PARSING 
        lines = result.strip().split("\n")
        
     
        for line in lines:
            if line.startswith("OVERALL:"):
                score_text = line.replace("OVERALL:", "").strip()
                try:
                    score_num = int(score_text.split("/")[0].strip())
                    
                    # Color based on score
                    if score_num >= 80:
                        color = "green"
                    elif score_num >= 60:
                        color = "orange"
                    else:
                        color = "red"
                    
                    st.markdown(
                        f"<h1 style='text-align:center; color:{color};'>"
                        f"{score_num}/100</h1>",
                        unsafe_allow_html=True
                    )
                except:
                    st.markdown(f"## Score: {score_text}")

        st.divider()

  
        st.markdown("## 📊 Full Breakdown")
        st.markdown(result)

        


        st.download_button(
            label=" Download Score Report",
            data=result,
            file_name="resume_score.txt",
            mime="text/plain"
        )

