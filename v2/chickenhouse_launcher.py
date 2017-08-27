#! /usr/bin/env python

# -*- coding: utf-8 -*-
# author: pBouillon - https://pierrebouillon.tech/

import chickenHouse_controller
from chickenHouse_controller import ChickenHouse_controller
import os
from os      import fork
from os      import setsid
from os      import umask
import sys
from sys     import stderr


def daemonize ():
    """Daemonize the script

    Does the first fork
    Then does the second
    Finally change the output of stderr in a log file
    """
    pid = fork ()
    if pid < 0:
        exit ('An error occured on the first fork')
    elif pid!=0:
        exit ()

    setsid()
    if pid < 0:
        exit ('An error occured on the second fork')
    elif pid!=0:
        exit ()

    stderr = open ('./logs.txt', 'w+')

if __name__ == '__main__':
    daemonize ()
    print ('now running as a background task')
    controller = ChickenHouse_controller ()
    controller.poll ()
