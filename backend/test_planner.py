from core.planner import plan_query

test_cases = [
    ("Why did revenue drop last month?", "change_analysis"),
    ("Revenue went down, why?", "change_analysis"),
    ("Compare apples and oranges", "comparison"),
    ("Apple vs Orange performance", "comparison"),
    ("Show sales by category", "breakdown"),
    ("How is revenue distributed?", "breakdown"),
    ("Give me total revenue", "summary"),
    ("Weekly overview of sales", "summary")
]

print("Running Plan Category Tests...\n" + "="*40)
for i, (query, expected) in enumerate(test_cases):
    result = plan_query(query)
    actual = result["category"]
    
    if actual == expected:
        print(f"✅ PASS: '{query}' -> {actual}")
    else:
        print(f"❌ FAIL: '{query}' -> Expected: {expected}, Got: {actual}")

print("="*40)
