# Video Prompt Reverse Skill 🎬

一个轻量级 Python Skill，用于反推视频生成提示词并支持交互式编辑和优化。

## 功能特性

✅ **反推视频提示词** - 从视频描述、风格线索自动生成视频生成提示词  
✅ **提示词编辑** - 对已有提示词进行修改、优化和增强  
✅ **元数据分析** - 提取关键词、风格标签、气氛、光影设置  
✅ **多语言支持** - 中文和英文提示词生成  
✅ **快速部署** - 支持本地运行、Docker 容器化、直接安装  

## 快速开始

### 方式 1: 本地 Python 环境

```bash
# 克隆仓库
git clone https://github.com/hhy765/video-prompt-reverse-skill.git
cd video-prompt-reverse-skill

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 方式 2: Docker 运行

```bash
# 构建镜像
docker build -t video-prompt-skill .

# 运行容器
docker run -p 8000:8000 video-prompt-skill
```

### 方式 3: Docker Compose

```bash
docker-compose up
```

## API 使用指南

### 1. 健康检查

```bash
curl http://localhost:8000/healthz
```

响应：
```json
{"status": "ok", "service": "video_prompt_reverse_skill"}
```

### 2. 反推视频提示词

**端点:** `POST /reverse-prompt`

请求示例：
```bash
curl -X POST http://localhost:8000/reverse-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "video_name": "sunset_city",
    "description": "a cinematic city at sunset with warm light and moving traffic",
    "style_hints": ["cinematic", "warm colors", "golden hour"],
    "target_platform": "gen-video",
    "duration_seconds": 12,
    "fps": 24
  }'
```

响应示例：
```json
{
  "success": true,
  "result": {
    "video_name": "sunset_city",
    "original_prompt": "cinematic, warm colors, golden hour, city, sunset, realistic, smooth motion, polished composition, immersive atmosphere",
    "refined_prompt": "A cinematic video showing city, sunset, warm colors, golden hour, featuring golden hour lighting and a immersive mood, cinematic composition, realistic textures, professional camera movement, natural depth of field, smooth transitions, ultra-detailed, high visual fidelity, 12s duration",
    "keywords": ["cinematic", "city", "sunset", "warm", "light", "traffic"],
    "style_tags": ["cinematic", "warm colors", "golden hour"],
    "confidence": 0.82,
    "analysis": {
      "scene": "cinematic",
      "mood": "immersive",
      "lighting": "golden hour"
    },
    "notes": [
      "✓ Prompt reconstructed from style hints and description.",
      "✓ Main visual cues inferred from metadata.",
      "✓ Refined version optimized for video generation models (RunwayML, Pika, Gen-2).",
      "✓ You can further customize by using /edit-prompt endpoint."
    ]
  }
}
```

### 3. 编辑和优化提示词

**端点:** `POST /edit-prompt`

请求示例：
```bash
curl -X POST http://localhost:8000/edit-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "original_prompt": "cinematic city, golden hour, realistic lighting",
    "edits": [
      "add more dramatic composition",
      "include neon reflections",
      "slow camera movement",
      "add depth of field effect"
    ],
    "tone": "cinematic",
    "length": "medium",
    "output_language": "en"
  }'
```

响应示例：
```json
{
  "success": true,
  "result": {
    "original_prompt": "cinematic city, golden hour, realistic lighting",
    "edited_prompt": "cinematic city, golden hour, realistic lighting, add more dramatic composition, include neon reflections, slow camera movement, add depth of field effect, cinematic tone, balanced composition, smooth pacing",
    "edits_applied": [
      "add more dramatic composition",
      "include neon reflections",
      "slow camera movement",
      "add depth of field effect"
    ],
    "edits_count": 4,
    "tone": "cinematic",
    "length": "medium",
    "summary": "✓ Prompt has been rewritten based on 4 requested edits. Original visual intent preserved with enhanced style and detail.",
    "tips": [
      "Copy the edited prompt and use it in your video generation tool.",
      "You can request further edits by calling /edit-prompt again.",
      "Consider breaking long prompts into scene-by-scene descriptions for better results."
    ]
  }
}
```

### 4. 视频分析

**端点:** `POST /analyze`

请求示例：
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_name": "test_video",
    "description": "beautiful landscape with mountains and rivers",
    "style_hints": ["nature", "4K", "peaceful"],
    "target_platform": "runway",
    "duration_seconds": 30,
    "fps": 30
  }'
```

## 参数说明

### AnalysisRequest / PromptRequest

| 参数 | 类型 | 必须 | 说明 |
|------|------|------|------|
| `video_name` | string | ✅ | 视频名称或ID |
| `description` | string | ❌ | 视频描述 |
| `style_hints` | array | ❌ | 风格提示 (如: ["cinematic", "warm colors"]) |
| `target_platform` | string | ❌ | 目标平台 (默认: "gen-video") |
| `duration_seconds` | integer | ❌ | 视频时长秒数 (默认: 15) |
| `fps` | integer | ❌ | 帧率 (默认: 24) |

### PromptEditRequest

| 参数 | 类型 | 必须 | 说明 |
|------|------|------|------|
| `original_prompt` | string | ✅ | 原始提示词 |
| `edits` | array | ❌ | 编辑清单 |
| `tone` | string | ❌ | 语气风格 (默认: "cinematic") |
| `length` | string | ❌ | 长度级别: short/medium/long (默认: "medium") |
| `output_language` | string | ❌ | 输出语言: en/zh (默认: "en") |

## 用于智能体集成

如果你想在 AI 智能体中集成这个 Skill，可以这样使用：

### Python 集成示例

```python
import requests

SKILL_URL = "http://localhost:8000"

def reverse_video_prompt(video_description, style_hints):
    """反推视频提示词"""
    response = requests.post(
        f"{SKILL_URL}/reverse-prompt",
        json={
            "video_name": "agent_generated_video",
            "description": video_description,
            "style_hints": style_hints,
            "duration_seconds": 15
        }
    )
    return response.json()["result"]

def edit_video_prompt(original_prompt, edits):
    """编辑视频提示词"""
    response = requests.post(
        f"{SKILL_URL}/edit-prompt",
        json={
            "original_prompt": original_prompt,
            "edits": edits,
            "output_language": "en"
        }
    )
    return response.json()["result"]

# 使用示例
prompt_result = reverse_video_prompt(
    video_description="beautiful sunset over the ocean",
    style_hints=["cinematic", "4K", "warm colors"]
)

print(f"Original Prompt: {prompt_result['original_prompt']}")
print(f"Refined Prompt: {prompt_result['refined_prompt']}")

# 进一步编辑
edited_result = edit_video_prompt(
    original_prompt=prompt_result['original_prompt'],
    edits=["add dramatic clouds", "add seagulls flying"]
)

print(f"Edited Prompt: {edited_result['edited_prompt']}")
```

## 项目结构

```
video-prompt-reverse-skill/
├── app.py                      # FastAPI 应用入口
├── requirements.txt            # 依赖项
├── Dockerfile                  # Docker 配置
├── docker-compose.yml          # Docker Compose 配置
├── skill_manifest.json         # Skill 清单
├── README.md                   # 本文件
└── video_prompt_skill/
    ├── __init__.py             # 包初始化
    ├── engine.py               # 核心引擎
    ├── schema.py               # 数据结构
    └── utils.py                # 工具函数
```

## 扩展建议

未来可以添加以下功能：

- [ ] 真实视频处理（FFmpeg 帧提取）
- [ ] 音频分析（Whisper ASR）
- [ ] 图像识别（OpenCV / Vision API）
- [ ] 更强大的 AI 驱动提示词生成（调用 OpenAI/Claude）
- [ ] 前端 UI 界面
- [ ] 提示词模板库
- [ ] 版本管理和历史记录

## 许可证

MIT

## 支持

如有问题或建议，欢迎提交 Issue 或 PR！
