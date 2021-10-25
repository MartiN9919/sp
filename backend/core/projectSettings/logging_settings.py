import os
from core.settings import BASE_DIR
import logging.handlers


LOG_DIR  = str(BASE_DIR)+'/log/'

PROJECT_LOG_MAIN     = 'MAIN'              # логгер главный
PROJECT_LOG_USERS    = 'USERS'             # логгер пользователи
PROJECT_LOG_REQUESTS = 'REQUESTS'          # логгер запросы
PROJECT_LOG_SCRIPT_ERROR = 'SCRIPT_ERROR'          # логгер запросы

if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)

PROJECT_ID = 'saphir'

logger = {}

handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'.log', when='midnight', interval=1, backupCount=5)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))  # %Y-%m-%d
handler.setLevel(logging.INFO)
logger['root'] = logging.getLogger()
logger['root'].setLevel(logging.INFO)
logger['root'].addHandler(handler)

handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_main.log', when='midnight', interval=1, backupCount=10)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))  # %Y-%m-%d
handler.setLevel(logging.INFO)
logger['main'] = logging.getLogger(PROJECT_LOG_MAIN)
logger['main'].setLevel(logging.INFO)
logger['main'].addHandler(handler)

handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_requests.log', when='midnight', interval=1, backupCount=30)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))  # %Y-%m-%d
handler.setLevel(logging.INFO)
logger['requests'] = logging.getLogger(PROJECT_LOG_REQUESTS)
logger['requests'].setLevel(logging.INFO)
logger['requests'].addHandler(handler)

handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_script_error.log', when='midnight', interval=1, backupCount=30)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))  # %Y-%m-%d
handler.setLevel(logging.INFO)
logger['script_error'] = logging.getLogger(PROJECT_LOG_SCRIPT_ERROR)
logger['script_error'].setLevel(logging.INFO)
logger['script_error'].addHandler(handler)

logger['main'].info('Start')