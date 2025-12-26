"""
Construct 3 RAG Assistant - 极简界面
"""
import gradio as gr

try:
    from src.rag.chain import RAGChain
    from src.config import QDRANT_HOST, QDRANT_PORT, LLM_MODEL, LLM_BASE_URL
except ImportError:
    import sys
    sys.path.insert(0, str(__file__).rsplit('/src/', 1)[0])
    from src.rag.chain import RAGChain
    from src.config import QDRANT_HOST, QDRANT_PORT, LLM_MODEL, LLM_BASE_URL

_rag = None

CSS = """
.container { max-width: 800px; margin: 0 auto; }
.title { text-align: center; font-weight: 300; margin: 20px 0; }
.input-box textarea { border: 1px solid #ddd !important; border-radius: 4px !important; }
.input-box textarea:focus { border-color: #888 !important; box-shadow: none !important; }
.output-box { border: 1px solid #eee; border-radius: 4px; padding: 16px;
              min-height: 300px; max-height: 60vh; overflow-y: auto;
              background: #fafafa; font-size: 14px; line-height: 1.6; }
.output-box:empty::before { content: "回答将显示在这里..."; color: #999; }
.submit-btn { border: 1px solid #333 !important; background: white !important;
              color: #333 !important; border-radius: 4px !important; }
.submit-btn:hover { background: #333 !important; color: white !important; }
footer { display: none !important; }
"""


def get_rag():
    global _rag
    if _rag is None:
        _rag = RAGChain(
            qdrant_host=QDRANT_HOST,
            qdrant_port=QDRANT_PORT,
            llm_model=LLM_MODEL,
            llm_base_url=LLM_BASE_URL
        )
    return _rag


def ask(question: str) -> str:
    if not question.strip():
        return ""
    return get_rag().answer(question).answer


def main():
    print("加载模型...")
    rag = get_rag()
    _ = rag.retriever.embedder
    print("就绪")

    with gr.Blocks(title="LLM") as demo:
        gr.HTML("<h2 class='title'>LLM</h2>")

        with gr.Column(elem_classes="container"):
            inp = gr.Textbox(
                placeholder="输入问题...",
                label=None,
                lines=2,
                elem_classes="input-box"
            )
            btn = gr.Button("提交", elem_classes="submit-btn")
            out = gr.HTML(elem_classes="output-box")

        def format_output(q):
            answer = ask(q)
            # 转换换行为 <br>，保留格式
            return answer.replace("\n", "<br>") if answer else ""

        btn.click(format_output, inp, out)
        inp.submit(format_output, inp, out)

    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        mcp_server=True,
        css=CSS
    )


if __name__ == "__main__":
    main()
