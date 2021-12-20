# -*- coding: utf-8 -*-

import time, os, gc

from   daemonIni              import DAEMON_INI
from   fun.funSys             import logger, logError, logging
from   fun.funText            import textToJSON
#from   fun.funBD              import BDReadLines, varGet
#from   fun.funSphinx          import SphinxReadLines, sphinxValidate
from   fun.funSocket          import SocketServer

#from   fun.ml.mlTFIDF         import TFIDF
from   mlServerTextConst      import CONNECT, SERVER_TEXT
from   mlModels               import (
    VAR,
    # BOT_TFIDF,
    _W2V_,
    _W2C_,
    #_D2V_,
    #_TFIDF_,
    _Tokenizer_,
    _TokenizerPhrases_,
)


class MLServerText():

    # ЗАМЕНА СЛОВ ПРИ КЛАСТЕРИЗАЦИИ
    wordsReplace = lambda self, words: words if (self.w2c is None) else self.w2c.wordsToKeys(words)

    def __init__(self, pathLib, worker):
        #logger.setLevel(logging.DEBUG)
        VAR_OWNER = 'mlServerText'
        logger.info('START!')

        try:
            self.var_owner    = 'mlServerText'
            VAR.PATH_LIB      = pathLib
            #connect           = textToJSON(varGet(self.var_owner, DAEMON_INI.WORKER, 'connect'))  # JSON-структура: читать

            # self.tk         = _Tokenizer_()
            self.tk           = _TokenizerPhrases_()
            self.w2v          = _W2V_  (tokenizer=self.tk)
            # self.reph       = Rephraser(tokenizer=self.tk, w2v=self.w2v, rnd=0.5, simWord=0.7, simMorph=0.7)
            self.w2c          = _W2C_  (w2v=self.w2v)
            # self.d2v        = _D2V_  (w2c=self.w2c)                           # (w2v=self.w2v)
            # self.bot        = BOT_TFIDF(w2c=self.w2c)                         # (w2v=self.w2v)

            # блокирующий процесс
            print('Ok')
            #logger.info('connect: '+str(connect))
            #self.mlServerText = SocketServer(funHandler=self.handler, host=connect.get('host', ''), port=connect.get('post', 5000))
            self.mlServerText = SocketServer(funHandler=self.handler, host=CONNECT.HOST, port=CONNECT.PORT)


            ##########################################################
            # группы подобных документов
            ##########################################################
            #tt = self.tfidf.groupData()
            #print(tt[:10])


            ##########################################################
            # импорт данных в ML_BOT
            ##########################################################
            # mochalka75                    561686  2019-03-07 15:00
            # Андрюза_Воеводин              878569  2019-01-08 15:00
            # Светлана_Григорьева_talks73   787804  2019-01-08 15:00 +
            # Андрей_Петровский_talks0      736916  2019-01-15 16:00 +
            # Love Belorussia               855278  2019-01-15 13:00
            # ellan                         141787  2019-01-21 15:00
            # id416116899                   809673  2019-03-06 15:00 +
            # apeook                        751105  2019-03-06 15:00 +
            # Kenos_Tischenkov              894829  2019-03-06 17:00 +
            # eedex                         317853  2019-03-06 17:00
            # Иван_Иванов_talks5            748499  2019-03-07 15:00
            # PanSportsmen                  24147   2019-03-07 16:00
            # maestro55                     306551  2019-03-18 12:00
            # self.bot.importArc(host='talks.by', author_id='306551', date_from='2018-06-01')


            ##########################################################
            # РАЗНОЕ
            ##########################################################
            # self.tfidf_bot = _TFIDF_(w2c=self.w2c, data_src=BDReadLines(sql="SELECT MIN(id), title_name FROM arc WHERE dat>='2019-03-20' AND host='talks.by' GROUP BY title_name LIMIT 500"), fileTF2V='')
            # self.bot.tfidf.simDocsAny(doc='Лукашенко встретился с Беларусь')


        except (KeyboardInterrupt, SystemExit):
            msg = 'Aborted by user. Wait for completion of processes ...'
            logger.info(msg)
            print('\n'+msg)
        except Exception as e:
            logError(e)
        finally:
            if hasattr(self, 'mlServerText'): self.mlServerText = None
            if hasattr(self, 'bot'):          self.bot.stop()
            logger.info('EXIT!')


    def handler(self, data):
        key     = data.get(SERVER_TEXT.KEY_TYPE,  None)
        param   = data.get(SERVER_TEXT.KEY_PARAM, {})
        data    = data.get(SERVER_TEXT.KEY_DATA,  None)
        retFlag = False
        retData = []
        try:
            ###################################################################
            # W2V: близкие слова
            # KEY_DATA  - слово
            # KEY_PARAM - SERVER_TEXT.PARAM_COUNT - количество возвращаемых слов, [10]
            ###################################################################
            if key == SERVER_TEXT.TYPE_W2V_SIM:
                word    = self.tk.run(data)
                word    = word[0] if len(word)>0 else ''
                if word != '':
                    retData = self.w2v.wordSim(word=word, topn=param.get(SERVER_TEXT.PARAM_COUNT, 10))
                    retFlag = True




            ###################################################################
            # TFIDF: наиболее подобный документ
            ###################################################################
            # KEY_DATA (KEY_PARAM.PARAM_DATA_2) - list or tuple: ((id, doc), ...) или (doc, ...) - id НЕ ИСПОЛЬЗУЕТСЯ
            # KEY_DATA (KEY_PARAM.PARAM_DATA_2) - SQL BD или SPHINX: "SELECT [id], title_name FROM arc WHERE host='talks.by' LIMIT 500;" - не длительный запрос, иначе увеличивать timeout
            # KEY_PARAM.PARAM_SQL_TYPE (KEY_PARAM.PARAM_SQL_TYPE_2) - тип SQL-запроса
            # RET - [[id_data_1, sim], ...]
            ###################################################################
            # elif key == SERVER_TEXT.TYPE_TFIDF_SIM:
            #     sqlType    = param.get(SERVER_TEXT.PARAM_SQL_TYPE, SERVER_TEXT.PARAM_SQL_TYPE_AUTO)
            #     data       = self.sqlToGenerator(data=data, sqlType=sqlType)

            #     sqlType_2  = param.get(SERVER_TEXT.PARAM_SQL_TYPE_2, SERVER_TEXT.PARAM_SQL_TYPE_AUTO)
            #     data_2     = param.get(SERVER_TEXT.PARAM_DATA_2,     None)
            #     data_2     = self.sqlToGenerator(data=data_2, sqlType=sqlType_2)
            #     data_2     = list(map((lambda item: item if isinstance(item, str) else item[1]), data_2))                   # убрать id

            #     isCorrect  = param.get(SERVER_TEXT.PARAM_CORRECT, False)

            #     tfidf_temp = TFIDF(dataSrc=data, tokenizer=self.tk, wordsReplace=self.wordsReplace, showInfo=False)
            #     retData    = []
            #     for item in data_2:
            #         val = tfidf_temp.simDoc(doc=item, isCorrect=isCorrect)
            #         retData.append([val[0], val[1]])
            #     retFlag    = True
            #     tfidf_temp = None
            #     gc.collect()




            ###################################################################
            # TFIDF: группировка документов
            ###################################################################
            # KEY_DATA  - list or tuple: ((id, doc), ...) или (doc, ...) - id добавляется автоматически
            # KEY_DATA  - SQL BD или SPHINX: "SELECT [id], title_name FROM arc WHERE host='talks.by' LIMIT 500;" - не длительный запрос, иначе увеличивать timeout
            # KEY_PARAM.PARAM_SIM      - минимальный коэффициент подобия, [0.2]
            # KEY_PARAM.PARAM_SQL_TYPE - тип SQL-запроса
            # KEY_PARAM.PARAM_UNIQUE   - только уникальные записи, [True]
            # RET       - [0, 3, 1, ...] (PARAM_UNIQUE=True)
            # RET       - [[0, 2], [1, 3], [3, 6, 1] ...] (PARAM_UNIQUE=False)
            ###################################################################
            elif key == SERVER_TEXT.TYPE_TFIDF_GROUP:
                simMin     = param.get(SERVER_TEXT.PARAM_SIM, 0.2)
                sqlType    = param.get(SERVER_TEXT.PARAM_SQL_TYPE, SERVER_TEXT.PARAM_SQL_TYPE_AUTO)
                isUnique   = param.get(SERVER_TEXT.PARAM_UNIQUE, True)
                data       = self.sqlToGenerator(data=data, sqlType=sqlType)

                # медленно на больших объемах
                # retData = self.bot.tfidf.groupDataFree(data=data, dataInd=dataInd, simMin=simMin)

                tfidf_temp = TFIDF(dataSrc=data, tokenizer=self.tk, wordsReplace=self.wordsReplace, showInfo=False)
                retData    = tfidf_temp.groupData(simMin=simMin, isUnique=isUnique)
                retFlag    = True
                tfidf_temp = None
                gc.collect()



            ###################################################################
            ########################### ML_BOT ################################
            ###################################################################

            ###################################################################
            # ML_BOT.TABLE: выбрать ответ
            ###################################################################
            # KEY_DATA - quest
            ###################################################################
            elif key == SERVER_TEXT.TYPE_BOT_GET:
                retData = self.bot.getAnswer(quest=data)
                retFlag = True

            ###################################################################
            # ML_BOT.TABLE: добавить запись
            ###################################################################
            # KEY_DATA - [quest, answer, [host], [author_id]]
            # KEY_DATA - {SERVER_TEXT.DATA_BOT_QUEST: '', SERVER_TEXT.DATA_BOT_ANSWER: '', ...}
            ###################################################################
            elif key == SERVER_TEXT.TYPE_BOT_SET:
                if isinstance(data, dict):
                    quest     = data.get(SERVER_TEXT.DATA_BOT_QUEST,     '')
                    answer    = data.get(SERVER_TEXT.DATA_BOT_ANSWER,    '')
                    host      = data.get(SERVER_TEXT.DATA_BOT_HOST,      '')
                    author_id = data.get(SERVER_TEXT.DATA_BOT_AUTHOR_ID, '')
                elif isinstance(data, (list, tuple)):
                    lenData = len(data)
                    quest     = data[0]
                    answer    = data[1]
                    host      = data[2] if lenData > 2 else ''
                    author_id = data[3] if lenData > 3 else ''
                retData = self.bot.addRec(
                    quest     = quest,
                    answer    = answer,
                    host      = host,
                    author_id = author_id
                    )
                retFlag = True

            ###################################################################
            # ML_BOT.TABLE: импортировать записи
            ###################################################################
            # KEY_DATA - [host, author_id, date_from]
            # KEY_DATA - {SERVER_TEXT.DATA_BOT_HOST: '', SERVER_TEXT.DATA_BOT_AUTHOR_ID: '', ...}
            ###################################################################
            elif key == SERVER_TEXT.TYPE_BOT_IMPORT:
                if isinstance(data, dict):
                    host      = data.get(SERVER_TEXT.DATA_BOT_HOST,      '')
                    author_id = data.get(SERVER_TEXT.DATA_BOT_AUTHOR_ID, '')
                    date_from = data.get(SERVER_TEXT.DATA_BOT_DATE_FROM, '')
                elif isinstance(data, (list, tuple)):
                    host      = data[0]
                    author_id = data[1]
                    date_from = data[2]
                self.bot.importRec(
                    host      = host,
                    author_id = author_id,
                    date_from = date_from
                    )
                retFlag = True





            ###################################################################
            # ЭКСПЕРИМЕНТ
            ###################################################################
            elif key == SERVER_TEXT.TYPE_DATA:
                retData = data.upper()
                retFlag = True

            elif key == SERVER_TEXT.TYPE_SQL:
                pass


        except Exception as e:
            logError(e)

        return {SERVER_TEXT.KEY_RET_FLAG: retFlag, SERVER_TEXT.KEY_RET_DATA: retData}



    # ###################################################################
    # # ЗАМЕНИТЬ SQL ГЕНЕРАТОРОМ
    # ###################################################################
    # def sqlToGenerator(self, data, sqlType=SERVER_TEXT.PARAM_SQL_TYPE_AUTO):
    #     if isinstance(data, str):
    #         if sqlType==SERVER_TEXT.PARAM_SQL_TYPE_AUTO:
    #             sqlType=SERVER_TEXT.PARAM_SQL_TYPE_SPHINX if sphinxValidate(sql=data) else SERVER_TEXT.PARAM_SQL_TYPE_BD
    #         if   sqlType==SERVER_TEXT.PARAM_SQL_TYPE_BD:     data = BDReadLines    (sql=data)
    #         elif sqlType==SERVER_TEXT.PARAM_SQL_TYPE_SPHINX: data = SphinxReadLines(sql=data)
    #     return data
