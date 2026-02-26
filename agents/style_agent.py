from __future__ import annotations

import re

from .types import Segment


class StyleAgent:
    """Normalize translated text into concise academic Chinese style."""

    def run(self, segments: list[Segment]) -> list[Segment]:
        for seg in segments:
            text = seg.text_zh.strip()
            text = re.sub(r"\s+", " ", text)
            text = text.replace("我们发现", "研究结果表明")
            text = text.replace("我认为", "本文认为")
            seg.text_zh_styled = text
        return segments
