from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import calc, objects

app = FastAPI(
    title="Solaris",
    description="Transport workload"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calc.router)
app.include_router(objects.router)


# if __name__ == "__main__":
#     uvicorn.run("main:app, reload = True")


