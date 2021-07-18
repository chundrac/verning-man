import numpy as np
from editdistance import distance
from collections import defaultdict
import re

vernerdict = {'MHG':{},'NHG':{}}
for l in open('germanic_verner_key.tsv','r'):
    ll = l.strip('\n').split('\t')
    if ll[1] != '':
        vernerdict['MHG'][ll[1]] = ll[0]
    if ll[2] != '':
        vernerdict['NHG'][ll[2]] = ll[0]

bonn_data = [l.strip('\n').split('\t') for l in open('../collect_data/all_ENHG_verbs.tsv','r')]

bonn_data = [l for l in bonn_data if l[5] != 'schwach']

verb_class = {}
for l in bonn_data:
    verb_class[l[6]]=l[5]

verbs = sorted(set([l[6] for l in bonn_data]))

#deal with prefixes

anselm_raw = [l.strip('\n').split('\t') for l in open('../collect_data/anselm_verbs.tsv','r')]

anselm_data = []
for l in anselm_raw:
    counter = 0
    for v in verbs:
        if l[3].endswith(v.strip('12-')) and not l[3].endswith('bringen'):
            counter += 1
    if counter > 0:
        #print(l[3])
        #print(sorted([v for v in verbs if l[3].endswith(v.strip('-12'))],key=lambda x: len(x)))
        stem = sorted([v for v in verbs if l[3].endswith(v.strip('-12'))],key=lambda x: len(x))[-1]
        prefix = l[3][:-len(stem.strip('-12'))]
        l[3] = stem
        #print(stem,prefix)
        anselm_data.append(l+[prefix])

fuerstinnen_raw = [l.strip('\n').split('\t') for l in open('../collect_data/fuerstinnen_verbs.tsv','r')]

fuerstinnen_data = []
for l in fuerstinnen_raw:
    counter = 0
    for v in verbs:
        if l[4].endswith(v.strip('12-')) and not l[4].endswith('bringen'):
            counter += 1
    if counter > 0:
        #print(l[3])
        #print(sorted([v for v in verbs if l[3].endswith(v.strip('-12'))],key=lambda x: len(x)))
        stem = sorted([v for v in verbs if l[4].endswith(v.strip('-12'))],key=lambda x: len(x))[-1]
        prefix = l[4][:-len(stem.strip('-12'))]
        l[4] = stem
        #print(stem,prefix)
        fuerstinnen_data.append(l+[prefix])

merged_NHG = []
for l in anselm_data:
    merged_NHG.append(l+['N'])

for l in fuerstinnen_data:
    ll = l[:3]+l[4:6]
    if l[6] == '':
        ll.append('---')
    else:
        ll.append(l[6])
    ll.append(l[3])
    ll.append(l[-1])
    ll.append('N')
    merged_NHG.append(ll)

for l in bonn_data:
    ll=[l[4].split('.')[1]]+l[0:2]+[l[6]]
    if l[2] == 'infinitiv':
        ll.append('VVINF')
        ll.append('--')
    if l[2] == 'partizip' or l[2] == 'unbekannt':
        ll.append('VVPP')
        ll.append('--')
    if l[2] == 'finit':
        if l[7] != 'imperativ':
            ll.append('VVFIN')
            infl = ''
            infl += l[10]
            if l[9] == 'singular':
                infl = 'Sg.' + infl
            if l[9] == 'plural':
                infl = 'Pl.' + infl
            if l[13] == 'praesens':
                infl = 'Pres.' + infl
            if l[13] == 'praeteritum':
                infl = 'Past.' + infl
            if l[7] == 'indikativ':
                infl = 'Ind.' + infl
            if l[7] == 'konjunktiv':
                infl = 'Subj.' + infl
            if l[7] == '---':
                infl = '*' + infl
            infl = infl.replace('Past.Subj','Past.Konj')
            ll.append(infl)
        else:
            ll.append('VVIMP')
            infl = ''
            if l[9] == 'singular':
                infl = 'Sg.2'
            if l[9] == 'plural':
                infl = 'Pl.2'
            ll.append(infl)
    ll.append(l[3])
    if l[11] != '---':
        ll.append(l[11])
    else:
        ll.append('')
    ll.append('N')
    merged_NHG.append(ll)

# load MHG data

MHG_data = [l.strip('\n').split('\t') for l in open('../collect_data/all_MHG_verbs.tsv','r')]   

MHG_data = [l for l in MHG_data if l[5] != 'wk']

for l in MHG_data:
    verb_class[l[9].split('-')[-1].split('/')[0]]=l[5].replace('st','stark_')

MHG_data = [l for l in MHG_data if l[9] != '[!]']

MHG_data_ = []
for l in MHG_data:
    if l[1] != '-':
        ll = l[0:2]+l[3:]
        MHG_data_.append(ll)
    else:
        ll = l[0:1]+l[2:]
        MHG_data_.append(ll)

MHG_data = MHG_data_

for l in MHG_data:
    ll = l[:3]
    verb = l[9].split('-')[-1].split('/')[0]
    prefix = ''
    if '-' in l[9]:
        prefix = l[9].split('-')[0]
    norm = l[8]
    ll.append(verb)
    ll.append(l[4])
    ll.append(l[7])
    ll.append(l[3])
    ll.append(prefix)
    ll.append('Y')
    inds = np.array([distance(prefix,norm[:i])+distance(verb[:1],norm[i:i+1]) for i in range(len(norm))])
    ind = np.where(inds==inds.min())[0][-1]
    stemmednorm = norm[ind:]
    ll.append(stemmednorm)
    merged_NHG.append(ll)
    print(verb,prefix,norm,stemmednorm)

norms_ = [l[9] if len(l) == 10 else '' for l in merged_NHG]

merged_NHG = [l[:9] for l in merged_NHG]

norms = []

data = []
for i,l in enumerate(merged_NHG):
    if l[-1] == 'N':
        if l[3].strip('*-12') in vernerdict['NHG'].keys():
            data.append(l+[vernerdict['NHG'][l[3].strip('*-12')]])
            norms.append(norms_[i])
        #else:
        #    print(l)
    if l[-1] == 'Y':
        if l[3] in vernerdict['MHG'].keys():
            data.append(l+[vernerdict['MHG'][l[3]]])
            norms.append(norms_[i])
        #else:
        #    print(l)

merged_NHG = data

date_dict = """10 (?)|1075
|_
_|_
-|_
13|1250
12|1150
11|1050
12?|1150
11?|1050
17xx|1750
12,M|1150
12,2|1150
159x|1590
15xx|1590
13,2|1250
11,2|1050
13,E|1225
12,1|1125
13,M|1250
14,1|1325
13,1|1225
14,1V|1325
12,4V|1175
12/2D|1125
11-12|1100
41609|-
14,1D|1325
12,1D|1125
12/2H|1175
12,3D|1130
12/13?|1200
13 (?)|1250
11 (?)|1050
12-13,A|1200
1342-43|1342
um 1180|1180
um 1065|1065
um 1400|1400
um 1100|1100
um 1330|1330
1057/65|1057
1276-81|1276
14. Jh.|1350
12,1(?)|1150
um 1120|1120
um 1130|1130
um 1080|1080
um 1160|1160
um 1070|1070
um 1140|1140
um 1190|1190
13/A (?)|1225
vor 1170|1170
bis 1272|1272
13,A (?)|1225
um 1140?|1140
1172 (?)|1172
1335-1341|1341
1346-1350|1350
12/13 (?)|1200
nach 1065|1075
1159-1170|1170
nach 1190|1190
1360-1396|1396
nach 1243|1250
1445-1452|1450
13,M-14,2V|1300
um 1160-70|1160
um 1180-90|1180
um 1190-95|1190
um 1150/60|1150
um 1140/60|1140
12,4V-13,A|1200
um 1160/70|1160
um 1160 (?)|1160
Ende 14.Jh.|1390
um 1150 (?)|1150
um 1100 (?)|1100
16th century|1550
Ende 14. Jh.|1390
15th century|1450
vor 1127 (?)|1127
14th century|1350
2. H. 15. Jh.|1475
ca. 1220-1300|1250
A.-M. 14. Jh.|1325
1340-vor 1346|1340
ca. 1200-1210|1210
1302-ca. 1310|1310
1258 oder 1269|1269
1378 vollendet|1378
1300 vollendet|1300
um 1140/50 (?)|1140
um 1200 / 13,1V|1225
12,E (VL 1, 609)|1190
1328 (VL 8, 416)|1328
spätestens 13,3V|1275
13,3D / nach 1260|1275
abgeschlossen 1293|1293
1275-76 (VL 8, 898)|1275
vielleicht noch 12,E|1190
um 1220? (VL 2, 744)|1220
um 1250 (VL 8, 323f.)|1250
1301 (Naumann 1923, 194)|1301
2nd half of 15th century|1475
2nd half of 14th century|1375
1st half of 14th century|1325
um 1200 (vgl. VL 3, 502)|1200
1st half of 16th century|1525
1st half of 15th century|1475
1274/75-1282 (VL 1, 1091)|1274
ca. 1180-1210 (VL 6, 932)|1195
wohl zwischen 1352 und 1370|1360
1270-1290 (Unger 1969, 182)|1280
13,1 (um oder nach 1215-20?)|1220
nicht vor 13,3D (VL 7, 1063)|1063
1485-86 und Zusätze bis 1530|1485
ca. 1215-25 (Beckers 1994, 3)|1225
1331-1336 (Schorbach 1888, XX)|1336
nach 1297 (um oder kurz nach 1300)|1300
wohl zwischen ca. 1170 und 1187-90|1180
13,A, (ca. 1200-1210, VL 10, 1378)|1210
etwa 1285-1290 (Bernt 1906, 185f.)|1285
1347 (Rede IV) und 1348 (Rede I-III)|1347
13. Jh. (VL 8, 524) bzw. vor ca. 1278|1278
ca. 1220-1230 (1224-1231?) (Eckhardt 1959, 459)|1225
nach 1283, vielleicht 1293-1297 (Mielke-Vandenhouten 1998, 58f.)|1295
Begonnen ca. 1235-1241/42?, dem Tod Konrads II von Öttingen (VL 8, 323f.)|1240
"Winsbecke" 1210-20, später nicht ausgeschlossen; "Winsbeckin" etwas jünger (VL 10, 1224f.)|1220
Aug./Sept. 1298 (Schlacht bei Göllheim) (Bach 1930, § 8); nach 1281 (Bach 1930, § 10); nach 1297 (Minnehof) (Bach 1930, § 12)|1298
13,1-13,2|1250
13,2-14,1|1300
14,2|1350
14,1-14,2|1350
12,1-12,2|1150
12,2-13,1|1200
14|1350"""

date_dict = {l.split('|')[0]:l.split('|')[1] for l in date_dict.split('\n')}

dial_dict = """NA|NA
obs.|Obs
rip.|Rip
thür.|Thuer
alem.|Ohchal
smrk.|Obs
mbair.|Mbair
rhfrk.|Ofr
schwäb.|Schwaeb
hchalem.|Ohchal
elbofäl.|Eastph
oschwäb.|Schwaeb
hessisch|Hess
bairisch|Mbair
ripuarisch|Rip
östl. nndd.|OstND
südl. ofäl.|Ostf
südbairisch|Mbair
ripuarisch?|Rip
alem./bair.|Ohchal
thüringisch|Thuer
alemannisch|Ohchal
rhfrk.-hess.|Hess
nbair./ofrk.|Ofr
bairisch (?)|Mbair
ostfränkisch|Ofr
Dessau/Anhalt|Obs
ostschwäbisch|Oschwaeb
Simmern/Pfalz|Schwaeb
oberfränkisch|Ofr
(süd)bairisch|Mbair
schwäb./rhfrk.|Schwaeb
Torgau/Sachsen|Obs
moselfränkisch|Ofr
ostalemannisch|Ohchal
mittelbairisch|Mbair
rheinfränkisch|Rip
Gotha/Thüringen|Thuer
hochalemannisch|Ohchal
alemannisch (?)|Ohchal
Harzgerode/Harz|Obs
zentralhessisch|Hess
Dresden/Sachsen|Obs
mittelfränkisch|Ofr
rheinfrkänkisch|Rip
westalemannisch|Ohchal
nordthüringisch|Thuer
Steinbach/Hessen|Hess
hchalem./ndalem.|Ohchal
Birkenfeld/Pfalz|Schwaeb
Weimar/Thüringen|Thuer
südrheinfränkisch|Rip
rheinfränkisch (?)|Rip
westmoselfränkisch|Rip
nbair./ofrk./thür.|Ofr
(süd)rheinfränkisch|Ofr
Reinstädt/Thüringen|Thuer
(ostmittel)bairisch|Mbair
bairisch-alemannisch|Mbair
niederösterreichisch|Mbair
hessisch-thüringisch|Hess
hessisch-thüringisch?|Hess
bairisch, alemannisch|Mbair
westl. mittelbairisch|Mbair
schwäbisch-alemannisch|Schwaeb
ostfränkisch, bairisch|Ofr
bairisch-ostalemannisch|Ohchal
bairisch, niederdeutsch|Mbair
(süd)rheinfränkisch (?)|Rip
rheinfränkisch-hessisch|Rip
bairisch-österreichisch|Mbair
bairisch, mitteldeutsch|Mbair
rheinfränkisch, hessisch|Rip
alemannisch (elsässisch)|Els
ostalemannisch, bairisch|Ohchal
Hildburghausen/Thüringen|Thuer
rheinfränkisch, bairisch|Rip
mittelfränkisch, bairisch|Ofr
mittelfränkisch, hessisch|Hess
mittelbairisch (westlich)|Mbair
thüringisch-obersächsisch|Thuer
mittelfränkisch,  bairisch|Mbair
hessisch, ostfränkisch (?)|Hess
ostfränkisch, nordbairisch|Ofr
rheinfränkisch (teilweise)|Rip
ostmitteldeutsch (böhmisch)|Obs
ostfränkisch (nürnbergisch)|Ofr
nordrheinfränkisch-hessisch|Hess
westbairisch-ostalemannisch|Ohchal
ostoberdeutsch, alemannisch|Ohchal
rheinfränkisch, alemannisch|Rip
bairisch (mit Alemannismen)|Mbair
mittelfränkisch (ripuarisch)|Rip
Düsseldorf/Jülich-Klewe-Berg|Rip
ostfränkisch, omitteldeutsch|Ofr
ostfränkisch, südthüringisch|Ofr
Weferlingen/Mark Brandenburg|Obs
ostmitteldeutsch (schlesisch)|Obs
mitteldeutsch, moselfränkisch|Rip
ostalemannisch, mitteldeutsch|Ohchal
rheinfränkisch (frz. Graphien)|Rip
mittelfränkisch, ostfälisch (?)|Ofr
bairisch (donauländischer Raum)|Mbair
mittelfränkisch, rheinfränkisch|Rip
unterostfränkisch-mitteldeutsch|Obs
alemannisch, rheinfränkisch (?)|Ohchal
ostmitteldeutsch, niederdeutsch|Obs
mittelfränkisch (moselfränkisch?)|Rip
ostfränkisch, nordbairisch, böhmisch|Ofr
bairisch-ostalemannisch (ostschwäbisch)|Ohchal
ostmitteldeutsch (mit bairischen Spuren)|Obs
bairisch (mit schwäbischen Einsprengseln)|Schwaeb
bairisch (östliches oder nördliches Bayern)|Mbair
mittelfränkisch, niederfränkisch, westfälisch|Rip
bairisch (mit mitteldeutschem Einschlag, Sschneider 2005)|Mbair
westniederalemannisch (elsässisch mit bairischem Einschlag)|Els
bairisch (bairisch-mitteldeutscher Grenzraum mit mitteldeutschen Anklängen)|Mbair"""

dial_dict = {l.split('|')[0]:l.split('|')[1] for l in dial_dict.split('\n')}

for i,l in enumerate(merged_NHG):
    if l[1] in date_dict.keys():
        merged_NHG[i][1] = date_dict[l[1]]
    if l[2] in dial_dict.keys():
        merged_NHG[i][2] = dial_dict[l[2]]

gmc_classes = {}
for l in open('pgmc_verb_class.tsv','r'):
    ll=l.strip('\n').split('\t')
    gmc_classes[ll[0]]=ll[1]

inflreplacer = """PastPl1;PastPlInd1
PastPl2;PastPlInd2
PastPl3;PastPlInd3
PastSg1;PastSgInd1
PastSg2;PastSgInd2
PastSg3;PastSgInd3
PresPl1;PresPlInd1
PresPl2;PresPlInd2
PresPl3;PresPlInd3
PresSg1;PresSgInd1
PresSg2;PresSgInd2
PresSg3;PresSgInd3
imp*;impSg.2
impPl;impPl.2
impSg;impSg.2"""

inflreplacer = {l.split(';')[0]:l.split(';')[1] for l in inflreplacer.split('\n')}

for i in range(1,len(merged_NHG)):
    l = merged_NHG[i]
    infl = ''
    if l[4].startswith('VVPP'):
        infl ='ppl'
    if l[4].startswith('VVINF'):
        infl = 'inf'
    if l[4].startswith('VVPS'):
        infl = 'prespl'
    if l[4].startswith('VVFIN'):
        infl = ''
        if 'Pres' in l[5]:
            infl += 'Pres'
        if 'Past' in l[5]:
            infl += 'Past'
        if 'Sg' in l[5]:
            infl += 'Sg'
        if 'Pl' in l[5]:
            infl += 'Pl'
        if 'Ind' in l[5]:
            infl += 'Ind'
        if 'Subj' in l[5] or 'Konj' in l[5]:
            infl += 'Subj'
        if '3' in l[5]:
            infl += '3'
        if '2' in l[5]:
            infl += '2'
        if '1' in l[5]:
            infl += '1'
    if l[4] == 'VVIMP':
        infl = 'imp'+l[5]
    if infl in inflreplacer.keys():
        inflreplacer[infl]
    merged_NHG[i].append(infl)
    merged_NHG[i].append(gmc_classes[l[9]])

form_norm = {}
for i,l in enumerate(merged_NHG):
    if norms[i] != '':
        if l[9] not in form_norm.keys():
            form_norm[l[9]] = {}
        form_norm[l[9]][l[10]] = norms[i]

#form_norm = defaultdict(list)
#for i,l in enumerate(merged_NHG):
#    if norms[i] != '':
#        form_norm[(l[9],l[10])] = norms[i]


for j,l in enumerate(merged_NHG):
    form = l[6]
    if l[7] != '':
        prefix = l[7].strip('= #()')
        stem = l[3]
        inds = np.array([distance(prefix,form[:i])+distance(stem[:1],form[i:i+1]) for i in range(len(form))])
        ind = np.where(inds==inds.min())[0][-1]
        stemmedform = form[ind:]
        if len(stemmedform) > 2:
            form = stemmedform
    merged_NHG[j].append(form)
    cons = l[9][-4]
    if cons == 'w':
        cons = 'hw'
    merged_NHG[j].append(cons)

merged_NHG = [l for l in merged_NHG if l[5] != '*.*.*.*']
#merged_NHG = [l for l in merged_NHG if l[5] != '--']
#merged_NHG = [l for l in merged_NHG if l[5] != '---']
merged_NHG = [l for l in merged_NHG if not l[4].startswith('VVIZ')]
maxl = max([len(l) for l in merged_NHG])
merged_NHG = [l for l in merged_NHG if len(l) == maxl]

merged_NHG = [l for l in merged_NHG if l[1] != '_' and l[1] != '-']

for i,l in enumerate(merged_NHG):
    if l[9] in form_norm.keys() and l[10] in form_norm[l[9]].keys():
        merged_NHG[i].append(form_norm[l[9]][l[10]])
    else:
        merged_NHG[i].append('')

merged_NHG = [['document','date','dialect/place','lemma','POS','infl','form','pref','MHG?','PGmc','inflcat','class','form.normalized','consonant','MHG.norm']]+merged_NHG

f = open('all_data_merged.tsv','w')
for l in merged_NHG:
    print('\t'.join(l),file=f)

f.close()