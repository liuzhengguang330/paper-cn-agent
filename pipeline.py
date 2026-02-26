from __future__ import annotations

import json
from pathlib import Path

from agents.ingest_agent import IngestAgent
from agents.qa_agent import QAAgent
from agents.segmentation_agent import SegmentationAgent
from agents.style_agent import StyleAgent
from agents.terminology_agent import TerminologyAgent
from agents.translation_agent import TranslationAgent
from agents.types import PipelineState
from exporters.pdf_exporter import ChinesePdfExporter


class PaperTranslationPipeline:
    def __init__(
        self,
        terms_path: str,
        output_dir: str,
        translator: str = "mock",
        model: str = "gpt-4.1-mini",
    ) -> None:
        self.ingest = IngestAgent()
        self.segmenter = SegmentationAgent()
        self.terms_agent = TerminologyAgent(terms_path=terms_path)
        self.translator = TranslationAgent(translator=translator, model=model)
        self.styler = StyleAgent()
        self.qa = QAAgent()
        self.pdf_exporter = ChinesePdfExporter()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, input_path: str) -> PipelineState:
        state = PipelineState(input_path=input_path)

        state.raw_text = self.ingest.run(input_path)
        state.segments = self.segmenter.run(state.raw_text)
        state.segments = self.terms_agent.run(state.segments)
        state.segments = self.translator.run(state.segments)
        state.segments = self.styler.run(state.segments)
        state.qa_report = self.qa.run(state.segments, self.terms_agent.terms)

        state.output_paths = self._export(state)
        return state

    def _export(self, state: PipelineState) -> dict[str, str]:
        stem = Path(state.input_path).stem

        zh_path = self.output_dir / f"{stem}.zh.md"
        bi_path = self.output_dir / f"{stem}.bilingual.md"
        qa_path = self.output_dir / f"{stem}.qa.json"
        pdf_path = self.output_dir / f"{stem}.zh.pdf"

        zh_lines = ["# 中文论文草稿\n"]
        bi_lines = ["# 中英对照\n"]
        paragraphs: list[str] = []

        for seg in state.segments:
            zh = seg.text_zh_styled or seg.text_zh
            zh_lines.append(f"\n## {seg.source_span_id}\n{zh}\n")
            paragraphs.append(zh)

            bi_lines.append(f"\n## {seg.source_span_id}\n")
            bi_lines.append(f"**EN**\n\n{seg.text_en}\n")
            bi_lines.append(f"**ZH**\n\n{zh}\n")

        zh_path.write_text("\n".join(zh_lines), encoding="utf-8")
        bi_path.write_text("\n".join(bi_lines), encoding="utf-8")
        qa_path.write_text(json.dumps(state.qa_report, ensure_ascii=False, indent=2), encoding="utf-8")
        self.pdf_exporter.export(title=f"{stem} 中文论文", segments=paragraphs, output_path=str(pdf_path))

        return {
            "zh_markdown": str(zh_path),
            "bilingual_markdown": str(bi_path),
            "qa_json": str(qa_path),
            "zh_pdf": str(pdf_path),
        }
