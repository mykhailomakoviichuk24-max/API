from flask_restx import Namespace, Resource
from app.repository.book_repo import BookRepository
from app.schemas.book_schema import get_book_model

# Створюємо ізольований простір для маршрутів
ns = Namespace('books', description='Операції з книгами')

# Реєструємо схему в цьому просторі
book_model = get_book_model(ns)

@ns.route('/')
class BookList(Resource):
    
    @ns.doc('list_books')
    @ns.marshal_list_with(book_model)
    def get(self):
        """Отримати список усіх книг"""
        return BookRepository.get_all()

    @ns.doc('create_book')
    @ns.expect(book_model)
    @ns.marshal_with(book_model, code=201)
    def post(self):
        """Додати нову книгу"""
        return BookRepository.create(ns.payload), 201

@ns.route('/<int:id>')
@ns.response(404, 'Книгу не знайдено')
class BookItem(Resource):
    
    @ns.doc('get_book')
    @ns.marshal_with(book_model)
    def get(self, id):
        """Отримати книгу за її ID"""
        book = BookRepository.get_by_id(id)
        if not book:
            ns.abort(404, "Книга не знайдена")
        return book