import os
from pathlib import Path

from fastapi import Body, FastAPI, HTTPException
from starlette import status

from .config import config


app = FastAPI(
    title="kappa-fn-code",
    version="0.0.0",
    author="dpdani",
    generate_unique_id_function=lambda route: f"{route.name}",
)


@app.post("/code/{code_id}/")
def create_code(code_id: str, code: str = Body()):
    code_path = Path(config.code_folder) / code_id
    if code_path.exists():
        raise HTTPException(status.HTTP_409_CONFLICT)
    with open(code_path, "w") as f:
        f.write(code)


@app.delete("/code/{code_id}/")
def delete_code(code_id: str):
    code_path = Path(config.code_folder) / code_id
    if not code_path.exists():
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    code_path.unlink(missing_ok=True)


@app.get("/code/{code_id}/", response_model=str)
def get_code(code_id: str):
    code_path = Path(config.code_folder) / code_id
    if not code_path.exists():
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    with open(code_path, 'r') as f:
        return f.read()


@app.get("/code/", response_model=list[str])
def get_code_ids():
    return os.listdir(Path(config.code_folder))
