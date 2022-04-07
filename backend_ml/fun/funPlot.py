# -*- coding: utf-8 -*-

# для отключения потребности в tkinter (GUI)
# https://stackoverflow.com/questions/4931376/generating-matplotlib-graphs-without-a-running-x-server/4935945
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from .funText import textCutDots

#####################################################
# https://matplotlib.org/faq/installing_faq.html
# pip install matplotlib
#####################################################
# matplotlib==2.2.2
# cycler==0.10.0
# python-dateutil==2.7.2
# numpy==1.14.2
# pyparsing==2.2.0
# kiwisolver==1.0.1
#####################################################
# tkinter НЕ СТАВИТЬ
#####################################################


#####################################################
# РАБОТА С matplotlib.pyplot
#####################################################
# filePath - путь к файлу, если не задан, то создать файл
#####################################################
def plotMulti(filePath, valX=[], valY=[], types=['bar'], title='', labelX='', labelY=''):
    if isinstance(title,  list): title  = ' '.join(title)  # (title[0]  if len(title)  > 0 else '')
    if isinstance(labelX, list): labelX = ' '.join(labelX) # (labelX[0] if len(labelX) > 0 else '')
    if isinstance(labelY, list): labelY = ' '.join(labelY) # (labelY[0] if len(labelY) > 0 else '')

    valXUseful = []                                             # valYUseful - без нулевых значений
    valYUseful = []
    for ind in range(0, len(valY)):
        if valY[ind] == 0: continue
        valXUseful.append(str(valX[ind]))
        valYUseful.append(valY[ind])

    valXStr = []
    for item in valX: valXStr.append(str(item))                 # ось X в виде строковых значений
    for ind  in range(len(valY), len(valX)): valY.append(0)     # выровнять размерность valX и valY

    fig  = plt.figure(
        figsize=(5, 4*len(types)),
        #dpi=100
    )

    grid = (len(types), 1)
    for ind, typ in enumerate(types):
        ax = plt.subplot2grid(grid, (ind, 0))

        if ind == 0: plt.title(textCutDots(title, 45))

        if types[ind]=='bar':
            ax.bar(
                valXStr,
                valY,
                alpha     = 0.4,
                color     = 'green',                            # import numpy as np / color = np.array([204,255,51])/255.
                edgecolor = 'r',
                align     = 'center',
            )
            #ax.plot(x, y, color='r')                           # color='#660099'
            #ax.grid(True)                                      # линии вспомогательной сетки
            ax.orientation='horizontal'

            plt.xlabel(labelX)
            plt.ylabel(labelY)

        elif types[ind]=='pie':
            ax.pie(
                valYUseful,
                labels         = valXUseful,
                startangle     = 90,
                autopct        = '%1.0f%%',
                #shadow        = True,
                #pctdistance   = 1.1,
                #labeldistance = 1.2,
            )

    fig.savefig(filePath)
