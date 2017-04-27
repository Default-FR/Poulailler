#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# IMPORTS
#
from alarm      import Alarm
from time       import sleep

##
# FUNCTIONS
#
def demonize():
    pass

##
# MAIN
#
if __name__ == "__main__":
    a = Alarm()
    while True:
        print (a)
        a.alarmchck()
        sleep(59)
