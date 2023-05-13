import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("Chatlog")
logger.setLevel(logging.WARNING)
handler = RotatingFileHandler(filename='mylog.log', maxBytes=1024, backupCount=2)
logger.addHandler(handler)
