# Book Review System

This is a RESTful API for a book review system built with FastAPI.

## Setup and running the application

### 1. Clone the Repository
```bash
git clone https://github.com/Aditya-Shekhar-73/assignment-fastapi3.git
cd assignment-fastapi3
```

### 2.  Install Virtual Environment (vir-env)
Assuming you have alraedy installed python 3.8.10 in your windows
```bash
python venv vir-env
```

### 3. Activate Virtual Environment and install dependencies
Open a command prompt and navigate to the root directory of the project
```bash
vir-env\Scripts\activate.bat
pip install -r app\requirements.txt
```

### 4. Running the Application
```bash
python run.py
```

### 5. Interacting with the API on browswer
You can interact with the endpoints using the Swagger UI at the following URL:

Swagger UI URL: localhost:5000/docs

### 6. Testing
Assuming you are in the root directory of the project and virtual environment is already activated
```bash
pytest -v tests\ut
```

### Endpoints
- Add a New Book: POST /addBooks/
- Submit a Review for a Book: POST /books/{book_id}/addReviews/
- Retrieve Books based upon author or publication_year: GET /getBooks/
- Retrieve All Reviews for a Specific Book: GET /books/{book_id}/getReviews/
- Update a Book: PUT /updateBook/{book_id}/
- Delete a Book: DELETE /deleteBook/{book_id}/
