# -*- coding: utf-8 -*-

import os, random

from   tqdm                            import tqdm
from   gensim.models.doc2vec           import Doc2Vec, TaggedDocument

from   fun.funSys                      import logger
from   fun.funFile                     import extSet, objSave, objLoad



##########################################################
# DOC2VEC
##########################################################
# ДЛЯ БОЛЬШОГО КОЛИЧЕСТВА ДОКУМЕНТОВ (2000 МАЛО, ЗАВИСИТ ОТ ИХ ДЛИНЫ)
# для повышения точности:
#     увеличить кол-во интерация для infer_vector
#     уменьшить window
##########################################################
# d2v.docToSimilarDocID(doc)
# d2v.docToDocVec(doc)
# d2v.vecDocToSimilarDocID(docVec)
# d2v.docToWords(doc)
# d2v.docIDToWords(docID)
# d2v.most_similar(vec, topn=1)
##########################################################
# new_sentences = ['moscow', 'weather', 'cold']
# d2v.model.build_vocab(new_sentences, update=True)
# d2v.model.train(new_sentences)
##########################################################
class D2V(object):
    def __init__(self,
        fileD2V      = '',                                                              # путь к файлу модели, если = '' - модель не сохраняется
        dataSrc      = None,                                                            # функция-генератор данных: ((id, [words]), ...)
        wordsReplace = None,                                                            # функция-замена words (НЕ ОБЯЗАТЕЛЬНО)
        tokenizer    = None,                                                            # токенизатор
        embed_size   = 300,                                                             # размер векторов
        epoch        = 200,                                                             # количество эпох
        wordMin      = 1,                                                               # рассматривать только предложения с количеством слов не менее wordMin
        window       = 2,                                                               # размер окна
        dm           = 0,                                                               # 0 - PV-DBOW
        dbow_words   = 1                                                                # dm=0 dbow_words=0 - не использует векторы слов
    ):
        self.LOG_ID       = 'D2V'
        self.model        = None
        self.wordsReplace = wordsReplace
        self.tokenizer    = tokenizer
        self.embed_size   = embed_size
        fileD2V           = fileD2V.strip()
        fileSrc           = extSet(fileD2V, 'dat') if fileD2V!='' else ''               # путь к файлу с исходными данными (меняем расширение)
        #self.vectors     = self.docvecs.doctag_syn0

        ##########################################################
        # ИНИЦИАЛИЗАЦИИЯ ДАННЫХ
        ##########################################################
        # данные: загрузить
        if os.path.exists(fileSrc):
            logger.info(self.LOG_ID+' load '+os.path.basename(fileSrc))
            self.data = objLoad(fileSrc)

        # данные: создать
        else:
            logger.info(self.LOG_ID+' data create '+os.path.basename(fileSrc))
            self.data = []
            for rec in tqdm(dataSrc, desc=self.LOG_ID+' data', unit='rec'):
                words = self.docToWords(rec[1])
                if len(words) < wordMin: continue
                self.data.append(TaggedDocument(words=words, tags=[rec[0]]))

            if fileSrc != '':
                logger.info(self.LOG_ID+' data save')
                objSave(self.data, fileSrc)


        ##########################################################
        # ИНИЦИАЛИЗАЦИЯ МОДЕЛИ
        ##########################################################
        # модель: загрузить
        if os.path.exists(fileD2V):
            logger.info(self.LOG_ID+' model load '+os.path.basename(fileD2V))
            self.model = Doc2Vec.load(fileD2V)

        # модель: создать
        else:
            logger.info(self.LOG_ID+' model create '+os.path.basename(fileD2V))

            self.model = Doc2Vec(
                vector_size = self.embed_size,
                window      = window,
                min_count   = wordMin,
                dm          = dm,
                dbow_words  = dbow_words,
                sample      = 0,
                negative    = 5,
                alpha       = 0.025,
                min_alpha   = 0.00025,
                # dm_concat = 0,
                hs          = 0)
            #Doc2Vec(dm = 1, min_count=1, window=10, size=150, sample=1e-4, negative=10)
            self.model.build_vocab(self.data)
            for epoch_item in tqdm(range(epoch), desc=self.LOG_ID+' model', unit='ep'):
                self.model.train(self.data, total_examples=self.model.corpus_count, epochs=self.model.iter)
                self.model.alpha    -= 0.0002
                self.model.min_alpha = self.model.alpha
                random.shuffle(self.data)
            #self.model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)

            if fileD2V != '':
                logger.info(self.LOG_ID+' model save')
                self.model.save(fileD2V)

        logger.info(self.LOG_ID+' INI OK')



    #####################################################
    # ДОКУМЕНТ В ID НАИБОЛЕЕ ПОХОЖЕГО ДОКУМЕТА, ВТОРОЙ ПАРАМЕТР - ВЕРОЯТНОСТЬ
    #####################################################
    def docToSimilarDocID(self, doc):
        docVec = self.docToDocVec(doc)
        return self.vecDocToSimilarDocID(docVec)


    #####################################################
    # ДОКУМЕНТ В ВЕКТОР ДОКУМЕНТА
    #####################################################
    def docToDocVec(self, doc):
        words = self.docToWords(doc)
        return self.model.infer_vector(doc_words=words, steps=self.EPOCH*10, alpha=0.025, min_alpha=0.00025)    # ?passes=5


    #####################################################
    # ВЕКТОР ДОКУМЕНТА В ID НАИБОЛЕЕ ПОХОЖЕГО ДОКУМЕТА, ВТОРОЙ ПАРАМЕТР - ВЕРОЯТНОСТЬ
    #####################################################
    def vecDocToSimilarDocID(self, docVec):
        rec = self.most_similar(docVec)[0]
        return rec[0], rec[1]


    #####################################################
    # ДОКУМЕНТ В СЛОВА (ОБРАБОТАННЫЕ)
    #####################################################
    def docToWords(self, doc):
        words = self.tokenizer.run(doc)
        if not(self.wordsReplace is None): words = self.wordsReplace(words)
        return words


    #####################################################
    # ID ДОКУМЕНТА В СПИСОК СЛОВ ДОКУМЕНТА (ОБРАБОТАННЫХ)
    #####################################################
    def docIDToWords(self, docID):
        words = []
        for item in self.data:
            if item.tags[0]==docID:
                words = item.words
                break
        return words


    #####################################################
    # СОКРАЩЕННАЯ ФОРМА
    #####################################################
    most_similar = lambda self, vec, topn=1: self.model.docvecs.most_similar(positive=[vec], topn=topn)
