from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from starlette import status

from .config import config


app = FastAPI(
    title="kappa-fn-logs",
    version="0.0.0",
    author="dpdani",
    generate_unique_id_function=lambda route: f"{route.name}",
)

mongo = MongoClient(config.db.url, password=config.db.password)[config.db.database][config.db.collection]


class CreateLog(BaseModel):
    fn: int
    exec_id: str
    stdout: str
    stderr: str


@app.post("/logs/")
def create_log(log: CreateLog):
    doc_id = mongo.find_one({
        "fn": log.fn,
    })["_id"]
    if doc_id is None:
        doc_id = mongo.insert_one({
            "fn": log.fn,
            "logs": [],
        })
    mongo.update_one({"_id": doc_id}, {
        "$push": {"logs": {
            "exec_id": log.exec_id,
            "stdout": log.stdout,
            "stderr": log.stderr,
        }}
    })


@app.get("/logs/{fn}/")
def get_logs(fn: int):
    doc = mongo.find_one({
        "fn": fn,
    })
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return doc
