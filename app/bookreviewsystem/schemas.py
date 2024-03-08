####
## Pydantic Models
####
from pydantic import BaseModel
from typing import List



class CreateBook(BaseModel):
    title: str
    author: str
    publication_year: int


class CreateReview(BaseModel):
    text: str
    rating: int


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    publication_year: int
    reviews: List[CreateReview]


class ReviewResponse(BaseModel):
    id: int
    text: str
    rating: int
    book_id: int