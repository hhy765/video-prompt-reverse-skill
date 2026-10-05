# Video Prompt Reverse Skill - 智能体安装指南 🤖

本指南帮助你快速为智能体配置和安装 Video Prompt Reverse Skill。

## 前置要求

- Python 3.12+
- pip 或 conda
- Docker (可选，用于容器化部署)

## 安装步骤

### 步骤 1: 克隆或下载项目

```bash
# 方式 A: 使用 Git 克隆
git clone https://github.com/hhy765/video-prompt-reverse-skill.git
cd video-prompt-reverse-skill

# 方式 B: 直接下载 ZIP 并解压
# 下载链接: https://github.com/hhy765/video-prompt-reverse-skill/archive/refs/heads/main.zip
```

### 步骤 2: 安装依赖

#### 选项 A: 使用 venv (推荐)

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Linux/Mac:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

#### 选项 B: 使用 Conda

```bash
conda create -n video-prompt-skill python=3.12
conda activate video-prompt-skill
pip install -r requirements.txt
```

### 步骤 3: 启动服务

#### 方式 1: 直接运行 (开发模式)

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

输出应该显示：
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### 方式 2: 后台运行 (生产模式)

```bash
# Linux/Mac:
nohup uvicorn app:app --host 0.0.0.0 --port 8000 > skill.log 2>&1 &

# Windows (使用 PowerShell):
Start-Process -NoNewWindow -FilePath python -ArgumentList "-m uvicorn app:app --host 0.0.0.0 --port 8000"
```

#### 方式 3: Docker 容器

```bash
# 构建镜像
docker build -t video-prompt-skill:latest .

# 运行容器
docker run -p 8000:8000 \
  --name video-prompt-skill \
  -d video-prompt-skill:latest

# 查看日志
docker logs -f video-prompt-skill
```

#### 方式 4: Docker Compose

```bash
docker-compose up -d
```

### 步骤 4: 验证安装

```bash
# 健康检查
curl http://localhost:8000/healthz

# 预期响应:
# {"status":"ok","service":"video_prompt_reverse_skill"}
```

## 智能体集成示例

### 对于 Python 智能体

```python
import requests
import json

class VideoPromptAgent:
    def __init__(self, skill_url="http://localhost:8000"):
        self.skill_url = skill_url
    
    def analyze_and_reverse(self, video_description, styles):
        """分析视频并反推提示词"""
        payload = {
            "video_name": "agent_video",
            "description": video_description,
            "style_hints": styles,
            "duration_seconds": 15
        }
        
        response = requests.post(
            f"{self.skill_url}/reverse-prompt",
            json=payload
        )
        
        return response.json()["result"]
    
    def edit_prompt(self, prompt, edits, language="en"):
        """编辑提示词"""
        payload = {
            "original_prompt": prompt,
            "edits": edits,
            "output_language": language
        }
        
        response = requests.post(
            f"{self.skill_url}/edit-prompt",
            json=payload
        )
        
        return response.json()["result"]

# 使用示例
agent = VideoPromptAgent()

# 反推提示词
result = agent.analyze_and_reverse(
    video_description="A beautiful sunset over mountains",
    styles=["cinematic", "4K", "peaceful"]
)

print(f"生成的提示词：{result['refined_prompt']}")

# 进一步编辑
edited = agent.edit_prompt(
    prompt=result['original_prompt'],
    edits=["add birds flying", "add wind effects"],
    language="en"
)

print(f"编辑后的提示词：{edited['edited_prompt']}")
```

### 对于 Node.js 智能体

```javascript
const axios = require('axios');

class VideoPromptAgent {
  constructor(skillUrl = 'http://localhost:8000') {
    this.skillUrl = skillUrl;
  }

  async analyzeAndReverse(videoDescription, styles) {
    const payload = {
      video_name: 'agent_video',
      description: videoDescription,
      style_hints: styles,
      duration_seconds: 15
    };

    try {
      const response = await axios.post(
        `${this.skillUrl}/reverse-prompt`,
        payload
      );
      return response.data.result;
    } catch (error) {
      console.error('Error calling reverse-prompt:', error.message);
      throw error;
    }
  }

  async editPrompt(prompt, edits, language = 'en') {
    const payload = {
      original_prompt: prompt,
      edits: edits,
      output_language: language
    };

    try {
      const response = await axios.post(
        `${this.skillUrl}/edit-prompt`,
        payload
      );
      return response.data.result;
    } catch (error) {
      console.error('Error calling edit-prompt:', error.message);
      throw error;
    }
  }
}

// 使用示例
const agent = new VideoPromptAgent();

(async () => {
  // 反推提示词
  const result = await agent.analyzeAndReverse(
    'A beautiful sunset over mountains',
    ['cinematic', '4K', 'peaceful']
  );

  console.log('Generated prompt:', result.refined_prompt);

  // 进一步编辑
  const edited = await agent.editPrompt(
    result.original_prompt,
    ['add birds flying', 'add wind effects'],
    'en'
  );

  console.log('Edited prompt:', edited.edited_prompt);
})();
```

## 常见问题

### Q: 我该如何停止服务？

A:
```bash
# 如果在前台运行，按 Ctrl+C

# 如果是后台进程
kill <PID>  # Linux/Mac

# 如果是 Docker
docker stop video-prompt-skill
```

### Q: 如何改变服务端口？

A:
```bash
# 修改启动命令的 --port 参数
uvicorn app:app --host 0.0.0.0 --port 9000

# 或者修改 docker-compose.yml 中的 ports 配置
```

### Q: 如何与远程智能体连接？

A:
```bash
# 将 localhost 改为你的服务器 IP
# 例如: http://192.168.1.100:8000

# 确保防火墙允许 8000 端口通过
```

### Q: 如何查看详细日志？

A:
```bash
# Docker 容器
docker logs -f video-prompt-skill

# 如果运行在后台
tail -f skill.log
```

## 配置文件

修改 `.env` 文件来自定义设置：

```bash
cp .env.example .env
# 编辑 .env 文件
```

## 下一步

1. 阅读 [README.md](README.md) 了解 API 详情
2. 查看 [skill_manifest.json](skill_manifest.json) 了解 Skill 元数据
3. 探索源代码，理解实现细节
4. 根据需要扩展功能

## 支持

- 📖 完整 API 文档: 访问 http://localhost:8000/docs
- 🐛 报告问题: https://github.com/hhy765/video-prompt-reverse-skill/issues
- 💬 讨论功能: https://github.com/hhy765/video-prompt-reverse-skill/discussions
