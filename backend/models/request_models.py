from pydantic import BaseModel

class QueryRequest(BaseModel):
    """
    Data model for the natural language query request.
    This schema is used by FastAPI to validate that incoming POST requests
    to /query contain the required 'query' string field.
    """
    query: str