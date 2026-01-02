import os
import json
from typing import Dict, Any
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def evaluate_resume_with_groq(
    resume_text: str,
    job_description: str = ""
) -> Dict[str, Any]:

    prompt = f"""
You are a professional resume evaluation assistant.

Return ONLY valid JSON:

{{
  "overall_score": int,
  "summary": str,
  "score_metrics": {{
    "summary_score": int,
    "summary_feedback": str,
    "experience_score": int,
    "experience_feedback": str,
    "skills_score": int,
    "skills_feedback": str,
    "education_score": int,
    "education_feedback": str,
    "projects_score": int,
    "projects_feedback": str,
    "grammar_score": int,
    "grammar_feedback": str,
    "formatting_score": int,
    "formatting_feedback": str
  }},
  "strengths": [str],
  "weaknesses": [str],
  "suggestions": [str],
  "job_description_match": int
}}

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

    if job_description:
        prompt += f"""
Job Description:
\"\"\"
{job_description}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ UPDATED MODEL
        messages=[
            {"role": "system", "content": "You are an expert resume evaluator."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )


        content = response.choices[0].message.content.strip()
        json_str = content[content.find("{"): content.rfind("}") + 1]
        return json.loads(json_str)

    except Exception as e:
        print("Groq resume analysis error:", e)
        return {
            "error": str(e),
            "overall_score": 0,
            "summary": "Analysis failed",
            "score_metrics": {},
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "job_description_match": 0,
        }
