import os
import re
import json
from itertools import count
import pandas as pd
import time

os.chdir(r'C:\Users\davide.panzeri\Desktop\Configs\NCS')

filename = [line.rstrip() for line in open('EST-2.txt')]

filteredlines = []
action = []
First_Split = []
Second_Split = []
end = []

for line in filename:
    if re.search(r"^policy-map \S+"
                 r"|^ +[C-c]lass.\S+.\S+"
                 r"|^ +[P-p]riority.\S+.\S+"
                 r"|^ +[P-p]olice.\S+.\S+.\S+"
                 r"|^ +[S-s]hape.\S+.\S+.\S+.\S+"
                 r"|set.(ip.(?!next-hop|local-preference)|"
                 r"atm-clp|cos|discard-class|dscp|fr-de|mpls|precedence|qos-group|srp-priority|traffic-class).\S+"
                 r"|^ +[B-b]andwidth.\S+.\S+.\S+"
                 r"|^ +(service-policy.(?!input|output|in|out)\S+)"
                 r"|^ +[C-c]onform-action.\S+."
                 r"|^ +[Q-q]ueue-limit.\S+.\S+"
                 r"|^ +[F-f]air-queue"
                 r"|^ +[E-e]xceed-action.\S+", line):
        b = re.sub("^ +", "", line)
        filteredlines.append(b)

print(filteredlines)

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

for lists in Second_Split:
    subdict = {}
    final = {}
    for element in lists:
        keys = element[0]
        value = element[1::]
        subdict.update([(keys, value)])
        final = {k: val[0] if len(val) == 1 else val for k, val in subdict.items()}
    end.append(final)

print(json.dumps(end, indent=4))

date = time.strftime("%Y-%m-%d_%H-%M-%S")
df = pd.DataFrame()
df = df.append(end, ignore_index=True,)

df.to_excel(r'C:\Users\davide.panzeri\Desktop\Router ' + date + '.xlsx',sheet_name='POLICY-MAP', index = True )
