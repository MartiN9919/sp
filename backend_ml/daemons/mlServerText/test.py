import sys
sys.path.append('')
sys.path.append('../')
sys.path.append('../..')

from   mlClientText           import MLClientText

client = MLClientText(host='', port=5000)
try:
    answer = client.w2vSim('государственный долг')
except Exception as e:
    client = None
    raise e
print(answer)
#if answer in ('', None): continue
