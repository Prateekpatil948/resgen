import google.generativeai as genai  # type: ignore
import json
from typing import Dict, Any

# Configure API key (same as in analyse_ai.py)
genai.configure(api_key="AIzaSyCbfbuiwHQW5rIdG_VIxg11kKeh-msIWU4")

def generate_ai_editing_suggestions(analysis_results: Dict[str, Any], resume_text: str) -> Dict[str, Any]:
    """
    Generates specific AI-powered editing suggestions based on weaknesses and suggestions from analysis.
    
    Args:
        analysis_results (dict): The results dictionary from evaluate_resume_with_gemini()
        resume_text (str): The original resume text content
    
    Returns:
        dict: Dictionary with AI-powered editing suggestions
    """
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
    
    # Extract weaknesses and suggestions from analysis
    weaknesses = analysis_results.get("weaknesses", [])
    suggestions = analysis_results.get("suggestions", [])
    
    prompt = f"""
You are a professional resume editing assistant. Based on the following weaknesses and general suggestions,
provide specific, actionable editing suggestions for improving the resume. Your response should be in JSON format
with the following structure:

{{
  "ai_suggestions_for_edit": [
    {{
      "section": str (which resume section this applies to),
      "current_content": str (excerpt from resume if applicable),
      "suggestion": str (specific editing suggestion),
      "example": str (example of how to implement the suggestion)
    }}
  ]
}}

Weaknesses identified:
{weaknesses}

General suggestions:
{suggestions}

Resume content for reference:
\"\"\"
{resume_text}
\"\"\"

Provide at least 3-5 specific editing suggestions targeting the identified weaknesses.
Focus on making concrete recommendations with examples where possible.
"""

    try:
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        json_start = response.text.find('{')
        json_end = response.text.rfind('}') + 1
        json_str = response.text[json_start:json_end] if json_start != -1 else response.text
        
        # Parse the JSON
        edit_suggestions = json.loads(json_str)
        
        return edit_suggestions
        
    except json.JSONDecodeError as e:
        print("Error parsing AI editing suggestions:", e)
        return {
            "error": "Failed to parse AI editing suggestions",
            "ai_suggestions_for_edit": []
        }
    except Exception as e:
        print("Error generating editing suggestions:", e)
        return {
            "error": str(e),
            "ai_suggestions_for_edit": []
        }