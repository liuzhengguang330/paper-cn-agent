from __future__ import annotations

import re
from collections import Counter

from .types import Segment


class QAAgent:
    """Rule-based quality checks for high-risk translation regressions."""

    number_pattern = re.compile(r"\d+(?:\.\d+)?%?")

    def _extract_numbers(self, text: str) -> list[str]:
        return self.number_pattern.findall(text)

    def run(self, segments: list[Segment], terms: dict[str, str]) -> dict:
        issues: list[dict] = []

        for seg in segments:
            en_nums = Counter(self._extract_numbers(seg.text_en))
            zh_nums = Counter(self._extract_numbers(seg.text_zh_styled or seg.text_zh))
            if en_nums != zh_nums:
                issues.append(
                    {
                        "type": "number_mismatch",
                        "segment_id": seg.source_span_id,
                        "en_numbers": dict(en_nums),
                        "zh_numbers": dict(zh_nums),
                    }
                )

            for en, zh in terms.items():
                if en in seg.text_en.lower() and zh not in (seg.text_zh_styled or ""):
                    issues.append(
                        {
                            "type": "term_missing",
                            "segment_id": seg.source_span_id,
                            "term_en": en,
                            "expected_zh": zh,
                        }
                    )

            if len((seg.text_zh_styled or "").strip()) < 4:
                issues.append(
                    {
                        "type": "too_short",
                        "segment_id": seg.source_span_id,
                    }
                )

        return {
            "summary": {
                "segments": len(segments),
                "issues": len(issues),
                "pass": len(issues) == 0,
            },
            "issues": issues,
        }
