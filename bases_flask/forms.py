from wtforms import DateField, Form, StringField, IntegerField, EmailField, SubmitField, RadioField, validators, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange
import math
from wtforms import Form, StringField, IntegerField, RadioField, validators
from wtforms.fields import EmailField, DateField

class UserForm(Form):
    matricula = IntegerField('Matrícula', [
        validators.DataRequired(message="La matrícula es obligatoria."),
        validators.NumberRange(min=1000, max=9999, message="Debe estar entre 1000 y 9999.")
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message="El nombre es obligatorio."),
        validators.Length(min=2, max=100)
    ])
    apellido = StringField('Apellido', [
        validators.DataRequired(message="El apellido es obligatorio."),
        validators.Length(min=2, max=100)
    ])
    correo = EmailField('Correo', [
        validators.DataRequired(message="El correo es obligatorio."),
        validators.Email(message="Correo inválido.")
    ])

class FiguraForm(Form):
    figura = RadioField('Figura', choices=[
        ('triangulo', 'Triángulo'),
        ('cuadrado', 'Cuadrado'),
        ('circulo', 'Círculo'),
        ('rectangulo', 'Rectángulo'),
        ('pentagono', 'Pentágono')
    ], validators=[validators.DataRequired(message="Selecciona una figura.")])

    base = IntegerField('Base')
    altura = IntegerField('Altura')
    radio = IntegerField('Radio')
    lado = IntegerField('Lado')
    submit = SubmitField('Calcular')

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        errores = False
        if self.figura.data in ['triangulo', 'rectangulo']:
            if not self.base.data or self.base.data <= 0:
                self.base.errors.append("La base debe ser positiva.")
                errores = True
            if not self.altura.data or self.altura.data <= 0:
                self.altura.errors.append("La altura debe ser positiva.")
                errores = True
        elif self.figura.data == 'circulo':
            if not self.radio.data or self.radio.data <= 0:
                self.radio.errors.append("El radio debe ser positivo.")
                errores = True
        elif self.figura.data in ['cuadrado', 'pentagono']:
            if not self.lado.data or self.lado.data <= 0:
                self.lado.errors.append("El lado debe ser positivo.")
                errores = True

        return not errores
    

class pizzaForm(Form):
    nombre = StringField('Nombre', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    num_pizzas = IntegerField('Número de Pizzas', validators=[DataRequired()])
    submit = SubmitField('Submit')