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
    return render_template('/index.html')

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/jugadores')
def jugadores():
    return render_template('jugadores.html')

@app.route('/login')
def loguin():
    return render_template('login.html')

@app.route('/selecciones')
def selecciones():
    return render_template('selecciones')



if __name__ == '__main__':
    app.run(port=3000, debug=True)