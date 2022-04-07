# -*- coding: utf-8 -*-

import os
import numpy as np

from   sklearn.cluster                 import KMeans, MiniBatchKMeans               # http://scikit-learn.org/stable/modules/clustering.html

from   fun.funSys                      import logger
from   fun.funFile                     import extSet, objSave, objLoad



##########################################################
# WORD2CLUSTER
##########################################################
# w2c.docToDoc(doc)                     # [None] - ошибка
# w2c.wordsToKeys(words)                # [None] - ошибка
# w2c.wordToKey(word)                   # [None] - ошибка
# w2c.wordsToClusters(words)            # [None] - ошибка
# w2c.wordToCluster(word)               # [None] - ошибка
# w2c.clusterToWords(cluster)           # [None] - ошибка
# w2c.clusterToKey(cluster)             # [None] - ошибка
##########################################################
# text    - необработанный текст (строка)
# word    - слово (обработанное токенизатором)
# key     - ключевое слово, первое слово кластера
# cluster - номер кластера (int)
##########################################################
# print(w2c.model.cluster_centers_)
# print(w2c.model.labels_)
# clusters = w2c.model.labels_.tolist()
# w2c.model.fit_predict(vectors)
##########################################################
class W2C_TYPES:
    MINI_BATCH_KMEANS = 1
    KMEANS            = 2

class W2C(object):
    def __init__(self,
            fileW2C,                                                                    # путь к файлу модели
            modelType     = W2C_TYPES.MINI_BATCH_KMEANS,                                # тип кластеризации
            clustersCount = 10000,                                                      # количество кластеров
            w2v           = None                                                        # модель word2vec
        ):
        self.LOG_ID       = 'W2C'
        self.STR_CLUSTER  = 'w2c_'
        self.w2v          = w2v
        self.vectors      = w2v.model.wv.syn0                                           # d2v.docvecs.doctag_syn0
        self.tokenizer    = w2v.tokenizer

        # модель: загрузить
        if os.path.exists(fileW2C):
            logger.info(self.LOG_ID+' load '+os.path.basename(fileW2C))
            self.word2cluster = objLoad(fileW2C)

        # модель: создать
        else:
            logger.info(self.LOG_ID+' create '+os.path.basename(fileW2C))

            if modelType == W2C_TYPES.MINI_BATCH_KMEANS:
                model = MiniBatchKMeans(
                    n_clusters           = clustersCount,                               # количество кластеров [8]
                    init                 = 'k-means++',                                 # способ выбора начальных центров ['k-means++']
                    batch_size           = clustersCount*20,
                    random_state         = np.random.RandomState(0),                    # [None]
                    reassignment_ratio   = 0, #10**-4,
                    max_no_improvement   = 30                                           # [10]
                )
            elif modelType == W2C_TYPES.KMEANS:
                model = KMeans(
                    n_clusters           = clustersCount,                               # количество кластеров [8]
                    max_iter             = 150,                                         # максимальное количество итераций [300]
                    init                 = 'k-means++',                                 # способ выбора начальных центров ['k-means++']
                    random_state         = np.random.RandomState(0),                    # [None]
                    precompute_distances = False                                        # отключить предварительный расчет дистанций: меньше памяти, больше времени ['auto']
                )
            else:
                raise('Тип модели ['+str(modelType)+'] не поддерживается')

            model.fit(self.vectors)

            logger.info(self.LOG_ID+' dictionary')
            clusters = model.predict(self.vectors)                                      # список: кластер для КАЖДОГО слова
            self.word2cluster = dict(zip(w2v.model.wv.index2word, clusters))            # словарь соответствия каждого слова номеру кластера

            logger.info(self.LOG_ID+' save '+os.path.basename(fileW2C))
            objSave(self.word2cluster, fileW2C)

        logger.info(self.LOG_ID+' INI OK')



    #####################################################
    # ЗАПОЛНИТЬ ПУСТЫЕ ЗАПИСИ ARC_DOP.TITLE_W2C
    #####################################################
    # sql: SELECT id FROM arc WHERE ...
    #####################################################
    # def iniArcDop(self, sql):
    #     words = self.tokenizer.run(doc)
    #     keys  = self.wordsToKeys(words)
    #     return ' '.join(keys) if not(keys is None) else None



    #####################################################
    # TEXT (НЕ ОБРАБОТАННЫЙ) В СТРОКУ КЛЮЧЕВЫХ СЛОВ
    #####################################################
    def docToDoc(self, doc):         # [None] - ошибка
        words = self.tokenizer.run(doc)
        keys  = self.wordsToKeys(words)
        return ' '.join(keys) if not(keys is None) else None



    #####################################################
    # СПИСОК СЛОВ В СПИСОК КЛЮЧЕВЫХ СЛОВ
    #####################################################
    def wordsToKeys(self, words):       # [None] - ошибка
        if words is None: return None
        keys = []
        for word in words:
            key = self.wordToKey(word)
            if not (key is None): keys.append(key)
        return keys


    #####################################################
    # СЛОВО В КЛЮЧЕВОЕ СЛОВО
    #####################################################
    def wordToKey(self, word):          # [None] - ошибка
        cluster = self.wordToCluster(word)
        return self.clusterToKey(cluster)



    #####################################################
    # СЛОВО В НОМЕР КЛАСТЕРА (INT)
    #####################################################
    def wordsToClusters(self, words):   # [None] - ошибка
        clusters = []
        for word in words:
            cluster = self.wordToCluster(word)
            if not (cluster is None): clusters.append(cluster)
        return clusters


    def wordToCluster(self, word):      # [None] - ошибка
        try:             cluster = self.word2cluster[word]
        except KeyError: cluster = None
        return cluster


    #####################################################
    # НОМЕР КЛАСТЕРА (INT) В СПИСОК СЛОВ
    #####################################################
    def clusterToWords(self, cluster):  # [None] - ошибка
        if cluster is None: return None
        words = []
        for cluster_word in self.word2cluster:
            if self.word2cluster[cluster_word] == cluster:
                words.append(cluster_word)
        return words


    #####################################################
    # НОМЕР КЛАСТЕРА (INT) В КЛЮЧЕВОЕ СЛОВО
    #####################################################
    clusterToKey = lambda self, cluster: (self.STR_CLUSTER+str(cluster)) if not (cluster is None) else None
    # def clusterToKey(self, cluster):    # [None] - ошибка
    #     if cluster is None: return None
    #     word = None
    #     for cluster_word in self.word2cluster:
    #         if self.word2cluster[cluster_word] == cluster:    # так нельзя с dict
    #             word = cluster_word
    #             break
    #     return word




##########################################################
# НЕ ИСПОЛЬЗУЕТСЯ
##########################################################
# РАЗБИТЬ НА КЛАСТЕРЫ
##########################################################
def getClusters(vectors, clustersCount=10):
    model = MiniBatchKMeans(
        n_clusters           = clustersCount,                                       # количество кластеров [8]
        init                 = 'k-means++',                                         # способ выбора начальных центров ['k-means++']
        batch_size           = clustersCount*20,
        random_state         = np.random.RandomState(0),                            # [None]
        reassignment_ratio   = 0, #10**-4,
        max_no_improvement   = 30                                                   # [10]
    )
    model.fit(vectors)
    clusters = model.predict(vectors)                                               # список: кластер для КАЖДОГО вектора
    return clusters
