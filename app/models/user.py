# from app import db

# class UserModel(db.Model):
#     __tablename__ = 'Users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120))
    
#     def __init__(self, username, email):
#         self.username = username
#         self.email = email

#     def __repr__(self):
#         return f"<User {self.username}>"

from app import db
from sqlalchemy.orm import relationship

# Modelo de Administrador
from app import db
from sqlalchemy.orm import relationship

# Modelo de Administrador
class AdministradorModel(db.Model):
    __tablename__ = 'administradores'
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False, unique=True)
    contraseña = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    compania = db.Column(db.String(100), nullable=False)
    # Relación con Domiciliario
    domiciliarios = relationship('DomiciliarioModel', backref='administrador', lazy=True)

# Modelo de Domiciliario
class DomiciliarioModel(db.Model):
    __tablename__ = 'domiciliarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    administrador_id = db.Column(db.Integer, db.ForeignKey('administradores.id'), nullable=False)
    # Relación con Vehiculo
    vehiculos = relationship('VehiculoModel', backref='domiciliario', lazy=True)

# Modelo de Vehiculo
class VehiculoModel(db.Model):
    __tablename__ = 'vehiculos'
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(30), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    placa = db.Column(db.String(20), unique=True, nullable=False)
    domiciliario_id = db.Column(db.Integer, db.ForeignKey('domiciliarios.id'), nullable=False)

# Modelo de Cliente
class ClienteModel(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    # Relación con Pedido
    pedidos = relationship('PedidoModel', backref='cliente', lazy=True)

# Modelo de Pedido
class PedidoModel(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    direccion_entrega = db.Column(db.String(255), nullable=False)
    direccion_salida = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    distancia = db.Column(db.Float, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    domiciliario_id = db.Column(db.Integer, db.ForeignKey('domiciliarios.id'), nullable=False)

