#!/usr/bin/env python3
"""
CV Generator from LinkedIn Data Export
Theme: Minimal White Blue Modern
Layout: Single-page, two-column
"""

import csv
import os
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
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

# Configuration
INPUT_NAME = "wmotkowska"
INPUT_DIR = Path(f"input/{INPUT_NAME}")
OUTPUT_DIR = Path(f"output/{INPUT_NAME}")
OUTPUT_FILE = OUTPUT_DIR / f"cv_{INPUT_NAME}.pdf"

FONTS_DIR = Path(os.path.expanduser("~/.cursor/skills/canvas-design/canvas-fonts"))

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 45
USABLE_WIDTH = PAGE_WIDTH - 2 * MARGIN

# Two-column layout
LEFT_COL_WIDTH = 260
GUTTER = 18
RIGHT_COL_WIDTH = USABLE_WIDTH - LEFT_COL_WIDTH - GUTTER


# =============================================================================
# PRE-WRITTEN DESCRIPTIONS (LLM-analyzed and structured)
# =============================================================================

# Experience descriptions - rewritten by language model for proper structure
EXPERIENCE_DESCRIPTIONS = {
    ("Data Scientist", "InPost"): [
        "Led end-to-end forecasting process including time series data cleaning and custom feature engineering",
        "Built forecasting models using Python frameworks (sklearn, Nixtla) and foundation models (TimesFM, Chronos)",
        "Developed reproducible code repository using Kedro framework with Azure Databricks",
        "Delivered weekly forecast maintenance and collaborated with operations and business teams",
    ],
    ("Junior Data Scientist", "InPost"): [],
    ("Research Assistant", "Uniwersytet Warszawski"): [
        "Co-authored working paper on cross-sector competition in film and gaming across 38 countries (2015-2023)",
        "Gathered historical data using web scraping techniques in R and Python",
        "Presented preliminary results at AIMAC 2024 international conference in Lisbon",
    ],
    ("Junior Data Scientist", "EssenceMediacom Poland"): [
        "Performed end-to-end sales data exploration and analysis for clients",
        "Built business models using econometric and Bayesian approaches in R and Python",
        "Gathered data from BigQuery, APIs, Google Trends, and web scraping",
        "Developed RShiny dashboards and deployed production solutions on GCP",
    ],
    ("Graduate Econometrician", "EssenceMediacom Poland"): [],
    ("Production Assistant", "Local Heroes"): [],
    ("Intern", "Local Heroes"): [],
}

# Education summaries - rewritten by language model (with field of study)
EDUCATION_DESCRIPTIONS = {
    ("Magister (Mgr)", "Uniwersytet Warszawski"): {
        "field_of_study": "Mathematics",
        "summary": "Risk Measures, Topological Data Analysis, Stochastic Simulations",
        "thesis": "",
    },
    ("Master's degree", "Uniwersytet Warszawski"): {
        "field_of_study": "Data Science",
        "summary": "Machine Learning, Econometrics, Big Data Analytics",
        "thesis": "Music marketing strategies on TikTok using PCA and Random Forest analysis",
    },
    ("Licencjat (Lic.)", "Uniwersytet Warszawski", "math"): {
        "field_of_study": "Mathematics",
        "summary": "Mathematical Analysis, Probability Theory, Topology, Statistics",
        "thesis": "Solutions to the wave equation in the vibrating string problem",
    },
    ("Licencjat (Lic.)", "Uniwersytet Warszawski", "econ"): {
        "field_of_study": "Economics",
        "summary": "Economics, Econometrics, Finance, Time Series Analysis",
        "thesis": "TikTok and online popularity of music - Spotify charts and TikTok trends",
    },
}

# Skills translation dictionary (Polish to English)
SKILLS_TRANSLATION = {
    "Rozwiązywanie problemów": "Problem Solving",
    "Produkty Databricks": "Databricks Products",
    "Planowanie budżetu i prognozowanie": "Budget Planning & Forecasting",
    "Media cyfrowe": "Digital Media",
    "Projektowanie badań": "Research Design",
    "Matematyka stosowana": "Applied Mathematics",
    "Modelowanie matematyczne": "Mathematical Modeling",
    "Nauczanie maszynowe": "Machine Learning",
    "Analiza szeregów czasowych": "Time Series Analysis",
    "Modelowanie statystyczne": "Statistical Modeling",
    "Analiza danych": "Data Analysis",
    "Modelowanie biznesowe": "Business Modeling",
    "Prezentacje": "Presentations",
    "Tabele przestawne": "Pivot Tables",
    "Ekonometria": "Econometrics",
    "Media społecznościowe": "Social Media",
    "Analiza sprzedaży": "Sales Analysis",
    "Analiza danych biznesowych": "Business Data Analysis",
    "Angielski biznesowy": "Business English",
    "Matematyka": "Mathematics",
    "Ekonomia": "Economics",
    "Zarządzanie produkcją": "Production Management",
    "Angielski": "English",
    "Praca zespołowa": "Teamwork",
    "Umiejętności analityczne": "Analytical Skills",
    "Statystyka": "Statistics",
    "Python (Programming Language)": "Python",
    "Statistical concepts": "Statistical Concepts",
}

# Skills categories for grouping
SKILLS_CATEGORIES = {
    "Programming": ["Python", "R", "SQL", "Git", "HTML", "LaTeX", "Microsoft Visual Studio Code"],
    "Data Science & ML": ["Machine Learning", "Supervised Learning", "Data Science", "Sklearn", 
                          "Time Series Analysis", "Statistical Modeling", "Econometrics", 
                          "Data Analysis", "Statistics", "Mathematical Modeling", "Applied Mathematics",
                          "Statistical Concepts", "Mathematics"],
    "AI & Automation": ["AI", "AI Agents", "Anthropic Claude", "Cursor AI", "GitHub Copilot", "Nixtla"],
    "Analytics & Tools": ["Microsoft Power BI", "Databricks Products", "Cloud Computing", 
                          "Microsoft Excel", "Pivot Tables", "PowerPoint", "Microsoft Office",
                          "Microsoft Word", "Canva"],
    "Business": ["Project Management", "Project Planning", "Business Modeling", "Sales Analysis",
                 "Business Data Analysis", "Budget Planning & Forecasting", "Presentations",
                 "Production Management", "Research Design"],
    "Communication": ["Teamwork", "English", "Business English", "Social Media", "Digital Media",
                      "Problem Solving", "Analytical Skills"],
}


def get_experience_bullets(title, company):
    """Get pre-written bullet points for a position."""
    return EXPERIENCE_DESCRIPTIONS.get((title, company), [])


def get_education_info(degree, school, notes=""):
    """Get pre-written education summary, field of study, and thesis."""
    # Try exact match first
    result = EDUCATION_DESCRIPTIONS.get((degree, school))
    if result:
        return result
    
    # For Licencjat degrees, distinguish by content in notes
    if "Licencjat" in degree:
        if "algebra" in notes.lower() or "topology" in notes.lower() or "wave equation" in notes.lower():
            return EDUCATION_DESCRIPTIONS.get((degree, school, "math"), {"field_of_study": "", "summary": "", "thesis": ""})
        else:
            return EDUCATION_DESCRIPTIONS.get((degree, school, "econ"), {"field_of_study": "", "summary": "", "thesis": ""})
    
    return {"field_of_study": "", "summary": "", "thesis": ""}


# =============================================================================
# THEME: Minimal White Blue Modern (Compact)
# =============================================================================

COLORS = {
    "accent": HexColor("#2563EB"),
    "heading": HexColor("#1E40AF"),
    "body": HexColor("#1F2937"),
    "secondary": HexColor("#374151"),
    "muted": HexColor("#6B7280"),
    "rule": HexColor("#D1D5DB"),
}


def register_fonts():
    """Register fonts from canvas-fonts directory."""
    pdfmetrics.registerFont(TTFont("Display", FONTS_DIR / "BricolageGrotesque-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Body", FONTS_DIR / "BricolageGrotesque-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("Accent", FONTS_DIR / "JetBrainsMono-Regular.ttf"))


def read_csv(filename):
    """Read a CSV file and return list of dictionaries."""
    filepath = INPUT_DIR / filename
    if not filepath.exists():
        return []
    
    rows = []
    for encoding in ["utf-8-sig", "utf-8", "latin-1"]:
        try:
            with open(filepath, encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned = {k.strip(): v.strip() if v else "" for k, v in row.items()}
                    rows.append(cleaned)
            break
        except (UnicodeDecodeError, csv.Error):
            continue
    return rows


def parse_profile():
    """Parse Profile.csv and Profile Summary.csv."""
    rows = read_csv("Profile.csv")
    if not rows:
        return {}
    
    profile = rows[0]
    first_name = profile.get("First Name", "")
    last_name = profile.get("Last Name", "")
    name = f"{first_name} {last_name}".strip()
    headline = profile.get("Headline", "").replace("👩‍💻", "").strip()
    summary = profile.get("Summary", "")
    location = profile.get("Geo Location", "")
    
    if not summary:
        summary_rows = read_csv("Profile Summary.csv")
        if summary_rows:
            summary = summary_rows[0].get("Profile Summary", "")
    
    return {"name": name, "headline": headline, "summary": summary, "location": location}


def parse_contact():
    """Parse Email Addresses.csv and PhoneNumbers.csv."""
    contact = {}
    
    email_rows = read_csv("Email Addresses.csv")
    for row in email_rows:
        if row.get("Primary", "").lower() == "yes":
            contact["email"] = row.get("Email Address", "")
            break
        if row.get("Confirmed", "").lower() == "yes" and "email" not in contact:
            contact["email"] = row.get("Email Address", "")
    
    phone_rows = read_csv("PhoneNumbers.csv")
    for row in phone_rows:
        number = row.get("Number", "").strip()
        if number:
            contact["phone"] = number
            break
    
    return contact


def parse_links():
    """Parse Links.csv for portfolio and other links (non-standard LinkedIn file)."""
    filepath = INPUT_DIR / "Links.csv"
    if not filepath.exists():
        return []
    
    links = []
    for encoding in ["utf-8-sig", "utf-8", "latin-1"]:
        try:
            with open(filepath, encoding=encoding) as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        label = row[0].strip()
                        url = row[1].strip()
                        if label and url:
                            # Clean up URL for display
                            display_url = url.replace("https://", "").replace("http://", "")
                            links.append({"label": label, "url": url, "display": display_url})
            break
        except (UnicodeDecodeError, csv.Error):
            continue
    return links


def parse_positions():
    """Parse Positions.csv."""
    rows = read_csv("Positions.csv")
    
    def parse_date(date_str):
        if not date_str:
            return (9999, 12)
        parts = date_str.split()
        months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                  "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        if len(parts) >= 2:
            return (int(parts[1]) if parts[1].isdigit() else 2000, months.get(parts[0], 1))
        return (2000, 1)
    
    positions = []
    for row in rows:
        started = row.get("Started On", "")
        finished = row.get("Finished On", "")
        date_range = f"{started} – {finished}" if finished else f"{started} – Present"
        
        title = row.get("Title", "")
        company = row.get("Company Name", "")
        
        # Use pre-written bullet points (LLM-analyzed)
        formatted_bullets = get_experience_bullets(title, company)
        
        positions.append({
            "title": title,
            "company": company,
            "location": row.get("Location", ""),
            "date_range": date_range,
            "description_bullets": formatted_bullets,
            "sort_key": parse_date(started),
        })
    
    positions.sort(key=lambda x: x["sort_key"], reverse=True)
    return positions


def parse_education():
    """Parse Education.csv."""
    rows = read_csv("Education.csv")
    
    def parse_date(date_str):
        if not date_str:
            return (9999, 12)
        parts = date_str.split()
        months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                  "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
        if len(parts) >= 2:
            return (int(parts[1]) if parts[1].isdigit() else 2000, months.get(parts[0], 1))
        return (2000, 1)
    
    education = []
    for row in rows:
        started = row.get("Start Date", "")
        ended = row.get("End Date", "")
        date_range = f"{started} – {ended}" if ended else (f"{started} – Present" if started else "")
        
        raw_notes = row.get("Notes", "")
        degree = row.get("Degree Name", "")
        school = row.get("School Name", "")
        
        # Use pre-written education info (LLM-analyzed)
        edu_info = get_education_info(degree, school, raw_notes)
        
        education.append({
            "school": school,
            "degree": degree,
            "field_of_study": edu_info.get("field_of_study", ""),
            "date_range": date_range,
            "summary": edu_info["summary"],
            "thesis": edu_info["thesis"],
            "sort_key": parse_date(started),
        })
    
    education.sort(key=lambda x: x["sort_key"], reverse=True)
    return education


def parse_skills():
    """Parse Skills.csv, translate to English, and group by category."""
    rows = read_csv("Skills.csv")
    raw_skills = [row.get("Name", "") for row in rows if row.get("Name")]
    
    # Translate all skills to English
    translated = []
    for skill in raw_skills:
        translated_skill = SKILLS_TRANSLATION.get(skill, skill)
        if translated_skill not in translated:
            translated.append(translated_skill)
    
    # Group skills by category
    categorized = {}
    uncategorized = []
    
    for skill in translated:
        placed = False
        for category, category_skills in SKILLS_CATEGORIES.items():
            if skill in category_skills:
                if category not in categorized:
                    categorized[category] = []
                if skill not in categorized[category]:
                    categorized[category].append(skill)
                placed = True
                break
        if not placed and skill not in uncategorized:
            uncategorized.append(skill)
    
    # Add uncategorized skills to "Other" if any
    if uncategorized:
        categorized["Other"] = uncategorized
    
    return categorized


def parse_languages():
    """Parse Languages.csv."""
    rows = read_csv("Languages.csv")
    return [{"name": row.get("Name", "").capitalize(), 
             "proficiency": row.get("Proficiency", "")} 
            for row in rows if row.get("Name")]


def parse_certifications():
    """Parse Certifications.csv."""
    rows = read_csv("Certifications.csv")
    certs = []
    for row in rows:
        name = row.get("Name", "")
        if name:
            certs.append({
                "name": name,
                "authority": row.get("Authority", ""),
                "date": f"Issued {row.get('Started On', '')}" if row.get("Started On") else "",
            })
    return certs


def create_compact_styles():
    """Create paragraph styles for single-page CV with full page utilization."""
    return {
        "name": ParagraphStyle(
            "Name", fontName="Display", fontSize=26, leading=30,
            textColor=COLORS["accent"], spaceAfter=4,
        ),
        "headline": ParagraphStyle(
            "Headline", fontName="Body", fontSize=10, leading=14,
            textColor=COLORS["secondary"], spaceAfter=2,
        ),
        "contact": ParagraphStyle(
            "Contact", fontName="Accent", fontSize=8, leading=12,
            textColor=COLORS["muted"], spaceAfter=0,
        ),
        "section_heading": ParagraphStyle(
            "SectionHeading", fontName="Display", fontSize=10.5, leading=14,
            textColor=COLORS["heading"], spaceAfter=0,
        ),
        "job_title": ParagraphStyle(
            "JobTitle", fontName="Display", fontSize=9.5, leading=13,
            textColor=COLORS["body"], spaceAfter=0,
        ),
        "company": ParagraphStyle(
            "Company", fontName="Body", fontSize=8.5, leading=12,
            textColor=COLORS["secondary"], spaceAfter=0,
        ),
        "date_range": ParagraphStyle(
            "DateRange", fontName="Accent", fontSize=7.5, leading=11,
            textColor=COLORS["muted"], spaceAfter=3,
        ),
        "bullet_item": ParagraphStyle(
            "BulletItem", fontName="Body", fontSize=8.5, leading=11.5,
            textColor=COLORS["body"], alignment=TA_LEFT, spaceAfter=2,
        ),
        "edu_summary": ParagraphStyle(
            "EduSummary", fontName="Body", fontSize=8, leading=11,
            textColor=COLORS["muted"], spaceAfter=1,
        ),
        "thesis": ParagraphStyle(
            "Thesis", fontName="Body", fontSize=8, leading=11,
            textColor=COLORS["secondary"], spaceAfter=1,
        ),
        "skills": ParagraphStyle(
            "Skills", fontName="Body", fontSize=8, leading=11,
            textColor=COLORS["secondary"], spaceAfter=0,
        ),
        "skills_category": ParagraphStyle(
            "SkillsCategory", fontName="Display", fontSize=7.5, leading=10,
            textColor=COLORS["heading"], spaceAfter=0,
        ),
        "languages": ParagraphStyle(
            "Languages", fontName="Body", fontSize=8.5, leading=12,
            textColor=COLORS["body"], spaceAfter=0,
        ),
        "cert_name": ParagraphStyle(
            "CertName", fontName="Body", fontSize=8.5, leading=11,
            textColor=COLORS["body"], spaceAfter=0,
        ),
    }


def add_section_heading_compact(flowables, styles, title):
    """Add a section heading with balanced spacing."""
    flowables.append(Spacer(1, 10))
    flowables.append(HRFlowable(
        width="100%", thickness=0.4, color=COLORS["rule"],
        spaceAfter=5, spaceBefore=0,
    ))
    flowables.append(Paragraph(title.upper(), styles["section_heading"]))
    flowables.append(Spacer(1, 5))


def build_left_column(profile, contact, links, positions, styles):
    """Build left column: Header + Experience."""
    flowables = []
    
    # Name
    if profile.get("name"):
        flowables.append(Paragraph(escape(profile["name"]), styles["name"]))
    
    # Headline
    if profile.get("headline"):
        flowables.append(Paragraph(escape(profile["headline"]), styles["headline"]))
    
    # Contact line
    contact_parts = []
    if profile.get("location"):
        contact_parts.append(profile["location"])
    if contact.get("email"):
        contact_parts.append(contact["email"])
    if contact.get("phone"):
        contact_parts.append(contact["phone"])
    if contact_parts:
        flowables.append(Spacer(1, 2))
        flowables.append(Paragraph(" · ".join(contact_parts), styles["contact"]))
    
    # Links line (portfolio, personal projects)
    if links:
        links_parts = []
        for link in links:
            # Create clickable link with label
            link_text = f'<link href="{link["url"]}">{escape(link["label"])}</link> {link["display"]}'
            links_parts.append(link_text)
        flowables.append(Spacer(1, 2))
        flowables.append(Paragraph(" · ".join(links_parts), styles["contact"]))
    
    # Experience
    if positions:
        add_section_heading_compact(flowables, styles, "Experience")
        
        for i, pos in enumerate(positions[:7]):
            if i > 0:
                flowables.append(Spacer(1, 8))
            
            flowables.append(Paragraph(escape(pos["title"]), styles["job_title"]))
            
            company_date = f"{pos['company']} · {pos['date_range']}"
            flowables.append(Paragraph(escape(company_date), styles["date_range"]))
            
            if pos.get("description_bullets"):
                for bullet in pos["description_bullets"][:4]:
                    bullet_text = f"• {escape(bullet)}"
                    flowables.append(Paragraph(bullet_text, styles["bullet_item"]))
    
    return flowables


def build_right_column(education, skills, certifications, languages, styles):
    """Build right column: Education + Skills + Certs + Languages."""
    flowables = []
    
    # Education - show all entries without grouping to preserve all degrees
    if education:
        flowables.append(Paragraph("EDUCATION", styles["section_heading"]))
        flowables.append(Spacer(1, 5))
        
        for i, edu in enumerate(education):
            if i > 0:
                flowables.append(Spacer(1, 6))
            
            flowables.append(Paragraph(escape(edu["school"]), styles["job_title"]))
            
            if edu.get("degree") or edu.get("field_of_study"):
                degree_parts = []
                if edu.get("degree"):
                    degree_parts.append(edu["degree"])
                if edu.get("field_of_study"):
                    degree_parts.append(f"in {edu['field_of_study']}")
                degree_line = " ".join(degree_parts)
                if edu.get("date_range"):
                    degree_line += f" ({edu['date_range']})"
                flowables.append(Paragraph(escape(degree_line), styles["company"]))
            
            if edu.get("summary"):
                flowables.append(Paragraph(escape(edu["summary"]), styles["edu_summary"]))
            
            if edu.get("thesis"):
                thesis_text = f"Thesis: {edu['thesis']}"
                flowables.append(Paragraph(escape(thesis_text), styles["thesis"]))
    
    # Skills - show ALL skills grouped by category
    if skills:
        add_section_heading_compact(flowables, styles, "Skills")
        
        # Define display order for categories
        category_order = ["Programming", "Data Science & ML", "AI & Automation", 
                         "Analytics & Tools", "Business", "Communication", "Other"]
        
        for category in category_order:
            if category in skills and skills[category]:
                category_skills = skills[category]
                category_text = f"<b>{category}:</b> {', '.join(category_skills)}"
                flowables.append(Paragraph(category_text, styles["skills"]))
                flowables.append(Spacer(1, 4))
    
    # Certifications - show full names without truncation
    if certifications:
        add_section_heading_compact(flowables, styles, "Certifications")
        
        for cert in certifications:
            flowables.append(Paragraph(escape(cert["name"]), styles["cert_name"]))
            if cert.get("authority"):
                flowables.append(Paragraph(escape(cert["authority"]), styles["date_range"]))
            flowables.append(Spacer(1, 4))
    
    # Languages
    if languages:
        add_section_heading_compact(flowables, styles, "Languages")
        
        lang_parts = []
        for lang in languages:
            prof = lang["proficiency"].replace(" proficiency", "").replace("Native or bilingual", "Native")
            lang_parts.append(f"{lang['name']} ({prof})")
        flowables.append(Paragraph(" · ".join(lang_parts), styles["languages"]))
    
    return flowables


def build_cv():
    """Build a single-page, two-column CV."""
    register_fonts()
    
    profile = parse_profile()
    contact = parse_contact()
    links = parse_links()
    positions = parse_positions()
    education = parse_education()
    skills = parse_skills()
    languages = parse_languages()
    certifications = parse_certifications()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    doc = SimpleDocTemplate(
        str(OUTPUT_FILE),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    
    styles = create_compact_styles()
    
    left_flowables = build_left_column(profile, contact, links, positions, styles)
    right_flowables = build_right_column(education, skills, certifications, languages, styles)
    
    left_table = Table(
        [[f] for f in left_flowables],
        colWidths=[LEFT_COL_WIDTH],
    )
    left_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    right_table = Table(
        [[f] for f in right_flowables],
        colWidths=[RIGHT_COL_WIDTH],
    )
    right_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    main_table = Table(
        [[left_table, right_table]],
        colWidths=[LEFT_COL_WIDTH, RIGHT_COL_WIDTH + GUTTER],
    )
    main_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (0, 0), 0),
        ('LEFTPADDING', (1, 0), (1, 0), GUTTER),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    
    doc.build([main_table])
    return OUTPUT_FILE


if __name__ == "__main__":
    output_path = build_cv()
    print(f"CV generated: {output_path}")
