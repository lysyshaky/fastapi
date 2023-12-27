from pydantic import BaseModel, Field
from starlette import status

from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: int = None and Field(title="id is not required")
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0, lt=3000)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Upwork",
                "author": "Yura Lysyshak",
                "description": "Upwork is the best!",
                "rating": 5,
                "published_date": 2021,
            }
        }


BOOKS = [
    Book(1, "Upwork", "Yura Lysyshak", "Upwork is the best!", 5, 2021),
    Book(2, "Me", "Yura Lysyshak", "I am the best!", 5, 2002),
    Book(3, "Dead Soul", "Yura Lysyshak", "Your thoughts make you feel bad", 3, 666),
    Book(4, "LeadGenerator", "Freelancer", "Freelance is so so populaer!", 2, 2023),
    Book(5, "WoW", "World of WarCraft ", "This is computer game", 4, 2002),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 1 else BOOKS[-1].id + 1
    # if len(BOOKS) > 0:
    #     book.id =  BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    return book


@app.put("/update_book/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/delete_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/show-by-year/")
async def show_newer_first():
    sorted_books = sorted(BOOKS, key=lambda x: x.published_date, reverse=True)

    return sorted_books


@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def published_by_year(year: int = Query(gt=0, lt=3000)):
    books_to_return = []
    for books in BOOKS:
        if books.published_date == year:
            books_to_return.append(books)
    return books_to_return
