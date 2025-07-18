from urllib.parse import urlparse
from extract_policy import extract_policy
from scrape import get_html, extract_links_from_html, clean_html, split_text
from extract_products import extract_products
from categorize_links import categorize_links
from extract_faqs import extract_faqs
from extract_email_and_phone import extract_email_and_phone
from extract_brand_description import extract_brand_description
from schemas import BrandData

# get home page text and link
url = "https://fanjoy.co/collections/take-care-of-yourself"
parsed_url = urlparse(url)
home_html = get_html(parsed_url)
home_text = clean_html(home_html)
links = extract_links_from_html(home_html)

# categorize links
categorized_links = categorize_links(links)

# extract heor products
hero_products = extract_products(split_text(home_html))

# extract all products
all_products = []
for link in categorized_links['products']:
    try:
        if link[0] != "h":
            link = parsed_url.netloc + link
        html = get_html(link)
        all_products.extend(extract_products(split_text(html)))
    except:
        continue

# extract policy
policy_text = "" 
for link in categorized_links['policy']:
    try:
        if link[0] != "h":
            link = parsed_url.netloc + link
        html = get_html(link)
        policy_text + clean_html(html)
    except:
        continue
policy = extract_policy(policy_text)

# extract FAQs
if categorized_links['faq'] is not None:
    if categorized_links['faq'][0] != "h":
        link = parsed_url.netloc + categorized_links['faq']
    html = get_html(link)
    faq_text = clean_html(html)
    faq = extract_faqs(faq_text)
else:
    faq = extract_faqs(home_text)

# extract emails and phone numbers
if categorized_links['contact'] is not None:
    if categorized_links['contact'][0] != "h":
        link = parsed_url.netloc + categorized_links['contact']
    html = get_html(link)
    contact_text = clean_html(html)
    contacts = extract_email_and_phone(contact_text)
else:
    contacts = extract_email_and_phone(home_text)

# extract brand description
if categorized_links['about'] is not None:
    if categorized_links['about'][0] != "h":
        link = parsed_url.netloc + categorized_links['about']
    html = get_html(link)
    about_text = clean_html(html)
    description = extract_brand_description(about_text)
else:
    description = extract_brand_description(home_text)



    

