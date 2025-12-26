#!/bin/bash
# 开发模式运行（自动重载）
# Usage: ./scripts/app/run-dev.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=========================================="
echo "  开发模式 - 自动重载"
echo "=========================================="

cd "$PROJECT_ROOT"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo ""
echo "访问地址: http://localhost:7860"
echo "修改代码后会自动重载"
echo "按 Ctrl+C 停止服务"
echo ""

# 使用 watchdog 监控文件变化并重启
if command -v watchmedo &> /dev/null; then
    watchmedo auto-restart \
        --patterns="*.py" \
        --recursive \
        --directory="$PROJECT_ROOT/src" \
        -- python -m src.app.gradio_ui
else
    echo "提示: 安装 watchdog 可启用自动重载"
    echo "      pip install watchdog"
    echo ""
    python -m src.app.gradio_ui
fi
