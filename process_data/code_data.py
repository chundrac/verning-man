from collections import defaultdict
import re

merged_NHG = [l.strip('\n').split('\t') for l in open('all_data_merged.tsv','r')]

"""
rules: 
expect voiceless (f/v,d,h/hw,s) in pres.ind, pres.subj, inf, imper, present participle, 1/3 sg.past.ind; expect voiced (b,t,g,r) in past.ind.pl, past.subj, ppl
class 1: diphthong in sg.past.ind, monophthong elsewhere in past
class 2: diphthong in pres.sg.ind, mono elsewhere; ô in sg.pret.ind and u in remaining forms
class 3: a in pret.sg.ind, u in other finite forms
classes 4-7 have uniform preterite
"""

envir = """PastPl1;Y
PastPl2;Y
PastPl3;Y
PastPlInd1;Y
PastPlInd2;Y
PastPlInd3;Y
PastPlSubj1;Y
PastPlSubj2;Y
PastPlSubj3;Y
PastSg1;N
PastSg2;Y
PastSg3;N
PastSgInd1;N
PastSgInd2;Y
PastSgInd3;N
PastSgSubj1;Y
PastSgSubj2;Y
PastSgSubj3;Y
PresPl1;N
PresPl2;N
PresPl3;N
PresPlInd1;N
PresPlInd2;N
PresPlInd3;N
PresPlSubj1;N
PresPlSubj2;N
PresPlSubj3;N
PresSg1;N
PresSg2;N
PresSg3;N
PresSgInd1;N
PresSgInd2;N
PresSgInd3;N
PresSgSubj1;N
PresSgSubj2;N
PresSgSubj3;N
imp*;N
impPl;N
impPl.1;N
impPl.2;N
impSg;N
impSg.2;N
impSg.3;N
inf;N
ppl;Y
prespl;N"""

envir = {l.split(';')[0]:l.split(';')[1] for l in envir.split('\n')}

for j,l in enumerate(merged_NHG):
    if j > 0:
        form = l[12].lower()
        if 'fr' in l[9]:
            form = form[2:]
        if l[13] == 'f':
            reflex = ''
            if 'b' in form or 'p' in form:
                reflex = 'b'
            else:
                reflex = 'f'
            if envir[l[10]] == 'Y':
                if reflex == 'b':
                    merged_NHG[j] += ['b','b','conservative']
                if reflex == 'f':
                    merged_NHG[j] += ['f','b','innovative']
            else:
                if reflex == 'b':
                    merged_NHG[j] += ['b','f','innovative']
                if reflex == 'f':
                    merged_NHG[j] += ['f','f','conservative']
        if l[13] == 'þ':
            reflex = ''
            if 't' in form and 'd' not in form[1:]:
                reflex = 't'
            else:
                reflex = 'd'
            if envir[l[10]] == 'Y':
                if reflex == 't':
                    merged_NHG[j] += ['t','t','conservative']
                if reflex == 'd':
                    merged_NHG[j] += ['d','t','innovative']
            else:
                if reflex == 't':
                    merged_NHG[j] += ['t','d','innovative']
                if reflex == 'd':
                    merged_NHG[j] += ['d','d','conservative']
        if l[13] == 'h' or l[13] == 'hw':
            reflex = ''
            if 'g' in form[1:].replace('sch','') or 'c' in form[1:].replace('sch',''):
                if 'ch' not in form.replace('sch',''):
                    reflex = 'g'
                else:
                    reflex = 'h'
            else:
                reflex = 'h'
            print(form,reflex)
            if envir[l[10]] == 'Y':
                if reflex == 'g':
                    merged_NHG[j] += ['g','g','conservative']
                if reflex == 'h':
                    merged_NHG[j] += ['h','g','innovative']
            else:
                if reflex == 'g':
                    merged_NHG[j] += ['g','h','innovative']
                if reflex == 'h':
                    merged_NHG[j] += ['h','h','conservative']
        if l[13] == 's':
            reflex = ''
            if 'r' in form[1:]:
                reflex = 'r'
            elif 's' not in form[1:] and 'z' not in form[1:]:
                reflex = 'r'
            else:
                reflex = 's'
            if envir[l[10]] == 'Y':
                if reflex == 'r':
                    merged_NHG[j] += ['r','r','conservative']
                else:
                    merged_NHG[j] += ['s','r','innovative']
            else:
                if reflex == 'r':
                    merged_NHG[j] += ['r','s','innovative']
                else:
                    merged_NHG[j] += ['s','s','conservative']


"""
present:
                    
Class II: eu/iu/iv in prs.ind.sg and imp.sg versus /ie/ elsewhere in present
Class IV and Class V
                    
                    i ~ e in 1sgpres
VI and VII: loss of umlaut in 2/3 pres sg

preterite:
Class I: ai -> i in past.sg.ind versus i (~ ai) in other
Class II: o ~ u in past.sg.ind; u ~ o in other forms
Class III: a in pst.sg.ind versus u in other forms
Class IV-V: a ~ â in past, o in ppl
VI: u in past, a in ppl
VII: i(e) in past, a in ppl

"""
                    
# ['PastPl1', 'PastPl2', 'PastPl3', 'PastPlInd1', 'PastPlInd2', 'PastPlInd3', 'PastPlSubj1', 'PastPlSubj2', 'PastPlSubj3', 'PastSg1', 'PastSg2', 'PastSg3', 'PastSgInd1', 'PastSgInd2', 'PastSgInd3', 'PastSgSubj1', 'PastSgSubj2', 'PastSgSubj3', 'PresPl1', 'PresPl2', 'PresPl3', 'PresPlInd1', 'PresPlInd2', 'PresPlInd3', 'PresPlSubj1', 'PresPlSubj2', 'PresPlSubj3', 'PresSg1', 'PresSg2', 'PresSg3', 'PresSgInd1', 'PresSgInd2', 'PresSgInd3', 'PresSgSubj1', 'PresSgSubj2', 'PresSgSubj3', 'imp*', 'impPl', 'impPl.1', 'impPl.2', 'impSg', 'impSg.2', 'impSg.3', 'inf', 'ppl', 'prespl']

for j,l in enumerate(merged_NHG):
    if j > 0:
        form = l[12]
        if l[11] == '1':
            if l[10] in ['PastSg1', 'PastSg3', 'PastSgInd1', 'PastSgInd3']:
                if 'ei' in form or 'ey' in form or 'ai' in form or 'ay' in form or 'i' not in form:
                    #    merged_NHG[j] += ['ei','ei','conservative']
                    if 'y' not in form:
                        merged_NHG[j] += ['ei','ei','conservative']
                    else:
                        merged_NHG[j] += ['ie','ei','innovative']
                else:
                    merged_NHG[j] += ['ie','ei','innovative']
            if l[10] in ['PastSg2', 'PastSgInd2', 'PastPl1', 'PastPl2', 'PastPl3', 'PastPlInd1', 'PastPlInd2', 'PastPlInd3', 'PastPlSubj1', 'PastPlSubj2', 'PastPlSubj3', 'PastSgSubj1', 'PastSgSubj2', 'PastSgSubj3', 'ppl']:
                if 'ei' in form or 'ey' in form or 'ai' in form or 'ay' in form or 'i' not in form:
                    #    merged_NHG[j] += ['ei','ie','innovative']
                    if 'y' not in form:
                        merged_NHG[j] += ['ei','ie','innovative']
                    else:
                        merged_NHG[j] += ['ie','ie','conservative']
                else:
                    merged_NHG[j] += ['ie','ie','conservative']
            #else:
            #    merged_NHG[j] += ['--','--']
        if l[11] == '2':
            if l[10] in ['PresSg1', 'PresSg2', 'PresSg3','PresSgInd1', 'PresSgInd2', 'PresSgInd3','imp','impSg', 'impSg.2', 'impSg.3']:
                if 'ie' in form or 'ei' in form:
                    merged_NHG[j] += ['ie','eu','innovative']
                elif 'i' in form and 'u' not in form and 'v' not in form and 'ü' not in form and 'w' not in form:
                    merged_NHG[j] += ['ie','eu','innovative']
                elif 'e' in form and 'u' not in form and 'v' not in form and 'ü' not in form and 'w' not in form:
                    merged_NHG[j] += ['ie','eu','innovative']
                else:
                    merged_NHG[j] += ['eu','eu','conservative']
            ##
            ##
            if l[10] in ['PresPl1', 'PresPl2', 'PresPl3', 'PresPlInd1', 'PresPlInd2', 'PresPlInd3', 'PresPlSubj1', 'PresPlSubj2', 'PresPlSubj3', 'impPl', 'impPl.1', 'inf', 'prespl']:
                if 'ie' in form or 'ei' in form:
                    merged_NHG[j] += ['ie','ie','conservative']
                elif 'i' in form and 'u' not in form and 'v' not in form and 'ü' not in form and 'w' not in form:
                    merged_NHG[j] += ['ie','ie','conservative']
                elif 'e' in form and 'u' not in form and 'v' not in form and 'ü' not in form and 'w' not in form:
                    merged_NHG[j] += ['ie','ie','conservative']
                else:
                    merged_NHG[j] += ['eu','ie','innovative']
            ##
            ##
            if l[10] in ['PastPl1', 'PastSg2', 'PastSgInd2', 'PastPl2', 'PastPl3', 'PastPlInd1', 'PastPlInd2', 'PastPlInd3', 'PastPlSubj1', 'PastPlSubj2', 'PastPlSubj3', 'PastSgSubj1', 'PastSgSubj2', 'PastSgSubj3']:
                if 'u' in form and 'o' not in form:
                    merged_NHG[j] += ['u','u','conservative']
                elif 'ü' in form and 'o' not in form:
                    merged_NHG[j] += ['u','u','conservative']
                else:
                    merged_NHG[j] += ['o','u','innovative']
            ##
            ##
            if l[10] in ['PastSg1', 'PastSg3', 'PastSgInd1', 'PastSgInd3']:
                if 'u' in form and 'o' not in form:
                    merged_NHG[j] += ['u','o','innovative']
                elif 'ü' in form and 'o' not in form:
                    merged_NHG[j] += ['u','o','innovative']
                else:
                    merged_NHG[j] += ['o','o','conservative']
            ##
            ##
            if l[10] in ['ppl']:
                if 'o' in form:
                    merged_NHG[j] += ['o','o','conservative']
                else:
                    merged_NHG[j] += ['?','o','innovative']
        if l[11] == '3':
            if l[10] in ['PastSg1', 'PastSg3', 'PastSgInd1', 'PastSgInd3']:
                if 'a' in form and 'u' not in form:
                    merged_NHG[j] += ['a','a','conservative']
                else:
                    merged_NHG[j] += ['u','a','innovative']
            if l[10] in ['PastPl1', 'PastPl2', 'PastSg2', 'PastSgInd2', 'PastPl3', 'PastPlInd1', 'PastPlInd2', 'PastPlInd3', 'PastPlSubj1', 'PastPlSubj2', 'PastPlSubj3', 'PastSgSubj1', 'PastSgSubj2', 'PastSgSubj3', 'ppl']:
                if 'a' in form and 'u' not in form:
                    merged_NHG[j] += ['a','u','innovative']
                else:
                    merged_NHG[j] += ['u','u','conservative']



                
forms = defaultdict(list)
maxline = max([len(l) for l in merged_NHG])
for j,l in enumerate(merged_NHG):
    if j > 0:
        if len(l) < maxline:
            forms[tuple(l[9:12])].append(l[12])

forms_ = {}
for k in forms.keys():
    vows = []
    for v in forms[k]:
        if k[1] == 'ppl' and v.startswith('ge'):
            v = v[2:]
        splitform = re.split(r'b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|x|z|ß|w|\W',v)
        if len([s for s in splitform if s != '']) > 0:
            splitform = [s for s in splitform if s != ''][0]
        else:
            splitform = ''
        vows.append(splitform)
    vows = sorted(vows,key=lambda x:vows.count(x))[-1]
    forms_[k] = vows

for j,l in enumerate(merged_NHG):
    if j > 0:
        if len(l) < maxline:
            merged_NHG[j] += [forms_[tuple(l[9:12])],forms_[tuple(l[9:12])],'conservative']




#for j,l in enumerate(merged_NHG):
#    if j > 0:
#        if len(l) < maxline:
#            form = l[12].lower().replace('uu','w').replace('eue','ewe').replace('eie','eje').replace('eua','ewa')
#            form_ = l[6].lower().replace('uu','w').replace('eue','ewe').replace('eie','eje').replace('eua','ewa')
#            if l[10] == 'ppl':
#                if form.startswith('ge'):
#                    form = form[2:]
#                if form_.startswith('ge'):
#                    form_ = form_[2:]
#            if 'a' in form or 'e' in form or 'i' in form or 'o' in form or 'u' in form or 'y' in form:
#                splitform = re.split(r'b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|v|x|z|ß|w|\W',form)
#            elif 'v' in form:
#                splitform = re.split(r'b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|x|z|ß|w|\W',form)
#            elif 'a' in l[6] or 'e' in l[6] or 'i' in l[6] or 'o' in l[6] or 'u' in l[6] or 'y' in l[6] or 'v' in l[6]:
#                splitform = re.split(r'b|c|d|f|g|h|j|k|l|m|n|p|q|r|s|t|x|z|ß|w|\W',l[6].lower())
#            else:
#                splitform = ['?']
#            splitform = [s for s in splitform if s != ''][0]
#            merged_NHG[j] += [splitform,'---']

#[l for l in merged_NHG if l[11]=='1']
#merged_NHG = [l[:14] for l in merged_NHG]



merged_NHG[0] = ['document', 'date', 'dialect/place', 'lemma', 'POS', 'infl', 'form', 'pref', 'MHG?', 'PGmc', 'inflcat', 'class', 'form.norm', 'cons', 'MHG.norm', 'C.obs', 'C.exp', 'C.coding', 
'V.obs', 'V.exp', 'V.coding']

merged_NHG = [l for l in merged_NHG if l[1] != '_']

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

for i,l in enumerate(merged_NHG):
    if l[10] in inflreplacer.keys():
        merged_NHG[i][10] = inflreplacer[l[10]]

#etyma = ['fleuhaną','freusaną','lesaną','leusaną','līhwaną','nesaną','rīhaną','rīsaną','sehwaną','sīhwaną','slahaną','teuhaną','tīhaną','þinhaną','þwinhaną']

merged_NHG = [merged_NHG[0]]+[l for l in merged_NHG[1:] if l[9] != 'habjan-']


f = open('verner_data.tsv','w')
for l in merged_NHG:
    print('\t'.join(l),file=f)


f.close()