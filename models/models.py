from app import db

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(40), nullable=False)
    console = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    imagem = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self) -> str:
        return "<Nome %r>" % self.name

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    idade = db.Column(db.String(2), nullable=False)
    senha = db.Column(db.String(20), nullable=False)

    def __repr__(self) -> str:
        return "<Nome %r>" % self.name

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comentario = db.Column(db.String(250), nullable=False)

    def __repr__(self) -> str:
        return "<comentario %r>" % self.comentario


