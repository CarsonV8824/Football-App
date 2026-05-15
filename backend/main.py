from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Team(BaseModel):
    name:str
    year:int

@app.post("/save_team")
async def save_team(team:Team):
    return {"message": "200", "name":team.name}