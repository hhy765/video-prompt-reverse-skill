# 🤖 智能体快速开始 - Video Prompt Reverse Skill

这是一个为 AI 智能体设计的快速集成指南。

## 1️⃣ 一键启动

```bash
# 假设你已经克隆了项目到本地
cd video-prompt-reverse-skill
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

服务会在 `http://localhost:8000` 启动。

## 2️⃣ 三个核心 API 调用

### API 1: 反推提示词 ⚡

```bash
curl -X POST http://localhost:8000/reverse-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "video_name": "my_video",
    "description": "sunset over ocean with waves",
    "style_hints": ["cinematic", "4K", "golden hour"],
    "duration_seconds": 15
  }'
```

**返回**: `original_prompt` + `refined_prompt` + 置信度

---

### API 2: 编辑提示词 ✏️

```bash
curl -X POST http://localhost:8000/edit-prompt \
  -H "Content-Type: application/json" \
  -d '{
    "original_prompt": "cinematic sunset, golden light, realistic, smooth motion",
    "edits": [
      "add dramatic clouds",
      "add seagulls flying in the distance",
      "enhance color saturation"
    ],
    "tone": "cinematic",
    "length": "medium",
    "output_language": "en"
  }'
```

**返回**: 编辑后的提示词 + 修改摘要

---

### API 3: 视频分析 🔍

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "video_name": "my_video",
    "description": "beautiful landscape",
    "style_hints": ["nature", "4K"],
    "target_platform": "runway"
  }'
```

**返回**: 关键词、风格标签、推断的场景/情绪/光影

---

## 3️⃣ 在你的智能体中使用

### Python 示例

```python
import requests

# 第 1 步：反推提示词
reverse_response = requests.post(
    "http://localhost:8000/reverse-prompt",
    json={
        "video_name": "user_request",
        "description": "user_video_description",
        "style_hints": ["style1", "style2"],
    }
)
prompt_data = reverse_response.json()["result"]
generated_prompt = prompt_data["refined_prompt"]

# 第 2 步：用户反馈 → 编辑提示词
edit_response = requests.post(
    "http://localhost:8000/edit-prompt",
    json={
        "original_prompt": generated_prompt,
        "edits": ["user_requested_change_1", "user_requested_change_2"],
    }
)
final_prompt = edit_response.json()["result"]["edited_prompt"]

# 第 3 步：将最终提示词发送给视频生成 API
print(f"Final prompt for video generation: {final_prompt}")
```

### JavaScript 示例

```javascript
const skillUrl = "http://localhost:8000";

// 步骤 1: 反推提示词
const reverseResponse = await fetch(`${skillUrl}/reverse-prompt`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    video_name: "user_request",
    description: "user_video_description",
    style_hints: ["style1", "style2"],
  }),
});
const promptData = await reverseResponse.json();
const generatedPrompt = promptData.result.refined_prompt;

// 步骤 2: 编辑提示词
const editResponse = await fetch(`${skillUrl}/edit-prompt`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    original_prompt: generatedPrompt,
    edits: ["user_requested_change_1"],
  }),
});
const finalPrompt = (await editResponse.json()).result.edited_prompt;

console.log(`Final prompt: ${finalPrompt}`);
```

---

## 4️⃣ 响应格式一览

### /reverse-prompt 响应

```json
{
  "success": true,
  "result": {
    "video_name": "my_video",
    "original_prompt": "...",           // 简化版
    "refined_prompt": "...",             // 优化版（推荐使用）
    "keywords": ["key1", "key2", ...],  // 提取的关键词
    "style_tags": ["tag1", "tag2", ...],// 风格标签
    "confidence": 0.82,                  // 置信度 (0-1)
    "analysis": {                        // 推断分析
      "scene": "cinematic",
      "mood": "immersive",
      "lighting": "golden hour"
    },
    "notes": ["Note 1", "Note 2", ...]  // 辅助说明
  }
}
```

### /edit-prompt 响应

```json
{
  "success": true,
  "result": {
    "original_prompt": "...",
    "edited_prompt": "...",              // 修改后的提示词
    "edits_applied": ["edit1", "edit2"], // 应用的修改列表
    "edits_count": 2,                    // 修改数量
    "summary": "✓ Prompt has been ...",  // 修改摘要
    "tips": ["Tip 1", "Tip 2", ...]     // 使用建议
  }
}
```

---

## 5️⃣ 智能体工作流示例

```
用户请求
    ↓
智能体收集信息
    ├─ 视频描述
    ├─ 风格偏好
    └─ 技术参数
    ↓
调用 /reverse-prompt
    ↓
获取初始提示词
    ↓
[用户审查和反馈]
    ↓
调用 /edit-prompt (如果需要修改)
    ↓
获得最终提示词
    ↓
发送给视频生成模型
    ↓
生成视频
```

---

## 6️⃣ 常见集成场景

### 场景 A: 一键生成视频提示词

```python
def generate_video_prompt(user_description):
    response = requests.post(
        "http://localhost:8000/reverse-prompt",
        json={
            "video_name": "auto_generated",
            "description": user_description,
            "style_hints": ["cinematic", "4K"],
        }
    )
    return response.json()["result"]["refined_prompt"]
```

### 场景 B: 交互式提示词编辑器

```python
def iterative_prompt_refinement(initial_prompt):
    current_prompt = initial_prompt
    
    while True:
        print(f"Current prompt: {current_prompt}\n")
        user_feedback = input("Provide feedback (or 'done' to finish): ")
        
        if user_feedback.lower() == "done":
            break
        
        response = requests.post(
            "http://localhost:8000/edit-prompt",
            json={
                "original_prompt": current_prompt,
                "edits": [user_feedback],
            }
        )
        
        current_prompt = response.json()["result"]["edited_prompt"]
    
    return current_prompt
```

### 场景 C: 批量提示词处理

```python
def batch_process_videos(videos_data):
    results = []
    
    for video in videos_data:
        response = requests.post(
            "http://localhost:8000/reverse-prompt",
            json={
                "video_name": video["name"],
                "description": video["description"],
                "style_hints": video.get("styles", []),
            }
        )
        
        results.append({
            "video_name": video["name"],
            "prompt": response.json()["result"]["refined_prompt"]
        })
    
    return results
```

---

## 7️⃣ 故障排除

| 问题 | 解决方案 |
|------|--------|
| 连接被拒绝 | 确保服务正在运行: `uvicorn app:app --host 0.0.0.0 --port 8000` |
| 404 错误 | 检查端点拼写，确保使用 `/reverse-prompt` 而不是其他 |
| JSON 解析错误 | 确保请求体是有效的 JSON 格式 |
| 响应为空 | 检查必需字段 `video_name` 和 `description` 是否提供 |

---

## 📚 更多资源

- 完整 API 文档: `http://localhost:8000/docs`
- 本地 Swagger UI: `http://localhost:8000/swagger/docs`
- 详细指南: 查看 [README.md](README.md)
- 完整安装指南: 查看 [INSTALL_GUIDE.md](INSTALL_GUIDE.md)

---

🎉 现在你已经准备好在智能体中使用 Video Prompt Reverse Skill！
