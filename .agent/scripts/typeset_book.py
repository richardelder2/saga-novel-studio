import os
import glob
import re

def make_drop_cap(text):
    # Wraps the first actual visible letter in a drop-cap span, bypassing leading HTML tags.
    in_tag = False
    for i, char in enumerate(text):
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
        elif not in_tag and char.isalnum():
            return f"{text[:i]}<span class='drop-cap'>{char}</span>{text[i+1:]}"
    return text

def markdown_to_basic_html(text):
    # Simple markdown block parsers (since we don't assume external dependencies like markdown package)
    lines = text.split("\n")
    html_lines = []
    in_paragraph = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            continue
            
        # Headers
        if line.startswith("# "):
            if in_paragraph: html_lines.append("</p>"); in_paragraph = False
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            if in_paragraph: html_lines.append("</p>"); in_paragraph = False
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            if in_paragraph: html_lines.append("</p>"); in_paragraph = False
            html_lines.append(f"<h3>{line[4:]}</h3>")
        # Horizontal Rule
        elif line == "***" or line == "---":
            if in_paragraph: html_lines.append("</p>"); in_paragraph = False
            html_lines.append("<div class='section-break'>✦ ✦ ✦</div>")
        # Paragraphs
        else:
            # Inline formatting: Bold, Italic
            line = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
            line = re.sub(r"\*(.*?)\*", r"<em>\1</em>", line)
            
            if not in_paragraph:
                # Check for drop-cap on first paragraph of a chapter
                if len(html_lines) > 0 and (html_lines[-1].startswith("<h1>") or html_lines[-1].startswith("<h2>")):
                    html_lines.append(f"<p class='first-para'>{make_drop_cap(line)}")
                else:
                    html_lines.append(f"<p>{line}")
                in_paragraph = True
            else:
                html_lines.append(" " + line)
                
    if in_paragraph:
        html_lines.append("</p>")
        
    return "\n".join(html_lines)

def typeset_book():
    draft_dir = "02_Drafting"
    output_file = "04_Publishing/typeset_manuscript.html"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    chapter_files = sorted(glob.glob(os.path.join(draft_dir, "chapter_*.md")))
    if not chapter_files:
        print("No chapter files found in 02_Drafting/.")
        return
        
    book_content_html = []
    
    for filename in chapter_files:
        with open(filename, "r", encoding="utf-8") as infile:
            text = infile.read()
            html_text = markdown_to_basic_html(text)
            book_content_html.append(f"<section class='chapter-page'>\n{html_text}\n</section>")
            
    # Gorgeous print stylesheet
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Manuscript Export</title>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Outfit:wght@400;600&family=Inter:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: 6in 9in;
      margin: 1in 0.8in 1in 0.8in;
    }}
    
    @media print {{
      body {{
        background: #fff;
        color: #000;
      }}
      .chapter-page {{
        page-break-after: always;
      }}
    }}
    
    body {{
      font-family: 'Inter', Georgia, serif;
      line-height: 1.6;
      font-size: 11.5pt;
      color: #111;
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
      background: #fbfbfc;
      box-shadow: 0 0 20px rgba(0,0,0,0.05);
      border-radius: 8px;
    }}
    
    .title-page {{
      text-align: center;
      padding-top: 150px;
      height: 600px;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }}
    
    .title-page h1 {{
      font-family: 'Cinzel', serif;
      font-size: 3rem;
      margin-bottom: 20px;
      letter-spacing: 0.05em;
    }}
    
    .title-page h2 {{
      font-family: 'Outfit', sans-serif;
      font-weight: 400;
      font-size: 1.5rem;
      color: #555;
      margin-bottom: 80px;
    }}
    
    .title-ornament {{
      font-size: 2rem;
      color: #888;
      margin-bottom: 40px;
    }}
    
    .chapter-page {{
      padding-top: 50px;
      margin-bottom: 80px;
      page-break-after: always;
    }}
    
    h1, h2, h3 {{
      font-family: 'Cinzel', serif;
      text-align: center;
      margin-bottom: 40px;
      font-weight: 600;
    }}
    
    h1 {{
      font-size: 2rem;
      border-bottom: none;
      padding-bottom: 0;
      margin-top: 50px;
    }}
    
    p {{
      text-indent: 1.5em;
      margin: 0 0 10px 0;
      text-align: justify;
    }}
    
    p.first-para {{
      text-indent: 0;
    }}
    
    .drop-cap {{
      font-family: 'Cinzel', serif;
      float: left;
      font-size: 3.5rem;
      line-height: 0.8;
      margin: 4px 8px 0 0;
      font-weight: 700;
      color: #111;
    }}
    
    .section-break {{
      text-align: center;
      font-size: 1.5rem;
      margin: 40px 0;
      letter-spacing: 0.5em;
      color: #666;
    }}
  </style>
</head>
<body>

  <div class="title-page">
    <div class="title-ornament">✧ ✦ ✧</div>
    <h1>The Manuscript</h1>
    <h2>Compiled & Typeset via CAMP</h2>
    <div class="section-break">✦ ✦ ✦</div>
  </div>

  {"\n\n".join(book_content_html)}

</body>
</html>
"""
    
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(html_template)
        
    print(f"Successfully generated print-typeset HTML book at {output_file}")

if __name__ == "__main__":
    typeset_book()
