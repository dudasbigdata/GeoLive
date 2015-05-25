#! /usr/bin/env python
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time
import os


# Keys de la API de Twitter
consumer_key = "zSUVYhsjhh7fcqF7VdDsH25GE";
consumer_secret = "Trg8dRkTpNH25u3yteWRhiLzarGaeeb3pDNKsQDy6YWkHQmy2B";
access_token = "2809827652-6pzODCcXwm26dgEyXrzcxa4pgdkUFSdFdWsNOOF";
access_token_secret = "LZdX6A9fUiKSn5Zqv8ELW8uBp8rlUTcqn1BvKkAZ8RkDN";
#----------------------------------------------------------------------
#consumer_key =	"xttxVhZm6dz0DvCbjhfHGWwm3";
#consumer_secret =	"4IJNZvm8VArBSGdmJblwGFL4CNw2BQdUcPmMK2Y2MYgd4qYiKo";
#access_token	= "2893123793-EWz1wTZnaAWWA59H7015EhnJkjoK7p8bvXJ1LsD";
#access_token_secret	= "QeKkINX6tfUtUTCTBOPWsUzqJnxUT5ZluFhKEW0MmgFTh";

pidstreaming = os.getpid()#proces id
print "el pid del streaming es: "+ str(pidstreaming)

#me guardo el pid en un txt
archiPid=open('../data/pid.txt','wa')
archiPid.write(str(pidstreaming))
archiPid.close()

# Abrimos el fichero donde vamos a escribir
fichero = open('datos.json', 'wa')

# Escribimos en el fichero abierto los tweets que vamos encontrando
class listener(StreamListener):

    def on_data(self, data):
        #print (data)
        fichero.write(str(data))
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
twitterStream = Stream(auth, listener())

print "\n ...ESCUCHANDO..."


#me abro el archiTerms.txt
archiTerms=open('../data/terms.txt','r')
cadenaBusqueda = archiTerms.readlines()
archiTerms.close()

values = ','.join([' ' + x + ' ' for x in cadenaBusqueda[0].split(",")])
print "compruebo que la cadena esta en el formato perfecto: " + str(values) #aqui ya tengo las palabras que quiero poner a escuchar y en el formato deseado

# Aplicamos el filtro de palabras que queremos escuchar
twitterStream.filter(track=[values], languages=["es", "en"])
#aqui leer el terms.txt y ponerlo en lugar de messi


