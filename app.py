from flask import Flask, render_template
from config import Config
from models.database import db
from views.routes import movie_bp
from controllers.movie_controller import load_movies_from_csv
from models.movie import Movie
import os
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
app.config.from_object(Config)

def remove_db_file():
    db_path = os.path.join(app.root_path, "movies.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Arquivo movies.db removido")

##Sempre Remove o db para carregar do movies.csv
remove_db_file()

db.init_app(app)

with app.app_context():

    #Criação da tabela baseado no modelo defino na classe
    db.create_all()

    # Se o banco estiver vazio, tentar carregar os dados do CSV
    if Movie.query.count() == 0:
        csv_status = load_movies_from_csv("movies.csv")
        app.config["CSV_STATUS"] = csv_status
    else:
        app.config["CSV_STATUS"] = True

# Rota raiz indica carregamento da base de dadosd
@app.route("/")
def index():
    csv_status = app.config.get("CSV_STATUS", True)
    if csv_status != True:
        # Define mensagens de erro de acordo com o status
        # Tratametno realizado caso não seja possível carregar os dados
        if csv_status == "CSV_NAO_ENCONTRADO":
            error_message = "O arquivo movies.csv não foi encontrado."
        elif csv_status == "CSV_INVALIDO":
            error_message = "O arquivo movies.csv não está respeitando o padrão esperado. \n\n Padrão: \n Colunas [{'year', 'title', 'studios', 'producers', 'winner'}] \n Delimitador ';' "
        elif csv_status == "CSV_LEITURA_ERRO":
            error_message = "Ocorreu um erro ao ler o arquivo movies.csv."
        else:
            error_message = "Erro desconhecido ao carregar o CSV."

        return render_template("error.html", error_message=error_message)

    return render_template("index.html")  # Sua página principal

app.register_blueprint(movie_bp)

if __name__ == "__main__":
    app.run()