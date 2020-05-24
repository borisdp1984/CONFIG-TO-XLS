import re
from itertools import count


class OutputToJson:
    def __init__(self, config):
        self.config = config

    def hostname_to_json(self):
        hostname = []
        end = {}
        # Find line with keyword "hostname" transform
        # in Dictionary and update the end  dictionary named "final"
        # received = self.config
        conf = self.config
        for line in conf:
            if re.search("^hostname", line):
                hostname.append(line)
        for s in hostname:
            spl = s.split()
            op = {spl[i]: spl[i + 1] for i in range(0, len(spl), 2)}
            end.update(op)
        return end

    def int_ip_to_json(self):
        filteredlines = []
        splitted_lists = []
        end = {}
        subnet_dict = {
            ' 0.0.0.0': '/0', ' 128.0.0.0': '/1 ', ' 192.0.0.0': '/2 ', ' 224.0.0.0': '/3 ', ' 240.0.0.0': '/4 ',
            ' 248.0.0.0': '/5 ', ' 252.0.0.0': '/6 ', ' 254.0.0.0': '/7 ', ' 255.0.0.0': '/8 ', ' 255.128.0.0': '/9 ',
            ' 255.192.0.0': '/10', ' 255.224.0.0': '/11', ' 255.240.0.0': '/12', ' 255.248.0.0': '/13',
            ' 255.252.0.0': '/14', ' 255.254.0.0': '/15', ' 255.255.0.0': '/16', ' 255.255.128.0': '/17',
            ' 255.255.192.0': '/18', ' 255.255.224.0': '/19', ' 255.255.240.0': '/20', ' 255.255.248.0': '/21',
            ' 255.255.252.0': '/22', ' 255.255.254': '/23', ' 255.255.255.0': '/24', ' 255.255.255.128': '/25',
            ' 255.255.255.192': '/26', ' 255.255.255.224': '/27', ' 255.255.255.240': '/28', ' 255.255.255.248': '/29',
            ' 255.255.255.252': '/30', ' 255.255.255.254': '/31', ' 255.255.255.255': '/32'}
        # Find line with keyword "interface" or "ip[v4] address X.X.X.X. Y.Y.Y.Y"
        # or "ip[v4] address X.X.X.X. Y.Y.Y.Y secondary"
        # remove the words "ip address" from the string transform
        # the result in a list named filteredlines
        conf = self.config
        for line in conf:
            if re.search(r"^interface|"
                         r"ip address \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$|"
                         r"ip address \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} secondary$|"
                         r"ipv4 address \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$|"
                         r"ipv4 address \d{1,3}\.\d{1,3}\.\d{1,3}\."
                         r"\d{1,3} \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} secondary$|"
                         r" no ip address$", line):
                b = re.sub("^ +ip address |^ip address|^ipv4 address|^ +ipv4 address| point-to-point$| secondary$", "",
                           line)
                filteredlines.append(b)
        # change the subnet mask With prefix mask
        for i, word in enumerate(filteredlines):
            for key in subnet_dict:
                filteredlines[i] = filteredlines[i].replace(key, subnet_dict.get(key))
        masktoprefix = filteredlines
        # Split the list in sublist with interface an his ip addresses
        for s in masktoprefix:
            if s == '':
                continue
            if s.startswith('interface') or len(splitted_lists) == 0:
                splitted_lists.append([s])
                continue
            splitted_lists[-1].append(s)
        # remove the interface that don't have any ip address
        onlywithip = [x for x in splitted_lists if x != ' no ip address']
        # Create a Dictionary with KEY = Interface and VALUES = Ip address of the interface
        for lists in onlywithip:
            keys = lists[0]
            value = lists[1::]
            cleankey = re.sub("^interface | point-to-point$", "", keys)
            end.update([(cleankey, value)])
        fin = {k: val[0] if len(val) == 1 else val for k, val in end.items()}
        final = {k: v for k, v in fin.items() if v != []}
        return final

    def policymap_to_json(self):
        received = self.config
        filteredline = []
        action = []
        first_split = []
        second_split = []
        end = []
        for line in received:
            if re.search(r"^policy-map \S+"
                         r"|^ +[C-c]lass.\S+.\S+"
                         r"|^ +[P-p]riority.\S+.\S+"
                         r"|^ +[P-p]olice.\S+.\S+.\S+"
                         r"|^ +[S-s]hape.\S+.\S+.\S+.\S+"
                         r"|set.(ip.(?!next-hop|local-preference)|"
                         r"atm-clp|cos|discard-class|dscp|fr-de|mpls|precedence|"
                         r"qos-group|srp-priority|traffic-class).\S+"
                         r"|^ +[B-b]andwidth.\S+.\S+.\S+"
                         r"|^ +(service-policy.(?!input|output|in|out)\S+)"
                         r"|^ +[C-c]onform-action.\S+."
                         r"|^ +[Q-q]ueue-limit.\S+.\S+"
                         r"|^ +[F-f]air-queue"
                         r"|^ +[E-e]xceed-action.\S+", line):
                b = re.sub("^ +", "", line)
                filteredline.append(b)

        for element in filteredline:
            if element.startswith('class'):
                action.append(element)
                action.append('actions')
            else:
                action.append(element)

        for s in action:
            if s == '':
                continue
            if s.startswith('policy-map') or len(first_split) == 0:
                first_split.append([s])
                continue
            first_split[-1].append(s)

        for sublist in first_split:
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
            second_split.append(container)

        for lists in second_split:
            subdict = {}
            final = {}
            for element in lists:
                keys = element[0]
                value = element[1::]
                subdict.update([(keys, value)])
                final = {k: val[0] if len(val) == 1 else val for k, val in subdict.items()}
            end.append(final)
        return end
