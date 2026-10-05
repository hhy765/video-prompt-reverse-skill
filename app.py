from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import os

from video_prompt_skill.engine import VideoPromptEngine

app = FastAPI(
    title="Video Prompt Reverse Skill",
    description="Reverse-engineers video generation prompts and supports prompt editing.",
    version="0.1.0",
)

engine = VideoPromptEngine()

class AnalysisRequest(BaseModel):
    video_name: str = Field(..., description="Video name or identifier")
    description: Optional[str] = Field(default=None, description="Optional user description")
    style_hints: List[str] = Field(default_factory=list, description="User-specified style hints")
    target_platform: str = Field(default="gen-video", description="Target platform: gen-video, runway, pika, etc.")
    duration_seconds: Optional[int] = Field(default=None, description="Video duration in seconds")
    fps: Optional[int] = Field(default=None, description="Frame rate")

class PromptEditRequest(BaseModel):
    original_prompt: str = Field(..., description="Original prompt to modify")
    edits: List[str] = Field(default_factory=list, description="List of desired style or content edits")
    tone: Optional[str] = Field(default="cinematic", description="Target tone")
    length: Optional[str] = Field(default="medium", description="Short/medium/long")
    output_language: Optional[str] = Field(default="en", description="Prompt language")

class PromptRequest(BaseModel):
    video_name: str
    description: Optional[str] = None
    style_hints: List[str] = []
    target_platform: str = "gen-video"
    duration_seconds: Optional[int] = None
    fps: Optional[int] = None

@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "video_prompt_reverse_skill"}

@app.get("/")
def root():
    return {
        "name": "Video Prompt Reverse Skill",
        "version": "0.1.0",
        "description": "Reverse-engineer video generation prompts and edit them interactively",
        "endpoints": {
            "healthz": "GET /healthz",
            "analyze": "POST /analyze",
            "reverse_prompt": "POST /reverse-prompt",
            "edit_prompt": "POST /edit-prompt"
        }
    }

@app.post("/analyze")
def analyze_video(payload: AnalysisRequest):
    """Analyze video metadata and extract features."""
    try:
        analysis = engine.analyze_video(payload)
        return {
            "success": True,
            "analysis": analysis
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/reverse-prompt")
def reverse_prompt(payload: PromptRequest):
    """Reverse-engineer the video prompt from metadata."""
    try:
        result = engine.reverse_prompt(payload)
        return {
            "success": True,
            "result": result
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/edit-prompt")
def edit_prompt(payload: PromptEditRequest):
    """Edit and optimize an existing prompt."""
    try:
        result = engine.edit_prompt(
            original_prompt=payload.original_prompt,
            edits=payload.edits,
            tone=payload.tone,
            length=payload.length,
            output_language=payload.output_language
        )
        return {
            "success": True,
            "result": result
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
