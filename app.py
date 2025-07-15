import streamlit as st
import openai

st.set_page_config(page_title="JobFit Copilot", layout="centered")

st.title("🎯 JobFit Copilot")
st.write("Generate tailored resumes and cover letters using AI.")

openai_api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")

resume = st.text_area("📄 Paste your Master Resume here:", height=300)
job_description = st.text_area("💼 Paste the Job Description here:", height=300)

if st.button("🎯 Generate Tailored Resume"):
    if not (resume and job_description and openai_api_key):
        st.warning("Please fill out all fields.")
    else:
        with st.spinner("Generating tailored resume..."):
            openai.api_key = openai_api_key
            prompt = f"""You are a job application expert. Take the resume below and tailor it specifically for the job description provided.

Master Resume:
{resume}

Job Description:
{job_description}

Return a customized, ATS-friendly resume that matches the job role with improved bullet points and optimized phrasing.
Make sure the Professional Summary section is formatted as clear, concise bullet points rather than paragraphs.
"""
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            tailored_resume = response.choices[0].message.content
            st.subheader("✅ Tailored Resume")
            st.text_area("Result:", tailored_resume, height=300)

if st.button("✉️ Generate Cover Letter"):
    if not (resume and job_description and openai_api_key):
        st.warning("Please fill out all fields.")
    else:
        with st.spinner("Generating cover letter..."):
            openai.api_key = openai_api_key
            prompt = f"""You are a professional cover letter writer. Write a tailored, engaging cover letter based on the resume and job description below.

Master Resume:
{resume}

Job Description:
{job_description}

Use a human tone, highlight key experiences, and keep it concise (under 300 words). Return only the letter.
"""
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6
            )
            cover_letter = response.choices[0].message.content
            st.subheader("✅ Tailored Cover Letter")
            st.text_area("Result:", cover_letter, height=300)
