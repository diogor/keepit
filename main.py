from fastapi import FastAPI

app = FastAPI()


@app.get("/{key}")
async def index(key: str):
    return {"Hello": "World"}
