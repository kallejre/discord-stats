"""Discordi sõnapilve statistika."""

import re

pattern = re.compile('[\W_]+')
f = open('disc_sõnapilveks.txt', encoding='utf-8')
s = f.read()
f.close()
print(len(s))
print(s.count(' '))
for symb in '-_.:,;~<>|+?´`=()!"¤%&/\\\'*':
    s = s.replace(symb, ' ')
print(s.count(' '))
for i in range(15):
    s = s.replace('\n\n', '\n')
    s = s.replace('  ', ' ')
    s = s.replace('\n ', '\n')
    s = s.replace(' \n', '\n')
print(len(s))
print(s.count(' '))
for i in range(100):
    s = s.replace('  ', ' ')
print(len(s))
print(s.count(' '))
print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
a = s.split()
d = set(a)
q = dict()
for i in d:
    q[i] = a.count(i)
    if q[i] > 5 and len(i) > 2:
        try:
            print(i, q[i], sep='\t')
        except:
            print('\t', q[i], sep='')
