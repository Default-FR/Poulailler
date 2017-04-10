# -*- coding: utf-8 -*-


##
# IMPORTS
#

from ephem      import Observer
from ephem      import Sun
from time       import localtime
from time       import sleep

##
# CHICKENHOUSE.MAIN
#

class Alarm:
    def __init__(self):
        self.__observer     = self.__builtObs()
        self.__currentTime  = self.__getCurrentTime()
        self.__morningAlarm = [9,0]
        self.__currentAlarm = [0,0]
        self.__nextAlarm()

    def __str__(self):
        defObject = "Observer : \n"
        defObject += "\tlat = "+str(self.__observer.lat)+"\n"
        defObject += "\tlon = "+str(self.__observer.lon)+"\n\n"

        defObject += "\tMorning alarm = "+str(self.__morningAlarm[0])+ \
                        ":"+str(self.__morningAlarm[1])+"\n"

        defObject += "\tCurrent alarm = "+str(self.__currentAlarm[0])+ \
                        ":"+str(self.__currentAlarm[1])+"\n"

        defObject += "\tCurrent time = "+str(self.__currentTime[2])+ \
                        ":"+str(self.__currentTime[3])+ \
                        ":"+str(localtime()[5])+"\n" 

        return defObject

    def __builtObs(self):
        obs          = Observer()
        obs.pressure = 0
        obs.horizon  = '-6'
        obs.lat      = '48.665'
        obs.lon      = '6.303'
        return obs

    def __getCurrentTime(self):
        currentTime = [0,0,0,0]
        for x in xrange(4):
            currentTime[x] = localtime()[(x+1)]
        return currentTime 

    def __getCurrentDate(self):
        currentDate = str(localtime()[0])+'/'
        if localtime()[2]<10:
            currentDate += '0'
        currentDate += str(localtime()[2])+'/'
        if localtime()[3]<10:
            currentDate += '0'
        currentDate +=str(localtime()[1])+' 12:00'
        return currentDate

    def __nextAlarm(self):
        # Set evening alarm
        obssttg = str(self.__observer.next_setting(
                        Sun(), use_center=True))

        if  self.__currentTime[2] < \
            int(obssttg[
                    len(obssttg)-8:
                    len(obssttg)-6
                ]) and self.__currentTime[2]>=self.__morningAlarm[0]:
        
            self.__observer.date = self.__getCurrentDate()
            sunst = str(self.__observer.next_setting(Sun(), 
                                            use_center=True))
            self.__currentAlarm[0] = sunst[len(sunst)-8:len(sunst)-6]
            self.__currentAlarm[1] = sunst[len(sunst)-5:len(sunst)-3]

        # Set morning alarm
        else:
            self.__currentAlarm[0] = self.__morningAlarm[0]
            self.__currentAlarm[1] = self.__morningAlarm[1]

    def __sendNotif(self):
        pass

    def alarmchck(self):
        self.__currentTime = self.__getCurrentTime()
        if self.__currentTime[2]==self.__currentAlarm[0] \
            and self.__currentTime[3]==self.__currentAlarm[1]:
            self.__nextAlarm()
            self.ring()

    def ring(self):
        sleep(1)
        self.__sendNotif()
        self.__nextAlarm()

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
