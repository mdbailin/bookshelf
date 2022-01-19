import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_books(self):
        """Test whether we get paginated books"""
        res = self.client().get('/books')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
    
    def test_404_sent_requesting_beyond_valid_page(self):
        """tests whether a 404 error occurs if we request an invalid page"""
        res = self.client().get('/books?page=1000')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')

        self.assertEqual(res.status_code, 404)
    
    def test_update_book(self):
        """tests whether a book's rating is updated"""
        res = self.client().patch('books/5', json={'rating': 1})
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(book.format()['rating'], 1)
    
    def test_400_no_update(self):
        """tests whether a 400 error occurs if no rating is passed"""
        res = self.client().patch('books/5')
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 5).one_or_none()

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

        self.assertEqual(res.status_code, 400)

    def test_delete_book (self):
        """tests whether book can be deleted"""
        res = self.client().delete('books/4')
        data = json.loads(res.data)

        book = Book.query.filter(Book.id == 4).one_or_none()
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_book'], 4)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))

        self.assertEqual(book, None)
    
    def test_422_no_book_deleted (self):
        """tests whether a 422 error occurs if we can't delete the book"""
        res = self.client().delete('books/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_create_book (self):
        """tests whether a book is created"""

        res = self.client().post('/books', json={
            "title": "Madness and Civilization", 
            "author": "Michel Foucault", 
            "rating": 5}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))
    
    def test_422_no_book_created (self):
        """tests whether a 422 error occurs if no book is created"""

        res = self.client().post('/books/45', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'method not allowed')




# @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
#        You can feel free to write additional tests for nuanced functionality,
#        Such as adding a book without a rating, etc.
#        Since there are four routes currently, you should have at least eight tests.
# Optional: Update the book information in setUp to make the test database your own!
    def test_get_book_search_with_results(self):
        res = self.client().post("/books", json={"search": "Novel"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_books"])
        self.assertEqual(len(data["total_books"]), 3)

    def test_search_book_with_no_results(self):
        """tests whether 0 books are found for bad search query"""
        res = self.client().post('/books', json={'search': 'applejacks'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_books'], 0)
        self.assertEqual(len(data['books']), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()