from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Harry Potter', 'author': 'J. K. Rowling', 'category': 'Fantasy'},
    {'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'category': 'Fantasy'},
    {'title': '1984', 'author': 'George Orwell', 'category': 'Dystopian'},
    {'title': 'Dune', 'author': 'Frank Herbert', 'category': 'Science Fiction'},
    {'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'category': 'Romance'},
    {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'category': 'Historical Fiction'},
    {'title': 'Fahrenheit 451', 'author': 'Ray Bradbury', 'category': 'Dystopian'},
    {'title': 'Moby Dick', 'author': 'Herman Melville', 'category': 'Adventure'},
    {'title': 'Brave New World', 'author': 'Aldous Huxley', 'category': 'Science Fiction'},
    {'title': 'The Catcher in the Rye', 'author': 'J.D. Salinger', 'category': 'Literary Fiction'},
    {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald', 'category': 'Classics'},
    {'title': 'War and Peace', 'author': 'Leo Tolstoy', 'category': 'Historical Fiction'},
    {'title': 'The Chronicles of Narnia', 'author': 'C.S. Lewis', 'category': 'Fantasy'},
    {'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'category': 'Thriller'},
    {'title': 'The Alchemist', 'author': 'Paulo Coelho', 'category': 'Philosophical'},
    {'title': 'Alice in Wonderland', 'author': 'Lewis Carroll', 'category': 'Fantasy'},
    {'title': 'Anne of Green Gables', 'author': 'L.M. Montgomery', 'category': 'Young Adult'},
    {'title': 'Dracula', 'author': 'Bram Stoker', 'category': 'Horror'},
    {'title': 'The Hunger Games', 'author': 'Michael Crichton', 'category': 'Dystopian'},
    {'title': 'Jurassic Park', 'author': 'Michael Crichton', 'category': 'Science Fiction'},
]

@app.get("/books")   
async def read_all_books():
    return BOOKS

# @app.get("/books/mybook")   
# async def read_all_books():
#     return {'title': 'My Book', 'author': 'Me'}

@app.get("/books/{book_title}")  
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
  

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
       if book.get('category').casefold()==category.casefold():
            books_to_return.append(book)
    return books_to_return

#Create a new API Endpoint that can fetch all books from a specific author using either Path Parameters or Query Parameters.

@app.get("/books/fetch_author/{book_author}")
async def fetch_author_path(book_author: str):
    books_to_return = []
    for book in BOOKS:
       if book.get('author').casefold()==book_author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/by_author/")
async def fetch_author_query(book_author: str):
    books_to_return = []
    for book in BOOKS:
       if book.get('author').casefold()==book_author.casefold():
            books_to_return.append(book)
    return books_to_return



@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
       if book.get('author').casefold()==book_author.casefold() and \
                book.get('category').casefold()==category.casefold():
            books_to_return.append(book)

    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book = Body(...)):
    BOOKS.append(new_book)
    return new_book

@app.put("/books/update_book/")
async def update_book(updated_book = Body(...)):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return updated_book

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            return {'message': 'Book deleted'}
        
