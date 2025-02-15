from flask import Blueprint, jsonify, request
from models.movie import Movie
from flasgger import swag_from


movie_bp = Blueprint("movie_bp", __name__)

#rota para listar filmes + documentação
@movie_bp.route("/movies", methods=["GET"])
@swag_from({
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'description': 'Número da página para paginação (padrão: 1)',
            'required': False,
            'default': 1
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de filmes cadastrados',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'description': 'Identificador único do filme'},
                        'producers': {'type': 'string', 'description': 'Nome(s) do(s) produtor(es) do filme'},
                        'studios': {'type': 'string', 'description': 'Nome do estúdio responsável pela produção do filme'},
                        'title': {'type': 'string', 'description': 'Título do filme'},
                        'winner': {'type': 'string', 'description': 'Indica se o filme foi vencedor de algum prêmio (Yes/No)'},
                        'year': {'type': 'integer', 'description': 'Ano de lançamento do filme'},
                    }
                }
            }
        },
        204: {
            'description': 'Nenhum filme encontrado'
        },
        500: {
            'description': 'Erro interno ao listar Filmes'
        }
    }
})
def get_movies():
    """
    Listagem completa de filmes da base de dados com paginação.
    """
    # Obtém o número da página dos parâmetros da query string, default 1
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Número de itens por página, pode ser parametrizado se necessário

    try:
        # Utiliza a funcionalidade de paginação do SQLAlchemy
        paginated_movies = Movie.query.paginate(page=page, per_page=per_page, error_out=False)
        movies = [movie.to_dict() for movie in paginated_movies.items]

        if not movies:
            return '', 204

        # Retorna os filmes paginados juntamente com informações de paginação
        return jsonify({
            "movies": movies,
            "page": page,
            "per_page": per_page,
            "total": paginated_movies.total,
            "pages": paginated_movies.pages
        }), 200
    except Exception as e:
        print("Erro ao listar Filmes:", str(e))
        return jsonify({"status": "Erro interno ao listar Filmes", "erro": str(e)}), 500


#Rota para listar producers e max e mim de intervalos
@movie_bp.route("/producers/intervals", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'Retorna os intervalos máximos e mínimos entre prêmios para produtores',
            'schema': {
                'type': 'object',
                'properties': {
                    'max': {
                        'type': 'array',
                        'description': 'Lista com os produtores com o maior intervalo entre prêmios',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'producer': {
                                    'type': 'string',
                                    'description': 'Nome do produtor'
                                },
                                'previousWin': {
                                    'type': 'integer',
                                    'description': 'Ano do prêmio anterior'
                                },
                                'followingWin': {
                                    'type': 'integer',
                                    'description': 'Ano do prêmio seguinte'
                                },
                                'interval': {
                                    'type': 'integer',
                                    'description': 'Intervalo de anos entre os prêmios'
                                }
                            }
                        }
                    },
                    'min': {
                        'type': 'array',
                        'description': 'Lista com os produtores com o menor intervalo entre prêmios',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'producer': {
                                    'type': 'string',
                                    'description': 'Nome do produtor'
                                },
                                'previousWin': {
                                    'type': 'integer',
                                    'description': 'Ano do prêmio anterior'
                                },
                                'followingWin': {
                                    'type': 'integer',
                                    'description': 'Ano do prêmio seguinte'
                                },
                                'interval': {
                                    'type': 'integer',
                                    'description': 'Intervalo de anos entre os prêmios'
                                }
                            }
                        }
                    }
                }
            }
        },
        204: {
            'description': 'Nenhum filme encontrado'
        },
        500: {
            'description': 'Erro interno ao listar Filmes'
        }
    }
})
def get_producers_intervals():
    """
    Produtor com o maior e menor intervalo entre dois prêmios consecutivos
    """
    try:
        # Consulta apenas os filmes vencedores (assumindo que a coluna 'winner' armazena "yes" para os vencedores)
        listwinners = Movie.query.filter(Movie.winner == "yes").all()

        if not listwinners:
            return '', 204

        return jsonify(Movie.get_producers_intervals(listwinners))
    except Exception as e:
        print("Erro ao listar produtor com maior e menor intervalo entre dois prêmios:", str(e))
        return jsonify({"status": "Erro ao listar produtor com maior e menor intervalo entre dois prêmios", "erro": str(e)}), 500
