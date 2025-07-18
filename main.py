import requests
from bs4 import BeautifulSoup

def scrape(url, max_length):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for a_tag in soup.find_all('a', href=True):
            links.append(a_tag['href'])
        links = [link for link in links if len(link) > 3]
        
        cleaned_content = soup.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )
        cleaned_content_list = [cleaned_content[i : i + max_length] for i in range(0, len(cleaned_content), max_length)]
        return cleaned_content_list, links
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping URL: {e}")
        return None




if __name__ == "__main__":

    url = input("Enter a URL: ")
    data = scrape(url,6000)

