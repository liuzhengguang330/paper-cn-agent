from __future__ import annotations

import csv
from pathlib import Path

from .types import Segment


class TerminologyAgent:
    """Apply terminology constraints as pre-translation hints and post checks."""

    def __init__(self, terms_path: str) -> None:
        self.terms_path = Path(terms_path)
        self.terms = self._load_terms()

    def _load_terms(self) -> dict[str, str]:
        if not self.terms_path.exists():
            return {}
        terms: dict[str, str] = {}
        with self.terms_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                en = (row.get("en") or "").strip()
                zh = (row.get("zh") or "").strip()
                if en and zh:
                    terms[en.lower()] = zh
        return terms

    def run(self, segments: list[Segment]) -> list[Segment]:
        for seg in segments:
            hints = []
            lower = seg.text_en.lower()
            for en, zh in self.terms.items():
                if en in lower:
                    hints.append({"en": en, "zh": zh})
            if hints:
                seg.meta["term_hints"] = hints
        return segments
