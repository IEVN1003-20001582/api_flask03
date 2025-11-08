import math
from flask import Flask, jsonify, redirect, render_template, request, url_for;
from flask import make_response, jsonify
import json
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
        estudiantes = []
        tem = []
        datos = {}

        alumnos_clase = forms.UserForm(request.form)
        if request.method == 'POST' and alumnos_clase.validate():
            mat = alumnos_clase.matricula.data
            nom = alumnos_clase.nombre.data
            ape = alumnos_clase.apellido.data
            em = alumnos_clase.correo.data
            datos = {"matricula": mat, "nombre": nom, "apellido": ape, "correo": em}

        datos_str = request.cookies.get('estudiantes')
        if not datos_str:
         return "nO HAY COOKIES"
        tem = json.loads(datos_str)
        estudiantes = tem
        print(type(estudiantes))
        estudiantes.append(datos)

        response=make_response(render_template('alumnos.html', form=alumnos_clase,
                               mat=mat, nom=nom, ape=ape, em=em))
        
        response.set_cookie('estudiantes', json.dumps(estudiantes))

        return response



@app.route('/pizzeria', methods=['GET', 'POST'])
def pizzeria():
    form = forms.PizzaForm(request.form)

    precios_tamano = {"Chica": 40, "Mediana": 80, "Grande": 120}
    precio_ingrediente = 10
 
    pedidos = json.loads(request.cookies.get('pedidos')) if request.cookies.get('pedidos') else []
    ventas_dia = json.loads(request.cookies.get('ventas')) if request.cookies.get('ventas') else []
 
    mensaje_total = None
    mostrar_ventas = False  
 
    if request.method == 'POST':
        accion = request.form.get("accion")
 
        if accion == "agregar":
            tam = request.form.get("tamannio")
            ingredientes = request.form.getlist("ingredientes")
            num = int(request.form.get("num_pizzas"))
 
            subtotal = (precios_tamano[tam] + len(ingredientes) * precio_ingrediente) * num
 
            pedidos.append({
                "tamannio": tam,
                "ingredientes": ingredientes,
                "num_pizzas": num,
                "subtotal": subtotal
            })
 
        if "quitar" in request.form and len(pedidos) > 0:
            pedidos.pop()  
 
        if accion == "terminar":
            total = sum(p["subtotal"] for p in pedidos)
            mensaje_total = f"El total de su pedido es: ${total}"
 
            venta = {
                "nombre": form.nombre.data,
                "direccion": form.direccion.data,
                "telefono": form.telefono.data,
                "total": total
            }
 
            encontrado = False
            for v in ventas_dia:
                if v["nombre"] == venta["nombre"] and v["telefono"] == venta["telefono"]:
                    v["total"] += total
                    encontrado = True
                    break
 
            if not encontrado:
                ventas_dia.append(venta)
 
            pedidos = []
 
        if accion == "ver_ventas":  
            mostrar_ventas = True
 
    total_dia = sum(v["total"] for v in ventas_dia)
 
    response = make_response(render_template(
        "Pizzeria.html",
        form=form,
        pedidos=pedidos,
        ventas_dia=ventas_dia,
        total_dia=total_dia if mostrar_ventas else None,
        mensaje_total=mensaje_total
    ))
 
    response.set_cookie('pedidos', json.dumps(pedidos))
    response.set_cookie('ventas', json.dumps(ventas_dia))
 
    return response

@app.route('/get_cookies')
def get_cookies():
    pedidos_str = request.cookies.get('pedidos')
    if not pedidos_str:
        return "nO HAY COOKIES"
    pedidos = json.loads(pedidos_str)
    return jsonify(pedidos)


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

