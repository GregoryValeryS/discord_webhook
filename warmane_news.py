# !/usr/bin/python3
# -*- coding: utf-8 -*-

import threading
from main import main


def looper():
    print('► Начат новый цикл')
    main('last_news.xlsx', 'warmane_news_hook.txt')

    myThread = threading.Timer(3600, looper)
    myThread.start()


if __name__ == '__main__':
    looper()
