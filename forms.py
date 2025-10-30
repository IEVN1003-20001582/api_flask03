from wtforms import Form, FloatField, validators, EmailField
from wtforms import StringField, SubmitField, IntegerField, DecimalField, SelectField, RadioField, TextAreaField, PasswordField, BooleanField, DateField, DateTimeField, TimeField, FileField, FieldList, FormField

class UserForm(Form):
    matricula = IntegerField('matricula', 
                              [validators.DataRequired(message="La matrícula es obligatoria."),
                               validators.NumberRange(min=1000, max=9999, message="La matrícula debe ser un número entre 1000 y 9999.")
                      ])
    nombre = StringField('Nombre', 
                         [validators.DataRequired(message="El nombre es obligatorio."),
                          validators.Length(min=2, max=100, message="El nombre debe tener entre 2 y 100 caracteres.")
                         ])
    apellido = StringField('Apellido', 
                         [validators.DataRequired(message="El apellido es obligatorio."),
                          validators.Length(min=2, max=100, message="El apellido debe tener entre 2 y 100 caracteres.")
                         ])
    correo = EmailField('correo', 
                        [validators.DataRequired(message="El correo es obligatorio."),
                            validators.Email(message="El correo no es válido.")
                            ])
    edad = IntegerField('Edad',
                      [validators.DataRequired(message="La edad es obligatoria."),
                       validators.NumberRange(min=1, max=120, message="La edad debe estar entre 1 y 120 años.")])
    


class FiguraForm(Form):
    figura = RadioField('Selecciona la figura', choices=[
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

        figura = self.figura.data
        errores = False

        if figura in ['triangulo', 'rectangulo']:
            if self.base.data is None or self.base.data <= 0:
                self.base.errors.append("La base debe ser un número positivo.")
                errores = True
            if self.altura.data is None or self.altura.data <= 0:
                self.altura.errors.append("La altura debe ser un número positivo.")
                errores = True
        elif figura == 'circulo':
            if self.radio.data is None or self.radio.data <= 0:
                self.radio.errors.append("El radio debe ser un número positivo.")
                errores = True
        elif figura in ['cuadrado', 'pentagono']:
            if self.lado.data is None or self.lado.data <= 0:
                self.lado.errors.append("El lado debe ser un número positivo.")
                errores = True

        return not errores


   
    

    