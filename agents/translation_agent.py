from __future__ import annotations

import os

from .types import Segment


class TranslationAgent:
    def __init__(self, translator: str = "mock", model: str = "gpt-4.1-mini") -> None:
        self.translator = translator
        self.model = model

    def _mock_translate(self, text: str) -> str:
        # 离线可运行的占位翻译，便于先打通工作流。
        return f"[中文草稿] {text}"

    def _openai_translate(self, text: str, term_hints: list[dict[str, str]] | None) -> str:
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")

        client = OpenAI(api_key=api_key)
        term_text = ""
        if term_hints:
            pairs = [f"{t['en']}=>{t['zh']}" for t in term_hints]
            term_text = "术语约束: " + "; ".join(pairs)

        prompt = (
            "请把以下英文学术段落翻译为中文学术表达，保持数字、单位、公式、引用编号不变。"
            f"{term_text}\n\n英文原文:\n{text}"
        )

        resp = client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0,
        )
        return resp.output_text.strip()

    def run(self, segments: list[Segment]) -> list[Segment]:
        for seg in segments:
            hints = seg.meta.get("term_hints", [])
            if self.translator == "openai":
                seg.text_zh = self._openai_translate(seg.text_en, hints)
            else:
                seg.text_zh = self._mock_translate(seg.text_en)
        return segments
