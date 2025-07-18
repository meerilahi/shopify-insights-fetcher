import requests
from bs4 import BeautifulSoup

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

def clean_html(html, max_length):
    soup = BeautifulSoup(html, "html.parser")
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    cleaned_content_list = [cleaned_content[i : i + max_length] for i in range(0, len(cleaned_content), max_length)]
    return cleaned_content_list





if __name__ == "__main__":

    # url = input("Enter a URL: ")
    html = get_html("https://fanjoy.co/collections/take-care-of-yourself")
    print(len(html))

    links = extract_links_from_html(html)
    print(len(links))

    texts = clean_html(html, 6000)
    print(len(texts)) 


