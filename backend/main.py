from fastapi import FastAPI, Query
from typing import Annotated
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None 
    price: float
    tax: float | None = None

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/movie/{movieid}")
def test(movieid: int):
    return {"received": movieid}

@app.get("/files/{filepath:path}")
async def read_file(filepath: str):
    return {"filepath": filepath}

@app.post("/items/")
async def create_item(item: Item):
    return item

# query data validation (using Annotated & Query)
@app.get("/itemsval/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id":"foo"}, {"item_id": "bar"}]}
    if q:
        results.update({"q":q})
    return results