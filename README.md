# Construct 3 RAG 助手

基于 RAG（检索增强生成）技术的 Construct 3 游戏引擎知识库助手。

## 功能

- **文档问答**: 回答 Construct 3 使用相关问题，并标注来源
- **术语翻译**: 中英术语查询，保持与官方翻译一致
- **代码生成**: 根据需求生成 Construct 3 事件表代码

---

## RAG 原理

**RAG = Retrieval-Augmented Generation（检索增强生成）**

| 方式 | 问题 |
|------|------|
| 纯 LLM | AI 只能凭"记忆"回答，可能过时或瞎编 |
| RAG | AI 先去"翻书"找到相关资料，再基于资料回答 |

RAG 就像给 AI 配了一个**即时查阅资料库的能力**。

### 工作流程

```
用户提问 ──→ ① 检索 ──→ ② 增强 ──→ ③ 生成 ──→ 回答
              │          │          │
              ↓          ↓          ↓
           向量数据库   拼接上下文    LLM
```

### 数据准备（离线，只做一次）

```
原始文档              分块                   向量化                存储
(Markdown/CSV)  ──→  按 H2 标题切分  ──→  转成数字向量  ──→  Qdrant 数据库
```

### 什么是向量化？

**向量化 = 把文字转换成一串数字（语义指纹）**

```
"苹果"  →  [0.12, -0.45, 0.78, ...]   (1024个数字)
"水果"  →  [0.15, -0.42, 0.75, ...]   (很接近！)
"汽车"  →  [0.89, 0.12, -0.56, ...]   (完全不同)
```

意思相近的词，向量距离近；意思不同的词，向量距离远。

搜索时，把用户问题也转成向量，找数据库里最接近的文档——这就是**语义搜索**。

### 什么是分块？

**分块 = 把长文档切成小段落**

本项目按 H2 标题切分，每个 H2 段落成为一个独立的"文档块"：

```markdown
# Sprite                              ← H1（文件级别）

## Sprite properties（属性）          ← H2 → 第 1 块
## Sprite conditions（条件）          ← H2 → 第 2 块
## Sprite actions（动作）             ← H2 → 第 3 块
```

每个块保留元数据（来源、标题、分类），回答时可以标注出处。

---

## 架构图

```
┌─────────────────────────────────────────────────────────┐
│                      Gradio Web 界面                      │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    RAGChain (chain.py)                   │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │ 问题分类      │ → │ 检索上下文    │ → │ LLM 生成   │ │
│  │ (qa/翻译/代码)│    │ (多集合搜索)  │    │ (Qwen3)   │ │
│  └──────────────┘    └──────────────┘    └───────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              HybridRetriever (retriever.py)              │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Qdrant 向量数据库                        │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │c3_guide │ │c3_plugins│ │c3_terms │ │c3_examples│      │
│  │入门教程  │ │插件参考  │ │术语翻译  │ │示例代码   │      │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │
└─────────────────────────────────────────────────────────┘
```

---

## 数据来源

| 来源 | 说明 |
|------|------|
| `../Construct3-Manual/` | Markdown 格式手册 (334 文件) |
| `source/zh-CN_R466.csv` | 编辑器中英翻译词条 (23,513 条) |
| `../Construct-Example-Projects-main/` | 官方示例项目 (490 个) |

## 向量集合

| 集合 | 内容 |
|------|------|
| `c3_guide` | 入门教程 + 概述 + 技巧指南 |
| `c3_interface` | 编辑器界面 (工具栏/对话框/调试器) |
| `c3_project` | 项目元素 (事件/对象/时间轴) |
| `c3_plugins` | 插件参考 (Sprite/Audio/Array 等) |
| `c3_behaviors` | 行为参考 (Platform/Physics/Tween 等) |
| `c3_scripting` | 脚本 API (JavaScript/TypeScript) |
| `c3_terms` | 官方术语翻译 |
| `c3_examples` | 示例项目代码 |

---

## 技术栈

| 组件 | 选择 | 说明 |
|------|------|------|
| LLM | Qwen3:30b | 本地运行，通过 Ollama |
| 向量数据库 | Qdrant | 高性能向量搜索 |
| Embedding | BAAI/bge-m3 | 多语言嵌入模型，1024 维 |
| 分块策略 | H2 语义分块 | 按文档结构切分 |
| 框架 | LangChain | RAG 编排框架 |
| 前端 | Gradio | 快速搭建 Web 界面 |

---

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

---

## 项目结构

```
Construct3-LLM/
├── src/
│   ├── config.py              # 全局配置
│   ├── collections.py         # 集合定义 + 目录映射 + 子分类
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
├── doc/
│   └── guides/
│       └── rag-introduction.md # RAG 详细原理讲解
├── source/                    # 数据文件
└── requirements.txt

../Construct3-Manual/          # 外部仓库 (Markdown 文档)
├── Construct3-Manual/         # 手册 (334 文件)
└── Construct3-Addon-SDK/      # SDK 文档 (62 文件)
```

## 关键组件

| 组件 | 文件 | 作用 |
|------|------|------|
| 配置 | `config.py` | 模型路径、数据库地址 |
| 集合定义 | `collections.py` | 向量集合名称、目录映射、子分类 |
| 解析器 | `markdown_parser.py` | Markdown → 小块文本 |
| 索引器 | `indexer.py` | 文本 → 向量 → 存入 Qdrant |
| 检索器 | `retriever.py` | 问题 → 向量 → 搜索相似文档 |
| 生成链 | `chain.py` | 组合检索结果 + LLM 生成回答 |
| 界面 | `gradio_ui.py` | Web 交互界面 |

---

## 更多文档

- [RAG 详细原理讲解](doc/guides/rag-introduction.md) - 向量化、分块、检索的深入解释

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
