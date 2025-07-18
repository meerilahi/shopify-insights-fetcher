from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import json
from dotenv import load_dotenv
load_dotenv()

template = PromptTemplate(
    template=
"""
You are an expert HTML parser. Extract a list of product information from the HTML content below.

Instructions:
- Each product should have the following fields:
  - name: The product's title or name
  - description: A short description, if available
  - image_url : Url of image
  - price: The product's price (numeric or formatted string)

If any field is missing in the HTML, omit it from that product's object.

Return only a list of products (not prose or markdown).

HTML content:
\"\"\"{html_chunk}\"\"\"
""",
    input_variables=['html_chunk']
)

model = ChatOpenAI(model="gpt-4o-2024-08-06")

instruction_schema = {
    "title": "ProductExtractionFromHTML",
    "type": "object",
    "properties": {
        "products": {
            "type": "array",
            "description": "List of products found in the HTML.",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "image_url": {"type": "string"},
                    "price": {"type": "string"}
                },
                "required": ["name", "image_url", "description", "price"]
            }
        }
    },
    "required": ["products"]
}

model = model.with_structured_output(instruction_schema)

def extract_products(chunks):
    products = []
    for html_chunk in chunks:
        prompt = template.invoke({'html_chunk': html_chunk})
        response = model.invoke(prompt)
        products.extend(response["products"])
    return products
