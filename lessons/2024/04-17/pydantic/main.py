from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

rooms = {}


class User(BaseModel):
    name: str


class Room(BaseModel):
    name: str


class Result(BaseModel):
    success: bool
    detail: str


@app.post("/join")
def join(user: User, room: Room) -> Result:
    if room.name not in rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"room {room.name} not found",
        )
    elif user.name in rooms[room.name]["users"]:
        raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="user {user.name} already joined in room {room.name}",
        )
    else:
        rooms[room.name]["users"].append(user)
        return Result(
            success=True, detail=f"user {user.name} joined to room {room.name}"
        )


@app.get("/messages")
def messages(user: User, room: Room) -> list[Any]:
    if room.name not in rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"room {room.name} not found",
        )
    if user.name not in rooms[room.name]["users"]:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"user {user.name} not joined in room {room.name}",
        )
    return rooms[room.name]["messages"]


@app.put("/message")
def add(user: User, room: Room, message: str) -> Result:
    if room.name not in rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"room {room.name} not found",
        )
    if user.name not in rooms[room.name]["users"]:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"user {user.name} not joined in room {room.name}",
        )

    rooms[room.name]["messages"].append(
        {"timestamp": datetime.now(), "message": message}
    )
    return Result(
        success=True,
        detail=f"user {user.name} sent message {message} to room {room.name}",
    )


@app.post("/room")
def create(user: User, room: Room) -> Result:
    if room.name in rooms:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"room {room.name} already found",
        )
    rooms[room.name] = {"users": [user.name], "messages": []}
    return Result(
        success=True, detail=f"user {user.name} create room {room.name}"
    )


@app.get("/rooms")
def room() -> list[str]:
    return list(rooms.keys())


@app.delete("/room")
def delete(user: User, room: Room) -> Result:
    if room.name not in rooms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"room {room.name} not found",
        )
    if user.name not in rooms[room.name]["users"]:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"user {user.name} not joined in room {room.name}",
        )
    del rooms[room.name]
    return Result(
        success=True, detail=f"user {user.name} deletes room {room.name}"
    )
