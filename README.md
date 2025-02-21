[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/) ![Python](https://img.shields.io/badge/Python-3.x-blue.svg) ![Flask](https://img.shields.io/badge/Flask-3.x-red.svg) ![SQLite](https://img.shields.io/badge/SQLite-3.x-orange.svg)

# Movies (Golden Raspberry API)

A Golden Raspberry API é uma API RESTful que permite a consulta da lista de indicados e vencedores na categoria "Pior Filme" do Golden Raspberry Awards (também conhecido como Razzie Awards). A API fornece endpoints para recuperar informações históricas sobre os prêmios, incluindo o ano, os filmes indicados e o vencedor de cada edição, além de uma listagem completa e paginada sobre todos os filmes da base de dados.


## Tecnologias

* Linguagem: Python 3.10
* Framework: Flask (Flask-RESTful) 3.0.0
* Banco de Dados: SQLite 3.1.1
* ORM: SQLAlchemy 3.1.1

## 

# step by step
1️⃣
![Instalar](https://img.shields.io/badge/Install-Download-blue?style=for-the-badge&logo=download)


📌Instalar flask_movies com git

```bash
  git clone https://github.com/rodrigodellajustina/flask_movies.git  
```
2️⃣
![Configurar](https://img.shields.io/badge/Settings-%E2%9A%99-lightgrey?style=for-the-badge)

📌Criar do ambiente virtual para execução do projeto (.venv)
```bash
  cd flask_movies
  python -m venv .venv
```

📌Ativar o ambiente (.venv) para execução do projeto
```bash
  cd .venv/Scripts
  #Windows
  activate

  #Linux
  source activate
```

📌Instalar dependências e pacotes
```bash
   pip install -r requirements.txt
```

3️⃣
![Dados](https://img.shields.io/badge/Data-%F0%9F%93%9A-blue?style=for-the-badge)

📌Necessário ter um arquivo movies.csv na raiz do projeto.

Exemplo arquivo 📄movies.csv ([Baixar arquivo exemplo](http://databaseit.com.br/movies/movies.csv))

```bash
\---flask_movies    
    |   app.py
    |   config.py
    |   📄 movies.csv
    |   requirements.txt
```
4️⃣
![Execução](https://img.shields.io/badge/Run-%F0%9F%9A%94-blue?style=for-the-badge)


📌Executar o projeto com Python 🐍
```bash
   #Nativamente 

   python app.py   

   Após execução do comando acima terá o retorno de host e porta de execução,
   conform exemplo abaixo:
      
   Dados dos filmes carregados com sucesso!
   * Serving Flask app 'app'
   * Debug mode: off
   * Running on http://127.0.0.1:5000

   Em caso de sucesso a aplicação estará rodando local na porta 5000   
   
```
📌Executar o projeto com Docker 🐳
```bash
   #Docker
   
   Para execução com Docker após o clone do projeto, deverá seguir os passsos  

   #Docker
   cd flask_movies 
   docker build -t flask_movies .
   docker run -d -p 5000:5000 --name flask_movies_container flask_movies:latest
   
   # Baixar um CSV de exemplo 
   curl -o /tmp/movies.csv http://databaseit.com.br/movies/movies.csv
   
   #Copiar o arquivo csv para o container
   docker cp /tmp/movies.csv flask_movies_container:/app/movies.csv
   
   #Restart no Container
   docker stop flask_movies_container
   docker start flask_movies_container
   
   #Testar a Aplicação
   curl -i http://127.0.0.1:5000/
   
   #Resultado Esperado
   <!DOCTYPE html>
   <html lang="pt">
   <head>
       <meta charset="UTF-8">
       <title>Bem-vindo</title>
   </head>
   <body>
       <h1>Aplicação de Filmes</h1>
       <p>Bem-vindo à aplicação de filmes.</p>
       <p>Acesse <a href="/movies" target="_blank">/movies</a> para ver os filmes.</p>
       <p>Acesse <a href="/producers/intervals" target="_blank">/producers awards</a> para ver produtor com maior e menor intervalo entre dois prêmios consecutivos</p>
   </body>   
```

5️⃣
## ⚠️ Check Dados do Projeto ⚠️

Para ter certeza de que os dados foram importados com sucesso após a sua primeira execução, existe um uma rota para verificação desse status, basta acessar:

💡Acesse em [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

![](https://raw.githubusercontent.com/rodrigodellajustina/challenge-dba/refs/heads/main/img1.png)

✅Caso retorne a pagina acima, indica que os dados estão importados e API está disponível 🚀

--------------------------------------------------------------------------------------
----------------------------------------------
----------------------------------

![](https://raw.githubusercontent.com/rodrigodellajustina/challenge-dba/refs/heads/main/img2.png)

❌Caso retorne pagina acima, indica que o arquivo csv não foi salvo na raiz do projeto, é necessário ir até o passo 3️⃣ para fazer a ação de salvar o arquivo.

--------------------------------------------------------------------------------------
----------------------------------------------
----------------------------------

![](https://raw.githubusercontent.com/rodrigodellajustina/challenge-dba/refs/heads/main/img3.png)


❌Caso retorne pagina acima, indica que o arquivo está no formato incorreto, na pagina especifica qual é o padrão.

## Documentação da API

Para acesso a documentação swagger diretamente no projeto basta acessar o link:

💡Acesse em [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)


#### Retorna todos os Filmes

```http
  GET /movies
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `page` | `integer` | **Obrigatório**. Retorna Paginação de filmes |

#### Retorna produtor com o maior e menor intervalo entre dois prêmios consecutivos

```http
  GET /producers/intervals
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |


## Collection Postman

Collection Postman 📄([Baixar arquivo](http://databaseit.com.br/movies/flask_movies.postman_collection.json))


[![Run in Postman](https://run.pstmn.io/button.svg)](http://databaseit.com.br/movies/flask_movies.postman_collection.json)

## Execução de Testes

Para realização de testes de integração deverá ser utilizado pytest

```bash
  cd flask_movies\tests\integration
  pytest test_integration.py
```

