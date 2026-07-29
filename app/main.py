from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI PDF Generator",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "AI Document Engine API"
    }

@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(router)