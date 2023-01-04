from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
from starlette import status

from .config import config


app = FastAPI(
    title="kappa-fn-logs",
    version="0.0.0",
    author="dpdani",
    generate_unique_id_function=lambda route: f"{route.name}",
)

client = MongoClient(config.db.url)[config.db.database]
try:
    client.create_collection(config.db.collection)
except CollectionInvalid:  # already exists
    pass
mongo = client.get_collection(config.db.collection)


class CreateLog(BaseModel):
    fn: int
    exec_id: str
    stdout: str
    stderr: str


@app.post("/logs/")
def create_log(log: CreateLog):
    doc = mongo.find_one({
        "fn": log.fn,
    })
    if doc is None:
        doc = mongo.insert_one({
            "fn": log.fn,
            "logs": [],
        })
        doc_id = doc.inserted_id
    else:
        doc_id = doc["_id"]
    mongo.update_one({"_id": doc_id}, {
        "$push": {"logs": {
            "exec_id": log.exec_id,
            "stdout": log.stdout,
            "stderr": log.stderr,
            "ts": datetime.utcnow(),
        }}
    })


class FnLog(BaseModel):
    exec_id: str
    stdout: str
    stderr: str
    ts: datetime


class FnLogs(BaseModel):
    fn: int
    logs: list[FnLog]


@app.get("/logs/{fn}/")
def get_logs(fn: int):
    doc = mongo.find_one({
        "fn": fn,
    })
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return FnLogs.parse_obj({
        "fn": doc["fn"],
        "logs": doc["logs"],
    })


@app.get("/logs/exec/{exec_id}/")
def get_exec_logs(exec_id: str):
    doc = mongo.find_one({
        "logs.exec_id": exec_id,
    })
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    print(doc)
    return FnLogs.parse_obj({
        "fn": doc["fn"],
        "logs": list(filter(lambda _: _["exec_id"] == exec_id, doc["logs"])),
    })
