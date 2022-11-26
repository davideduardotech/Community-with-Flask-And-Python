from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import sass

app = Flask(__name__)


#$ CODDING: CONFIGURAÇÕES DO FLASK
app.config['SECRET_KEY'] = '6*4X8&tUb7P471Ya!7Aj@gok'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça Login para acessar essa pagina'
login_manager.login_message_category = 'alert-info'

#$ CODDING: SASS
sass.compile(dirname=('comunidade\\static\\scss', 'comunidade\\static\\css'), output_style='compressed')

from comunidade import routes

