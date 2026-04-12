from core.planner import plan_query

def test_plan_query_change_analysis():
    query = "Why did the sales increase last month?"
    result = plan_query(query)
    assert result["category"] == "change_analysis"
    assert "Matched pattern" in result["note"]

def test_plan_query_comparison():
    query = "Compare revenue between laptops and smartphones"
    result = plan_query(query)
    assert result["category"] == "comparison"

def test_plan_query_breakdown():
    query = "Show me the breakdown of quantity sold by category"
    result = plan_query(query)
    assert result["category"] == "breakdown"

def test_plan_query_summary_explicit():
    query = "Give me a summary of last week"
    result = plan_query(query)
    assert result["category"] == "summary"

def test_plan_query_fallback():
    query = "random query that doesn't match"
    result = plan_query(query)
    assert result["category"] == "summary"
    assert "Fallback" in result["note"]

def test_plan_query_case_insensitivity():
    query = "WHY DID SALES DROP"
    result = plan_query(query)
    assert result["category"] == "change_analysis"
