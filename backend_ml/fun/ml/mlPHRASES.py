# -*- coding: utf-8 -*-

import os

from   tqdm                            import tqdm
from   gensim.models.phrases           import Phrases, Phraser

from   fun.funSys                      import logger, logError
from   fun.funFile                     import extSet


##########################################################
# PHRASES
##########################################################
class PHRASES(object):
    LOG_ID     = 'PHRASES'

    def __init__(self,
        filePhrases,                                                                    # путь к файлу модели (расширение меняется)
        dataSrc      = None,                                                            # функция-генератор данных: ((id, [words]), ...)
        min_count    = 5,                                                               # [5]  игнорировать все слова и биграммы с общим количеством ниже этого значения
        threshold    = 10,                                                              # [10] большее значение - меньше фраз
        vocab_size   = 40000000,                                                        # [40000000] 40M - 3,6Gb
    ):
        filePhrases2 = extSet(filePhrases, 'bin2')
        filePhrases3 = extSet(filePhrases, 'bin3')
        filePhrases4 = extSet(filePhrases, 'bin4')
        isLoad = os.path.exists(filePhrases2) and \
                 os.path.exists(filePhrases3) and \
                 os.path.exists(filePhrases4)

        # загрузить
        if isLoad:
            logger.info(self.LOG_ID+' load')
            self.model2 = Phraser.load(filePhrases2)
            self.model3 = Phraser.load(filePhrases3)
            self.model4 = Phraser.load(filePhrases4)

        # создать
        else:
            logger.info(self.LOG_ID+' create')

            try:
                param = {
                    'min_count'      : min_count,
                    'threshold'      : threshold,
                    'max_vocab_size' : vocab_size,
                }

                logger.info(self.LOG_ID+' phrases model2')
                self.model2 = Phrases(sentences = tqdm(dataSrc,              desc=self.LOG_ID+' model2', unit='rec'), **param)
                logger.info(self.LOG_ID+' phrases model3')
                self.model3 = Phrases(sentences = tqdm(self.model2[dataSrc], desc=self.LOG_ID+' model3', unit='rec'), **param)
                logger.info(self.LOG_ID+' phrases model4')
                self.model4 = Phrases(sentences = tqdm(self.model3[dataSrc], desc=self.LOG_ID+' model4', unit='rec'), **param)

                logger.info(self.LOG_ID+' phraser 2')
                self.model2 = Phraser(self.model2)
                logger.info(self.LOG_ID+' phraser 3')
                self.model3 = Phraser(self.model3)
                logger.info(self.LOG_ID+' phraser 4')
                self.model4 = Phraser(self.model4)

                logger.info(self.LOG_ID+' save')
                self.model2.save(filePhrases2)
                self.model3.save(filePhrases3)
                self.model4.save(filePhrases4)

            except Exception as e:
                logError(e)
                raise('Ошибка инициализации')

        logger.info(self.LOG_ID+' INI OK')


    run = lambda self, words: self.model2[self.model3[self.model4[words]]]
