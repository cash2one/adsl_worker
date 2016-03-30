# -*- coding: utf-8 -*-

import urllib, urllib2
from tools import Adsl
import time, os, logging
from threading import Thread


adsl_config = {
    'host': '127.0.0.1',
    'port': 6379,
}

LOG_PATH = '/ROOT/logs/worker'
FILE_NAME = 'worker-' + time.strftime('%Y-%m-%d', time.localtime()) + '.log'
LOG_FILE = LOG_PATH + '/' + FILE_NAME

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s',
                    filemode='a',
                    filename=LOG_FILE)
logger = logging.getLogger(__name__)


def dail(ip_idc):
    try:
        url = 'http://' + ip_idc + ':8000'
        data = urllib.urlencode({'dail': True})
        ret = urllib2.urlopen(url, data).read()
        logger.info(ret)
    except Exception, error:
        logger.error("dail %s error: %s" % (url, str(error)))


def main():
    adsl = Adsl(adsl_config['host'], adsl_config['port'])

    while True:
        lines = adsl.getlines()
        threads = []

        for line in lines:
            if adsl.getstatusbyline(line) == 'dailing':
                ip_idc = adsl.getidcbyline(line)
                t = Thread(target=dail, args=(ip_idc,), name=line)
                t.start()
                threads.append(t)
                logger.info('start dail ' + line)

        if len(threads) == 0:
            time.sleep(1)
        else:
            for t in threads:
                t.join()
                logger.info('end dail: ' + t.getName())


if __name__ == '__main__':
    main()