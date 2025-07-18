from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

template1 = PromptTemplate(
    template=
"""
You are writing a fictional dialogue between a person and Karl Marx based on the passage below.

Instructions:
- The **person** should ask Karl Marx a reflective, philosophical, or opinion-based question inspired by the passage.
- The **question must directly address Karl Marx** using second-person phrasing (e.g., “Why do you think...?”, “What is your opinion on...?”, etc.).
- Do **NOT** use third-person phrasing like “Why does Marx believe...” or “What is Marx’s opinion on...”.
- The **response** should be written as if *Karl Marx himself* is answering the question.
- The tone, vocabulary, and reasoning of Marx’s response should match the style of the passage.
- Do **NOT** refer to "the passage" in either the question or the response. Avoid phrases like “the passage says...” or “according to the text.”

Your output should be a question from the person and an answer from Karl Marx.

Passage:
\"\"\"{chunk}\"\"\"
""",
    input_variables=['chunk']
)

model1 = ChatOpenAI(model="gpt-4o-2024-08-06")
instruction_schema1 = {
    "title": "DialogueWithMarx_from_passage",
    "type": "object",
    "properties": {
        "question": {
            "type": "string",
            "description": "The reflective, philosophical question asked by the person, addressed directly to Karl Marx using 'you'."
        },
        "marx_response": {
            "type": "string",
            "description": "Karl Marx's response, written in his tone and reasoning style based on the passage."
        }
    },
    "required": ["question", "marx_response"]
}

model1 = model1.with_structured_output(instruction_schema1)

dialogue = {}
with open("data.ndjson", "a") as file:
    for index, chunk in enumerate(chunks[22:]):
        print(f"\nProcessing chunk {index + 1+ 22} of {len(chunks)}... with chunk size {len(chunk)}")
        print("  Generating question and Marx-style response from passage...")
        prompt1 = template1.invoke({'chunk': chunk})
        response1 = model1.invoke(prompt1)
        print("  Generating naive Marx response without passage...")
        prompt2 = template2.invoke({'question': response1['question']})
        response2 = model2.invoke(prompt2)
        dialogue["index"] = index+22
        dialogue["text"] = chunk
        dialogue["question"] = response1["question"]
        dialogue["marx_response_from_passage"] = response1["marx_response"]
        dialogue["marx_response_naive"] = response2["marx_response"]
        json_line = json.dumps(dialogue)
        file.write(json_line + "\n")


