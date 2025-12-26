# 部署指南

## 本地部署

### 硬件要求

| 配置项 | 最低要求 | 推荐配置 |
|--------|----------|----------|
| GPU | RTX 3080 10GB | RTX 4090 24GB |
| RAM | 16GB | 32GB+ |
| 存储 | 30GB | 50GB+ |
| CPU | 8 核 | 16 核 |

### Docker Compose 部署

创建 `docker-compose.yml`:

```yaml
version: '3.8'

services:
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - ./qdrant_storage:/qdrant/storage
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_models:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  app:
    build: .
    ports:
      - "7860:7860"
      - "8000:8000"
    depends_on:
      - qdrant
      - ollama
    environment:
      - QDRANT_HOST=qdrant
      - OLLAMA_HOST=ollama
    restart: unless-stopped
```

启动服务：

```bash
docker-compose up -d
```

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860 8000

CMD ["python", "-m", "src.app.gradio_ui"]
```

## 云服务器部署

### 阿里云 GPU 服务器

推荐配置：
- 实例规格：ecs.gn7i-c8g1.2xlarge（A10 24GB）
- 系统镜像：Ubuntu 22.04 + CUDA 12.x

### 安装步骤

```bash
# 1. 安装 Docker
curl -fsSL https://get.docker.com | sh

# 2. 安装 NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/libnvidia-container/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 3. 克隆项目并启动
git clone <your-repo>
cd llm
docker-compose up -d
```

## 性能优化

### 1. 使用 vLLM 替代 Ollama

vLLM 提供更高的推理吞吐量：

```bash
pip install vllm

python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-14B-Instruct-AWQ \
  --quantization awq \
  --gpu-memory-utilization 0.9
```

### 2. 启用 Flash Attention

```bash
pip install flash-attn --no-build-isolation
```

### 3. 使用 ONNX 加速 Embedding

```python
from optimum.onnxruntime import ORTModelForFeatureExtraction

model = ORTModelForFeatureExtraction.from_pretrained(
    "BAAI/bge-m3",
    export=True,
    provider="CUDAExecutionProvider"
)
```

## 监控与日志

### 添加 Prometheus 监控

```yaml
# docker-compose.yml 添加
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### 日志配置

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```
