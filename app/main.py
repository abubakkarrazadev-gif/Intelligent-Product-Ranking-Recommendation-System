import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import endpoints

app = FastAPI(title="Amazon Ranker", version="1.0")

# Mount API routes
app.include_router(endpoints.router, prefix="/api")

# Mount static files for UI
app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

if __name__ == "__main__":
    # Get port from environment variable (Railway/Heroku/Render)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
