import streamlit as st
import os
import asyncio
from groq import Groq
import subprocess 

from streamlit_pdf_viewer import pdf_viewer


from dotenv import load_dotenv
load_dotenv()


groq = Groq(api_key=os.getenv("GROQ_API_KEY"))


async def tailor_resume(job_description, latex_content):
    completion = groq.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Given the LaTeX-formatted resume below, replace only existing keywords with synonyms or similar terms from the job description. Do not add new experiences, alter factual details, or change the LaTeX structure and formatting. Ensure that only existing terms closely matched in both the resume and job description are modified. Return only the LaTeX content without additional text. Job Description: {job_description} LaTeX Content: {latex_content}"
            }
        ],
        model="llama3-8b-8192",
    )

    tailored_resume = completion.choices[0].message.content.strip()
    if tailored_resume:
        return tailored_resume
    else:
        st.error("Error tailoring resume: No response from Groq API")
        return None


def convert_latex_to_pdf(latex_content, output_file):
    latex_content = "\\" + latex_content.split("\\", 1)[-1]
    latex_content = latex_content.rsplit("}", 1)[0] + "}"  
    with open("temp.tex", "w") as f:
        f.write(latex_content)
    subprocess.run(["pdflatex", "temp.tex"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    os.rename("temp.pdf", output_file)


st.title("Resume Tailoring Tool")
job_description = st.text_area("Enter Job Description:")
company_name = st.text_input("Enter Company Name:")  # New field for company name
if st.button("Tailor Resume"):
    if job_description and company_name:  # Check if both fields are filled

        os.makedirs(company_name, exist_ok=True)

        # Read the LaTeX file
        with open("test.tex", "r") as f:
            latex_content = f.read()
        
        tailored_resume = asyncio.run(tailor_resume(job_description, latex_content))
        if tailored_resume:
            output_file = os.path.join(company_name, f"{os.getenv('NAME')}.pdf")  # Save in company folder with name from env
            convert_latex_to_pdf(tailored_resume, output_file)
            with open(output_file, "rb") as pdf_file:
                pdfbyte = pdf_file.read()
            
            st.success("Resume tailored and converted to PDF successfully!")


    else:
        st.warning("Please enter both job description and company name.")
