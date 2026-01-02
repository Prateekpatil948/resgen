import os
import json
from typing import Dict, Any
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_ai_editing_suggestions(
    analysis_results: Dict[str, Any],
    resume_text: str
) -> Dict[str, Any]:

    prompt = f"""
You are a professional resume editor.

Return ONLY valid JSON:

{{
  "ai_suggestions_for_edit": [
    {{
      "section": str,
      "current_content": str,
      "suggestion": str,
      "example": str
    }}
  ]
}}

Weaknesses:
{analysis_results.get("weaknesses", [])}

Suggestions:
{analysis_results.get("suggestions", [])}

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

    try:
        response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ UPDATED MODEL
        messages=[
            {"role": "system", "content": "You improve resumes."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

        content = response.choices[0].message.content.strip()
        json_str = content[content.find("{"): content.rfind("}") + 1]
        return json.loads(json_str)

    except Exception as e:
        print("Groq suggestion error:", e)
        return {
            "error": str(e),
            "ai_suggestions_for_edit": []
        }
