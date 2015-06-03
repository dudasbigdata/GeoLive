from flask import Flask, render_template, request, url_for
from threading import Thread, current_thread
import logging
import os


app = Flask(__name__)

@app.route('/')
def form():
    return render_template('index.html')


@app.route('/inicio/', methods=['POST','GET'])
def inicio():
    return render_template('index.html')


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


@app.route('/verPalabras/', methods=['POST','GET'])
def verPalabras():
    term=request.form['terms']
    terms = [str(t) for t in term.split(",")]


    mytrack = str(",".join(terms))
    archiTerms=open('./data/terms.txt','wa')
    archiTerms.writelines(mytrack)
    
    print "los terminos son"+str(terms)

    return render_template('form_action.html', name=terms)


@app.route('/mostrar/', methods=['POST','GET'])
def mostrar():
    print request
    global terms

    if request.method == 'POST':
        term=request.form['terms']
        terms = [str(t) for t in term.split(",")]

        mytrack = str(",".join(terms))
        archiTerms=open('./data/terms.txt','wa')
        archiTerms.writelines(mytrack)

        print "los terminos son"+str(terms)


    print terms

    return render_template('mostrar.html', name=terms)



@app.route('/mostrarTorque/', methods=['POST','GET'])
def mostrarTorque():
    return render_template('mostrarTorque.html')


@app.route('/mostrarCalor/', methods=['POST','GET'])
def mostrarCalor():
    return render_template('mostrarCalor.html')


@app.route('/mostrarCluster/', methods=['POST','GET'])
def mostrarCluster():
    return render_template('mostrarCluster.html')


if __name__ == '__main__':
    terms=[]
    app.run(debug=True)
