from flask import Flask, request
from flask_restful import Resource, Api
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)

# Ініціалізація Flasgger
# Swagger буде доступний за адресою http://localhost:8000/apidocs
swagger = Swagger(app)

# Наша тимчасова база даних
books_db = [
    {"id": 1, "title": "1984", "author": "George Orwell", "release_year": 1949}
]

# Клас-ресурс для роботи зі списком книг
class BookList(Resource):
    def get(self):
        """
        Отримати список усіх книг
        ---
        tags:
          - Books
        responses:
          200:
            description: Повертає список усіх книг
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  author:
                    type: string
                  release_year:
                    type: integer
        """
        return books_db

    def post(self):
        """
        Додати нову книгу
        ---
        tags:
          - Books
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - title
                - author
                - release_year
              properties:
                title:
                  type: string
                  example: Кобзар
                author:
                  type: string
                  example: Тарас Шевченко
                release_year:
                  type: integer
                  example: 1840
        responses:
          201:
            description: Книга успішно створена
        """
        data = request.get_json()
        new_book = {
            "id": len(books_db) + 1,
            "title": data['title'],
            "author": data['author'],
            "release_year": data['release_year']
        }
        books_db.append(new_book)
        return new_book, 201

# Клас-ресурс для конкретної книги
class BookItem(Resource):
    def get(self, book_id):
        """
        Отримати книгу за її ID
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: ID книги
        responses:
          200:
            description: Дані про книгу
          404:
            description: Книгу не знайдено
        """
        for book in books_db:
            if book['id'] == book_id:
                return book
        return {"message": "Книга не знайдена"}, 404

# Прив'язка ресурсів до маршрутів
api.add_resource(BookList, '/books')
api.add_resource(BookItem, '/books/<int:book_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)