import streamlit as st

st.set_page_config(
    page_title="Resume Genie",
   
    layout="centered"
)


st.markdown("""
<h1 style='text-align: center;'> Resume Genie</h1>
<p style='text-align: center; font-size: 18px; color: gray;'>
Your AI-powered career assistant
</p>
""", unsafe_allow_html=True)

st.divider()

#INTRODUCTION

st.markdown("""
###  Welcome!
Resume Genie helps you land your dream job using the power of AI.
Choose a tool below to get started
""")

st.divider()


col1, col2 = st.columns(2)

with col1:
    st.markdown("###  Resume Checker")
    st.markdown("Get detailed AI feedback on your resume — strengths, weaknesses, missing keywords and priorities.")
    if st.button("Open Resume Checker →", use_container_width=True):
        st.switch_page("pages/resume_checker.py")

    st.markdown("---")

    st.markdown("###  Cover Letter Generator")
    st.markdown("Generate a personalised cover letter tailored to any job description in seconds.")
    if st.button("Open Cover Letter Generator →", use_container_width=True):
        st.switch_page("pages/cover_letter_generator.py")

with col2:
    st.markdown("###  Resume Scorer")
    st.markdown("Get a score out of 100 with a detailed breakdown of exactly where your resume stands.")
    if st.button("Open Resume Scorer →", use_container_width=True):
        st.switch_page("pages/resume_scorer.py")

    st.markdown("---")

    st.markdown("###  AI Career Coach")
    st.markdown("Chat with an AI career coach. Upload your resume and ask anything about your job search.")
    if st.button("Open AI Career Coach →", use_container_width=True):
        st.switch_page("pages/ai_career_coach.py")



st.divider()
st.caption("Built with Gemini AI + Streamlit | Made by Erika Mediratta")