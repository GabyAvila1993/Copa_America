from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'copa_america'

mysql = MySQL(app)

@app.route('/')
def index ():
    return "Hola Mundo"

@app.route('/estadisticas')
def estadisticas():
    return "estadisticas"

@app.route('/jugadores')
def jugadores():
    return "jugadores"

@app.route('/login')
def loguin():
    return "login"

@app.route('/selecciones')
def selecciones():
    return "selecciones"



if __name__ == '__main__':
    app.run(port=3000, debug=True)