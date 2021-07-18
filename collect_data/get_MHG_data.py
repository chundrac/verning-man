import re
import os
from bs4 import BeautifulSoup

f = open('rem-corralled-20161222/M001-N1.xml','r')
text = f.read()
f.close()
soup = BeautifulSoup(text)

children = []
for w in soup.find_all('token'):
    if w['type'] == 'token' and w.find('pos')['tag'].startswith('VV'):
        for child in w.findChildren():
            children.append(child.name)


children = set(children)
children = ['tok_anno', 'pos', 'inflclass', 'lemma', 'infl', 'norm', 'lemma_gen']

allfeats = []
for fn in os.listdir('rem-corralled-20161222'):
    print(fn,os.listdir('rem-corralled-20161222').index(fn)/len(os.listdir('rem-corralled-20161222')))
    f = open('rem-corralled-20161222/'+fn,'r')
    text = f.read()
    f.close()
    soup = BeautifulSoup(text)
    sprachraum = soup.find('language-area').text
    if sprachraum == '-':
        sprachraum = soup.find('language-type').text
    jahr1 = soup.find('date').text
    print(jahr1)
    jahr2 = soup.find('time').text
    print(jahr2)
    for w in soup.find_all('token'):
        if w['type'] == 'token' and w.find('pos')['tag'].startswith('VV'):
            attrs_ = [fn,jahr1,jahr2,sprachraum]
            for child in children:
                attrs_.append(w.find(child)[list(w.find(child).attrs.keys())[0]])
            allfeats.append(attrs_)

f = open('all_MHG_verbs.tsv','w')
for l in allfeats:
    print('\t'.join(l),file=f)

f.close()