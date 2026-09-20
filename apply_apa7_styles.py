"""Apply APA-7 page-format compliance to reference.docx.

Operations:
  1. Set Times New Roman 12 as the default font for Normal and the standard
     heading styles (Heading 1 .. Heading 5).
  2. Set body alignment to JUSTIFIED, line spacing to 1.5.
  3. Set Heading 1 (chapter title) to centred, two-line by using a paragraph
     break in the source (we keep heading style consistent; layout is
     controlled by the source markdown).
  4. Add a footer with centered page numbers.
  5. Add a "Reference" paragraph style with hanging indent (left 1.27 cm,
     first-line -1.27 cm) for the reference list.

Re-run safely: this script is idempotent.
"""
from __future__ import annotations

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt

DOC = "reference.docx"
FONT_NAME = "Times New Roman"
FONT_SIZE = Pt(12)


def set_run_font(run, name=FONT_NAME, size=FONT_SIZE):
    run.font.name = name
    # East-Asian font hint (some renderers need it for non-ASCII fallback).
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), name)
    if size is not None:
        run.font.size = size


def set_paragraph_format(p, alignment=None, line_spacing=None, space_before=None, space_after=None):
    if alignment is not None:
        p.alignment = alignment
    if line_spacing is not None:
        p.paragraph_format.line_spacing_rule = line_spacing
    if space_before is not None:
        p.paragraph_format.space_before = space_before
    if space_after is not None:
        p.paragraph_format.space_after = space_after


def apply_normal_style(doc):
    style = doc.styles["Normal"]
    font = style.font
    font.name = FONT_NAME
    font.size = FONT_SIZE
    # Force East-Asian font name too.
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), FONT_NAME)
    pf = style.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    # Full double line spacing (2.0) per dissertation brief.
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)


def apply_heading_style(doc, level):
    """Heading 1..5 — APA-7 conventions.

    Level 1: chapter title — centred, bold, TNR 14 (one step above body).
    Level 2: centred, bold, TNR 13.
    Level 3: left, bold italic, TNR 12.
    Level 4: indented, bold italic + period, TNR 12.
    Level 5: indented, italic + period, TTR 12.
    """
    name = f"Heading {level}"
    if name not in [s.name for s in doc.styles]:
        return
    style = doc.styles[name]
    style.font.name = FONT_NAME
    style.font.size = {
        1: Pt(14),
        2: Pt(13),
        3: Pt(12),
        4: Pt(12),
        5: Pt(12),
    }[level]
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), FONT_NAME)

    pf = style.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)

    if level == 1:
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 2:
        pf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 3:
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif level == 4:
        pf.left_indent = Cm(1.27)
        pf.first_line_indent = Cm(-1.27)  # hanging indent for sub-subsection labels
    elif level == 5:
        pf.left_indent = Cm(2.54)

    font = style.font
    font.bold = level <= 2  # H1, H2 bold
    font.italic = level >= 3  # H3, H4, H5 italic


def ensure_reference_style(doc):
    """Add or update a paragraph style 'Reference' with hanging indent, TNR 12."""
    name = "Reference"
    styles = doc.styles
    if name in [s.name for s in styles]:
        style = styles[name]
    else:
        from docx.enum.style import WD_STYLE_TYPE
        style = styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    style.font.name = FONT_NAME
    style.font.size = FONT_SIZE
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.insert(0, rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rFonts.set(qn(attr), FONT_NAME)
    pf = style.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    pf.left_indent = Cm(1.27)
    pf.first_line_indent = Cm(-1.27)
    pf.space_after = Pt(6)


def add_centered_page_number_footer(doc):
    """Add a footer to every section with a centered page number field."""
    for section in doc.sections:
        footer = section.footer
        # Clear existing footer paragraphs except the first.
        for p in list(footer.paragraphs)[1:]:
            p._element.getparent().remove(p._element)
        p = footer.paragraphs[0]
        p.clear()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Insert PAGE field via raw XML.
        run = p.add_run()
        fldChar1 = OxmlElement("w:fldChar")
        fldChar1.set(qn("w:fldCharType"), "begin")
        instrText = OxmlElement("w:instrText")
        instrText.set(qn("xml:space"), "preserve")
        instrText.text = "PAGE   \\* MERGEFORMAT"
        fldChar2 = OxmlElement("w:fldChar")
        fldChar2.set(qn("w:fldCharType"), "end")
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
        set_run_font(run)
        # Remove any inherited header reference on first-page headers
        section.different_first_page_header_footer = False


def set_margins(doc):
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)


def main():
    doc = Document(DOC)
    apply_normal_style(doc)
    for level in range(1, 6):
        apply_heading_style(doc, level)
    ensure_reference_style(doc)
    add_centered_page_number_footer(doc)
    set_margins(doc)
    doc.save(DOC)
    print(f"Saved {DOC}")


if __name__ == "__main__":
    main()
