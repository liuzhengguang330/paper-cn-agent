from __future__ import annotations

import argparse
from pathlib import Path

from pipeline import PaperTranslationPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="English paper -> Chinese paper agent network (MVP)")
    parser.add_argument("--input", required=True, help="Input file path (.txt/.md/.pdf)")
    parser.add_argument("--translator", choices=["mock", "openai"], default="mock")
    parser.add_argument("--model", default="gpt-4.1-mini", help="OpenAI model name")
    parser.add_argument("--terms", default="config/terms.csv", help="Terminology CSV")
    parser.add_argument("--output-dir", default="data/output", help="Output directory")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    pipeline = PaperTranslationPipeline(
        terms_path=args.terms,
        output_dir=args.output_dir,
        translator=args.translator,
        model=args.model,
    )
    try:
        state = pipeline.run(args.input)
    except Exception as exc:
        print(f"Pipeline failed: {exc}")
        raise SystemExit(1) from exc

    stem = Path(args.input).stem
    print("Pipeline done.")
    print(f"- Chinese draft: {args.output_dir}/{stem}.zh.md")
    print(f"- Bilingual:     {args.output_dir}/{stem}.bilingual.md")
    print(f"- QA report:     {args.output_dir}/{stem}.qa.json")
    print(f"- Chinese PDF:   {args.output_dir}/{stem}.zh.pdf")
    print(f"- QA summary:    {state.qa_report.get('summary')}")


if __name__ == "__main__":
    main()
