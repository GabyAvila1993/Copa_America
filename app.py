from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'copa_america'

mysql = MySQL(app)

# Ruta principal para renderizar la página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar todos los jugadores con detalles generales
@app.route('/jugadores')
def jugadores():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nombre, apellido, nacionalidad, peso, altura FROM jugadores")
    jugadores = cursor.fetchall()
    cursor.close()

    return render_template('jugadores.html', jugadores=jugadores)

# Ruta para obtener jugadores de una selección específica
@app.route('/jugadores/seleccion', methods=['GET'])
def obtener_jugadores_por_seleccion():
    seleccion = request.args.get('seleccion')
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT nombre, apellido FROM jugadores WHERE nacionalidad = %s", (seleccion,))
    jugadores = [{"nombre": f"{fila[0]} {fila[1]}"} for fila in cursor.fetchall()]
    cursor.close()

    return jsonify(jugadores)

# Ruta para obtener y mostrar estadísticas de un jugador específico
@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    # Obtener selecciones desde la base de datos
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT nacionalidad FROM jugadores")
    selecciones = [row[0] for row in cursor.fetchall()]
    cursor.close()

    # Procesamiento del jugador si está seleccionado
    nombre_completo = request.args.get('jugador')
    
    if not nombre_completo:
        return render_template('estadisticas.html', selecciones=selecciones, error="No se proporcionó un jugador. Selecciona uno para ver sus estadísticas.")

    try:
        nombre, apellido = nombre_completo.split()
    except ValueError:
        return render_template('estadisticas.html', selecciones=selecciones, error="El formato del nombre es incorrecto.")

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM estadisticas WHERE nombre = %s AND apellido = %s", (nombre, apellido))
    stats = cursor.fetchone()
    cursor.close()

    if stats:
        estadisticas={
            "velocidad": stats[4],
            "aceleracion": stats[5],
            "definicion": stats[6],
            "posicion_ataque": stats[7],
            "potencia": stats[8],
            "tiros_lejanos": stats[9],
            "penaltis": stats[10],
            "voleas": stats[11],
            "vision": stats[12],
            "centros": stats[13],
            "precision_faltas": stats[14],
            "pases_largos": stats[15],
            "pases_cortos": stats[16],
            "efecto": stats[17],
            "agilidad": stats[18],
            "equilibrio": stats[19],
            "reflejo": stats[20],
            "compostura": stats[21],
            "control_de_balon": stats[22],
            "regates": stats[11],
            "intercepciones": stats[23],
            "presición_de_cabeza": stats[24],
            "conciencia_defensiva": stats[25],
            "robo": stats[26],
            "entrada_agresiva": stats[27],
            "salto": stats[28],
            "resistencia": stats[29],
            "fuerza": stats[30],
            "agresividad": stats[31],
            "estirada": stats[32],
            "paradas": stats[33],
            "saques": stats[34],
            "colocación": stats[35],
            "reflejos": stats[36],
        }
        return jsonify(estadisticas)
    else:
        return render_template('estadisticas.html', error="No se encontraron estadísticas para el jugador especificado.")

# Ruta para la página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para la página de selecciones
@app.route('/selecciones')
def selecciones():
    return render_template('selecciones.html')

if __name__ == '__main__':
    app.run(port=3000,debug=True)