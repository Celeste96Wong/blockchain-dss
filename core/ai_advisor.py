"""
AI Advisor — calls OpenAI API directly via requests (no openai library needed)
Avoids version conflicts on Vercel
"""

import json
import os

try:
    import urllib.request as urlrequest
except ImportError:
    urlrequest = None


def generate_recommendation(topsis_result: dict, business_context: dict) -> dict:
    api_key = business_context.get("api_key", "").strip() or os.environ.get("OPENAI_API_KEY", "")

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
Always explain WHY, not just WHAT.
Never use technical blockchain terms without immediately explaining them in plain language.
Structure your response in clear sections."""

    user_prompt = f"""A business owner completed a blockchain adoption readiness assessment.

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
(2-3 sentences explaining their score in plain language)

## Your Key Strengths
(Explain the top 2 strengths and why they matter)

## What To Work On First
(Explain the 2 gaps with 1 concrete actionable step each)

## Our Recommendation
(Clear YES/NOT YET/PREPARE FIRST recommendation with 3 next steps)

Keep the entire response under 350 words. Be warm and encouraging."""

    if not api_key:
        return {
            "success": False,
            "error": "No API key provided",
            "full_text": get_fallback_advice(topsis_result),
            "sections": {},
        }

    try:
        payload = json.dumps({
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 600,
            "temperature": 0.7,
        }).encode("utf-8")

        req = urlrequest.Request(
            "https://api.openai.com/v1/chat/completions",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST"
        )

        with urlrequest.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        advice_text = data["choices"][0]["message"]["content"]
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
        return f"Your readiness score of {score}/100 indicates strong potential for blockchain adoption. Your strengths align well with blockchain's core benefits. We recommend consulting a blockchain implementation specialist to begin your journey."
    elif tier == "medium":
        return f"Your readiness score of {score}/100 shows moderate potential. You have some foundations in place, but there are areas to strengthen before committing to full blockchain adoption. Focus on building technical readiness and securing budget allocation first."
    else:
        return f"Your readiness score of {score}/100 suggests blockchain may not be the right fit right now. Start by digitising your core processes and educating your team about blockchain basics."