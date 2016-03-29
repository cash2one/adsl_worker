# -*- coding: utf-8 -*-

import urllib
from tools import Adsl
import time
from mythread import MyThread

adsl_config = {
    'host': '127.0.0.1',
    'port': 6379,
}

def dail(ip_idc):
    try:
        url = 'http://' + ip_idc + ':8000'
        data = urllib.urlencode({'dail': True})
        ret = urllib.urlopen(url, data).read()
        tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        return str(tm) + ' ' + ip_idc + " dailed!"
    except Exception:
        return False


if __name__ == '__main__':
    adsl = Adsl(adsl_config['host'], adsl_config['port'])

    while True:
        lines = Adsl.getlines()
        threads = []
        for line in lines:
            if adsl.getstatusbyline(line) == 'used':
                ip_idc = adsl.getidcbyline(line)
                t = MyThread(dail, (line,), name=line)
                threads.append(t)

        for i in range(len(threads)):
            threads[i].start()

        for i in range(len(threads)):
            threads[i].join()
            print threads[i].getResult()

