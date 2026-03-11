from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
import uvicorn
import os
from dotenv import load_dotenv

from api.router import router as api_router
from core.security import verify_api_key

# Load from the parent directory where .env is located
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

app = FastAPI(
    title="Sales Insight Automator API",
    description="API for processing sales data, generating AI summaries, and emailing them.",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost:5173", # Vite default
    "http://localhost:3000",
    "https://sales-insight-automater.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api", tags=["sales"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Sales Insight Automator API. Access /docs for Swagger UI."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
