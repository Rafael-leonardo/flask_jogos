from app import app, db, render_template, session, url_for, redirect, request, flash, send_from_directory
from models.models import Jogos, Comentario
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo, FormularioComentario
import time

@app.route('/')
def index():    
    lista = Jogos.query.order_by(Jogos.id)
    capa_jogo = recupera_imagem()
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
    capa_jogo = recupera_imagem()
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
    form.descricao.data = jogo.descricao    

    return render_template('editar.html', titulo='Editar Jogo', id=id, form=form)

@app.route('/atualizar', methods=['POST', 'GET'])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        jogo = Jogos.query.filter_by(id=request.form['id']).first()
        jogo.nome = form.nome.data
        jogo.categoria = form.categoria.data
        jogo.console = form.console.data
        jogo.descricao = form.descricao.data
        jogo.imagem = form.imagem.data

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

@app.route('/criar', methods=['POST'])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        print(form.errors)  
        return redirect(url_for('novo_jogo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    descricao = form.descricao.data
    imagem = form.imagem.data 

    jogo = Jogos.query.filter_by(nome=nome).first()

    #if form.imagem.data:
    #    if hasattr(form.imagem.data, 'filename') and hasattr(form.imagem.data, 'read'):
    #        imagem = form.imagem.data.read()  # Leia os dados binários do arquivo
    #    else:
    #       flash("Campo de imagem não é um arquivo válido")
    #       return redirect(url_for('novo_jogo'))
    #else:
    #    flash("Imagem não foi enviada")
    #    return redirect(url_for('novo_jogo'))

    if jogo:
        flash("O jogo já existe!")
        return redirect(url_for("index"))

    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console, descricao=descricao, imagem=imagem)

    db.session.add(novo_jogo)
    db.session.commit()

    flash("Jogo criado com sucesso")
    return redirect(url_for('index'))


@app.route('/updloads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

