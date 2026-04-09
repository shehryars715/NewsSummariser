import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.routes import query, summarize
from src.app.services.rag import load_faiss_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not load_faiss_index():
        print("Warning: FAISS index not loaded. API will not work properly.")
    yield


app = FastAPI(
    title="News RAG API",
    description="Retrieve and Generate summaries from news articles",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)
app.include_router(summarize.router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "News RAG API is running", "status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    PORT = int(os.environ.get("PORT", 8000))
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=PORT, log_level="info")
