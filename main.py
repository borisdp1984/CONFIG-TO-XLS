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
for each in policycomplete:
    if each.startswith('class'):
        action.append(each)
        action.append('action')
    else:
        action.append(each)




print(policycomplete)
print()
print(action)
