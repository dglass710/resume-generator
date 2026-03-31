#!/usr/bin/env python3
"""Generate a master resume containing all data from data.json."""

import json
import os
import copy
from generator import Generator

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def main():
    data_path = os.path.join(SCRIPT_DIR, "data.json")
    with open(data_path, "r") as f:
        data = json.load(f)

    sections = copy.deepcopy(data)
    for section in sections:
        if section["title"] == "Objective":
            # Rename so all objectives render as bullet points
            section["title"] = "Objectives"
            break

    output_path = os.path.join(SCRIPT_DIR, "Master_Resume.docx")
    Generator(sections).generate(output_path)
    print(f"Master resume generated: {output_path}")


if __name__ == "__main__":
    main()
