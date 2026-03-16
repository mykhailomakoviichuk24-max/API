from repository.book_repo import BookRepository
from schemas.book import BookStatus
from typing import Optional

class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_books(self, status: Optional[BookStatus] = None, 
                         author: Optional[str] = None, 
                         sort_by: Optional[str] = None):
        books = await self.repo.get_all()
        
        
        if status:
            books = [b for b in books if b["status"] == status]
        if author:
            books = [b for b in books if author.lower() in b["author"].lower()]
        
        
        if sort_by == "title":
            books = sorted(books, key=lambda x: x["title"].lower())
        elif sort_by == "release_year":
            books = sorted(books, key=lambda x: x["release_year"])
            
        return books

    async def get_book(self, book_id):
        
        return await self.repo.get_by_id(book_id) 

    async def add_book(self, book_data):
        return await self.repo.create(book_data)

    async def remove_book(self, book_id):
        return await self.repo.delete(book_id)