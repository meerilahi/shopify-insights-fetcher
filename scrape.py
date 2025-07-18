import requests
from bs4 import BeautifulSoup
from extract_products import extract_products

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error scraping URL: {e}")
        return None

def extract_links_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a_tag in soup.find_all('a', href=True):
        links.append(a_tag['href'])
    links = [link for link in links if len(link) > 3]
    return links

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

def split_text(text, max_length):
    return [text[i : i + max_length] for i in range(0, len(text), max_length)]