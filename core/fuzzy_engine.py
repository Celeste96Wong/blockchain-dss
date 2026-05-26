"""
Fuzzy AHP + TOPSIS Engine
For Blockchain Adoption Readiness Assessment
"""

import numpy as np
from typing import List, Dict, Tuple

# ─── Triangular Fuzzy Number helpers ───────────────────────────────────────────
# A TFN is represented as (l, m, u) — lower, middle, upper

# Linguistic scale → TFN mapping (standard 9-point scale)
LINGUISTIC_SCALE = {
    "equally_important":        (1, 1, 1),
    "weakly_important":         (1, 3, 5),
    "moderately_important":     (3, 5, 7),
    "strongly_important":       (5, 7, 9),
    "extremely_important":      (7, 9, 9),
}

# User answer (slider 1–5) → TFN
RATING_SCALE = {
    1: (1, 1, 3),   # Very Low
    2: (1, 3, 5),   # Low
    3: (3, 5, 7),   # Medium
    4: (5, 7, 9),   # High
    5: (7, 9, 9),   # Very High
}

def tfn_multiply(a: tuple, b: tuple) -> tuple:
    return (a[0]*b[0], a[1]*b[1], a[2]*b[2])

def tfn_add(a: tuple, b: tuple) -> tuple:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def tfn_divide(a: tuple, b: tuple) -> tuple:
    return (a[0]/b[2], a[1]/b[1], a[2]/b[0])

def tfn_defuzzify(tfn: tuple) -> float:
    """Convert TFN to crisp value using Centre of Area method"""
    return (tfn[0] + tfn[1] + tfn[2]) / 3.0


# ─── Criteria Definition ───────────────────────────────────────────────────────
CRITERIA = [
    {
        "id": "data_integrity",
        "label": "Data Integrity Need",
        "question": "How important is it that your business data cannot be altered or tampered with?",
        "description": "e.g. records, contracts, transactions",
        "icon": "🔒",
        "weight_tfn": (5, 7, 9),   # Pre-set expert weights (Fuzzy AHP result)
    },
    {
        "id": "trust_parties",
        "label": "Multi-Party Trust Issues",
        "question": "How many untrusted parties does your business interact with regularly?",
        "description": "e.g. suppliers, partners, customers across organisations",
        "icon": "🤝",
        "weight_tfn": (5, 7, 9),
    },
    {
        "id": "transparency",
        "label": "Transparency Requirement",
        "question": "How important is full transparency of transactions to your stakeholders?",
        "description": "e.g. auditors, regulators, customers want visibility",
        "icon": "👁️",
        "weight_tfn": (3, 5, 7),
    },
    {
        "id": "automation",
        "label": "Process Automation Potential",
        "question": "How much of your business process could benefit from automatic execution (smart contracts)?",
        "description": "e.g. payments triggered when conditions are met",
        "icon": "⚙️",
        "weight_tfn": (3, 5, 7),
    },
    {
        "id": "tech_readiness",
        "label": "Technical Readiness",
        "question": "How would you rate your team's current digital/IT capability?",
        "description": "e.g. ability to use and maintain new digital tools",
        "icon": "💻",
        "weight_tfn": (1, 3, 5),
    },
    {
        "id": "budget",
        "label": "Budget Availability",
        "question": "How much budget can your organisation allocate to new technology adoption?",
        "description": "Relative to your organisation's size",
        "icon": "💰",
        "weight_tfn": (1, 3, 5),
    },
    {
        "id": "regulatory",
        "label": "Regulatory Compliance Pressure",
        "question": "How strong is the regulatory/legal pressure in your industry to adopt transparent systems?",
        "description": "e.g. finance, healthcare, food safety regulations",
        "icon": "📋",
        "weight_tfn": (3, 5, 7),
    },
]


# ─── Fuzzy TOPSIS ──────────────────────────────────────────────────────────────

def run_fuzzy_topsis(user_ratings: Dict[str, int]) -> Dict:
    """
    Run Fuzzy TOPSIS to compute blockchain adoption readiness score.

    user_ratings: {criterion_id: rating (1–5)}
    Returns: score dict with readiness level, scores per criterion, recommendation tier
    """
    n = len(CRITERIA)

    # Step 1: Convert ratings to TFNs
    rating_tfns = []
    weight_tfns = []
    for c in CRITERIA:
        r = user_ratings.get(c["id"], 3)
        rating_tfns.append(RATING_SCALE[r])
        weight_tfns.append(c["weight_tfn"])

    # Step 2: Normalise weights
    weight_crisp = [tfn_defuzzify(w) for w in weight_tfns]
    total_w = sum(weight_crisp)
    norm_weights = [w / total_w for w in weight_crisp]

    # Step 3: Weighted normalised fuzzy decision matrix
    # Ideal best = (1,1,1) scaled, Ideal worst = (0,0,0) — simplified for 1 alternative
    # For a single user, we compute distance from ideal best and ideal worst
    # FPIS (Fuzzy Positive Ideal Solution) = highest possible TFN per criterion
    # FNIS (Fuzzy Negative Ideal Solution) = lowest possible TFN per criterion

    FPIS = (7, 9, 9)   # Best possible rating TFN
    FNIS = (1, 1, 3)   # Worst possible rating TFN

    def vertex_distance(a: tuple, b: tuple) -> float:
        return np.sqrt(((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2) / 3)

    d_pos_list = []
    d_neg_list = []
    criterion_scores = []

    for i, c in enumerate(CRITERIA):
        rtfn = rating_tfns[i]
        w = norm_weights[i]

        # Weighted TFN
        wtfn = (rtfn[0]*w, rtfn[1]*w, rtfn[2]*w)
        wfpis = (FPIS[0]*w, FPIS[1]*w, FPIS[2]*w)
        wfnis = (FNIS[0]*w, FNIS[1]*w, FNIS[2]*w)

        dp = vertex_distance(wtfn, wfpis)
        dn = vertex_distance(wtfn, wfnis)

        d_pos_list.append(dp)
        d_neg_list.append(dn)

        # Per-criterion score (0–100)
        crit_score = (tfn_defuzzify(rtfn) / 9.0) * 100
        criterion_scores.append({
            "id": c["id"],
            "label": c["label"],
            "icon": c["icon"],
            "score": round(crit_score, 1),
            "rating": user_ratings.get(c["id"], 3),
            "weight": round(norm_weights[i] * 100, 1),
        })

    # Step 4: Closeness coefficient
    D_pos = sum(d_pos_list)
    D_neg = sum(d_neg_list)
    CC = D_neg / (D_pos + D_neg) if (D_pos + D_neg) > 0 else 0

    readiness_score = round(CC * 100, 1)

    # Step 5: Tier classification
    if readiness_score >= 70:
        tier = "high"
        tier_label = "High Readiness"
        tier_color = "#22c55e"
        tier_emoji = "🟢"
    elif readiness_score >= 45:
        tier = "medium"
        tier_label = "Moderate Readiness"
        tier_color = "#f59e0b"
        tier_emoji = "🟡"
    else:
        tier = "low"
        tier_label = "Low Readiness"
        tier_color = "#ef4444"
        tier_emoji = "🔴"

    # Step 6: Identify top strengths and gaps
    sorted_scores = sorted(criterion_scores, key=lambda x: x["score"], reverse=True)
    strengths = sorted_scores[:2]
    gaps = sorted_scores[-2:]

    return {
        "readiness_score": readiness_score,
        "tier": tier,
        "tier_label": tier_label,
        "tier_color": tier_color,
        "tier_emoji": tier_emoji,
        "criterion_scores": criterion_scores,
        "strengths": strengths,
        "gaps": gaps,
        "D_pos": round(D_pos, 4),
        "D_neg": round(D_neg, 4),
        "CC": round(CC, 4),
    }


def get_criteria_for_frontend() -> List[Dict]:
    return [
        {
            "id": c["id"],
            "label": c["label"],
            "question": c["question"],
            "description": c["description"],
            "icon": c["icon"],
        }
        for c in CRITERIA
    ]
