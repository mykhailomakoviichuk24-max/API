from flask import Flask
from flask_restx import Api

# Імпортуємо наш налаштований Namespace
from app.api.books import ns as books_ns

def create_app():
    app = Flask(__name__)
    
    # Ініціалізація головного API та Swagger
    api = Api(app, 
              version='1.0', 
              title='Modular Library API',
              description='API на Flask-RESTX з професійною структурою',
              doc='/docs')
    
    # Додаємо наш маршрут до головного API
    api.add_namespace(books_ns)
    
    return app