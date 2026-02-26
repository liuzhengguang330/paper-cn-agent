from __future__ import annotations

from pathlib import Path


class IngestAgent:
    """Load input content while preserving basic structure."""

    def _read_pdf_text(self, path: Path) -> str:
        try:
            from pypdf import PdfReader
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Missing dependency: pypdf. Please run `pip install -r requirements.txt` first."
            ) from exc

        reader = PdfReader(str(path))
        pages: list[str] = []
        for idx, page in enumerate(reader.pages, start=1):
            page_text = (page.extract_text() or "").strip()
            if page_text:
                pages.append(f"[Page {idx}]\n{page_text}")
        return "\n\n".join(pages).strip()

    def run(self, input_path: str) -> str:
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        suffix = path.suffix.lower()
        if suffix in {".txt", ".md"}:
            return path.read_text(encoding="utf-8")
        if suffix == ".pdf":
            text = self._read_pdf_text(path)
            if not text:
                raise ValueError("PDF extracted no readable text (may be scanned image PDF).")
            return text
        raise ValueError("Only .txt/.md/.pdf are supported.")
