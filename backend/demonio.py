from flask import Flask, render_template, request, url_for
from threading import Thread, current_thread
import logging
import os
import time
import signal


#archiPid=open('../data/pid.txt','r')
#cadenaPidString = archiPid.readlines()
#print cadenaPidString
#print cadenaPidString[0]
#PidAdaptadoString = cadenaPidString[0]
#archiPid.close()
#print "el pid del streaming es: " + PidAdaptadoString

import subprocess


print "\n Arranque Streaming"
file = 'streaming.py'
os.system('python ' + file + ' &')
#subprocess.Popen("python " + file, shell=True)

time.sleep(5)

archiTerms=open('../data/terms.txt','r')
cadenaTerms = archiTerms.readlines()
archiTerms.close()
print "los terminos iniciales son: " + str(cadenaTerms)


archiPid=open('../data/pid.txt','r')
cadenaPidString = archiPid.readline()
PidAdaptadoString = cadenaPidString
archiPid.close()
print "Init PID: " + PidAdaptadoString

while True:
       # print "\n he entrado en el while"
        #print "=========================="
        time.sleep(5)

        archiTerms=open('../data/terms.txt','r')
        cadenaTermsNueva = archiTerms.readlines()
        #print "los terminos ahora son: " + str(cadenaTermsNueva)
        archiTerms.close()

        if(cadenaTerms != cadenaTermsNueva):
            #print "\n si entro aqui nos han cambiado los terminos, por lo tanto tengo que MATARTE..." + PidAdaptadoString
            print "kill " + PidAdaptadoString
            os.kill(int(PidAdaptadoString), signal.SIGKILL)

            #print "actualizo los terminos viejos por los nuevos"
            cadenaTerms = cadenaTermsNueva

            #leo el fichero pid


            #print "\n ya te he matado, ahora te volvere a arrancar"
            #python streaming.py
            file = 'streaming.py'
            os.system('python ' + file + ' &')
            #subprocess.Popen("python " + file, shell=True)
            time.sleep(5)
            archiPid=open('../data/pid.txt','r')
            cadenaPidString = archiPid.readline()
            PidAdaptadoString = cadenaPidString
            archiPid.close()
            print "NUEVO PID: " + PidAdaptadoString
