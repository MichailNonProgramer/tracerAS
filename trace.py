import sys
from sys import argv
import os
from re import findall
from subprocess import check_output
from json import loads
from urllib import request

LENIP, LENCOUNTRY, LENCITY = 20, 5 , 20
LENAS = 10
LENDIF = 60

def AS_trace():
    DN = argv[1]
    try:
        tracert_result = check_output('tracert -4 -d -h 40 ' + DN, shell=True).decode('cp866')
    except:
        print("Incorrect domain name")
        sys.exit(1)
    list_of_ip_adresses = findall('\d+.\d+.\d+.\d+' , tracert_result)
    list_of_ip_adresses.pop(0)
    i = 1
    print("-" * LENDIF)
    for ip in list_of_ip_adresses:
        info = get_information_about_ip(ip)
        if 'bogon' in info:
            print(str(i) + '\t' + correct_output(info['ip'], LENIP) + '\t' + correct_output("It's bogon (My AS)", LENAS))
        else:
            try:
                print(str(i) + '\t' + correct_output(str(info['ip']), LENIP) + '\t'
                      + correct_output(str(info['country']).split(" ")[0], LENCOUNTRY)
                      + '\t\t' + correct_output(info['city'], LENCITY)
                      +
                      '\t' + correct_output(str(info['org']).split()[0], LENAS) +
                      '\t' + ' '.join((info['org'].split()[1::])))
            except:
                continue
        i += 1
    print("-" * LENDIF)

def correct_output(str, len_output):
    res = str
    for i in range(len_output - len(str)):
        res += " "
    return res

def get_information_about_ip(IP):
    return loads(request.urlopen('https://ipinfo.io/' + IP + '/json').read())


if __name__ == '__main__':
    AS_trace()
