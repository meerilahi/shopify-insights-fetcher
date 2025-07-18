from extract_policy import extract_policy
from scrape import get_html, extract_links_from_html, clean_html
from extract_products import extract_products
from categorize_links import categorize_links
from extract_faqs import extract_faqs

# get home page text and link
home_html = get_html("https://fanjoy.co/collections/take-care-of-yourself")
home_texts = clean_html(home_html, 6000)
links = extract_links_from_html(home_html)

# categorize links
categorized_links = categorize_links(links)

# extract heor products
hero_products = extract_products(home_texts)

# extract all products
all_products = []
for link in categorized_links['products']:
    try:
        if link[0] != "h":
            url = "https://fanjoy.co" + link
        html = get_html(url)
        texts = clean_html(html, 6000)
        all_products.extend(extract_products(texts))
    except:
        continue

# extract policy
policy_text_list = []
for link in categorized_links['policy']:
    if link[0] != "h":
        url = "https://fanjoy.co" + link
    html = get_html(url)
    policy_text_list.extend(clean_html(html, 6000))
    policy_text = "\n".join(policy_text_list)
policy = extract_policy(policy_text)

# extract FAQs
if categorized_links['faq'] is not None:
    if categorized_links['faq'][0] != "h":
        url = "https://fanjoy.co" + categorized_links['faq']
    html = get_html(url)
    faq_text = "\n".join(clean_html(html, 6000))
    faq = extract_faqs(faq_text)
else:
    faq = extract_faqs("\n".join(home_texts))


