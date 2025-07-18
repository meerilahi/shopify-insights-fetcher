from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def extract_policy(text):


    prompt_template = PromptTemplate(
        template=
        """
You are a legal text analyzer. From the given website content, extract the following two sections if they exist:

1. **Privacy Policy**: Extract only the content relevant to privacy—how the site collects, stores, and handles user data.
2. **Return/Refund Policy**: Extract only the section(s) discussing the return, exchange, or refund of purchased items.

If a section is not present, set it to `None`. Don't fabricate or guess.

Content:
\"\"\"{text}\"\"\"

Return a JSON-compatible dictionary with two keys: "privacy_policy" and "return_refund_policy".
        """,
        input_variables=["text"]
    )

    model = ChatOpenAI(model="gpt-4o-2024-08-06")

    schema = {
        "title": "ExtractedPolicySections",
        "type": "object",
        "properties": {
            "privacy_policy": {"type": ["string", "null"]},
            "return_refund_policy": {"type": ["string", "null"]}
        },
        "required": ["privacy_policy", "return_refund_policy"]
    }

    model = model.with_structured_output(schema)

    prompt = prompt_template.invoke({"text": text})
    return model.invoke(prompt)
