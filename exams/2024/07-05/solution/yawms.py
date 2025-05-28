#!/usr/bin/env -S poetry -C /axc-mgmt/github/teaching/104779-internet_programming/exams/2024/07-05/solution run python

import uvicorn
from config import host, port

if __name__ == "__main__":
    uvicorn.run("app:app", host=host, port=port, reload=True)
