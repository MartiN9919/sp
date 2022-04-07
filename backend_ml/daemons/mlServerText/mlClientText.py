# -*- coding: utf-8 -*-

from   fun.funSys             import logger, logError
from   fun.funSocket          import SocketClient, VAR

from   mlServerTextConst      import SERVER_TEXT


class MLClientText():
    def __init__(self, host=VAR.HOST, port=VAR.PORT):
        self.host = host
        self.port = port

        # print(self.w2vSim('Статкевич'))
        # ret = self.request(SERVER_TEXT.TYPE_DATA, 'Привет0 Лунатикам!!!')
        # ret = self.request(SERVER_TEXT.TYPE_SQL, 'Привет Земляне!')

    def stop(self):
        pass

    ##########################################################
    # W2V
    ##########################################################
        # print(self.w2vSim('Статкевич'))
    def w2vSim(self, word, count=10):
        ret = self.request(
            type  = SERVER_TEXT.TYPE_W2V_SIM,
            data  = word,
            param = {SERVER_TEXT.PARAM_COUNT: count}
        )
        return ret.get(SERVER_TEXT.KEY_RET_DATA, []) if ret != None else None



    ##########################################################
    # TFIDF: SIM
    ##########################################################
    def tfidfSim(self, docs1, docs2, type_sql1=SERVER_TEXT.PARAM_SQL_TYPE_AUTO, type_sql2=SERVER_TEXT.PARAM_SQL_TYPE_AUTO, isCorrect=False):
        ret = self.request(
            type  = SERVER_TEXT.TYPE_TFIDF_SIM,
            data  = docs1,
            param = {SERVER_TEXT.PARAM_DATA_2: docs2, SERVER_TEXT.PARAM_SQL_TYPE: type_sql1, SERVER_TEXT.PARAM_SQL_TYPE_2: type_sql2, SERVER_TEXT.PARAM_CORRECT: isCorrect}
        )
        return ret.get(SERVER_TEXT.KEY_RET_DATA, []) if ret != None else None




    ##########################################################
    # TFIDF: GROUP
    ##########################################################
        # print(self.tfidfGroup(docs="SELECT title_name FROM arc WHERE dat BETWEEN '2019-05-05' AND '2019-05-06' AND host='talks.by' ORDER BY dat DESC LIMIT 20;", sim=0.2))
        # print(self.tfidfGroup(docs="SELECT id, title_name FROM iarc WHERE host='talks.by' ORDER BY dat ASC LIMIT 20;", sim=0.2))
        # print(self.tfidfGroup(docs=[
        #     "Национальная культура, история белорус",
        #     "Петрович провел пресс-конференцию",
        #     "Национальная культура, язык и история белорус",
        #     "Петрович назначил пресс-конференцию для журналистов",
        #     "Я купил новую болгарку для работ",
        #     "буду работать с купленной болгаркой",
        #     "купить болгарку на пресс-конференцию для журналистов"
        # ], sim=0.2))
        # print(self.tfidfGroup(docs=[
        #     (1, "Национальная культура, история белорус"),
        #     (2, "Петрович провел пресс-конференцию"),
        #     (3, "Национальная культура, язык и история белорус"),
        #     (4, "Петрович назначил пресс-конференцию для журналистов")
        # ]))
        # ret = [0, 1, 2, ...]                           isUnique=True
        # ret = [[0, 2], [1, 3], [2, 0], [3, 6, 1], ...] isUnique=False
    ##########################################################
    def tfidfGroup(self, docs, sim=0.2, type_sql=SERVER_TEXT.PARAM_SQL_TYPE_AUTO, isUnique=True):
        ret = self.request(
            type  = SERVER_TEXT.TYPE_TFIDF_GROUP,
            data  = docs,
            param = {SERVER_TEXT.PARAM_SIM: sim, SERVER_TEXT.PARAM_SQL_TYPE: type_sql, SERVER_TEXT.PARAM_UNIQUE: isUnique}
        )
        return ret.get(SERVER_TEXT.KEY_RET_DATA, []) if ret != None else None




    ##########################################################
    # BOT
    ##########################################################
        # print(self.botGetAnswer('Порошенко Киев заявил'))
    def botGetAnswer(self, quest):
        ret = self.request(
            type = SERVER_TEXT.TYPE_BOT_GET,
            data = quest
        )
        return ret.get(SERVER_TEXT.KEY_RET_DATA, '') if ret != None else None

    def botAddRec(self, quest, answer, host='', author_id=''):
        ret = self.request(
            type = SERVER_TEXT.TYPE_BOT_SET,
            data = {
                SERVER_TEXT.DATA_BOT_QUEST:     quest,
                SERVER_TEXT.DATA_BOT_ANSWER:    answer,
                SERVER_TEXT.DATA_BOT_HOST:      host,
                SERVER_TEXT.DATA_BOT_AUTHOR_ID: author_id,
            }
        )
        return ret.get(SERVER_TEXT.KEY_RET_DATA, False) if ret != None else None

    def botImportRec(self, host='', author_id='', date_from=''):
        ret = self.request(
            type = SERVER_TEXT.TYPE_BOT_IMPORT,
            data = {
                SERVER_TEXT.DATA_BOT_HOST:      host,
                SERVER_TEXT.DATA_BOT_AUTHOR_ID: author_id,
                SERVER_TEXT.DATA_BOT_DATE_FROM: date_from,
            }
        )


    ##########################################################
    # ОБРАБОТЧИК ЗАПРОСА
    ##########################################################
    def request(self, type, data=None, param=None):
        client = SocketClient(host=self.host, port=self.port, timeout=30.0)
        try:
            dat    = {SERVER_TEXT.KEY_TYPE: type}
            if data  != None: dat[SERVER_TEXT.KEY_DATA]  = data
            if param != None: dat[SERVER_TEXT.KEY_PARAM] = param
            ret    = client.request(dat)
        except Exception as e:
            ret = None
            raise e
        finally:
            client = None
        return ret


