# -*- coding: utf-8 -*-

# virtualenv --no-site-packages -p python3.4 envML
# source envML/bin/activate

# pip install --upgrade tensorflow
# pip install numpy scipy
# pip install scikit-learn
# pip install pillow
# pip install h5py
# pip install keras
# pip install --upgrade gensim

import os, keras, collections

from   fun.funSys      import logger
from   fun.funFile     import extValidate, extSet



class ML():
    def __init__(self):
        # отключить уведомление о возможности поддержки AVX2 http://qaru.site/questions/189394/your-cpu-supports-instructions-that-this-tensorflow-binary-was-not-compiled-to-use-avx-avx2
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        self.model      = None

    def ini(self):
        pass




    #####################################################
    # МОДЕЛЬ: СОХРАНИТЬ / ЗАГРУЗИТЬ
    #####################################################
    def extValid(self, file, ext):
        ret = extValidate(file, ext)
        if not ret: logger.error('Расширение файла не '+ext)
        return ret


    #####################################################
    def modelSave(self, file):
        if not self.modelSaveConfig (extSet(file, '.json')): return False
        return self.modelSaveWeights(extSet(file, '.h5' ))

    def modelSaveConfig(self, file):
        if not self.extValid(file, '.json'): return False
        try:
            model_json = self.model.to_json()
            json_file  = open(file, 'w')
            json_file.write(model_json)
            json_file.close()
            ret = True
        except:
            ret = False
        return ret

    def modelSaveWeights(self, file):
        if not self.extValid(file, '.h5'): return False
        try:
            self.model.save_weights(file)
            ret = True
        except:
            ret = False
        return ret


    #####################################################
    def modelLoad(self, file):
        if not self.modelLoadConfig (extSet(file, '.json')): return False
        return self.modelLoadWeights(extSet(file, '.h5' ))

    def modelLoadConfig(self, file):
        if not self.extValid(file, '.json'): return False
        try:
            json_file  = open(file, 'r')
            model_json = json_file.read()
            json_file.close()
            self.model = keras.models.model_from_json(model_json)
            ret = True
        except:
            ret = False
        return ret

    def modelLoadWeights(self, file):
        if not self.extValid(file, '.h5'): return False
        try:
            self.model.load_weights(file)
            ret = True
        except:
            ret = False
        return ret



#####################################################
# СФОРМИРОВАТЬ СЛОВАРЬ ДОКУМЕНТОВ ИЗ ГЕНЕРАТОРА
#####################################################
# src       - класс-источник данных ((IND_TEXT, IND_LABEL), ...)
# tokenizer - класс-токенайзер предложений
# vocSize   - максимальное количество индексов для кодирования слов (размер словаря)
#####################################################
def getDoc2Ind(src, tokenizer, vocSize):
    def normalize_text(text):
        norm_text = text.lower()
        #norm_text = norm_text.replace('<br />', ' ')                   # Replace breaks with spaces
        norm_text = re.sub(r"([\.\",\(\)!\?;:])", " \\1 ", norm_text)   # Pad punctuation with spaces on both sides
        return norm_text

    print('Построение словаря документов из генератора ...')
    IND_TEXT   = 0
    #IND_LABEL  = 1
    #word2count = collections.Counter()                                  # cчетчик упоминаний слов в тексте
    #word2ind   = collections.defaultdict(int)                           # индексы (рейтинги) слов

    for ind, item in enumerate(src):
        print(item)
        #if ind%10000==0: print(str(ind)+' записей')
        #for word in tokenizer.run(item[IND_TEXT]):
        #    word2count[word] += 1
    #for ind, item in enumerate(word2count.most_common(vocSize)):
    #    word2ind[item[IND_TEXT]] = ind + 1                              # item = ('хотя', 1693)

    #print('Слов уникальных / использованных: '+str(len(word2count))+' / '+str(len(word2ind)))
    #if len(word2ind) < vocSize: print('Размер словаря vocSize можно уменьшить с '+str(vocSize)+' до '+str(len(word2ind)))

    #return word2ind



#####################################################
# СФОРМИРОВАТЬ СЛОВАРЬ СЛОВ ИЗ ГЕНЕРАТОРА
#####################################################
# src       - класс-источник данных ((IND_TEXT, IND_LABEL), ...)
# tokenizer - класс-токенайзер предложений
# vocSize   - максимальное количество индексов для кодирования слов (размер словаря)
#####################################################
def getWord2Ind(src, tokenizer, vocSize):
    print('Построение словаря слов из генератора ...')
    IND_TEXT   = 0
    #IND_LABEL  = 1
    word2count = collections.Counter()                                  # cчетчик упоминаний слов в тексте
    word2ind   = collections.defaultdict(int)                           # индексы (рейтинги) слов

    for ind, item in enumerate(src):
        if ind%10000==0: print(str(ind)+' записей')
        for word in tokenizer.run(item[IND_TEXT]):
            word2count[word] += 1
    for ind, item in enumerate(word2count.most_common(vocSize)):
        word2ind[item[IND_TEXT]] = ind + 1                              # item = ('хотя', 1693)

    print('Слов уникальных / использованных: '+str(len(word2count))+' / '+str(len(word2ind)))
    if len(word2ind) < vocSize: print('Размер словаря vocSize можно уменьшить с '+str(vocSize)+' до '+str(len(word2ind)))

    return word2ind


#####################################################
# СФОРМИРОВАТЬ ДАННЫЕ ИЗ ГЕНЕРАТОРА
#####################################################
# src       - класс-источник данных ((IND_TEXT, IND_LABEL), ...)
# tokenizer - класс-токенайзер предложений
# X         - [[word_ind_1, word_ind_2, ...], ...]
# Y         - [label_1,                       ...]
# длина X и Y - число записей в источнике за исключением пустых
#####################################################
def getXYGlobal(src, tokenizer, word2ind):
    print('Подготовка данных из генератора ...')
    IND_TEXT   = 0
    IND_LABEL  = 1
    X, Y       = [], []

    for ind, item in enumerate(src):
        if ind%10000==0: print(str(ind)+' записей')
        words = tokenizer.run(item[IND_TEXT])
        if len(words)==0: continue
        inds  = [word2ind[word] for word in words]                      # список индексов (рейтингов) слов
        X.append(inds)
        Y.append(float(item[IND_LABEL]))

    return X, Y

