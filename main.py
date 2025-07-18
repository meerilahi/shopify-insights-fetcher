from scrape import get_html, extract_links_from_html, clean_html
from extract_products import extract_products
from categorize_links import categorize_links
import json

# url = input("Enter a URL: ")
html = get_html("https://fanjoy.co/collections/take-care-of-yourself")
print(len(html))

links = extract_links_from_html(html)
print(len(links))

texts = clean_html(html, 6000)
print(len(texts))

# heor_products = extract_products(texts)
# print(heor_products)

cat_links = categorize_links(links)
print(cat_links)

all_products = []
for link in cat_links['products'][:3]:
    if link[0] != "h":
        url = "https://fanjoy.co" + link
    html = get_html(url)
    texts = clean_html(html, 6000)
    products = extract_products(texts)
    all_products.extend(products)

while open("temp.json","+w"):
    json.dumps(all_products)
    