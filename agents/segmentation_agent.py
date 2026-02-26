from __future__ import annotations

import re

from .types import Segment


class SegmentationAgent:
    """Split text into paragraph-level segments with stable ids."""

    def run(self, text: str) -> list[Segment]:
        raw_parts = re.split(r"\n\s*\n", text.strip())
        parts = [p.strip() for p in raw_parts if p.strip()]
        return [Segment(source_span_id=f"seg_{i+1:04d}", text_en=part) for i, part in enumerate(parts)]
