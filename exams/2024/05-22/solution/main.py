import logging

import admin.book  # noqa: F401
import admin.customer  # noqa: F401
import admin.loan  # noqa: F401
import admin.user  # noqa: F401
import auth  # noqa: F401
import me.book  # noqa: F401
import me.customer  # noqa: F401
import me.loan  # noqa: F401
import me.user  # noqa: F401
import uvicorn
from admin import router as router_admin
from auth import router as router_auth
from fastapi import FastAPI
from me import router as router_me

app_name = "yalm"

logger = logging.getLogger(app_name.lower())
app = FastAPI(title=app_name.upper(), debug=True)

app.include_router(router_me)
app.include_router(router_admin)
app.include_router(router_auth)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9998, reload=True)
