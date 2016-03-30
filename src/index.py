# -*- coding: utf-8 -*-

import urllib
from tools import Adsl
import time, os, logging
from mythread import MyThread

adsl_config = {
    'host': '127.0.0.1',
    'port': 6379,
}

LOG_PATH = '/ROOT/logs/worker'
FILE_NAME = 'worker-' + time.strftime('%Y-%m-%d', time.localtime()) + '.log'
LOG_FILE = LOG_PATH + '/' + FILE_NAME

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)


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


def main():
    adsl = Adsl(adsl_config['host'], adsl_config['port'])

    while True:
        lines = adsl.getlines()
        threads = []
        for line in lines:
            if adsl.getstatusbyline(line) == 'dailing':
                # print line
                ip_idc = adsl.getidcbyline(line)
                t = MyThread(dail, (ip_idc,), name=line)
                threads.append(t)

        if len(threads) == 0:
            time.sleep(1)
        else:
            for i in range(len(threads)):
                threads[i].start()

            print 'started!'
            for i in range(len(threads)):
                print 'before join'
                threads[i].join()
                print 'end join'
                print threads[i].getResult()
            print 'end!'


if __name__ == '__main__':
    main()