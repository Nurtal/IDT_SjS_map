"""
Convert docs/manuscript.md → docs/manuscript.pdf via weasyprint.
"""
import pathlib
import re
import markdown
from weasyprint import HTML, CSS

SRC  = pathlib.Path("docs/manuscript.md")
OUT  = pathlib.Path("docs/manuscript.pdf")

CSS_STYLE = """
@page {
    size: A4;
    margin: 2.5cm 2.8cm 2.5cm 2.8cm;
    @bottom-center {
        content: counter(page);
        font-size: 9pt;
        color: #666;
    }
}

body {
    font-family: "Linux Libertine O", "Libertinus Serif", Georgia, "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #111;
    text-align: justify;
    hyphens: auto;
}

h1 {
    font-size: 16pt;
    font-weight: bold;
    text-align: center;
    margin-top: 0;
    margin-bottom: 0.4em;
    line-height: 1.3;
    color: #1a1a2e;
}

h2 {
    font-size: 12pt;
    font-weight: bold;
    margin-top: 1.4em;
    margin-bottom: 0.3em;
    color: #1a1a2e;
    border-bottom: 1px solid #ccc;
    padding-bottom: 2px;
    page-break-after: avoid;
}

h3 {
    font-size: 11pt;
    font-weight: bold;
    font-style: italic;
    margin-top: 1em;
    margin-bottom: 0.2em;
    color: #222;
    page-break-after: avoid;
}

/* Authors / affiliation block (first ¶ after h1) */
.author-block {
    text-align: center;
    font-size: 10.5pt;
    color: #333;
    margin-bottom: 0.2em;
}

/* Abstract box */
.abstract-box {
    border: 1px solid #bbb;
    background: #f8f8f8;
    padding: 0.7em 1em;
    margin: 1em 0;
    font-size: 10pt;
}

.abstract-box p { margin: 0.3em 0; }

p {
    margin: 0.5em 0;
    text-indent: 0;
}

/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    font-size: 9.5pt;
    margin: 0.8em 0;
    page-break-inside: avoid;
}

th {
    background: #2c3e50;
    color: white;
    padding: 5px 8px;
    text-align: left;
    font-weight: bold;
}

td {
    border: 1px solid #ccc;
    padding: 4px 8px;
    vertical-align: top;
}

tr:nth-child(even) td { background: #f5f5f5; }

/* Code blocks (used for pathway diagram) */
pre {
    background: #f4f4f4;
    border-left: 3px solid #2c3e50;
    padding: 0.5em 0.8em;
    font-size: 8.5pt;
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
    overflow-x: auto;
    page-break-inside: avoid;
    white-space: pre-wrap;
}

code {
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 9pt;
    background: #f0f0f0;
    padding: 1px 3px;
    border-radius: 2px;
}

/* Horizontal rule — section separator */
hr {
    border: none;
    border-top: 1px solid #ccc;
    margin: 1.2em 0;
}

/* Bold / italic */
strong { color: #1a1a2e; }

/* Keywords line */
em { color: #333; }

/* Lists */
ul, ol {
    margin: 0.4em 0 0.4em 1.5em;
    padding: 0;
}
li { margin: 0.2em 0; }

/* Avoid page break inside key sections */
h2 + p, h3 + p { page-break-before: avoid; }

/* Reference section smaller */
h2#references + ul, h2:last-of-type + ul {
    font-size: 9.5pt;
    line-height: 1.4;
}
"""


def md_to_pdf(src: pathlib.Path, out: pathlib.Path) -> None:
    text = src.read_text(encoding="utf-8")

    # Detect author line (italic paragraph just after h1 before abstract)
    # Wrap Abstract section in a styled div
    text = re.sub(
        r"(## Abstract\n)(.*?)(\n## )",
        lambda m: m.group(1) + '<div class="abstract-box">\n\n'
                  + m.group(2).strip() + '\n\n</div>\n\n' + m.group(3),
        text, flags=re.DOTALL
    )

    html_body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "attr_list"],
    )

    # Wrap metadata block (first 3 paras: title, author, affiliation)
    html_full = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<title>SjD-BoolAttractors Manuscript</title>
</head>
<body>
{html_body}
</body>
</html>"""

    out.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_full, base_url=str(src.parent)).write_pdf(
        str(out),
        stylesheets=[CSS(string=CSS_STYLE)],
        uncompressed_pdf=False,
    )
    print(f"PDF written: {out}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    md_to_pdf(SRC, OUT)
