# import module
from wifi import Cell, Scheme
 
# scan available Wifi networks
raw_networks = list(Cell.all('wlan0'))
networks = []
ssids = set()
for network in raw_networks:
    if network.ssid not in ssids:
        networks.append(network)
        ssids.add(network.ssid)
