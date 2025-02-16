import os
from dotenv import load_dotenv
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo import MongoClient
import urllib.parse
from typing import Any, Dict, List

load_dotenv()

USERNAME_MONGODB: str = os.getenv("USERNAME_MONGODB", "")
PASSWORD_MONGODB: str = os.getenv("PASSWORD_MONGODB", "")
INSTANCE_MONGODB: str = os.getenv("INSTANCE_MONGODB", "")
REGION_MONGODB: str = os.getenv("REGION_MONGODB", "")
PATH_TLS_CERTIFICATE_MONGODB: str = os.getenv("PATH_TLS_CERTIFICATE_MONGODB", "")


def get_mongo_client() -> MongoClient[Any]:
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
    client: MongoClient[Any] = MongoClient(connection_string)

    return client
    # flake8: noqa


def get_database() -> Database[Any]:
    client = get_mongo_client()
    db = client[USERNAME_MONGODB]
    return db


def get_table(db: Database[Any], table_name: str) -> Collection[Any]:
    return db[table_name]


def create_index(table: Collection[Any], fields: List[str]) -> None:
    table.create_index(fields)


def insert(table: Collection[Any], document: Dict[str, Any]) -> None:
    table.insert_one(document)


def find_one(table: Collection[Any], query: Dict[str, Any]) -> Any:
    return table.find_one(query)


def find(table: Collection[Any], query: Dict[str, Any]) -> Any:
    return table.find(query)
