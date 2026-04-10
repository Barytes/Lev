# AI Agent Loop

一个轻量的 agent loop 核心模块，支持工具调用（网络搜索、网页阅读）。

## 功能

- **Agent Loop**: 自动处理 LLM 的工具调用，最多循环 5 次
- **Web Search**: 使用 Tavily 搜索引擎搜索网络信息
- **Read Page**: 获取网页内容并提取纯文本

## 项目结构

```
client.py        - AI Builders Space API 配置和客户端
tools.py         - 工具函数定义（web_search, read_page）和 Function Schema
main.py          - 核心 agent loop 与 CLI 入口
.env             - 环境变量配置（BUILDER_API_KEY）
```

## 快速开始

### 1. 安装依赖

```bash
uv pip install openai python-dotenv httpx beautifulsoup4 lxml pydantic
```

### 2. 配置环境变量

在 `my-agent-loop/` 目录下创建 `.env` 文件：

```
BUILDER_API_KEY=your_api_key_here
```

`client.py` 会显式读取这个本地 `.env` 文件。

### 3. 运行一次 agent loop

```bash
python main.py "Who won the Super Bowl 2025?"
```

### 4. 作为模块导入

```python
from main import ChatRequest, chat

response = chat(ChatRequest(message="Search for the latest Python release."))
print(response.response)
```

## 示例对话

- "Who won the Super Bowl 2025?" → 自动搜索网络并返回答案
- "Search for the latest release of Python, then read the official changelog page to tell me the new features." → 搜索 + 读网页 + 总结

## 技术栈

- **AI API**: AI Builders Space (https://space.ai-builders.com/backend/v1)
- **Runtime**: Python module + CLI
- **Tools**: Tavily Search, BeautifulSoup
