import logging
from sys import stdout

logger = logging.getLogger()

# cleanup logging handlers
if logger.handlers:
    logger.handlers.clear()
streamHandler = logging.StreamHandler(stdout)

logger.addHandler(streamHandler)

logger.setLevel(logging.INFO)

def log(title, *args):
    msg = ""
    for a in args:
        msg = str(msg) + str(a)
    s = f"{title}: {msg}"
    logger.info(str(s))

def err(title, *args):
    msg = ""
    for a in args:
        msg = str(msg) + str(a)
    s = f"{title}: {msg}"
    logger.error(str(s))