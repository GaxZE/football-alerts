from fastapi import FastAPI
from os import getcwd
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def main():
    return FileResponse(path=getcwd() + "/api/data/scores.json")