#!/usr/bin/env python3
"""
resume_cli.py

Command-line tool to generate a tailored resume using AI auto-selection.
Uses the Claude Agent SDK with your Claude subscription for AI calls.

Usage:
    python resume_cli.py <output_path> <job_posting>

Arguments:
    output_path     Path for the generated .docx file
    job_posting     Job posting text (as a string)
"""

import argparse
import json
import os
import sys

from ai_selector import AISelector
from generator import Generator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_data():
    data_path = os.path.join(SCRIPT_DIR, "data.json")
    fallback_path = os.path.join(SCRIPT_DIR, "default_data.json")
    for path in (data_path, fallback_path):
        if os.path.isfile(path):
            with open(path, "r") as f:
                return json.load(f)
    print("Error: could not find data.json or default_data.json.", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a tailored resume using AI to select the best options."
    )
    parser.add_argument("output_path", help="Path for the output .docx file")
    parser.add_argument("job_posting", help="Job posting text")
    parser.add_argument(
        "--model",
        default=None,
        help="Claude model to use (e.g., sonnet, opus, haiku)",
    )
    args = parser.parse_args()

    master_resume = load_data()
    print(f"Output: {args.output_path}")

    selector = AISelector(master_resume)
    result, error = selector.call_with_retry(
        args.job_posting, model=args.model, on_progress=print
    )

    if error:
        print(f"\nError: {error}", file=sys.stderr)
        sys.exit(1)

    # Build the selected items for the reorder prompt
    projects = selector._get_section_content("Technical Projects")
    competencies = selector._get_section_content("Core Competencies")
    selected_projects = [projects[i] for i in result["technical_project_indices"]]
    selected_comps = [competencies[i] for i in result["core_competency_indices"]]

    reorder, reorder_error = selector.call_reorder(
        args.job_posting, selected_projects, selected_comps,
        model=args.model, on_progress=print
    )
    if reorder_error:
        print(f"\nReorder warning: {reorder_error}", file=sys.stderr)
        print("Proceeding with default order.", file=sys.stderr)

    selected_sections = selector.build_selected_sections(result, reorder=reorder)

    try:
        Generator(selected_sections).generate(args.output_path)
    except Exception as e:
        print(f"Error generating document: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\nResume generated: {os.path.abspath(args.output_path)}")


if __name__ == "__main__":
    main()
