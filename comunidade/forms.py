from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidade.models import Usuario
from comunidade.routes import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired()], render_kw={'placeholder':'Nome de Usuario'}) 
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)], render_kw={'placeholder':'Senha'})
    confirmar_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo("senha")], render_kw={'placeholder':'Confirmar Senha'})
    submit_criar_conta = SubmitField('Criar Conta')
    
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('email já existente na plataforma')

class FormLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder':'Email'})
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)], render_kw={'placeholder':'Senha'})
    remember = BooleanField('Me Manter Conectado')
    submit_login = SubmitField('Entrar')


class FormEditarPerfil(FlaskForm):
    username = StringField('Editar Nome de Usuario', validators=[], render_kw={'placeholder':'Novo Nome de Usuario'}) 
    email = StringField('Editar Email', validators=[Email()], render_kw={'placeholder':'Novo Email'})
    foto_de_perfil = FileField('Alterar Foto de Perfil', validators=[FileAllowed(['jpg','png'])])
    submit_editar_perfil = SubmitField('Concluir Edição')
    
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadora')
    curso_sql = BooleanField('SQL Impressionador')
    
    def validate_email(self, email):
        if current_user.email != email.data and email.data != '':
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                ValidationError('este email já existe na plataforma, tente novamente...')

class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 144)])
    corpo = TextAreaField('Escreve seu post aqui...', validators=[DataRequired()])
    submit_criar_post = SubmitField('Criar Post')

class FormConfirmarDeletePost(FlaskForm):
    deleteField = StringField(validators=[DataRequired()], render_kw={'placeholder':'digite "deletar"'})
    submitField = SubmitField('Deletar')
    
    def validate_deletefield(self, deleteField):
        print('FUNÇÃO FOI CHAMADA')
        print(deleteField.data)
        if deleteField.data != 'deletar':
            ValidationError('Informação incorreta, impossivel excluir post')
    
   


            
    



