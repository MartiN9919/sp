# -*- coding: utf-8 -*-

from   fun.funConst           import ML_BOT, ARC
from   fun.funSys             import logger, logError, logging, dictRemoveKey
from   fun.funBD              import BDReadLines

from   fun.ml.mlPHRASES       import PHRASES
from   fun.ml.mlW2V           import W2V
from   fun.ml.mlW2C           import W2C, W2C_TYPES
from   fun.ml.mlD2V           import D2V
from   fun.ml.mlTFIDF         import TFIDF, TFIDFManage
from   fun.ml.mlText          import Tokenizer
from   fun.ml.mlFun           import File2Sentences
from   fun.ml.mlBDBot         import MLBDBot


##################################################################
# src
# .csv: [[word, word, ...], ...]
##################################################################
# d2v
# ML_BOT.TABLE.QUESTION ==fit==> [[word, word, ...], ...] OR
#                       ==fit==> [[key,  key,  ...], ...]
# text ==textToDocVec==>
##################################################################

# ВАЖНО !!! задать PATH_LIB при инициализации !!!
class VAR:
    VEC_SIZE             = 300                                          # размер векторов between 100 and 1,000 [100]
    CLUSTERS             = 50000                                        # количество кластеров
    REC_SRC              = 0                                            # записей из SRC(CSV):     0 - без ограниченний
    REC_SRC_PHRASES      = 2000000                                      # записей из SRC(CSV):     0 - без ограниченний
    REC_BOT_COUNT        = 0                                            # записей из ATLAS.ML_BOT: 0 - без ограниченний
    REC_BOT_ID           = 0                                            # максимальный ID записей из ATLAS.ML_BOT: 0 - без ограниченний (не путать с количеством обрабатываемых записей) (mlBot)
    WORD_LIMIT           = 50                                           # количество слов в каждом предложении

    # УДАЛИТЬ
    # REC_SRC            = 500
    # CLUSTERS           = 25000
    REC_BOT_ID           = 304542

    PATH_LIB             = ''                                           # ВАЖНО !!! задать при инициализации !!!
    PATH_PREF            = 'arc'
    PATH_COUNT           = '_src22m'                                    # '_src22m' '_src20m' '_src10t'
    PATH_REC_SRC         = (('_recSrc'     +str(REC_SRC        )) if REC_SRC         > 0 else '')
    PATH_REC_SRC_PHRASES = (('_recSrc'     +str(REC_SRC_PHRASES)) if REC_SRC_PHRASES > 0 else '')
    PATH_REC_BOT         = (('_recBotCount'+str(REC_BOT_COUNT  )) if REC_BOT_COUNT   > 0 else '')+\
                           (('_recBotID'   +str(REC_BOT_ID     )) if REC_BOT_ID      > 0 else '')



##################################################################
# ИСТОЧНИК ДАННЫХ: ML_BOT
##################################################################
class SrcMlBot_(BDReadLines):
    def __init__(self, data_type=1, data_limit=0, max_id=0):
        super().__init__(
            sql =
                'SELECT '+\
                    'MIN('+ML_BOT.ID+'), '+\
                    ML_BOT.QUESTION+' '+\
                'FROM '    +ML_BOT.TABLE+' '+\
                'WHERE '   +ML_BOT.TYPE_ID+'='+str(data_type)+' '+\
                    (('AND '+ML_BOT.ID+'<='+str(max_id)+' ') if max_id > 0 else '')+\
                'GROUP BY '+ML_BOT.QUESTION+\
                (' LIMIT '+str(data_limit) if data_limit > 0 else '')
        )
class SrcMlBot(SrcMlBot_):
    def __init__(self):
        super().__init__(data_type=1, data_limit=VAR.REC_BOT_COUNT, max_id=VAR.REC_BOT_ID)



##################################################################
# PHRASES
##################################################################
# options: tokenizer
##################################################################
class _PHRASES_(PHRASES):
    def __init__(self, **options):
        self.MIN_COUNT  = 5                                             # [5]  игнорировать все слова и биграммы с общим количеством ниже этого значения
        self.THREESHOLD = 10                                            # [10] большее значение - меньше фраз
        self.VOCAB_SIZE = 100000000                                     # [40000000] 40M - 3,6Gb
        self.tokenizer  = options['tokenizer']
        self.PATH_SRC   = \
            VAR.PATH_LIB+\
            'src/'+\
            VAR.PATH_PREF+\
            VAR.PATH_COUNT+\
            '.csv'

        self.PATH      = \
            VAR.PATH_LIB+\
            'phrases/'+\
            VAR.PATH_PREF+\
            VAR.PATH_COUNT +\
            '_wordMax'   +str(VAR.WORD_LIMIT   )+\
            '_minCount'  +str(self.MIN_COUNT )+\
            '_threeshold'+str(self.THREESHOLD)+\
            self.tokenizer.PATH+\
            VAR.PATH_REC_SRC_PHRASES+\
            '.bin'

        options['filePhrases'] = self.PATH
        options['dataSrc']     = File2Sentences(file=self.PATH_SRC, encoding='utf-8', tokenizer=self.tokenizer, wordLimit=VAR.WORD_LIMIT, recLimit=VAR.REC_SRC_PHRASES)
        options['min_count']   = self.MIN_COUNT
        options['threshold']   = self.THREESHOLD
        options['vocab_size']  = self.VOCAB_SIZE
        options = dictRemoveKey(options, 'tokenizer')

        super().__init__(**options)



##################################################################
# ТОКЕНИЗАТОР
##################################################################
class _Tokenizer_(Tokenizer):
    def __init__(self):
        self.LOWER            = True                            # привести к нижнему регистру
        self.NORMAL           = True                            # обработка текста как в loader-ах
        self.PUNKT            = True                            # убрать пунктуацию
        self.STOPW            = True                            # убрать стоп-слова
        self.STEM             = True                            # выделить стеммы
        self.PATH             = \
            ('L' if self.LOWER  else '')+\
            ('N' if self.NORMAL else '')+\
            ('P' if self.PUNKT  else '')+\
            ('W' if self.STOPW  else '')+\
            ('S' if self.STEM   else '')
        if self.PATH != '': self.PATH = '_'+self.PATH

        super().__init__(
            isLower        = self.LOWER,
            isNormalize    = self.NORMAL,
            delPunctuation = self.PUNKT,
            delStopWords   = self.STOPW,
            isStemming     = self.STEM
        )



##################################################################
# ТОКЕНИЗАТОР PHRASES
##################################################################
class _TokenizerPhrases_(_Tokenizer_):
    def __init__(self, **options):
        super().__init__(**options)
        self.ph = _PHRASES_(tokenizer=self)                     # инициализация _PHRASES_ работает с ОРИГИНАЛЬНЫМ токанайзером

    run = lambda self, doc: self.ph.run(super().run(doc)) if hasattr(self, 'ph') else super().run(doc)




##################################################################
# WORD2VEC
##################################################################
class _W2V_(W2V):
    def __init__(self, tokenizer):
        self.WORD_MIN  = 10                                     # рассматривать только слова, которые встречаются не менее раз [5], 30
        self.PATH_SRC  = \
            VAR.PATH_LIB+\
            'src/'+\
            VAR.PATH_PREF+\
            VAR.PATH_COUNT+\
            '.csv'
        self.PATH      = \
            VAR.PATH_LIB+\
            'w2v/'+\
            VAR.PATH_PREF+\
            VAR.PATH_COUNT +\
            '_vecSize'+str(VAR.VEC_SIZE)+\
            '_wordMin'+str(self.WORD_MIN)+\
            '_wordMax'+str(VAR.WORD_LIMIT)+\
            tokenizer.PATH+\
            VAR.PATH_REC_SRC+\
            '.bin'

        super().__init__(
            fileW2V        = self.PATH,
            dataSrc        = File2Sentences(file=self.PATH_SRC, encoding='utf-8', tokenizer=tokenizer, wordLimit=VAR.WORD_LIMIT, recLimit=VAR.REC_SRC),
            tokenizer      = tokenizer,
            embed_size     = VAR.VEC_SIZE,
            wordMin        = self.WORD_MIN
        )



##################################################################
# WORD2CLUSTER
##################################################################
class _W2C_(W2C):
    def __init__(self, w2v):
        self.tokenizer = w2v.tokenizer
        self.TYPE      = W2C_TYPES.MINI_BATCH_KMEANS
        self.CLUSTERS  = VAR.CLUSTERS
        self.PATH      = \
            VAR.PATH_LIB+\
            'w2c/'+\
            VAR.PATH_PREF+\
            VAR.PATH_COUNT+\
            '_type'+str(self.TYPE    )+\
            '_clst'+str(self.CLUSTERS)+\
            VAR.PATH_REC_SRC+\
            '.w2c'

        super().__init__(
            fileW2C        = self.PATH,
            modelType      = self.TYPE,
            clustersCount  = self.CLUSTERS,
            w2v            = w2v
        )



##################################################################
# DOC2VEC
##################################################################
# w2v - нормальная работа
# или
# w2c - слова меняются на key-word кластеров
# data_src - источник данных: (id, text)
# fileD2V - путь к файлу модели, если = '' - модель не сохраняется
##################################################################
class _D2V_(D2V):
    def __init__(self, w2v=None, w2c=None, data_src=SrcMlBot(), fileD2V=None):
        self.w2v         = w2v
        self.w2c         = w2c
        if (w2v is None) and (not (w2c is None)): self.w2v = self.w2c.w2v
        self.tokenizer   = self.w2v.tokenizer
        self.embed_size  = self.w2v.embed_size
        self.EPOCH       = 200
        self.WORD_MIN    = 2                                  # рассматривать только предложения с количеством слов не менее wordMin
        self.WINDOW      = 2
        self.DM          = 0
        self.DBOW_WORDS  = 1
        self.PATH        = \
            (VAR.PATH_LIB+\
            'd2v/'+\
            VAR.PATH_PREF+\
            VAR.PATH_COUNT+\
            ('_wordText' if w2c is None else ('_wordCluster'+str(VAR.CLUSTERS)))+\
            '_vecSize'+str(self.embed_size)+\
            '_epoch'  +str(self.EPOCH   )+\
            '_wordMin'+str(self.WORD_MIN)+\
            '_window' +str(self.WINDOW  )+\
            '_dm'     +str(self.DM      )+\
            self.tokenizer.PATH+\
            VAR.PATH_REC_SRC+\
            VAR.PATH_REC_BOT+\
            '.bin') if fileD2V is None else fileD2V

        super().__init__(
            fileD2V        = self.PATH,
            dataSrc        = data_src,
            wordsReplace   = self.wordsReplace,
            tokenizer      = self.tokenizer,
            embed_size     = self.embed_size,
            epoch          = self.EPOCH,
            wordMin        = self.WORD_MIN,
            window         = self.WINDOW,
            dm             = self.DM,
            dbow_words     = self.DBOW_WORDS
        )


    # ЗАМЕНА СЛОВ ПРИ КЛАСТЕРИЗАЦИИ
    wordsReplace = lambda self, words: words if (self.w2c is None) else self.w2c.wordsToKeys(words)



##################################################################
# TFIDF
##################################################################
# TFIDF       - без автоматического обновления
# TFIDFManage - с   автоматическим  обновлением
# w2v - нормальная работа
# или
# w2c - слова меняются на key-word кластеров
# data_src - источник данных: (id, text)
# fileTF2V - путь к файлу модели, если = '' - модель не сохраняется
##################################################################
class _TFIDF_(TFIDFManage):
    def __init__(self, w2v=None, w2c=None, data_src=SrcMlBot(), fileTF2V=None):
        self.w2v         = w2v
        self.w2c         = w2c
        if (w2v is None) and (not (w2c is None)): self.w2v = self.w2c.w2v
        self.tokenizer   = self.w2v.tokenizer
        self.embed_size  = self.w2v.embed_size
        self.WORD_MIN    = 1                                  # рассматривать только предложения с количеством слов не менее wordMin
        self.PATH        = \
            (VAR.PATH_LIB+\
            'tfidf/'+\
            VAR.PATH_PREF+\
            VAR.PATH_COUNT+\
            ('_wordText' if w2c is None else ('_wordCluster'+str(VAR.CLUSTERS)))+\
            '_vecSize'+str(self.embed_size)+\
            '_wordMin'+str(self.WORD_MIN)+\
            self.tokenizer.PATH+\
            VAR.PATH_REC_SRC+\
            VAR.PATH_REC_BOT+\
            '.tfidf') if fileTF2V is None else fileTF2V

        super().__init__(
            fileTF2V       = self.PATH,
            dataSrc        = data_src,
            wordsReplace   = self.wordsReplace,
            tokenizer      = self.tokenizer,
            wordMin        = self.WORD_MIN
        )


    # ЗАМЕНА СЛОВ ПРИ КЛАСТЕРИЗАЦИИ
    wordsReplace = lambda self, words: words if (self.w2c is None) else self.w2c.wordsToKeys(words)


##################################################################
# BOT
##################################################################
# работа с ботом на основе модели TFIDF, ПАРАМЕТРЫ КАК ДЛЯ TFIDF_
##################################################################
class BOT_TFIDF(object):
    def __init__(self, **options):
        self.mlbdBot = MLBDBot()
        self.tfidf   = _TFIDF_(**options)

    def __del__(self):
        self.stop()

    def stop(self):
        if hasattr(self, 'tfidf'): self.tfidf.stop()



    def getAnswer(self, quest):
        # подобный вопрос (тексты вопросов в памяти не хранятся)
        quest2_id, quest2_sim, _ = self.tfidf.simDoc(doc=quest)
        if quest2_id < 0: return ''

        # случайный ответ и текст вопроса
        answer, quest2_txt = self.mlbdBot.getAnswer(recID=quest2_id, max_id=VAR.REC_BOT_ID)
        # print('Подобие ('+str(quest2_sim)+'):', quest2_txt)
        # print(str(self.tfidf.docToWords(quest))+'\n'+str(self.tfidf.docToWords(quest2_txt)))
        if quest2_sim < 0.30: answer, quest2_txt = ('', '')

        # logger.info('(: '+quest+' / '+answer)
        return answer

    def addRec(self, quest, answer, host='', author_id=''):
        ret = self.mlbdBot.addRec(
            question  = quest,
            answer    = answer,
            host      = host,
            author_id = author_id,
        )
        if ret: logger.info('bot add: '+quest+' / '+answer+' / '+author_id)
        return ret

    def importRec(self, host='', author_id='', date_from=''):
        self.mlbdBot.importRec(table=ARC.TABLE,     host=host, author_id=author_id, date_from=date_from)
        self.mlbdBot.importRec(table=ARC.TABLE_REP, host=host, author_id=author_id, date_from=date_from)
