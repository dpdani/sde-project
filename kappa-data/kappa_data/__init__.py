from typing import Self

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from starlette import status

from kappa_data.models import Function, KappaLog, User, get_db
from kappa_data.security import authenticate_user, create_access_token, get_current_user


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
    return SuccessfulLogin(
        access_token=access_token,
        token_type="bearer",
    )


@app.post("/signup/", response_model=Status)
def signup(user: LoginUser, db: Session = Depends(get_db)):
    User.signup(db, user.username, user.password)
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
    db.add(fn)
    fn = Function.get(db, fn.owner, fn.name)
    KappaLog.add(db, fn.owner, fn.name, {
        "status": "created"
    })
    return fn


@app.get("/functions/{fn_name}/", response_model=Function)
def get_function(fn_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return Function.get(db, owner=user.user_id, name=fn_name)


@app.get("/functions/id/{fn_id}/", response_model=Function)
def get_function_by_id(fn_id: int, db: Session = Depends(get_db)):
    return Function.get_by_id(db, fn_id)


@app.get("/functions/{fn_name}/logs/", response_model=list[KappaLog])
def get_function_logs(fn_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return KappaLog.get_all(db, user.user_id, fn_name)


@app.post("/functions/{fn_id}/logs/execution/{exec_id}", response_model=Status)
def log_function_execution(fn_id: int, exec_id: str, db: Session = Depends(get_db)):
    fn = Function.get_by_id(db, fn_id)
    KappaLog.add(db, fn.owner, fn.name, {
        "execution": "started",
        "exec_id": exec_id,
    })
    return Status.ok()


@app.delete("/functions/{fn_name}/", response_model=Status)
def delete_function(fn_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    fn = Function.get(db, owner=user.user_id, name=fn_name)
    if fn is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    db.delete(fn)
    return Status(status="deleted")
