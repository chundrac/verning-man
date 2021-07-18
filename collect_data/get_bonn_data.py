import re
import os
from bs4 import BeautifulSoup

f = open('FnhdC.XML/111.xml','r')
text = f.read()
f.close()
soup = BeautifulSoup(text)

attrs = []
for w in soup.find_all('wortform',{'typ':'verb'}):
    for attr in w.attrs:
        attrs.append(attr)

attrs = sorted(set(attrs))

allfeats = []
for fn in os.listdir('FnhdC.XML'):
    if bool(re.match(r'\d{3}',fn)) == True:
        print(fn)
        f = open('FnhdC.XML/'+fn,'r')
        text = f.read()
        f.close()
        soup = BeautifulSoup(text)
        jahr = soup.find('jahr').text
        sprachraum = soup.find('sprachraum').text
        for w in soup.find_all('wortform',{'typ':'verb'}):
            attrs_ = [jahr,sprachraum]
            for attr in attrs:
                if attr in w.attrs:
                    attrs_.append(w[attr])
                else:
                    attrs_.append('---')
            allfeats.append(attrs_)

f = open('all_ENHG_verbs.tsv','w')
for l in allfeats:
    print('\t'.join(l),file=f)

f.close()