import os
import textfsm

os.chdir(r'C:\Users\davide.panzeri\Desktop\Configs\NCS')

input_file = open('EST-1.txt')
cli_data = input_file.read()
input_file.close()

with open(r'C:\CONFIG-TO-XLS\TEMPLATES\POLICY-MAP') as f:
    template = textfsm.TextFSM(f)
    fsm_results = template.ParseText(cli_data)

print(fsm_results)
