from flask_restx import fields

def get_book_model(ns):
    """Створює Swagger-модель для книг у вказаному Namespace"""
    return ns.model('Book', {
        'id': fields.Integer(readonly=True, description='Унікальний ідентифікатор'),
        'title': fields.String(required=True, description='Назва книги', example='Кобзар'),
        'author': fields.String(required=True, description='Автор', example='Тарас Шевченко'),
        'release_year': fields.Integer(required=True, description='Рік видання', example=1840)
    })