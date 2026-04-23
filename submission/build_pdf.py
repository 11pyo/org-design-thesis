"""
Convert manuscript.md + report.md into PDFs.

Strategy:
  1. Try wkhtmltopdf / chromium-headless on Windows (most reliable for
     complex markdown with figures).
  2. Fallback: write a self-contained HTML that can be opened in a browser
     and "Save as PDF" via the browser's print dialog.

Run: python build_pdf.py
"""
from __future__ import annotations
import os, sys, shutil, subprocess
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parent.parent
MANUSCRIPT = ROOT / "paper" / "manuscript.md"
REPORT = ROOT / "results" / "report.md"
SUB = ROOT / "submission"

CSS = """
<style>
  body { font-family: Georgia, 'Noto Serif CJK KR', serif;
         max-width: 760px; margin: 2em auto; line-height: 1.55; color: #222;
         font-size: 11pt; }
  h1 { font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 0.2em; }
  h2 { font-size: 14pt; color: #333; border-bottom: 1px solid #ccc; padding-bottom: 0.15em; }
  h3 { font-size: 12pt; color: #555; }
  code { background: #f4f4f4; padding: 1px 4px; border-radius: 3px; font-size: 10pt; }
  pre { background: #f4f4f4; padding: 0.8em; border-radius: 6px;
        overflow-x: auto; font-size: 10pt; }
  table { border-collapse: collapse; margin: 1em 0; font-size: 10pt; }
  th, td { border: 1px solid #ccc; padding: 4px 10px; }
  th { background: #eee; }
  blockquote { border-left: 3px solid #888; padding-left: 1em; color: #555; }
  img { max-width: 100%; height: auto; }
  hr { border: none; border-top: 1px solid #ccc; margin: 2em 0; }
  .math { font-family: 'Cambria Math', 'STIX', serif; }
  @page { size: A4; margin: 2cm; }
</style>
"""


def md_to_html(md_path: Path) -> str:
    md_text = md_path.read_text(encoding="utf-8")
    body = markdown.markdown(md_text, extensions=[
        "tables", "fenced_code", "toc", "nl2br"])
    return f"<!doctype html><html><head><meta charset='utf-8'>{CSS}</head><body>{body}</body></html>"


def save_html(md_path: Path, out_html: Path) -> Path:
    html = md_to_html(md_path)
    html = html.replace('src="figures/', f'src="file:///{ROOT / "results" / "figures"}/'.replace("\\","/"))
    out_html.write_text(html, encoding="utf-8")
    return out_html


def try_browser_print_to_pdf(html_path: Path, pdf_path: Path) -> bool:
    for exe_candidate in [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]:
        if os.path.exists(exe_candidate):
            cmd = [
                exe_candidate, "--headless=new", "--disable-gpu",
                f"--print-to-pdf={pdf_path}",
                f"file:///{html_path.as_posix()}",
            ]
            try:
                r = subprocess.run(cmd, capture_output=True, timeout=60)
                if r.returncode == 0 and pdf_path.exists() and pdf_path.stat().st_size > 2000:
                    return True
            except Exception as e:
                print(f"  {exe_candidate} failed: {e}")
    return False


def main():
    SUB.mkdir(parents=True, exist_ok=True)

    manus_html = SUB / "manuscript.html"
    manus_pdf = SUB / "manuscript.pdf"
    save_html(MANUSCRIPT, manus_html)
    print(f"Wrote {manus_html}")
    if try_browser_print_to_pdf(manus_html, manus_pdf):
        print(f"Wrote {manus_pdf} via headless browser")
    else:
        print(f"PDF fallback: open {manus_html} in Chrome/Edge and Ctrl+P → Save as PDF")

    report_html = SUB / "report.html"
    report_pdf = SUB / "report.pdf"
    save_html(REPORT, report_html)
    print(f"Wrote {report_html}")
    if try_browser_print_to_pdf(report_html, report_pdf):
        print(f"Wrote {report_pdf} via headless browser")
    else:
        print(f"PDF fallback: open {report_html} in Chrome/Edge and Ctrl+P → Save as PDF")


if __name__ == "__main__":
    main()
