"""Re-extract Chapter 1 with all 1.1-1.9 sections preserved.

Root cause of the earlier loss: the previous extractor assumed sections were
stored as bold Markdown runs like `**1.1 Background**`. In fact
Chapter1_Introduction.docx uses real Word heading styles: "Heading 1" for
1.1-1.9 and "Heading 2" for 1.1.1-1.1.4. The earlier compose_chapters_1_3.py
frontmatter strip only kept paragraphs that started with a literal '#'
heading and chopped off the styled ones.

This script:
  - Walks paragraphs in source order
  - Skips everything before "1.1 Background" (cover, TOC, dedication, abstract)
  - Maps real Word styles to Markdown headings:
      Heading 1 -> ## 1.X Title
      Heading 2 -> ### 1.X.Y Title
  - Converts em-dashes to commas / colons / periods
  - Converts bullet lists to numbered / roman / lettered lists
  - Writes outputs/chapters/chapter1_fixed.md prepended with the two-line
    centred "CHAPTER ONE / INTRODUCTION" raw-OpenXML heading block
"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document

DOC = Path(
    r"C:\Users\HomePC\Documents\reportwritingprojects\studnetxai"
    r"\Chapter1_Introduction.docx"
)
FIXED = Path(
    r"C:\Users\HomePC\Documents\reportwritingprojects\studnetxai"
    r"\outputs\chapters\chapter1_fixed.md"
)


def safe_style_name(p) -> str:
    try:
        return p.style.name if p.style else "Normal"
    except AttributeError:
        return "Normal"


def extract(docx_path: Path) -> str:
    d = Document(docx_path)
    out: list[str] = []
    started_body = False

    for p in d.paragraphs:
        style = safe_style_name(p)
        txt = p.text.strip()

        # Skip until we hit the first numbered section. Anything before that
        # (cover, title, abstract, dedication, TOC) is front matter.
        if not started_body:
            if style == "Heading 1" and txt.startswith("1.1 ") and "Background" in txt:
                started_body = True
                out.append(f"## {txt}\n")
            continue

        # Body.
        if not txt:
            out.append("")
            continue

        if style == "Heading 1":
            out.append(f"## {txt}\n")
        elif style == "Heading 2":
            out.append(f"### {txt}\n")
        elif style == "Heading 3":
            out.append(f"#### {txt}\n")
        elif style == "List Paragraph":
            # Preserve list items verbatim; the normalise() bullet-to-number
            # pass won't see them because they're already non-bulleted.
            out.append(txt)
        else:
            out.append(txt)

    return "\n".join(out)


EM_DASH = "—"  # —
EN_DASH = "–"  # –


def replace_em_dashes(text: str) -> str:
    """Replace em-dashes with commas, colons, or periods.

    APA-7 disallows em-dashes as parenthetical punctuation in running prose.
    APA-7 §6.62 keeps the en-dash for numeric ranges (e.g. 2013–2014) —
    those are preserved untouched.

    Three dash forms are handled:
      U+2014 (em-dash)            e.g. "foo — bar"
      " -- " or " --- " (ASCII)   e.g. "foo -- bar"
      Leading "--- " / "-- " at line start
    """
    # Three ASCII dashes (long form) before two, so we don't double-replace.
    text = re.sub(r"\s+---\s+", ", ", text)
    text = re.sub(r"\s+--\s+", ", ", text)
    # Leading dashes after a newline.
    text = re.sub(r"(?m)^---\s+", "", text)
    text = re.sub(r"(?m)^--\s+", "", text)
    # Unicode em-dash (U+2014) — surrounded by spaces or not.
    text = re.sub(r"\s+" + EM_DASH + r"\s+", ", ", text)
    text = re.sub(r"(?m)^" + EM_DASH + r"\s+", "", text)
    # Em-dash with no spaces: most often a clause break — collapse to ", ".
    text = re.sub(r"(\S)" + EM_DASH + r"(\S)", r"\1, \2", text)
    # Em-dash with space on one side only.
    text = re.sub(r"\s+" + EM_DASH, ",", text)
    text = re.sub(EM_DASH + r"\s+", ", ", text)
    return text


def bullets_to_numbered(text: str) -> str:
    """Convert '-' bullets at varying indent to numbered / roman / lettered."""
    lines = text.split("\n")
    counters = [0, 0, 0]
    prev_depth = -1
    out: list[str] = []
    for raw in lines:
        m = re.match(r"^( *)(-)\s+(.*)$", raw)
        if not m:
            counters = [0, 0, 0]
            prev_depth = -1
            out.append(raw)
            continue
        indent = len(m.group(1))
        depth = 0 if indent == 0 else max(1, indent // 2)
        depth = min(depth, 2)
        if depth != prev_depth:
            counters[depth + 1:] = [0] * (2 - depth)
        counters[depth] += 1
        if depth == 0:
            marker = f"{counters[0]}."
        elif depth == 1:
            n = counters[1]
            roman_map = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"),
                         (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
                         (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
            sym = ""
            for v, s in roman_map:
                while n >= v:
                    sym += s
                    n -= v
            marker = f"{sym}."
        else:
            marker = f"{chr(ord('a') + counters[2] - 1)}."
        out.append(f"{' ' * (depth * 2)}{marker} {m.group(3)}")
        prev_depth = depth
    return "\n".join(out)


def two_line_heading(top: str, bottom: str) -> str:
    return (
        "```{=openxml}\n"
        f"<w:p><w:pPr><w:pStyle w:val=\"Heading1\"/>"
        f"<w:jc w:val=\"center\"/><w:spacing w:before=\"240\" w:after=\"120\"/></w:pPr>"
        f"<w:r><w:rPr><w:rFonts w:ascii=\"Times New Roman\" w:hAnsi=\"Times New Roman\"/>"
        f"<w:b/><w:sz w:val=\"28\"/></w:rPr><w:t>{top}</w:t></w:r></w:p>"
        f"<w:p><w:pPr><w:pStyle w:val=\"Heading1\"/>"
        f"<w:jc w:val=\"center\"/><w:spacing w:before=\"0\" w:after=\"240\"/></w:pPr>"
        f"<w:r><w:rPr><w:rFonts w:ascii=\"Times New Roman\" w:hAnsi=\"Times New Roman\"/>"
        f"<w:b/><w:sz w:val=\"28\"/></w:rPr><w:t>{bottom}</w:t></w:r></w:p>\n"
        "```\n\n"
    )


def main() -> None:
    text = extract(DOC)
    text = replace_em_dashes(text)
    text = bullets_to_numbered(text)
    head = two_line_heading("CHAPTER ONE", "INTRODUCTION")
    FIXED.parent.mkdir(parents=True, exist_ok=True)
    FIXED.write_text(head + text + "\n", encoding="utf-8")
    print(f"Wrote {FIXED} ({FIXED.stat().st_size} bytes)")
    print(f"words: {len(text.split())}")
    # Quick sanity: should have headings 1.1 .. 1.9 and 1.1.1 .. 1.1.4.
    for needle in ("## 1.1 Background", "## 1.2 Problem Statement",
                   "## 1.3 Research Aim", "## 1.4 Research Objectives",
                   "## 1.9 Organisation of the Report",
                   "### 1.1.1 Learning Analytics"):
        present = needle in text
        print(f"  {'OK ' if present else 'MISS'}  {needle}")


if __name__ == "__main__":
    main()
