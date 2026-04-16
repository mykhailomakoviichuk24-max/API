# Тимчасова база даних в пам'яті
books_db = [
    {"id": 1, "title": "1984", "author": "George Orwell", "release_year": 1949}
]

class BookRepository:
    @staticmethod
    def get_all():
        return books_db

    @staticmethod
    def get_by_id(book_id):
        for book in books_db:
            if book['id'] == book_id:
                return book
        return None

    @staticmethod
    def create(data):
        new_book = {
            "id": len(books_db) + 1,
            "title": data['title'],
            "author": data['author'],
            "release_year": data['release_year']
        }
        books_db.append(new_book)
        return new_book