# 数据处理流程

## 数据源概览

| 数据源 | 大小 | 格式 | 用途 |
|--------|------|------|------|
| construct3-manual.pdf | 34.5MB | PDF | 主手册文档 |
| construct3-Addon-SDK.pdf | 2.7MB | PDF | 插件开发文档 |
| zh-CN_R466.csv | 2.8MB | CSV | 23,513 条中英翻译 |
| example-projects/ | 616MB | C3 项目 | 490 个示例项目 |

## 1. PDF 手册处理

### 处理流程

```
PDF 文件
    │
    ▼
┌─────────────────┐
│ PyMuPDF 提取    │  提取文本和页码信息
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 章节结构识别     │  识别标题层级
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 语义分块        │  chunk_size: 1000, overlap: 200
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 元数据添加      │  来源、页码、章节路径
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 向量化入库      │  bge-m3 -> Qdrant
└─────────────────┘
```

### 输出格式

```json
{
  "text": "The Sprite object is used to display...",
  "metadata": {
    "source": "construct3-manual.pdf",
    "page": 42,
    "chapter": "Plugin reference",
    "section": "Sprite"
  }
}
```

## 2. i18n 翻译词条处理

### 原始格式

```
term_key,中文翻译,,,英文原文
text.behaviors.eightdir.actions.stop.list-name,停止移动,,,,Stop
```

### 处理流程

```
CSV 文件
    │
    ▼
┌─────────────────┐
│ 逐行解析        │  分隔符: 逗号
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 路径层级解析     │  text.behaviors.eightdir.actions.stop
│                 │  -> ["behaviors", "eightdir", "actions", "stop"]
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 分类标注        │  behavior/plugin/system/condition/action/expression
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 双索引构建      │  向量索引 + BM25 索引
└─────────────────┘
```

### 输出格式

```json
{
  "term_key": "text.behaviors.eightdir.actions.stop.list-name",
  "path": ["behaviors", "eightdir", "actions", "stop"],
  "category": "behaviors",
  "type": "action",
  "zh": "停止移动",
  "en": "Stop",
  "full_text": "停止移动 | Stop"
}
```

## 3. 示例项目处理

### 项目结构

```
example-projects/
├── stealth-example/
│   ├── project.c3proj         # 项目配置
│   ├── eventSheets/           # 事件表
│   │   └── eMain.json
│   ├── objectTypes/           # 对象类型
│   │   └── Player.json
│   ├── layouts/               # 布局
│   │   └── Main.json
│   └── scripts/               # 脚本
│       └── main.js
```

### 处理流程

```
项目目录
    │
    ▼
┌─────────────────┐
│ 遍历 490 项目   │
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 解析 c3proj     │  提取项目描述、插件依赖
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 解析事件表      │  eventSheets/*.json
│                 │  提取条件、动作、表达式
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 语义化转换      │  JSON -> 自然语言描述
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ 向量化入库      │
└─────────────────┘
```

### 事件表 JSON 示例

原始 JSON:
```json
{
  "eventType": "block",
  "conditions": [
    {"id": "on-start-of-layout", "objectClass": "System"}
  ],
  "actions": [
    {"id": "set-position", "objectClass": "Player", "parameters": {"x": "100", "y": "200"}}
  ]
}
```

转换为自然语言:
```
当布局开始时:
  - 设置 Player 位置为 (100, 200)
```

## 4. 数据统计预估

| 数据类型 | 原始条目 | 分块后条目 | 向量维度 |
|----------|----------|-----------|---------|
| 手册文档 | ~500 页 | ~2,000 chunks | 1024 |
| 术语表 | 23,513 条 | 23,513 条 | 1024 |
| 示例项目 | 490 项目 | ~5,000 事件 | 1024 |
| **总计** | - | ~30,500 向量 | - |

## 脚本位置

```
src/data_processing/
├── pdf_parser.py      # PDF 解析
├── csv_parser.py      # 术语表解析
├── project_parser.py  # 示例项目解析
└── indexer.py         # 向量化入库
```
