from typing import Any, Union
from fastapi import FastAPI
from pydantic import BaseModel


# object for processing input from the frontend
class TranslateInput(BaseModel):
    data: Any
    type: str


app = FastAPI()


@app.get("/")
def read_root():
    # return {"Hello": "World"}
    return "Hello World!"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/translate/api")
async def translate(data: TranslateInput):
    return {"translated": "this should be the translated thing"}

