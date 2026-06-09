from fastapi import FastAPI, Query
from typing import Annotated
from enum import Enum
from pydantic import BaseModel
from pydantic import AfterValidator

app = FastAPI()

@app.get('/user/me')
async def read_user_me():
    return {"message": "I am an fast api application"}

@app.get('/user/{user_id}')
async def read_user(user_id: str):
    return {"user_id": user_id}

class ModelName(int, Enum):
    alexnet = 1
    resnet = 2
    lenet = 3

@app.get('/models/{name}')
async def model_name(name: ModelName):
    if name is ModelName.alexnet:
        return {"model": name, "application": "Used for Purpose X"}
    elif name is ModelName.resnet:
        return {"model": name, "application": "Used for Purpose Y"}
    elif name is ModelName.lenet:
        return {"model": name, "application": "Used for purpose Z"}
    

@app.get('/file/{file_path:path}')
async def read_file_path(file_path: str):
    return {"file_path": file_path}

db_items = [{"item1": "Cooker"}, {"item2": "laptop"}, {"item3":"mobile"},{"item4": "charger"}]
@app.get('/items/')
async def read_db_items(skip: int = 1 , limit: int = 10):
    return db_items[skip: skip+limit]


@app.get('/item/')
async def read_db_item(item: str, q: str| None=None):
    if q:
        return {"item": item, "q": q}
    return {"item": item}


@app.get('/users/{user_id}/items/{item_id}')
def read_user_items(user_id: int, item_id: str, q: str | None=None, short: bool | None=None):
    item = {"user":user_id,"item": item_id}
    if q:
        item.update({"q": q})
    if short:
        item.update({"short": short})
    

    return item
    
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post('/items/')
def create_item(item: Item):
    return item