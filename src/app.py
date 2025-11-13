from flask import Flask , jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
 
from config import config
 
app = Flask(__name__)
 
conexion=MySQL(app)
 
@app.route('/Alumnos', methods=['GET'])
def listar_alumnos():
    try:        
        cursor = conexion.connection.cursor()
        sql="SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos"
        cursor.execute(sql)
        datos=cursor.fetchall()
        alumnos=[]
        for fila in datos:
            alumno={
                'matricula': fila[0],
                'nombre': fila[1],
                'apaterno': fila[2],
                'amaterno': fila[3],
                'correo': fila[4]
            }
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Alumnos encontrados'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al listar alumnos: ' + str(ex),
                        "exito": False})
 
 
def leer_alumno(matricula):
    try:
        cursor = conexion.connection.cursor()
        sql="SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos WHERE matricula={0}".format(matricula)
        cursor.execute(sql)
        fila = cursor.fetchone()
        if fila:
            alumno={
                'matricula': fila[0],
                'nombre': fila[1],
                'apaterno': fila[2],
                'amaterno': fila[3],
                'correo': fila[4]
            }
            return alumno
        else:
            return None
    except Exception as ex:
        print('Error al leer alumno: ' + str(ex))
        return None
 
 
@app.route('/Alumnos/<matricula>', methods=['GET'])
def obtener_alumno(matricula):
    try:
        alumno = leer_alumno(matricula)
        if alumno:
            return jsonify({'alumno': alumno, 'mensaje': 'Alumno encontrado'})
        else:
            return jsonify({'mensaje': 'Alumno no encontrado', "exito": False})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al obtener alumno: ' + str(ex),
                        "exito": False})
   
 
def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe...</h1>", 404
 
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
 