import os
import pandas as pd
from models.movie import Movie
from models.database import db

#Função para carregar os filmes do csv para uma base SQLITE
def load_movies_from_csv(csv_path):
    # Verifica se o arquivo existe
    if not os.path.exists(csv_path):
        print(f"Arquivo {csv_path} não encontrado.")
        return "CSV_NAO_ENCONTRADO"  # Sinaliza que não encontrou o arquivo

    try:
        df = pd.read_csv(csv_path, sep=";")
    except Exception as e:
        print(f"Erro ao ler o CSV: {e}")
        return "CSV_LEITURA_ERRO"

    # Define as colunas esperadas (podem ser ajustadas conforme sua classe)
    expected_columns = {"year", "title", "studios", "producers", "winner"}

    # Verifica se todas as colunas esperadas estão presentes
    if not expected_columns.issubset(df.columns):
        return "CSV_INVALIDO"

    # Se tudo estiver correto, persiste os dados
    for _, row in df.iterrows():
        #PTBR - Tratamento para verificação de dados nulos do winner
        #EN   -
        winner = row.get("winner", "")
        winner = None if pd.isna(winner) else winner.strip() or None
        movie = Movie(
            year=row["year"],
            title=row["title"],
            studios=row["studios"],
            producers=row["producers"],
            winner=winner
        )
        db.session.add(movie)

    db.session.commit()
    print("Dados dos filmes carregados com sucesso!")
    return True
