import re

CATEGORY_PATTERNS = {
    "change_analysis": [
        r"why.*(drop|increase|decrease|change|rise|fall)",
        r"(increase|decrease|drop|rise|fall|growth|decline)",
        r"(what caused|reason for|cause of)",
        r"(trend|over time|pattern)",
        r"(went up|went down)"
    ],

    "comparison": [
        r"\bvs\b",
        r"versus",
        r"compare",
        r"comparison",
        r"(more than|less than|greater than|lower than)",
        r"(difference between|compare between)",
        r"(compared to|against)",
        r"\bbetween\b.*\band\b"
    ],

    "breakdown": [
        r"breakdown",
        r"composition",
        r"distribut(ion|ed)",
        r"(make up|made up of|consists of|composed of)",
        r"(by category|by product|by segment|by region)",
        r"(split by|divided by)"
    ],

    "summary": [
        r"summary",
        r"overview",
        r"(total|overall|all)",
        r"(weekly|monthly|daily).*summary",
        r"(report|insight|high level)",
        r"(how much|what is total)"
    ]
}

PRIORITY = ["change_analysis", "comparison", "breakdown", "summary"]

def plan_query(query: str) -> dict:
    query_clean = query.strip().lower()

    for category in PRIORITY:
        for pattern in CATEGORY_PATTERNS[category]:
            if re.search(pattern, query_clean, re.IGNORECASE):
                return {
                    "category": category,
                    "note": f"Matched pattern for {category}"
                }

    # Always keep a fallback
    return {
        "category": "summary",
        "note": "Fallback category triggered"
    }
