from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from bs4 import BeautifulSoup
import urllib.parse





def flipkartSearch(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.flipkart.com/search?q={encoded_query}"
    print(url)
    return url

def amazonSearch(query):
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.amazon.in/s?k={encoded_query}"
    return url

def scrape_website(website):
    options = FirefoxOptions()
    options.add_argument("--headless")

    with Firefox(options=options, service=FirefoxService()) as driver:
        driver.get(website)

        driver.implicitly_wait(10)

        # Get the entire page source
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
