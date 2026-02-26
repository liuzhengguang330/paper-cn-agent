from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Segment:
    source_span_id: str
    text_en: str
    text_zh: str = ""
    text_zh_styled: str = ""
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class PipelineState:
    input_path: str
    raw_text: str = ""
    segments: list[Segment] = field(default_factory=list)
    qa_report: dict[str, Any] = field(default_factory=dict)
    output_paths: dict[str, str] = field(default_factory=dict)
