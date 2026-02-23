---
name: linkedin-cv
description: Generate a beautifully typeset CV PDF directly from a LinkedIn data export. Use when the user wants to create a CV, resume, or curriculum vitae from their LinkedIn data, or mentions generating a CV from LinkedIn.
---

# LinkedIn CV Generator

Create a meticulously crafted, purely typographic CV directly from a LinkedIn data export (CSV files). No intermediate files, no scraping — the user downloads their data from LinkedIn, and the agent turns it into a professional PDF.

## The Core Philosophy

This is **typographic design**, not decoration. Every design decision is made through:
- **Font pairing** — contrasting weights, styles, and families to build hierarchy
- **Whitespace** — generous margins, section breathing room, line spacing as a design tool
- **Alignment** — a strict grid that organizes information with invisible precision
- **Scale** — deliberate size relationships between name, headings, body, and metadata
- **Color** — a restrained palette applied only through text color (no boxes, lines, or fills beyond simple thin rules)

Nothing is ornamental. Everything communicates.

## Prerequisites

### Project setup

Run `uv sync` to install dependencies (`reportlab`) into the project virtual environment.

### Font prerequisite

The skill uses fonts from the **canvas-design** skill. Ensure the canvas-design skill is installed at `~/.cursor/skills/canvas-design/` with its `canvas-fonts/` subdirectory containing TTF files.

### Getting the LinkedIn Data

If the user hasn't already downloaded their LinkedIn data, instruct them:

1. Go to **LinkedIn.com** → click your profile photo → **Settings & Privacy**
2. Navigate to **Data privacy** → **Get a copy of your data**
3. Click **Request archive** — LinkedIn will email a download link (usually within 10 minutes, sometimes up to 24 hours)
4. Download the ZIP file and **unzip** it
5. Place the CSV files into `input/<name>/` in the project directory (e.g. `input/jane_doe/`)

**Expected files after unzipping** (not all may be present depending on profile completeness):

| File | What it provides |
|---|---|
| `Profile.csv` | Name, headline, summary, location, industry |
| `Profile Summary.csv` | Professional summary (may be empty) |
| `Positions.csv` | Work experience entries |
| `Education.csv` | Education history |
| `Skills.csv` | Skills list |
| `Languages.csv` | Languages and proficiency |
| `Certifications.csv` | Certifications with issuer and dates |
| `Email Addresses.csv` | Contact email(s) |
| `PhoneNumbers.csv` | Phone number(s) |

**Minimum required**: `Profile.csv` and at least one of `Positions.csv` or `Education.csv` to generate a meaningful CV. All other files enrich the output but are optional.

### Handling Additional Custom Files

The input folder may contain files beyond the standard LinkedIn export. These could include:
- `Hobbies.csv` or `Interests.csv` — personal interests and hobbies
- `Volunteer.csv` or `Volunteering.csv` — volunteer work
- `Projects.csv` — personal or side projects
- `Publications.csv` — articles, papers, or books
- `Awards.csv` — honors and awards
- `References.csv` — professional references
- `Links.csv` — additional portfolio or social links
- Any other `.csv`, `.txt`, or `.md` files with custom content

**The agent MUST check for these additional files and intelligently incorporate them as new sections at the end of the CV.**

## Workflow

### Step 0: Ensure Dependencies

Before generating anything, ensure project dependencies are installed:

```bash
uv sync
```

This installs `reportlab` and any other dependencies from `pyproject.toml` into the project's `.venv`.

### Step 1: Parse the User Prompt and Locate Data

The user prompt follows this pattern:

```
Generate a CV from LinkedIn data for <name> with a "<theme>" theme
```

Extract two pieces of information:
- **Name** — the person's name (e.g. `jane_doe`). This determines the input subfolder and output paths.
- **Theme** — the style direction (e.g. `"minimal swiss"`). Used to select fonts, colors, and typographic personality.

Locate the LinkedIn export at `input/<name>/` in the workspace root (where `<name>` matches what the user provided). If the user provides an explicit path instead, use that.

Use `Glob` to discover which CSV files exist inside that folder, then **read the CSV files** to understand the actual content. A LinkedIn data export typically contains these files:

| File | Contains | Required? |
|---|---|---|
| `Profile.csv` | First Name, Last Name, Headline, Summary, Industry, Geo Location, Websites | **Yes** — core identity |
| `Profile Summary.csv` | Single-column file with the professional summary text | No — often empty; fallback for Summary |
| `Positions.csv` | Company Name, Title, Description, Location, Started On, Finished On | **Yes** — work experience |
| `Education.csv` | School Name, Degree Name, Start Date, End Date, Notes, Activities | **Yes** — education history |
| `Skills.csv` | Single column `Name` with one skill per row | No |
| `Languages.csv` | Name, Proficiency | No |
| `Certifications.csv` | Name, Url, Authority, Started On, Finished On, License Number | No |
| `Email Addresses.csv` | Email Address, Confirmed, Primary, Updated On | No — for contact info |
| `PhoneNumbers.csv` | Extension, Number, Type | No — for contact info |

Parse each CSV using Python's `csv.DictReader` with UTF-8 encoding (try `utf-8-sig` as fallback). Strip whitespace from all keys and values. Handle missing files gracefully — a missing file means that section is empty.

**Field mappings:**

#### Profile.csv → header fields

| CSV Column | Usage | Notes |
|---|---|---|
| `First Name` + `Last Name` | Name (hero element) | Concatenate with a space |
| `Headline` | Subtitle under name | Direct mapping |
| `Summary` | About section | Preserve paragraph breaks as `\n`. **If empty, check `Profile Summary.csv`** |
| `Geo Location` | Location line | Direct mapping |
| `Industry` | Industry context | Can be used as a secondary subtitle or omitted |
| `Websites` | Personal links | Include in contact info if present |

#### Profile Summary.csv → about section (fallback)

This file has a single column `Profile Summary`. It may contain a multi-line professional summary. Use this as the About section **only if** `Profile.csv`'s `Summary` field is empty.

#### Email Addresses.csv → contact info

| CSV Column | Usage | Notes |
|---|---|---|
| `Email Address` | Contact email | Use the row where `Primary` is `Yes`, or the first `Confirmed` = `Yes` row |
| `Confirmed` | Filter | Only use confirmed addresses |
| `Primary` | Filter | Prefer primary address |

#### PhoneNumbers.csv → contact info

| CSV Column | Usage | Notes |
|---|---|---|
| `Number` | Phone number | Strip leading/trailing whitespace. May include country code (e.g. `+48 512 012 989`) |
| `Type` | Label | May be empty; use if present (e.g. "Mobile") |
| `Extension` | Extension | Usually empty; append if present |

**Note**: Phone numbers may have leading spaces. Always `.strip()` the value.

#### Positions.csv → experience entries

| CSV Column | Usage | Notes |
|---|---|---|
| `Title` | Job title | Direct mapping |
| `Company Name` | Company | Direct mapping |
| `Started On` / `Finished On` | Date range | Format as `"Mon YYYY – Mon YYYY"` or `"Mon YYYY – Present"` if Finished On is empty. Raw format is `"Mon YYYY"` (e.g. `Sep 2024`) |
| `Location` | Location | Direct mapping. May be in local language (e.g. `"Warszawa, Woj. Mazowieckie, Polska"`) |
| `Description` | Role description | Preserve line breaks. May be empty for some positions |

Sort by start date descending (most recent first).

#### Education.csv → education entries

| CSV Column | Usage | Notes |
|---|---|---|
| `School Name` | School | Direct mapping |
| `Degree Name` | Degree | Direct mapping. May be in local language (e.g. `"Magister (Mgr)"`, `"Licencjat (Lic.)"`) |
| `Field Of Study` | Field of study | **MUST be displayed**. Shows the major/concentration (e.g., "Data Science", "Mathematics"). If missing, derive from Notes or thesis. |
| `Notes` | Coursework / field of study | Often contains detailed coursework lists. Also check for field of study clues if `Field Of Study` column is missing. |
| `Start Date` / `End Date` | Date range | Format like experience dates. `End Date` may be empty if ongoing |
| `Activities` | Extracurriculars | Use if present; often empty |

**CRITICAL - Field of Study**: The field of study MUST be displayed for each education entry. This is essential context (e.g., "M.Sc. in Data Science" vs just "Master's degree"). If the `Field Of Study` column is missing, the LLM MUST derive it from the Notes (coursework topics) or thesis during Step 2 processing.

**Note on Education Notes**: The `Notes` field can be very long (full coursework lists). For CV readability, either summarize key topics or show only the first few items with "..." truncation. Never dump the entire raw list.

**CRITICAL - Do NOT group education entries**: A person may have multiple degrees from the same institution (e.g., Bachelor's and Master's from the same university, or two Bachelor's degrees in different fields). Each `Education.csv` row is a separate degree entry and must be rendered individually with its own date range, degree name, summary, and thesis info. Never consolidate or group by school name.

#### Skills.csv → skills list

Single column `Name`. Each row has one skill name. Collect into a flat list.

**CRITICAL - Skill Processing Requirements:**

1. **Show ALL skills** — Never truncate or limit skills. Display every skill from the export.

2. **Translate to English** — Skills may be in mixed languages (e.g., Polish). Translate ALL non-English skills to their English equivalents. Common translations:
   - "Analiza danych" → "Data Analysis"
   - "Uczenie maszynowe" / "Nauczanie maszynowe" → "Machine Learning"
   - "Analiza szeregów czasowych" → "Time Series Analysis"
   - "Modelowanie statystyczne" → "Statistical Modeling"
   - "Praca zespołowa" → "Teamwork"
   - "Umiejętności analityczne" → "Analytical Skills"
   - "Rozwiązywanie problemów" → "Problem Solving"
   - etc.

3. **Group by category** — Organize skills into logical categories for better readability:
   - **Programming**: Python, R, SQL, Git, HTML, LaTeX, etc.
   - **Data Science & ML**: Machine Learning, Deep Learning, Sklearn, Time Series Analysis, etc.
   - **Analytics & Tools**: Power BI, Excel, Databricks, Statistical Modeling, etc.
   - **AI & Automation**: AI Agents, Claude, Cursor AI, GitHub Copilot, etc.
   - **Business**: Project Management, Presentations, Business Analysis, etc.

4. **Remove duplicates** — After translation, deduplicate skills (e.g., "Python" and "Python (Programming Language)" become just "Python").

#### Languages.csv → languages list

| CSV Column | Usage |
|---|---|
| `Name` | Language name (may be in the local language, e.g. `"angielski"` for English) |
| `Proficiency` | Proficiency level (e.g. `"Full professional proficiency"`, `"Native or bilingual proficiency"`) |

#### Certifications.csv → certifications list

| CSV Column | Usage |
|---|---|
| `Name` | Certification name |
| `Url` | Link to certificate (include if generating a digital/interactive PDF, otherwise omit) |
| `Authority` | Issuing organization |
| `Started On` | Format as `"Issued Mon YYYY"` |
| `Finished On` | Expiry date — format as `"Expires Mon YYYY"` if present |
| `License Number` | License/certificate number — include if present |

**Important**: Column names may vary slightly across exports. Match case-insensitively and try common variants. Skip missing columns gracefully rather than erroring.

**CRITICAL - Do NOT truncate certification names**: Certification names should be displayed in full. If a name is long, allow text to wrap naturally rather than truncating with "...". Truncation loses important information like proficiency levels and credential types.

### Step 2: Rewrite Descriptions with Language Model (CRITICAL)

**This step is mandatory.** Raw LinkedIn descriptions are often poorly formatted — run-on sentences, no structure, missing punctuation, walls of text with bullet points starting mid-sentence. Before generating any code, YOU (the language model) must analyze and rewrite all descriptions into clean, professional content.

#### Why This Step Exists

LinkedIn export descriptions are notoriously messy:
- Multiple responsibilities jammed into one paragraph
- Missing periods between sentences
- Random capitalization
- Bullet points that split logical phrases

Regex-based parsing in Python code **cannot reliably fix these issues**. Only a language model can understand the semantic meaning and restructure the text properly.

#### Process

1. **Read the CSV files** — Use the Read tool to examine `Positions.csv` (the `Description` column) and `Education.csv` (the `Notes` column)

2. **Analyze each description** — For each non-empty description, identify:
   - Distinct responsibilities or achievements
   - Action verbs and their associated outcomes
   - Technical skills and tools mentioned
   - Logical sentence boundaries (not just regex patterns)

3. **Rewrite as structured bullet points** — Transform each description into 3-5 clean bullet points that:
   - Start with an action verb (Built, Developed, Managed, Led, Created, etc.)
   - Contain complete sentences or coherent phrases
   - Never split a logical idea across bullet points
   - Highlight quantifiable achievements when present

4. **Rewrite education notes** — For education entries:
   - Extract the core focus areas (2-4 topics max)
   - Identify any thesis topic
   - Remove verbose course listings
   - Keep only meaningful information

5. **Store the rewritten content** — Create a data structure (dictionary) that maps each position/education entry to its rewritten bullet points. This will be embedded directly into the generated Python script.

#### Example Transformation

**Raw LinkedIn description:**
```
End-to-end Machine Learning projects including fraud detectionWorking with LightGBM, scikit-learnManaging data pipelines in production environments using AirflowWeekly presentations to stakeholders
```

**Rewritten by language model:**
```python
[
    "Led end-to-end machine learning projects including fraud detection systems",
    "Developed models using LightGBM and scikit-learn frameworks",
    "Managed production data pipelines with Apache Airflow",
    "Delivered weekly presentations to stakeholders on project outcomes"
]
```

#### Output of This Step

After completing this step, you should have:
- A Python dictionary mapping position titles/companies to their rewritten bullet points
- A Python dictionary mapping education entries to their summary and thesis
- These dictionaries will be **hardcoded into the generated Python script**, replacing any regex-based parsing

**CRITICAL**: Do not skip this step. Do not rely on Python regex to format descriptions. The language model MUST rewrite all descriptions before code generation.

### Step 2b: Detect and Process Additional Custom Files (CRITICAL)

After processing the standard LinkedIn files, the agent MUST scan the input folder for any additional files that are not part of the standard LinkedIn export.

#### Standard LinkedIn Files (ignore these in this step)

These are the known LinkedIn export files — they're already handled in Step 1:
- `Profile.csv`
- `Profile Summary.csv`
- `Positions.csv`
- `Education.csv`
- `Skills.csv`
- `Languages.csv`
- `Certifications.csv`
- `Email Addresses.csv`
- `PhoneNumbers.csv`
- `Connections.csv` (not used in CV)
- `Messages.csv` (not used in CV)
- `Invitations.csv` (not used in CV)
- `Reactions.csv` (not used in CV)
- `Endorsement*.csv` (not used in CV)
- `Registration.csv` (not used in CV)

#### Process for Additional Files

1. **Scan the input folder** — Use `Glob` or `ls` to list all files in `input/<name>/`

2. **Identify non-standard files** — Any file not in the standard list above is a candidate for a custom section. Supported formats:
   - `.csv` files — parse as structured data
   - `.txt` files — read as plain text
   - `.md` files — read as markdown (strip formatting for CV)

3. **Analyze each additional file** — For each non-standard file, YOU (the language model) MUST:
   - Read the file contents using the Read tool
   - **Infer the section topic** from the filename and content:
     - `Hobbies.csv` or `Interests.txt` → "Interests" or "Hobbies" section
     - `Volunteer.csv` → "Volunteer Experience" section
     - `Projects.csv` → "Projects" section
     - `Publications.csv` → "Publications" section
     - `Awards.csv` → "Honors & Awards" section
     - `Links.csv` → "Links" or merge into Contact section
     - Generic files → derive section name from content theme
   - **Extract meaningful content** — parse the data and understand what it represents
   - **Rewrite for CV format** — clean up the content just like Step 2 does for experience

4. **Determine section placement** — Additional sections go at the END of the CV, after the standard sections. Suggested order:
   - Volunteer Experience (if present)
   - Projects (if present)
   - Publications (if present)
   - Honors & Awards (if present)
   - Interests/Hobbies (if present) — always last as it's least professional
   - Other custom sections

5. **Store processed content** — Create a dictionary mapping section names to their formatted content, to be embedded in the generated Python script

#### Example: Processing a Links File

**File discovered**: `input/jane_doe/Links.csv`

**Raw content**:
```csv
My Portfolio, https://github.com/janedoe
Personal Blog, https://janedoe.com/blog
```

**Agent analysis**:
- Filename suggests external links/portfolio
- Best integrated into the Contact header section
- URLs must be displayed visibly (not hidden under text)

**Processed output**:
```python
# Links displayed with visible URLs in contact section
# Format: "Label: visible-url" (clickable but URL always shown)
links = [
    {"label": "My Portfolio", "url": "https://github.com/janedoe", "display": "github.com/janedoe"},
    {"label": "Personal Blog", "url": "https://janedoe.com/blog", "display": "janedoe.com/blog"}
]
```

**CRITICAL - Link Display Requirements**:
- Links must ALWAYS show the visible URL, never hide it under text
- Format: `Label: url` where the URL is clickable but fully visible
- Remove `https://` and `http://` prefixes from display URL for cleaner appearance
- Links are typically placed in the header/contact section for easy access

#### Example: Processing a Hobbies File

**File discovered**: `input/jane_doe/Hobbies.csv`

**Raw content**:
```csv
Hobby,Description
Photography,Street and landscape photography
Running,Completed 3 marathons
Cooking,Specializing in Italian cuisine
```

**Agent analysis**:
- Filename suggests "Hobbies" section
- Content confirms personal interests
- Suitable for "Interests" section at CV end

**Processed output for script**:
```python
additional_sections = {
    "Interests": [
        "Photography — street and landscape",
        "Running — marathon finisher (3 completed)",
        "Cooking — specializing in Italian cuisine"
    ]
}
```

#### Example: Processing a Projects File

**File discovered**: `input/jane_doe/Projects.txt`

**Raw content**:
```
Personal ML Pipeline
Built an end-to-end ML pipeline for stock prediction using Python and TensorFlow

Open Source Contribution
Contributed to pandas library - fixed 5 bugs related to datetime handling
```

**Agent analysis**:
- Filename suggests "Projects" section
- Content shows technical projects with descriptions
- Good for professional credibility

**Processed output**:
```python
additional_sections = {
    "Projects": [
        ("Personal ML Pipeline", "Built end-to-end ML pipeline for stock prediction using Python and TensorFlow"),
        ("Open Source Contribution", "Contributed to pandas library — fixed 5 bugs related to datetime handling")
    ]
}
```

#### Important Guidelines

- **Never fabricate content** — only include what's actually in the files
- **Smart inference** — use the filename AND content to determine the section type
- **Professional judgment** — if content seems inappropriate for a CV (e.g., personal diary entries), skip it
- **Flexible formatting** — adapt the section layout based on the content type (list vs. entries with descriptions)
- **Space awareness** — additional sections must still fit within the single-page constraint. If space is limited, summarize or use compact formatting

### Step 3: Interpret the User Theme

The user provides a theme name, mood, or color direction. Interpret this the way a designer would: extract a feeling, a palette sensibility, and a typographic personality.

| Theme Aspect | Design Decision |
|---|---|
| **Mood** | Formal → serif-heavy, tight spacing. Creative → sans-serif mix, generous whitespace. Technical → monospace accents, grid precision. |
| **Color palette** | Derive 2-3 text colors maximum. One dominant (body), one accent (headings/name), one muted (dates/metadata). No background colors — always white/off-white page. |
| **Typographic voice** | Quiet authority → thin weights, large sizes. Bold confidence → heavy weights, compact layout. Elegant restraint → italic accents, wide letter-spacing on headings. |

**CRITICAL**: The theme is a lens, not a costume. Always maintain CV readability and professionalism.

### Step 4: Select Fonts

Choose fonts from the `canvas-fonts` directory at `~/.cursor/skills/canvas-design/canvas-fonts/`. See [references/font-pairings.md](references/font-pairings.md) for curated combinations.

Select exactly **2-3 fonts** forming a system:

| Role | Purpose | Typical Choice |
|---|---|---|
| **Display** | Name, possibly section headings | A font with personality — serif or distinctive sans |
| **Body** | Descriptions, about section, experience details | Highly readable at small sizes — clean sans or book serif |
| **Accent** (optional) | Dates, metadata, labels, skills | Monospace or contrasting weight of body font |

Register all fonts with `reportlab.pdfbase.ttfonts.TTFont` and `pdfmetrics.registerFont`.

### Step 5: Filter Empty Sections

Before building the layout, check each data section. **Only include a section if it contains meaningful content.**

- A list with no entries → skip entirely
- A string that is empty or whitespace-only → skip entirely

**Do not render a section heading, spacing, or horizontal rule for any empty section.** The CV should read as if the empty sections never existed.

### Step 6: Build the CV Layout

Use `reportlab` to generate the PDF. Build the layout programmatically using Platypus (`SimpleDocTemplate`, `Paragraph`, `Spacer`, `Table`, `HRFlowable`).

**CRITICAL CONSTRAINT: Single-page CV with Full Page Utilization**

The CV **MUST fit on exactly one A4 page**. This is non-negotiable for professional CVs — recruiters spend 6 seconds scanning.

**CRITICAL - No Blank Spaces**: The CV must utilize the full page height without leaving blank/empty areas at the bottom. Adjust spacing dynamically:
- If content is sparse, increase spacing between sections, use larger fonts, or add more bullet points
- If content is dense, reduce spacing and fonts proportionally
- The goal is a balanced, professional layout that fills the page naturally without appearing cramped or sparse
- Never leave more than 1 inch (72pt) of blank space at the bottom of the page

**Page setup:**
- A4 page size (595.27 × 841.89 points)
- Margins: 40-50pt all sides (tighter than multi-page to maximize space)

**Layout strategy — choose based on content volume:**

#### Strategy A: Single-column (for lighter profiles)

If the content naturally fits in one page with comfortable spacing:
- Single column, full width (~500pt usable)
- Standard spacing between sections

#### Strategy B: Two-column layout (for content-heavy profiles)

If single-column would overflow, use a **two-column table layout**:

```python
from reportlab.platypus import Table, TableStyle

# Page divided into two columns with a gutter
left_col_width = 235  # points
right_col_width = 235
gutter = 20

# Build left and right content separately
left_content = [header, contact, experience_section]
right_content = [education_section, skills_section, certifications_section, languages_section]

# Create a table with two cells
main_table = Table(
    [[left_flowables, right_flowables]],
    colWidths=[left_col_width, right_col_width],
    spaceBefore=0,
)
main_table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (0, 0), 0),
    ('RIGHTPADDING', (1, 0), (1, 0), 0),
    ('LEFTPADDING', (1, 0), (1, 0), gutter),  # Gutter between columns
]))
```

**Two-column content distribution:**

| Left Column | Right Column |
|---|---|
| Name, Headline, Contact | Skills |
| Experience (most important) | Education |
| | Certifications |
| | Languages |

The left column gets the "story" (who you are, what you've done). The right column gets supporting details.

**Layout reference**: See [references/layout-guide.md](references/layout-guide.md) for detailed spacing, size scales, and construction patterns.

**Section order** (only sections with content — omit any that are empty):
1. **Header** — Name (large display font), headline (if non-empty), location (if non-empty)
2. **Contact** — Email, phone, websites — displayed compactly on one or two lines, separated by a delimiter (e.g. `·` or `|`). Only include fields that have actual values.
3. **About** — Professional summary paragraph (only if about text is non-empty, checking both `Profile.csv` Summary and `Profile Summary.csv`)
4. **Experience** — Reverse chronological, with title/company/dates/description as bullet points (using the pre-written bullet points from Step 2)
5. **Education** — School, degree, **field of study** (REQUIRED), dates. Show summarized focus areas and thesis (using the pre-written summaries from Step 2)
6. **Skills** — Show ALL skills, translated to English, grouped by category (Programming, Data Science, Analytics, AI, Business, etc.)
7. **Certifications** — Name, issuer, date, license number
8. **Languages** — Name with proficiency level
9. **Additional Sections** (from Step 2b) — Any custom sections discovered from non-standard files in the input folder. These appear at the end in this order:
   - Volunteer Experience
   - Projects
   - Publications
   - Honors & Awards
   - Interests/Hobbies (always last — least professional relevance)

### Step 6b: Content Prioritization for Single Page

When content is too dense, apply these rules **in order**:

1. **Reduce font sizes** — Scale everything down proportionally (e.g., name 28→24pt, body 10→9pt)
2. **Tighten spacing** — Reduce spacers between sections (18pt → 12pt)
3. **Limit experience bullets** — Maximum 3-4 bullets for older roles, 4-5 for current role
4. **Show all positions** — Include all work experience (up to 7 positions). Older/shorter roles can omit descriptions but must show title + company + dates
5. **Show all education entries** — Do NOT group degrees by school. Each degree is a separate entry with its own date range and thesis info. Users may have multiple degrees from the same institution.
6. **Show ALL skills** — Display all skills, translated to English, and grouped by category. Use compact formatting (smaller font, tighter spacing) if needed.
7. **Switch to two-column** — If still overflowing, use the two-column table layout

**Never sacrifice**:
- Name visibility
- Current/most recent role details
- Contact information
- Education entries (each degree should be shown)
- Certification names (never truncate)

**Acceptable to minimize**:
- Experience descriptions for old/short positions (title + company + dates only)
- Extensive coursework lists (summarize key areas instead)
- Number of bullet points per role (reduce from 4 to 2-3 for older roles)
- Additional sections (hobbies, interests, volunteer work) — condense to single line each or omit entirely if space is critical
- Projects/Publications — show only top 2-3 most relevant if space is limited

**Additional sections priority** (lowest to highest — cut from top first when space is tight):
1. Interests/Hobbies — cut first, least professional value
2. Volunteer Experience — can be condensed significantly
3. Awards/Honors — keep if notable
4. Projects — keep if technical and relevant to role
5. Publications — keep if demonstrating expertise

### Step 7: Apply Craftsmanship

Before finalizing, refine:

- **Check spacing consistency** — Equal gaps between like elements, larger gaps between sections
- **Verify font sizes form a clear scale** — Name > Section Heading > Job Title > Body > Metadata
- **Ensure single-page fit** — If content overflows, apply prioritization rules from Step 6b, then switch to two-column layout
- **Thin horizontal rules** (0.3-0.5pt) may separate sections — this is the ONLY non-text element allowed
- **Test that all text fits within margins** with no overflow or clipping
- **NEVER exceed one page** — Two-column layout is the fallback, not a second page
- **Color must be functional** — accent color draws the eye to the right things (name, section headers), never distracts

### Step 8: Write and Execute the Script

Combine all the logic from Steps 1-7 into a single Python script. Write it to a **user-specific file** in the workspace: `generate_<name>_cv.py` (e.g., `generate_jane_doe_cv.py`). This ensures each user's script with their hardcoded data is preserved separately. The script should:

1. Parse the CSV files from the input folder (for basic profile info, contact, skills, etc.)
2. **Use the pre-written descriptions from Step 2** — embed the rewritten bullet points directly in the script as dictionaries, NOT parse descriptions with regex
3. **Include additional sections from Step 2b** — embed any custom sections discovered from non-standard files as dictionaries in the script
4. Register fonts from the canvas-fonts directory
5. Build the reportlab Platypus story with all styled elements, including additional sections at the end
6. Output the PDF to the correct path

**CRITICAL**: The Python script should NOT contain any regex-based description parsing. The descriptions were already analyzed and rewritten by the language model in Step 2. Embed those rewritten descriptions directly in the script.

**Output path**: Use the `<name>` from the user prompt directly as the output folder and file slug:

```
output/<name>/cv_<name>.pdf
```

For example, if the user said `for jane_doe`, output to `output/jane_doe/cv_jane_doe.pdf`.

Create the output directory if it doesn't exist.

**Execute the script** using the project's virtual environment:

```bash
uv run python generate_<name>_cv.py
```

For example, if the user is `jane_doe`, run `uv run python generate_jane_doe_cv.py`.

If the script fails, read the error output, fix the script, and re-run. Common issues:
- Missing font files — verify paths in `~/.cursor/skills/canvas-design/canvas-fonts/`
- CSV encoding issues — try `utf-8-sig` if `utf-8` fails
- Missing CSV columns — ensure field name matching is case-insensitive and handles variants

After successful execution, report the output file path to the user along with a summary of what sections were included.

## Essential Constraints

- **Single page only** — The CV MUST fit on exactly one A4 page. Use two-column layout and content prioritization to achieve this. Never generate a multi-page CV.
- **100% text** — No images, icons, logos, decorative shapes, or background fills. Only text and thin horizontal rules.
- **Fonts only from canvas-fonts** — Never use built-in PDF fonts. Always register and use TTF files from `~/.cursor/skills/canvas-design/canvas-fonts/`.
- **White/off-white background** — Page background is always clean. Design lives in the typography.
- **Professional readability** — Despite creative theming, the CV must be scannable by a recruiter in 6 seconds. Information hierarchy is paramount.
- **LLM-preprocessed descriptions (CRITICAL)** — The language model MUST read and rewrite all experience and education descriptions BEFORE generating Python code. Never use regex-based parsing to split descriptions into bullet points. The Python script should contain pre-written, well-structured bullet points as hardcoded data.
- **Expert craftsmanship** — The result must look like it took hours to design. Meticulous spacing. Precise alignment. Painstaking attention to every typographic detail.
- **Never fabricate data** — If a CSV file is missing or a field is blank, skip it. Never invent content. When rewriting descriptions, preserve the original meaning and facts.
- **Always use `uv run`** — Execute all Python code through `uv run python` to use the project's virtual environment. Never use bare `python` or `python3`.

## Additional Resources

- For curated font pairings, see [references/font-pairings.md](references/font-pairings.md)
- For detailed layout specifications, see [references/layout-guide.md](references/layout-guide.md)
