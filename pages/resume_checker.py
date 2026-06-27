import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
import tempfile
import pdfplumber

## LOAD API KEY

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(
    page_title="Resume Checker",
    layout="centered"
)

st.title("Resume Checker")
st.markdown("Paste your resume below and get instant AI-powered feedback.")
st.divider()
###divider creates a horizontal line across the page,
#seperates sections visually

def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read()) ### saves to disk first
        tmp_path = tmp.name ###get its path
    
    text = ""
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    os.unlink(tmp_path)  # delete temp file after reading
    return text.strip()

uploaded_file=st.file_uploader(
    "Upload resume PDF",
    type=["pdf"]
)
if uploaded_file:
    resume_text=extract_text_from_pdf(uploaded_file)
    st.success(f"Resume loaded-{len(resume_text)} characters extracted")
else:
    resume_text=st.text_area(
        #big tall box for large text(whole resume)
        #user types-get saved into resume_text
        label="Paste your resume here:",
        placeholder="Copy and paste your entire resume text here..",
        height=300

    )
job_role=st.text_input(
    #small single line box for short text
    #user types get saved into job role
    label="What job role are you applying for?",
    placeholder="e.g.Software Engineer, Data Analyst, Product Manager"
)


### MAIN FUNCTION

def resume_checker(resume,role):
    prompt= f"""
    You are an expert resume reviewer with 15 years of HR experience.
    Analyse the following resume for the {role} role,

    Resume: {resume}

    ## STRENGTHS
    Identify and explain 3-4 strong points about the resume 
    
    ##WEAKNESSES
    Identify and explin 3-4 missing points or improvements that could be done in the resume

    ##MISSING KEYWORDS
    Explain what are the missing keywords or skills required for the {role} role

    ##PRIORITIES
    Explain in the priority order,
    1.what should be the first and foremost thing to improve
    2. the second most important thing to improve
    3. other optional improvements

    ##VERDICT
    Summarise the resume for its current state and fit for {role} role
    """

    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

if st.button("🔍 Check My Resume", type="primary", use_container_width=True):
    if not resume_text:
        st.error("Please paste your resume text!")
    elif not job_role:
        st.error("Please enter the job role you're applying for!")
    else:
        with st.spinner("AI is analysing your resume..."):
            result=resume_checker(resume_text,job_role)

        st.divider()
        st.markdown("## Your Resume Analysis")
        st.markdown(result)

        st.download_button(
            label="Download Analysis",
            data=result,
            file_name="resume-analysis.txt",
            mime="text/plain"
            #mime means multipurpose Internet mail extensions
            #tells the browser that this file is plain text, open it accordingly

        )
