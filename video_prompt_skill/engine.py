from typing import List, Optional, Dict, Any
from .utils import normalize_text, extract_keywords, build_style_tags, infer_scene_type, infer_mood, infer_lighting

class VideoPromptEngine:
    """Engine for analyzing videos and reverse-engineering/editing prompts."""
    
    def analyze_video(self, payload: Any) -> Dict[str, Any]:
        """Analyze video metadata and extract features."""
        description = normalize_text(payload.description or "")
        style_hints = [normalize_text(item) for item in (payload.style_hints or []) if normalize_text(item)]
        duration = payload.duration_seconds or 15
        fps = payload.fps or 24

        keywords = extract_keywords(description + " " + " ".join(style_hints))
        style_tags = build_style_tags(style_hints, description)

        return {
            "video_name": payload.video_name,
            "description": description,
            "style_hints": style_hints,
            "keywords": keywords,
            "style_tags": style_tags,
            "target_platform": payload.target_platform,
            "duration_seconds": duration,
            "fps": fps,
            "summary": {
                "scene": infer_scene_type(description, style_hints),
                "mood": infer_mood(description, style_hints),
                "lighting": infer_lighting(description, style_hints),
            }
        }

    def reverse_prompt(self, payload: Any) -> Dict[str, Any]:
        """Reverse-engineer a prompt from video metadata."""
        analysis = self.analyze_video(payload)
        keywords = analysis["keywords"]
        style_tags = analysis["style_tags"]

        if not keywords:
            keywords = ["cinematic", "high detail", "realistic", "smooth motion"]

        if not style_tags:
            style_tags = ["cinematic", "high quality", "dramatic lighting"]

        # Original prompt (simpler version)
        prompt = (
            f"{', '.join(style_tags)} "
            f"{', '.join(keywords[:8])}, "
            f"high detail, realistic, smooth motion, polished composition, immersive atmosphere"
        )

        # Refined prompt (optimized for video generation models)
        refined = (
            f"A {analysis['summary']['scene']} video showing {', '.join(keywords[:6])} "
            f"with {', '.join(style_tags[:4])}, "
            f"featuring {analysis['summary']['lighting']} and a {analysis['summary']['mood']} mood, "
            f"cinematic composition, realistic textures, professional camera movement, "
            f"natural depth of field, smooth transitions, ultra-detailed, high visual fidelity, "
            f"{analysis['duration_seconds']}s duration"
        )

        return {
            "video_name": payload.video_name,
            "original_prompt": prompt,
            "refined_prompt": refined,
            "keywords": keywords,
            "style_tags": style_tags,
            "confidence": 0.82,
            "analysis": analysis["summary"],
            "notes": [
                "✓ Prompt reconstructed from style hints and description.",
                "✓ Main visual cues inferred from metadata.",
                "✓ Refined version optimized for video generation models (RunwayML, Pika, Gen-2).",
                "✓ You can further customize by using /edit-prompt endpoint."
            ],
        }

    def edit_prompt(self, original_prompt: str, edits: Optional[List[str]] = None, tone: str = "cinematic", length: str = "medium", output_language: str = "en") -> Dict[str, Any]:
        """Edit and optimize a prompt based on user feedback."""
        edits = edits or []
        cleaned = normalize_text(original_prompt)

        additions = []
        for edit in edits:
            if edit:
                additions.append(normalize_text(edit))

        base = cleaned
        
        # Add edits
        if additions:
            base = f"{base}, {', '.join(additions)}"

        # Add tone
        if tone and tone.lower() not in base.lower():
            base = f"{base}, {tone} tone"

        # Add length-specific enhancement
        if length == "short":
            base = f"{base}, concise composition, quick transitions"
        elif length == "long":
            base = f"{base}, extended cinematic flow, multiple scenes, narrative progression"
        else:
            base = f"{base}, balanced composition, smooth pacing"

        # Create summary message
        if output_language.lower() == "zh":
            summary = f"✓ 已根据你提供的 {len(additions)} 项调整重写提示词。保留了主要视觉意图并增强了风格细节。"
        else:
            summary = f"✓ Prompt has been rewritten based on {len(additions)} requested edits. Original visual intent preserved with enhanced style and detail."

        return {
            "original_prompt": cleaned,
            "edited_prompt": base,
            "edits_applied": additions,
            "edits_count": len(additions),
            "tone": tone,
            "length": length,
            "summary": summary,
            "tips": [
                "Copy the edited prompt and use it in your video generation tool.",
                "You can request further edits by calling /edit-prompt again.",
                "Consider breaking long prompts into scene-by-scene descriptions for better results."
            ] if output_language.lower() == "en" else [
                "复制修改后的提示词，在你的视频生成工具中使用。",
                "你可以再次调用 /edit-prompt 进行进一步编辑。",
                "考虑将长提示词分解成场景描述，以获得更好的效果。"
            ]
        }
