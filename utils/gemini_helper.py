import os
import time
from google import genai
from google.genai import types
import json

GEMINI_MODEL = 'gemini-3.1-flash-lite'

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        return None
    return genai.Client(api_key=api_key)

def generate_ai_response(prompt):
    client = get_gemini_client()
    if not client:
        return "Error: GEMINI_API_KEY is missing or invalid. Please check your .env file."
    
    wait_times = [2, 4, 8]
    
    for attempt in range(len(wait_times) + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            is_retryable = '503' in error_str or '429' in error_str or 'UNAVAILABLE' in error_str or 'RESOURCE_EXHAUSTED' in error_str or 'timeout' in error_str.lower()
            
            if is_retryable and attempt < len(wait_times):
                time.sleep(wait_times[attempt])
            else:
                if is_retryable:
                    return "Gemini AI is temporarily unavailable. Please try again after a short while."
                else:
                    return f"Error communicating with AI: {error_str}"

def extract_resume_data(resume_text, standardized_skills):
    client = get_gemini_client()
    if not client:
        return None, "Error: GEMINI_API_KEY is missing. Please add it to your .env file."
        
    prompt = f"""
    You are an expert HR Resume Parser.
    Extract the following information from the resume text into a structured JSON format.
    
    Resume Text:
    {resume_text}
    
    IMPORTANT: You MUST respond ONLY with a valid JSON object. Do not include markdown blocks like ```json.
    Map any skills to the following STANDARDIZED SKILLS list if they are close matches:
    {', '.join(standardized_skills)}
    If a skill doesn't map exactly but is a valid technical skill, include it as is.
    
    Use this exact JSON structure:
    {{
        "name": "Full Name",
        "branch": "Branch or degree",
        "cgpa": "Extract CGPA as string or number (e.g. 8.5)",
        "skills": ["Skill1", "Skill2"],
        "projects": "Short summary of main projects",
        "certifications": "Short summary of certifications"
    }}
    If a field is not found, leave it as an empty string or empty list for skills.
    """
    
    wait_times = [2, 4, 8]
    for attempt in range(len(wait_times) + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                )
            )
            return json.loads(response.text), None
        except Exception as e:
            error_str = str(e)
            is_retryable = '503' in error_str or '429' in error_str or 'UNAVAILABLE' in error_str or 'RESOURCE_EXHAUSTED' in error_str or 'timeout' in error_str.lower()
            
            if is_retryable and attempt < len(wait_times):
                time.sleep(wait_times[attempt])
            else:
                if is_retryable:
                    return None, "Gemini AI is temporarily unavailable. Please try again after a short while."
                else:
                    return None, f"Failed to parse resume with AI: {error_str}"
