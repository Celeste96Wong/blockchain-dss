"""
AI Advisor — uses OpenAI to generate plain-language blockchain adoption recommendations
based on Fuzzy TOPSIS results.
"""

from openai import OpenAI
import json

def generate_recommendation(topsis_result: dict, business_context: dict) -> dict:
    """
    Generate AI-powered plain language recommendation.

    topsis_result: output from run_fuzzy_topsis()
    business_context: {industry, size, goal}
    """
    client = OpenAI(api_key=business_context.get("api_key", ""))

    score = topsis_result["readiness_score"]
    tier = topsis_result["tier"]
    strengths = [s["label"] for s in topsis_result["strengths"]]
    gaps = [g["label"] for g in topsis_result["gaps"]]
    criterion_scores = topsis_result["criterion_scores"]

    criteria_summary = "\n".join([
        f"- {c['label']}: {c['score']}/100 (user rated {c['rating']}/5)"
        for c in criterion_scores
    ])

    system_prompt = """You are a friendly blockchain adoption advisor helping non-technical 
small business owners understand whether blockchain is right for them.
Your tone is warm, clear, jargon-free, and encouraging.
You always explain WHY, not just WHAT.
Never use technical blockchain terms without immediately explaining them in plain language.
Structure your response in clear sections."""

    user_prompt = f"""A business owner has just completed a blockchain adoption readiness assessment.

Business Context:
- Industry: {business_context.get('industry', 'General Business')}
- Company Size: {business_context.get('size', 'Small')}
- Main Goal: {business_context.get('goal', 'Improve operations')}

Assessment Results:
- Overall Readiness Score: {score}/100
- Readiness Level: {topsis_result['tier_label']}
- Top Strengths: {', '.join(strengths)}
- Areas Needing Attention: {', '.join(gaps)}

Detailed Scores:
{criteria_summary}

Please provide a response with EXACTLY these 4 sections (use these exact headers):

## What This Means For You
(2-3 sentences explaining their score in plain language, relating to their specific industry)

## Your Key Strengths
(Explain the top 2 strengths and why they matter for blockchain adoption — no jargon)

## What To Work On First
(Explain the 2 gaps and give 1 concrete, actionable step for each — like advice from a trusted friend)

## Our Recommendation
(Based on their tier, give a clear YES/NOT YET/PREPARE FIRST recommendation with 3 specific next steps)

Keep the entire response under 350 words. Be warm and encouraging, never discouraging."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=600,
            temperature=0.7,
        )
        advice_text = response.choices[0].message.content

        # Parse sections
        sections = parse_sections(advice_text)

        return {
            "success": True,
            "full_text": advice_text,
            "sections": sections,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "full_text": get_fallback_advice(topsis_result),
            "sections": {},
        }


def parse_sections(text: str) -> dict:
    """Extract the 4 sections from AI response"""
    sections = {}
    current_section = None
    current_content = []

    section_map = {
        "What This Means For You": "meaning",
        "Your Key Strengths": "strengths",
        "What To Work On First": "gaps",
        "Our Recommendation": "recommendation",
    }

    for line in text.split("\n"):
        stripped = line.strip()
        matched = False
        for header, key in section_map.items():
            if header in stripped:
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = key
                current_content = []
                matched = True
                break
        if not matched and current_section:
            current_content.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def get_fallback_advice(topsis_result: dict) -> str:
    tier = topsis_result["tier"]
    score = topsis_result["readiness_score"]

    if tier == "high":
        return f"Your readiness score of {score}/100 indicates strong potential for blockchain adoption. Your strengths in data integrity and multi-party trust align well with blockchain's core benefits. We recommend consulting a blockchain implementation specialist to begin your journey."
    elif tier == "medium":
        return f"Your readiness score of {score}/100 shows moderate potential. You have some foundations in place, but there are areas to strengthen before committing to full blockchain adoption. Focus on building technical readiness and securing budget allocation first."
    else:
        return f"Your readiness score of {score}/100 suggests blockchain may not be the right fit right now. This isn't a setback — it's an opportunity to build the right foundations. Start by digitising your core processes and educating your team about blockchain basics."
