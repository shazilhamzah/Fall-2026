import os
import re
import base64
import subprocess
import markdown

base_dir = os.path.dirname(os.path.abspath(__file__))
md_path = os.path.join(base_dir, "REPORT.md")
html_path = os.path.join(base_dir, "report.html")
pdf_path = os.path.join(base_dir, "REPORT.pdf")

with open(md_path, "r", encoding="utf-8") as f:
    md_content = f.read()

def fix_all_images(html):
    pattern = re.compile(r'<img\s+([^>]*?)src="([^"]+)"([^>]*?)>', re.IGNORECASE)
    def repl(m):
        src = m.group(2)
        clean_src = src.lstrip("./").replace("/", os.sep)
        abs_path = os.path.normpath(os.path.join(base_dir, clean_src))
        if not os.path.exists(abs_path):
            alt_src = clean_src.replace("Challenge_", "Challenge ")
            abs_path = os.path.normpath(os.path.join(base_dir, alt_src))
        if os.path.exists(abs_path):
            with open(abs_path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode("ascii")
            ext = os.path.splitext(abs_path)[1].lstrip(".").lower()
            mime = "image/png" if ext == "png" else f"image/{ext}"
            return f'<div class="img-box"><img {m.group(1)}src="data:{mime};base64,{encoded}"{m.group(3)}></div>'
        print(f"Warning: Image not found at {abs_path}")
        return m.group(0)
    return pattern.sub(repl, html)

raw_html = markdown.markdown(md_content, extensions=["fenced_code", "tables"])
html_body = fix_all_images(raw_html)

css = """
@page {
    size: A4;
    margin: 15mm 15mm 15mm 15mm;
}
@media print {
    body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    h2, h3 {
        page-break-after: avoid;
        break-after: avoid;
    }
    .img-box {
        page-break-inside: avoid;
        break-inside: avoid;
    }
    pre {
        page-break-inside: avoid;
        break-inside: avoid;
    }
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1a1f2c;
    line-height: 1.6;
    font-size: 13px;
    max-width: 850px;
    margin: 0 auto;
    padding: 0;
}
h1 {
    font-size: 22px;
    margin-top: 0;
    margin-bottom: 6px;
    color: #0b57d0;
    border-bottom: 2px solid #e1e4e8;
    padding-bottom: 6px;
}
h2 {
    font-size: 17px;
    margin-top: 20px;
    margin-bottom: 8px;
    color: #24292f;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 4px;
}
h3 {
    font-size: 15px;
    margin-top: 22px;
    margin-bottom: 8px;
    background: #f1f4f9;
    padding: 8px 12px;
    border-left: 4px solid #0b57d0;
    border-radius: 4px;
}
h4 {
    font-size: 13.5px;
    margin-top: 14px;
    margin-bottom: 4px;
    color: #333;
}
hr {
    border: none;
    border-top: 1px solid #e1e4e8;
    margin: 20px 0;
}
p, ul, ol {
    margin-top: 4px;
    margin-bottom: 8px;
}
code {
    background-color: #f6f8fa;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "Cascadia Code", Consolas, "Courier New", monospace;
    font-size: 12px;
    color: #b31d28;
    border: 1px solid #eaecef;
}
pre {
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 10px 14px;
    overflow-x: auto;
    font-family: "Cascadia Code", Consolas, "Courier New", monospace;
    font-size: 11.5px;
    line-height: 1.45;
}
pre code {
    background-color: transparent;
    padding: 0;
    border: none;
    color: inherit;
}
blockquote {
    margin: 8px 0;
    padding: 6px 14px;
    border-left: 4px solid #0b57d0;
    background: #f0f7ff;
    color: #444;
    font-style: italic;
}
.img-box {
    margin: 10px 0;
    text-align: center;
}
img {
    max-width: 95%;
    max-height: 360px;
    height: auto;
    display: inline-block;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
"""

template = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>CS3002 - Information Security Assignment #01</title>
<style>
{css}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(template)

print("Generated report.html successfully.")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_path):
    chrome_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]

print(f"Running: {' '.join(cmd)}")
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"Browser exited with code {res.returncode}")

if os.path.exists(pdf_path):
    print(f"SUCCESS: Generated {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
else:
    print("FAILED to generate PDF")

