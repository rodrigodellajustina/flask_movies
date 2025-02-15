import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#Configuração de Dados da base SQLITE
class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'movies.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
