from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from starlette import status

from .config import config


app = FastAPI()

mongo = MongoClient(config.db.url, password=config.db.password)[config.db.database][config.db.collection]


class CreateLog(BaseModel):
    user: int
    fn: int
    exec_id: int
    content: str


@app.post("/logs/")
def create_log(log: CreateLog):
    doc_id = mongo.find_one({
        "user": log.user,
        "fn": log.fn,
    })["_id"]
    if doc_id is None:
        doc_id = mongo.insert_one({
            "user": log.user,
            "fn": log.fn,
            "logs": [],
        })
    mongo.update_one({"_id": doc_id}, {
        "$push": {"logs": {
            "exec_id": log.exec_id,
            "content": log.content,
        }}
    })


@app.get("/logs/{user}/{fn}/")
def get_logs(user: int, fn: int):
    doc = mongo.find_one({
        "user": user,
        "fn": fn,
    })
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return doc
