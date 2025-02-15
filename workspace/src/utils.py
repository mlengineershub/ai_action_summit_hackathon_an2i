import os
import json
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from typing import Any, Type
from pydantic import BaseModel

ResponseType = Type[BaseModel]

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
        if response.choices[0].message.content is not None:
            return response.choices[0].message.content
        else:
            return "No content in response."
    except OpenAIError as e:
        print(f"An error occured:{e}")
    return "An error occurred while generating the response."


def generate_structured_response(
    client: OpenAI, system_prompt: str, user_prompt: str, model: ResponseType
) -> dict[str, Any]:
    try:
        response = client.beta.chat.completions.parse(
            model="ministral-8b-latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=model,
        )
        response_content = response.choices[0].message.content
        print(response_content)
        # Attempt to parse the content as JSON
        try:
            if response_content is not None:
                data = json.loads(response_content)
            else:
                print("Response content is None.")
                return {"error": "Response content is None."}
        except json.JSONDecodeError as json_err:
            print(f"JSON parsing error: {json_err}")
            return {"error": "Response is not valid JSON."}
        # Validate using Pydantic
        response_object = model.model_validate(data)
        return response_object.model_dump()
    except OpenAIError as e:
        print(f"An error occurred: {e}")
    return {"error": "An error occurred while generating the response."}
