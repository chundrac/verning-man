allfeats = [l.strip('\n').split('\t') for l in open('fuerstinnen_data.tsv','r')]

data = [l for l in allfeats if l[6].startswith('VV')]

data = [[l[i] for i in [0,1,2,3,5,6,7]] for l in data]

for i,l in enumerate(data):
    data[i][1] = l[1].split('.')[-1]

f = open('fuerstinnen_verbs.tsv','w')
for l in data:
    print('\t'.join(l),file=f)

f.close()