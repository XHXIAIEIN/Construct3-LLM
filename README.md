# Construct 3 RAG 助手

基于 RAG（检索增强生成）技术的 Construct 3 游戏引擎知识库助手。

## 功能

- **文档问答**: 回答 Construct 3 使用相关问题，并标注来源
- **术语翻译**: 中英术语查询，保持与官方翻译一致
- **代码生成**: 根据需求生成 Construct 3 事件表代码

## 数据来源

| 文件 | 说明 |
|------|------|
| `mate/construct3-manual.pdf` | 官方手册 (34.5MB) |
| `mate/construct3-Addon-SDK.pdf` | 插件开发文档 (2.7MB) |
| `mate/zh-CN_R466.csv` | 编辑器中英翻译词条 (23,513 条) |
| `mate/Construct-Example-Projects-main/` | 官方示例项目 (490 个) |
| `mate/manual-1.xml` | 手册结构 sitemap |

原始 sitemap URL: https://www.construct.net/sitemaps/manual-1.xml

## 技术栈

| 组件 | 选择 |
|------|------|
| LLM | Qwen2.5-14B (Ollama) |
| 向量数据库 | Qdrant |
| Embedding | BAAI/bge-m3 |
| 框架 | LangChain |
| 前端 | Gradio |

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# 3. 安装 Ollama 并拉取模型
ollama pull qwen2.5:14b

# 4. 处理数据并入库
python -m src.data_processing.sitemap_parser  # 解析手册结构
python -m src.data_processing.pdf_parser      # 处理 PDF
python -m src.data_processing.csv_parser      # 处理术语表
python -m src.data_processing.indexer         # 向量入库

# 5. 启动 Web 界面
python -m src.app.gradio_ui
```

## 项目结构

```
llm/
├── doc/                    # 文档
│   ├── design/            # 设计文档
│   │   ├── architecture.md
│   │   ├── data-processing.md
│   │   └── implementation-plan.md
│   └── guides/            # 使用指南
│       ├── quick-start.md
│       └── deployment.md
├── mate/                   # 训练数据
│   ├── construct3-manual.pdf
│   ├── construct3-Addon-SDK.pdf
│   ├── zh-CN_R466.csv
│   ├── manual-1.xml
│   └── Construct-Example-Projects-main/
├── src/                    # 源代码
│   ├── data_processing/   # 数据处理
│   ├── rag/               # RAG 系统
│   └── app/               # Web 应用
└── requirements.txt
```

## 文档

- [系统架构](doc/design/architecture.md)
- [数据处理流程](doc/design/data-processing.md)
- [实施计划](doc/design/implementation-plan.md)
- [快速开始指南](doc/guides/quick-start.md)
- [部署指南](doc/guides/deployment.md)
