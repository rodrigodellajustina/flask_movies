import pytest
from app import app, db
from models.movie import Movie

@pytest.fixture
def client():
    """
    Fixture que configura o Flask para testes,
    cria um banco de dados em memória, insere dados de teste
    e fornece um client de teste para requisições HTTP.
    """
    app.config["TESTING"] = True

    # Usa um banco de dados em memória para não afetar nada em disco
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Dados de teste (baseados na tabela fornecida, novos dados precisam gerar novos testes)
            data = [
                # (year, title, studios, producers, winner)
                (1980, "Can't Stop the Music", "Associated Film Distribution", "Allan Carr", "yes"),
                (1980, "Cruising", "Lorimar Productions, United Artists", "Jerry Weintraub", ""),
                (1980, "The Formula", "MGM, United Artists", "Steve Shagan", ""),
                (1980, "Friday the 13th", "Paramount Pictures", "Sean S. Cunningham", ""),
                (1980, "The Nude Bomb", "Universal Studios", "Jennings Lang", ""),
                (1980, "The Jazz Singer", "Associated Film Distribution", "Jerry Leider", ""),
                (1980, "Raise the Titanic", "Associated Film Distribution", "William Frye", ""),
                (1980, "Saturn 3", "Associated Film Distribution", "Stanley Donen", ""),
                (1980, "Windows", "United Artists", "Mike Lobell", ""),
                (1980, "Xanadu", "Universal Studios", "Lawrence Gordon", ""),
                (1981, "Mommie Dearest", "Paramount Pictures", "Frank Yablans", "yes"),
                (1981, "Endless Love", "Universal Studios, PolyGram", "Dyson Lovell", ""),
                (1981, "Heaven's Gate", "United Artists", "Joann Carelli", ""),
                (1981, "The Legend of the Lone Ranger", "Universal Studios, Associated Film Distribution",
                 "Walter Coblenz", ""),
                (1981, "Tarzan, the Ape Man", "MGM, United Artists", "John Derek", ""),
                (1982, "Inchon", "MGM", "Mitsuharu Ishii", "yes"),
            ]

            for row in data:
                movie = Movie(
                    year=row[0],
                    title=row[1],
                    studios=row[2],
                    producers=row[3],
                    winner=row[4]
                )
                db.session.add(movie)

            db.session.commit()

        yield client  # Fornece o client de teste para os testes

        # Cleanup: remove as tabelas
        with app.app_context():
            db.drop_all()


def test_get_movies(client):
    """
    Testa o endpoint /movies para garantir que todos os filmes inseridos sejam retornados,
    levando em conta que a resposta pode vir paginada ou conter metadados em um dicionário.
    """
    response = client.get("/movies")
    assert response.status_code == 200

    data = response.get_json()

    # Verifica se a resposta é um dicionário (pois pode conter paginação, etc.)
    assert isinstance(data, dict)

    # Se o endpoint retorna algo como {"movies": [...], "page": 1, "pages": 2, ...}
    # Verifique se a chave "movies" está presente
    assert "movies" in data

    # Verifica se "movies" é uma lista
    assert isinstance(data["movies"], list)

    # Checa se vieram 10 filmes (baseado nos dados inseridos)
    assert len(data["movies"]) == 10

    # Opcional: verificar outras chaves de paginação, se existirem
    # assert data["page"] == 1
    # assert data["pages"] == 2
    # assert data["per_page"] == 10
    # assert data["total"] == 16


def test_producers_intervals(client):
    """
    Testa o endpoint /producers/intervals (caso exista) para verificar a lógica
    de cálculo de intervalos de prêmios consecutivos.

    Observação: neste dataset, cada 'yes' pertence a um produtor diferente:
      - 1980: Allan Carr
      - 1981: Frank Yablans
      - 1982: Mitsuharu Ishii
    Então, não há nenhum produtor que tenha 2 prêmios. Logo, a lista de intervalos
    deve ficar vazia ou ter a lógica correspondente.
    """
    response = client.get("/producers/intervals")
    assert response.status_code == 200

    data = response.get_json()
    # Verifica se as chaves "min" e "max" existem
    assert "min" in data
    assert "max" in data

    # Neste dataset, não há produtor com mais de um prêmio
    # Então esperamos que "min" e "max" sejam vazios
    assert len(data["min"]) == 0
    assert len(data["max"]) == 0
