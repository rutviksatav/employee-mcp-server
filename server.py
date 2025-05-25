import uvicorn
import os
from app import app

# Environment variable configuration
HOST = os.getenv("HOST", "127.0.0.1")  # Changed to localhost
PORT = int(os.getenv("PORT", "8000"))   # Changed to 8000 for local development

def run():
    """Start the FastAPI server with uvicorn"""
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")

if __name__ == "__main__":
    run()

