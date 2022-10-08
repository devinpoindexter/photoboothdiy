# import module
from re import I
from wifi import Cell, Scheme
 
# scan available Wifi networks
raw_networks = list(Cell.all('wlan0'))
networks = dict()
for network in raw_networks:
    if network.ssid not in networks.keys():
        networks[network.ssid] = network


output = list(networks.keys())

for i,v in enumerate(output):
    print(f'{i}:{v}')

selection = input()

if output[selection]:
    Print(f'Connecting to {output[selection]}')
else:
    print('Please make a valid selection')
