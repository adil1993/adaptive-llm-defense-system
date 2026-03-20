from fastapi import FastAPI
from app.api import router

app = FastAPI(title="Adaptive LLM Defense System")

app.include_router(router)
