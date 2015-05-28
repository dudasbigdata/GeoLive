# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
from threading import Thread, current_thread
import logging
import os


# logging.basicConfig(level=logging.DEBUG,
#                     format='(%(threadName)-10s) %(message)s',
#                     )

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')

####--------------------------------------------------------------------------------------

@app.route('/inicio/', methods=['POST','GET'])
def inicio():
    return render_template('index.html')
####--------------------------------------------------------------------------------------

@app.route('/buscar/', methods=['POST','GET'])
def buscar():
    global terms

    archiTerms=open('../data/terms.txt','r')
    terms = archiTerms.readlines()
    archiTerms.close()
    mytrack = str(",".join(terms))
    terms = mytrack.split(",")
    print terms

    return render_template('buscar.html', name=terms)

####--------------------------------------------------------------------------------------
@app.route('/verPalabras/', methods=['POST','GET'])
def verPalabras():
    term=request.form['terms']
    terms = [str(t) for t in term.split(",")]

    #print terms #aqui el array de palabras estaria relleno, viendolo en la consola lo comprobamos

    #----------------------------
    #con estras tres lineas hago el fichero lo relleno con el array de palabras y lo cierro
    mytrack = str(",".join(terms))
    archiTerms=open('./data/terms.txt','wa')
    archiTerms.writelines(mytrack)
    #----------------------------
    print "los terminos son"+str(terms)

    return render_template('form_action.html', name=terms)

####--------------------------------------------------------------------------------------
@app.route('/mostrar/', methods=['POST','GET'])
def mostrar():
    print request
    global terms

    if request.method == 'POST':
        term=request.form['terms']
        terms = [str(t) for t in term.split(",")]

        #print terms #aqui el array de palabras estaria relleno, viendolo en la consola lo comprobamos

        #----------------------------
        #con estras tres lineas hago el fichero lo relleno con el array de palabras y lo cierro
        mytrack = str(",".join(terms))
        archiTerms=open('./data/terms.txt','wa')
        archiTerms.writelines(mytrack)
        #----------------------------
        print "los terminos son"+str(terms)


    print terms

    return render_template('mostrar.html', name=terms)

####--------------------------------------------------------------------------------------

@app.route('/mostrarTorque/', methods=['POST','GET'])
def mostrarTorque():
    return render_template('mostrarTorque.html')

####--------------------------------------------------------------------------------------
@app.route('/mostrarCalor/', methods=['POST','GET'])
def mostrarCalor():
    return render_template('mostrarCalor.html')

####--------------------------------------------------------------------------------------
@app.route('/mostrarCluster/', methods=['POST','GET'])
def mostrarCluster():
    return render_template('mostrarCluster.html')

####--------------------------------------------------------------------------------------
if __name__ == '__main__':
    terms=[]
    app.run(debug=True)


#=======================================================================================================================
