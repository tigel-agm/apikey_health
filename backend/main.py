from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.keys import router
from .db import init_db
from .scheduler import start_scheduler

app = FastAPI(title="API Key Health Monitor")

# Allow CORS for Streamlit UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()
