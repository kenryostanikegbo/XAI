"""Restart page numbering at Chapter 1 in dissertation_full.docx.

Pandoc puts everything in one section by default. Word counts pages within a
section, so to restart the page counter at Chapter 1 we need to:

  1. Insert a w:sectPr (section break) at the start of Chapter 1's content.
     The break type is "next page" so Chapter 1 starts on a fresh page.
  2. Set the new section's page-number restart to start at 1.
  3. (Front-matter section keeps page numbers suppressed or uses roman
     numerals — in this dissertation there is no front matter, so the section
     is empty; we just keep page numbering continuous from there.)

Operation performed on the already-rendered docx:

  - Walk through paragraphs; find the first Heading-1 paragraph whose text
    is "CHAPTER ONE".
  - Insert a w:pPr/w:sectPr in the previous paragraph (or in the first
    paragraph) declaring a section break.
  - Set the section's <w:pgNumType w:start="1"/> so Chapter 1 is page 1.

This script is idempotent — running it twice does no harm.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


DOC = Path(r"C:\Users\HomePC\Documents\reportwritingprojects\studnetxai\outputs\chapters\dissertation_full.docx")


def make_sectPr(start_page: int = 1) -> OxmlElement:
    """Build a section-properties element that restarts page numbering at start_page."""
    sectPr = OxmlElement("w:sectPr")

    # Page size and margins — match reference.docx.
    pgSz = OxmlElement("w:pgSz")
    pgSz.set(qn("w:w"), "11906")  # A4 width in twips
    pgSz.set(qn("w:h"), "16838")  # A4 height in twips
    sectPr.append(pgSz)

    pgMar = OxmlElement("w:pgMar")
    for attr, val in [("w:top", "1440"), ("w:right", "1440"),
                      ("w:bottom", "1440"), ("w:left", "1440"),
                      ("w:header", "720"), ("w:footer", "720"),
                      ("w:gutter", "0")]:
        pgMar.set(qn(attr), val)
    sectPr.append(pgMar)

    # Section type: next page.
    typ = OxmlElement("w:type")
    typ.set(qn("w:val"), "nextPage")
    sectPr.append(typ)

    # Restart page numbering at 1.
    pgNumType = OxmlElement("w:pgNumType")
    pgNumType.set(qn("w:start"), str(start_page))
    sectPr.append(pgNumType)

    return sectPr


def first_heading1_paragraph(doc: Document, text: str):
    for p in doc.paragraphs:
        if p.style.name == "Heading 1" and p.text.strip() == text:
            return p
    return None


def insert_section_break_before(doc: Document, paragraph):
    """Insert a section break (next page) just before `paragraph`.

    In OOXML, a section break is declared by placing a <w:sectPr> inside a
    <w:pPr> at the END of the paragraph that should be the LAST paragraph of
    the preceding section. The next paragraph then becomes the first of the
    new section.

    So to start a new section at `paragraph`, we attach sectPr to the
    paragraph immediately before `paragraph`.
    """
    body = doc.element.body
    p_el = paragraph._element
    # Find the index of p_el in the body
    children = list(body)
    idx = children.index(p_el)
    if idx == 0:
        # paragraph is the very first paragraph — prepend a stub paragraph
        # carrying the section break.
        stub = OxmlElement("w:p")
        pPr = OxmlElement("w:pPr")
        pPr.append(make_sectPr(start_page=1))
        stub.append(pPr)
        body.insert(0, stub)
        return
    prev = children[idx - 1]
    # Attach sectPr inside prev's pPr.
    pPr = prev.find(qn("w:pPr"))
    if pPr is None:
        pPr = OxmlElement("w:pPr")
        prev.insert(0, pPr)
    # Replace any existing sectPr in pPr with our own.
    for old in pPr.findall(qn("w:sectPr")):
        pPr.remove(old)
    pPr.append(make_sectPr(start_page=1))


def main():
    doc = Document(DOC)
    ch1 = first_heading1_paragraph(doc, "CHAPTER ONE")
    if ch1 is None:
        raise SystemExit("No Heading 1 'CHAPTER ONE' found in document")
    insert_section_break_before(doc, ch1)
    doc.save(DOC)
    print(f"Inserted section break before CHAPTER ONE; restarted page count at 1")
    print(f"Saved {DOC}")


if __name__ == "__main__":
    main()
