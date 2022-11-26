from comunidade import app, database, bcrypt
from flask import render_template, url_for, request, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required
from .forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormConfirmarDeletePost
from comunidade.models import Usuario, Post
from datetime import datetime
import secrets, os
from PIL import Image


@app.route('/')
def homepage():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('homepage.html', posts=posts)

@app.route('/login', methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()
    if form_login.validate_on_submit() and 'submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.remember.data)
            flash('Login feito com sucesso, bem vindo(a) {}'.format(form_login.email.data), 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            return redirect(url_for('homepage'))
        else:
            flash('Email/Senha incorretos, verifique as informações e tente novamente...'.format(form_login.email.data), 'alert-danger')

    if form_criar_conta.validate_on_submit() and 'submit_criar_conta' in request.form:
        senha_bcrypt = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha_bcrypt)
        database.session.add(usuario)
        database.session.commit()
        flash('Conta criada com sucesso, bem vindo(a) {}'.format(form_criar_conta.email.data), 'alert-success')
        return redirect(url_for('homepage'))
        
    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)

@app.route('/contato')
def contato():
    return 'Qualquer dúvida entre em contato pelo email suporte@github.com'

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso', 'alert-success')
    return redirect(url_for('homepage'))

@app.route('/perfil')
@login_required
def perfil():
    foto_de_perfil = url_for('static', filename='img/fotos_de_perfil/{}'.format(current_user.foto_de_perfil))
    numero_de_cursos = "0" if "Não" in current_user.cursos else str(len(current_user.cursos.split(';')))
    numero_de_posts = str(len(current_user.posts))
    return render_template('perfil.html', foto_de_perfil=foto_de_perfil, numero_de_cursos=numero_de_cursos, numero_de_posts=numero_de_posts)

#$ FUNCTIONS: /perfil/editar
def salvar_foto_de_perfil(foto_de_perfil):
    token_hex = secrets.token_hex(8)
    nome, extensao = os.path.splitext(foto_de_perfil.filename)
    nome_arquivo = nome+token_hex+extensao
    caminho_completo = os.path.join(app.root_path, 'static/img/fotos_de_perfil', nome_arquivo)
    tamanho = (200, 200)
    foto_de_perfil_reduzida = Image.open(foto_de_perfil)
    foto_de_perfil_reduzida.thumbnail(tamanho)
    foto_de_perfil_reduzida.filename= nome_arquivo
    foto_de_perfil_reduzida.save(caminho_completo)
    return nome_arquivo
def atualizar_cursos(form_editar_perfil):
    lista_de_cursos = []
    for campo in form_editar_perfil:
        if 'curso_' in campo.name and campo.data == True:
            lista_de_cursos.append(campo.label.text)
    if len(lista_de_cursos) == 0:
        return 'Não Informado'
    else:
        return ';'.join(lista_de_cursos)
            
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    foto_de_perfil = url_for('static', filename='img/fotos_de_perfil/{}'.format(current_user.foto_de_perfil))
    form_editar_perfil = FormEditarPerfil()
    numero_de_cursos = "0" if "Não Informado" in current_user.cursos else str(len(current_user.cursos.split(';')))
    numero_de_posts = str(len(current_user.posts))

    
    if form_editar_perfil.validate_on_submit():
        if form_editar_perfil.username.data != '' and current_user.username != form_editar_perfil.username.data:
            current_user.username = form_editar_perfil.username.data
        current_user.email = form_editar_perfil.email.data
        if form_editar_perfil.foto_de_perfil.data:
            nome_da_imagem = salvar_foto_de_perfil(form_editar_perfil.foto_de_perfil.data)
            current_user.foto_de_perfil = nome_da_imagem
        current_user.cursos = atualizar_cursos(form_editar_perfil)
        
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form_editar_perfil.username.data = current_user.username
        form_editar_perfil.email.data = current_user.email
        lista_de_cursos = current_user.cursos.split(';')
        for campo in form_editar_perfil:
            if 'curso_' in campo.name and campo.label.text in lista_de_cursos:
                campo.data = True
            
    
    return render_template('editar_perfil.html', foto_de_perfil=foto_de_perfil, form_editar_perfil=form_editar_perfil, numero_de_cursos=numero_de_cursos, numero_de_posts=numero_de_posts)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criar_post = FormCriarPost()
    if form_criar_post.validate_on_submit():
        post = Post(titulo=form_criar_post.titulo.data, corpo=form_criar_post.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('homepage'))

        
    return render_template('criar_post.html', form_criar_post=form_criar_post)


@app.route('/usuarios')
@login_required
def usuarios():
    lista_de_usuario = Usuario.query.all()
    return render_template('usuarios.html', lista_de_usuario=lista_de_usuario)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    form_criar_post = FormCriarPost()
    form_confirmar_delete_post = FormConfirmarDeletePost()
    if post:
        if request.method == 'GET':
            if post.autor.email == current_user.email:
                form_criar_post.titulo.data = post.titulo
                form_criar_post.corpo.data = post.corpo
                form_criar_post.submit_criar_post.label.text = 'Concluir Edição'
        if request.method == 'POST':
            if form_criar_post.validate_on_submit():
                post.titulo = form_criar_post.titulo.data
                post.corpo = form_criar_post.corpo.data
                post.data_de_criacao = datetime.fromtimestamp(datetime.utcnow().timestamp() - 10800)
                flash('Post editado com sucesso','alert-success')
                database.session.commit()
                #flash('Post ediatdo com sucesso', 'alert-success')
                return redirect(url_for('homepage'))
            
            if form_confirmar_delete_post.validate_on_submit():
                if form_confirmar_delete_post.deleteField.data == 'deletar':
                    database.session.delete(post)
                    database.session.commit()
                    flash('Seu post foi excluido com sucesso...', 'alert-success')
                    return redirect(url_for('homepage'))
                else:
                    flash('Não foi possivel excluir o post, você não digitou "deletar"', 'alert-danger')
                    return redirect(url_for('exibir_post', post_id=post.id))
                    
        return render_template('post.html', post=post, form_criar_post=form_criar_post, form_confirmar_delete_post=form_confirmar_delete_post)
    flash('Post não encontrado...', 'alert-danger')
    return redirect(url_for('homepage'))

@app.route('/perfil/<username>')
@login_required
def exibir_perfil(username):
    usuario = Usuario.query.filter_by(username=username).first()
    if usuario:
        return render_template('exibir_perfil.html', usuario=usuario)
    flash('Usuario "{}" não encontrado...'.format(username), 'alert-danger')
    return redirect(url_for('homepage'))


