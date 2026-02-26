from __future__ import annotations

import shutil
from pathlib import Path

import streamlit as st

from pipeline import PaperTranslationPipeline


APP_DIR = Path(__file__).parent
INPUT_DIR = APP_DIR / "data" / "input"
OUTPUT_DIR = APP_DIR / "data" / "output"
TERMS_PATH = APP_DIR / "config" / "terms.csv"


def save_upload(uploaded_file) -> Path:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    target = INPUT_DIR / uploaded_file.name
    with target.open("wb") as f:
        shutil.copyfileobj(uploaded_file, f)
    return target


def file_bytes(path: str) -> bytes:
    return Path(path).read_bytes()


def main() -> None:
    st.set_page_config(page_title="Paper CN Agent", layout="wide")
    st.title("英文论文 PDF -> 中文论文 PDF")
    st.caption("上传英文论文，自动执行多 Agent 翻译流水线并输出中文 PDF。")

    with st.sidebar:
        st.subheader("参数")
        translator = st.selectbox("翻译后端", options=["mock", "openai"], index=0)
        model = st.text_input("OpenAI 模型", value="gpt-4.1-mini")
        st.markdown("术语库路径")
        st.code(str(TERMS_PATH), language="text")

    uploaded = st.file_uploader("上传论文文件", type=["pdf", "txt", "md"])

    if st.button("开始转换", type="primary", disabled=uploaded is None):
        if uploaded is None:
            st.warning("请先上传文件")
            return

        input_path = save_upload(uploaded)
        st.info(f"已接收文件: {input_path.name}")

        pipeline = PaperTranslationPipeline(
            terms_path=str(TERMS_PATH),
            output_dir=str(OUTPUT_DIR),
            translator=translator,
            model=model,
        )

        with st.spinner("正在执行 Agent 网络..."):
            try:
                state = pipeline.run(str(input_path))
            except Exception as exc:
                st.error(f"转换失败: {exc}")
                return

        st.success("转换完成")
        summary = state.qa_report.get("summary", {})
        st.json(summary)

        paths = state.output_paths
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                label="下载中文 PDF",
                data=file_bytes(paths["zh_pdf"]),
                file_name=Path(paths["zh_pdf"]).name,
                mime="application/pdf",
            )
        with col2:
            st.download_button(
                label="下载中文 Markdown",
                data=file_bytes(paths["zh_markdown"]),
                file_name=Path(paths["zh_markdown"]).name,
                mime="text/markdown",
            )
        with col3:
            st.download_button(
                label="下载 QA 报告",
                data=file_bytes(paths["qa_json"]),
                file_name=Path(paths["qa_json"]).name,
                mime="application/json",
            )

        st.subheader("中文预览")
        st.text(Path(paths["zh_markdown"]).read_text(encoding="utf-8")[:4000])


if __name__ == "__main__":
    main()
