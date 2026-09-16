# jsonify() allows Flask to return our Python data as a JSON response.

from flask import Flask, jsonify, request
from database import initialize_database, get_db_connection
from datetime import date
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Reading Tracker Backend is running"



    # SEARCH FOR A BOOK
@app.route("/api/books/search", methods=["GET"])
def search_book():
    title = request.args.get("title")
    if not title:
        return jsonify({
            "error": "Book title is required"
        }), 400
    url = "https://openlibrary.org/search.json"

    params = {
        "title": title
    }
    response = requests.get(url, params=params)
    print(response.status_code)
    print(response.url)
    print(response.text[:500])

    if response.status_code != 200:
        return jsonify({
            "error": "Unable to search for book"
        }), 502
    data = response.json()
    books = data.get("docs", [])

    if not books:
        return jsonify({
            "error": "No matches found"
        }), 404

    book = books[0]
    external_book_id = book.get("key", "").replace("/works/", "")
    title = book.get("title", "Unknown title")

    authors = book.get("author_name", [])
    author = authors[0] if authors else "Unknown author"

    publication_year = book.get("first_publish_year")
    cover_id = book.get("cover_i")

    cover_url = (
    f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    if cover_id
    else None
    )

    return jsonify({
    "books": [
        {
            "external_book_id": external_book_id,
            "title": title,
            "author": author,
            "cover_url": cover_url,
            "publication_year": publication_year
        }
    ]
    }), 200



#VIEW SAVED BOOKS
@app.route("/api/books", methods=["GET"])
def get_books():
    connection = get_db_connection()
    books = connection.execute("SELECT * FROM books").fetchall()
    connection.close()
    return jsonify({
        "books":[dict(book) for book in books]
    })




# SAVE A NEW BOOK
@app.route("/api/books", methods=["POST"])
def save_book():
    # Check if json contains body
    if not request.is_json:
        return jsonify({
            "error": "Request Body must contain a JSON"
        }), 400
    
    data = request.json

    # extract the values 
    external_book_id = data.get("external_book_id")
    title = data.get("title")
    author = data.get("author")
    cover_url = data.get("cover_url")
    reading_status = data.get("reading_status")

    # check if theres a missing field
    if not external_book_id or not title or not author or not cover_url or not reading_status:
        return jsonify({
            "error": "Required book information is missing"
        }), 400
    date_added = date.today().isoformat()

    # handle duplicates
    connection = get_db_connection()

    existing_book = connection.execute(
        """
            SELECT external_book_id FROM books WHERE external_book_id = ?
        """,
        (external_book_id,)
    ).fetchone()

    if existing_book:
        connection.close()
        return jsonify({
            "error": "Book already Saved"
        }), 409
    
    cursor = connection.execute(
        """
        INSERT INTO books(
            external_book_id,
            title,
            author,
            cover_url,
            reading_status,
            date_added
        )
        VALUES(? , ? , ? , ? , ? , ?)
        """,
        ( external_book_id,
            title,
            author,
            cover_url,
            reading_status,
            date_added)
    )
    connection.commit()
    book_id = cursor.lastrowid
    connection.close()
    
    return jsonify({
        "book": {
             "id": book_id,
            "external_book_id": external_book_id,
            "title": title,
            "author": author,
            "cover_url": cover_url,
            "reading_status": reading_status,
            "date_added": date_added
        }
    }), 201



#UPDATE READING STATUS OF A SAVED BOOK
@app.route("/api/books/<external_book_id>", methods=["PATCH"])
def update_reading_status(external_book_id):
    data = request.json
    new_reading_status = data.get("reading_status")

    valid_statuses = ["Want to Read", "Currently Reading", "Completed"]
    if new_reading_status not in valid_statuses:
        return jsonify({
            "error": "Invalid readind status."
        }), 400
    
    # Check if book exists in database
    connection = get_db_connection()
    book_exists = connection.execute("SELECT * FROM books WHERE external_book_id = ?", (external_book_id,)).fetchone()
    if book_exists is None:
        connection.close()
        return jsonify({
            "error": "Book not found in the reading list"
        }), 404
    
    if book_exists["reading_status"] == new_reading_status:
        connection.close()
        return jsonify({
            "error": "No changes detected. The new status matches the current status"
        }), 400

    connection.execute("UPDATE books SET reading_status = ? WHERE external_book_id = ?", (new_reading_status, external_book_id))
    connection.commit()
    connection.close()
    return jsonify({
        "book": {
            "id" : book_exists["id"],
            "reading_status": new_reading_status
        }
    }), 200




# REMOVE A SAVED BOOK
@app.route("/api/books/<external_book_id>", methods=["DELETE"])
def remove_book(external_book_id):
    connection = get_db_connection()
    book_exists = connection.execute("SELECT * FROM books WHERE external_book_id = ?",(external_book_id,)).fetchone()

    if book_exists is None:
        connection.close()
        return jsonify({
            "error": "The book was not saved in the reading list, cannot delete non-existent book."
        }), 404

    connection.execute("DELETE FROM books WHERE external_book_id = ?", (external_book_id,))
    connection.commit()
    connection.close()
    return jsonify({
        "message": "The book has been removed from the reading list."
    }), 200
    

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
    
