import logging

import admin.category  # noqa: F401
import admin.tag  # noqa: F401
import admin.task  # noqa: F401
import admin.task_tag  # noqa: F401
import admin.user  # noqa: F401
import auth  # noqa: F401
import me.category  # noqa: F401
import me.tag  # noqa: F401
import me.task  # noqa: F401
import me.task_tag  # noqa: F401
from admin import router as router_admin
from auth import router as router_auth
from error import ConflictException, NotFoundException, exception_handler
from fastapi import FastAPI
from me import router as router_me

app_name = "yatms"

logging.getLogger("passlib").setLevel(logging.ERROR)
logger = logging.getLogger(app_name.lower())

app = FastAPI(title=app_name.upper(), debug=True)

app.include_router(router_me)
app.include_router(router_admin)
app.include_router(router_auth)
app.add_exception_handler(NotFoundException, exception_handler)
app.add_exception_handler(ConflictException, exception_handler)
