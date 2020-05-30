import outputtojson
import os
import json
import time
import pandas as pd

os.chdir(r'C:\Users\davide.panzeri\Desktop\Configs\NCS')

fi = [line.rstrip() for line in open('EST-2.txt')]
date = time.strftime("%Y-%m-%d_%H-%M-%S")

config = outputtojson.OutputToJson(fi)

hostname = config.hostname_to_json()
ipadd = config.int_ip_to_json()
policymap = config.policymap_to_json()

print(hostname)
print()
print(ipadd)
print()
print(policymap)
print()


# df1 = pd.DataFrame(hostname)
# df2 = pd.DataFrame(ipadd, ignore_index=True,)
# df3 = df.
#
# df.to_excel(r'C:\Users\davide.panzeri\Desktop\Router ' + date + '.xlsx',sheet_name='POLICY-MAP', index = True )