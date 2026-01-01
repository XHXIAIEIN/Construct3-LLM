# Construct 3 RAG 助手

基于 RAG（检索增强生成）技术的 Construct 3 游戏引擎知识库助手。

## 功能

- **文档问答**: 回答 Construct 3 使用相关问题，并标注来源
- **术语翻译**: 中英术语查询，保持与官方翻译一致
- **代码生成**: 根据需求生成 Construct 3 事件表代码

## 数据来源

| 来源 | 说明 |
|------|------|
| `../Construct3-Manual/` | Markdown 格式手册 (334 文件) |
| `source/zh-CN_R466.csv` | 编辑器中英翻译词条 (23,513 条) |
| `source/Construct-Example-Projects-main/` | 官方示例项目 (490 个) |

## 向量集合

| 集合 | 内容 | Chunks |
|------|------|--------|
| `c3_guide` | 入门教程 + 概述 + 技巧指南 | 121 |
| `c3_interface` | 编辑器界面 (工具栏/对话框/调试器) | 146 |
| `c3_project` | 项目元素 (事件/对象/时间轴) | 136 |
| `c3_plugins` | 插件参考 (Sprite/Audio/Array 等) | 420 |
| `c3_behaviors` | 行为参考 (Platform/Physics/Tween 等) | 156 |
| `c3_scripting` | 脚本 API (JavaScript/TypeScript) | 201 |
| `c3_terms` | 官方术语翻译 | - |
| `c3_examples` | 示例项目代码 | - |

## 技术栈

| 组件 | 选择 |
|------|------|
| LLM | Qwen3:30b (Ollama) |
| 向量数据库 | Qdrant |
| Embedding | BAAI/bge-m3 (1024 维) |
| 分块策略 | H2 语义分块 |
| 框架 | LangChain |
| 前端 | Gradio |

## 快速开始

```bash
# 1. 克隆相关仓库
git clone <this-repo>
git clone <Construct3-Manual-repo>  # 放在同级目录

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动 Qdrant
docker run -d -p 6333:6333 qdrant/qdrant

# 4. 安装 Ollama 并拉取模型
ollama pull qwen3:30b

# 5. 索引数据
python -m src.data_processing.indexer --rebuild

# 6. 启动 Web 界面
python -m src.app.gradio_ui
```

## 项目结构

```
Construct3-LLM/
├── src/
│   ├── collections.py         # 集合配置 (8 集合 + 映射)
│   ├── config.py              # 全局配置
│   ├── data_processing/
│   │   ├── markdown_parser.py # Markdown 解析 + H2 分块
│   │   ├── csv_parser.py      # 术语表解析
│   │   ├── project_parser.py  # 示例项目解析
│   │   └── indexer.py         # 向量索引
│   ├── rag/
│   │   ├── retriever.py       # 多集合检索
│   │   ├── chain.py           # RAG 链
│   │   └── prompts.py         # 提示词模板
│   └── app/
│       └── gradio_ui.py       # Web 界面
├── source/                    # 数据文件
├── doc/                       # 文档
└── requirements.txt

../Construct3-Manual/          # 外部仓库 (Markdown 文档)
├── Construct3-Manual/         # 手册 (334 文件)
└── Construct3-Addon-SDK/      # SDK 文档 (62 文件)
```

## 配置

集合和目录映射在 `src/collections.py` 中配置：

```python
# 目录 → 集合映射
DIR_TO_COLLECTION = {
    "getting-started": COLLECTION_GUIDE,
    "plugin-reference": COLLECTION_PLUGINS,
    "scripting": COLLECTION_SCRIPTING,
    # ...
}

# 子分类映射 (用于 metadata)
SUBCATEGORY_MAPPING = {
    "plugin-reference": {
        "sprite": "visual",
        "audio": "audio",
        "array": "data",
        # ...
    }
}
```

## License

MIT
