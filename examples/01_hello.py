# Step 1: the smallest FastAPI app.
# Run:   fastapi dev examples/01_hello.py
# Open:  http://127.0.0.1:8000  and the docs at  http://127.0.0.1:8000/docs
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello from itadimaigal!"}


@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello, {name}!"}
