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
        print 'dailing ' + ip_idc
        return str(tm) + ' ' + ip_idc + " dailed!"
    except Exception:
        return False


if __name__ == '__main__':
    adsl = Adsl(adsl_config['host'], adsl_config['port'])

    while True:
        lines = adsl.getlines()
        threads = []
        for line in lines:
            if adsl.getstatusbyline(line) == 'dailing':
                ip_idc = adsl.getidcbyline(line)
                t = MyThread(dail, (ip_idc,), name=line)
                threads.append(t)
        if len(threads) == 0:
            time.sleep(10)
        else:
            for i in range(len(threads)):
                threads[i].start()

            for i in range(len(threads)):
                threads[i].join()
                print threads[i].getResult()