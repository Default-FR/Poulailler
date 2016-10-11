import time
import ephem


# -------------- VARIABLES -----------------------

#creation d'un observatoire lenoncourt
lenoncourt = ephem.Observer()
lenoncourt.pressure = 0
lenoncourt.horizon = "-6"
lenoncourt.lat, lenoncourt.lon = '48.665', '6.303'

#pour les cases j[0]m[1]h[2]mn[3] (jour/mois/heure/minute) courantes
jmhmn = []

#pour les cases j[0]m[1]h[2]mn[3] (jour/mois/heure/minute) de l'alarme
a_hmn = []

#ouverture matin
heureMatin = 9
minuteMatin = 00



# -------------- FONCTIONS -----------------------

def alarmeSuivante():
    global a_hmn
    if int(jmhmn[2])<int(str(lenoncourt.next_setting(ephem.Sun(), use_center=True))[len(str(lenoncourt.next_setting(ephem.Sun(), use_center=True)))-8:len(str(lenoncourt.next_setting(ephem.Sun(), use_center=True)))-6]) and int(jmhmn[2])>=heureMatin:
        lenoncourt.date=dateCourante()
        coucher = str(lenoncourt.next_setting(ephem.Sun(), use_center=True))
        heure = coucher[len(coucher)-8:len(coucher)-6]
        minute = coucher[len(coucher)-5:len(coucher)-3]
        a_hmn[:] = [] #on vide la liste
        a_hmn.append(heure) # heures
        a_hmn.append(minute) # minutes
        print "alarme soir set a ",a_hmn[0],":",a_hmn[1]
    else:
    	a_hmn[:] = [] #on vide la liste
        a_hmn.append(heureMatin) # heures
        a_hmn.append(minuteMatin) # minutes
        print "alarme matin set a ",a_hmn[0],":",a_hmn[1]

def dateCourante():
    dateCourante = str(time.localtime()[0])+'/'
    if time.localtime()[2]<10:
        dateCourante += '0'
    dateCourante += str(time.localtime()[2])+'/'
    if time.localtime()[3]<10:
        dateCourante += '0'
    dateCourante +=str(time.localtime()[1])+' 12:00'
    return dateCourante


def sonner(): # Joue le role de l'alarme
    print("\nAlarme On")
    print 'Heure actuelle -> mois:', jmhmn[0], ' | jour:', jmhmn[1], ' | heure:', jmhmn[2], ' | minutes:', jmhmn[3]
    time.sleep(1)
    print("Alarme Off\n")
    alarmeSuivante()

def verifAlarme(): # Renvoie vrai si les heures minutes et jours mois correspondent, faux sinon
    if int(jmhmn[2])==int(a_hmn[0]) and int(jmhmn[3])==int(a_hmn[1]):
        alarmeSuivante()
        return True
    return False

def updateHeure(): # Actualise jmhmn
    global jmhmn
    jmhmn[:] = [] #on vide la liste
    jmhmn.append(time.localtime()[1]) # jours
    jmhmn.append(time.localtime()[2]) # mois
    jmhmn.append(time.localtime()[3]) # heures
    jmhmn.append(time.localtime()[4]) # minutes



# -------------- MAIN -----------------------

#set de base des alarmes
updateHeure()

#On initialie avec les heures du soir
lenoncourt.date=dateCourante()
a_hmn.append(str(lenoncourt.next_setting(ephem.Sun(), use_center=True))[len(str(lenoncourt.next_setting(ephem.Sun(), use_center=True)))-8:len(str(lenoncourt.next_setting(ephem.Sun(), use_center=True)))-6]) # heures
a_hmn.append(str(lenoncourt.next_setting(ephem.Sun(), use_center=True))[len(str(lenoncourt.next_setting(ephem.Sun(), use_center=True)))-5:len(str(lenoncourt.next_setting(ephem.Sun(), use_center=True)))-3]) # minutes

#on verifie si l'alarme est bonne
if int(jmhmn[2])<int(str(lenoncourt.next_setting(ephem.Sun(), use_center=True))[len(str(lenoncourt.next_setting(ephem.Sun(), use_center=True)))-8:len(str(lenoncourt.next_setting(ephem.Sun(), use_center=True)))-6]) and int(jmhmn[2])>=heureMatin:
    a_hmn[:]=[]
    lenoncourt.date=dateCourante()
    coucher = str(lenoncourt.next_setting(ephem.Sun(), use_center=True))
    heure = coucher[len(coucher)-8:len(coucher)-6]
    minute = coucher[len(coucher)-5:len(coucher)-3]
    a_hmn.append(heure) # heures
    a_hmn.append(minute) # minutes

    print "alarme soir set a ",a_hmn[0],":",a_hmn[1]
else: #sinon on met celle du matin
    a_hmn[:]=[]
    a_hmn.append(heureMatin) # heures
    a_hmn.append(minuteMatin) # minutes
    print "alarme matin set a ",a_hmn[0],":",a_hmn[1]


#boucle de l'alarme
while True:
    updateHeure()
    #print '\n\nHeure actuelle: \nmois:', jmhmn[0], ' | jour:', jmhmn[1], ' | heure:', jmhmn[2], ' | minutes:', jmhmn[3]

    if verifAlarme():
        sonner()
    time.sleep(60)


#################################################################
# Auteur: Pierre Bouillon
# Contact/Remarques/Problemes: pierre.bouillon@openmailbox.org
#
# Date de creation: 01/10/2016
#################################################################