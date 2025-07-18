from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()


prompt_template = PromptTemplate(
    template=
    """
You are an expert in web navigation and user experience. Given the following list of URLs from a brand or e-commerce website, categorize them into the following keys and return a JSON-compatible dictionary:

1. **products**: A list of links related to product categories or types (e.g., new arrivals, trending, kitchen items, shoes, clothing, electronics).
2. **social_handles**: A list of links pointing to official social media platforms like Instagram, Facebook, Twitter, YouTube, TikTok, etc.
3. **contact**: A single link to the contact page.
4. **policy**: A list of links to pages like privacy policy, refund policy, shipping policy, terms and conditions.
5. **faq**: A single link to the frequently asked questions (FAQ) page.
6. **about**: A single link to the about us page.
7. **important_links**: A list of useful links that don’t fit in the above categories but are still significant (e.g., careers, store locator, size guide, press, sustainability, blog).

If a category does not apply (e.g., no FAQ link), set its value to None (if it's a string) or an empty list (if it's a list).

Return only the structured dictionary.

Links:
{links}
    """,
    input_variables=["links"]
)

model = ChatOpenAI(model="gpt-4o-2024-08-06")

schema = {
    "title": "LinkCategorization",
    "type": "object",
    "properties": {
        "products": {"type": "array", "items": {"type": "string"}},
        "social_handles": {"type": "array", "items": {"type": "string"}},
        "contact": {"type": ["string", "null"]},
        "policy": {"type": "array", "items": {"type": "string"}},
        "faq": {"type": ["string", "null"]},
        "about": {"type": ["string", "null"]},
        "important_links": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["products", "social_handles", "contact", "policy", "faq", "about", "important_links"]
}

model = model.with_structured_output(schema)

def categorize_links(links):
    formatted_links = "\n".join(links)
    prompt = prompt_template.invoke({"links": formatted_links})
    return model.invoke(prompt)
