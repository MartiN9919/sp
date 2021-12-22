from synonyms_manager.socket_driver import request
from synonyms_manager.constant import SYNONYMS_CONSTANT


def get_synonyms(word, count=SYNONYMS_CONSTANT.ANSWER_COUNT, host=SYNONYMS_CONSTANT.HOST, port=SYNONYMS_CONSTANT.PORT):
    return [item[0] for item in request(host=host, port=port, data_type=0, data=word, param={'count': count})['data']]
