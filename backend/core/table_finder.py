import re

REGEX_PATTERNS = {
    "sales_metrics": re.compile(
        r"\b(sales|revenue|profit|margin|growth|units|amount|total|transaction|order|customer|discount|sold|bought)\b",
        re.IGNORECASE
    ),

    "product_data": re.compile(
        r"\b(product|category|brand|sku|item|laptop|smartphone|headphones|monitor|price|cost)\b",
        re.IGNORECASE
    ),

    "time_data": re.compile(
        r"\b(month|year|quarter|daily|weekly|january|february|march|q1|2026|date|when)\b",
        re.IGNORECASE
    ),

    "sql_injection": re.compile(
        r"\b(drop|delete|truncate|update|insert|alter|exec|union)\b",
        re.IGNORECASE
    )
}


def detect_query_scope(query: str):
    query = query.lower()

    result = {
        "tables": [],
        "requires_join": False,
        "flags": {}
    }

    # 🚨 safety
    if REGEX_PATTERNS["sql_injection"].search(query):
        result["flags"]["unsafe"] = True
        return result

    sales_match = REGEX_PATTERNS["sales_metrics"].search(query)
    product_match = REGEX_PATTERNS["product_data"].search(query)

    # 🧠 decision logic
    if sales_match and product_match:
        result["tables"] = ["fact_sales", "dim_products"]
        result["requires_join"] = True

    elif sales_match:
        result["tables"] = ["fact_sales"]

    elif product_match:
        result["tables"] = ["dim_products"]

    else:
        # fallback (safe default)
        result["tables"] = ["fact_sales"]

    return result