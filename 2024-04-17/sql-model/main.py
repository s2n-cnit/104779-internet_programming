import message  # noqa: F401
import room  # noqa: F401
import user  # noqa: F401
import user_room  # noqa: F401
import uvicorn
from app import app, logger  # noqa: F401

if __name__ == "__main__":
    logger.info("CIao")
    uvicorn.run("main:app", host="0.0.0.0", port=9999, reload=True)
