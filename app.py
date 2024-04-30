from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from views.views_jogos import *
from views.views_user import *
from models.models import Comentario, User, Jogos 

with app.app_context():
    print("Criando banco...")
    db.create_all()
    print("Banco criado com sucesso!")


if __name__ == '__main__':
    app.run(debug=True)