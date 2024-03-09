####
# To test the endpoints written for book review system.
####


def test_add_book(client):
    response = client.post("/addBooks/", json={"title": "Test Book", "author": "Test Author", "publication_year": 2022})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

def test_submit_review(client):
    book_id = 1  # Assuming book with ID 1 exists
    response = client.post(f"/books/{book_id}/addReviews/", json={"text": "Test Review", "rating": 5})
    assert response.status_code == 200
    assert response.json()["text"] == "Test Review"

def test_get_books_with_author_filter(client):
    # Assuming there are books with the author "Test Author"
    response = client.get("/getBooks/?author=Test Author")
    assert response.status_code == 200
    assert len(response.json()) > 0
    for book in response.json():
        assert book["author"] == "Test Author"

def test_get_books_with_publication_year_filter(client):
    # Assuming there are books published in the year 2022
    response = client.get("/getBooks/?publication_year=2022")
    assert response.status_code == 200
    assert len(response.json()) > 0
    for book in response.json():
        assert book["publication_year"] == 2022

def test_get_books_with_publication_year_filter(client):
    # Assuming there are books published in the year 2022
    response = client.get("/getBooks/?publication_year=2022")
    assert response.status_code == 200
    assert len(response.json()) > 0
    for book in response.json():
        assert book["publication_year"] == 2022

def test_get_book_reviews_existing_book(client):
    # Assuming there is a book with ID 1 in the database, and it has some reviews
    response = client.get("/books/1/getReviews/")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Assuming there are reviews for the book

def test_get_book_reviews_non_existing_book(client):
    # Assuming there is no book with ID 999 in the database
    response = client.get("/books/999/getReviews/")
    assert response.status_code == 404

def test_get_book_reviews_invalid_book_id(client):
    # Assuming the book_id parameter is not an integer
    response = client.get("/books/abc/getReviews/")
    assert response.status_code == 422  # Assuming FastAPI returns 422 for validation errors

def test_update_book_existing_book(client):
    # Assuming there is a book with ID 1 in the database
    book_update_data = {"title": "Updated Title", "author": "Updated Author", "publication_year": 2023}
    response = client.put("/updateBook/1/", json=book_update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["author"] == "Updated Author"
    assert response.json()["publication_year"] == 2023

def test_update_book_non_existing_book(client):
    # Assuming there is no book with ID 999 in the database
    book_update_data = {"title": "Updated Title", "author": "Updated Author", "publication_year": 2023}
    response = client.put("/updateBook/999/", json=book_update_data)
    assert response.status_code == 404

def test_update_book_invalid_book_id(client):
    # Assuming the book_id parameter is not an integer
    book_update_data = {"title": "Updated Title", "author": "Updated Author", "publication_year": 2023}
    response = client.put("/updateBook/abc/", json=book_update_data)
    assert response.status_code == 422  # Assuming FastAPI returns 422 for validation errors