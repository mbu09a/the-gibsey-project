#!/usr/bin/env python3
"""
Character Consciousness Test Server
Runs all character APIs without external dependencies
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import character APIs
from backend.app.api.glyph_marrow_api import router as glyph_marrow_router
from backend.app.api.london_fox_api import router as london_fox_router
from backend.app.api.jacklyn_variance_api import router as jacklyn_variance_router
from backend.app.api.oren_progresso_api import router as oren_progresso_router
# arieol_owlist_api not yet implemented
from backend.app.api.phillip_bafflemint_api import router as phillip_bafflemint_router

# Create minimal FastAPI app
app = FastAPI(
    title="Character Consciousness Test Server",
    description="Testing all character consciousness implementations",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include character routers
app.include_router(glyph_marrow_router)
app.include_router(london_fox_router)
app.include_router(jacklyn_variance_router)
app.include_router(oren_progresso_router)
# app.include_router(arieol_owlist_router)  # Not yet implemented
app.include_router(phillip_bafflemint_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Character Consciousness Test Server",
        "version": "1.0.0", 
        "status": "online",
        "endpoints": {
            "docs": "/api/docs",
            "glyph_marrow": "/api/glyph-marrow",
            "london_fox": "/api/london-fox",
            "jacklyn_variance": "/api/jacklyn-variance",
            "oren_progresso": "/api/oren-progresso",
            "arieol_owlist": "/api/arieol-owlist",
            "phillip_bafflemint": "/api/phillip-bafflemint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "characters": ["glyph_marrow", "london_fox", "jacklyn_variance", "oren_progresso", "arieol_owlist", "phillip_bafflemint"],
        "message": "Character consciousness test server running"
    }

if __name__ == "__main__":
    import uvicorn
    print("🎭 Starting Character Consciousness Test Server...")
    print("🦊 London Fox Graph & Consciousness Engine")
    print("🔤 Glyph Marrow QDPI with Linguistic Vertigo")
    print("📊 Jacklyn Variance Database & Surveillance Analysis")
    print("🎩 Oren Progresso Executive Orchestration & Observability")
    print("🔮 Arieol Owlist NLP & Semantic Understanding")
    print("📋 Phillip Bafflemint UI/UX & Workflow Automation")
    print("📡 API Docs: http://localhost:8001/api/docs")
    print("🔍 Health: http://localhost:8001/health")
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)