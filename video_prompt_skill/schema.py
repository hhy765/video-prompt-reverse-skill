from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class VideoFeatures(BaseModel):
    style: str = ""
    mood: str = ""
    scene: str = ""
    camera: str = ""
    lighting: str = ""
    color_palette: List[str] = []
    subjects: List[str] = []
    composition: str = ""
    motion: str = ""
    environment: str = ""

class ReversePromptResult(BaseModel):
    original_prompt: str
    refined_prompt: str
    keywords: List[str]
    style_tags: List[str]
    confidence: float
    notes: List[str] = []

class PromptEditResult(BaseModel):
    original_prompt: str
    edited_prompt: str
    edits_applied: List[str]
    summary: str

class VideoAnalysisResult(BaseModel):
    video_name: str
    description: str
    style_hints: List[str]
    keywords: List[str]
    style_tags: List[str]
    target_platform: str
    duration_seconds: int
    fps: int
    summary: Dict[str, str]
