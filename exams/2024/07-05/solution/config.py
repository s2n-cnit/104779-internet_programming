import logging

host = "0.0.0.0"
port = 9998

app_name = "yawms"
db_path = f"{app_name}.db"
debug = True
echo_engine = False

logging.getLogger("passlib").setLevel(logging.ERROR)
logger = logging.getLogger(app_name)
