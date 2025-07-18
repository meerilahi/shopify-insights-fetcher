from urllib.parse import urlparse
from extract_policy import extract_policy
from scrape import get_html, extract_links_from_html, clean_html, split_text
from extract_products import extract_products
from categorize_links import categorize_links
from extract_faqs import extract_faqs
from extract_email_and_phone import extract_email_and_phone
from extract_brand_description import extract_brand_description
from schemas import BrandData, Product, FAQ


def get_brand_data_service(url):
    parsed_url = urlparse(url)
    home_html = get_html(parsed_url)
    home_text = clean_html(home_html)
    links = extract_links_from_html(home_html)

    categorized_links = categorize_links(links)
    hero_products_raw = extract_products(split_text(home_html))

    # Extract all products
    all_products_raw = []
    for link in categorized_links['products']:
        try:
            if link[0] != "h":
                link = "https://" + parsed_url.netloc + link
            html = get_html(link)
            all_products_raw.extend(extract_products(split_text(html)))
        except:
            continue

    # Extract policy
    policy_text = ""
    for link in categorized_links['policy']:
        try:
            if link[0] != "h":
                link = "https://" + parsed_url.netloc + link
            html = get_html(link)
            policy_text += clean_html(html)
        except:
            continue
    policy = extract_policy(policy_text)

    # Extract FAQs
    if categorized_links['faq']:
        link = categorized_links['faq']
        if link[0] != "h":
            link = "https://" + parsed_url.netloc + link
        html = get_html(link)
        faq_text = clean_html(html)
        faqs_raw = extract_faqs(faq_text)
    else:
        faqs_raw = extract_faqs(home_text)

    # Extract contact info
    if categorized_links['contact']:
        link = categorized_links['contact']
        if link[0] != "h":
            link = "https://" + parsed_url.netloc + link
        html = get_html(link)
        contact_text = clean_html(html)
        contacts = extract_email_and_phone(contact_text)
    else:
        contacts = extract_email_and_phone(home_text)

    # Extract brand description
    if categorized_links['about']:
        link = categorized_links['about']
        if link[0] != "h":
            link = "https://" + parsed_url.netloc + link
        html = get_html(link)
        about_text = clean_html(html)
        description = extract_brand_description(about_text)
    else:
        description = extract_brand_description(home_text)

    # Convert raw data to Pydantic models
    hero_products = [Product(**p) for p in hero_products_raw]
    all_products = [Product(**p) for p in all_products_raw] + hero_products
    faq_list = [FAQ(**f) for f in faqs_raw]

    return BrandData(
        whole_product_catalog=all_products,
        hero_products=hero_products,
        privacy_policy=policy.get("privacy_policy"),
        return_refund_policy=policy.get("return_refund_policy"),
        faqs=faq_list,
        social_handles=categorized_links.get("social_handles", []),
        emails=contacts.get("emails", []),
        phone_numbers=contacts.get("phone_numbers", []),
        brand_description=description,
        important_links=categorized_links.get("important_links", [])
    )
