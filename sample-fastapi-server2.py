from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Sample FastAPI Server 2",
    description="A sample FastAPI server with common endpoints",
    version="1.0.0"
)

# Models
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

# Sample data storage
items = []
users = []

# Basic CRUD endpoints
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items/", response_model=List[Item])
async def read_items(skip: int = 0, limit: int = 10):
    return items[skip : skip + limit]

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int):
    item = next((item for item in items if item.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    if item_id != item.id:
        raise HTTPException(status_code=400, detail="ID mismatch")
    for i, stored_item in enumerate(items):
        if stored_item.id == item_id:
            items[i] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for i, item in enumerate(items):
        if item.id == item_id:
            items.pop(i)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")

# User endpoints
@app.post("/users/", response_model=User)
async def create_user(user: User):
    users.append(user)
    return user

@app.get("/users/", response_model=List[User])
async def read_users():
    return users

# Query parameter example
@app.get("/search/")
async def search_items(q: str = Query(..., min_length=3)):
    results = [item for item in items if q.lower() in item.name.lower()]
    return results

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)