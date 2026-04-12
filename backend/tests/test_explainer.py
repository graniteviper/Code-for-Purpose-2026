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

def test_build_explainer_prompts():
    query = "test query"
    data = [{"id": 1}]
    
    assert "Understand What Changed" in build_change_explainer(query, data)
    assert "Category: Compare" in build_comparison_explainer(query, data)
    assert "Category: Breakdown" in build_breakdown_explainer(query, data)
    assert "Category: Summarize" in build_summary_explainer(query, data)

def test_get_explainer_prompt():
    query = "test"
    data = []
    
    assert "Understand What Changed" in get_explainer_prompt("change_analysis", query, data)
    assert "Category: Compare" in get_explainer_prompt("comparison", query, data)
    assert "Category: Breakdown" in get_explainer_prompt("breakdown", query, data)
    assert "Category: Summarize" in get_explainer_prompt("summary", query, data)
    assert "Category: Summarize" in get_explainer_prompt("unknown", query, data)

@patch("core.explainer_data.genai.GenerativeModel")
def test_explanation_generator_generate(mock_model_class):
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"summary": "test"}'
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    generator = ExplanationGenerator()
    result = generator.generate("query", [], "summary")
    
    assert result == '{"summary": "test"}'
    mock_model.generate_content.assert_called_once()
