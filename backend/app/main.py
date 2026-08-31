from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import chat
from .routes import conversitions



app = FastAPI();

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router);
app.include_router(conversitions.router);

@app.get("/heath")
def heath():
    return {
        "status":"AI Backend is live"
    }