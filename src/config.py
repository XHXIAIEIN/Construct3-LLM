"""
Construct 3 RAG Assistant Configuration

支持环境变量覆盖默认配置:
  - LLM_MODEL: Ollama 模型名称 (默认 qwen2.5:7b)
  - QDRANT_HOST: Qdrant 地址 (默认 localhost)
  - EMBEDDING_MODEL: 嵌入模型 (默认 BAAI/bge-m3)
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "mate"

# Data Sources
PDF_MANUAL = DATA_DIR / "construct3-manual.pdf"
PDF_SDK = DATA_DIR / "construct3-Addon-SDK.pdf"
CSV_TERMS = DATA_DIR / "zh-CN_R466.csv"
EXAMPLE_PROJECTS_DIR = DATA_DIR / "Construct-Example-Projects-main" / "example-projects"
SITEMAP_FILE = DATA_DIR / "manual-1.xml"

# Vector Database
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
COLLECTION_MANUAL = "c3_manual"
COLLECTION_TERMS = "c3_terms"
COLLECTION_EXAMPLES = "c3_examples"

# Embedding Model
# 可选: BAAI/bge-m3 (多语言), BAAI/bge-large-zh-v1.5 (中文优化)
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
EMBEDDING_DIMENSION = 1024

# LLM Configuration (Ollama)
# Mac M4 24GB 推荐: qwen2.5:7b (速度快) 或 qwen2.5:14b (效果好)
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:7b")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")

# Chunking Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval Settings
TOP_K = 5
