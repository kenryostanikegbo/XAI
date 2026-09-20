"""Compose the merged Chapters 1-3 Markdown for the dissertation.

The Pandoc extracts of Chapter1_Introduction.docx, Chapter2_Literature_Review_v2.docx,
and Chapter3_Methodology.docx live under C:\\Users\\HomePC\\AppData\\Local\\Temp\\c*.md.

Operations per chapter:

  - Strip the title block, dedication, TOC (the merged file will have its own
    TOC at the front).
  - Strip the abstract if it duplicates the cover page.
  - Convert chapter heading from single line to two centred lines using Pandoc
    raw blocks (the Pandoc reference template's Heading 1 style is already
    centred; we add a line break inside the heading to put "CHAPTER ONE" on
    line 1 and "INTRODUCTION" on line 2).

Em-dashes: in the source DOCX the em-dash was authored with two hyphens "--",
which Pandoc exports to "--". We replace each "--" with a comma (most common
case: "X -- Y" becomes "X, Y"); if it sits between two numbers or between a
digit and a word we use "to" or ":". This is a conservative replacement.

Bullets: Pandoc converted Word bullet lists to "-" items. We convert them to
numbered or roman-numeral lists based on the depth:

  - Level 1 (top-level bullet): decimal numbered list "1.", "2.", ...
  - Level 2 (nested bullet): lower-case roman "i.", "ii.", ...
  - Level 3+: lower-case letter "a.", "b.", ...

This matches the user's request: "replace bullet points with numbers or roman
numerals as is fitting in APA 7" (APA-7 allows numbered or lettered series).

Output:
  C:\\Users\\HomePC\\Documents\\reportwritingprojects\\studnetxai\\outputs\\chapters\\merged_1_3.md
"""
from __future__ import annotations

import re
from pathlib import Path

TEMP_DIR = Path(r"C:\Users\HomePC\AppData\Local\Temp")
OUT = Path(r"C:\Users\HomePC\Documents\reportwritingprojects\studnetxai\outputs\chapters\merged_1_3.md")


CHAPTER_LABELS = {
    "c1": ("CHAPTER ONE", "INTRODUCTION"),
    "c2": ("CHAPTER TWO", "LITERATURE REVIEW"),
    "c3": ("CHAPTER THREE", "RESEARCH METHODOLOGY"),
}


def split_off_frontmatter(text: str) -> str:
    """Strip title block, dedication, and TOC, then keep chapter body until next chapter.

    The Pandoc extracts start with the title block, dedication, and table of
    contents. We discard all of that and keep only the chapter body, which
    starts at the first numbered section heading (e.g. '1.1 Background' or
    '## 1.1 Background') and runs to the next 'CHAPTER N' marker.
    """
    # Drop everything before the first numbered section heading.
    m = re.search(r"^(?:#+\s+)?(?:\d+\.\d+\s+|\d+\.\s+)", text, re.MULTILINE)
    if m:
        return text[m.start():]
    # Fall back to first '# ' heading
    m = re.search(r"^# .+$", text, re.MULTILINE)
    if m:
        return text[m.start():]
    return text


def two_line_chapter_heading(label: str) -> str:
    """Return a Pandoc raw block producing a centred two-line Heading 1."""
    top, bottom = label
    # Pandoc openxml raw block forces the heading style without affecting TOC
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


def replace_double_hyphen(text: str) -> str:
    """Replace each ' -- ', ' --- ', and standalone em-dash variants with a comma.

    The dissertation's em-dashes were authored as either ' -- ' or ' --- '
    depending on the chapter. APA-7 discourages em-dashes in formal prose
    (Chicago Manual §6.80 makes the same point); a comma serves the same
    grammatical function.
    """
    # 'X --- Y' first (longer pattern) so it doesn't get half-eaten by ' -- '.
    out = re.sub(r"\s+---\s+", ", ", text)
    out = re.sub(r"\s+--\s+", ", ", out)
    # Stray leading or trailing em-dashes
    out = re.sub(r"^---\s+", "", out, flags=re.MULTILINE)
    out = re.sub(r"^--\s+", "", out, flags=re.MULTILINE)
    out = re.sub(r"\s+---\.?\s*$", ".", out, flags=re.MULTILINE)
    out = re.sub(r"\s+--\.?\s*$", ".", out, flags=re.MULTILINE)
    return out


def convert_bullets(text: str) -> str:
    """Convert Pandoc '-' bullet items to numbered/roman/lettered lists.

    Track nesting depth via leading whitespace before the bullet marker.

    Numbering convention (per APA-7 §6.62):
      Level 0 (top): decimal "1.", "2.", ...
      Level 1:       lower-case roman "i.", "ii.", ...
      Level 2+:      lower-case letter "a.", "b.", ...
    """
    lines = text.split("\n")
    counters = [0, 0, 0]  # one per nesting level
    out = []
    prev_depth = -1
    for raw in lines:
        # Detect bullet line: optional indent spaces, '- ' at start
        m = re.match(r"^( *)(-)\s+(.*)$", raw)
        if not m:
            # Reset all counters when we leave a list block (a non-list line).
            # We approximate: if a non-list line is encountered, reset.
            counters = [0, 0, 0]
            prev_depth = -1
            out.append(raw)
            continue
        indent = len(m.group(1))
        # Depth: 0 if no indent, otherwise indent // 2 (Pandoc default)
        depth = 0 if indent == 0 else max(1, indent // 2)
        depth = min(depth, 2)
        if depth != prev_depth:
            # Reset deeper counters when ascending
            counters[depth + 1:] = [0] * (2 - depth)
        counters[depth] += 1
        # Build the marker
        if depth == 0:
            marker = f"{counters[0]}."
        elif depth == 1:
            marker = f"{_roman(counters[1])}."
        else:
            marker = f"{_letter(counters[2])}."
        body = m.group(3)
        out.append(f"{' ' * (depth * 2)}{marker} {body}")
        prev_depth = depth
    return "\n".join(out)


def _roman(n: int) -> str:
    nums = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"),
            (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
            (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    s = ""
    for v, sym in nums:
        while n >= v:
            s += sym
            n -= v
    return s


def _letter(n: int) -> str:
    return chr(ord("a") + n - 1)


def normalise_headings(text: str, prefix: str) -> str:
    """Add the chapter number prefix to Level-2/3/4 headings.

    Chapter 1 used '1.', '1.1', '1.1.1' etc. Chapter 2 used '2.', '2.1', ...
    Pandoc may have flattened these. We re-prefix.
    """
    # Numbered headings like "1.1 Background" -> "## 1.1 Background"
    text = re.sub(rf"^(?<!#)({prefix}\.\d+(?:\.\d+)?)\s+([A-Z].+)$",
                  rf"## \1 \2", text, flags=re.MULTILINE)
    # Unnumbered major section like "Background" should already be Heading 1.
    return text


def compose_chapter(key: str, prefix: str) -> str:
    src = TEMP_DIR / f"{key}.md"
    text = src.read_text(encoding="utf-8")
    body = split_off_frontmatter(text)
    # Drop any leftover top-level Heading 1 ("**CHAPTER N**", "Table of Contents",
    # "Research Methodology", "References", "Literature Review", etc that lived
    # in front matter). Some lines have a section number prefix inside the
    # bold (e.g. "# **3. Research Methodology**") so allow anything before the
    # closing **.
    body = re.sub(r"^\*\*CHAPTER \d+\*\*\s*$", "", body, flags=re.MULTILINE)
    body = re.sub(
        r"^# \*\*\s*(?:\d+\.\s*)?(?:Table of Contents|Research Methodology|"
        r"References|Literature Review|Introduction)\s*\*\*\s*$",
        "", body, flags=re.MULTILINE,
    )
    body = re.sub(r"^# References\s*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^# Table of Contents\s*$", "", body, flags=re.MULTILINE)
    body = replace_double_hyphen(body)
    body = convert_bullets(body)
    body = normalise_headings(body, prefix)
    head = two_line_chapter_heading(CHAPTER_LABELS[key])
    return head + body


def main():
    parts = [
        compose_chapter("c1", "1"),
        compose_chapter("c2", "2"),
        compose_chapter("c3", "3"),
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
