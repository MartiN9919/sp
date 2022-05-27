import os

from core.projectSettings.constant import LOG_ROOT
from core.settings import BASE_DIR
import logging.handlers


LOG_DIR = LOG_ROOT if os.path.exists(LOG_ROOT) else str(BASE_DIR)+'/log/'

PROJECT_LOG_MAIN = 'MAIN'              # логгер главный
PROJECT_LOG_USERS = 'USERS'             # логгер пользователи
PROJECT_LOG_REQUESTS = 'REQUESTS'          # логгер запросы
PROJECT_LOG_SCRIPT_ERROR = 'SCRIPT_ERROR'          # логгер запросы

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

PROJECT_ID = 'saphir'


root_handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_other_error.log', when='midnight', interval=1, backupCount=5)
root_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))  # %Y-%m-%d
root_handler.setLevel(logging.WARNING)
root_logger = logging.getLogger()
root_logger.setLevel(logging.WARNING)
root_logger.addHandler(root_handler)

main_handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_main.log', when='midnight', interval=1, backupCount=10)
main_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(module)s:%(lineno)d %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))  # %Y-%m-%d
main_handler.setLevel(logging.INFO)
main_logger = logging.getLogger(PROJECT_LOG_MAIN)
main_logger.setLevel(logging.INFO)
main_logger.addHandler(main_handler)

request_handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_requests.log', when='midnight', interval=1, backupCount=30)
request_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))  # %Y-%m-%d
request_handler.setLevel(logging.INFO)
request_logger = logging.getLogger(PROJECT_LOG_REQUESTS)
request_logger.setLevel(logging.INFO)
request_logger.addHandler(request_handler)

script_handler = logging.handlers.TimedRotatingFileHandler(LOG_DIR+PROJECT_ID+'_script_error.log', when='midnight', interval=1, backupCount=30)
script_handler.setFormatter(logging.Formatter(fmt='%(asctime)s %(message)s', datefmt='%Y-%m-%d, %H:%M:%S'))  # %Y-%m-%d
script_handler.setLevel(logging.INFO)
script_error_logger = logging.getLogger(PROJECT_LOG_SCRIPT_ERROR)
script_error_logger.setLevel(logging.INFO)
script_error_logger.addHandler(script_handler)

main_logger.info('Start')
