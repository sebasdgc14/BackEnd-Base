from fastapi import FastAPI

app = FastAPI()  # This creates the app


@app.get("/")
def index():
    return {"data": {"name": "Sebastian"}}


@app.get("/about")
def about():
    return {"data": "about page"}
