# LinkedIn to CV

Turn your LinkedIn data export into a beautifully typeset PDF curriculum vitae — entirely through a single Cursor agent skill.

## How It Works

One agent skill handles everything:

1. You download your profile data from LinkedIn (CSV export)
2. Place the unzipped folder in `input/<your_name>/`
3. Ask the agent to generate a CV with a theme
4. The agent reads the CSVs and produces a typographic PDF

## Setup

```bash
uv sync
```

### Font Prerequisite

The CV skill uses fonts from the **canvas-design** skill:

1. Get the `canvas-design` skill from [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/canvas-design)
2. Place it at `~/.cursor/skills/canvas-design/`

## Usage

### Step 1: Download your LinkedIn data

1. Go to **LinkedIn.com** → profile photo → **Settings & Privacy**
2. Navigate to **Data privacy** → **Get a copy of your data**
3. Request the full archive
4. Download the ZIP when LinkedIn emails the link (usually within minutes)
5. Unzip and place the folder at `input/<your_name>/` in this project

### Step 2: Generate the CV

In Cursor, prompt:

```
Generate a CV from LinkedIn data for <your_name> with a <theme description> theme
```

This produces `output/<your_name>/cv_<your_name>.pdf`.

## Theme Examples

| Prompt | Result |
|--------|--------|
| `"minimal swiss"` | Clean grotesque typography, grid precision, monospace accents |
| `"editorial elegance"` | Serif-forward, book-like layout, literary refinement |
| `"bold startup vibe"` | Geometric sans-serif, strong presence, modern energy |
| `"quiet sophistication"` | Thin display type, sturdy serif body, whispered elegance |
| `"technical precision"` | Monospace-forward, engineering-minded, systematic |
| `"minimal white blue modern"` | My favorite <3 |

## Output

```
output/
  your_name/
    cv_your_name.pdf      # Generated CV
```
