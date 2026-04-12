from fastapi import FastAPI
from routes.query_routes import router as query_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://code-for-purpose-2026.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(query_router)

@app.get("/")
def root():
    return {"message": "API running 🚀"}