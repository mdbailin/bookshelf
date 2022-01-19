import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    @app.route('/books', methods=['GET'])
    def get_books():
        page = request.args.get('page', 1, type=int)
        start = (page -1) * BOOKS_PER_SHELF
        end = start + 8
        books = Book.query.order_by(Book.id).all()
        formatted_books = [book.format() for book in books]

        if len(formatted_books[start:end]) == 0:
            abort(404)
        
        else:
            return jsonify({
                'success': True,
                'books': formatted_books[start:end],
                'total_books': len(formatted_books)
        })


    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars

    @app.route("/books/<int:book_id>", methods=["PATCH"])
    def update_book(book_id):

        body = request.get_json()

        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)

            if "rating" in body:
                book.rating = int(body.get("rating"))

            book.update()

            return jsonify(
                {
                    "success": True,
                    "id": book_id
                }
            )

        except:
            abort(400)


    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)
            
            book.delete()

            page = request.args.get('page', 1, type=int)
            start = (page -1) * BOOKS_PER_SHELF
            end = start + 8
            books = Book.query.order_by(Book.id).all()
            formatted_books = [book.format() for book in books]

            return jsonify({
                'success': True,
                'deleted_book': book_id,
                'books': formatted_books[start:end],
                'total_books': len(Book.query.all())
            })

        except:
            abort(422)

    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.
    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()

        new_title = body.get('title', None)
        new_author = body.get('author', None)
        new_rating = body.get('rating', None)
        search = body.get('search', None)

        
        try:
            if search:
                books = Book.query.order_by(Book.id).filter(Book.title.ilike('%{}%'.format(search)))
                page = request.args.get('page', 1, type=int)
                start = (page -1) * BOOKS_PER_SHELF
                end = start + 8
                searched_books = [book.format() for book in books]

                return jsonify({
                    'success': True,
                    'books': searched_books[start:end],
                    'total_books': len(searched_books)
                })
            else:   
                book = Book(title=new_title, author=new_author, rating=new_rating)
                book.insert()

                page = request.args.get('page', 1, type=int)
                start = (page -1) * BOOKS_PER_SHELF
                end = start + 8
                books = Book.query.order_by(Book.id).all()
                formatted_books = [book.format() for book in books]

                return jsonify({
                    'success': True,
                    'book_id': book.id,
                    'books': formatted_books[start:end],
                    'total_books': len(Book.query.all())
        })
        except:
            abort(422)
    
    @app.route('/books/<int:book_id>', methods=['GET'])
    def find_book(book_id):
        book = Book.query.filter(Book.id == book_id).one_or_none()
        formatted_book = book.format()

        return jsonify({
            "success": True,
            "id": book_id,
            "title": formatted_book["title"],
            "author": formatted_book["author"],
            "rating": formatted_book["rating"]
        })


    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Not found"
            }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405
        
    return app