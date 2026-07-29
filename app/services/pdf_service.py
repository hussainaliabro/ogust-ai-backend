import os
from playwright.async_api import async_playwright
import subprocess
import re

async def create_pdf(title, content):
    title = re.sub(r'[^a-zA-Z0-9_-]', '_', title)
    output_dir = "app/generated/pdfs"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{output_dir}/{title}.pdf"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page()

        await page.set_content(content, wait_until="networkidle")
        await page.wait_for_timeout(2000)  # IMPORTANT

        await page.pdf(
            path=filename,
            format="A4",
            print_background=True
        )

        await browser.close()

    return filename

def save_html(title, html):
    output_dir = "app/generated/pdfs"
    os.makedirs(output_dir, exist_ok=True)

    html_path = f"{output_dir}/{title}.html"

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    return html_path

def save_docx(title, html):
    output_dir = "app/generated/pdfs"
    os.makedirs(output_dir, exist_ok=True)

    html_path = os.path.join(output_dir, f"{title}.html")
    docx_path = os.path.join(output_dir, f"{title}.docx")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    subprocess.run(
        [
            "pandoc",
            html_path,
            "-o",
            docx_path,
            "--standalone",
        ],
        check=True,
    )

    return docx_path