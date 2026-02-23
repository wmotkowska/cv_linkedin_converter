# Layout Guide

Detailed typographic specifications for constructing a CV with `reportlab`. Every measurement is intentional — treat these as a senior typographer's working notes.

## Page Setup

**CRITICAL: Single-page constraint.** All CVs must fit on exactly one A4 page.

### Single-Column Layout (lighter profiles)

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate

PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.27 × 841.89 pt

doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    leftMargin=50,
    rightMargin=50,
    topMargin=40,
    bottomMargin=40,
)
```

Usable text width: ~495pt. Tighter margins to maximize single-page space.

### Two-Column Layout (content-heavy profiles)

When content won't fit in single-column, use a two-column table layout:

```python
from reportlab.platypus import Table, TableStyle, Spacer
from reportlab.lib.colors import HexColor

# Calculate column widths
USABLE_WIDTH = PAGE_WIDTH - 100  # ~495pt with 50pt margins
LEFT_COL = 240  # Primary content (experience)
GUTTER = 15     # Space between columns
RIGHT_COL = USABLE_WIDTH - LEFT_COL - GUTTER  # ~240pt

def build_two_column_cv(left_flowables, right_flowables):
    """
    Create a two-column layout using a Table.
    
    Left column: Header, Contact, Experience (the "story")
    Right column: Education, Skills, Certifications, Languages (supporting details)
    """
    # Wrap flowables in nested tables for proper flow
    left_cell = Table([[f] for f in left_flowables], colWidths=[LEFT_COL])
    left_cell.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    right_cell = Table([[f] for f in right_flowables], colWidths=[RIGHT_COL])
    right_cell.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    # Main two-column table
    main_table = Table(
        [[left_cell, right_cell]],
        colWidths=[LEFT_COL, RIGHT_COL + GUTTER],
    )
    main_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('LEFTPADDING', (1, 0), (1, 0), GUTTER),  # Gutter on right column
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    return main_table
```

**Content distribution for two-column:**

| Left Column (240pt) | Right Column (240pt) |
|---|---|
| Name (hero, can span full width above table) | Education |
| Headline & Contact | Skills |
| Experience section | Certifications |
| | Languages |

**Visual balance tip**: The left column should have roughly equal visual weight to the right. If experience is very detailed, move education to left column and use right for skills/certs/languages only.

## Type Scale

Use a modular scale. Base size 10pt, ratio ~1.25 (Major Third).

### Standard Scale (single-column)

| Element | Size | Leading | Font Role |
|---|---|---|---|
| Name | 26-32pt | 34-40pt | Display |
| Headline / Subtitle | 11-13pt | 16-18pt | Body Italic or Display Light |
| Section Heading | 13-15pt | 18-20pt | Display or Body Bold |
| Job Title / Degree | 10.5-11pt | 14-15pt | Body Bold |
| Company / School | 10-10.5pt | 14pt | Body Regular |
| Body text | 9.5-10pt | 13.5-14pt | Body Regular |
| Dates / Metadata | 8.5-9pt | 12-13pt | Accent (monospace or light) |
| Skills / Tags | 9-9.5pt | 12pt | Body Regular or Accent |

### Compact Scale (two-column / dense content)

When fitting everything on one page requires compaction:

| Element | Size | Leading | Font Role |
|---|---|---|---|
| Name | 22-26pt | 28-32pt | Display |
| Headline / Subtitle | 9-10pt | 13-14pt | Body Italic or Display Light |
| Section Heading | 10-11pt | 14-15pt | Display or Body Bold |
| Job Title / Degree | 9-9.5pt | 12-13pt | Body Bold |
| Company / School | 8.5-9pt | 12pt | Body Regular |
| Body text | 8-8.5pt | 11-12pt | Body Regular |
| Dates / Metadata | 7.5-8pt | 10-11pt | Accent (monospace or light) |
| Skills / Tags | 8-8.5pt | 11pt | Body Regular or Accent |
| Bullet points | 8-8.5pt | 11-12pt | Body Regular |

**Minimum readable sizes**: Never go below 7.5pt for any text. Below this, readability suffers significantly.

**CRITICAL**: Leading (line spacing) is where amateur and expert diverge. Set leading explicitly via `ParagraphStyle(leading=N)` — never rely on defaults.

## Vertical Spacing

Spacing between elements creates rhythm. Use `Spacer(1, N)` between elements:

### Standard Spacing (single-column)

| Between | Space |
|---|---|
| Name and headline | 4-6pt |
| Headline and location | 2-3pt |
| Header block and first section | 20-28pt |
| Section heading and first item | 8-12pt |
| Items within a section | 10-14pt |
| Sub-elements within an item (title → company → date) | 1-3pt |
| Between sections | 18-24pt |
| Section rule and section heading | 10-14pt |

### Compact Spacing (two-column / dense content)

| Between | Space |
|---|---|
| Name and headline | 2-3pt |
| Headline and location | 1-2pt |
| Header block and first section | 10-14pt |
| Section heading and first item | 4-6pt |
| Items within a section | 6-8pt |
| Sub-elements within an item (title → company → date) | 0-1pt |
| Between sections | 10-14pt |
| Section rule and section heading | 6-8pt |
| Between bullet points | 1-2pt |

**Principle**: More space between unrelated things, less between related things. This is Gestalt proximity — the most powerful layout tool.

**Compact layout tip**: In two-column layouts, reduce horizontal rules to 0.3pt thickness and minimize spaceAfter/spaceBefore on rules.

## Section Headings

Section headings should be unmistakable but not loud:

```python
from reportlab.platypus import Paragraph, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor

section_heading_style = ParagraphStyle(
    "SectionHeading",
    fontName="YourDisplayFont",
    fontSize=13,
    leading=18,
    textColor=HexColor("#2A2A2A"),
    spaceAfter=0,
    spaceBefore=0,
    textTransform="uppercase",  # Optional: uppercase headings
    letterSpacing=1.5,  # Only if using uppercase
)
```

Pair with a thin rule above or below:

```python
HRFlowable(
    width="100%",
    thickness=0.4,
    color=HexColor("#CCCCCC"),
    spaceAfter=10,
    spaceBefore=2,
)
```

Rules are the ONLY non-text element. Keep them thin (0.3-0.5pt) and muted.

## Header Construction

The name is the hero element. Build it with presence:

```python
name_style = ParagraphStyle(
    "Name",
    fontName="YourDisplayFont",
    fontSize=28,
    leading=34,
    textColor=HexColor("#1A1A1A"),
    spaceAfter=4,
)

headline_style = ParagraphStyle(
    "Headline",
    fontName="YourBodyFont",
    fontSize=11,
    leading=16,
    textColor=HexColor("#555555"),
    spaceAfter=2,
)

location_style = ParagraphStyle(
    "Location",
    fontName="YourAccentFont",
    fontSize=9,
    leading=13,
    textColor=HexColor("#888888"),
)
```

## Experience Entry Pattern

Each experience entry has a strict internal hierarchy:

```python
job_title_style = ParagraphStyle(
    "JobTitle",
    fontName="YourBodyFont-Bold",
    fontSize=10.5,
    leading=14,
    textColor=HexColor("#1A1A1A"),
    spaceAfter=1,
)

company_style = ParagraphStyle(
    "Company",
    fontName="YourBodyFont",
    fontSize=10,
    leading=14,
    textColor=HexColor("#333333"),
    spaceAfter=1,
)

date_style = ParagraphStyle(
    "DateRange",
    fontName="YourAccentFont",
    fontSize=8.5,
    leading=12,
    textColor=HexColor("#777777"),
    spaceAfter=4,
)

description_style = ParagraphStyle(
    "Description",
    fontName="YourBodyFont",
    fontSize=9.5,
    leading=13.5,
    textColor=HexColor("#2A2A2A"),
    spaceAfter=0,
)
```

Combine date and location on the same line when possible: `"Jan 2020 – Present  ·  London, UK"`

## Education Entry Pattern

Mirrors experience but typically shorter:

- **School name** — Bold, same as job title style
- **Degree, Field of Study** — Regular body, on same line or next line
- **Date range** — Accent/muted
- **Description** — Only if substantive

## Skills Layout

Skills work best as a flowing comma-separated list or a compact table:

**Option A — Inline flow** (preferred for fewer than 15 skills):
```python
skills_text = "  ·  ".join([s["name"] for s in profile["skills"]])
```

**Option B — Multi-column table** (for many skills):
```python
from reportlab.platypus import Table, TableStyle

cols = 3
rows = [skills[i:i+cols] for i in range(0, len(skills), cols)]
table = Table(rows, colWidths=[usable_width / cols] * cols)
table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (-1, -1), "YourBodyFont"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("TEXTCOLOR", (0, 0), (-1, -1), HexColor("#333333")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
]))
```

## Color Application

Colors are applied ONLY to text. Never to backgrounds, boxes, or borders (except thin rules).

| Element | Typical Color Range |
|---|---|
| Name | Near-black: `#1A1A1A` to `#0D0D0D` |
| Section headings | Dark or accent: depends on theme |
| Job titles | Near-black: `#1A1A1A` to `#222222` |
| Body text | Dark gray: `#2A2A2A` to `#333333` |
| Companies / Schools | Medium: `#333333` to `#444444` |
| Dates / Metadata | Muted: `#666666` to `#888888` |
| Rules | Light: `#BBBBBB` to `#DDDDDD` |

The accent color (from the user's theme) should be used sparingly — only on the name or section headings, never both. Restraint is sophistication.

## Reportlab Implementation Notes

### Font Registration

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS_DIR = os.path.expanduser("~/.cursor/skills/canvas-design/canvas-fonts")

pdfmetrics.registerFont(TTFont("DisplayFont", os.path.join(FONTS_DIR, "YourDisplay.ttf")))
pdfmetrics.registerFont(TTFont("BodyFont", os.path.join(FONTS_DIR, "YourBody-Regular.ttf")))
pdfmetrics.registerFont(TTFont("BodyFont-Bold", os.path.join(FONTS_DIR, "YourBody-Bold.ttf")))
pdfmetrics.registerFont(TTFont("AccentFont", os.path.join(FONTS_DIR, "YourAccent.ttf")))
```

### Building the Story

```python
story = []

story.append(Paragraph(profile["name"], name_style))
story.append(Paragraph(profile["headline"], headline_style))
story.append(Paragraph(profile["location"], location_style))
story.append(Spacer(1, 24))

# For each section, follow the pattern:
# 1. HRFlowable (thin rule)
# 2. Spacer
# 3. Section heading Paragraph
# 4. Spacer
# 5. Section content (entries or inline text)
# 6. Spacer before next section

doc.build(story)
```

### Handling Long Text

For description fields that may contain long paragraphs, ensure the `ParagraphStyle` has appropriate `leading` and wrap naturally. Reportlab Paragraphs handle line wrapping automatically within the frame.

If a description contains multiple paragraphs (separated by `\n`), split and add each as a separate `Paragraph` with a small `Spacer(1, 3)` between them.

### Special Characters

Escape XML entities in text before passing to `Paragraph`:
```python
from xml.sax.saxutils import escape
text = escape(raw_text)
```

## The Refinement Pass

After the initial build, review the output PDF and adjust:

1. **Is the name the first thing your eye hits?** If not, increase its size or darken its color.
2. **Can you distinguish sections at a glance?** Section headings need more contrast or spacing if they blend in.
3. **Are dates visually subordinate?** They should be the quietest element on the page.
4. **Is there enough space between sections?** When in doubt, add more.
5. **Does it feel like one cohesive document?** The same font, color, and spacing logic should repeat predictably.

This is the difference between competent and exceptional. Take the second pass.
