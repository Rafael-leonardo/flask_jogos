from app import app, db
from flask import render_template, request, redirect, flash, session, url_for, send_from_directory
from models.models import User
from helpers import FormularioUsuario, FormularioCadastro
from flask_bcrypt import check_password_hash, generate_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    
    form = FormularioUsuario()

    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = User.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)

    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['POST', "GET"])
def cadastro():
    form = FormularioCadastro()

    return render_template('Cadastro.html', titulo='Cadastro', form=form)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    form = FormularioCadastro(request.form)

    nome = form.nome.data
    nickname = form.nickname.data
    senha = form.senha.data
    senha = generate_password_hash(senha)
    
    novo_user = User(nome=nome, nickname=nickname, senha=senha)
    db.session.add(novo_user)
    db.session.commit()

    return redirect(url_for('index'))
