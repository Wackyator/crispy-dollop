from fastapi import FastAPI
from app import api


app = FastAPI()
app.include_router(api.router)


@app.get("/")
async def index():
    return {"msg": "hello world!"}
