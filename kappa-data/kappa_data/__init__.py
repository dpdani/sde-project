import json
from typing import Self

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from starlette import status

from kappa_data.models import Function, KappaLog, User, get_db
from kappa_data.security import authenticate_user, create_access_token, get_current_user, get_password_hash


app = FastAPI(
    title="kappa-data",
    version="0.0.0",
    author="dpdani",
    generate_unique_id_function=lambda route: f"{route.name}",
)


class Status(BaseModel):
    status: str

    @classmethod
    def ok(cls) -> Self:
        return cls(status="ok")


class LoginUser(BaseModel):
    username: str
    password: str


class SuccessfulLogin(BaseModel):
    access_token: str
    token_type: str


@app.post("/login/", response_model=SuccessfulLogin)
def login(user: LoginUser, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.username, user.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.login}
    )
    user.token = access_token
    db.add(user)
    db.commit()
    return SuccessfulLogin(
        access_token=access_token,
        token_type="bearer",
    )


@app.post("/signup/", response_model=Status)
def signup(user: LoginUser, db: Session = Depends(get_db)):
    User.signup(db, user.username, get_password_hash(user.password))
    return Status.ok()


@app.get("/users/me/", response_model=User)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


class CreateFunction(BaseModel):
    name: str
    code_id: str


@app.post("/functions/", response_model=Function)
def create_function(function: CreateFunction, user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    fn = Function(
        name=function.name,
        code_id=function.code_id,
        owner=user.user_id,
    )
    try:
        db.add(fn)
        db.commit()
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT)
    fn = Function.get(db, fn.owner, fn.name)
    KappaLog.add(db, fn.owner, fn.fn_id, {
        "status": "created"
    })
    db.commit()
    return fn


@app.get("/functions/{fn_name}/", response_model=Function)
def get_function(fn_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    fn = Function.get(db, owner=user.user_id, name=fn_name)
    if fn is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return fn


@app.get("/functions/id/{fn_id}/", response_model=Function)
def get_function_by_id(fn_id: int, db: Session = Depends(get_db)):
    return Function.get_by_id(db, fn_id)


@app.get("/functions/{fn_id}/logs/", response_model=list[KappaLog])
def get_function_logs(fn_id: int, db: Session = Depends(get_db)):
    logs = KappaLog.get_all(db, fn_id).all()

    def converter(_: KappaLog):
        _.content = json.dumps(_.content)
        return _

    logs = list(map(converter, logs))
    return logs


@app.post("/functions/{fn_id}/logs/execution/{exec_id}", response_model=Status)
def log_function_execution(fn_id: int, exec_id: str, db: Session = Depends(get_db)):
    fn = Function.get_by_id(db, fn_id)
    KappaLog.add(db, fn.owner, fn.fn_id, {
        "status": "started",
        "exec_id": exec_id,
    })
    db.commit()
    return Status.ok()


@app.delete("/functions/{fn_name}/", response_model=Status)
def delete_function(fn_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    fn = Function.get(db, owner=user.user_id, name=fn_name)
    if fn is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    db.delete(fn)
    db.commit()
    return Status(status="deleted")


class Bill(BaseModel):
    total: int
    fn: dict[str, int]


@app.get("/bill/", response_model=Bill)
def bill(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    logs = db.exec(
        select(KappaLog)
        .where(KappaLog.user == user.user_id)
    ).all()
    functions = db.exec(
        select(Function)
        .where(Function.owner == user.user_id)
    ).all()
    get_fn_name = lambda fn_id: next(filter(lambda _: _.fn_id == fn_id, functions)).name
    counter = {}
    for fn in functions:
        counter[fn.fn_id] = 0
    for log in logs:
        if "exec_id" in log.content and "status" in log.content and log.content["status"] == "started":
            counter[log.fn] += 1
    counter = {
        get_fn_name(fn_id): counter[fn_id]
        for fn_id in counter
    }
    return Bill(total=sum(counter.values()), fn=counter)
