from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Feature(BaseModel):
    
    ...

@app.get('/')
async def get_item(Item):
    data = Item