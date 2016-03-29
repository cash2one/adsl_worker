# -*- coding: utf-8 -*-

import threading


class MyThread(threading.Thread):
    def __init__(self, func, args, name=None):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        self.res = apply(self.func, self.args)