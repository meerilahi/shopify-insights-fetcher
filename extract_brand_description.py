from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate(
    template=
    """
You are an expert web content summarizer. From the text below, extract a short and meaningful brand description.

- Focus on summarizing what the brand is, what it sells or offers, and what makes it unique.
- Avoid boilerplate content like "Welcome to our website" or purely legal/policy language.
- If no brand identity or description is found, return null.

Text:
\"\"\"{text}\"\"\"

Return the result in this format:
{
"brand_description": "..."
}
    """,
    input_variables=["text"]
)

model = ChatOpenAI(model="gpt-4o-2024-08-06")

# Output schema
schema = {
    "title": "BrandDescriptionExtraction",
    "type": "object",
    "properties": {
        "brand_description": {"type": ["string", "null"]}
    },
    "required": ["brand_description"]
}

model = model.with_structured_output(schema)

def extract_brand_description(text):
    prompt = prompt_template.invoke({"text": text})
    return model.invoke(prompt)
