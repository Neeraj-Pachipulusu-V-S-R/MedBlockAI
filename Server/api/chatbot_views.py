# api/chatbot.py
import os
import google.generativeai as genai
import PyPDF2

os.environ['GEMINI_API_KEY'] = "AIzaSyDxK7CxvKYGt62fL3XsLJDR6oB-cXdX35I"
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

def generate_gemini_content(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def extract_text_from_pdf(pdf_file_path):
    text = ''
    try:
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        text = f"Failed to extract text due to: {str(e)}"
    return text