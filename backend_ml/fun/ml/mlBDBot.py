# -*- coding: utf-8 -*-

import random
from   tqdm            import tqdm

from   fun.funConst    import ARC, MSG, ML_BOT, ML_BOT_TYPE
from   fun.funBD       import bdConnect, bdDisconnect, bdSQL, BDReadLines
from   fun.funSys      import logger, sqlDateTimeNow, getMD5
from   fun.funText     import textNormal, textWithoutObj


#####################################################
# РАБОТА С ML_BOT
#####################################################
class MLBDBot():
    def __init__(self):
        logger.info('OK ML-bot')

    ##########################################################
    # ПРОЧИТАТЬ СЛУЧАЙНЫЙ ОТВЕТ ИЗ БД
    ##########################################################
    def getAnswer(self, recID, max_id=0):
        sql = \
            "SELECT t2."+ML_BOT.QUESTION+", t2."+ML_BOT.ANSWER+" "+\
            "FROM "+ML_BOT.TABLE+" as t1 INNER JOIN "+ML_BOT.TABLE+" as t2 "+\
            "ON t1."+ML_BOT.QUESTION+"=t2."+ML_BOT.QUESTION+" "+\
            "WHERE t1."+ML_BOT.ID+"="+str(recID)+\
            ((" AND t2."+ML_BOT.ID+"<="+str(max_id)) if max_id > 0 else "")
        try:
            val = random.choice(bdSQL(sql, wait=True, read=True))
            if len(val)==0: val = ('', '')
        except:
            val = ('', '')
            logger.warning('Not found rec with id: '+str(recID))
        return val[1], val[0]



    ##########################################################
    # ДОБАВИТЬ ЗАПИСЬ
    ##########################################################
    def addRec(self, bot_type=ML_BOT_TYPE.ID_COMMON, question='', answer='', host='', author_id='', dat=None, db=-1):
        question = textNormal(textWithoutObj(question))
        answer   = textNormal(textWithoutObj(answer  ))
        if (question in ['', MSG.NO_TEXT]) or (answer in ['', MSG.NO_TEXT]): return False
        if dat is None: dat = sqlDateTimeNow()

        sql = "INSERT IGNORE "+ML_BOT.TABLE+" SET "+\
            ML_BOT.TYPE_ID  +"=" +str(bot_type)+", "+\
            ML_BOT.CRC      +"='"+getMD5(str(bot_type)+question+answer)+"', "+\
            ML_BOT.QUESTION +"='"+question     +"', "+\
            ML_BOT.ANSWER   +"='"+answer       +"', "+\
            ML_BOT.HOST     +"='"+host         +"', "+\
            ML_BOT.AUTHOR_ID+"='"+author_id    +"', "+\
            ML_BOT.DATE     +"='"+str(dat)     +"'"
        bdSQL(sql=sql, wait=True, read=False, db=db)
        return True



    ##########################################################
    # ИМПОРТ ВАРИАНТОВ ОТВЕТА
    ##########################################################
    # importRec(host=HOST.TALKS, author_id='95735', date_from='2018-01-01')
    ##########################################################
    def importRec(self, host, author_id, date_from='', table=ARC.TABLE_REP, bot_type=ML_BOT_TYPE.ID_COMMON):
        print(host, author_id, date_from, table)
        db = bdConnect()
        for rec in tqdm(BDReadLines(
            sql=
                "SELECT "+\
                    ARC.TITLE_NAME+", "+\
                    ARC.CONTENT   +", "+\
                    ARC.HOST      +", "+\
                    ARC.AUTHOR_ID +", "+\
                    ARC.DATE      +" " +\
                "FROM "  +table   +" " +\
                "WHERE " +\
                    ((ARC.DATE+" >= '" +date_from+"' AND ") if date_from!='' else '')+\
                    ARC.HOST     +"='"+host     +"' AND "+\
                    ARC.AUTHOR_ID+"='"+author_id+"'"
            ),
            desc='MlBot.importArc',
            unit='rec'
        ):

            self.addRec(
                bot_type  = ML_BOT_TYPE.ID_COMMON,
                question  = rec[0],
                answer    = rec[1],
                host      = rec[2],
                author_id = rec[3],
                dat       = rec[4],
                db        = db,
            )

        bdDisconnect(db)
        print('OK')


    ##########################################################
    # УДАЛИТЬ ЗАПИСИ-ДУБЛИКАТЫ
    ##########################################################
    # def delClone(self, db=-1):
    #     sql =\
    #         "DELETE t1 "+\
    #         "FROM "+ML_BOT.TABLE+" t1 "+\
    #         "JOIN ("+\
    #             "SELECT MAX("+ML_BOT.TYPE_ID+") AS "+ML_BOT.TYPE_ID+" "+\
    #             "FROM "+ML_BOT.TABLE+" "+\
    #             "GROUP BY "+ML_BOT.QUESTION+", "+ML_BOT.ANSWER+" "+\
    #             "HAVING COUNT(*) > 1) t2 "+\
    #         "USING("+ML_BOT.TYPE_ID+")"
    #     bdSQL(sql=sql, wait=True, read=False, db=db)

