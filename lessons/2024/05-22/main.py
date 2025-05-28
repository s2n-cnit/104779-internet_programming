import logging

import admin.message  # noqa: F401
import admin.room  # noqa: F401
import admin.user  # noqa: F401
import auth  # noqa: F401
import uvicorn
from admin import router as router_admin
from auth import router as router_auth
from fastapi import FastAPI
from me import router as router_me

app_name = "yacr"

logger = logging.getLogger(app_name.lower())
app = FastAPI(title=app_name.upper(), debug=True)

app.include_router(router_me)
app.include_router(router_admin)
app.include_router(router_auth)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)
