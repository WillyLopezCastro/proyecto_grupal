
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.modelo_base import ModeloBase

class Noticia(ModeloBase):

    modelo = 'noticias' #nombre de la tabla
    campos = ['titulo', 'parrafo','file','date_made', 'usuario_id']

    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.parrafo = data['parrafo']
        self.file = data['file']
        self.date_made = data['date_made']
        self.usuario_id = data['usuario_id']
        self.usuario_nombre = data['nombre']
        self.usuario_apellido = data['apellido']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_with_users(cls):
        query = f"SELECT * FROM {cls.modelo} join usuarios on usuarios.id = {cls.modelo}.usuario_id;"
        results = connectToMySQL('proyecto_grupal').query_db(query)
        all_data = []
        for data in results:
            all_data.append(cls(data))
        return all_data

    @staticmethod
    def validar(user):
        is_valid = True
        if len(user['titulo']) < 3:
            is_valid = False
            flash(f'El largo del titulo no puede ser menor a 3', 'error')
        if len(user['parrafo']) < 3:
            is_valid = False
            flash(f'El largo del párrafo no puede ser menor a 3', 'error')
        if len(user['date_made']) < 9:
            is_valid = False
            flash(f'El largo del date_made no puede ser menor a 9', 'error')

        return is_valid


    @classmethod
    def update(cls,data):
        query = """UPDATE noticias 
                        SET titulo = %(titulo)s,
                        parrafo = %(parrafo)s,
                        file = %(file)s,
                        date_made = %(date_made)s,
                        updated_at=NOW() 
                    WHERE id = %(id)s"""
        resultado = connectToMySQL('proyecto_grupal').query_db(query, data)
        return resultado

    @classmethod
    def get_by_id_with_users(cls, id):
        query = f"SELECT * FROM {cls.modelo} join usuarios on usuarios.id = {cls.modelo}.usuario_id where noticias.id = %(id)s;"
        data = {'id': id}
        results = connectToMySQL('proyecto_grupal').query_db(query, data)
        all_data = []
        for data in results:
            all_data.append(cls(data))
        return all_data