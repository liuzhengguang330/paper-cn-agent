from __future__ import annotations

from pathlib import Path


class ChinesePdfExporter:
    """Export translated Chinese content to a readable PDF."""

    def __init__(self) -> None:
        self._font_registered = False

    def _ensure_reportlab(self) -> None:
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Missing dependency: reportlab. Please run `pip install -r requirements.txt` first."
            ) from exc
        if not self._font_registered:
            # Built-in CJK CID font on reportlab, avoids local font dependency.
            pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
            self._font_registered = True

    def export(self, title: str, segments: list[str], output_path: str) -> str:
        self._ensure_reportlab()
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(output),
            pagesize=A4,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
            title=title,
        )

        title_style = ParagraphStyle(
            name="TitleCN",
            fontName="STSong-Light",
            fontSize=17,
            leading=22,
            spaceAfter=10,
        )
        body_style = ParagraphStyle(
            name="BodyCN",
            fontName="STSong-Light",
            fontSize=11,
            leading=18,
            spaceAfter=8,
        )

        story = [Paragraph(title, title_style), Spacer(1, 8)]
        for paragraph in segments:
            text = (paragraph or "").strip()
            if not text:
                continue
            # Preserve line breaks from markdown-like content.
            text = text.replace("\n", "<br/>")
            story.append(Paragraph(text, body_style))

        doc.build(story)
        return str(output)
