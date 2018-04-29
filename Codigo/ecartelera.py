# -*- coding: utf-8 -*-

########################################################
#################### TELEGRAM BOT ######################
################ CINEBOT - @CICINEBOT ##################
## UCM - MASTER INGENIERIA INFORMATICA - TMI - GRUPO 3 #
########################################################

##################### AUTORES ##########################
############## Andres Aguirre Juarez ###################
############### Pablo Blanco Peris #####################
############# Maria Castaneda Lopez ####################
############### Maurizio Vittorini #####################
########################################################

import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import urllib
from bs4 import BeautifulSoup
import urllib.request
import requests
import MySQLdb

##CONEXION CON LA BD

def conecction():
    conn = MySQLdb.connect(host= "localhost",
                           user="root",
                           passwd="",
                           db="cinebot")
                           
    return conn

def cargarCinesEnBBDD(nombreCine, enlaceCine):
    i = 0
    conn = conecction()
    x = conn.cursor()

    for cine in nombreCine:

        query = "INSERT IGNORE INTO Cine (nombre, enlace, id ) VALUES ('{0}', '{1}', '{2}');" .format(cine, enlaceCine[i], i)
        
        try:
            #print(query)
            x.execute(query)
        except MySQLdb.ProgrammingError:
            print("La siguiente query ha fallado:%s" % query + '\n')
        print("El cine " + str(cine) + " ha sido añadido con el enlace " + enlaceCine[i])
        i = i + 1
    
    conn.commit()
    x.close()
    conn.close()

def cargarPasesEnBBDD(enlaceCine, pelicula, hora):
    i = 0
    conn = conecction()
    x = conn.cursor()
    
    query = "INSERT IGNORE INTO Pases (nombreCine, idPelicula, hora) VALUES ('{0}', '{1}', '{2}');" .format(enlaceCine, pelicula, hora)
        
    try:
        #print(query)
        x.execute(query)
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado:%s" % query + '\n')
    print("El cine " + str(enlaceCine) + " ha añadido la peli " + str(pelicula) + " a la hora: " + hora)

    conn.commit()
    x.close()
    conn.close()

def leerCinesFichero(nombreFichero):
    nombreCine = list()
    enlaceCine = list()
    f = open(nombreFichero)
    linea = f.readline()
    while linea != "":
        l = linea.split("_")
        #print ("ENLACE: " + l[0] + " NOMBRE : " + l[1])
        nombreCine.append(l[1][:-1])
        enlaceCine.append(l[0])
        linea = f.readline()
    f.close()
    return (nombreCine, enlaceCine)

def buscarPeliEnBD(peli):
    conn = conecction()
    x = conn.cursor()
    #escaped = re.escape(peli)
    peli = peli.replace("'", "")

    query = "SELECT nombre FROM Pelicula WHERE nombre = '{0}';".format(peli)
    print (query)
    try:
        x.execute(query)
        
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')
    

    if x.rowcount == 0:
        conn.commit()
        x.close()
        conn.close()
        return False

    for line in x:
        print (peli + " " + line[0])
        if peli == line[0]:
            conn.commit()
            x.close()
            conn.close()
            return True
        conn.commit()
        x.close()
        conn.close()
        return False


def cargarPeliculasEnBBDD(pelicula):
    conn = conecction()
    x = conn.cursor()
    
    for p in pelicula:
        p = p.replace("'", "")
        print (p)
        if (buscarPeliEnBD(p)==False):
            #p = str(MySQLdb.escape_string(p))
            query = "INSERT IGNORE INTO Pelicula (nombre) VALUES ('{0}');" .format(p)
            
            try:
                print(query)
                x.execute(query)
            except MySQLdb.ProgrammingError:
                print("La siguiente query ha fallado:%s" % query + '\n')
            print("La pelicula " + str(p) + " ha sido añadida.")

    #print (pelicula)

    conn.commit()
    x.close()
    conn.close()

def getClaveCine(nombreCine):
    conn = conecction()
    x = conn.cursor()
    resultados =[]
    
    query = "SELECT enlace FROM Cine WHERE nombre = '{0}';" .format(nombreCine);
    
    try:
        x.execute(query)
    
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')
    
    k = 0
    for i in x:
        resultados.append( i[0])
    
    conn.commit()
    x.close()
    conn.close()

    return resultados[0]

def getClaveCineID(id):
    conn = conecction()
    x = conn.cursor()
    resultados =[]
    
    query = "SELECT enlace FROM Cine WHERE id = '{0}';" .format(id);
    
    try:
        x.execute(query)
    
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')
    
    k = 0
    for i in x:
        resultados.append( i[0])

    conn.commit()
    x.close()
    conn.close()

    return resultados[0]

def getCines():
    conn = conecction()
    x = conn.cursor()
    resultados =[]
    
    query = "SELECT nombre FROM Cine ORDER BY nombre;"
    
    try:
        x.execute(query)
    
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')
    
    k = 0
    
    for i in x:
        resultados.append( i[0])
        k = k+1

    conn.commit()
    x.close()
    conn.close()

    return resultados

# Devuelve el id del cine
def getIdCine(nombre):
    conn = conecction()
    x = conn.cursor()
    resultados =[]
    
    query = "SELECT id FROM Cine WHERE nombre = '{0}';" .format(nombre);
    
    try:
        x.execute(query)
    
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')
    
    k = 0
    for i in x:
        resultados.append( i[0])

    conn.commit()
    x.close()
    conn.close()

    return resultados[0]

# Devuelve las películas que hay en un cine concreto.
def getPeliculasEnCine(nombreCine):
    conn = conecction()
    x = conn.cursor()
    resultados = getClaveCine(nombreCine)
    
    #query = "SELECT nombrePelicula, hora FROM Pases WHERE nombreCine = '{0}' ORDER BY hora;" .format(resultados[0]);
    query = "SELECT DISTINCT Pelicula.nombre FROM Pelicula, Pases WHERE Pases.idPelicula = Pelicula.id AND Pases.nombreCine = '{0}';" .format(resultados);
    print(query)
    try:
        x.execute(query)

    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')

    resultados = []
    for i in x:
        #resultados.append(str(i[0] + ' ' + i[1]))
        resultados.append(i[0])
        #print ( i[0] + ' ' + i[1] )
        #print ( i[0] )

    conn.commit()
    x.close()
    conn.close()

    return resultados

#Devuelve los pases de una película en el último cine seleccionado
def getPasesDePelicula(pelicula, cine):
    conn = conecction()
    x = conn.cursor()
    resultados =[]
    
    query = "SELECT hora FROM Pases WHERE nombreCine = '{0}' and idPelicula = '{1}';" .format(cine, pelicula);
    print(query)
    try:
        x.execute(query)
    
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')

    k = 0
    for i in x:
        resultados.append(i[0])

    conn.commit()
    x.close()
    conn.close()

    return resultados

def getNombreCineById(id):
    conn = conecction()
    x = conn.cursor()
    resultados =[]
    
    query = "SELECT nombre FROM Cine WHERE id = '{0}';" .format(id);
    print(query)
    try:
        x.execute(query)
    
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')
    
    k = 0
    for i in x:
        resultados.append(i[0])
    
    conn.commit()
    x.close()
    conn.close()

    return resultados[0]

def getNombrePeliculaById(id):
    conn = conecction()
    x = conn.cursor()
    resultados =[]
    
    query = "SELECT nombre FROM Pelicula WHERE id = '{0}';" .format(id);
    print(query)
    try:
        x.execute(query)
    
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')
    
    k = 0
    for i in x:
        resultados.append(i[0])

    conn.commit()
    x.close()
    conn.close()

    return resultados[0]

def getIdPelicula(pelicula):
    conn = conecction()
    x = conn.cursor()
    resultados =[]
    pelicula = pelicula.replace("'","")
    
    query = "SELECT id FROM Pelicula WHERE nombre = '{0}';" .format(pelicula);
    print(query)
    try:
        x.execute(query)
    
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')
    
    k = 0
    for i in x:
        resultados.append(i[0])

    conn.commit()
    x.close()
    conn.close()
    print (resultados)
    return resultados[0]

def buscarPeliculaEnCine(url):
    pelicula = list()
    peliculaPase =dict()
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    peliculas = soup.find_all('div', class_="lfilmb")
    soup = BeautifulSoup(str(peliculas), 'lxml')
    horarioPeliculas = soup.find_all('div', class_="cartelerascont")
    nombrePeliculas = soup.find_all('h4')
    cont = 0
    for i in nombrePeliculas:
        line = re.split("<|>",str(i))
        pelicula.append(line[6])
    #Esto solo debe hacerse una vez, sino fallará
    cargarPeliculasEnBBDD(pelicula)
    for i in horarioPeliculas:
        soup = BeautifulSoup(str(i), 'lxml')
        horas = soup.find_all('p', class_="stn")
        listaHorasPelicula = list()
        for h in horas:
            line = re.split("<|>",str(h))
            listaHorasPelicula.append(line[2])
        peliculaPase[pelicula[cont]] = listaHorasPelicula
        cont = cont + 1
    for i in peliculaPase:
        for time in peliculaPase[i]:
            #print (str(i) + time)
            cargarPasesEnBBDD(url, getIdPelicula(i), time)
    return peliculaPase

#getCines()

#En fichero.txt están los enlaces a cada cine y el nombre de cada cines en una misma linea, separado por _
#(nombreCine, enlaceCine) = leerCinesFichero("cinesMadrid.txt")

#Es necesario cargar los cines una vez en la BBDD
#cargarCinesEnBBDD(nombreCine, enlaceCine)

#url = 'https://www.ecartelera.com/cines/dreams-cinema-palacio-hielo/'
#for url in enlaceCine:
#    buscarPeliculaEnCine(url)




