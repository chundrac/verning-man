from bs4 import BeautifulSoup
from collections import defaultdict
import os

f = open('anselm_v1.0_coraxml/B.xml','r')
text = f.read()
f.close()

soup = BeautifulSoup(text)

children = []
for w in soup.find_all('token'):
    if 'pos' in [c.name for c in w.findChildren()] and w.find('pos')['tag'].startswith('VV'):
        for child in w.findChildren():
            children.append(child.name)


children = set(children)
children = ['lemma','pos','morph']
#children = ['tok_anno', 'pos', 'inflclass', 'lemma', 'infl', 'norm', 'lemma_gen']

allfeats = []

for fn in os.listdir('anselm_v1.0_coraxml/'):
    f = open('anselm_v1.0_coraxml/'+fn,'r')
    text = f.read()
    f.close()
    soup = BeautifulSoup(text)
    jahr = [l for l in text.split('\n') if l.startswith('Datum:')][0].split(': ')[1]
    sprachraum = [l for l in text.split('\n') if l.startswith('Sprachraum:')][0].split(': ')[1]
    #print(jahr,sprachraum)
    for w in soup.find_all('token'):
        if 'pos' in [c.name for c in w.findChildren()] and w.find('pos')['tag'].startswith('VV'):
            attrs_ = [fn,jahr,sprachraum]
            for child in children:
                if w.find(child) != None:
                    attrs_.append(w.find(child)[list(w.find(child).attrs.keys())[0]])
                else:
                    attrs_.append('---')
            attrs_.append(w.find('tok_anno')['ascii'])
            allfeats.append(attrs_)


f = open('anselm_verbs.tsv','w')
for l in allfeats:
    print('\t'.join(l),file=f)

f.close()