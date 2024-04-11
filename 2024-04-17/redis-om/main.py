from fastapi import FastAPI, HTTPException, status
from model import Message, Room, User
from pydantic import BaseModel

app = FastAPI()


class Result(BaseModel):
    success: bool
    detail: str


@app.post("/user")
async def create_user(user: User) -> Result:
    u = await user.save()
    return Result(success=True, detail="user created", user=u)


@app.get("/user")
async def list_user():
    return await User.all_pks()


@app.get("/user/{pk}")
async def get_user(pk: str) -> User:
    try:
        return await User.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"Customer {pk} not found")
