#!/usr/bin/env python3
import os, sys, socket, json, getopt
from urllib.request import urlopen
from urllib.error import URLError


def header():
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system('clear')
    elif sys.platform == "win32":
        os.system('cls')
    print('#' * 5 + ' IP Finder by J0k3m4n ' + '#' * 5)


# help screen
def help():
    sys.exit("\nUsage: "
             "\n         python3 getIP.py"
             "\n         python3 getIP.py [-hsig] [-t {target}]"

             "\n\nOPTIONS:"
             "\n         -h | --help : shows this help dialog"
             "\n         -s | --simple : returns the IP and nothing else"
             "\n         -i | --no-internet-check : skips the internet check; use it if your connection is slow"
             "\n         -g | --geolocate : locate the found IP afterwards"
             "\n         -t | --target : specifies the target; it can be a hostname or an IP")


# check for internet connection
def internet_check():
    print("\nChecking internet connection...")
    try:
        urlopen('https://www.google.com', timeout=10)
        return
    except URLError:
        sys.exit("\nPlease connect your device to the internet to use this script"
                 "\nOr is your response time > 10000ms? Then use -s to skip the internet check")
    except:
        sys.exit("\nSomething went wrong at our end, please start a issue # at "
                 "https://github.com/JokemanSec/getIP/issues")


# get IP from hostname
def get_ip(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        sys.exit("\n\033[91mError: wrong input, check \033[1mpython3 getIP.py -h")
    except:  # handle unexpected Exceptions
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

    print(f'Successfully located IP: \n\n'

          f'hostname: {hostname}\n'
          f'organisation: {organisation}\n'
          f'address: ({postal}) {city}, {region}, {country}\n'
          f'coordinates: {location}\n'
          f'timezone: {timezone}\n\n'

          f'Please keep in mind that the coordinates do not show the exact location of {ip} but of {city}'
          )


def main(argv):

    try:
        opts, args = getopt.getopt(argv, shortopts="hsigt:", longopts=["help", "simple", "no-internet-check",
                                                                       "geolocate", "hostname="])
    except getopt.GetoptError:
        print('ERROR: option not found')
        help()

    # args is thrown away
    inet_check = True
    geo, simple = False, False
    hostname = None

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()  # ends the script
        elif opt in ("-s", "--simple"):
            simple = True
        elif opt in ("-i", "--no-internet-check"):
            inet_check = False
        elif opt in ("-g", "--geolocate"):
            geo = True
        elif opt in ("-t", "--hostname"):
            hostname = arg

    if hostname is None:
        hostname = input("Target: ")

    if simple is True:
        return print(get_ip(hostname))

    header()

    if inet_check is True:
        internet_check()

    ip = get_ip(hostname)
    print(f'\nIP: {ip}')

    if geo is True:
        try:
            geolocate(ip)
        except KeyError:
            sys.exit("\nDid you enter a local ip address? If not please start a issue # at "
                     "https://github.com/JokemanSec/getIP/issues")


# constructor
if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit('\n\n\033[91muser exit: KeyboardInterrupt')
