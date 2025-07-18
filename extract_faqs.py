from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def extract_faqs(text):

    prompt_template = PromptTemplate(
        template=
        """
You are an intelligent FAQ extractor. From the content below, extract all frequently asked questions (FAQs) along with their direct answers.

Each FAQ must contain:
- "question": The question being asked (as a string)
- "answer": A clear and complete answer (as a string)

Only include actual FAQs. If none are present, return an empty list.

Content:
\"\"\"{text}\"\"\"

Return only a JSON-compatible list of objects like:
[
  {{
    "question": "...",
    "answer": "..."
  }},
  ...
]
        """,
        input_variables=["text"]
    )

    model = ChatOpenAI(model="gpt-4o-2024-08-06")

    # Output schema
    schema = {
        "title": "FAQExtraction",
        "type": "object",
        "properties": {
            "faqs": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "answer": {"type": "string"}
                    },
                    "required": ["question", "answer"]
                }
            }
        },
        "required": ["faqs"]
    }

    model = model.with_structured_output(schema)

    prompt = prompt_template.invoke({"text": text})
    return model.invoke(prompt)
