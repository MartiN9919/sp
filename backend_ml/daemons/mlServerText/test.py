import sys
sys.path.append('')
sys.path.append('../')
sys.path.append('../..')

from   mlClientText           import MLClientText

#client = MLClientText(host='', port=5000)
client = MLClientText(host='200.200.200.236', port=5000)
try:
    txt = input()
    answer = client.w2vSim(txt)
except Exception as e:
    client = None
    raise e
print(answer)
#if answer in ('', None): continue
