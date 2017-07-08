# -*- coding: utf-8 -*-
# author: pBouillon - https://github.com/pBouillon

import alarm
from alarm   import Alarm
import os
from os      import fork
from os      import setsid
from os      import umask

#TODO(Pierre Bouillon): conceive CLI

def daemonize():
    """Daemonize the script

    Does the first fork
    Then does the second
    Finally change the output of stderr in a log file
    """
    pid = fork()
    if pid < 0:
        exit ('An error occured on the first fork')
    elif pid!=0:
        exit()

    setsid()
    if pid < 0:
        exit ('An error occured on the second fork')
    elif pid!=0:
        exit()

    sys.stderr = open('./logs.txt', 'w+')


'''Runs the program

Main code executed on launch
'''
if __name__ == '__main__':
    # Uncomment to daemonize the script
    # daemonize()
    alarm = Alarm()
