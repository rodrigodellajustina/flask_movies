from models.database import db

#Classe principal das Filmes
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    studios = db.Column(db.String(255), nullable=False)
    producers = db.Column(db.String(255), nullable=False)
    winner = db.Column(db.String(10), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "year": self.year,
            "title": self.title,
            "studios": self.studios,
            "producers": self.producers,
            "winner": self.winner
        }

    # Método para realizar a busca pelo minimo e maximo de produtores ganhos.
    def get_producers_intervals(self):
        winners = Movie.query.filter(Movie.winner == "yes").all()

        # Dicionário para armazenar os anos de vitória para cada produtor
        producer_wins = {}

        for movie in winners:
            year = movie.year
            # A coluna 'producers' pode conter vários produtores separados por vírgula e/ou " and "
            producers_list = []
            # Primeiro, separa por vírgula
            for part in movie.producers.split(","):
                # Em seguida, separa por " and " caso exista
                for subpart in part.split(" and "):
                    producer = subpart.strip()
                    if producer:
                        producers_list.append(producer)

            for producer in producers_list:
                producer_wins.setdefault(producer, []).append(year)

        # Lista para armazenar todos os intervalos calculados
        intervals = []

        for producer, years in producer_wins.items():
            if len(years) < 2:
                continue  # Não tem intervalo se houver menos de 2 vitórias
            years.sort()
            # Calcula intervalo entre cada par consecutivo de vitórias
            for i in range(1, len(years)):
                interval = years[i] - years[i - 1]
                intervals.append({
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i - 1],
                    "followingWin": years[i]
                })

        if intervals:
            min_interval = min(item["interval"] for item in intervals)
            max_interval = max(item["interval"] for item in intervals)

            min_list = [item for item in intervals if item["interval"] == min_interval]
            max_list = [item for item in intervals if item["interval"] == max_interval]
        else:
            min_list = []
            max_list = []

        return {
            "min": min_list,
            "max": max_list
        }