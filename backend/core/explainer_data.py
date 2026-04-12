def build_change_explainer(query, data):
    return f"""
You are a business data analyst.

Category: Understand What Changed

User Query:
{query}

Data Result:
{data}

Instructions:
- Identify whether the metric increased or decreased
- Quantify the change (percentage or absolute)
- Identify key drivers (top contributing categories/products)
- Highlight the most impactful segment
- Do NOT assume reasons outside data
- Use simple, clear language

Output format (STRICT JSON):
{{
  "summary": "Overall change in metric",
  "key_insight": "Main driver of change",
  "details": "Supporting data explanation",
  "source": "inventory"
}}
"""

def build_comparison_explainer(query, data):
    return f"""
You are a business data analyst.

Category: Compare

User Query:
{query}

Data Result:
{data}

Instructions:
- Compare entities (products/categories/time periods)
- Identify which performed better
- Quantify difference (percentage or absolute)
- Highlight key contrast
- Keep explanation concise
- Handle time phrases correctly

Output format (STRICT JSON):
{{
  "summary": "Comparison overview",
  "key_insight": "Who performed better and by how much",
  "details": "Key differences explained",
  "source": "inventory"
}}
"""

def build_breakdown_explainer(query, data):
    return f"""
You are a business data analyst.

Category: Breakdown

User Query:
{query}

Data Result:
{data}

Instructions:
- Decompose total into components (product/category/etc.)
- Identify top contributors
- Mention percentage contribution if possible
- Highlight dominant segments or concentration
- Describe any patterns (skew, spread)

Output format (STRICT JSON):
{{
  "summary": "Breakdown overview",
  "key_insight": "Top contributors",
  "details": "Contribution and pattern explanation",
  "source": "inventory"
}}
"""

def build_summary_explainer(query, data):
    return f"""
You are a business data analyst.

Category: Summarize

User Query:
{query}

Data Result:
{data}

Instructions:
- Provide concise summary of insights
- Highlight trends, anomalies, or important changes
- Avoid unnecessary details
- Focus only on key points
- Make it understandable for non-technical users

Output format (STRICT JSON):
{{
  "summary": "Key highlights",
  "key_insight": "Most important takeaway",
  "details": "Short supporting explanation",
  "source": "inventory"
}}
"""

def get_explainer_prompt(category, query, data):
    if category == "change_analysis":
        return build_change_explainer(query, data)
    elif category == "comparison":
        return build_comparison_explainer(query, data)
    elif category == "breakdown":
        return build_breakdown_explainer(query, data)
    else:
        return build_summary_explainer(query, data)

class ExplanationGenerator:
    def __init__(self):
        import os
        import google.generativeai as genai
        from dotenv import load_dotenv

        load_dotenv()
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate(self, query, data, category):
        prompt = get_explainer_prompt(category, query, data)

        response = self.model.generate_content(prompt)

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()

        return text