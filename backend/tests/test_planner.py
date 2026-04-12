from core.planner import plan_query

"""
Unit tests for the query planner module.
Verifies that natural language queries are correctly classified into business 
categories using regex pattern matching.
"""

def test_plan_query_change_analysis():
    """Matches keywords like 'increase', 'why', 'drop' to the change_analysis category."""
    query = "Why did the sales increase last month?"
    result = plan_query(query)
    assert result["category"] == "change_analysis"
    assert "Matched pattern" in result["note"]

def test_plan_query_comparison():
    """Matches 'compare' and 'between' to the comparison category."""
    query = "Compare revenue between laptops and smartphones"
    result = plan_query(query)
    assert result["category"] == "comparison"

def test_plan_query_breakdown():
    """Matches 'breakdown' and 'by category' to the breakdown category."""
    query = "Show me the breakdown of quantity sold by category"
    result = plan_query(query)
    assert result["category"] == "breakdown"

def test_plan_query_summary_explicit():
    """Matches 'summary' to the summary category."""
    query = "Give me a summary of last week"
    result = plan_query(query)
    assert result["category"] == "summary"

def test_plan_query_fallback():
    """Ensures queries that don't match any pattern still land in a safe fallback (summary)."""
    query = "random query that doesn't match"
    result = plan_query(query)
    assert result["category"] == "summary"
    assert "Fallback" in result["note"]

def test_plan_query_case_insensitivity():
    """Validates that matching works regardless of text casing."""
    query = "WHY DID SALES DROP"
    result = plan_query(query)
    assert result["category"] == "change_analysis"
