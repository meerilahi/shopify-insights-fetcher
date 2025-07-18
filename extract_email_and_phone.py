from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

prompt_template = PromptTemplate(
        template=
        """
You are a smart text parser. From the content below, extract:

1. A list of all valid email addresses.
2. A list of all phone numbers (local or international formats).

Only return the structured output. Do NOT fabricate missing information. If not found, return empty lists.

Text:
\"\"\"{text}\"\"\"

Return format:
{
  "emails": [...],
  "phone_numbers": [...]
}
        """,
        input_variables=["text"]
    )

model = ChatOpenAI(model="gpt-4o-2024-08-06")

# Define schema for structured output
schema = {
    "title": "EmailAndPhoneExtraction",
    "type": "object",
    "properties": {
        "emails": {
            "type": "array",
            "items": {"type": "string"}
        },
        "phone_numbers": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["emails", "phone_numbers"]
}

model = model.with_structured_output(schema)

def extract_email_and_phone(text): 

    prompt = prompt_template.invoke({"text": text})
    return model.invoke(prompt)
