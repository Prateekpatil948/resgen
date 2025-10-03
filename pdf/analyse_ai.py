import google.generativeai as genai # type: ignore
import json
from typing import Dict, Any

# Configure API key
genai.configure(api_key="AIzaSyDqK6DM7QGtVDISupaQkrFENYYxVTP-T2A")

def evaluate_resume_with_gemini(resume_text: str, job_description: str = "") -> Dict[str, Any]:
    """
    Evaluates a resume using Gemini Flash model and returns a comprehensive analysis.
    
    Args:
        resume_text (str): The text content of the resume.
        job_description (str): Optional job description for targeted analysis.
    
    Returns:
        dict: Dictionary with evaluation scores and insights matching the Profile model.
    """
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
    
    prompt = f"""
You are a professional resume evaluation assistant. Analyze the following resume content and provide a detailed JSON response with the following structure:

{{
  "overall_score": int (0 to 100),
  "summary": str (detailed analysis summary),
  "score_metrics": {{
    "summary_score": int (0 to 10),
    "summary_feedback": str,
    "experience_score": int (0 to 10),
    "experience_feedback": str,
    "skills_score": int (0 to 10),
    "skills_feedback": str,
    "education_score": int (0 to 10),
    "education_feedback": str,
    "projects_score": int (0 to 10),
    "projects_feedback": str,
    "grammar_score": int (0 to 10),
    "grammar_feedback": str,
    "formatting_score": int (0 to 10),
    "formatting_feedback": str
  }},
  "strengths": [str],
  "weaknesses": [str],
  "suggestions": [str],
  "job_description_match": int (0 to 100) if job description provided
}}

IMPORTANT: Your response must be valid JSON only, with no additional text or markdown formatting.

Evaluation criteria:
1. Relevance to job description (if provided)
2. Clarity and professionalism
3. Grammar and spelling
4. Formatting and organization
5. Content completeness
6. Impact and achievement orientation

Resume content:
\"\"\"
{resume_text}
\"\"\"
"""

    if job_description:
        prompt += f"""
Job Description to compare against:
\"\"\"
{job_description}
\"\"\"
"""

    try:
        response = model.generate_content(prompt)
        
        # Ensure we have text content
        if not response.text:
            raise ValueError("Empty response from Gemini API")
        
        # Try to find JSON in the response (sometimes Gemini adds markdown)
        json_start = response.text.find('{')
        json_end = response.text.rfind('}') + 1
        json_str = response.text[json_start:json_end] if json_start != -1 else response.text
        
        # Parse the JSON
        result = json.loads(json_str)
        
        
        # Validate required fields
        if "overall_score" not in result:
            raise ValueError("Invalid response format - missing required fields")
            
        return result
    
        
    except json.JSONDecodeError as e:
        print("Error parsing JSON response:", e)
        print("Raw response:", response.text if 'response' in locals() else 'No response')
        return {
            "error": "Failed to parse AI response",
            "overall_score": 0,
            "summary": "Error in analysis - invalid response format",
            "score_metrics": {},
            "strengths": [],
            "weaknesses": [],
            "suggestions": ["The analysis service is currently unavailable. Please try again later."]
        }
    # except Exception as e:
    #     print("Error in resume evaluation:", e)
    #     return {
    #         "error": str(e),
    #         "overall_score": 0,
    #         "summary": "Error in analysis - service unavailable",
    #         "score_metrics": {},
    #         "strengths": [],
    #         "weaknesses": [],
    #         "suggestions": ["The analysis service encountered an error. Please try again later."]
    #     }
    
