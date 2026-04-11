from fastapi import FastAPI
from routes.query_routes import router as query_router

app = FastAPI()

app.include_router(query_router)

@app.get("/")
def root():
    return {"message": "API running 🚀"}