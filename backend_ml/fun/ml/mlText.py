# -*- coding: utf-8 -*-

# pip3 install -U nltk
# pip3 install -U pymorphy2

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

# pip3 install natasha -U

import re, string, random, nltk, pymorphy2 #, natasha as nt

from   fun.funText  import textNormal, textConsistDigits
from   fun.funSys   import dictRemoveKey, logError


# + отфильтровать наречия и служебные части речи (pymorphy2)
# + выделение устойчивых конструкций и идиом: Нижний_Новгород, Fullstack_Разработчик
# + все слова в начальную форму (pymorphy2)
# + склеить "не" с последующим словом (не_прийти, не_сделать)
# - разделить цифры и буквы (100г, 25ый) - лучше удалять из-за некорректности определения, например: г. (грамм, год) проблема: 25-ый
#   "__МУЖСКОЕ_ИМЯ__" и "__ЖЕНСКОЕ_ИМЯ__"
#   фэнтезийные имена
#   объединить числительные в группы 1,2,3,4_10,10_50,50_100,100_250...1500_1800,1800_1900, 1900_1918,1918_1938,1938_1940,1941,1942,1943,1944,1945,
#   1946_1953,1953_1990,1990_2000,2000_2008,2008_2012,2012_2016,2016_3000,3000_5000,5000-10000,over10000    __число_между_3_и_10__
#   иcправление опечаток
# + удалить URL и EMAIL



##########################################################
# ТОКЕНИЗИРОВАТЬ КОРПУС ДАННЫХ (еще не релизовывал)
##########################################################
def srcTokenizer(
        tokenizer,                                                                                      # токенайзер
        dataSrc,                                                                                        # генератор данных
        fileDest,                                                                                       # файл с преобразованным корпусом данных
    ):
    f = open(fileDest, 'w')
    try:
        for text in dataSrc:
            text = ' '.join(tokenizer.run(text))
            if text != '': f.write(text) # + '\n'
    finally:
        f.close()



##########################################################
# ТЕКСТ: ПЕРЕФРАЗИРОВАТЬ
##########################################################
# rnd      - вероятность замены элемента, который можно менять
# simWord  - степень подобия слова (w2v)
# simMorph - степень подобия морфемы слова
##########################################################
class Rephraser(object):
    def __init__(self, tokenizer, w2v, rnd=0.5, simWord=0.7, simMorph=0.7):
        self.tokenizer  = tokenizer
        self.w2v        = w2v
        self.morph      = pymorphy2.MorphAnalyzer()
        self.rnd        = rnd
        self.simWord    = simWord
        self.simMorph   = simMorph

    def run(self, text):
        words = text.split(' ')
        for ind, word in enumerate(words):
            if '_' in word: continue
            word1_title    = word.istitle()
            word1_lastchar = word[-1] if (word[-1] in string.punctuation) else ''
            word1 = word.lower()

            # разбор слова word1, первый вариант наиболее точный
            parse1 = self.morph.parse(word1)[0]
            if parse1.score<self.simMorph: continue

            # word10 - начальная форма слова
            word10 = self.tokenizer.run(word1)
            word10 = word10[0] if len(word10)>0 else ''
            if word10 == '': continue

            # подобные слова word2
            for sim in self.w2v.wordSim(word=word10):
                if sim[1]<self.simWord: break                                                               # степень подобия слова
                if '_' in sim[0]: continue                                                                  # подобное слово не должно быть составным
                if random.random()>self.rnd: continue                                                       # случайный отбор
                word20 = sim[0]

                # лексемы подобного слова word2, score=1.0
                isStop = False
                for parse2 in self.morph.parse(word20)[0].lexeme:
                    if \
                        (parse2.tag.POS          == parse1.tag.POS         ) and \
                        (parse2.tag.aspect       == parse1.tag.aspect      ) and \
                        (parse2.tag.case         == parse1.tag.case        ) and \
                        (parse2.tag.gender       == parse1.tag.gender      ) and \
                        (parse2.tag.involvement  == parse1.tag.involvement ) and \
                        (parse2.tag.mood         == parse1.tag.mood        ) and \
                        (parse2.tag.number       == parse1.tag.number      ) and \
                        (parse2.tag.person       == parse1.tag.person      ) and \
                        (parse2.tag.tense        == parse1.tag.tense       ) and \
                        (parse2.tag.transitivity == parse1.tag.transitivity) and \
                        (parse2.tag.voice        == parse1.tag.voice       ):
                        # словоформы совпадают: заменить слово
                        word2 = parse2.word+word1_lastchar
                        if word1_title: word2=word2.capitalize()
                        words[ind] = word2 #+'('+words[ind]+')'
                        isStop = True
                        #print(word1, ' --> ', word2)
                        break
                if isStop: break

        return ' '.join(words)


##########################################################
# ТОКЕНИЗАТОР ТЕКСТА
##########################################################
class Tokenizer(object):
    def __init__(self,
        wordLenMin      = 2,                                                                                # минимальная длина слов
        isLower         = False,                                                                            # привести к нижнему регистру
        isNormalize     = False,                                                                            # обработка текста как в loader-ах
        delPunctuation  = False,                                                                            # убрать пунктуацию
        delStopWords    = False,                                                                            # убрать стоп-слова
        isStemming      = False                                                                             # выделить стеммы
    ):
        self.wordLenMin     = wordLenMin
        self.isLower        = isLower
        self.isNormalize    = isNormalize
        self.delPunctuation = delPunctuation
        self.delStopWords   = delStopWords
        self.isStemming     = isStemming

        # self.BLOCK          = 'блок_'
        # self.BLOCK_MONEY    = self.BLOCK+'валюта_'
        # self.BLOCK_DATE     = self.BLOCK+'дата'
        # self.ntMoney        = nt.MoneyExtractor()
        # self.ntDate         = nt.DatesExtractor()

        self.no_chars   = ['не', 'no', 'без', 'против', 'against']
        self.stop_chars = [
            ':DD', ':D', 'о-)', ':"(', ':3', 'х(', ':o)', ':с', ':-Р', '—', '“', '”',
            'все-таки', 'всего-навсего', 'как-то', 'просто-напросто',
            'ладно', 'привет', 'по крайней мере', 'как дела',
            # вводные слова (фразы)
            'главным образом', 'самое главное', 'одним словом', 'иными словами', 'другими словами', 'иначе говоря', 'мягко выражаясь',
            'в смысле', 'то есть', 'если можно так', 'лучше сказать',
            'согласитесь', 'извините', 'по слухам', 'гораздо',
            'может быть', 'быть может', 'по-видимому', 'в самом деле', 'несомненно', 'без всякого сомнения', 'наверное',
            # 'то-то', 'так-таки', 'представьте себе',
        ]
        if self.delPunctuation:
            self.stop_chars.extend(list(string.punctuation))
            self.stop_chars.remove("'")                                 # n't - отдельная обработка

        if self.delStopWords:
            self.stop_words =      nltk.corpus.stopwords.words('russian')
            self.stop_words.extend(nltk.corpus.stopwords.words('english'))
            self.stop_words.extend([
                'че', 'еле', 'имхо', 'очень', 'все',
                # наречия
                #'туда', 'сюда',
                # вводные слова
                'вообще', #'вероятно', 'вероятно',
                'як', 'бо',
                'што', 'але', 'якi',
                'гэта', 'навогул', 'хоць', 'яшчэ', 'зусiм', 'усiм', 'проста', 'надта', 'напэуна', 'нажаль',
            ])
            #    'всё', 'лет', 'знаю', 'года', 'всем', 'которые', 'который'
            self.stop_words = [word for word in self.stop_words if (not word in self.no_chars+['быть', 'можно', 'нельзя'])]

        if self.isStemming:
            self.morph = pymorphy2.MorphAnalyzer()
            #self.stem_rus = nltk.stem.snowball.SnowballStemmer("russian")
            #self.stem_eng = nltk.stem.snowball.SnowballStemmer("english")


    def run(self, doc):
        try:
            # убрать двойные кавычки, в которые заключена строка и вообще в тексте (в дальнейшем при сохранении от этого отказатья)
            doc = doc.replace('"', '')

            # нормализация (используется loader-ами)
            if self.isNormalize: doc = textNormal(doc)
            doc = doc.replace('"', "'") # скорректировать результат textNormal

            # прописные буквы
            if self.isLower: doc = doc.lower()

            # удалить цифры
            # doc = textDigitsDel(doc)

            # удалить символы
            for char in self.stop_chars:  doc = doc.replace(char, ' ')

            # пробелы по обе стороны пунктуации
            if not self.delPunctuation: doc = re.sub(r"([\.\",\(\)!\?;:])", " \\1 ", doc)

            # замена
            doc = doc\
                .replace('ў',             'у'      ) \
                .replace('№',             ' номер ')
            #     .replace('бакс',          'доллар') \
            #     .replace('долларау',      'долларов') \
            #     .replace('доларау',       'долларов') \
            #     .replace(' б.р',          ' р') \
            #     .replace(' бел.р',        ' р') \
            #     .replace(' белоруских р', ' р') \
            #     .replace(' беларускiх р', ' р') \

            # # замена Money '1 доллар' -> '__usd__'
            # offset = 0
            # for match in self.ntMoney(doc):
            #     start, stop = match.span
            #     start  += offset
            #     stop   += offset
            #     block  = ' '+self.BLOCK_MONEY+match.fact.currency.lower()+' '
            #     doc = doc[:start]+block+doc[stop:]
            #     offset += -stop+start+len(block)

            # # замена дат '1 января 2000' -> 'блок_дата_2000_01_01'
            # offset = 0
            # for match in self.ntDate(doc):
            #     start, stop = match.span
            #     start  += offset
            #     stop   += offset
            #     block  = ' '+self.BLOCK_DATE+\
            #              (('_'+str(match.fact.year )) if (not match.fact.year  is None) else '')+\
            #              (('_'+str(match.fact.month)) if (not match.fact.month is None) else '')+\
            #              (('_'+str(match.fact.day  )) if (not match.fact.day   is None) else '')+\
            #              ' '
            #     doc = doc[:start]+block+doc[stop:]
            #     offset += -stop+start+len(block)

            # токенизация (разбить на слова)
            words = nltk.word_tokenize(doc)
            for ind, word in enumerate(words):
                if word in ["n't", "not", "nor"]: words[ind] = 'no'         # don't  => [do] [n't] => [do] [no] : doesn't aren't couldn't haven't isn't mightn't mustn't needn't weren't
                if word == 'ни': words[ind] = 'не'

            # если не блок: удалить слова с цифрами
            words = [word for word in words if (not textConsistDigits(word))] #or (word[:len(self.BLOCK)]==self.BLOCK)]

            if self.isStemming:
                for ind, word in enumerate(words):
                    pars = self.morph.parse(word)[0]

                    # слова в начальную форму
                    words[ind] = pars.normal_form      # только для русского
                    # можно использовать import en, но английский не приоритетен

                    # не делать: утрачивается обратная совместимость
                    # выделить стеммы - 'ден', 'выда', 'удачн', 'ожида', 'худш', 'настроен'
                    # words = [self.stem_rus.stem(word) for word in words]
                    # words = [self.stem_eng.stem(word) for word in words]

                    # удалить [наречия ADVB], предлоги PREP, союзы CONJ, частицы PRCL, междометия INTJ, местоимения-существительные NPRO
                    if (pars.tag.POS in ['PREP', 'CONJ', 'PRCL', 'INTJ', 'NPRO']) and (not words[ind] in self.no_chars): words[ind] = ''

            # удалить стоп-слова и пустые элементы (чтобы self.no_chars+'_'+''+'второе слово')
            if self.delStopWords:
                words = [word for word in words if (word not in self.stop_words+[''])]

            # склеить: не_слово
            for ind in range(len(words)-2,-1,-1):
                if (words[ind] not in self.no_chars) or (words[ind+1]==''): continue
                words[ind+1] = words[ind]+'_'+words[ind+1]                  # без '_' можно потерять обратную совместимость в w2v
                del words[ind]

            # подчистить из мусор, удалить пустые элементы
            words = [word.replace("`", "").replace("'", "").replace("..", "").replace('ё', 'е').strip() for word in words]
            words = [word for word in words if word != '']

            # фильтр по минимальной длине слов (необходимость сомнительна, так как задачу решает удаление стоп-слов)
            if self.wordLenMin > 1:
                words = [word for word in words if len(word) >= self.wordLenMin]

            # удалить короткие иностранные слова (приоритет: русский)
            words = [word for word in words if (len(word)>5) or (not (word[0] in list(string.ascii_lowercase)))]

        except Exception as e:
            logError(e)
            words = []

        return words
