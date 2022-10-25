# acá dejaremos las funciones comunes
from flask_app import ALLOWED_EXTENSIONS
from datetime import datetime


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def agregar_codigo(nombre_imagen):
    horas = datetime.now()
    codigo = f'{horas.year}{horas.month}{horas.day}{horas.hour}{horas.minute}{horas.second}_{nombre_imagen}'
    return codigo
