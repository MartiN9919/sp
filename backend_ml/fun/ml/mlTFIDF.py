# -*- coding: utf-8 -*-

import os, threading, time, copy

from   tqdm                            import tqdm
from   sklearn.feature_extraction.text import TfidfVectorizer
from   sklearn.metrics.pairwise        import cosine_similarity

from   fun.funSys                      import logger, logError, lstUnique
from   fun.funFile                     import objSave, objLoad

# self.model.fit(docs)
# self.model.vocabulary_            # {'make': 11, 'in': 9, '.': 0, 'the': 19, 'one': 13, ... }
# self.model.get_feature_names())   # ['.', "Don't", 'The', 'Two', 'a', 'all', 'basket', ...]
# vector = self.model.transform(doc)


##########################################################
# TFIDF
##########################################################
# dataSrc - источник данных
#         или функция-генератор данных, или список, или кортеж
#         ((id, doc), ...) или (doc, ...) - id добавляется автоматически (лучше этого избегать: см.ниже)
#         !!! STR SQL - НЕЛЬЗЯ
#         !!! количество данных может быть МЕНЬШЕ len(dataSrc) т.к. при токенизации могут быть короткие строки, которые ПРОПУСКАЮТСЯ
#         поэтому индексы ЛУЧШЕ СТАВИТЬ СВОИ
##########################################################
class TFIDF(object):
    LOG_ID     = 'TFIDF'
    DATA_ID    = 'id'
    DATA_WORDS = 'words'

    def __init__(self,
        fileTF2V     = '',                                                              # путь к файлу модели, если = '' - модель не сохраняется
        dataSrc      = None,                                                            # источник данных
        wordsReplace = None,                                                            # функция-замена words (НЕ ОБЯЗАТЕЛЬНО)
        tokenizer    = None,                                                            # токенизатор
        wordMin      = 1,                                                               # рассматривать только предложения с количеством слов не менее wordMin
        showInfo     = True                                                             # отображать ли инфо о работе на экран, в лог
    ):
        self.fileTF2V     = fileTF2V.strip()
        self.dataSrc      = dataSrc                                                     # отсюда читает данные Thread tfidf2
        self.wordsReplace = wordsReplace
        self.tokenizer    = tokenizer
        self.wordMin      = wordMin
        self.showInfo     = showInfo
        self.isStop       = False                                                       # требование принудительной остановки

        self.blockIni()
        if not self.dataLoad(): self.dataCreate(dataSrc=dataSrc)                        # загрузить данные
        self.model = TfidfVectorizer(                                                   # создать модель
            analyzer      = 'word',
            tokenizer     = lambda x: x,                                                # lambda не сохраняется в pick, надо def dummy_fun(doc): return doc
            preprocessor  = lambda x: x,
            token_pattern = None
            #lowercase    = False,
        )
        # self.model.fit(self.data[self.DATA_WORDS])                                    # обучить модель
        if self.showInfo: logger.info(self.LOG_ID+' INI OK')


    # принудительная остановка
    def stop(self):
        self.isStop = True

    # блокировка обновления данных при работе с потоками
    def blockIni(self): self.block  = 0
    def blockOn(self):  self.block += 1
    def blockOff(self): self.block -= 1
    def blockVer(self): return self.block > 0



    #####################################################
    # ДАННЫЕ: СОЗДАТЬ / СОХРАНИТЬ / ЗАГРУЗИТЬ
    #####################################################
    def dataCreate(self, dataSrc):
        self.data = {self.DATA_ID: [], self.DATA_WORDS: []}
        if dataSrc is None: return

        self.blockOn()
        try:
            if self.showInfo: logger.info(self.LOG_ID+' create '+os.path.basename(self.fileTF2V))

            # проверить/скорректировать dataSrc в src
            if isinstance(dataSrc, (list, tuple)):
                src = copy.deepcopy(dataSrc)
                if len(src)>0:
                    if isinstance(src[0], str):
                        for ind, item in enumerate(src):
                            src[ind] = [ind, item]
            elif hasattr(dataSrc,'__iter__'):
                src = dataSrc
            else:
                raise(self.LOG_ID+' unknow format dataSrc: '+str(src)[:100])

            # сформировать self.data
            for ind, rec in enumerate(tqdm(src, desc=self.LOG_ID+' data', unit='rec') if self.showInfo else src):
                if self.isStop: break
                words = self.docToWords(rec[-1])
                if len(words) < self.wordMin: continue
                self.data[self.DATA_ID   ].append(rec[0] if len(rec)>1 else ind)                    # если нет индекса - создать
                self.data[self.DATA_WORDS].append(words)

            # сохранить self.data
            self.dataSave()
        except Exception as e:
            self.data = {self.DATA_ID: [], self.DATA_WORDS: []}
            raise e
        finally:
            self.blockOff()

    def dataSave(self):
        if self.fileTF2V == '': return
        if self.isStop: return
        if self.showInfo: logger.info(self.LOG_ID+' save '+str(len(self.data[self.DATA_ID]))+' rec')
        objSave(self.data, self.fileTF2V)

    def dataLoad(self):
        if self.fileTF2V == '': return False
        if os.path.exists(self.fileTF2V):
            if self.showInfo: logger.info(self.LOG_ID+' load '+os.path.basename(self.fileTF2V))
            self.data = objLoad(self.fileTF2V)
            return True
        else:
            return False



    #####################################################
    # ДОКУМЕНТ В СЛОВА (ОБРАБОТАННЫЕ)
    #####################################################
    # !!! НЕ ТРЕБУЕТСЯ dataSrc, self.data
    #####################################################
    def docToWords(self, doc):
        words = self.tokenizer.run(doc)
        if not(self.wordsReplace is None): words = self.wordsReplace(words)
        return words




    #####################################################
    # ГРУППИРОВКА СХОЖИХ ТЕКСТОВ (МЕДЛЕННО НА БОЛЬШОМ КОЛИЧЕСТВЕ)
    # НЕ ИСПОЛЬЗУЕТСЯ
    #####################################################
    # data    - ((doc1, text, ...), ...) или (doc1, doc2, ...) list or tuple
    # dataInd - индекс анализируемого столбца
    # simMin  - минимальный коэффициент подобия
    # return  - [0, 1, 0, 1, 2, 2, 2] - номера групп для data
    #####################################################
    # !!! НЕ ТРЕБУЕТСЯ dataSrc, self.data
    #####################################################
    # def groupDataFree(self, data, dataInd=0, simMin=0.2):
    #     w2c = []                                                                                # w2c = [['w2c_22611', 'w2c_294', 'w2c_4021'], ...]
    #     for item in data:
    #         if isinstance(item, (list, tuple)):
    #             item = item[dataInd] if len(item)>0 else ''
    #         w2c.append(self.docToWords(item))

    #     VAL_NONE = -1                                                                           # группа по умолчанию (не определено)
    #     data_len = len(w2c)
    #     ret      = [VAL_NONE] * data_len

    #     igroup   = -1                                                                           # счетчик групп
    #     for ind1 in range(0, data_len):
    #         if ret[ind1] != VAL_NONE: continue                                                  # пропустить если группа уже определена

    #         igroup   += 1                                                                       # новая группа
    #         ret[ind1] = igroup

    #         for ind2 in range(0, data_len):                                                     # сформировать группу из оставшихся элементов
    #             if ret[ind2] != VAL_NONE: continue
    #             if ind1 == ind2: continue

    #             sim = self.simDocsFree(words1=w2c[ind1], words2=w2c[ind2])                      # подобие
    #             if sim >= simMin:
    #                 ret[ind2] = igroup

    #     return ret



    #####################################################
    # ГРУППИРОВКА СХОЖИХ ЗАПИСЕЙ self.data
    #####################################################
    # simMin   - порог признания элемента подобным
    # isUnique - только уникальные записи
    # return   - [id1, id2, ...]        (isUnique=True)
    # return   - [[id1, id2, ...], ...] (isUnique=False)
    #####################################################
    def groupData(self, simMin=0.35, isUnique=True):
        self.blockOn()
        ret = []
        try:
            tfidf   = self.model.fit_transform(self.data[self.DATA_WORDS])                  # искать подобие
            dataLen = len(self.data[self.DATA_WORDS])

            # сформировать groupInd
            groupInd = []                                                                   # [[ind1, ind2, ...], ...], для self.data[self.DATA_WORDS(DATA_ID)][indN]
            for dataInd in range(0, dataLen):                                               # перебрать self.data
                groupIndStep   = []

                sims     = cosine_similarity(tfidf[dataInd], tfidf)[0]                      # список коэффициентов схожести с очередным элементом self.data: [0., 0.555, 1.0, ... ]
                indsSort = sims.argsort()                                                   # отсортированный в порядке убывания схожести список индексов: self.data[self.DATA_WORDS][], sims[]

                for i in range(dataLen-1, -1, -1):                                          # в порядке убывания схожести
                    ind = indsSort[i]                                                       # индекс очередного подобного элемента
                    if ind       == dataInd: continue                                       # пропустить самого себя
                    if sims[ind] <  simMin:    break                                        # так как sims[ind] в порядке убывания
                    groupIndStep.append(ind)

                groupIndStep.insert(0, dataInd)
                groupInd.append(groupIndStep)

            # сформировать результат
            for groupIndItem in groupInd:
                listIDStep = []
                for ind in groupIndItem:
                    listIDStep.append(self.data[self.DATA_ID][ind])
                ret.append(listIDStep)                                                       # ret = [[0, 2], [1, 3], [2, 0], [3, 6, 1], ... ]

            # только уникальные записи
            if isUnique:
                ret_len = dict(map(lambda ind: (self.data[self.DATA_ID][ind], len(self.data[self.DATA_WORDS][ind])), range(0, dataLen)))
                for ind_group, item_group in enumerate(ret):                                # item_group = [0, 2]
                    ind_sel = item_group[0]
                    for ind in item_group:                                                  # ind = 0
                        if ret_len[ind] > ret_len[ind_sel]:
                            ind_sel = ind
                    ret[ind_group] = ind_sel                                                # ret = [1, 2, 2, 3, ... ] - с наибольшим количеством значимых слов
                ret = lstUnique(ret)                                                        # ret = [1, 2, 3, ... ]    - удалить дубликаты

        except Exception as e:
            logError(e)
        finally:
            self.blockOff()
        return ret




    #####################################################
    # СХОЖЕСТЬ ДВУХ ПРОИЗВОЛЬНЫХ ДОКУМЕНТОВ
    #####################################################
    # задавать или docN или wordsN
    #####################################################
    # !!! НЕ ТРЕБУЕТСЯ dataSrc, self.data
    #####################################################
    def simDocsFree(self, doc1=None, doc2=None, words1=None, words2=None):
        if not (doc1 is None): words1 = self.docToWords(doc1)
        if not (doc2 is None): words2 = self.docToWords(doc2)
        if (words1 is None) or (words2 is None): raise Exception('Не задано words')

        tfidf = self.model.fit_transform([words1, words2])
        sim   = ((tfidf * tfidf.T).A)[0,1]
        return round(sim, 2)



    #####################################################
    # НАИБОЛЕЕ СХОЖИЙ ЭЛЕМЕНТ ИЗ self.data ДЛЯ ПРОИЗВОЛЬНОГО ДОКУМЕНТА doc
    #####################################################
    # doc       - текст документа
    # isCorrect - корректировать ли коэф. подобия
    # return    - (self.data[DATA_ID], ПОДОБИЕ (0...1), self.data[DATA_WORDS])
    #####################################################
    def simDoc(self, doc, isCorrect=True):
        self.blockOn()
        try:
            ret      = [-1, -1, None]
            data_len = len(self.data[self.DATA_ID])
            words1   = self.docToWords(doc)
            tfidf    = self.model.fit_transform(self.data[self.DATA_WORDS]+[words1])        # искать подобие в списке, дополненном [words1]
            sims     = cosine_similarity(tfidf[-1], tfidf)[0]                               # список коэффициентов схожести
            indsSort = sims.argsort()                                                       # отсортированный список индексов sims

            if isCorrect:
                for i in range(-2, -5, -1):                                                 # наиболее похожие на [-1] среди [-2][-3][-4]
                    if data_len < -(i+1) : continue
                    ind    = indsSort[i]                                                    # похожий элемент №i: индекс
                    id2    = self.data[self.DATA_ID   ][ind]                                # похожий элемент №i: id в источнике (БД)
                    words2 = self.data[self.DATA_WORDS][ind]                                # похожий элемент №i: список слов (БД)

                    sim12  = sims[ind]                                                      # коэффициент схожести 1 с 2
                    sim21  = self.simDocsFree(words1=words1, words2=words2)                 # коэффициент схожести 2 с 1

                    sim    = self.simCorrect(sim12, sim21, len(words1), len(words2))        # коррекция
                    if sim > ret[1]: ret = [id2, sim, words2]                               # запомнить лучший результат

            else:
                if data_len > 0:
                    ind = indsSort[-2]
                    id2    = self.data[self.DATA_ID   ][ind]
                    words2 = self.data[self.DATA_WORDS][ind]
                    sim    = sims[ind]
                    ret    = [id2, sim, words2]

        except Exception as e:
            logError(e)
        finally:
            self.blockOff()
        return ret[0], float(round(ret[1], 2)), ret[2]                                      # float т.к. round возвращает 'numpy.float64', а np может не быть на клиенте



    #####################################################
    # КОРРЕКЦИЯ КОЭФФИЦИЕНТА ПОДОБИЯ
    #####################################################
    # simN - коэффициент подобия
    # lenN - количество слов
    #####################################################
    def simCorrect(self, sim12, sim21, wordsCount1, wordsCount2):
        def simCorrectStep(sim, wordsCount):
            '''
            |
        1   |--+     -------------
            |  |    /
        Y   |  |---/          1-DY
            |  |  /|
            |  | / | Y-DY
        DY  |  +---+--------------
            |   X-DX
            |    X_MAX-DX
            +--------+------------
            0 DX

            1-DY        Y-DY
            --------- = ----
            X_MAX-DX    X-DX

            X     - wordsCount
            Y     - понижающий коэффициент
            Y*sim - cкорректированный коэффициент подобия
            '''
            DX    = 1
            DY    = 0.6
            X_MAX = 7
            if (wordsCount >= (X_MAX-DX)) or (sim >= 0.9): return sim
            return (((wordsCount-DX) * (1-DY) / (X_MAX-DX)) + DY) * sim

        #####################################################
        sim12  = simCorrectStep(sim12, wordsCount1)                                         # понизить коэффициент схожести для коротких текстов
        sim12  = simCorrectStep(sim12, wordsCount2)
        sim21  = simCorrectStep(sim21, wordsCount1)
        sim21  = simCorrectStep(sim21, wordsCount2)
        #sim   = max(sim12, sim21)                                                          # коэффициент схожести максимальный
        #sim   = min(sim12, sim21)                                                          # коэффициент схожести минимальный
        sim    = (sim12 + sim21) / 2.0                                                      # коэффициент схожести средний
        return sim




##########################################################
# TFIDF ОБНОВЛЕНИЯ ДАННЫХ (САМОСТОЯТЕЛЬНЫЙ ПОТОК)
##########################################################
class TFIDFThread(threading.Thread):
    def __init__(self, tfidf1, funDelay, **options):
        threading.Thread.__init__(self)
        self.tfidf1         = tfidf1
        self.funDelay       = funDelay
        self.options        = options
        self.isStop         = False                                                 # требование принудительной остановки

    def run(self):
        logger.info('Running the background branch tfidf')
        self.options['showInfo'] = False                                             # отключить вывод инфо
        self.tfidf2 = TFIDF(**self.options)                                          # создать ВТОРОЙ экземпляр для фонового обновления
        self.sleep(self.funDelay())
        while not self.isStop:
            try:
                delayNext = self.funDelay()
                timeStart = time.time()                                             # время начала текущего цикла
                timeNext  = timeStart+delayNext                                     # время начала следующего цикла

                self.tfidf2.dataCreate(dataSrc=self.tfidf1.dataSrc)                 # построить данные из источника первой модели
                while ((not self.dataRefresh()) and (not self.isStop)): pass        # [ждать отмены блокировки], [ждать требования остановки], обновить данные в первом TFIDF

            except (KeyboardInterrupt, SystemExit):
                self.isStop = True

            except Exception as e:
                logError(e)

            finally:
                if 'timeNext' in locals():
                    self.sleep(timeNext-time.time())


    def stop(self):
        self.isStop = True
        if hasattr(self, 'tfidf2'): self.tfidf2.stop()                           # обязательно if так как при работе с TFIDFManage метод может быть уже уничтожен


    def sleep(self, sec, step=0.5):
        while ((sec > 0) and (not self.isStop)):
            time.sleep(step)
            sec -= step

    def dataRefresh(self):
        if self.tfidf1.blockVer(): return False                                        # если блокировка включена, то отвергаем изменения данных
        self.tfidf1.data = self.tfidf2.data
        logger.info('New tfidf.data has been applied')
        return True





##########################################################
# TFIDF MANAGE
##########################################################
# TFIDFManage(TFIDF1) -> TFIDFThread -> TFIDF2
# TFIDF1 1-й экземпляр - рабочий
# TFIDF2 2-й экземпляр - для фонового обновления данных
##########################################################
class TFIDFManage(TFIDF):
    def __init__(self, **options):
        logger.info('Running the main branch tfidf')
        super().__init__(**options)                                             # запуск основного экзземпляра

        self.thread = TFIDFThread(tfidf1=self, funDelay=self.funDelay, **options)
        #self.daemon = True
        self.thread.start()

    def stop(self):
        super().stop()
        self.thread.stop()
        self.thread.join()

    def funDelay(self):
        return 60*3
