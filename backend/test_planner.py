from core.planner import plan_query

"""
Manual Planner Verification Script.
Quickly tests several representative queries against the regex-based 
classification system and prints the results to the console.
Run with: python backend/test_planner.py
"""

# List of test queries and their expected categories
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

# Iterate through test cases and verify the planner's output
for i, (query, expected) in enumerate(test_cases):
    result = plan_query(query)
    actual = result["category"]
    
    if actual == expected:
        print(f"✅ PASS: '{query}' -> {actual}")
    else:
        # Highlight failures for easy debugging
        print(f"❌ FAIL: '{query}' -> Expected: {expected}, Got: {actual}")

print("="*40)
