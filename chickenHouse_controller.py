# -*- coding: utf-8 -*-
# author: pBouillon - https://pierrebouillon.tech/

import datetime
from datetime   import datetime as dt
import ephem
from ephem      import Observer
from ephem      import Sun
import ressources
from ressources import ALARM_MORNING_H
from ressources import ALARM_MORNING_M
from ressources import ALARM_TIME
from ressources import HORIZON
from ressources import LATENCY
from ressources import LATITUDE
from ressources import LONGITUDE
from ressources import PIN_SIG
from ressources import TO_GMT
import RPi.GPIO
from RPi.GPIO   import BCM
from RPi.GPIO   import HIGH
from RPi.GPIO   import LOW
from RPi.GPIO   import OUT
from RPi.GPIO   import cleanup
from RPi.GPIO   import output
from RPi.GPIO   import setmode
from RPi.GPIO   import setup
import sys
from sys        import exit
from sys        import version_info as version
import time
from time       import localtime
from time       import sleep


class ChickenHouse_controller :
    '''Reference Alarm

    Set its own clock each LATECY seconds
    Get the next alarm after each ring:
        H_MORNING h M_MORNING for the Morning
        Next sunset for the Evening

    Attributes:
        _observer      : physical location of the clock
        _morning_alarm : hours and minutes of the morning alarm
        _current_alarm : next time at which the clock will ring
    '''
    def __init__ (self) :
        self._alarm_hour   = 0
        self._alarm_minute = 0
        self._observer = self.__build_obs ()
        self.__init_rasp_config ()
        self.__setup_next_alarm ()

    def __build_obs (self) :
        '''Set up the Observer

        Returns:
            The observer built
        '''
        local_observer = Observer ()
        local_observer.pressure = 0
        local_observer.horizon  = HORIZON
        local_observer.lat = LATITUDE
        local_observer.lon = LONGITUDE
        return local_observer

    def __init_rasp_config (self) :
        setmode (BCM)
        setup   (PIN_SIG, OUT)
        output  (PIN_SIG, LOW)

    def __get_current_date (self):
        '''catch and build the current date

        Returns:
            The current date as YYYY/M(M)/DD HH:MM
        '''
        current_date =  str (localtime()[0]) + '/'
        current_date += str (localtime()[2]) + '/'
        current_date += str (localtime()[1]) + ' 12:00'
        return current_date

    def __ring (self):
        output (PIN_SIG, HIGH)
        sleep  (ALARM_TIME)
        output (PIN_SIG, LOW)

    def __setup_next_alarm (self):
        '''Switch to the next alarm
        '''
        if dt.now().hour > ALARM_MORNING_H :
            self._observer.date = self.__get_current_date ()
            # sunset = YYYY:MM/DD HH:MM:SS
            sunset = self._observer.next_setting (Sun (), use_center = True)
            sunset = str(sunset).split(' ')[1]
            self._alarm_hour   = sunset.split(':')[0]
            self._alarm_minute = sunset.split(':')[1]
        else:
            self._alarm_hour   = ALARM_MORNING_H
            self._alarm_minute = ALARM_MORNING_M

    def __update (self):
        '''Check if the alarm should ring
        '''
        if int(self._alarm_hour) == dt.now().hour \
            and int(self._alarm_minute) == dt.now().minute :
            self.__ring ()
            self.__setup_next_alarm ()

    def poll (self) :
        '''Initiate polling
        '''
        while True:
            try:
                self.__update()
                # in tests needed
                # print('now: '+str(dt.now())+' --- alarm: '+str(self._alarm_hour)+':'+str(self._alarm_minute))
                sleep (LATENCY)
            except (KeyboardInterrupt, SystemExit):
                cleanup ()
                exit ('Program was manually ended')
            except:
                cleanup ()
                exit ('Unexpected error:\n'+sys.exc_info()[0])
