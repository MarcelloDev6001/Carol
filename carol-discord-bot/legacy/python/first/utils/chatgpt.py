from openai import OpenAI

client = OpenAI(
    api_key="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",
)

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "what was the most famous artist on 1918?",
        }
    ],
    model="gpt-3.5-turbo-16k-0613",
    response_format={"type": "json_object"},
)
print(completion)