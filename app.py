import math
from flask import Flask, jsonify, render_template, request;

import forms

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"


@app.route('/Alumnos', methods=['GET', 'POST'])
def alumnos():  
        mat = 0
        nom = ""
        ape = ""
        em = ""
        alumnos_clase = forms.UserForm(request.form)
        if request.method == 'POST' and alumnos_clase.validate():
            mat = alumnos_clase.matricula.data
            nom = alumnos_clase.nombre.data
            ape = alumnos_clase.apellido.data
            em = alumnos_clase.correo.data
        return render_template('alumnos.html', form=alumnos_clase,
                               mat=mat, nom=nom, ape=ape, em=em)



@app.route('/figuras', methods=['GET', 'POST'])
def figuras():
    figura = ""
    area = None
    figura_clase = forms.FiguraForm(request.form)

    if request.method == 'POST' and figura_clase.validate():
        figura = figura_clase.figura.data
        if figura == "triangulo":
            area = (figura_clase.base.data * figura_clase.altura.data) / 2
        elif figura == "rectangulo":
            area = figura_clase.base.data * figura_clase.altura.data
        elif figura == "circulo":
            area = 3.1416 * figura_clase.radio.data ** 2
        elif figura == "cuadrado":
            area = figura_clase.lado.data ** 2
        elif figura == "pentagono":
            apotema = figura_clase.lado.data / (2 * math.tan(math.pi / 5))
            area = (5 / 2) * figura_clase.lado.data * apotema

    return render_template('figuras.html', form=figura_clase, figura=figura, area=area)


@app.route('/index')
def index():

        titulo = "Página de Inicio"
        listado=["Operación 1", "Operación 2", "Operación 3", "Operación 4"]

        return render_template('index.html', titulo=titulo, listado=listado)




@app.route('/operas', methods=['GET', 'POST'])
def operas():


    if request.method == 'POST':
        x1 = request.form.get('numero1', type=int)
        x2 = request.form.get('numero2', type=int)
        resultado =  x1 + x2
        return render_template('operas.html', resultado=resultado)

    return render_template('operas.html')




@app.route('/distancia')
def distancia():
    return render_template('distancia.html')



@app.route('/about')
def about():
    return "This is the about page."



@app.route('/user/<string:user>')
def user(user):
    return "Hola " + user


@app.route('/user/<int:n>')
def numero(n):
    return "Numero: {}".format(n)

@app.route("/user/<int:id>/<string:username>")
def user_profile(id, username):
    return "User ID: {}, Username: {}".format(id, username)

@app.route("/suma/<float:a>/<float:b>")
def func(a, b):
    return "La suma de {} y {} es {}".format(a, b, a + b)


@app.route("/prueba")
def prueba():
    return '''
    <html>
        <head>
            <title>Prueba</title>
        </head>
        <body>
            <h1>Hola desde una página HTML</h1>
            <p>Esta es una página de prueba.</p>
            <p>Otro párrafo de prueba.</p>

            <form action="/submit" method="post">
                <label for="name">Nombre:</label>
                <input type="text" id="name" name="name">
                <input type="submit" value="Enviar">
            </form>

            <p>Este es un párrafo después del formulario.</p>
            <p>Otro párrafo después del formulario.</p>
            <p>Y otro párrafo después del formulario.</p>


        </body>
    
    </html>

    
'''

if __name__ == '__main__':
    app.run(debug=True)

