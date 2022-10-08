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

selected=False
while selected == False: 
    for i,v in enumerate(output):
        print(f'{i}: {v}')

    selection = int(input("Enter the number of the network you'd like to connect to: "))

    try:
        output[selection]
    except:
        print('Please make a valid selection')
    else: 
        scheme = Scheme.find('wlan0', 'home')
        if not scheme:
            password = input(f'Please enter the password for "{output[selection]}": ')
            try:
                scheme = Scheme.for_cell('wlan0', output[selection], networks[output[selection]], password)
                scheme.save()
            except Exception as e:
                print(e)

        try:
            scheme.activate()
        except Exception as e:
            print(e)
        else:
            selected = True
            print("Connected")

