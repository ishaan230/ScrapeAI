from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from bs4 import BeautifulSoup
import os

def scrape_website(website):
    print("Connecting to Firefox...")
    options = FirefoxOptions()
    # Optionally, set other options for Firefox, e.g., headless mode
    # options.add_argument("--headless")

    # Initialize the Firefox WebDriver
    with Firefox(options=options, service=FirefoxService()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        # You may need to handle captchas manually or use other approaches as needed
        # The following is a placeholder and may not work if no captcha is handled via JavaScript
        solve_res = driver.execute_script(
            "return window.Captcha && window.Captcha.waitForSolve({detectTimeout: 10000});"
        )
        print("Captcha solve status:", solve_res)
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html


def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
