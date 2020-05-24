import outputtojson
import os
import json

os.chdir(r'C:\Users\davide.panzeri\Desktop\Configs\NCS')

fi = [line.rstrip() for line in open('EST-2.txt')]

config = outputtojson.OutputToJson(fi)

hostname = config.hostname_to_json()
ipadd = config.int_ip_to_json()
policymap = config.policymap_to_json()

print(hostname)
print()
print(ipadd)
print()
print(policymap)
