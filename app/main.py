from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import endpoints

app = FastAPI(title="Amazon Ranker", version="1.0")

# Mount API routes
app.include_router(endpoints.router, prefix="/api")

# Mount static files for UI
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
