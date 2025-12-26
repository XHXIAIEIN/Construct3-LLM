#!/bin/bash
# 查看系统状态
# Usage: ./scripts/status.sh

echo "=========================================="
echo "  系统状态"
echo "=========================================="
echo ""

# Docker 状态
echo "Docker:"
if docker info > /dev/null 2>&1; then
    echo "  ✓ 运行中"
else
    echo "  ✗ 未运行"
fi

# Qdrant 状态
echo ""
echo "Qdrant (向量数据库):"
if curl -s http://localhost:6333/collections > /dev/null 2>&1; then
    echo "  ✓ 运行中 - http://localhost:6333"

    # 显示集合信息
    echo ""
    echo "  数据集合:"

    for collection in c3_manual c3_terms c3_examples; do
        COUNT=$(curl -s "http://localhost:6333/collections/$collection" 2>/dev/null | grep -o '"points_count":[0-9]*' | grep -o '[0-9]*' || echo "N/A")
        if [ "$COUNT" != "N/A" ]; then
            echo "    - $collection: $COUNT 条记录"
        else
            echo "    - $collection: 未创建"
        fi
    done
else
    echo "  ✗ 未运行"
fi

# Ollama 状态
echo ""
echo "Ollama (LLM 推理):"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "  ✓ 运行中 - http://localhost:11434"

    # 显示已安装的模型
    echo ""
    echo "  已安装模型:"
    ollama list 2>/dev/null | tail -n +2 | while read -r line; do
        echo "    - $line"
    done
else
    echo "  ✗ 未运行"
fi

# Python 环境
echo ""
echo "Python 环境:"
if [ -d "venv" ]; then
    echo "  ✓ 虚拟环境存在: venv/"
else
    echo "  ✗ 虚拟环境未创建"
fi

echo ""
echo "=========================================="
