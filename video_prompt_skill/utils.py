import re
from typing import List

def normalize_text(value: str) -> str:
    """Normalize text by removing extra whitespace."""
    if not value:
        return ""
    return re.sub(r"\s+", " ", value).strip()

def extract_keywords(text: str) -> List[str]:
    """Extract keywords from text."""
    if not text:
        return []
    tokens = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]+", text)
    stop_words = {
        "the", "and", "with", "for", "into", "from", "of", "in", "on", "a", "an", "to", "is", "video",
        "scene", "shot", "style", "high", "quality", "very", "by", "at", "as", "that", "this",
        "are", "be", "been", "have", "has", "do", "does", "did", "will", "would", "should"
    }
    result = []
    for token in tokens:
        token_lower = token.lower()
        if token_lower not in stop_words and len(token_lower) > 2:
            result.append(token_lower)
    return result[:20]

def build_style_tags(style_hints: List[str], description: str = "") -> List[str]:
    """Build comprehensive style tags from hints and description."""
    tags = []
    for item in style_hints:
        if item:
            tags.append(item.strip())
    if description:
        tags.extend(extract_keywords(description))
    deduped = []
    seen = set()
    for tag in tags:
        key = tag.lower()
        if key not in seen:
            deduped.append(tag)
            seen.add(key)
    return deduped[:15]

def infer_scene_type(description: str, style_hints: List[str]) -> str:
    """Infer scene type from description."""
    text = (description + " " + " ".join(style_hints)).lower()
    if any(word in text for word in ["cinematic", "movie", "film", "dramatic"]):
        return "cinematic"
    elif any(word in text for word in ["abstract", "surreal", "dreamy"]):
        return "abstract"
    elif any(word in text for word in ["realistic", "documentary", "real"]):
        return "realistic"
    elif any(word in text for word in ["animation", "cartoon", "anime"]):
        return "animation"
    return "dynamic"

def infer_mood(description: str, style_hints: List[str]) -> str:
    """Infer mood from description."""
    text = (description + " " + " ".join(style_hints)).lower()
    if any(word in text for word in ["peaceful", "calm", "quiet", "serene"]):
        return "peaceful"
    elif any(word in text for word in ["dramatic", "intense", "powerful", "epic"]):
        return "dramatic"
    elif any(word in text for word in ["energetic", "dynamic", "fast", "action"]):
        return "energetic"
    elif any(word in text for word in ["moody", "dark", "mysterious"]):
        return "moody"
    return "immersive"

def infer_lighting(description: str, style_hints: List[str]) -> str:
    """Infer lighting style from description."""
    text = (description + " " + " ".join(style_hints)).lower()
    if any(word in text for word in ["golden", "warm", "sunset", "sunrise"]):
        return "golden hour"
    elif any(word in text for word in ["neon", "cyberpunk", "blue", "cool"]):
        return "neon glow"
    elif any(word in text for word in ["natural", "daylight", "bright"]):
        return "natural light"
    elif any(word in text for word in ["dark", "night", "shadow"]):
        return "dramatic shadow"
    return "studio light"
