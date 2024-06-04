import logging

from fastapi import FastAPI

app_name = "yacr"

logger = logging.getLogger(app_name.lower())
app = FastAPI(title=app_name.upper(), debug=True)
