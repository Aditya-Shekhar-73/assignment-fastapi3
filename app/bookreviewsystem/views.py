from fastapi import Depends, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional

from ..main import app, logger
from .database import engine, session_local, Base
from .schemas import CreateBook, CreateReview, BookResponse, ReviewResponse
from .models import Book, Review
from ..constants import Constants


Base.metadata.create_all(bind=engine)

const = Constants()


## Method to get the db session object for carrying out database operations
def get_db():
    db = session_local()

    try:
        yield db
    finally:
        db.close()

## Method to send confirmation email once review is submitted
def send_confirmation_email(review_text: str, email: str):
    # Simulated sending confirmation email
    print(f"Sending confirmation email to {email} for review: {review_text}")


@app.get("/")
def index():
    '''
    API for welcome page
    '''
    return "Welcome to my FastAPI appliction."


@app.post("/addBooks/", response_model=BookResponse)
def add_book(book: CreateBook, db: Session = Depends(get_db)):
    '''
    API To create books
    '''
    try:
        db_book = Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        logger.info(f"Added new book: {book.title} by {book.author} ({book.publication_year})")
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Unable to create book')
    return db_book


@app.post("/books/{book_id}/addReviews/", response_model=ReviewResponse)
def submit_review(book_id: int, review: CreateReview, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    '''
    API to submit review for any book and send the confirmation mail to the mentioned mail id 
    once the review is submitted.
    '''
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    try:
        db_review = Review(**review.model_dump(), book_id=book_id)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        logger.info(f"Submitted review for book ID {book_id}")
        background_tasks.add_task(send_confirmation_email, review_text=review.text, email=const.EMAIL_ID)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='Unable to submit review for the book')
    return db_review


@app.get("/getBooks/", response_model=List[BookResponse])
def get_books(author: Optional[str] = None, publication_year: Optional[int] = None, db: Session = Depends(get_db)):
    '''
    API to get all the books based upon author or publication_year
    '''
    try:
        query = db.query(Book)
        if author:
            query = query.filter(Book.author == author)
        if publication_year:
            query = query.filter(Book.publication_year == publication_year)
        return query.all()
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Unable to get reviews for the specified author or publication year")


@app.get("/books/{book_id}/getReviews/", response_model=List[ReviewResponse])
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    '''
    Retrieve all reviews for a specific book
    '''
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Book not found")
    return db_book.reviews


@app.delete("/deleteBook/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    '''
    API to delete book and reviews related to it.
    '''
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    try:
        # Delete associated reviews
        db.query(Review).filter(Review.book_id == book_id).delete()
        
        # Delete the book
        db.delete(db_book)
        db.commit()
        logger.info(f"Deleted book ID {book_id}")
        return {"message": "Book deleted successfully"}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unable to delete the book and its related reviews')


@app.put("/updateBook/{book_id}/", response_model=BookResponse)
def update_book(book_id: int, book_update: CreateBook, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    try:
        for attr, value in book_update.model_dump().items():
            setattr(db_book, attr, value)
        db.commit()
        db.refresh(db_book)
        logger.info(f"Updated book ID {book_id}: {book_update}")
        return db_book
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'Unable to update details of the book id {book_id}')
