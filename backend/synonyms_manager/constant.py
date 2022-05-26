import os

from core.projectSettings.constant import DEPLOY_SETTING

mode = os.environ.get('MODE')


class SYNONYMS_CONSTANT:
    HOST = DEPLOY_SETTING['synonyms']['host'] if mode == 'deploy' else '200.200.200.236'
    PORT = DEPLOY_SETTING['synonyms']['port'] if mode == 'deploy' else 5000
    SIZE = DEPLOY_SETTING['synonyms']['size'] if mode == 'deploy' else 1024
    ANSWER_COUNT = DEPLOY_SETTING['synonyms']['count'] if mode == 'deploy' else 10
