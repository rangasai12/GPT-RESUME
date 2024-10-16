# Simple AUTO-RESUME


## Prerequisites
- Python 3.7 or higher

## Setup Instructions

1. **Clone the Repository**

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   add variables in the  `.env` file in the project’s root directory , add your Groq API key and Name:
   ```
   GROQ_API_KEY="groq_api_key_here"
   NAME="Your Name Here"
   ```

5. **Run the Application**
   ```bash
   streamlit run resume_auto.py
   ```

## How to Use It
- Open your web browser and go to `http://localhost:8501`.
- enter Job description and Company Name
- Resume should be in a new Company Name folder

## NOTE
- Not very optimized with the token usage
- Assumes that you have a single latex file with all the content
- Cross check the resume once

