from flask import Flask, render_template, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy

# flask app init
app = Flask(__name__)
# setting sqlite URI for books.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
# database module init
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    soldout = db.Column(db.Boolean, nullable=False)
    
    @staticmethod
    def new(title:str, price:float, soldout:bool=False):
        b = Book()
        b.title = title
        b.price = price
        b.soldout = soldout
        db.session.add(b)
        db.session.commit()
    
    def toDict(self) -> dict:
        '''convert book to dictionary'''
        return {
            'id': self.id,
            'title': self.title,
            'price': self.price,
            'soldout': self.soldout
        }

@app.route('/')
def index():
    '''
        Returns a HTML page app that retrieves books from BookAPI
    '''
    return render_template('index.html') # templates/index.html

@app.route('/get-books', methods=['GET'])
def get_books():
    '''
        Retrieve all books from database.
        Returns a JSON Array.
        No body required.
    '''
    books = Book.query.all()
    ret = []
    for book in books:
        ret.append(book.toDict())
    return jsonify(ret)

@app.route('/new-book', methods=['POST'])
def new_book():
    '''
        Adds a new book to database.
        JSON may contain title (string) and price (float) values.
    '''
    jsondata = request.get_json()
    Book.new(jsondata['title'], jsondata['price'])
    return Response(status=200)

@app.route('/del-book/<id>', methods=['DELETE'])
def del_book(id:int):
    '''
        Delete a book refferred by its ID from database. 
        Returns 204 http code if book not found.
        No body required.
    '''
    book = Book.query.filter_by(id=id).first()
    if(book):
        db.session.delete(book)
        db.session.commit()
        return Response(status=200)
    return Response(status=204)

@app.route('/update-book/<id>', methods=['PUT'])
def update_book(id:str):
    '''
        Update a book refferred by its ID on database. 
        Returns 204 http code if book not found.
        JSON may contain title, price and/or soldout.
    '''
    book = Book.query.filter_by(id=id).first()
    if(book):
        jsondata = request.get_json()
        if('title' in jsondata):
            book.title = jsondata['title']
        if('price' in jsondata):
            book.price = jsondata['price']
        if('soldout' in jsondata):
            book.soldout = jsondata['soldout']
        db.session.commit()
        return jsonify(book.toDict())
    return Response(status=204)

@app.route('/update-book/<id>/soldout/<boolval>', methods=['PUT'])
def update_status(id:str, boolval:str):
    '''
        Update a book refferred by its ID on database. 
        Returns 204 http code if book not found.
        No body required.
    '''
    book = Book.query.filter_by(id=id).first()
    if(book):
        book.soldout = (boolval == '1')
        db.session.commit()
        return jsonify(book.toDict())
    return Response(status=204)

# initializes the sqlite db, if not initialized yet.
with app.app_context():
    db.create_all()
