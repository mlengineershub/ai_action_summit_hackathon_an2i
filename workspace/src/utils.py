import os
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from typing import Any

load_dotenv()


api_key = os.getenv("API_KEY")
url = os.getenv("PROVIDER_URL")


def initialize_client(api_key: str = api_key or "", url: str = url or "") -> OpenAI:
    client = OpenAI(api_key=api_key, base_url=url)
    return client


def generate_prompt(prompt_template: str, **kwargs: Any) -> str:
    return prompt_template.format(**kwargs)


def generate_response(client: OpenAI, system_prompt: str, user_prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        if (
            response.choices
            and response.choices[0].message
            and response.choices[0].message.content
        ):
            return response.choices[0].message.content
        else:
            return "No content in response."
    except OpenAIError as e:
        print(f"An error occured:{e}")
    return "An error occurred while generating the response."
