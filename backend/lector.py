#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importar los modulos necesarios
import json
import sys
import mysql.connector
import time
import os
from cartodb import CartoDBAPIKey, CartoDBException
from geopy.geocoders import Nominatim

# Definimos tweets
tweets = []

contador = 0
contador_tweets = 0

# Definimos la fecha actual
fecha = time.strftime('%Y%m%d_%H%M%S')

# Informacion de CartoDB
API_KEY = '21ac19bc3a18a9b2ea76b2ed1a43244a463ee15e'
cartodb_domain = 'bigdatatfg'
cl = CartoDBAPIKey(API_KEY, cartodb_domain)

# Inicio de las diferentes sentencias para las tablas de CartoDB
sentencia = "INSERT INTO tweets (id_tweet, nombre_usuario, fecha, creado, texto, latitud, longitud, localizacion, " \
            "codigo_pais, idioma, origen) VALUES "

cadenavalores = ""
valores = ""

config_mysql = {
    'user': 'upsa',
    'password': '12345',
    'host': 'localhost',
    'database': 'pruebaTwitter',
}

# Funcion para escapar de algunos caracteres a la hora de insertar en base de datos
def unescapeMySQL(s):
    s = s.replace("'", "&apos;")
    s = s.replace(", '", "&coma;")
    s = s.replace(",", "&coma;")
    s = s.replace("\\", "&barra;")
    return s


# Conectamos al servidor MySql
conector = mysql.connector.connect(**config_mysql)
cursor = conector.cursor()

# Guardamos lo que hay en datos.json en otro fichero que se va a llamar datos_fechaActual.json
datos = open('datos.json')
datos_fecha = open('datos' + fecha + '.json', "w")

for line in open('datos.json'):
    try:
        tweets.append(json.loads(line))
        datos_fecha.write(line)
    except:
        pass

tweet = tweets[0]

num = 0

for tweet in tweets:
    latitud = ""
    longitud = ""
    codigo_pais = ""
    localizacion = ""
    num = num + 1

    def getLatLon(codigo_pais, latitud, longitud, localizacion):
        result = ""
        # From twitter
        if latitud != "" and longitud !="":
            # OK
            result = [latitud, longitud, "T"]
        else:
            # Nominatim request
            geolocator = Nominatim()
            if(localizacion != ""):
                # Nominatim
                latlong_loc = geolocator.geocode(localizacion, timeout=5)
                if latlong_loc != None:
                    result = [latlong_loc.latitude, latlong_loc.longitude ,"L"]
                else:
                    # Nominatim
                    latlong_cod = geolocator.geocode(codigo_pais, timeout=5)
                    result = [latlong_cod.latitude, latlong_cod.longitude ,"LM"]
            elif(codigo_pais != ""):
                # Nominatim
                latlong_cod = geolocator.geocode(codigo_pais, timeout=5)
                result = [latlong_cod.latitude, latlong_cod.longitude ,"C"]

        return result

    # Comprobacion id
    if 'id' not in tweet:
        id_tweet = ""
    else:
        id_tweet = tweet['id']

    # Comprobacion usuario
    if 'user' not in tweet:
            usuario = ""
    else:
        if 'screen_name' not in tweet['user']:
            usuario = ""
        else:
            usuario = tweet['user']['screen_name']
            usuario = "@" + str(usuario)

    # Comprobacion creado
    if 'created_at' not in tweet:
        creado = ""
    else:
        creado = tweet['created_at']

    # Comprobacion texto
    if 'text' not in tweet:
        texto = ""
    else:
        texto = tweet['text']
        texto = unescapeMySQL(texto)

    # Comprobacion idioma
    if 'lang' not in tweet:
        idioma = ""
    else:
        idioma = tweet['lang']

    # Comprobacion codigo pais
    if 'place' not in tweet:
        codigo_pais = ""
    elif tweet['place'] == None:
        codigo_pais = ""
    else:
        if 'country_code' not in tweet['place']:
            codigo_pais = ""
        else:
            codigo_pais = tweet['place']['country_code']

        # Comprobacion de la geolocalizacion
        if 'geo' not in tweet:
            latitud = ""
            longitud = ""
        elif tweet['geo'] is None:
            latitud = ""
            longitud = ""
        else:
            if 'coordinates' not in tweet['geo']:
                latitud = ""
                longitud = ""
            else:
                latitud = tweet['geo']['coordinates'][0]
                longitud = tweet['geo']['coordinates'][1]

        # Comprobacion de la localizacion
        if 'user' not in tweet:
                localizacion = ""
        else:
            if 'location' not in tweet['user']:
                localizacion = ""
            else:
                localizacion = tweet['user']['location']

    localizacion_final = getLatLon(codigo_pais, latitud, longitud, localizacion)

    if localizacion_final != "":
        latitud = localizacion_final[0]
        longitud = localizacion_final[1]
        origen = localizacion_final[2]

        localizacion = unescapeMySQL(localizacion)
        parametros = ("'" + str(id_tweet) + "', '" + str(usuario) + "', '" + creado + "', '" + str(creado) + "', '" + texto + "', " + str(latitud) + ", " + str(longitud) + ", '" + localizacion + "', '" + str(codigo_pais) + "', '" + str(idioma) + "', '" + str(origen) +"'").encode('utf-8')
        valores = valores + "(" + parametros + "),"
        contador = contador + 1

    # Query para insertar en MySQL
    localizacion = unescapeMySQL(localizacion)
    query = """INSERT INTO tweets (id_tweet, nombre_usuario, creado, texto, latitud, longitud, localizacion ,codigo_pais, idioma)
    VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (id_tweet, usuario, creado, texto,
    latitud, longitud, localizacion, codigo_pais, idioma)
    cursor.execute(query)
    contador_tweets = contador_tweets + 1



conector.commit()

# Vaciamos el contenido del fichero datos.json,
# ya que los hemos metido anteriormente en el fichero datos_fechaActual.json
archivo = open("datos.json","rw+")
lineas = archivo.readlines()

for linea in lineas:
    pass

archivo.truncate(0)
archivo.close()

try:

    # Insertar en tabla CartoDB
    if contador > 0:
        valores = valores[0:-1]
        sentencia = sentencia + valores
        # print sentencia
        cl.sql(sentencia)
        sentencia_the_geom = "UPDATE tweets SET the_geom = cdb_latlng (latitud, longitud)"
        # print sentencia_the_geom
        cl.sql(sentencia_the_geom)

    print "Tweets con coordenadas: " + str(contador)
    print "Tweets totales: " + str(contador_tweets)

except CartoDBException as e:
    print ("some error ocurred", e)