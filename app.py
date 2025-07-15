import streamlit as st
from openai import OpenAI
from docx import Document
from fpdf import FPDF
import io

st.set_page_config(page_title="JobFit Copilot", layout="centered")
st.title("🎯 JobFit Copilot")
st.write("Generate tailored resumes and cover letters using AI.")

openai_api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

resume = st.text_area("📄 Paste your Master Resume here:", height=300)
job_description = st.text_area("💼 Paste the Job Description here:", height=300)

client = None
if openai_api_key:
    client = OpenAI(api_key=openai_api_key)

def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )
    return response.choices[0].message.content

def download_buttons(content, filename_prefix):
    # TXT
    st.download_button(
        label="⬇️ Download as .txt",
        data=content,
        file_name=f"{filename_prefix}.txt",
        mime="text/plain"
    )
    
    # DOCX
    doc = Document()
    for line in content.split("\n"):
        doc.add_paragraph(line)
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    st.download_button(
        label="⬇️ Download as .docx",
        data=doc_io,
        file_name=f"{filename_prefix}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_io = io.BytesIO()
    pdf.output(pdf_io)
    pdf_io.seek(0)
    st.download_button(
        label="⬇️ Download as .pdf",
        data=pdf_io,
        file_name=f"{filename_prefix}.pdf",
        mime="application/pdf"
    )

if st.button("🎯 Generate Tailored Resume"):
    if not (resume and job_description and openai_api_key):
        st.warning("Please fill out all fields.")
    else:
        with st.spinner("Generating tailored resume..."):
            prompt = f"""You are a job application expert. Take the resume below and tailor it specifically for the job description provided.

Return a customized, ATS-friendly resume that matches the job role with improved bullet points and optimized phrasing. Convert any professional summary paragraph into bullet points.

Master Resume:
{resume}

Job Description:
{job_description}
"""
            tailored_resume = generate_response(prompt)
            st.subheader("✅ Tailored Resume")
            st.text_area("Result:", tailored_resume, height=300)
            download_buttons(tailored_resume, "tailored_resume")

if st.button("✉️ Generate Cover Letter"):
    if not (resume and job_description and openai_api_key):
        st.warning("Please fill out all fields.")
    else:
        with st.spinner("Generating cover letter..."):
            prompt = f"""You are a professional cover letter writer. Write a tailored, engaging cover letter based on the resume and job description below.

Use a human tone, highlight key experiences, and keep it concise (under 300 words). Return only the letter.

Master Resume:
{resume}

Job Description:
{job_description}
"""
            cover_letter = generate_response(prompt)
            st.subheader("✅ Tailored Cover Letter")
            st.text_area("Result:", cover_letter, height=300)
            download_buttons(cover_letter, "cover_letter")
