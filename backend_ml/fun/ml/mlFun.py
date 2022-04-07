# -*- coding: utf-8 -*-

from   fun.funFile import FileReadLines


##########################################################
# ФОРМИРУЕТ ИЗ ФАЙЛА ПРЕДЛОЖЕНИЯ ПО wordLimit ТОКЕНИЗИРОВАННЫХ СЛОВ В КАЖДОМ
##########################################################
# file:         txt, csv, gz
# tokenizer:    если не указан - разбитие на слова по пробелам
# wordLimit:    максимум слов в предложении (0 - не ограничено)
# recLimit:     максимум читаемых строк (0 - не ограничено)
##########################################################
class File2Sentences(object):
    def __init__(self, file, encoding='utf-8', tokenizer=None, wordLimit=0, recLimit=0):
        self.file      = file
        self.encoding  = encoding
        self.tokenizer = tokenizer
        self.wordLimit = wordLimit
        self.recLimit  = recLimit

    def __iter__(self):
        recCount = 0
        for line in FileReadLines(self.file, encoding=self.encoding):
            # разбить на нормализованные слова
            words = self.tokenizer.run(line) if self.tokenizer != None else line.split(' ')

            # строки неограниченной длины
            if self.wordLimit == 0:
                ret = words

            # строки ограниченной длины
            else:
                ret = []
                for word in words:
                    ret.append(word)
                    if len(ret) >= self.wordLimit:
                        yield ret
                        ret = []

                        recCount += 1
                        if recCount > self.recLimit: break

            # отправить результат
            if ret !=[]: yield ret

            # ограничение по количеству строк
            if self.recLimit > 0:
                recCount += 1
                if recCount > self.recLimit: break
