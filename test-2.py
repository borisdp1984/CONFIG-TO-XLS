import os
import re
import json
from itertools import count
import pandas as pd
import time

os.chdir(r'C:\Users\davide.panzeri\Desktop\Configs\NCS')

filename = [line.rstrip() for line in open('EST-1.txt')]
conf = filename

filteredlines = []
splitted_lists = []
end = {}

for line in conf:
    if re.search(r"^interface|"
                 r"[S-s]ervice-policy.(input|output|in|out).\S+", line):
        b = re.sub("^ +service-policy", "",
                   line)
        filteredlines.append(b)

for s in filteredlines:
    if s == '':
        continue
    if s.startswith('interface'):
        splitted_lists.append([s])
        continue
    splitted_lists[-1].append(s)

#print(splitted_lists)

for lists in splitted_lists:
    keys = lists[0]
    value = lists[1::]
#    cleankey = re.sub("^interface ", "", keys)
    end.update([(keys, value)])



fin = {k: val[0] if len(val) == 1 else val for k, val in end.items()}
final = {k: v for k, v in fin.items() if v != []}

print(final)
e = {}



#print(json.dumps(final, indent=4))
#
# date = time.strftime("%Y-%m-%d_%H-%M-%S")
# df = pd.DataFrame()
# df = df.append(final, ignore_index=True,)
#
# df.to_excel(r'C:\Users\davide.panzeri\Desktop\Router ' + date + '.xlsx',sheet_name='POLICY-MAP', index = True )