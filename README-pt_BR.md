# Book API <img src="static/img/book.svg"> — see in [🇺🇸](README.md)

Este repositório implementa um exemplo de uma API Web, utilizando o microframework [Flask](https://flask.palletsprojects.com/), com o intuito de gerenciar o [CRUD](https://pt.wikipedia.org/wiki/CRUD) para um sistema de livrarias. O serviço utiliza um banco de dados [SQLite](https://www.sqlite.org/) que é construído a partir do mapeamento da classe [Book](#objeto) via [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/). O banco é criado na primeira execução do servidor.

*OBS: Este é um produto criado apenas para fins educativos*

## Como rodar o BookAPI

Para rodar o **BookAPI** é recomendável que você crie primeiro um ambiente virtual ([*virtualenv*](https://virtualenv.pypa.io/en/latest/user_guide.html)) para que as bibliotecas utilizadas neste exemplo não interfiram na configuração de bibliotecas padrões do seu sistema.

### Preparando um ambiente virtual (*virtualenv*)

1) Antes de tudo você irá instalar via `pip` a ferramenta `virtualenv`.
```bash
pip install virtualenv
```

2) Após a instalação, crie no diretório deste repositório o seu ambiente virtual. Aqui o nome escolhido foi `.venv`:
```bash
virtualenv .venv
```

3) Para ativar o ambiente virtual, utilize um dos comandos abaixo.

```bash
# linux / mac
source .venv/bin/activate

# windows
...
.\.venv\Scripts\activate
```

- *OBS: Esse passo deverá ser repetido toda vez em que se desejar utilizar o ambiente criado para este repositório.*

4) Para se certificar de que o ambiente foi ativado verifique se no início da linha de comando há a presença do termo `(.venv)`, como no exemplo:

```bash
(.venv) user@linux:~/BookAPI$ 
```

### Instalando dependências via *pip*

Instale as bibliotecas necessárias para rodar **BookAPI** com a linha de comando abaixo. Caso esteja utilizando uma [ambiente virtual](#preparando-um-ambiente-virtual-virtualenv), certifique-se antes de existir na linha de comando o termo `(.venv)`.

```bash
pip install -r requirements.txt
```

### Executando

A linha abaixo inicia o servidor em *modo debugging*. Caso esteja utilizando uma [ambiente virtual](#preparando-um-ambiente-virtual-virtualenv), certifique-se antes de existir na linha de comando o termo `(.venv)`.

```bash
flask run --debug
```

## Documentação da API

### Objeto

A classe [Book](app.py) em Python e a sua representação em JSON:

```python
class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    soldout = db.Column(db.Boolean, nullable=False)
    ...
```

```JSON
{
    "id": 1,                       // integer
    "title": "Um título de livro", // string
    "price": 19.99,                // float
    "soldout": false               // boolean
}
```

### Rotas

#### Index

Retorna um HTML com funcionalidades de visualização dos livros.

```plain
Route: /
Method: GET
Input: None
Output: html
```

* Saída:

<img style="border-radius: 5px" src="screenshots/ss-01.png">

#### Get Books

Retorna um Array de JSON contendo todos os livros cadastrados na base de dados.

```plain
Route: /get-books
Method: GET
Input: None
Output: JSON Array
```

* Exemplo de saída:
```json
[
    {
        "id": 1,
        "price": 50.0,
        "soldout": false,
        "title": "Neno Vasco por Neno Vasco: fragmentos autobiográficos de um anarquista"
    },
    {
        "id": 2,
        "price": 38.9,
        "soldout": false,
        "title": "Harry Potter e a Pedra Filosofal"
    },
    {
        "id": 3,
        "price": 39.15,
        "soldout": true,
        "title": "O Meu Pé de Laranja Lima"
    },
    {
        "id": 4,
        "price": 29.9,
        "soldout": false,
        "title": "Vidas secas"
    }
]
```

#### Insert Books

Fornece um meio de inserção de novos livros na base de dados.

```plain
Route: /new-book
Method: POST
Input: JSON
Output: Status 200
```

* Exemplo de entrada:
```json
{
    "title": "Vidas secas",
    "price": 29.9
}
```

#### Delete Books

Fornece um meio de remoção de livros da base de dados.

```plain
Route: /del-book/<id>
Method: DELETE
Input: <id>
Output: Status 200
Error: Status 204 if book not found
```

* Exemplo de entrada: `http://127.0.0.1/del-book/2`

#### Update Book

Fornece um meio de atualizar todos os dados de um determinado livro na base de dados. 
 - Retorna JSON do livro atualizado.
 - Retorna 204 se o livro não for encontrado.

```plain
Route: /update-book/<id>
Method: PUT
Input: JSON
Output: JSON
Error: Status 204 if book not found
```

* Exemplo de entrada:

```json
{
    "title" : "new title",  // optional
    "price" : 34.0,         // optional
    "soldout": true         // optional
}
```
*OBS: os parâmetros de entrada são opcionais. Isto é, não há necessidade de declarar todos em uma mesma requisição de update.*

#### Update Status

Atualiza o status de "vendido" (*soldout*) na base de dados.
 - Retorna JSON do livro atualizado.
 - Retorna 204 se o livro não for encontrado.

```plain
Route: /update-book/<id>/soldout/<boolval>
Method: PUT
Input: <id> & <boolval>
Output: Status 200
```

* Exemplo de entrada: `http://127.0.0.1/update-book/1/soldout/1`

*OBS: **boolval** deve ser 1 (true) ou 0 (false)*

<hr>

Autor: [Vinícius F. Maciel](https://www.viniciusfm.pro.br)