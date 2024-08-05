from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import assistant, thread
from app.logger import setup_logging

logger = setup_logging()

app = FastAPI(title="Math Teacher API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assistant.router)
app.include_router(thread.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
