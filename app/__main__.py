"""python -m app — запустить сервер на http://127.0.0.1:8765"""
import os

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8765))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port)
