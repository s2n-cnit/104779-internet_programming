from typing import Union
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

@app.post("/x")
@app.get("/test")
def test_post():
    return {"today": datetime.now() }

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
@app.get("/items")
def read_item(item_id: Union[str, None] = "bye", q: Union[str, None] = "hello"):
    return {"item_id": item_id, "q": q}
