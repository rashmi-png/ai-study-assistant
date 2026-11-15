import streamlit as st
from google import genai
from pypdf import PdfReader

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
MODEL = "gemini-3.5-flash-lite"
PROMPTS = {
    "Summary": "Summarize these study notes in simple bullet points:",
    "Quiz": "Create 5 multiple-choice questions from these study notes. Give 4 options (A-D) for each question, and list the correct answers at the end:",
    "Flashcards": "Create 8 flashcards from these study notes. Format each one as 'Q: ...' and 'A: ...':",
    "Ask a Question": "Answer the student's question using only these study notes. If the answer is not in the notes, say so.",
}

st.title("AI Study Assistant")
st.write("Upload a PDF or paste your notes, then choose what you want.")

mode = st.radio("What do you want to do?", list(PROMPTS.keys()), horizontal=True)
pdf_file = st.file_uploader("Upload a PDF", type="pdf")
notes = st.text_area("Or paste your notes", height=200)

question = ""
if mode == "Ask a Question":
    question = st.text_input("Type your question")

if st.button("Generate"):
    text = ""
    if pdf_file is not None:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
    else:
        text = notes

    if text.strip() == "":
        st.warning("Please upload a PDF or paste some notes first.")
    elif mode == "Ask a Question" and question.strip() == "":
        st.warning("Please type your question.")
    else:
        prompt = PROMPTS[mode] + "\n\n"
        if mode == "Ask a Question":
            prompt += "Question: " + question + "\n\n"
        prompt += "Notes:\n" + text

        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )
        st.write(response.text)