import admin.category  # noqa: F401
import admin.command  # noqa: F401
import admin.command_tag  # noqa: F401
import admin.tag  # noqa: F401
import admin.user  # noqa: F401
import admin.workflow  # noqa: F401
import auth  # noqa: F401
import me.category  # noqa: F401
import me.command  # noqa: F401
import me.command_tag  # noqa: F401
import me.tag  # noqa: F401
import me.workflow  # noqa: F401
from admin import router as router_admin
from auth import router as router_auth
from config import app_name, debug, logger  # noqa: F401
from error import ConflictException, NotFoundException, exception_handler
from fastapi import FastAPI
from me import router as router_me

app = FastAPI(title=app_name, debug=debug)

app.include_router(router_me)
app.include_router(router_admin)
app.include_router(router_auth)
app.add_exception_handler(NotFoundException, exception_handler)
app.add_exception_handler(ConflictException, exception_handler)
