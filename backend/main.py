from fastapi import FastAPI
from routes.query_routes import router as query_router
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI application
app = FastAPI(title="NatWest Code For Purpose API")

# Configure Cross-Origin Resource Sharing (CORS)
# This allows the frontend (running on different ports/domains) to interact with the API
app.add_middleware(
    CORSMiddleware,
    # Defined origins for local development and production deployment
    allow_origins=["http://localhost:5173", "https://code-for-purpose-2026.vercel.app"],
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Register the query routes from the routes module
app.include_router(query_router)

@app.get("/")
def root():
    """
    Health check endpoint to verify that the API is running correctly.
    """
    return {"message": "API running 🚀"}