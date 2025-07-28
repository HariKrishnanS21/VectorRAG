import requests
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

visited_urls = set()

def is_valid_url(url, base_domain):
    parsed = urlparse(url)
    return base_domain in parsed.netloc and url not in visited_urls and url.startswith("http")

def extract_text_from_url(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, timeout=60000)  
            except Exception as e:
                print(f"Page load error: {e}")
                return ""
            page.wait_for_timeout(5000)     
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=' ', strip=True)
        return text

    except Exception as e:
        print(f"Playwright error fetching {url}: {e}")
        return ""
   
    #try:
     #   response = requests.get(url, timeout=10)
     #   soup = BeautifulSoup(response.text, "html.parser")

        # Remove navbars, scripts, styles
     #   for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
     #       tag.decompose()

      #  text = soup.get_text(separator=' ', strip=True)
    #    return text
    #except Exception as e:
    #    print(f"Error fetching {url}: {e}")
     #   return ""

def crawl_website(start_url, max_pages=30):
    base_domain = urlparse(start_url).netloc
    to_visit = [start_url]
    all_text = []

    print(f"Scraping: {start_url}")
    while to_visit and len(visited_urls) < max_pages:
        url = to_visit.pop(0)
        if not is_valid_url(url, base_domain):
            continue

        visited_urls.add(url)
        text = extract_text_from_url(url)
        if text:
            all_text.append(text)

        try:
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
            for link in soup.find_all("a", href=True):
                new_url = urljoin(url, link['href'])
                if is_valid_url(new_url, base_domain):
                    to_visit.append(new_url)
        except:
            continue

    return all_text

#changi_data = crawl_website("https://www.changiairport.com/in/en.html", max_pages=25)
jewel_data = crawl_website("https://www.jewelchangiairport.com/", max_pages=25)

#with open("changi_cleaned.txt", "w", encoding="utf-8") as f:
    #f.write("\n\n".join(changi_data))

with open("jewel_cleaned.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(jewel_data))