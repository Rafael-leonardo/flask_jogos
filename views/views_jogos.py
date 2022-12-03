from flask import render_template, request, redirect, flash, session, url_for, send_from_directory
from app import app, db
from models.models import Jogos, Comentario
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo, FormularioComentario
import time

@app.route('/')
def index():    
    lista = Jogos.query.order_by(Jogos.nome)
    capa_jogo = recupera_imagem(1)
    return render_template('lista.html', titulo='Jogos', jogos=lista, capa_jogo=capa_jogo)

@app.route('/novo_jogo')
def novo_jogo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo_jogo')))
    
    form = FormularioJogo()

    return render_template('novo_jogo.html', titulo='Novo Jogo', form=form)

@app.route('/jogo/<int:id>', methods=["POST", "GET"])
def jogo_page(id):
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    form = FormularioComentario()
    return render_template('jogo_page.html', titulo='Editar Jogo', id=id, capa_jogo=capa_jogo, jogo=jogo, form=form)


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    jogo = Jogos.query.filter_by(id=id).first()

    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editar Jogo', id=id, capa_jogo=capa_jogo, form=form)

@app.route('/comentar/<int:id>')
def comentar(id):
    form = FormularioComentario(request.form)
    comentario = form.comentario.data
    
    novo_comentario = Comentario(comentario=comentario, jogo_id=id)
    
    db.session.add(novo_comentario)
    db.commit()
    
    return redirect(url_for('index'))


@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data

        db.session.add(jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH'] 
        timestamp = time.time()
        deleta_arquivo(jogo.id)
        arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpeg')

    return redirect(url_for('index'))

@app.route("/deletar<int:id>")
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login',))

    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash("O jogo foi deletado com sucesso!")

    return redirect(url_for('index'))

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo_jogo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data 
    
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash("O jogo ja existe!")
        return redirect(url_for("index"))
    

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)

    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f"{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg")

    return redirect(url_for('index'))

@app.route('/updloads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

