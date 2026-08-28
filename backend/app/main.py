from fastapi import FastAPI

from .routes import chat



app = FastAPI();

app.include_router(chat.router);

@app.get("/heath")
def heath():
    return {
        "status":"AI Backend is live"
    }