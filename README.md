##API Reference

### Getting Started
- Base URL: This app is only run locally and is not hosted as a base URL. The backend app is hosted at `http://127.0.0.1:5000/`, which is set as a proxy on the frontend.
- Authentication: This app does not require authentication or API keys.


### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Not found"
}

```
There are four error types the app may return when a request fails:
- 400: Bad Request
- 404: Not Found
- 405: Method Not Allowed
- 422: Unprocessable

### Endpoints
#### GET / Books
- General:
    - Returns a list of book objects, success value, and the total number of books currently in the database
    - Results are paginated in groups of 8. Includes a request argument to start at any page number (defaults to 1).
- Sample: `curl http://127.0.0.1:5000/books`

```
{
     "books": [
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 4,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 4,
      "title": "The Great Alone"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Leila Slimani",
      "id": 6,
      "rating": 2,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Gina Apostol",
      "id": 9,
      "rating": 5,
      "title": "Insurrecto: A Novel"
    },
    {
      "author": "Tayari Jones",
      "id": 10,
      "rating": 5,
      "title": "An American Marriage"
    }
  ],
  "success": true,
  "total_books": 15
}
```

#### POST /books
- General:
    - creates a new book using the submitted title, author, and rating. Returns the book id, success value, total number of books, and book list based on the new insertion to update the frontend (Note: the book is appended to the end of the book list so it should not appear on the 1st page).
    - Sample: `curl http://127.0.0.1:5000/books -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'`

```
{
    "book_id": 26,
    "books": [
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 4,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 4,
      "title": "The Great Alone"
    },
    {
      "author": "Tara Westover",
      "id": 4,
      "rating": 5,
      "title": "Educated: A Memoir"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Leila Slimani",
      "id": 6,
      "rating": 2,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Gina Apostol",
      "id": 9,
      "rating": 5,
      "title": "Insurrecto: A Novel"
    },
    {
      "author": "Tayari Jones",
      "id": 10,
      "rating": 5,
      "title": "An American Marriage"
    }
  ],
  "success": true,
  "total_books": 17
}
```
#### DELETE /books/{book_id}
- General:
    - Deletes the book of the given ID if it exists. Returns the id of the deleted book, success value, total books, and book list based on the current number of books to update the frontend.
- Sample: `curl -X DELETE http://127.0.0.1:5000/books/4'

```
{
  "books": [
    {
      "author": "Lisa Halliday",
      "id": 2,
      "rating": 4,
      "title": "Asymmetry: A Novel"
    },
    {
      "author": "Kristin Hannah",
      "id": 3,
      "rating": 4,
      "title": "The Great Alone"
    },
    {
      "author": "Jojo Moyes",
      "id": 5,
      "rating": 5,
      "title": "Still Me: A Novel"
    },
    {
      "author": "Leila Slimani",
      "id": 6,
      "rating": 2,
      "title": "Lullaby"
    },
    {
      "author": "Amitava Kumar",
      "id": 7,
      "rating": 5,
      "title": "Immigrant, Montana"
    },
    {
      "author": "Gina Apostol",
      "id": 9,
      "rating": 5,
      "title": "Insurrecto: A Novel"
    },
    {
      "author": "Tayari Jones",
      "id": 10,
      "rating": 5,
      "title": "An American Marriage"
    },
    {
      "author": "Jordan B. Peterson",
      "id": 11,
      "rating": 5,
      "title": "12 Rules for Life: An Antidote to Chaos"
    }
  ],
  "deleted_book": 4,
  "success": true,
  "total_books": 16
}
```
#### PATCH /books/{book_id}
- General:
    - If provided, updates the rating of a specific books. Returns a success value and the id of the modified book.
- Sample: `curl http://127.0.0.1:5000/books/11 -X PATCH -H "Content-Type: application/json" -d '{"rating":"4"}'`

```
{
  "id": 11,
  "success": true
}
```