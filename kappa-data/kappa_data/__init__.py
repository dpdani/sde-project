from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlmodel import Session
from starlette import status

from .models import Function, KappaLog, User, get_db
from .security import authenticate_user, create_access_token, get_current_user


app = FastAPI(
    title="kappa-data",
    version="0.0.0",
    author="dpdani",
    generate_unique_id_function=lambda route: f"{route.name}",
)


class SuccessfulLogin(BaseModel):
    access_token: str
    token_type: str


@app.post("/login/", response_model=SuccessfulLogin)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
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


@app.get("/users/me/", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
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
    result = Function.get(db, fn.owner, fn.name)
    KappaLog.add(db, result.owner, result.name, {
        "status": "created"
    })
    return result


@app.get("/functions/{fn_name}/", response_model=Function)
def get_function(fn_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return Function.get(db, owner=user.user_id, name=fn_name)


class Status(BaseModel):
    status: str


@app.delete("/functions/{fn_name}/", response_model=Status)
def delete_function(fn_name: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    fn = Function.get(db, owner=user.user_id, name=fn_name)
    if fn is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    db.delete(fn)
    return Status(status="deleted")
