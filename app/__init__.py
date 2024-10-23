from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
# from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
api = Api(app)


# registro de los modelos en el app.
from app.models.user import AdministradorModel

from app.views.user_views import user_routes
from app.views.admin_view import administrador_ns
#registro de rutas
api.add_namespace(user_routes, path='/api/v1/users')
api.add_namespace(administrador_ns, path='/api/v1/admin')