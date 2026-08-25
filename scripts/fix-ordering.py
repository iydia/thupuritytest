#!/usr/bin/env python3
"""Renumbers question IDs in questions.json sequentially (1, 2, 3, ...) based on array order."""

import json
import re
import sys
from pathlib import Path

QUESTIONS_FILE = Path(__file__).parent.parent / "data" / "questions.json"


def fix_json_escaping(content):
    """Restore escaped quotes inside HTML attribute values that may have been corrupted."""
    result = []
    i = 0
    in_text_value = False
    while i < len(content):
        c = content[i]
        if not in_text_value:
            result.append(c)
            if c == '"' and ('"text": "' in ''.join(result[-20:]) or '"text":"' in ''.join(result[-20:])):
                in_text_value = True
        else:
            if c == '\\' and i + 1 < len(content):
                result.append(c)
                result.append(content[i + 1])
                i += 2
                continue
            elif c == '"':
                rest = content[i + 1:i + 3].strip()
                if rest.startswith('}') or rest.startswith(','):
                    result.append(c)
                    in_text_value = False
                else:
                    result.append('\\"')
            else:
                result.append(c)
        i += 1
    return ''.join(result)


def main():
    raw = QUESTIONS_FILE.read_text(encoding="utf-8")

    try:
        questions = json.loads(raw)
    except json.JSONDecodeError:
        print("JSON broken — attempting to fix escaping...")
        raw = fix_json_escaping(raw)
        questions = json.loads(raw)

    for i, q in enumerate(questions, 1):
        q["id"] = i
        
        # Remove old question number, then add the new one
        text = re.sub(r"^\d+\.\s*", "", q["text"])
        q["text"] = f"{i}. {text}"

    lines = ["[\n"]
    for i, q in enumerate(questions):
        comma = "," if i < len(questions) - 1 else ""
        lines.append(f"  {json.dumps(q, ensure_ascii=False)}{comma}\n")
    lines.append("]\n")

    QUESTIONS_FILE.write_text("".join(lines), encoding="utf-8")
    print(f"Done — {len(questions)} questions renumbered 1–{len(questions)}.")


if __name__ == "__main__":
    main()
