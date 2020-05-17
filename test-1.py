import os
import re

os.chdir(r'C:\Users\davide.panzeri\Desktop\Configs\NCS')

filename = [line.rstrip() for line in open('EST-1.txt')]

filteredlines = []

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

#print(filteredlines)

splitted_lists = []

for s in filteredlines:
    if s == '':
        continue
    if s.startswith('policy-map') or len(splitted_lists) == 0:
        splitted_lists.append([s])
        continue
    splitted_lists[-1].append(s)

for lines in splitted_lists:
    print(lines)

