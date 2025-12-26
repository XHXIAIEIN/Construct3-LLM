#!/bin/bash
# 启动 Gradio Web 界面
# Usage: ./scripts/app/run.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=========================================="
echo "  Construct 3 RAG Assistant"
echo "=========================================="

cd "$PROJECT_ROOT"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 检查服务状态
echo ""
echo "检查服务状态..."

# 检查 Qdrant
if ! curl -s http://${QDRANT_HOST:-localhost}:${QDRANT_PORT:-6333}/collections > /dev/null 2>&1; then
    echo "警告: Qdrant 未运行"
    echo "请先运行: ./scripts/setup/start-services.sh"
    exit 1
fi
echo "  ✓ Qdrant 正常"

# 检查 Ollama
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "警告: Ollama 未运行"
    echo "请先运行: ./scripts/setup/start-services.sh"
    exit 1
fi
echo "  ✓ Ollama 正常"

# 检查是否有数据
COLLECTIONS=$(curl -s http://${QDRANT_HOST:-localhost}:${QDRANT_PORT:-6333}/collections | grep -o '"name":"[^"]*"' | wc -l)
if [ "$COLLECTIONS" -eq 0 ]; then
    echo ""
    echo "警告: 向量数据库为空"
    echo "请先运行: ./scripts/data/index-all.sh"
    exit 1
fi
echo "  ✓ 数据已索引"

echo ""
echo "=========================================="
echo "  启动 Web 界面"
echo "=========================================="
echo ""
echo "访问地址: http://localhost:7860"
echo "按 Ctrl+C 停止服务"
echo ""

python -m src.app.gradio_ui
