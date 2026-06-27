import streamlit as st
from google import genai
import os
import tempfile
import pdfplumber
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


st.set_page_config(
    page_title="AI Career Coach",
   
    layout="centered"
)

st.title(" AI Career Coach")
st.markdown("Upload your resume and ask me anything about your career.")
st.info(" I remember your conversation -You can ask follow up Questions !")
st.divider()


def extract_text_from_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    text = ""
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    os.unlink(tmp_path)
    return text.strip()


# Streamlit reruns your ENTIRE script from top to bottom
# every single time the user does anything —
# clicks a button, types a message, uploads a file

# So without session_state this happens:
#messages = []   # ← resets to empty EVERY rerun
                # chat history wiped after every message!


if "messages" not in st.session_state:
    st.session_state.messages = []

if "resume_context" not in st.session_state:
    st.session_state.resume_context = None


#Without this — every time the user typed a message, the page reruns and the resume text would disappear!

uploaded_file = st.file_uploader(
    "Upload your resume PDF ",
    type=["pdf"]
)

if uploaded_file:
    st.session_state.resume_context = extract_text_from_pdf(uploaded_file)
    st.success(" Resume loaded — I'll use it to personalise my advice!")

st.divider()

def ask_coach(question, history, resume):

   
    resume_section = ""
    if resume:
        resume_section = f"""
        
        Resume:
        {resume}
        """

    # Build conversation history
    history_text = ""
    for msg in history:
        if msg["role"] == "user":
            history_text += f"User: {msg['content']}\n"
        else:
            history_text += f"Coach: {msg['content']}\n"

    prompt = f"""
    You are an expert AI career coach with 20 years of experience
    in tech hiring, resume writing, interview preparation, and
    career development in the Indian and global tech industry.

    You are warm, honest, encouraging and give specific actionable advice.
    You never give vague answers — always give concrete next steps.
    Keep responses short  and easy to read.

    {resume_section}

    Previous conversation:
    {history_text}

    User's question: {question}

    Answer as a supportive career coach:
    """

    return prompt


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your career coach anything..."):

    # save and show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # build prompt and get response
    full_prompt = ask_coach(prompt, st.session_state.messages, st.session_state.resume_context)

    with st.spinner("Coach is thinking..."):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        full_response = response.text

    # show and save coach response
    with st.chat_message("assistant"):
        st.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# ─── CLEAR CHAT ────────────────────────────────────────
if st.session_state.messages: #only show if chat exists
    if st.button(" Clear Conversation"):
        st.session_state.messages = []
        st.session_state.resume_context = None
        st.rerun()