import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    # Robust port detection for Railway/Render/Heroku
    port_str = os.environ.get("PORT", "8000")
    try:
        port = int(port_str)
    except ValueError:
        # If the platform passes "$PORT" literally for some reason, fallback to 8000
        port = 8000
    
    print(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
