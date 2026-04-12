import re

# CATEGORY_PATTERNS: A dictionary of regular expressions used to classify user queries.
# Each key represents a business logic category, and the list of patterns identifies
# keywords or phrases associated with that category.
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

# PRIORITY: Defines the order in which patterns are checked.
# Since a query might match multiple categories, the order of classification matters.
PRIORITY = ["change_analysis", "comparison", "breakdown", "summary"]

def plan_query(query: str) -> dict:
    """
    Classifies the user query into one of the predefined analysis categories.
    This classification helps guide both SQL generation and the final insight explanation.
    
    Args:
        query: The raw string of the user's natural language question.
        
    Returns:
        dict: A dictionary containing the 'category' and a 'note' about why it was chosen.
    """
    # Normalize the query for case-insensitive matching
    query_clean = query.strip().lower()

    # Iterate through each category in order of priority
    for category in PRIORITY:
        for pattern in CATEGORY_PATTERNS[category]:
            # Use regex to find a match in the cleaned query
            if re.search(pattern, query_clean, re.IGNORECASE):
                return {
                    "category": category,
                    "note": f"Matched pattern for {category}"
                }

    # If no specific patterns match, default to a general 'summary' category
    return {
        "category": "summary",
        "note": "Fallback category triggered"
    }
