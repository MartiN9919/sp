# -*- coding: utf-8 -*-

# virtualenv --no-site-packages -p python3.4 envML
# source envML/bin/activate

# pip install --upgrade gensim
# pip install testfixtures         # doc2vec

# при ошибке: Недопустимая инструкция (сделан дамп памяти) - tensorflow (1.6.0) не работает с некоторыми процессорами https://toster.ru/q/515812
# pip3 uninstall tensorflow
# pip3 install tensorflow==1.5

# pip install pattern - работает и без нее, но: textcleaner.py:37 'pattern' package not found; tag filters are not available for English https://python-catalin.blogspot.com/2017/03/the-pattern-python-module-part-001.html

import os, logging, gensim, multiprocessing
import numpy as np

from   tqdm                            import tqdm
from   gensim.models                   import KeyedVectors
from   gensim.models.word2vec          import Word2Vec
from   gensim.models.callbacks         import CallbackAny2Vec
#from   gensim.test.utils               import get_tmpfile   # common_corpus, common_texts

from   fun.funSys                      import logger
from   fun.funFile                     import extValidate, filePostfixAdd, filePosfixMax


class VAR:
    PATH_EPOCH = '_epoch'


##########################################################
# Callback to save model after each epoch
##########################################################
class W2VEpochSaver(CallbackAny2Vec):
    def __init__(self, fileW2V, epochBegin=1):
        self.fileW2V = fileW2V
        self.epoch   = epochBegin

    def on_epoch_end(self, model):
        path = w2vFileEpoch(self.fileW2V, self.epoch)
        logger.info('save '+path)
        model.save(path)
        self.epoch += 1


##########################################################
# WORD2VEC
##########################################################
# w2v.wordToVecWord(word) # [None] - ошибка
# w2v.most_similar(word)
##########################################################
#    w2v.model.vocab - список ключей модели
#    if word in w2v_model.wv.vocab: ...
#    w2v.model.wv.index2word
#    w2v.model.vector_size
#    w2v.model.wv["броник"]
#    w2v.model.most_similar('дурак')
#    w2v.model.most_similar(positive=['москва', 'минск'], negative=['россия'], topn=10)
#    w2v.model.similarity("дверь", "окно")
##########################################################
class W2V(object):
    def __init__(self,
        fileW2V,                                                                        # путь к файлу модели
        dataSrc    = None,                                                              # генератор данных: sentences
        tokenizer  = None,                                                              # токенизатор
        embed_size = 300,                                                               # размер векторов between 100 and 1,000 [100]
        workers    = 0,                                                                 # количество задействованных ядер [1]
        epoch      = 5,                                                                 # количество эпох, ранее [1], теперь [5]
        #window    = 10,                                                                # размер окна 10 for skip-gram and 5 for CBOW
        wordMin    = 10,                                                                # рассматривать только слова, которые встречаются не менее раз [5], 30
        isInitSims = True,                                                              # финализация модели
        isInfo     = False                                                              # информация о ходе построения модели на экран
    ):
        LOG_ID            = 'W2V'
        self.model        = None
        self.tokenizer    = tokenizer                                                   # для использования производными классами
        self.embed_size   = embed_size                                                  # для использования производными классами
        epochLast         = filePosfixMax(path=os.path.dirname(fileW2V), postfixBegin=os.path.splitext(os.path.basename(fileW2V))[0]+VAR.PATH_EPOCH) # последняя сохраненная эпоха

        if isInfo: logging.basicConfig(format='%(message)s', level=logging.INFO)

        # модель: загрузить
        if os.path.exists(fileW2V):
            logger.info(LOG_ID+' load '+os.path.basename(fileW2V))
            self.load(fileW2V)

        # модель: продолжить обучение
        elif 0 < epochLast < epoch:
            fileW2VEpoch = filePostfixAdd(file=fileW2V, postfix=VAR.PATH_EPOCH+str(epochLast))
            self.model   = Word2Vec.load(fileW2VEpoch)                                                          # только так
            self.model.train(
                tqdm(dataSrc, desc=LOG_ID+' data', unit='rec'),
                total_examples = self.model.corpus_count,
                epochs         = epoch-epochLast,
                callbacks      = [W2VEpochSaver(fileW2V=fileW2V, epochBegin=epochLast+1)],
            )
            if isInitSims: self.model.init_sims(replace=True)
            self.save(fileW2V)

        # модель: сохранить последнюю эпоху как итоговый файл
        elif epochLast == epoch:
            fileW2VEpoch = filePostfixAdd(file=fileW2V, postfix=VAR.PATH_EPOCH+str(epochLast))
            self.model   = Word2Vec.load(fileW2VEpoch)                                                          # только так
            if isInitSims: self.model.init_sims(replace=True)
            self.save(fileW2V)

        # модель: создать
        else:
            logger.info(LOG_ID+' create '  +os.path.basename(fileW2V))
            logger.info(LOG_ID+' optimize '+str(gensim.models.word2vec.FAST_VERSION))

            if workers == 0:
                workers = multiprocessing.cpu_count()
                if workers > 1: workers-=1
                logger.info(LOG_ID+' cores '+str(workers))

            self.model = Word2Vec(
                tqdm(dataSrc, desc=LOG_ID+' data', unit='rec'),
                size      = embed_size,
                iter      = epoch,
                min_count = wordMin,
                # window  = window,
                workers   = workers,
                callbacks = [W2VEpochSaver(fileW2V=fileW2V, epochBegin=0)],
            )

            if isInitSims: self.model.init_sims(replace=True)                                                   # ./convertvec bin2txt input.bin output.txt
            self.save(fileW2V)

        logger.info(LOG_ID+' INI OK. Words '+str(len(self.model.wv.index2word)))



    #####################################################
    # МОДЕЛЬ: СОХРАНИТЬ / ЗАГРУЗИТЬ
    #####################################################
    def save(self, file):
        if   extValidate(file, 'txt'): self.saveTXT(file)
        elif extValidate(file, 'bin'): self.saveBIN(file)
        elif extValidate(file, 'w2v'): self.saveW2V(file)
    def saveTXT(self, file): self.model.wv.save_word2vec_format(file, binary=False)
    def saveBIN(self, file): self.model.wv.save_word2vec_format(file, binary=True)
    def saveW2V(self, file): self.model.wv.save(file)

    def load(self, file):
        if   extValidate(file, 'txt'): self.loadTXT(file)
        elif extValidate(file, 'bin'): self.loadBIN(file)
        elif extValidate(file, 'w2v'): self.loadW2V(file)
        else:
            lfile = os.path.basename(file).lower().split('.')
            if   'bin' in lfile: self.loadBIN(file)
            elif 'txt' in lfile: self.loadTXT(file)
            elif 'vec' in lfile: self.loadTXT(file)
            elif 'w2v' in lfile: self.loadW2V(file)
            else:                self.loadTXT(file)
    def loadTXT(self, file):            self.model = KeyedVectors.load_word2vec_format(file, binary=False)  # .txt .bz2 (bzip2 -zkf file)
    def loadBIN(self, file):            self.model = KeyedVectors.load_word2vec_format(file, binary=True)   # .bin .bz2 (bzip2 -zkf file)
    def loadW2V(self, file, mmap=None): self.model = KeyedVectors.load(file, mmap=mmap)                     # .w2v .bz2; mmap='r', limit=500000 http://qaru.site/questions/1673057/how-to-speed-up-gensim-word2vec-model-load-time


    #####################################################
    # СЛОВО В ВЕКТОР СЛОВА
    #####################################################
    def wordToVecWord(self, word): # [None] - ошибка
        try:             ret = self.model.wv[word]
        except KeyError: ret = None
        return ret


    #####################################################
    # ДОКУМЕНТ В ВЕКТОР ДОКУМЕНТА (MEAN)
    #####################################################
    def docToVecDocMean(self, doc):
        words = self.tokenizer.run(doc)
        return np.mean([self.model[w] for w in words if w in self.model] or [np.zeros(self.embed_size)], axis=0)


    #####################################################
    # ПОДОБНЫЕ СЛОВА [(слово, подобие), ...]
    #####################################################
    def wordSim(self, word, topn=5):
        try:             ret = self.model.most_similar(positive=[word], topn=topn)
        except KeyError: ret = []
        return ret



# имя файла для эпохи
w2vFileEpoch = lambda file, epoch: filePostfixAdd(file, VAR.PATH_EPOCH+str(epoch))


'''
import numpy as np
class DocSim(object):
    def __init__(self, w2v_model , stopwords=[]):
        self.w2v_model = w2v_model
        self.stopwords = stopwords

    def vectorize(self, doc):
        """Identify the vector values for each word in the given document"""
        doc = doc.lower()
        words = [w for w in doc.split(" ") if w not in self.stopwords]
        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        # PS: There are other & better ways to do it.
        vector = np.mean(word_vecs, axis=0)
        return vector


    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    def calculate_similarity(self, source_doc, target_docs=[], threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        if isinstance(target_docs, str):
            target_docs = [target_docs]

        source_vec = self.vectorize(source_doc)
        results = []
        for doc in target_docs:
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            if sim_score > threshold:
                results.append({
                    'score' : sim_score,
                    'doc' : doc
                })
            # Sort results by score in desc order
            results.sort(key=lambda k : k['score'] , reverse=True)

        return results
'''