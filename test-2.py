import re
import pandas as pd
import time
import json
from itertools import count

policycomplete = ['policy-map SET_DIGITEN', 'class DIGITEN-103', 'police cir 4000000000 4000000000',
                  'conform-action set qos-group 5', 'conform-action set mpls experimental imposition 5',
                  'exceed-action drop', 'class DIGITEN-101', 'police cir 1000000000', 'conform-action set qos-group 5',
                  'conform-action set mpls experimental imposition 5', 'exceed-action drop', 'class DIGITEN-115',
                  'police cir 600000000', 'conform-action set mpls experimental imposition 5',
                  'conform-action set qos-group 5', 'exceed-action drop', 'class DIGITEN-119', 'police cir 600000000',
                  'conform-action set qos-group 5', 'conform-action set mpls experimental imposition 5',
                  'exceed-action drop', 'class DIGITEN-123', 'police cir 600000000',
                  'conform-action set mpls experimental imposition 5', 'conform-action set qos-group 5',
                  'exceed-action drop', 'class DIGITEN-125', 'police cir 600000000',
                  'conform-action set mpls experimental imposition 5', 'conform-action set qos-group 5',
                  'exceed-action drop', 'class DIGITEN-121', 'police cir 600000000',
                  'conform-action set mpls experimental imposition 5', 'conform-action set qos-group 5',
                  'exceed-action drop']


action = []
for element in policycomplete:
    if element.startswith('class'):
        action.append(element)
        action.append('actions')
    else:
        action.append(element)

startclass = 1
incrclass = count(startclass)
startcact = 1
incrcact = count(startclass)



splitted_lists = []

for s in action:
    if s == '':
        continue
    if s.startswith('policy-map') or len(splitted_lists) == 0:
        splitted_lists.append(s.split())
        continue
    if s.startswith('class') or len(splitted_lists) == 0:
        numclass = re.sub(r'^class', lambda x: x.group(0) + '-' + str(next(incrclass)), s)
        splitted_lists.append(numclass.split())
        continue
    if s.startswith('action') or len(splitted_lists) == 0:
        numcact = re.sub(r'^actions', lambda x: x.group(0) + '-' + str(next(incrcact)), s)
        splitted_lists.append(numcact.split())
        continue
    splitted_lists[-1].append(s)

end = {}

for lists in splitted_lists:
    keys = lists[0]
    value = lists[1::]
    end.update([(keys, value)])

final = {k: val[0] if len(val) == 1 else val for k, val in end.items()}


print(splitted_lists)
print()
print(final)
print(json.dumps(final, indent=2))

date = time.strftime("%Y-%m-%d_%H-%M-%S")
df = pd.DataFrame(final, columns=end.keys())
#df = df.append(final, ignore_index=True)
print(df.to_string)
df.to_excel(r'C:\Users\davide.panzeri\Desktop\Router ' + date + '.xlsx',sheet_name='POLICY-MAP', index = True )
