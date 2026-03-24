#!/usr/bin/env python3
"""Generate CV for Weronika Motkowska — Artsy Mystical (Mauve, Blue, Green) theme.

Watercolor-inspired background washes on warm cream, bold Lora display fonts,
same-company positions grouped to show career progression.
"""

import os
import random as _random
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
    Table,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── paths ──────────────────────────────────────────────────────────────────────
FONTS = os.path.expanduser("~/.cursor/skills/canvas-design/canvas-fonts")
OUT_DIR = "output/wmotkowska"
OUT_PDF = os.path.join(OUT_DIR, "cv_wmotkowska.pdf")
os.makedirs(OUT_DIR, exist_ok=True)

# ── fonts ──────────────────────────────────────────────────────────────────────
# Display: Lora Bold/BoldItalic — warm, artsy, expressive
# Body: InstrumentSans — clean modern readability
# Accent: Lora Italic — artistic flair for dates & metadata
pdfmetrics.registerFont(TTFont("Lora", os.path.join(FONTS, "Lora-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Lora-B", os.path.join(FONTS, "Lora-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Lora-BI", os.path.join(FONTS, "Lora-BoldItalic.ttf")))
pdfmetrics.registerFont(TTFont("Lora-I", os.path.join(FONTS, "Lora-Italic.ttf")))
pdfmetrics.registerFont(TTFont("ISans", os.path.join(FONTS, "InstrumentSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("ISans-B", os.path.join(FONTS, "InstrumentSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("ISans-I", os.path.join(FONTS, "InstrumentSans-Italic.ttf")))
pdfmetrics.registerFont(TTFont("ISans-BI", os.path.join(FONTS, "InstrumentSans-BoldItalic.ttf")))
pdfmetrics.registerFontFamily(
    "ISans", normal="ISans", bold="ISans-B", italic="ISans-I", boldItalic="ISans-BI"
)

# ── page geometry ──────────────────────────────────────────────────────────────
W, H = A4  # 595.27 × 841.89
M = 44
UW = W - 2 * M
L_COL = 262
G = 16
R_COL = UW - L_COL - G

# ── mystical palette ───────────────────────────────────────────────────────────
C_NAME = HexColor("#7B3F7B")
C_HEAD = HexColor("#1E6B5B")
C_TITLE = HexColor("#1E1E1E")
C_BODY = HexColor("#2A2A2A")
C_COMP = HexColor("#2A5A5A")
C_DATE = HexColor("#4A7A5A")
C_RULE = HexColor("#B888D0")
C_CONT = HexColor("#4A7A5A")
C_TEAL_HEX = "#1E6B5B"


# ── organic painterly background ───────────────────────────────────────────────

RNG = _random.Random(42)


def _soft_wash(canvas, cx, cy, rx, ry, color, alpha=0.025, layers=6):
    """Build an organic wash from overlapping, jittered ellipses (no single
    perfect shape). Each sub-ellipse is randomly offset/scaled so the result
    looks like a diffused watercolor cloud."""
    canvas.setFillColor(HexColor(color))
    for _ in range(layers):
        ox = RNG.gauss(0, rx * 0.18)
        oy = RNG.gauss(0, ry * 0.18)
        sx = rx * RNG.uniform(0.6, 1.4)
        sy = ry * RNG.uniform(0.6, 1.4)
        canvas.setFillAlpha(alpha * RNG.uniform(0.6, 1.0))
        canvas.ellipse(
            cx - sx + ox, cy - sy + oy, cx + sx + ox, cy + sy + oy,
            fill=1, stroke=0,
        )



def draw_background(canvas, doc):
    """Organic, barely-there watercolor layer inspired by floral mixed-media.

    Washes stay under 5% alpha; decorative marks (dots, flowers, stems) are
    scattered at 3-10% so the overall feel is hand-made, not computational.
    """
    canvas.saveState()

    # warm cream base
    canvas.setFillColor(HexColor("#FDF5F0"))
    canvas.rect(0, 0, W, H, fill=1, stroke=0)

    # ── diffuse washes (alpha 2-4%) ──
    _soft_wash(canvas, 160, H - 140, 190, 150, "#E8A8CC", 0.025, 7)
    _soft_wash(canvas, 300, H / 2 + 60, 230, 140, "#F0C0D0", 0.018, 5)
    _soft_wash(canvas, W - 90, 320, 170, 200, "#A0D098", 0.022, 6)
    _soft_wash(canvas, 150, 110, 180, 110, "#F0C8A0", 0.025, 5)
    _soft_wash(canvas, W - 100, H - 100, 120, 120, "#C8A8E8", 0.020, 5)
    _soft_wash(canvas, W - 70, 400, 80, 90, "#88C8D8", 0.018, 4)
    _soft_wash(canvas, 300, 140, 170, 120, "#F8D8B8", 0.015, 4)

    canvas.restoreState()


# ── paragraph styles ───────────────────────────────────────────────────────────

s_name = ParagraphStyle(
    "Name", fontName="Lora-BI", fontSize=28, leading=34,
    textColor=C_NAME, spaceAfter=3,
)
s_hl = ParagraphStyle(
    "HL", fontName="ISans", fontSize=9.5, leading=13,
    textColor=HexColor("#555555"), spaceAfter=4,
)
s_contact = ParagraphStyle(
    "Contact", fontName="Lora-I", fontSize=8, leading=11, textColor=C_CONT,
)
s_sec = ParagraphStyle(
    "Sec", fontName="Lora-B", fontSize=12, leading=15, textColor=C_HEAD,
)
s_co = ParagraphStyle(
    "Co", fontName="ISans-B", fontSize=9, leading=12,
    textColor=C_COMP, spaceAfter=1,
)
s_jt = ParagraphStyle(
    "JT", fontName="ISans-B", fontSize=8.5, leading=11.5,
    textColor=C_TITLE, spaceAfter=0,
)
s_dt = ParagraphStyle(
    "Dt", fontName="Lora-I", fontSize=7.5, leading=10,
    textColor=C_DATE, spaceAfter=3,
)
s_bul = ParagraphStyle(
    "Bul", fontName="ISans", fontSize=8, leading=11,
    textColor=C_BODY, leftIndent=8, spaceAfter=1,
)
s_et = ParagraphStyle(
    "ET", fontName="ISans-B", fontSize=9, leading=12,
    textColor=C_TITLE, spaceAfter=0,
)
s_esub = ParagraphStyle(
    "ESub", fontName="Lora-I", fontSize=7.5, leading=10,
    textColor=C_DATE, spaceAfter=1,
)
s_ed = ParagraphStyle(
    "ED", fontName="ISans", fontSize=7.5, leading=10.5,
    textColor=C_BODY, spaceAfter=0,
)
s_sk = ParagraphStyle(
    "SK", fontName="ISans", fontSize=8, leading=11.5,
    textColor=C_BODY, spaceAfter=3,
)
s_cert = ParagraphStyle(
    "Cert", fontName="ISans", fontSize=7.5, leading=10.5,
    textColor=C_BODY, spaceAfter=2,
)
s_lang = ParagraphStyle(
    "Lang", fontName="ISans", fontSize=8, leading=11,
    textColor=C_BODY, spaceAfter=1,
)
s_entb = ParagraphStyle(
    "EntB", fontName="ISans", fontSize=8, leading=11,
    textColor=C_BODY, leftIndent=8, spaceAfter=1,
)


# ── pre-written content (LLM-rewritten from CSV) ──────────────────────────────

EXP = {
    "inpost_ds": [
        "Designed end-to-end forecasting pipelines with time series cleaning, "
        "feature engineering, and exploration in Python",
        "Developed forecasts using ML frameworks (scikit-learn, Nixtla) and "
        "foundation models (TimesFM, Chronos)",
        "Built reproducible code repositories with Kedro on Azure Databricks "
        "and GitHub",
        "Maintained weekly forecasts, collaborating with operations and business "
        "teams on strategic planning",
        "Led sprint planning, task management, and onboarding of new team members",
    ],
    "uw_ra": [
        "Co-authored paper on cross-sector competition in film and gaming "
        "across 38 countries (2015\u20132023)",
        "Gathered historical data using web scraping in R and Python",
        "Conducted empirical research in cultural economics frameworks",
        "Presented findings at AIMAC 2024 International Conference, Lisbon",
    ],
    "emc_ds": [
        "Led end-to-end sales data exploration and analysis for agency clients",
        "Built econometric and Bayesian business models in R and Python",
        "Collected data via BigQuery, APIs, Google Trends, and web scraping",
        "Developed RShiny dashboards and automated HTML/PowerPoint reports",
        "Deployed production solutions on Google Cloud Platform",
    ],
}

EDU = [
    {
        "deg": "M.Sc. in Data Science",
        "school": "University of Warsaw",
        "dates": "Oct 2021 \u2013 Dec 2023",
        "focus": "ML, Big Data Analytics, Econometrics, Text Mining, Web Scraping",
        "thesis": "Music marketing on TikTok \u2014 audio and lyrics analysis "
                  "using PCA and Random Forest",
    },
    {
        "deg": "B.Sc. in Mathematics",
        "school": "University of Warsaw",
        "dates": "Oct 2018 \u2013 Jul 2021",
        "focus": "Analysis, Algebra, Probability Theory, Topology, Differential Equations",
        "thesis": "Solutions to the wave equation in the vibrating string problem",
    },
    {
        "deg": "B.Sc. in Economics",
        "school": "University of Warsaw",
        "dates": "Oct 2018 \u2013 Jul 2021",
        "focus": "Micro/Macroeconomics, Econometrics, Finance, Time Series, SQL",
        "thesis": "TikTok and music popularity \u2014 Spotify chart duration "
                  "vs TikTok trend persistence",
    },
]

SKILLS = {
    "Programming": "Python \u00b7 R \u00b7 SQL \u00b7 Git \u00b7 HTML \u00b7 LaTeX",
    "Data Science & ML": (
        "Machine Learning \u00b7 Supervised Learning \u00b7 Scikit-learn \u00b7 "
        "Nixtla \u00b7 Time Series Analysis \u00b7 Statistical Modeling \u00b7 "
        "Data Analysis \u00b7 Data Science \u00b7 Econometrics \u00b7 Statistics \u00b7 "
        "Applied Mathematics \u00b7 Mathematical Modeling"
    ),
    "AI & Automation": (
        "AI Agents \u00b7 Claude \u00b7 Cursor AI \u00b7 GitHub Copilot \u00b7 VS Code"
    ),
    "Analytics & Tools": (
        "Power BI \u00b7 Databricks \u00b7 Excel \u00b7 PowerPoint \u00b7 "
        "Cloud Computing \u00b7 Canva \u00b7 Pivot Tables"
    ),
    "Business": (
        "Project Management \u00b7 Project Planning \u00b7 Business Modeling \u00b7 "
        "Sales Analysis \u00b7 Business Data Analysis \u00b7 Budget Forecasting \u00b7 "
        "Research Design \u00b7 Presentations \u00b7 Production Management \u00b7 "
        "Digital Media \u00b7 Social Media \u00b7 Problem Solving \u00b7 "
        "Analytical Skills \u00b7 Teamwork"
    ),
}

CERTS = [
    (
        "Language Proficiency Certificate (ESOKJ), English C1",
        "University of Warsaw",
        "Feb 2021",
        "#113/21",
    ),
    ("Certificate of Presentation", "AIMAC Lisbon 2024", "Jul 2024", None),
]

LANGS = [("English", "Full professional proficiency"), ("Polish", "Native")]

CERAMIC = {
    "name": "Motka Rzeczy",
    "role": "Founder & Creator",
    "link": "tiktok.com/@motka.rzeczy",
    "bullets": [
        "Run a small ceramic business with end-to-end production \u2014 "
        "design, clay work, glazing, and fulfillment",
        "Build brand awareness through organic TikTok marketing, growing "
        "an engaged community with authentic content",
        "Apply production management and creative strategy to drive sales "
        "without paid advertising",
    ],
}


# ── helpers ────────────────────────────────────────────────────────────────────

def section_heading(text, width):
    return [
        HRFlowable(
            width=width, thickness=0.3, color=C_RULE, spaceAfter=6, spaceBefore=0
        ),
        Paragraph(escape(text.upper()), s_sec),
        Spacer(1, 5),
    ]


def company_group(company, positions, gap_after=10):
    """Render grouped positions under one company name.

    Shows company once; positions listed underneath with tight internal spacing
    so recruiters see career progression at a glance.

    positions: list of (title, dates, bullets_or_None)
    """
    els = [Paragraph(escape(company), s_co)]
    for i, (title, dates, bullets) in enumerate(positions):
        els.append(Paragraph(escape(title), s_jt))
        els.append(Paragraph(escape(dates), s_dt))
        if bullets:
            for b in bullets:
                els.append(Paragraph(f"\u2013  {escape(b)}", s_bul))
        if i < len(positions) - 1:
            els.append(Spacer(1, 3))
    els.append(Spacer(1, gap_after))
    return els


def col_table(flowables, w):
    t = Table([[f] for f in flowables], colWidths=[w])
    t.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ])
    )
    return t


# ── build story ────────────────────────────────────────────────────────────────

story = []

# HEADER — full width
story.append(Paragraph(escape("Weronika Motkowska"), s_name))
story.append(Paragraph(escape("Data Scientist  |  Forecasting & Marketing"), s_hl))
story.append(
    Paragraph(
        escape(
            "weronikamotkowska@gmail.com  \u00b7  +48 512 012 989  \u00b7  "
            "github.com/wmotkowska"
        ),
        s_contact,
    )
)
story.append(Spacer(1, 12))

# ── LEFT COLUMN: Experience ────────────────────────────────────────────────────

left = []
left.extend(section_heading("Experience", L_COL))

left.extend(
    company_group("InPost", [
        (
            "Data Scientist",
            "Sep 2024 \u2013 Present  \u00b7  Warsaw",
            EXP["inpost_ds"],
        ),
        (
            "Junior Data Scientist",
            "Jan \u2013 Sep 2024  \u00b7  Warsaw",
            None,
        ),
    ])
)

left.extend(
    company_group("University of Warsaw", [
        (
            "Research Assistant",
            "Oct 2023 \u2013 Sep 2024  \u00b7  Warsaw",
            EXP["uw_ra"],
        ),
    ])
)

left.extend(
    company_group("EssenceMediacom Poland", [
        (
            "Junior Data Scientist",
            "May \u2013 Dec 2023  \u00b7  Warsaw",
            EXP["emc_ds"],
        ),
        (
            "Graduate Econometrician",
            "May 2022 \u2013 Apr 2023",
            None,
        ),
    ])
)

left.extend(
    company_group("Local Heroes", [
        (
            "Intern \u2192 Production Assistant",
            "Mar \u2013 Jul 2020  \u00b7  Warsaw",
            None,
        ),
    ])
)

# ── RIGHT COLUMN: Education, Entrepreneurship, Certs, Languages ────────────────

right = []

# Education
right.extend(section_heading("Education", R_COL))
for e in EDU:
    right.append(Paragraph(escape(e["deg"]), s_et))
    right.append(
        Paragraph(escape(f'{e["school"]}  \u00b7  {e["dates"]}'), s_esub)
    )
    right.append(Paragraph(escape(f'Focus: {e["focus"]}'), s_ed))
    right.append(
        Paragraph(
            f'<font name="Lora-I">Thesis:</font> {escape(e["thesis"])}', s_ed
        )
    )
    right.append(Spacer(1, 6))

# Entrepreneurship — ceramic business
right.extend(section_heading("Entrepreneurship", R_COL))
right.append(Paragraph(escape(CERAMIC["name"]), s_co))
right.append(
    Paragraph(
        escape(f'{CERAMIC["role"]}  \u00b7  {CERAMIC["link"]}'), s_esub
    )
)
for b in CERAMIC["bullets"]:
    right.append(Paragraph(f"\u2013  {escape(b)}", s_entb))
right.append(Spacer(1, 4))

# Certifications
right.extend(section_heading("Certifications", R_COL))
for name, auth, date, lic in CERTS:
    line = f"{name}  \u2014  {auth}  \u00b7  {date}"
    if lic:
        line += f"  ({lic})"
    right.append(Paragraph(escape(line), s_cert))

# Languages
right.extend(section_heading("Languages", R_COL))
for lang, prof in LANGS:
    right.append(Paragraph(escape(f"{lang}  \u2014  {prof}"), s_lang))

# ── TWO-COLUMN TABLE ──────────────────────────────────────────────────────────

main = Table(
    [[col_table(left, L_COL), col_table(right, R_COL)]],
    colWidths=[L_COL, R_COL + G],
)
main.setStyle(
    TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), G),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ])
)
story.append(main)

# ── FULL-WIDTH SKILLS (below columns — fills remaining page space) ─────────────

story.append(Spacer(1, 6))
story.extend(section_heading("Skills", UW))
for cat, items in SKILLS.items():
    story.append(
        Paragraph(
            f'<font name="ISans-B" color="{C_TEAL_HEX}">{escape(cat)}:</font>  '
            f"{escape(items)}",
            s_sk,
        )
    )

# ── GENERATE PDF ───────────────────────────────────────────────────────────────

doc = SimpleDocTemplate(
    OUT_PDF,
    pagesize=A4,
    leftMargin=M,
    rightMargin=M,
    topMargin=38,
    bottomMargin=38,
)
doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background)
print(f"CV generated: {OUT_PDF}")
