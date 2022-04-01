# -*- coding: utf-8 -*-

# pip install -U nltk
# pip install pymorphy2

# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')

# pip install natasha

import re, string, nltk, pymorphy2, natasha as nt

from   fun.funText import textNormal, textConsistDigits
from   fun.funSys  import dictRemoveKey, logError


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

        self.BLOCK          = 'блок_'
        self.BLOCK_MONEY    = self.BLOCK+'валюта_'
        self.BLOCK_DATE     = self.BLOCK+'дата'
        self.ntMoney        = nt.MoneyExtractor()
        self.ntDate         = nt.DatesExtractor()

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
                .replace('№',             ' номер ') \
                .replace('бакс',          'доллар') \
                .replace('долларау',      'долларов') \
                .replace('доларау',       'долларов') \
                .replace(' б.р',          ' р') \
                .replace(' бел.р',        ' р') \
                .replace(' белоруских р', ' р') \
                .replace(' беларускiх р', ' р') \

            # замена Money '1 доллар' -> '__usd__'
            offset = 0
            for match in self.ntMoney(doc):
                start, stop = match.span
                start  += offset
                stop   += offset
                block  = ' '+self.BLOCK_MONEY+match.fact.currency.lower()+' '
                doc = doc[:start]+block+doc[stop:]
                offset += -stop+start+len(block)

            # замена дат '1 января 2000' -> 'блок_дата_2000_01_01'
            offset = 0
            for match in self.ntDate(doc):
                start, stop = match.span
                start  += offset
                stop   += offset
                block  = ' '+self.BLOCK_DATE+\
                         (('_'+str(match.fact.year )) if (not match.fact.year  is None) else '')+\
                         (('_'+str(match.fact.month)) if (not match.fact.month is None) else '')+\
                         (('_'+str(match.fact.day  )) if (not match.fact.day   is None) else '')+\
                         ' '
                doc = doc[:start]+block+doc[stop:]
                offset += -stop+start+len(block)

            # токенизация (разбить на слова)
            words = nltk.word_tokenize(doc)
            for ind, word in enumerate(words):
                if word in ["n't", "not", "nor"]: words[ind] = 'no'         # don't  => [do] [n't] => [do] [no] : doesn't aren't couldn't haven't isn't mightn't mustn't needn't weren't
                if word == 'ни': words[ind] = 'не'

            # если не блок: удалить слова с цифрами
            words = [word for word in words if (not textConsistDigits(word)) or (word[:len(self.BLOCK)]==self.BLOCK)]

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
