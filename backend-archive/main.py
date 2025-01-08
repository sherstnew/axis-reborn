from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import user
from data.db import init_db

app = FastAPI(
    title="Solaris",
    description="Transport workload"
)


@app.on_event("startup")
async def start_db():
    await init_db()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)