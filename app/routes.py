from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append({
                "id": book.id,
                "title": book.title,
                "description": book.description
            })
        return jsonify(books_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title=request_body["title"],
                    description=request_body["description"])
    
        db.session.add(new_book)
        db.session.commit()
        return make_response(f"Book {new_book.title} successfully created", 201)

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def book(book_id):
    if book == None:
        return {"Message": "Book does not exist!"}, 404

    if request.method == "GET":
        title_from_url = request.args.get("title")
        if title_from_url:
            books = Book.query.filter_by(title = title_from_url)
        else:
            books = Book.query.all()
        return {
        "id": book.id,
        "title": book.title,
        "description": book.description
        }
    elif request.method == "PUT":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return {
                "Message": "Request requires both a title and a description."
            }, 400

        book.title = request_body["title"]
        book.description = request_body["description"]
        # Save Action
        db.session.add(book)
        db.session.commit()
        return {
            "id": book.id,
            "title": book.title,
            "description": book.description
            }, 200
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return {
            "Message": f"Book with id {book_id} has been deleted."
        }, 200


# Get and Post Authors
@authors_bp.route("", methods=["GET", "POST"])
def handle_authors():
    if request.method == "GET":
        authors = Author.query.all()
        authors_response = []
        for author in authors:
            authors_response.append({
                "id": author.id,
                "name": author.name
            })
        return jsonify(authors_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_author = Author(name = request_body["name"])
        
        db.session.add(new_author)
        db.session.commit()
        return make_response(f"Book {new_author.name} successfully created", 201)

@authors_bp.route("/<author_id>/books", methods=["GET", "POST"])
def handle_authors_books(author_id):
    author = Author.query.get(id=author_id)
    if author is None:
        return make_response("Author not found", 404)

    if request.method == "POST":
        request_body = request.get_json()
        new_book = Book(
            title=request_body["title"],
            description=request_body["description"],
            author=author
            )
    elif request.method == "GET":
        books_response = []
        for book in author.books:
            books_response.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description
                    }
        )
        return jsonify(books_response)
        
    db.session.add(new_book)
    db.session.commit()
    return make_response(f"Book {new_book.title} by {new_book.author.name} successfully created", 201)