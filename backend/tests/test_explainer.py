import pytest
from unittest.mock import MagicMock, patch
from core.explainer_data import (
    build_change_explainer, 
    build_comparison_explainer, 
    build_breakdown_explainer, 
    build_summary_explainer, 
    get_explainer_prompt,
    ExplanationGenerator
)

"""
Unit tests for the business logic explainer module.
Verifies that prompts are correctly constructed for different categories
and that the ExplanationGenerator correctly interacts with the LLM API.
"""

def test_build_explainer_prompts():
    """
    Ensures that each specific explainer builder (change, comparison, breakdown, summary)
    includes the expected category headers in the generated prompt.
    """
    query = "test query"
    data = [{"id": 1}]
    
    assert "Understand What Changed" in build_change_explainer(query, data)
    assert "Category: Compare" in build_comparison_explainer(query, data)
    assert "Category: Breakdown" in build_breakdown_explainer(query, data)
    assert "Category: Summarize" in build_summary_explainer(query, data)

def test_get_explainer_prompt():
    """
    Validates the routing logic that chooses the correct prompt builder 
    based on the classification category.
    """
    query = "test"
    data = []
    
    assert "Understand What Changed" in get_explainer_prompt("change_analysis", query, data)
    assert "Category: Compare" in get_explainer_prompt("comparison", query, data)
    assert "Category: Breakdown" in get_explainer_prompt("breakdown", query, data)
    assert "Category: Summarize" in get_explainer_prompt("summary", query, data)
    # Default case for unknown categories
    assert "Category: Summarize" in get_explainer_prompt("unknown", query, data)

@patch("core.explainer_data.genai.GenerativeModel")
def test_explanation_generator_generate(mock_model_class):
    """
    Tests the main generate function of the ExplanationGenerator by mocking 
    the Google Gemini API response.
    """
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"summary": "test"}'
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    generator = ExplanationGenerator()
    result = generator.generate("query", [], "summary")
    
    # Assert that the cleaned-up output matches the mock response
    assert result == '{"summary": "test"}'
    mock_model.generate_content.assert_called_once()
