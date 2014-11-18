import logging

DEBUG = True

PIDFILE = "/opt/logs/fp.pid"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename="/opt/logs/fp.log",
    filemode='a'
)

API = ""
PROCESS_SIZE = 1

FILE_PATH = "/opt/files/fp"