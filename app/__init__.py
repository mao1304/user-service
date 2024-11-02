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

from app.views.user_views import domiciliario_ns
from app.views.admin_view import administrador_ns
from app.views.vehiculo_view import vehiculo_ns
from app.views.client_view import cliente_ns
from app.views.pedido_view import pedido_ns
#registro de rutas
api.add_namespace(domiciliario_ns, path='/api/v1/domi')
api.add_namespace(administrador_ns, path='/api/v1/admin')
api.add_namespace(vehiculo_ns, path='/api/v1/vehiculo')
api.add_namespace(cliente_ns, path='/api/v1/cliente')
api.add_namespace(pedido_ns, path='/api/v1/pedido')