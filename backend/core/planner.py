import re

CATEGORY_PATTERNS = {
    "change_analysis": [
        r"why.*(drop|increase|decrease|change|rise|fall|growth|decline)",
        r"(increase|decrease|drop|rise|fall|growth|decline|fluctuation|slump|spike|jump|plummet)",
        r"(what caused|reason for|cause of|why did|how did)",
        r"(trend|over time|pattern|upward|downward|volatility)",
        r"(went up|went down|variance)",
        r"\b(mom|yoy|wow|qoq|mom|yoy|wow|qoq)\b",
        r"(month-on-month|year-on-year|quarter-on-quarter)"
    ],

    "comparison": [
        r"\bvs\b",
        r"versus",
        r"compare",
        r"comparison",
        r"(more than|less than|greater than|lower than|higher than|better than|worse than)",
        r"(difference between|compare between|gap between|benchmarked against|relative to)",
        r"(compared to|against|overlap)",
        r"\bbetween\b.*\band\b",
        r"(over|under|instead of)",
        r"top.*vs.*bottom"
    ],

    "breakdown": [
        r"breakdown",
        r"composition",
        r"distribut(ion|ed)",
        r"(make up|made up of|consists of|composed of|contributed by|contribution of)",
        r"(by category|by product|by segment|by region|by.*)",
        r"(split by|divided by|split among|partitioned by)",
        r"(share|portion|slice|percentage|ratio|proportion|fraction|segmentation)",
        r"across.*(categories|products|segments)"
    ],

    "summary": [
        r"(summary|overview|snapshot|status)",
        r"(total|overall|all|sum)",
        r"(weekly|monthly|daily).*summary",
        r"(report|insight|high level|information about|details of)",
        r"(how much|what is total|how many|total count)",
        r"(list|show|fetch|get|tell me|display|give me)",
        r"(average|avg|min|max|count|stats|statistics|numbers|metrics)"
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
