
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routers import rdv, litige
import os

app = FastAPI(title="TRM LLM MVP - RDV & Litiges")

# CORS (dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rdv.router, prefix="/api/rdv", tags=["rdv"])
app.include_router(litige.router, prefix="/api/litige", tags=["litige"])

@app.get("/api/health")
def health():
    return {"status": "ok"}

# Serve frontend if present
if os.path.isdir("/app/frontend_build"):
    app.mount("/", StaticFiles(directory="/app/frontend_build", html=True), name="frontend")
