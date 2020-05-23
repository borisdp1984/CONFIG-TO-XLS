import os
import re
import json
from itertools import count

os.chdir(r'C:\Users\davide.panzeri\Desktop\Configs\NCS')

filename = [line.rstrip() for line in open('EST-1.txt')]

filteredlines = []
action = []
First_Split = []
Second_Split = []
dct = {}
mainlst =  []
final = {}

for line in filename:
    if re.search(r"^policy-map \S+"
                 r"|^ +[C-c]lass.\S+.\S+"
                 r"|^ +[P-p]riority.\S+.\S+"
                 r"|^ +[P-p]olice.\S+.\S+.\S+"
                 r"|^ +[S-s]hape.\S+.\S+.\S+.\S+"
                 r"|set.\S+.\S+.\S+.\S+"
                 r"|^ +[B-b]andwidth.\S+.\S+.\S+"
                 r"|^ +(service-policy.(?!input|output)\S+)"
                 r"|^ +[C-c]onform-action.\S+."
                 r"|^ +[E-e]xceed-action.\S+", line):
        b = re.sub("^ +", "", line)
        filteredlines.append(b)

for element in filteredlines:
    if element.startswith('class'):
        action.append(element)
        action.append('actions')
    else:
        action.append(element)

for s in action:
    if s == '':
        continue
    if s.startswith('policy-map') or len(First_Split) == 0:
        First_Split.append([s])
        continue
    First_Split[-1].append(s)

# print(First_Split)
# print()

for sublist in First_Split:
    startclass = 1
    startcact = 1
    incrcact = count(startcact)
    incrclass = count(startclass)
    container = []
    for s in sublist:
        if s == '':
            continue
        if s.startswith('policy-map'):
            container.append(s.split())
            continue
        if s.startswith('class'):
            numclass = re.sub(r'^class', lambda x: x.group(0) + '-' + str(next(incrclass)), s)
            container.append(numclass.split())
            continue
        if s.startswith('action'):
            numcact = re.sub(r'^actions', lambda x: x.group(0) + '-' + str(next(incrcact)), s)
            container.append(numcact.split())
            continue
        container[-1].append(s)
    Second_Split.append(container)

# print(Second_Split)
# print()

for lines in Second_Split:
   print(lines)



for lists in Second_Split:
    dct = {}
    for sublst in lists:
        keys = sublst[0]
        value = sublst[1::]
    dct.update([(keys, value)])
    mainlst.append(dct)

# final = {k: val[0] if len(val) == 1 else val for k, val in dct.items()}

# print()
print(mainlst)
# print(final)
# print(json.dumps(final, indent=4))
