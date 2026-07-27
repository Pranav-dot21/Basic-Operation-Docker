
from datetime import datetime
import os
from typing import Any, Dict, List

from pymongo import MongoClient
from pymongo.collection import Collection


def get_mongo_client() -> MongoClient:
    # Priority: full URI, then user/password/host/port
    uri = os.getenv("MONGO_URI")
    if uri:
        return MongoClient(uri)
    host = os.getenv("MONGO_HOST", "some-mongo")
    port = os.getenv("MONGO_PORT", "27017")
    user = os.getenv("MONGO_USER")
    password = os.getenv("MONGO_PASSWORD")
    if user and password:
        return MongoClient(f"mongodb://{user}:{password}@{host}:{port}")
    return MongoClient(f"mongodb://{host}:{port}")


def get_collection() -> Collection:
    client = get_mongo_client()
    db_name = os.getenv("MONGO_DB", "calculator_db")
    coll_name = os.getenv("MONGO_COLLECTION", "calculations")
    db = client[db_name]
    return db[coll_name]


def init_db() -> None:
    collection = get_collection()
    # ensure index on created_at for sorting
    collection.create_index([("created_at", -1)])


def save_calculation(input1: float, input2: float, operator: str, result: float) -> str:
    collection = get_collection()
    document = {
        "input1": input1,
        "input2": input2,
        "operator": operator,
        "result": result,
        "created_at": datetime.utcnow(),
    }
    inserted = collection.insert_one(document)
    return str(inserted.inserted_id)


def fetch_history(limit: int = 100, skip: int = 0) -> List[Dict[str, Any]]:
    collection = get_collection()
    cursor = collection.find().sort("created_at", -1).skip(skip).limit(limit)
    return [
        {
            "id": str(item.get("_id")),
            "input1": item.get("input1"),
            "input2": item.get("input2"),
            "operator": item.get("operator"),
            "result": item.get("result"),
            "created_at": item.get("created_at").isoformat() if item.get("created_at") is not None else None,
        }
        for item in cursor
    ]
