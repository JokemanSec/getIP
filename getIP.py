#!/usr/bin/env python3
# Creator: Jokeman
import os, sys, socket, json
from urllib.request import urlopen
from urllib.error import URLError

# header
if sys.platform == "linux" or sys.platform == "linux2":
    os.system('clear')
elif sys.platform == "win32":
    os.system('cls')
print('#' * 5 + ' IP Finder by J0k3m4n ' + '#' * 5)


# help screen
def help():
    sys.exit("\nUsage: "
             "\n         python3 getIP.py"
             "\n         python3 getIP.py [hostname]"
             "\n")


# check for internet connection
def internet_check():
    print("\nChecking internet connection...")
    try:
        urlopen('https://www.google.com', timeout=10)
        return
    except URLError:
        sys.exit("\nPlease connect your device to the internet to use this script"
                 "\nOr is your internet really that slow? oO")
    except:
        sys.exit("\nSomething went wrong at our end, please start a issue # at "
                 "https://github.com/JokemanSec/getIP/issues")


# get IP from hostname
def get_ip():
    try:
        ip = socket.gethostbyname(name)
        print(f'\nIP: {ip}')
        geolocate(ip)
    except socket.gaierror:
        sys.exit("\n\033[91mError: wrong input, check \033[1mpython3 getIP.py -h")
    except KeyError:
        sys.exit("\nDid you enter a local ip address? If not please start a issue # at "
                 "https://github.com/JokemanSec/getIP/issues")
    except:
        sys.exit("\nSomething went wrong at our end, please start a issue # at "
                 "https://github.com/JokemanSec/getIP/issues")


# lookup the location of the obtained ip address
def geolocate(ip):
    print(f'Locating {ip}...')

    response = urlopen(f'https://ipinfo.io/{ip}/json')
    data = json.load(response)

    hostname = data['hostname']
    city = data['city']
    region = data['region']
    country = data['country']
    location = data['loc']
    organisation = data['org']
    postal = data['postal']
    timezone = data['timezone']

    sys.exit(f'Successfully located IP: \n\n'

             f'hostname: {hostname}\n'
             f'organisation: {organisation}\n'
             f'address: ({postal}) {city}, {region}, {country}\n'
             f'coordinates: {location}\n'
             f'timezone: {timezone}\n\n'

             f'Please keep in mind that the coordinates do not show the exact location of {ip} but of {city}'
             )


def main():
    internet_check()

    global name
    try:
        name = sys.argv[1]

        if name in ['--help', '-h']:
            help()
    except IndexError:
        name = input('\nEnter an IP Address or Hostname: ')

    get_ip()


# constructor
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\n\n\033[91muser exit: KeyboardInterrupt')
