import streamlit as st
from google import genai
import os
import pdfplumber
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


st.set_page_config(
    page_title="Cover Letter Generator",
   
    layout="centered"
)

st.title("Cover Letter Generator")
st.markdown("Upload your resume + paste the job description → get a tailored cover letter instantly.")
st.info(" The cover letter is tailored specifically to the job description and company.")
st.divider()


def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

### text.strip() removes any accidental space or blank lines at the very start and end of the whole text


col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input(
        label="Company name:",
        placeholder="e.g. Google, Microsoft, Startup XYZ"
    )

with col2:
    tone = st.selectbox(
        label="Tone of the letter:",
        options=["Professional", "Enthusiastic", "Concise", "Creative"]
    )

st.divider()


left, right = st.columns(2)

with left:
    st.markdown("###  Your Resume")
    uploaded_file = st.file_uploader(
        "Upload resume PDF",
        type=["pdf"]
    )
   
    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        st.success(f" Resume loaded — {len(resume_text)} characters extracted")
        with st.expander("Preview extracted text"):
            st.text(resume_text[:500] + "...")
    else:
        resume_text = st.text_area(
            label="Or paste resume text manually:",
            placeholder="Copy and paste your resume here...",
            height=300
        )

with right:
    st.markdown("### Job Description")
    job_description = st.text_area(
        label="Paste the full job description:",
        placeholder="Copy and paste the job description here...",
        height=300
    )

st.divider()

def generate_cover_letter(resume, job_desc, company, tone):
    prompt = f"""
    You are an expert career coach and professional writer.
    
    Write a compelling cover letter for this candidate applying to {company}.
    
    Tone: {tone}
    
    Candidate Resume:
    {resume}
    
    Job Description:
    {job_desc}
    
    Instructions:
    - Start with a strong opening that immediately shows value
    - Match specific skills from resume to requirements in job description
    - Show genuine enthusiasm for {company} specifically  
    - Include 1-2 quantified achievements from their resume
    - End with a confident call to action
    - Keep it to 3-4 paragraphs, under 350 words
    - Do NOT use generic phrases like "I am writing to apply for"
    - Write like a human, not a list of achievements
    - Make it sound personal and specific, not like a template
    
    Write the cover letter now:
    """
    
    response = client.models.generate_content(      # ← actually calls Gemini
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text  


if st.button("✉️ Generate Cover Letter", type="primary", use_container_width=True):

    if not resume_text:
        st.error("Please upload your resume PDF or paste resume text!")
    elif not job_description:
        st.error("Please paste the job description!")
    elif not company_name:
        st.error("Please enter the company name!")
    else:
        with st.spinner("Writing your cover letter..."):
            result = generate_cover_letter(
                resume_text,
                job_description,
                company_name,
                tone
            )

        st.divider()
        st.markdown("## ✉️ Your Cover Letter")

        st.text_area(
            label="Copy your cover letter:",
            value=result,
            height=400
        )

        st.download_button(
            label="📥 Download Cover Letter",
            data=result,
            file_name=f"cover_letter_{company_name}.txt",
            mime="text/plain"
        )