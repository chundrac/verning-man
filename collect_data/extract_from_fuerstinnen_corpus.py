from bs4 import BeautifulSoup
from collections import defaultdict
import os

f = open('Fuerstinnen_1.1 exb/AD/AD_JE2_1677_08_14.exb','r')
text = f.read()
f.close()

soup = BeautifulSoup(text)

attrs = [t['category'] for t in soup.find_all('tier')]
attrs.pop(attrs.index('orig'))

allfeats = [['speaker']+attrs]

for sp in os.listdir('Fuerstinnen_1.1 exb'):
    for fn in os.listdir('Fuerstinnen_1.1 exb/'+sp):
        f = open('Fuerstinnen_1.1 exb/'+sp+'/'+fn,'r')
        text = f.read()
        f.close()
        soup = BeautifulSoup(text)
        speaker = soup.find('speaker')['id']
        date = soup.find_all('ud-information',{'attribute-name':'date'})[0].text
        region = soup.find_all('ud-information',{'attribute-name':'prov'})[0].text
        anno = {}
        for t in soup.find_all('tier'):
            if t['category'] != 'orig':
                for e in t.find_all('event'):
                    if e['start'] not in anno.keys():
                        anno[e['start']] = defaultdict(list)
                    anno[e['start']][t['category']].append(e.text)
        for k in anno.keys():
            feats = [speaker,date,region]
            for attr in attrs:
                if attr in anno[k].keys():
                    feats.append('|'.join(anno[k][attr]))
                else:
                    feats.append('')
            allfeats.append(feats)
        
f = open('fuerstinnen_data.tsv','w')
for l in allfeats:
    print('\t'.join(l),file=f)

f.close()