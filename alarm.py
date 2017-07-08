# -*- coding: utf-8 -*-
# author: pBouillon - https://github.com/pBouillon

import ephem
from ephem      import Observer
from ephem      import Sun
import time
from time       import localtime
from time       import sleep

'''Constant: integer equals to 59 seconds'''
LATENCY = 59
'''Constant: morning hours to open the doors'''
H_MORNING = 9
'''Constant: morning minutes to open the doors'''
M_MORNING = 00

class Alarm:
    '''Reference Alarm

    Set its own clock each LATECY seconds
    Get the next alarm after each ring:
        H_MORNING h M_MORNING for the Morning
        Next sunset for the Evening

    Attributes:
        _observer     : physical location of the clock
        _current_time  : current time of the clock
        _morning_alarm : hours and minutes of the morning alarm
        _current_alarm : next time at which the clock will ring
    '''
    def __init__ (self):
        self._observer      = self.__build_obs ()
        self._current_time  = self._get_current_time ()
        self._morning_alarm = [H_MORNING,M_MORNING]
        self._current_alarm = [0,0]
        self._next_alarm ()
        self.run ()

    def __str__ (self):
        object_str = "Observer : \n"
        object_str += "\tlat = " + str (self._observer.lat) + "\n"
        object_str += "\tlon = " + str (self._observer.lon) + "\n\n"

        object_str += "\tMorning alarm = " + str (self._morning_alarm[0])+ \
                        ":" + str (self._morning_alarm[1]) + "\n"

        object_str += "\tCurrent alarm = " + str (self._current_alarm[0])+ \
                        ":" + str (self._current_alarm[1]) + "\n"

        object_str += "\tCurrent time  = " + str (self._current_time[2])+ \
                        ":" + str (self._current_time[3])+ \
                        ":" + str (localtime()[5]) + "\n"
        return object_str

    def __build_obs (self):
        '''Set up the Observer

        Returns:
            The built in observer
        '''
        obs          = Observer()
        obs.pressure = 0
        obs.horizon  = '-6'
        obs.lat      = '48.665'
        obs.lon      = '6.303'
        return obs

    def _get_current_time (self):
        #TODO(Pierre Bouillon): Improve time recuperation)
        '''Build the current time in a list

        Returns:
            The current time as a list of 4 slots
        '''
        current_time = [0,0,0,0]
        for x in xrange(4):
            current_time[x] = localtime()[(x+1)]
        return current_time

    def __get_current_date (self):
        '''catch and build the current date

        Returns:
            The build current date as a string
        '''
        current_date = str(localtime()[0])+'/'
        if localtime()[2]<10:
            current_date += '0'
        current_date += str(localtime()[2])+'/'
        if localtime()[3]<10:
            current_date += '0'
        current_date +=str(localtime()[1])+' 12:00'
        return current_date

    def _next_alarm (self):
        '''Set up the next alarm regarding the observer and local time

        Set up the next alarm to be raised
        '''
        # Set evening alarm
        obssttg = str(self._observer.next_setting(
                        Sun(), use_center=True))

        if  self._current_time[2] < \
            int(obssttg[
                    len(obssttg)-8:
                    len(obssttg)-6
                ]) and self._current_time[2]>=self._morning_alarm[0]:

            self._observer.date = self.__get_current_date()
            sunst = str(self._observer.next_setting(Sun(),
                                            use_center=True))
            self._current_alarm[0] = sunst[len(sunst)-8:len(sunst)-6]
            self._current_alarm[1] = sunst[len(sunst)-5:len(sunst)-3]

        # Set morning alarm
        else:
            self._current_alarm[0] = self._morning_alarm[0]
            self._current_alarm[1] = self._morning_alarm[1]

    def check_alarm (self):
        '''Verify if the times are matching

        If times are matching, perform the ring()
        Else pass
        '''
        self._current_time = self._get_current_time  ()
        if self._current_time[2]==self._current_alarm[0] \
            and self._current_time[3]==self._current_alarm[1]:
            self._next_alarm()
            self.ring()

    def ring (self):
        '''Actions to perform whenever the program's clock match the alarm

        Do all actions
        Then set up its next alarm
        '''
        sleep(1)
        self._next_alarm()

    def run (self):
        '''ChickenHouse infinity loop

        Run the loop forever and check each alarm
        Wait each iteration LATENCY seconds
        '''
        while True:
            self.check_alarm()
            sleep(LATENCY)
