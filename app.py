import streamlit as st
from io import BytesIO
from docx import Document
from fpdf import FPDF
from openai import OpenAI

# Streamlit UI setup
st.set_page_config(page_title="JobFit Copilot", layout="centered")
st.title("🎯 JobFit Copilot")
st.write("Generate tailored resumes and cover letters using AI.")

# Input fields
openai_api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")
resume = st.text_area("📄 Paste your Master Resume here:", height=300)
job_description = st.text_area("💼 Paste the Job Description here:", height=300)

# Helper functions to create different file formats
def create_docx(text):
    doc = Document()
    for line in text.split('\n'):
        doc.add_paragraph(line)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# API client
client = OpenAI(api_key=openai_api_key) if openai_api_key else None

# Generate Tailored Resume
if st.button("🎯 Generate Tailored Resume"):
    if not (resume and job_description and openai_api_key):
        st.warning("Please fill out all fields.")
    else:
        with st.spinner("Generating tailored resume..."):
            prompt = f"""You are a job application expert. Take the resume below and tailor it specifically for the job description provided.

Make sure the professional summary is in bullet point format, and return an ATS-optimized resume.

Master Resume:
{resume}

Job Description:
{job_description}

Return only the tailored resume.
"""
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            tailored_resume = response.choices[0].message.content
            st.subheader("✅ Tailored Resume")
            st.text_area("Result:", tailored_resume, height=300)

            # File download buttons
            st.download_button("📥 Download as TXT", tailored_resume, "tailored_resume.txt", "text/plain")
            st.download_button("📥 Download as Word (.docx)", create_docx(tailored_resume), "tailored_resume.docx")
            st.download_button("📥 Download as PDF", create_pdf(tailored_resume), "tailored_resume.pdf", "application/pdf")

# Generate Cover Letter
if st.button("✉️ Generate Cover Letter"):
    if not (resume and job_description and openai_api_key):
        st.warning("Please fill out all fields.")
    else:
        with st.spinner("Generating cover letter..."):
            prompt = f"""You are a professional cover letter writer. Write a tailored, engaging cover letter based on the resume and job description below.

Master Resume:
{resume}

Job Description:
{job_description}

Use a human tone, highlight key experiences, and keep it concise (under 300 words). Return only the letter.
"""
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            cover_letter = response.choices[0].message.content
            st.subheader("✅ Tailored Cover Letter")
            st.text_area("Result:", cover_letter, height=300)

            # File download buttons
            st.download_button("📥 Download as TXT", cover_letter, "cover_letter.txt", "text/plain")
            st.download_button("📥 Download as Word (.docx)", create_docx(cover_letter), "cover_letter.docx")
            st.download_button("📥 Download as PDF", create_pdf(cover_letter), "cover_letter.pdf", "application/pdf")
