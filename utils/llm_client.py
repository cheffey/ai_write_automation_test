import os
from pathlib import Path

os.environ["OPENAI_API_KEY"] = "FAKE_KEY"
from openai import OpenAI


class LLMClient:
    def __init__(self, base_url, api_key):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

    def ask(self, query, save_to=None, print_response=True):
        response = self.client.chat.completions.create(
            model="model",
            messages=[
                {"role": "user", "content": query}
            ],
            stream=True
        )
        resp = ''
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content is not None:
                resp += content
                print_response and print(content, end='')
        if save_to:
            save_to = Path(save_to)
            save_to.parent.mkdir(parents=True, exist_ok=True)
            save_to.write_text(resp)
        return resp
