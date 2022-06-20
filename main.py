from fastapi import FastAPI

from controllers import router

app = FastAPI()

app.include_router(router)