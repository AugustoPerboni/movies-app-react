from fastapi import FastAPI
import uvicorn
from src.controllers.v1.auth_controller import router as auth_router

app = FastAPI(
    title="My Auth API",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="debug",
    )