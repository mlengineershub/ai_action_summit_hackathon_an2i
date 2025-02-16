import os
import json
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
from typing import Any, Type
from pydantic import BaseModel
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import MongoClient
import urllib.parse
from typing import Optional, Any, Dict, List

ResponseType = Type[BaseModel]

load_dotenv()

api_key = os.getenv("API_KEY")
url = os.getenv("PROVIDER_URL")

USERNAME_MONGODB: str = os.getenv("USERNAME_MONGODB", "")
PASSWORD_MONGODB: str = os.getenv("PASSWORD_MONGODB", "")
INSTANCE_MONGODB: str = os.getenv("INSTANCE_MONGODB", "")
REGION_MONGODB: str = os.getenv("REGION_MONGODB", "")
PATH_TLS_CERTIFICATE_MONGODB: str = os.getenv("PATH_TLS_CERTIFICATE_MONGODB", "")


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
            model="mistral-large-latest",
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


def get_mongo_client() -> MongoClient:
    username = urllib.parse.quote_plus(USERNAME_MONGODB)
    password = urllib.parse.quote_plus(PASSWORD_MONGODB)  # URL-encode the colon
    instance_id = INSTANCE_MONGODB
    region = REGION_MONGODB  # the region of your database instance. "fr-par" if Paris
    tls_certificate = PATH_TLS_CERTIFICATE_MONGODB  # path to your TLS certificate file
    # Construct the connection string
    connection_string = (
        f"mongodb+srv://{username}:{password}@{instance_id}.mgdb.{region}.scw.cloud/"
        f"?tls=true&tlsCAFile={tls_certificate}"
    )
    client = MongoClient(connection_string)

    return client
    # flake8: noqa


def get_database() -> Database:
    client = get_mongo_client()
    db = client[USERNAME_MONGODB]
    return db


def get_table(db: Database, table_name: str) -> Collection:
    return db[table_name]


def create_index(table: Collection, fields: List[str]) -> None:
    table.create_index(fields)


def insert(table: Collection, document: Dict[str, Any]) -> None:
    table.insert_one(document)


def find_one(table: Collection, query: Dict[str, Any]) -> Any:
    return table.find_one(query)


def find(table: Collection, query: Dict[str, Any]) -> Any:
    return table.find(query)
