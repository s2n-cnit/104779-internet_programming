from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

rooms = {}


@app.post("/join")
def join(username: str, room: str):
    if room not in rooms:
        raise HTTPException(status_code=404, detail=f"room {room} not found")
    elif username in rooms[room]['users']:
        raise HTTPException(status_code=304, detail="user {username} already joined in room {room}")
    else:
        rooms[room]["users"].append(username)
        return {'success': True, 'detail': f"user {username} joined to room {room}"}


@app.get('/messages')
def messages(username: str, room: str):
    if room not in rooms:
        raise HTTPException(status_code=404, detail=f"room {room} not found")
    if username not in rooms[room]['users']:
        raise HTTPException(status_code=405, detail=f"user {username} not joined in room {room}")
    return rooms[room]['messages']


@app.put('/message')
def add(username: str, room: str, message: str):
    if room not in rooms:
        raise HTTPException(status_code=404, detail=f"room {room} not found")
    if username not in rooms[room]['users']:
        raise HTTPException(status_code=405, detail=f"user {username} not joined in room {room}")
    rooms[room]['messages'] = {
        'timestamp': datetime.now(),
        'message': message
    }
    return {'success': True, 'detail': f"user {username} sent message {message} to room {room}"}


@app.post('/room')
def create(username: str, room: str):
    if room in rooms:
        raise HTTPException(status_code=409, detail=f"room {room} already found")
    rooms[room] = {
        "users": [username],
        'messages': []
    }
    return {'success': True, 'detail': f"user {username} create room {room}"}


@app.get('/room')
def room():
    return list(rooms.keys())