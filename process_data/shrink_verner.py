text = []
for l in open('verner_data.tsv','r'):
    text.append(l.strip('\n').split('\t'))

text = [l for l in text if l[11] in ['class','1','2']]

sorted(set([l[9] for l in text]))

text = [l for l in text if l[13]!='þ']

f = open('verner_data_for_analysis.tsv','w')
for l in text:
    print('\t'.join(l),file=f)

f.close()