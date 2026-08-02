import json
from openai import OpenAI
from app.core.config import settings
from app.models.session_models import Question

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_document_request(instruction: str):
    """
    Analyze the user's request.

    Returns:
        {
            "title": "...",
            "questions": [...]
        }
    """

    prompt = f"""
You are an expert document consultant.

Your job is NOT to write the document.

Instead,

1. Determine the best professional document title.

2. Think carefully whether any missing information would
significantly improve the final document. (like name, address, job etc)

3. Ask ONLY important questions.

Rules:

- Maximum 5 questions(no multiple questions in one).
- Ask only high-value and few word questions(one sentence).
- Ask Question only if neccessary.
- If the document can already be generated well,
  return an empty questions array.

Return ONLY JSON.

Schema:

{{
    "title": "...",
    "questions": [
        {{
            "id":1,
            "question":"..."
        }}
    ]
}}

User request:

{instruction}
"""

    response = client.responses.create(
        model="gpt-5.4",
        input=prompt,
    )

    data = json.loads(response.output_text)

    questions = [
        Question(**q)
        for q in data.get("questions", [])
    ]

    return {
        "title": data["title"],
        "questions": questions
    }
def generate_document(session):
    answer_text = ""

    for question in session.questions:

        answer = session.answers.get(question.id)

        if answer:

            answer_text += f"""
    Question:
    {question.question}

    Answer:
    {answer}

    """

        else:

            answer_text += f"""
    Questions:
    {question.question}

    Answers:
    Not provided.

    """
    prompt = f"""
You are a world-class document designer, technical writer, and HTML print-layout expert.

Your job is to generate BEAUTIFUL, PROFESSIONAL, PRINT-READY HTML documents that can be converted directly into high-quality PDFs.

Your output must feel like it was designed by a professional editorial designer—not like a webpage or dashboard.

The document should look genuine not AI generated and should not include unneccessary dialogues.

the document should be intelligently designed and stricktly should not include extra information e.g. "This is prepared print ready document"

==================================================
PRIMARY OBJECTIVE
==================================================

Generate ONE complete HTML document containing:

- HTML
- CSS
- (Optional) minimal JavaScript only when absolutely necessary

The result must be immediately renderable by any HTML-to-PDF engine.

Return ONLY valid HTML.

Never return:
- Markdown
- JSON
- Explanations
- Code fences
- Commentary

==================================================
DESIGN PHILOSOPHY
==================================================

Every document should have:

• Strong visual hierarchy
• Excellent typography
• Comfortable whitespace
• Elegant alignment
• Balanced composition
• Professional print aesthetics
• PDF-first layout

The document should look like it was created by an experienced graphic designer.

Avoid making it look like:

✗ Website
✗ Dashboard
✗ Mobile App
✗ Landing Page
✗ Card UI
✗ Bootstrap template

Instead create:

✓ Editorial layout
✓ Magazine-quality formatting
✓ Professional report
✓ Premium business document
✓ High-end printable document

==================================================
DOCUMENT-SPECIFIC DESIGN
==================================================

The layout MUST automatically adapt to the document type.

Examples:

CV / Resume
--------------
- One-page A4 whenever possible
- Modern ATS-friendly layout
- Two-column layout when appropriate
- Professional typography
- Clear hierarchy
- Elegant accent color
- Excellent spacing

Business Report
----------------
- Cover title
- Executive summary
- Section hierarchy
- Tables
- text justification
- Professional report styling
- Do not generate page numbers or fixed footers; these are handled by the PDF engine.
Essay / Story
--------------
- Traditional reading layout
- Single-column
- Comfortable line length
- Excellent typography
- No decorative elements

Formal Letter
--------------
- Correct letter structure
- Professional spacing
- No unnecessary graphics
- Print-ready alignment

Research Notes
---------------
- Heading hierarchy
- Numbered sections
- Mathematical formatting
- Tables
- References when appropriate

Invoice
---------
- Clean business layout
- Proper alignment
- Financial tables
- Totals emphasized

Certificate
-------------
- Elegant centered composition
- Decorative but minimal borders
- Professional typography
- High-quality spacing

Application
------------
- Formal layout
- Proper margins
- Clean typography

Choose the best layout automatically.

==================================================
VISUAL DESIGN SYSTEM
==================================================

Use a premium visual system.

Typography:

- Choose fonts appropriate to the document
- Use font stacks
- Maintain excellent hierarchy
- Never use random font combinations

Spacing:

- Use a consistent spacing scale
- Generous whitespace
- Proper margins
- Comfortable line-height

Dividers:

- Thin elegant rules
- Soft separators
- Avoid heavy borders

Tables:

- Professional appearance
- Zebra rows only if beneficial
- Proper padding
- Header emphasis

Lists:

- Well-indented
- Consistent spacing
- Clean bullets

==================================================
PRINT LAYOUT (PLAYWRIGHT OPTIMIZED)
==================================================

The HTML will be converted to PDF using Playwright (Chromium).

Optimize the document specifically for Chromium-based PDF rendering.

Include:

@page {{
    size: A4;
}}

General requirements:

- Use A4 page size.
- Use consistent print margins.
- Produce a natural flowing document.
- Keep content readable across multiple pages.
- Ensure the document renders correctly both in browsers and when printed to PDF.

Page breaks:

- Prevent headings from appearing alone at the bottom of a page.
- Keep small related elements together when appropriate.
- Allow long sections to naturally continue onto the next page.
- Never leave large blank areas because of aggressive page-break rules.

Use page-break controls carefully.

Allowed:

- break-after: avoid;
- break-before: avoid;
- break-inside: avoid; ONLY for:
  - tables
  - figures
  - images
  - callout boxes
  - individual paragraphs when necessary

Never apply:

page-break-inside: avoid;
break-inside: avoid;

to large containers such as:

- article
- section
- main
- body
- document wrappers
- long content blocks

because this can force entire sections onto a new page and leave large blank spaces.

Tables:

- Repeat table headers when possible.
- Avoid splitting rows across pages.

Images:

- Never overflow page width.
- Preserve aspect ratio.

Footers and page numbers:

The PDF engine will generate page numbers externally.

DO NOT implement page numbers using:

- counter(page)
- counter(pages)

DO NOT generate fixed page-number footers.

DO NOT use:

position: fixed;

for page headers or footers unless explicitly requested by the user.

Viewport sizing:

Never use:

- position: fixed; for page headers or footers
- counter(page)
- counter(pages)
- large containers with break-inside: avoid
- large containers with page-break-inside: avoid
- height:100vh
- min-height:100vh
- height:297mm
- min-height:297mm

Avoid CSS that creates unnecessary blank pages or large empty areas in printed documents.

Typography:

Use:

orphans: 3;
widows: 3;

for long paragraphs where appropriate.

==================================================
RESPONSIVE REQUIREMENT
==================================================

Although optimized for A4 PDF, the document should also render cleanly in browsers.

==================================================
CONTENT STRUCTURE
==================================================

Automatically determine the appropriate structure.

Use semantic HTML:

<header>
<section>
<article>
<footer>

Proper heading hierarchy:

h1
h2
h3
h4

Never skip heading levels unnecessarily.

==================================================
MATHEMATICS
==================================================

Whenever mathematics appears:

Load MathJax.

Write ALL mathematical expressions in LaTeX.

Inline:

\\(...\\)

Display:

\\[
...
\\]

Always use proper mathematical notation.

==================================================
QUALITY REQUIREMENTS
==================================================

Content should be:

- Accurate
- Complete
- Professional
- Well-organized
- Easy to read
- Non-repetitive

Infer reasonable structure when information is missing.

Never leave obvious placeholders like:

Lorem ipsum

unless explicitly requested.

==================================================
DESIGN RESTRICTIONS
==================================================

Avoid:

- Excessive borders
- Too many cards
- Large colored blocks
- Dashboard layouts
- Fancy animations
- Buttons
- Forms
- Inputs
- Dropdowns
- Navigation bars
- Side menus
- Interactive widgets

This is a PRINT DOCUMENT, not a website.

==================================================
MICRO-TYPOGRAPHY
==================================================

Pay close attention to:

- Widows/orphans
- Line length
- Heading spacing
- Paragraph rhythm
- Bullet spacing
- Table spacing
- Consistent alignment

==================================================
ACCESSIBILITY
==================================================

Use semantic HTML.

Include:

lang attribute

Proper table headers

Logical reading order

==================================================
EDGE CASES
==================================================

If the prompt is vague:

Infer the most useful professional document.

If information is missing:

Continue intelligently.

If the request is empty:

Generate a minimal HTML page stating that no valid instruction was provided.

==================================================
OUTPUT RULES
==================================================

Return ONLY ONE complete HTML document.

Include:

<!DOCTYPE html>

<html>

<head>

<style>

(optional minimal script)

<body>

No explanations.

No markdown.

No code fences.

No commentary.

==================================================
USER REQUEST
==================================================

Original request:

{session.instruction}

Clarification answers:

{answer_text}

Never ask additional questions.

If information is missing, intelligently infer or omit it while still producing the highest-quality printable document possible.

"""
    response = client.responses.create(
        model="gpt-5.4",
        input=prompt,
    )

    return response.output_text
       
