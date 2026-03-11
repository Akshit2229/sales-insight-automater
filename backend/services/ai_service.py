import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Ensure we have the environment loaded in this context if testing locally
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

def generate_sales_summary(data_context: str) -> str:
    """
    Uses Google Gemini API to generate a narrative summary of the sales data.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert sales analyst. The following is extracted information from a quarterly sales data file.
    Please review the statistics and the data preview, and write a professional, executive-level narrative summary.
    Highlight key trends, best-performing products, or regions if visible, and summarize the overall revenue or units sold.
    Keep the tone professional and concise (under 300 words).
    
    Data context:
    {data_context}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "An error occurred while generating the AI summary. Please check the logs."
