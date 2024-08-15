from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos MySQL
def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="copa_america"
    )

# Ruta principal para renderizar la página de jugadores con detalles generales
@app.route('/')
def index():
    conn = conectar_bd()
    cursor = conn.cursor()

    # Obtener todos los jugadores con detalles generales
    cursor.execute("SELECT nombre, apellido, nacionalidad, peso, altura FROM jugadores")
    jugadores = cursor.fetchall()

    conn.close()
    return render_template('jugadores.html', jugadores=jugadores)

# Ruta para obtener jugadores de una selección (si quieres seguir utilizando esto en otro contexto)
@app.route('/jugadores', methods=['GET'])
def obtener_jugadores():
    seleccion = request.args.get('seleccion')

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre, apellido FROM jugadores WHERE nacionalidad = %s", (seleccion,))
    jugadores = [{"nombre": f"{fila[0]} {fila[1]}"} for fila in cursor.fetchall()]

    conn.close()
    return jsonify(jugadores)

# Ruta para obtener y mostrar estadísticas de un jugador específico
@app.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    nombre_completo = request.args.get('jugador')
    nombre, apellido = nombre_completo.split()

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM estadisticas WHERE nombre = %s AND apellido = %s", (nombre, apellido))
    stats = cursor.fetchone()

    conn.close()

    estadisticas = {
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

if __name__ == '__main__':
    app.run(debug=True)