from comunidade import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_de_perfil = database.Column(database.String, default='defalt.png')
    posts = database.relationship('Post', backref='autor', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

class Post(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_de_criacao = database.Column(database.DateTime, nullable=False, default=datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800))
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

