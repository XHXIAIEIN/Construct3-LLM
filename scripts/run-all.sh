#!/bin/bash
# 一键启动完整系统
# Usage: ./scripts/run-all.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo "  Construct 3 RAG Assistant - 一键启动"
echo "=========================================="
echo ""

cd "$PROJECT_ROOT"

# 步骤 1: 检查虚拟环境
echo "[1/4] 检查 Python 环境..."
if [ ! -d "venv" ]; then
    echo "首次运行，安装依赖..."
    "$SCRIPT_DIR/setup/install.sh"
fi

# 激活虚拟环境
source venv/bin/activate
echo "  ✓ Python 环境就绪"

# 步骤 2: 启动服务
echo ""
echo "[2/4] 启动后端服务..."

# 检查 Docker
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker 未运行，请先启动 Docker Desktop"
    exit 1
fi

# 启动 Qdrant（如果未运行）
if ! curl -s http://localhost:6333/collections > /dev/null 2>&1; then
    "$SCRIPT_DIR/setup/start-services.sh"
else
    echo "  ✓ Qdrant 已运行"
fi

# 检查 Ollama
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "启动 Ollama..."
    ollama serve &
    sleep 3
fi
echo "  ✓ Ollama 已运行"

# 步骤 3: 检查数据索引
echo ""
echo "[3/4] 检查数据索引..."

MANUAL_COUNT=$(curl -s "http://localhost:6333/collections/c3_manual" 2>/dev/null | grep -o '"points_count":[0-9]*' | grep -o '[0-9]*' || echo "0")
TERMS_COUNT=$(curl -s "http://localhost:6333/collections/c3_terms" 2>/dev/null | grep -o '"points_count":[0-9]*' | grep -o '[0-9]*' || echo "0")
EXAMPLES_COUNT=$(curl -s "http://localhost:6333/collections/c3_examples" 2>/dev/null | grep -o '"points_count":[0-9]*' | grep -o '[0-9]*' || echo "0")

if [ "$MANUAL_COUNT" -eq 0 ] && [ "$TERMS_COUNT" -eq 0 ] && [ "$EXAMPLES_COUNT" -eq 0 ]; then
    echo "数据库为空，开始索引数据..."
    echo "（首次运行可能需要 5-10 分钟）"
    echo ""
    "$SCRIPT_DIR/data/index-all.sh"
else
    echo "  ✓ 手册文档: $MANUAL_COUNT 条"
    echo "  ✓ 翻译术语: $TERMS_COUNT 条"
    echo "  ✓ 示例项目: $EXAMPLES_COUNT 条"
fi

# 步骤 4: 启动 Web 界面
echo ""
echo "[4/4] 启动 Web 界面..."
echo ""
echo "=========================================="
echo "  系统已就绪!"
echo "=========================================="
echo ""
echo "访问地址: http://localhost:7860"
echo "按 Ctrl+C 停止服务"
echo ""

python -m src.app.gradio_ui
