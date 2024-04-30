import os

SECRET_KEY = "secreto"

SQLALCHEMY_DATABASE_URI = 'sqlite:///banco_de_dados.db'
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB



UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\uploads"