import re
import pandas as pd
import time
import json


policycomplete = ['policy-map SET_DIGITEN', 'class DIGITEN-103', 'police cir 4000000000 4000000000', 'conform-action set qos-group 5', 'conform-action set mpls experimental imposition 5', 'exceed-action drop', 'class DIGITEN-101', 'police cir 1000000000', 'conform-action set qos-group 5', 'conform-action set mpls experimental imposition 5', 'exceed-action drop', 'class DIGITEN-115', 'police cir 600000000', 'conform-action set mpls experimental imposition 5', 'conform-action set qos-group 5', 'exceed-action drop', 'class DIGITEN-119', 'police cir 600000000', 'conform-action set qos-group 5', 'conform-action set mpls experimental imposition 5', 'exceed-action drop', 'class DIGITEN-123', 'police cir 600000000', 'conform-action set mpls experimental imposition 5', 'conform-action set qos-group 5', 'exceed-action drop', 'class DIGITEN-125', 'police cir 600000000', 'conform-action set mpls experimental imposition 5', 'conform-action set qos-group 5', 'exceed-action drop', 'class DIGITEN-121', 'police cir 600000000', 'conform-action set mpls experimental imposition 5', 'conform-action set qos-group 5', 'exceed-action drop']

date = time.strftime("%Y-%m-%d_%H-%M-%S")

end = {}
splitted_lists = []

for s in policycomplete:
    if s == '':
        continue
    if s.startswith('policy-map') or len(splitted_lists) == 0:
        splitted_lists.append(s.split())
        continue
    if s.startswith('class') or len(splitted_lists) == 0:
        splitted_lists.append([s])
        continue
    splitted_lists[-1].append(s)

for lists in splitted_lists:
    keys = lists[0]
    value = lists[1::]
    end.update([(keys, value)])


final = {k: val[0] if len(val) == 1 else val for k, val in end.items()}

print(json.dumps(final, indent=2))


# df = pd.DataFrame()
# df = df.append(final, ignore_index=True)
# df.to_excel(r'C:\Users\davide.panzeri\Desktop\Router ' + date + '.xlsx',sheet_name='POLICY-MAP', index = True )

