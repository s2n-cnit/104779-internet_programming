#!/usr/bin/env -S poetry run python

import uvicorn
from config import host, port

if __name__ == "__main__":
    uvicorn.run("app:app", host=host, port=port, reload=True)
