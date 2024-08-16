from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

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
@app.route('/jugadores', methods=['GET', 'POST'])
def jugadores():
    cursor = mysql.connection.cursor()

    # Obtener selecciones (países) desde la base de datos
    cursor.execute("SELECT DISTINCT nacionalidad FROM jugadores")
    selecciones = [row[0] for row in cursor.fetchall()]

    jugadores = []
    jugador_info = None
    seleccion = request.form.get('country')  # Obtener el país seleccionado del formulario
    jugador_id = request.form.get('player_id')

    if seleccion:
        cursor.execute("SELECT id, nombre, apellido FROM jugadores WHERE nacionalidad = %s", (seleccion,))
        jugadores = cursor.fetchall()

    if jugador_id:
        cursor.execute("""
            SELECT nombre, apellido, edad, equipo_actual, historial_equipos, 
                   tarjetas_rojas, tarjetas_amarillas, imagen 
            FROM jugadores WHERE id = %s
        """, (jugador_id,))
        jugador_info = cursor.fetchone()

    cursor.close()
    return render_template('jugadores.html', selecciones=selecciones, jugadores=jugadores, jugador_info=jugador_info, seleccion=seleccion, jugador_id=jugador_id)

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
            "regates": stats[23],
            "intercepciones": stats[24],
            "presicion_de_cabeza": stats[25],
            "conciencia_defensiva": stats[26],
            "robo": stats[27],
            "entrada_agresiva": stats[28],
            "salto": stats[29],
            "resistencia": stats[30],
            "fuerza": stats[31],
            "agresividad": stats[32],
            "estirada": stats[33],
            "paradas": stats[34],
            "saques": stats[35],
            "colocacion": stats[36],
            "reflejos": stats[37],
        }
        return jsonify(estadisticas)
    else:
        return render_template('estadisticas.html', selecciones=selecciones, error="No se encontraron estadísticas para el jugador especificado.")

# Ruta para la página de login
@app.route('/login')
def login():
    return render_template('login.html')

# Ruta para la página de selecciones
@app.route('/selecciones')
def selecciones():
    return render_template('selecciones.html')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
