from flask import Flask , jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
 
from config import config
 
app = Flask(__name__)
 
conexion=MySQL(app)
CORS(app, resources={"/Alumnos/": {"origins": "*"}})

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
   


@app.route('/Alumnos',methods=['POST'])
def registrar_alumno():
    try:
        alumno=leer_alumno(request.json['matricula'])
        if alumno != None:
            return jsonify({'mensaje': 'La matrícula ya existe', "exito": False})
        else:
            cursor=conexion.connection.cursor()
            sql="""insert into alumnos (matricula, nombre, apaterno, amaterno, correo)
                   values ({0}, '{1}', '{2}', '{3}', '{4}')""".format(
                       request.json['matricula'],
                       request.json['nombre'],
                       request.json['apaterno'],
                       request.json['amaterno'],
                       request.json['correo']
                   )
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': 'Alumno registrado correctamente', "exito": True})

    except Exception as ex:
        return jsonify({'mensaje': 'Error al registrar alumno: ' + str(ex),
                        "exito": False})
    

@app.route('/Alumnos/<matricula>', methods=['PUT'])
def actualizar_curso(matricula):
        try:
            alumno = leer_alumno(matricula)
            if alumno != None:
                cursor = conexion.connection.cursor()
                sql = """UPDATE alumnos SET nombre = '{0}', apaterno = '{1}', amaterno='{2}', correo='{3}'
                WHERE matricula = {4}""".format(request.json['nombre'], request.json['apaterno'], request.json['amaterno'],request.json['correo'], matricula)
                cursor.execute(sql)
                conexion.connection.commit()  # Confirma la acción de actualización.
                return jsonify({'mensaje': "Alumno actualizado.", 'exito': True})
            else:
                return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})
        except Exception as ex:
            return jsonify({'mensaje': "Error {0} ".format(ex), 'exito': False})


@app.route('/Alumnos/<matricula>', methods=['DELETE'])

def eliminar_curso(matricula):

    try:

        alumno = leer_alumno(matricula)
        if alumno != None:

            cursor = conexion.connection.cursor()

            sql = "DELETE FROM alumnos WHERE matricula = {0}".format(matricula)

            cursor.execute(sql)

            conexion.connection.commit()  # Confirma la acción de eliminación.

            return jsonify({'mensaje': "Alumno eliminado.", 'exito': True})

        else:

            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False})

    except Exception as ex:

        return jsonify({'mensaje': "Error", 'exito': False})








def pagina_no_encontrada(error):
    return "<h1>La página que intentas buscar no existe...</h1>", 404
 
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
 