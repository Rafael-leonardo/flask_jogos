import os
from app import app, db
from wtforms import StringField, SubmitField, PasswordField, validators, EmailField, FileField
from flask_wtf import FlaskForm
from models.models import Jogos

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    descricao = StringField('descricao', [validators.DataRequired(), validators.Length(min=1, max=200)])
    imagem = FileField('Imagem')
    salvar = SubmitField('Salvar')

class FormularioCadastro(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=20)])
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    email = EmailField('Email', [validators.DataRequired(), validators.Length(min=1, max=150)])
    idade = StringField('Idade', [validators.DataRequired(), validators.Length(min=1, max=2)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=24)])
    cadastro = SubmitField('Cadastro')

class FormularioUsuario(FlaskForm):
    email = EmailField('Email', [validators.DataRequired(), validators.Length(min=1, max=150)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=24)])
    login = SubmitField('Login')

class FormularioComentario(FlaskForm):
    comentario = StringField('Comentario', [validators.Length(min=1, max=250)])
    comentar = SubmitField('Comentar')

def recupera_imagem():
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        list_id = db.session.query(Jogos.id).all()
        for jogo_id in list_id:
            print(jogo_id[0])
            if f'capa{jogo_id}' in nome_arquivo:
                return nome_arquivo
        return 'capa_padrao.webp'

def recupera_imagem2():
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
            if f'capa{id}' in nome_arquivo:
                return nome_arquivo
            return 'capa_padrao.webp'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.webp':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
